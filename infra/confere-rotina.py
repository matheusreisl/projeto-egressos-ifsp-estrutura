#!/usr/bin/env python3
"""
Confere a rotina agendada de disparo (E21) contra o criterio da etapa: o
disparo executa no horario e atinge so os nao respondentes.

Tres partes:

  regras     (sempre) a cadencia de scripts/cadencia.py contra casos
             construidos, sem plataforma: o estado de cada participante (secao
             12 do P5), o vencimento do convite e de cada lembrete, dia util e
             a faixa admissivel da agenda. Nao toca nada.

  --agendada o caminho real, pelo agendador de pe. Planta catorze participantes
             do instrumento, um por situacao, e aponta o agendador para um
             CICLO DE TESTE (2099) em modo real, com horario daqui a poucos
             minutos. No ciclo 2099 a ancora de todos esta no futuro, de modo
             que os outros 486 participantes nao vencem convite: sao o controle
             negativo. Espera o horario e confere que a execucao comecou nele,
             que receberam mensagem exatamente os que deviam, com o ramo certo,
             e que a janela de 60 dias foi gravada. Desfaz tudo — cada passo de
             limpeza independente dos outros — e devolve o agendador ao que o
             .env diz, sem editar o .env: os valores de teste entram pelo
             ambiente do comando, que tem precedencia sobre o arquivo.

  --perdida  um horario que passou sem execucao vira registro `perdida`. Sobe
             o agendador com o horario de hoje ja vencido alem da tolerancia,
             no ciclo de teste e em modo simulado, confere o registro e desfaz.

O que e plantado, e como:

  pelo caminho real do respondente, por HTTP, na interface: a abertura sem
  envio de pagina, o preenchimento interrompido depois da pagina 1 e as duas
  recusas — e o que mostra que o estado lido pela rotina e o que a plataforma
  produz. O formulario sem JavaScript precisa dos campos de relevancia
  (relevance<qid>, relevanceG<n>), que o navegador preencheria: sem eles a
  plataforma descarta a resposta em silencio.

  pela API: datas de envio e contadores de lembrete no passado, que e como se
  comprime o tempo sem esperar dias; o contato invalido; e a conclusao do
  respondente, porque percorrer as onze paginas e cenario da E26.

Nada sai da maquina: o correio fica so na rede interna e os enderecos estao sob
.test. Nenhum dado e de pessoa real.

Uso, a partir da pasta infra/:

    python3 confere-rotina.py                 (so as regras)
    python3 confere-rotina.py --agendada      (regras e caminho real)
    python3 confere-rotina.py --perdida       (regras e execucao perdida)
"""

import argparse
import email
import email.policy
import http.cookiejar
import importlib.util
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))
sys.path.insert(0, os.path.join(AQUI, "instrumento"))

import cadencia  # noqa: E402
import instrumento  # noqa: E402
import mensagens  # noqa: E402
from limesurvey_console import api_do_hospedeiro, carrega_env  # noqa: E402

# Os auxiliares de caixa e de banco da conferencia da E20, reaproveitados sem
# copia: o arquivo tem hifen no nome e por isso entra por importlib.
_spec = importlib.util.spec_from_file_location(
    "confere_mensagens", os.path.join(AQUI, "confere-mensagens.py"))
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)


def _insistente(funcao, tentativas=6, pausa=5):
    """A caixa, com insistencia. Num hospedeiro WSL o relogio da maquina
    virtual salta, e o Dovecot recusa login por alguns segundos depois do
    salto — observado na primeira execucao desta conferencia, com o relogio
    voltando 7 s, sem suspensao alguma. O auxiliar da E20 sai com SystemExit
    nessa recusa; aqui se tenta de novo."""
    def chamada(*args, **kwargs):
        for i in range(tentativas):
            try:
                return funcao(*args, **kwargs)
            except SystemExit:
                if i == tentativas - 1:
                    raise
                time.sleep(pausa)
    return chamada


for _nome in ("imap", "mensagens_do_token", "apaga"):
    setattr(cm, _nome, _insistente(getattr(cm, _nome)))

SID = instrumento.SID_INSTRUMENTO
ENV = carrega_env()
PORTA = ENV.get("PORTA_HTTP", "8080")
DOMINIO = ENV.get("CORREIO_DOMINIO", "egressos.test")
AGENDA = cadencia.carrega_agenda(
    os.path.join(AQUI, "rotinas", "configuracao", "agenda.json"))
FUSO = AGENDA.fuso
UTC = timezone.utc
CICLO_TESTE = "2099"
VERDE, VERMELHO, FIM = "\033[32m", "\033[31m", "\033[0m"

# Quanto o inicio registrado pode ficar ANTES do horario e ainda contar como no
# horario. O relogio da maquina virtual do WSL, que os conteineres usam, foi
# medido na E21 7,3 s atras do Windows, e corrigido aos saltos de 7 a 8 s para
# tras: um inicio "antes" do horario e o relogio sendo corrigido, e nao a rotina
# adiantada. Depois do horario, a margem e um passo do laco (20 s) com folga.
ANTES_TOLERADO, DEPOIS_TOLERADO = -30, 60

resultados = []


def registra(rotulo, falhas, evidencia=""):
    ok = not falhas
    resultados.append(ok)
    cor = VERDE if ok else VERMELHO
    print(f"  {cor}[{'ok' if ok else 'FALHA':5}]{FIM} {len(resultados)}. "
          f"{rotulo}" + (f": {evidencia}" if ok and evidencia else ""))
    for f in falhas:
        print(f"           - {f}")


# ===========================================================================
# Parte 1 — regras, sem plataforma
# ===========================================================================

# Segunda-feira, 05/10/2026, 10:00 — o horario da agenda num dia util.
AGORA = datetime(2026, 10, 5, 10, 0, tzinfo=FUSO)


def enviado(dias, horas=0, base=AGORA):
    """`sent` na forma da plataforma: UTC, AAAA-MM-DD HH:MM."""
    return (base - timedelta(days=dias, hours=horas)).astimezone(UTC) \
        .strftime("%Y-%m-%d %H:%M")


def P(tid, **kw):
    kw.setdefault("ano_conclusao", "2020")
    kw.setdefault("semestre_conclusao", "1")
    kw.setdefault("participant_id", f"pid-{tid}")
    return cadencia.Participante(tid=tid, **kw)


R = cadencia.Resposta
C = cadencia


def confere_regras():
    print("\nregras da cadencia (scripts/cadencia.py), sem plataforma")

    # --- estado: um caso por linha da secao 12, mais a precedencia ---------
    casos_estado = [
        ("pendente", P(1), C.PENDENTE),
        ("convidado", P(2, sent=enviado(1)), C.CONVIDADO),
        ("abriu sem enviar pagina (lastpage 0, CON1 vazio)",
         P(3, sent=enviado(1), respostas=[R(False, None)]), C.CONVIDADO),
        ("enviou a pagina 1 concordando",
         P(4, sent=enviado(1), respostas=[R(False, "CONC")]),
         C.EM_PREENCHIMENTO),
        ("concluiu", P(5, sent=enviado(1), completed="Y",
                       respostas=[R(True, "CONC")]), C.RESPONDENTE),
        ("concluiu, com parcial orfa ao lado",
         P(6, sent=enviado(1), completed="Y",
           respostas=[R(False, None), R(True, "CONC")]), C.RESPONDENTE),
        ("recusou o termo (marcada como concluida pela plataforma)",
         P(7, sent=enviado(1), completed="Y", respostas=[R(True, "RCONS")]),
         C.RECUSA_CONSENTIMENTO),
        ("recusou contato em CON1",
         P(8, sent=enviado(1), completed="Y", respostas=[R(True, "RCONT")]),
         C.RECUSA_CONTATO),
        ("recusa de contato na base central",
         P(9, sent=enviado(5), recusa_base_central=True), C.RECUSA_CONTATO),
        ("recusa de contato no participante (OptOut)",
         P(10, sent=enviado(5), emailstatus="OptOut"), C.RECUSA_CONTATO),
        ("contato invalido", P(11, sent=enviado(5), emailstatus="invalido"),
         C.CONTATO_INVALIDO),
        ("respondente com contato invalido continua respondente",
         P(12, sent=enviado(5), emailstatus="invalido", completed="Y",
           respostas=[R(True, "CONC")]), C.RESPONDENTE),
        ("janela encerrada", P(13, sent=enviado(61),
                               validuntil=(AGORA - timedelta(days=1)).strftime(
                                   "%Y-%m-%d %H:%M:%S")), C.EXPIRADO),
        ("janela encerrada sem validuntil gravado (convite de fora da rotina)",
         P(14, sent=enviado(61)), C.EXPIRADO),
        ("em preenchimento com a janela encerrada",
         P(15, sent=enviado(61), respostas=[R(False, "CONC")]), C.EXPIRADO),
        ("concluido sem resposta que o explique",
         P(16, sent=enviado(5), completed="Y"), C.CONCLUIDO_SEM_RESPOSTA),
    ]
    falhas = [f"{nome}: {C.estado(p, AGORA, AGENDA)}, esperado {esperado}"
              for nome, p, esperado in casos_estado
              if C.estado(p, AGORA, AGENDA) != esperado]
    registra("estado de cada participante, pela secao 12 do P5", falhas,
             f"{len(casos_estado)} casos; abrir o endereco nao e iniciar")

    # --- o que vence -------------------------------------------------------
    def vence(p, agora=AGORA, no_ciclo=None, fora=None, ciclo=2026):
        r = C.plano([p], AGENDA, ciclo, agora, no_ciclo, fora)
        if r.convites:
            return f"convite:{r.convites[0].motivo}"
        if r.lembretes:
            a = r.lembretes[0]
            return f"lembrete {a.numero}:{a.variante}"
        return "nada"

    um_ano = AGORA.date() - timedelta(days=200)
    treze = AGORA.date() - timedelta(days=400)
    casos = [
        ("ancora do 1o semestre (15/07) ja passou", P(20), {}, "convite:ancora"),
        ("ancora do 2o semestre (15/12) ainda nao", P(21, semestre_conclusao="2"),
         {}, "nada"),
        ("concluiu depois do ano do ciclo", P(22, ano_conclusao="2027"), {},
         "nada"),
        ("convidado em outro ciclo ha 200 dias (menos de 12 meses)", P(23),
         {"fora": {"pid-23": um_ano}}, "nada"),
        ("convidado em outro ciclo ha 400 dias", P(24),
         {"fora": {"pid-24": treze}}, "convite:ancora"),
        ("voltou a pendente depois do reparo: reconvite, sem ancora",
         P(25, semestre_conclusao="2"), {"no_ciclo": {25: 1}},
         "convite:reconvite"),
        ("segunda volta a pendente no ciclo: teto de uma rodada",
         P(26), {"no_ciclo": {26: 2}}, "nada"),
        ("convite ha 3 dias: D+4 ainda nao", P(27, sent=enviado(3)), {}, "nada"),
        ("convite ha 4 dias: primeiro lembrete", P(28, sent=enviado(4)), {},
         "lembrete 1:convidado"),
        # O `sent` da plataforma esta em UTC. Um convite as 22h de quinta,
        # hora local, e 01h de sexta em UTC: o D+4 conta da quinta e vence na
        # segunda. Lido como hora local, venceria so na terca.
        ("convite as 22h locais (01h UTC do dia seguinte) conta do dia local",
         P(38, sent=enviado(3, horas=12)), {}, "lembrete 1:convidado"),
        ("em preenchimento, D+7 e 3 dias do anterior: segundo lembrete, ramo de "
         "retomada", P(29, sent=enviado(7), remindercount=1,
                       remindersent=enviado(3), respostas=[R(False, "CONC")]),
         {}, "lembrete 2:em_preenchimento"),
        ("D+7 vencido, mas so 1 dia do anterior: espera o intervalo minimo",
         P(30, sent=enviado(8), remindercount=1, remindersent=enviado(1)), {},
         "nada"),
        ("D+14: terceiro lembrete", P(31, sent=enviado(14), remindercount=2,
                                       remindersent=enviado(7)), {},
         "lembrete 3:convidado"),
        ("tres lembretes enviados: acabou", P(32, sent=enviado(20),
                                              remindercount=3,
                                              remindersent=enviado(6)), {},
         "nada"),
        ("respondente nao recebe", P(33, sent=enviado(4), completed="Y",
                                     respostas=[R(True, "CONC")]), {}, "nada"),
        ("recusa de consentimento nao recebe",
         P(34, sent=enviado(4), completed="Y", respostas=[R(True, "RCONS")]),
         {}, "nada"),
        ("recusa de contato nao recebe", P(35, sent=enviado(4),
                                           recusa_base_central=True), {},
         "nada"),
        ("contato invalido nao recebe", P(36, sent=enviado(4),
                                          emailstatus="invalido"), {}, "nada"),
        ("expirado nao recebe", P(37, sent=enviado(61)), {}, "nada"),
    ]
    falhas = []
    for nome, p, extra, esperado in casos:
        obtido = vence(p, no_ciclo=extra.get("no_ciclo"), fora=extra.get("fora"))
        if obtido != esperado:
            falhas.append(f"{nome}: {obtido}, esperado {esperado}")
    registra("convite pela ancora e lembretes por D+n do envio de cada um",
             falhas, f"{len(casos)} casos")

    # --- fim de semana: D+4 que cai no sabado sai na segunda, e o D+7 espera
    # os 3 dias do intervalo minimo ------------------------------------------
    terca = datetime(2026, 9, 29, 10, 0, tzinfo=FUSO)
    p = P(40, sent=enviado(0, base=terca))
    segunda = datetime(2026, 10, 5, 10, 0, tzinfo=FUSO)
    falhas = []
    if vence(p, agora=segunda) != "lembrete 1:convidado":
        falhas.append("D+4 no sabado nao saiu na segunda")
    p.remindercount, p.remindersent = 1, enviado(0, base=segunda)
    terca2 = datetime(2026, 10, 6, 10, 0, tzinfo=FUSO)
    quinta = datetime(2026, 10, 8, 10, 0, tzinfo=FUSO)
    if vence(p, agora=terca2) != "nada":
        falhas.append("D+7 na terca saiu um dia depois do primeiro lembrete")
    if vence(p, agora=quinta) != "lembrete 2:convidado":
        falhas.append("D+7 adiado nao saiu na quinta")
    registra("lembrete que vence fora de dia util sai no seguinte, sem quebrar o "
             "intervalo minimo", falhas, "D+4 (sab) na seg; D+7 (ter) na qui")

    # --- janela -------------------------------------------------------------
    # Esperado calculado aqui, do instante local do convite, e nao pela funcao
    # que se confere — senao a conferencia concordaria com o proprio erro.
    p = P(41, sent=enviado(1))
    r = C.plano([p], AGENDA, 2026, AGORA)
    esperado = (AGORA - timedelta(days=1) + timedelta(days=60)).strftime(
        "%Y-%m-%d %H:%M:%S")
    falhas = [] if [a.validuntil for a in r.janelas] == [esperado] else \
        [f"janela {[a.validuntil for a in r.janelas]}, esperado {esperado}"]
    registra("convidado sem janela recebe validuntil = envio + 60 dias",
             falhas, esperado)

    # --- dia util e horario ---------------------------------------------------
    falhas = []
    if C.previsto_para(AGENDA, date(2026, 10, 5)) != AGORA:
        falhas.append("segunda 05/10 nao esta prevista as 10:00")
    for dia, nome in ((date(2026, 10, 10), "sabado"), (date(2026, 10, 11),
                      "domingo"), (date(2026, 10, 12), "feriado de 12/10")):
        if C.previsto_para(AGENDA, dia) is not None:
            falhas.append(f"{nome} previsto")
    registra("um horario fixo por dia util; nenhum em fim de semana ou feriado",
             falhas, f"{AGENDA.horario:%H:%M}, seg a sex, "
             f"{len(AGENDA.feriados)} feriados")

    # --- agenda: faixa admissivel da secao 5.1 ------------------------------
    with open(os.path.join(AQUI, "rotinas", "configuracao", "agenda.json"),
              encoding="utf-8") as fh:
        base = json.load(fh)
    falhas = [] if not AGENDA.avisos else [f"aviso: {AGENDA.avisos}"]
    recusadas = [
        ("primeiro lembrete em D+2", {"lembretes_dias": [2, 7, 14]}),
        ("primeiro lembrete em D+8", {"lembretes_dias": [8, 12, 16]}),
        ("intervalo de 1 dia", {"lembretes_dias": [4, 5, 14]}),
        ("ultimo depois de D+21", {"lembretes_dias": [4, 7, 25]}),
        ("quatro lembretes", {"lembretes_dias": [4, 7, 10, 14]}),
        ("disparo no sabado", {"dias_da_semana": [0, 1, 2, 3, 4, 5]}),
        ("duas rodadas de reparo", {"reconvites_por_ciclo": 2}),
        ("convite a cada 6 meses", {"meses_entre_convites": 6}),
        ("lote acima do maxemails", {"lote": 100}),
    ]
    for nome, mudanca in recusadas:
        try:
            C.le_agenda(dict(base, **mudanca))
            falhas.append(f"aceitou: {nome}")
        except C.ErroAgenda:
            pass
    try:
        a = C.le_agenda(dict(base, lembretes_dias=[4, 7, 25],
                             registro_fora_da_faixa="ADR-XXXX (teste)"))
        if not a.avisos:
            falhas.append("fora da faixa com registro nao gerou aviso")
    except C.ErroAgenda as e:
        falhas.append(f"fora da faixa com registro recusado: {e}")
    registra("agenda versionada dentro da faixa; fora dela, so com registro",
             falhas, f"{len(recusadas)} configuracoes recusadas, 1 aceita com "
             "aviso")

    # --- coerencia com a E20 ------------------------------------------------
    falhas = []
    if (C.VARIANTE_CONVIDADO, C.VARIANTE_EM_PREENCHIMENTO) != (
            mensagens.VARIANTE_CONVIDADO, mensagens.VARIANTE_EM_PREENCHIMENTO):
        falhas.append("valores do ramo diferem de mensagens.py")
    registra("ramos do lembrete iguais aos de instrumento/mensagens.py", falhas)


# ===========================================================================
# Parte 2 — o caminho real, pelo agendador
# ===========================================================================

class Ocultos(HTMLParser):
    """Campos ocultos do formulario, inclusive os de relevancia, que vem com
    aspas simples e que um filtro por expressao regular deixa escapar."""

    def __init__(self):
        super().__init__()
        self.campos = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "input" and a.get("type") == "hidden" and a.get("name"):
            self.campos[a["name"]] = a.get("value") or ""


def abre(token):
    """Abre o endereco individual numa sessao nova. Devolve (abridor, campos)."""
    jar = http.cookiejar.CookieJar()
    abridor = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(jar))
    pagina = abridor.open(f"http://127.0.0.1:{PORTA}/index.php/{SID}?token="
                          f"{token}&lang=pt-BR&newtest=Y", timeout=60).read()
    o = Ocultos()
    o.feed(pagina.decode("utf-8", "replace"))
    return abridor, o.campos


def envia_pagina_1(token, con1):
    """Responde a pagina 1 como o respondente: CON1, e CON2 quando concorda."""
    abridor, campos = abre(token)
    campos = dict(campos, Q676=con1, move="movenext")
    if con1 == C.CON1_CONCORDO:
        campos.update(Q677="CONC", relevance677="1")
    abridor.open(urllib.request.Request(
        f"http://127.0.0.1:{PORTA}/index.php/{SID}",
        data=urllib.parse.urlencode(campos).encode()), timeout=60).read()


def utc_texto(instante):
    return instante.astimezone(UTC).strftime("%Y-%m-%d %H:%M")


def compose(*args, rotina=None):
    """docker compose com ROTINA_* do comando, e nao do .env — ou, sem
    `rotina`, exatamente o que o .env diz."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("ROTINA_")}
    env.update(rotina or {})
    return subprocess.run(["docker", "compose", *args], cwd=AQUI, env=env,
                          capture_output=True, text=True)


def sobe_agendador(rotina=None, limite=120):
    """Recria o conteiner rotinas e espera o agendador anunciar o ciclo.
    Devolve o instante da subida (para ler o log dali em diante), ou None."""
    desde = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    r = compose("up", "-d", "rotinas", rotina=rotina)
    if r.returncode != 0:
        return None
    ciclo = (rotina or {}).get("ROTINA_CICLO", ENV.get("ROTINA_CICLO"))
    inicio = time.time()
    while time.time() - inicio < limite:
        log = compose("logs", "--no-log-prefix", "--since", desde,
                      "rotinas").stdout
        if f"agendador de pe · modo" in log and f"ciclo {ciclo}" in log:
            return desde
        time.sleep(3)
    return None


def mostra_log(desde):
    """O log do agendador desde a subida. Recriar o conteiner apaga o log do
    anterior — por isso ele e mostrado antes de o agendador do .env voltar."""
    for linha in compose("logs", "--no-log-prefix", "--since", desde,
                         "rotinas").stdout.splitlines():
        if linha.strip():
            print(f"    | {linha}")


def fora_da_virada_de_devolucoes(minutos=10):
    """O agendador de teste, em modo real, leria e consumiria a caixa de
    devolucoes se uma virada do intervalo caisse durante o teste. Espera a
    virada passar, para que ela fique com o agendador do .env."""
    passo = AGENDA.devolucoes_intervalo_minutos * 60
    agora = time.time()
    falta = passo - agora % passo
    if falta < minutos * 60:
        print(f"  aguardando {falta + 60:.0f} s: a leitura de devolucoes "
              "agendada cai durante o teste", flush=True)
        time.sleep(falta + 60)


CAMPOS = ("tid, token, participant_id, sent, remindersent, remindercount, "
          "completed, emailstatus, validuntil, usesleft, attribute_7")

# Situacoes plantadas: rotulo -> (preparo, esperado no disparo)
#   esperado: None (nada), ("lembrete", n, ramo) ou ("convite", motivo)
SITUACOES = [
    ("A convidado, D+4", None),
    ("B abriu o endereco sem enviar pagina, D+4", None),
    ("C em preenchimento, D+7, lembrete 1 ha 3 dias", None),
    ("D convidado, D+14, lembrete 2 ha 7 dias", None),
    ("E convidado, D+2", None),
    ("F convidado, D+8, lembrete 1 ontem", None),
    ("G tres lembretes ja enviados", None),
    ("H respondente", None),
    ("I recusa de consentimento", None),
    ("J recusa de contato", None),
    ("K contato invalido, D+4", None),
    ("L expirado", None),
    ("M reparado: volta a pendente apos um convite no ciclo", None),
    ("N reparado pela segunda vez no ciclo", None),
]
ESPERADO = {
    "A": ("lembrete", 1, mensagens.VARIANTE_CONVIDADO),
    "B": ("lembrete", 1, mensagens.VARIANTE_CONVIDADO),
    "C": ("lembrete", 2, mensagens.VARIANTE_EM_PREENCHIMENTO),
    "D": ("lembrete", 3, mensagens.VARIANTE_CONVIDADO),
    "M": ("convite", 0, "reconvite"),
}


def confere_agendada():
    print(f"\ncaminho real, pelo agendador (questionario {SID}, ciclo de teste "
          f"{CICLO_TESTE}, modo real)")
    agora = datetime.now(FUSO)
    if not AGENDA.dia_util(agora.date()):
        raise SystemExit("o agendador so dispara em dia util; rode num dia util")

    sql = cm.sql
    fora_da_virada_de_devolucoes()
    with api_do_hospedeiro() as api:
        # --- estado de partida: a rotina ativa em simulado nao enviou nada -
        falhas = []
        linhas = sql("SELECT situacao, modo, previsto_para, iniciado_em FROM "
                     "egressos_execucoes WHERE tarefa='disparo' AND "
                     f"origem='agendada' AND ciclo='{ENV.get('ROTINA_CICLO')}'"
                     " ORDER BY id")
        if not linhas:
            falhas.append("nenhuma execucao agendada do ciclo corrente ainda")
        for l in linhas:
            if l["situacao"] != "simulada" or l["modo"] != "simulado":
                falhas.append(f"execucao {l}: esperada simulada")
            elif not ANTES_TOLERADO <= (datetime.strptime(l["iniciado_em"],
                                                          "%Y-%m-%d %H:%M:%S")
                                        - datetime.strptime(
                                            l["previsto_para"],
                                            "%Y-%m-%d %H:%M:%S")
                                        ).total_seconds() <= DEPOIS_TOLERADO:
                falhas.append(f"execucao {l}: fora do horario")
        if sql("SELECT COUNT(*) n FROM egressos_disparos")[0]["n"] != "0":
            falhas.append("ha envio registrado antes do teste")
        if sql(f"SELECT COUNT(*) n FROM lime_tokens_{SID} WHERE sent<>'N'"
               )[0]["n"] != "0":
            falhas.append("ha participante convidado antes do teste")
        ultima = linhas[-1] if linhas else {}
        registra("rotina ativa em modo simulado: rodou no horario e nada "
                 "enviou", falhas,
                 f"{len(linhas)} execucao(oes) agendada(s); a ultima previu "
                 f"{ultima.get('previsto_para')} e comecou "
                 f"{ultima.get('iniciado_em')}")

        # --- planta ---------------------------------------------------------
        escolhidos = sql(
            f"SELECT {CAMPOS} FROM lime_tokens_{SID} t WHERE email LIKE "
            f"'%@{DOMINIO}' AND sent='N' AND completed='N' AND "
            "emailstatus='OK' AND (SELECT COUNT(*) FROM lime_tokens_"
            f"{SID} u WHERE u.email=t.email)=1 ORDER BY tid LIMIT "
            f"{len(SITUACOES)}")
        if len(escolhidos) != len(SITUACOES):
            raise SystemExit("participantes insuficientes para plantar")
        por = {rotulo[0]: p for (rotulo, _), p in zip(SITUACOES, escolhidos)}
        antes = {l["tid"]: l for l in sql(f"SELECT {CAMPOS} FROM "
                                          f"lime_tokens_{SID}")}
        caixa_antes = cm.imap(cm.CAIXA_ENTREGUES,
                              "print(json.dumps(len(m.search(None, 'ALL')[1]"
                              "[0].split())))")
        print("  plantados (tid): " + ", ".join(
            f"{k}={v['tid']}" for k, v in por.items()))

        agora = datetime.now(FUSO)

        def ajusta(letra, **campos):
            api.chamar("set_participant_properties",
                       [SID, int(por[letra]["tid"]), campos])

        try:
            ajusta("A", sent=utc_texto(agora - timedelta(days=4)))
            ajusta("B", sent=utc_texto(agora - timedelta(days=4)))
            abre(por["B"]["token"])
            ajusta("C", sent=utc_texto(agora - timedelta(days=7)),
                   remindercount=1,
                   remindersent=utc_texto(agora - timedelta(days=3)))
            envia_pagina_1(por["C"]["token"], C.CON1_CONCORDO)
            ajusta("D", sent=utc_texto(agora - timedelta(days=14)),
                   remindercount=2,
                   remindersent=utc_texto(agora - timedelta(days=7)))
            ajusta("E", sent=utc_texto(agora - timedelta(days=2)))
            ajusta("F", sent=utc_texto(agora - timedelta(days=8)),
                   remindercount=1,
                   remindersent=utc_texto(agora - timedelta(days=1)))
            ajusta("G", sent=utc_texto(agora - timedelta(days=20)),
                   remindercount=3,
                   remindersent=utc_texto(agora - timedelta(days=6)))
            ajusta("H", sent=utc_texto(agora - timedelta(days=5)),
                   completed=utc_texto(agora - timedelta(days=1)))
            api.chamar("add_response", [SID, {
                "token": por["H"]["token"], "Q676": "CONC", "Q677": "CONC",
                "lastpage": 10}])
            for letra, con1 in (("I", C.CON1_RECUSA_CONSENTIMENTO),
                                ("J", C.CON1_RECUSA_CONTATO)):
                ajusta(letra, sent=utc_texto(agora - timedelta(days=5)))
                envia_pagina_1(por[letra]["token"], con1)
            ajusta("K", sent=utc_texto(agora - timedelta(days=4)),
                   emailstatus="invalido")
            ajusta("L", sent=utc_texto(agora - timedelta(days=61)),
                   validuntil=(agora - timedelta(days=1)).strftime(
                       "%Y-%m-%d %H:%M:%S"))
            # Reparo: o convite anterior do ciclo esta no registro da rotina.
            for letra, quantos in (("M", 1), ("N", 2)):
                for _ in range(quantos):
                    sql("INSERT INTO egressos_disparos (execucao_id, "
                        "registrado_em, questionario, ciclo, tid, "
                        "participant_id, tipo, numero, motivo, estado, "
                        "resultado) VALUES (0, NOW() - INTERVAL 10 DAY, "
                        f"{SID}, '{CICLO_TESTE}', {por[letra]['tid']}, "
                        f"'{por[letra]['participant_id']}', 'convite', 0, "
                        "'ancora', 'pendente', 'enviado')")

            # O caminho real produziu o que a rotina le?
            falhas = []
            resp = {l["token"]: l for l in sql(
                f"SELECT token, lastpage, Q676, submitdate FROM "
                f"lime_responses_{SID}")}
            b, c_, i, j = (resp.get(por[x]["token"], {}) for x in "BCIJ")
            if not (b and b["Q676"] is None and b["submitdate"] is None):
                falhas.append(f"B: abrir nao deixou parcial sem CON1 ({b})")
            if not (c_ and c_["Q676"] == "CONC" and c_["submitdate"] is None
                    and c_["lastpage"] == "1"):
                falhas.append(f"C: pagina 1 nao deixou parcial com CON1 ({c_})")
            for letra, linha, con1 in (("I", i, "RCONS"), ("J", j, "RCONT")):
                tok = sql(f"SELECT completed FROM lime_tokens_{SID} WHERE "
                          f"tid={por[letra]['tid']}")[0]
                if not (linha and linha["Q676"] == con1 and linha["submitdate"]
                        and tok["completed"] not in ("N", None)):
                    falhas.append(f"{letra}: recusa nao encerrou como a E15 "
                                  f"observou ({linha}, {tok})")
            registra("situacoes plantadas pelo caminho real como a plataforma "
                     "as produz", falhas,
                     "abrir: lastpage 0 e CON1 vazio; pagina 1: lastpage 1 e "
                     "CONC; recusas: enviadas e concluidas")

            plantado = {l["tid"]: l for l in sql(f"SELECT {CAMPOS} FROM "
                                                 f"lime_tokens_{SID}")}

            # --- agendador em modo real, ciclo de teste, horario proximo ---
            agora = datetime.now(FUSO)
            horario = (agora + timedelta(seconds=150)).replace(second=0,
                                                               microsecond=0)
            desde = sobe_agendador({
                "ROTINA_DISPARO": "real", "ROTINA_CICLO": CICLO_TESTE,
                "ROTINA_QUESTIONARIO": str(SID),
                "ROTINA_HORARIO": f"{horario:%H:%M}"})
            if not desde:
                raise SystemExit("agendador de teste nao subiu")
            print(f"  agendador de teste de pe; horario {horario:%H:%M}, "
                  "aguardando...", flush=True)

            execucao = None
            while datetime.now(FUSO) < horario + timedelta(minutes=6):
                linhas = sql("SELECT * FROM egressos_execucoes WHERE "
                             f"tarefa='disparo' AND ciclo='{CICLO_TESTE}' AND "
                             f"previsto_para='{horario:%Y-%m-%d %H:%M:%S}'")
                if linhas and linhas[0]["situacao"] not in ("reservada",
                                                            "em_execucao"):
                    execucao = linhas[0]
                    break
                time.sleep(10)

            print("  log do agendador de teste:")
            mostra_log(desde)

            # --- 1. no horario ---------------------------------------------
            falhas = []
            if execucao is None:
                raise SystemExit("o disparo agendado nao terminou no prazo")
            inicio = datetime.strptime(execucao["iniciado_em"],
                                       "%Y-%m-%d %H:%M:%S").replace(tzinfo=FUSO)
            atraso = (inicio - horario).total_seconds()
            if not ANTES_TOLERADO <= atraso <= DEPOIS_TOLERADO:
                falhas.append(f"comecou {atraso:.0f} s depois do horario")
            if (execucao["situacao"], execucao["modo"], execucao["origem"]) != (
                    "concluida", "real", "agendada"):
                falhas.append(f"execucao {execucao['situacao']} "
                              f"{execucao['modo']} {execucao['origem']}")
            registra("o disparo executou no horario", falhas,
                     f"previsto {horario:%H:%M:%S}, comecou "
                     f"{inicio:%H:%M:%S} ({atraso:.0f} s), "
                     f"{execucao['situacao']}")

            # --- 2. quem recebeu, pelo registro da rotina -------------------
            falhas = []
            letra_de = {int(v["tid"]): k for k, v in por.items()}
            envios = sql("SELECT tid, tipo, numero, motivo, variante, estado, "
                         "resultado FROM egressos_disparos WHERE "
                         f"execucao_id={execucao['id']}")
            obtido = {}
            for e in envios:
                letra = letra_de.get(int(e["tid"]), f"tid {e['tid']}")
                terceiro = e["variante"] if e["tipo"] == "lembrete" else \
                    e["motivo"]
                obtido[letra] = (e["tipo"], int(e["numero"]), terceiro)
                if e["resultado"] != "enviado":
                    falhas.append(f"{letra}: {e['resultado']}")
                if e["estado"] not in (C.CONVIDADO, C.EM_PREENCHIMENTO,
                                       C.PENDENTE):
                    falhas.append(f"{letra}: enviado a estado {e['estado']}")
            if obtido != ESPERADO:
                falhas.append(f"envios {obtido}, esperados {ESPERADO}")
            lembretes = sorted(k for k, v in obtido.items() if v[0] == "lembrete")
            registra("lembretes so para nao respondentes, com o ramo certo",
                     falhas, f"lembretes para {', '.join(lembretes)} "
                     "(convidado e em preenchimento); reconvite para M; "
                     "nenhum para respondente, recusas, invalido, expirado, "
                     "antes do D+n, intervalo minimo ou teto")

            # --- 3. os 500 na plataforma ------------------------------------
            # Comparados com o estado logo depois do plantio. O que pode
            # mudar, e so em quem: contadores e ramo em quem recebeu lembrete;
            # o convite em M; e a janela de 60 dias em todo convidado que
            # estava sem ela — de A a G e M. Nada nos outros 486.
            falhas = []
            depois = {l["tid"]: l for l in sql(f"SELECT {CAMPOS} FROM "
                                               f"lime_tokens_{SID}")}
            pode = {letra: set() for letra in por}
            for letra in "ABCD":
                pode[letra] = {"remindersent", "remindercount", "attribute_7",
                               "validuntil"}
            for letra in "EFG":
                pode[letra] = {"validuntil"}
            pode["M"] = {"sent", "validuntil"}
            for tid, l in depois.items():
                letra = letra_de.get(int(tid))
                mudou = {c for c in ("sent", "remindersent", "remindercount",
                                     "validuntil", "attribute_7")
                         if (l[c] or None) != (plantado[tid][c] or None)}
                if mudou - (pode[letra] if letra else set()):
                    falhas.append(f"{letra or 'tid ' + tid} mudou "
                                  f"{sorted(mudou)}")
            for letra, (tipo, n, terceiro) in ESPERADO.items():
                l = depois[por[letra]["tid"]]
                if tipo == "lembrete" and (int(l["remindercount"]) != n
                                           or l["attribute_7"] != terceiro):
                    falhas.append(f"{letra}: remindercount "
                                  f"{l['remindercount']}, ramo "
                                  f"{l['attribute_7']}")
            for letra in "ABCDEFGM":
                l = depois[por[letra]["tid"]]
                if l["sent"] in ("N", None):
                    falhas.append(f"{letra}: sem convite gravado")
                    continue
                janela = (C.instante_utc(l["sent"]).astimezone(FUSO)
                          + timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
                if l["validuntil"] != janela:
                    falhas.append(f"{letra}: validuntil {l['validuntil']}, "
                                  f"esperado {janela}")
            nao = len([t for t in depois if int(t) not in letra_de])
            registra("na plataforma: contador e ramo so de quem recebeu; "
                     "janela de 60 dias do envio de cada convidado", falhas,
                     f"{nao} nao plantados intactos; M reconvidado com "
                     f"validuntil {depois[por['M']['tid']]['validuntil']}")

            # --- 4. a caixa --------------------------------------------------
            falhas = []
            for letra, v in por.items():
                achadas = cm.aguarda(cm.CAIXA_ENTREGUES, v["token"],
                                     1 if letra in ESPERADO else 0, limite=60) \
                    if letra in ESPERADO else \
                    cm.mensagens_do_token(cm.CAIXA_ENTREGUES, v["token"])
                quer = 1 if letra in ESPERADO else 0
                if len(achadas) != quer:
                    falhas.append(f"{letra}: {len(achadas)} mensagem(ns), "
                                  f"esperada(s) {quer}")
                    continue
                if not achadas:
                    continue
                msg = email.message_from_bytes(achadas[0],
                                               policy=email.policy.default)
                texto = cm.texto_visivel(cm.corpo_html(msg))
                tipo = ESPERADO[letra][0]
                assunto = (mensagens.ASSUNTO_LEMBRETE if tipo == "lembrete"
                           else mensagens.ASSUNTO_CONVITE)
                if str(msg["Subject"]) != assunto:
                    falhas.append(f"{letra}: assunto {msg['Subject']}")
                retomada = "Carregar questionário não finalizado" in texto
                if tipo == "lembrete" and retomada != (
                        ESPERADO[letra][2] == mensagens.VARIANTE_EM_PREENCHIMENTO):
                    falhas.append(f"{letra}: ramo errado no texto")
            total = cm.imap(cm.CAIXA_ENTREGUES,
                            "print(json.dumps(len(m.search(None, 'ALL')[1]"
                            "[0].split())))")
            if total - caixa_antes != len(ESPERADO):
                falhas.append(f"{total - caixa_antes} mensagens novas na caixa, "
                              f"esperadas {len(ESPERADO)}")
            registra("as mensagens chegaram, uma por destinatario, e nenhuma a "
                     "mais", falhas,
                     f"{total - caixa_antes} novas: 4 lembretes (o de C com a "
                     "retomada) e 1 convite")
        finally:
            limpa(api, por, antes)


def limpa(api, por, antes):
    """Cada passo independente: uma falha num nao impede os outros."""
    falhas = []
    tokens = [v["token"] for v in por.values()]
    def agendador_do_env():
        if not sobe_agendador():
            raise RuntimeError("o agendador do .env nao subiu")

    passos = [
        ("agendador", agendador_do_env),
        ("participantes", lambda: [api.chamar(
            "set_participant_properties", [SID, int(v["tid"]), {
                "sent": antes[v["tid"]]["sent"],
                "remindersent": antes[v["tid"]]["remindersent"],
                "remindercount": int(antes[v["tid"]]["remindercount"]),
                "completed": antes[v["tid"]]["completed"],
                "emailstatus": antes[v["tid"]]["emailstatus"],
                "validuntil": antes[v["tid"]]["validuntil"],
                "usesleft": int(antes[v["tid"]]["usesleft"]),
                "attribute_7": antes[v["tid"]]["attribute_7"] or ""}])
            for v in por.values()]),
        ("respostas", lambda: [
            api.chamar("delete_response", [SID, int(r["id"])])
            for r in cm.sql(f"SELECT id FROM lime_responses_{SID} WHERE token "
                            "IN (" + ",".join(f"'{t}'" for t in tokens) + ")")]),
        ("caixa", lambda: [cm.apaga(cm.CAIXA_ENTREGUES,
                                    ["HEADER", "X-tokenid", t])
                           for t in tokens]),
        ("registro da rotina", lambda: (
            cm.sql(f"DELETE FROM egressos_disparos WHERE ciclo='{CICLO_TESTE}'"),
            cm.sql("DELETE FROM egressos_execucoes WHERE "
                   f"ciclo='{CICLO_TESTE}'"),
            cm.sql("DELETE FROM egressos_devolucoes WHERE "
                   f"ciclo='{CICLO_TESTE}'"))),
    ]
    for rotulo, passo in passos:
        try:
            passo()
        # SystemExit tambem: e assim que os auxiliares da E20 acusam falha de
        # caixa, e foi o que deixou a primeira limpeza pela metade.
        except (Exception, SystemExit) as ex:  # noqa: BLE001 — registra e segue
            falhas.append(f"limpeza de {rotulo}: {ex}")
    depois = {l["tid"]: l for l in cm.sql(f"SELECT {CAMPOS} FROM "
                                          f"lime_tokens_{SID}")}
    for tid, a in antes.items():
        for c in ("sent", "remindersent", "remindercount", "completed",
                  "emailstatus", "validuntil", "usesleft", "attribute_7"):
            if (depois[tid][c] or None) != (a[c] or None):
                falhas.append(f"tid {tid}: {c} {a[c]} -> {depois[tid][c]}")
    contagens = cm.sql(
        f"SELECT (SELECT COUNT(*) FROM lime_responses_{SID}) r, "
        "(SELECT COUNT(*) FROM egressos_disparos) d, "
        f"(SELECT COUNT(*) FROM egressos_execucoes WHERE ciclo='{CICLO_TESTE}')"
        " e, (SELECT COUNT(*) FROM lime_participants WHERE blacklisted='Y') b"
    )[0]
    if contagens != {"r": "0", "d": "0", "e": "0", "b": "0"}:
        falhas.append(f"sobrou: {contagens}")
    if any(cm.mensagens_do_token(cm.CAIXA_ENTREGUES, t) for t in tokens):
        falhas.append("mensagens de teste ficaram na caixa")
    r = compose("exec", "-T", "rotinas", "printenv", "ROTINA_DISPARO",
                "ROTINA_CICLO", "ROTINA_HORARIO")
    estado = r.stdout.split()
    if estado[:2] != [ENV.get("ROTINA_DISPARO"), ENV.get("ROTINA_CICLO")]:
        falhas.append(f"agendador ficou com {estado}")
    registra("limpeza", falhas,
             "500 participantes como antes, nenhuma resposta, nenhum envio "
             f"registrado, nenhuma recusa; agendador de volta a "
             f"{' · '.join(estado[:2])}")


# ===========================================================================
# Parte 3 — execucao perdida
# ===========================================================================

def confere_perdida():
    print("\nexecucao perdida (horario passado sem execucao)")
    sql = cm.sql
    agora = datetime.now(FUSO)
    primeiro = sql("SELECT MIN(COALESCE(iniciado_em, previsto_para)) p FROM "
                   "egressos_execucoes")[0]["p"]
    primeiro = datetime.strptime(primeiro, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=FUSO)
    horario = (agora - timedelta(minutes=AGENDA.tolerancia_minutos + 5)
               ).replace(second=0, microsecond=0)
    if horario <= primeiro or horario.date() != agora.date():
        raise SystemExit("e cedo demais: o horario de teste precisa cair depois "
                         "do primeiro registro da rotina, hoje")
    fora_da_virada_de_devolucoes(minutos=3)
    try:
        if not sobe_agendador({
                "ROTINA_DISPARO": "simulado", "ROTINA_CICLO": CICLO_TESTE,
                "ROTINA_QUESTIONARIO": str(SID),
                "ROTINA_HORARIO": f"{horario:%H:%M}"}):
            raise SystemExit("agendador de teste nao subiu")
        time.sleep(15)
        linhas = sql("SELECT situacao, previsto_para, iniciado_em FROM "
                     f"egressos_execucoes WHERE ciclo='{CICLO_TESTE}' AND "
                     "tarefa='disparo'")
        log = compose("logs", "--no-log-prefix", "--since", "2m",
                      "rotinas").stdout
        falhas = []
        if [(l["situacao"], l["previsto_para"]) for l in linhas] != [
                ("perdida", f"{horario:%Y-%m-%d %H:%M:%S}")]:
            falhas.append(f"registro {linhas}")
        if "PERDIDO" not in log:
            falhas.append("o log nao acusou")
        registra("horario vencido sem execucao fica registrado como perdido, "
                 "e nao e executado fora da hora", falhas,
                 f"{horario:%H:%M} com tolerancia de "
                 f"{AGENDA.tolerancia_minutos} min, acusado ao subir")
    finally:
        sobe_agendador()
        sql(f"DELETE FROM egressos_execucoes WHERE ciclo='{CICLO_TESTE}'")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--agendada", action="store_true",
                    help="exercita o caminho real pelo agendador e desfaz")
    ap.add_argument("--perdida", action="store_true",
                    help="confere o registro de execucao perdida e desfaz")
    args = ap.parse_args()
    confere_regras()
    if args.agendada:
        confere_agendada()
    if args.perdida:
        confere_perdida()
    print(f"\n  {sum(resultados)} de {len(resultados)} conferencias passaram")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
