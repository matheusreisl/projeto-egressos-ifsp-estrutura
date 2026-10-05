#!/usr/bin/env python3
"""
Rotina de disparo (E21): convites e lembretes do ciclo, conforme a cadencia de
docs/especificacao/parametros-contato.md.

Quem decide o que vence e scripts/cadencia.py, que e logica pura. Esta rotina:

  1. confere a guarda — se falhar, nao dispara nada;
  2. le o estado de cada participante na plataforma;
  3. pede o plano a cadencia;
  4. executa o plano: convite, janela de 60 dias, ramo do lembrete e lembrete;
  5. registra a execucao e cada envio em tabelas proprias.

A guarda, antes de cada disparo:

  - as conferencias 1 a 7 da E19 (scripts/conferencia_participantes.py): token
    presente, unico e bem formado; identificador presente e unico; elo com a
    base central. Um disparo sobre base inconsistente manda o endereco de uma
    pessoa a outra;
  - as condicoes de que o disparo depende na E20: remetente e retorno sob o
    dominio de ensaio, nas caixas do ambiente, e o lembrete referenciando o
    atributo `variante_lembrete`, que existe e tem coluna. A identidade textual
    dos modelos com os versionados e conferida no hospedeiro, por
    infra/confere-mensagens.py, que alcanca o arquivo versionado.

O envio e da plataforma, com lista explicita de participantes:
`invite_participants` e `remind_participants`. Tres armadilhas dela, conferidas
no codigo do LimeSurvey 7 e tratadas aqui:

  - cada chamada envia no maximo `maxemails` (50) e ignora o resto da lista —
    por isso os lotes;
  - sem `continueOnError`, o lote PARA na primeira falha de um participante;
  - o "N left to send" conta todos os candidatos do questionario, e nao os da
    lista — nao serve para saber se a lista acabou.

E uma escolha: `remind_participants` recebe intervalo nulo, porque a cadencia
D+n e desta rotina, e teto igual ao numero de lembretes da agenda — rede de
seguranca, para que um engano aqui nao produza um quarto lembrete.

Registro proprio, sem token, nome nem endereco:

  egressos_execucoes   cada execucao: tarefa, modo, horario previsto e real,
                       situacao e resumo — e onde aparece a execucao PERDIDA,
                       que sem isso seria falha silenciosa
  egressos_disparos    cada envio tentado: participante (tid e participant_id),
                       tipo, numero, ramo, estado de partida e resultado

Uso, no conteiner rotinas (questionario e ciclo vem do ambiente):

    python3 disparar.py --simular     calcula e registra o plano, nao envia
    python3 disparar.py               dispara agora, fora do agendador

O disparo fora do agendador fica registrado como manual, e e recusado em dia
que nao e util. O modo agendado e o do agendador.py.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta

import pymysql

import cadencia
from conferencia_participantes import BLOQUEIAM_DISPARO, carrega, confere
from limesurvey_api import API, ErroAPI

QUESTIONARIO = os.environ.get("ROTINA_QUESTIONARIO")
CICLO = os.environ.get("ROTINA_CICLO")
AGENDA = os.environ.get("ROTINA_AGENDA", "/configuracao/agenda.json")

DOMINIO = os.environ.get("CORREIO_DOMINIO", "egressos.test")
CAIXA_REMETENTE = os.environ.get("CORREIO_CAIXA_REMETENTE", "acompanhamento")
CAIXA_DEVOLUCOES = os.environ.get("CORREIO_CAIXA_DEVOLUCOES", "devolucoes")

ATRIBUTO_VARIANTE = "variante_lembrete"

BANCO = {
    "host": os.environ.get("BANCO_HOST", "banco"),
    "port": int(os.environ.get("BANCO_PORTA", "3306")),
    "user": os.environ.get("BANCO_USUARIO"),
    "password": os.environ.get("BANCO_SENHA"),
    "database": os.environ.get("BANCO_NOME"),
    "charset": "utf8mb4",
    "autocommit": True,
}

DDL = [
    """CREATE TABLE IF NOT EXISTS egressos_execucoes (
      id            INT AUTO_INCREMENT PRIMARY KEY,
      tarefa        VARCHAR(20)  NOT NULL,
      modo          VARCHAR(10)  NOT NULL,
      origem        VARCHAR(10)  NOT NULL,
      questionario  INT          NULL,
      ciclo         VARCHAR(20)  NULL,
      previsto_para DATETIME     NULL,
      iniciado_em   DATETIME     NULL,
      terminado_em  DATETIME     NULL,
      situacao      VARCHAR(20)  NOT NULL,
      resumo        TEXT         NULL,
      erro          TEXT         NULL,
      UNIQUE KEY uma_por_horario (tarefa, previsto_para),
      KEY por_situacao (tarefa, situacao)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""",
    """CREATE TABLE IF NOT EXISTS egressos_disparos (
      id             INT AUTO_INCREMENT PRIMARY KEY,
      execucao_id    INT          NOT NULL,
      registrado_em  DATETIME     NOT NULL,
      questionario   INT          NOT NULL,
      ciclo          VARCHAR(20)  NOT NULL,
      tid            INT          NOT NULL,
      participant_id VARCHAR(50)  NULL,
      tipo           VARCHAR(10)  NOT NULL,
      numero         TINYINT      NOT NULL,
      motivo         VARCHAR(15)  NOT NULL,
      variante       VARCHAR(20)  NULL,
      estado         VARCHAR(30)  NOT NULL,
      resultado      VARCHAR(10)  NOT NULL,
      erro           TEXT         NULL,
      KEY por_participante (participant_id, tipo, resultado),
      KEY por_ciclo (questionario, ciclo, tid)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""",
]


class Bloqueio(Exception):
    """A guarda recusou o disparo."""


def agora(agenda):
    return datetime.now(agenda.fuso)


def local(instante):
    """DATETIME do registro proprio: hora local, sem fuso, como o resto."""
    return instante.strftime("%Y-%m-%d %H:%M:%S") if instante else None


# --- Banco ------------------------------------------------------------------

def conecta():
    return pymysql.connect(**BANCO)


def consulta_texto(conexao):
    """Funcao de consulta no formato que conferencia_participantes espera:
    lista de dicionarios com valores em texto ou None."""
    def sql(texto):
        with conexao.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(texto)
            return [{k: (None if v is None else str(v)) for k, v in l.items()}
                    for l in cur.fetchall()]
    return sql


def garante_tabelas(conexao):
    with conexao.cursor() as cur:
        for ddl in DDL:
            cur.execute(ddl)


def abre_execucao(conexao, tarefa, modo, origem, previsto=None, situacao=None,
                  iniciado=None):
    """Reserva a execucao. Para a agendada, a chave unica (tarefa, previsto)
    impede duas execucoes do mesmo horario — inclusive de dois agendadores."""
    with conexao.cursor() as cur:
        cur.execute(
            """INSERT INTO egressos_execucoes
               (tarefa, modo, origem, questionario, ciclo, previsto_para,
                iniciado_em, situacao)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (tarefa, modo, origem, QUESTIONARIO, CICLO, local(previsto),
             local(iniciado), situacao or "em_execucao"))
        return cur.lastrowid


def fecha_execucao(conexao, execucao, situacao, resumo=None, erro=None,
                   iniciado=None, terminado=None):
    with conexao.cursor() as cur:
        cur.execute(
            """UPDATE egressos_execucoes
                  SET situacao=%s, resumo=%s, erro=%s,
                      iniciado_em=COALESCE(%s, iniciado_em),
                      terminado_em=%s
                WHERE id=%s""",
            (situacao, json.dumps(resumo, ensure_ascii=False)
             if resumo is not None else None, erro, local(iniciado),
             local(terminado), execucao))


def registra_envio(conexao, execucao, acao, resultado, erro=None, quando=None):
    with conexao.cursor() as cur:
        cur.execute(
            """INSERT INTO egressos_disparos
               (execucao_id, registrado_em, questionario, ciclo, tid,
                participant_id, tipo, numero, motivo, variante, estado,
                resultado, erro)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (execucao, local(quando), int(QUESTIONARIO), CICLO, acao.tid,
             acao.participant_id, acao.tipo, acao.numero, acao.motivo,
             acao.variante, acao.estado, resultado, erro))


def historico(conexao):
    """Do registro proprio: convites ja enviados a cada participante neste
    questionario e ciclo, e a data do ultimo convite a cada pessoa fora dele."""
    sql = consulta_texto(conexao)
    no_ciclo = {int(l["tid"]): int(l["n"]) for l in sql(
        f"""SELECT tid, COUNT(*) n FROM egressos_disparos
             WHERE questionario={int(QUESTIONARIO)}
               AND ciclo={conexao.escape(CICLO)}
               AND tipo='convite' AND resultado='enviado'
             GROUP BY tid""")}
    fora = {l["participant_id"]: datetime.strptime(
                l["ultimo"], "%Y-%m-%d %H:%M:%S").date() for l in sql(
        f"""SELECT participant_id, MAX(registrado_em) ultimo
              FROM egressos_disparos
             WHERE participant_id IS NOT NULL
               AND tipo='convite' AND resultado='enviado'
               AND NOT (questionario={int(QUESTIONARIO)}
                        AND ciclo={conexao.escape(CICLO)})
             GROUP BY participant_id""")}
    return no_ciclo, fora


# --- Plataforma -------------------------------------------------------------

def espera_plataforma(limite):
    """Abre sessao na API, tentando ate o instante `limite`. Depois de um
    reinicio do hospedeiro, os conteineres voltam sem ordem garantida, e a
    rotina pode acordar antes da plataforma."""
    while True:
        try:
            return API().abrir()
        except ErroAPI as e:
            if datetime.now(limite.tzinfo) >= limite:
                raise ErroAPI(f"plataforma indisponivel ate o limite: {e}")
            print(f"  plataforma indisponivel; nova tentativa em 30 s ({e})",
                  flush=True)
            time.sleep(30)


def colunas_dos_atributos(api, sid):
    props = api.chamar("get_survey_properties", [sid, ["attributedescriptions"]])
    descricoes = json.loads(props.get("attributedescriptions") or "{}")
    return {info.get("description"): col for col, info in descricoes.items()}


def guarda(api, sql, sid):
    """Devolve a lista de motivos de bloqueio; vazia, libera o disparo."""
    motivos = []

    res, _ = confere(carrega(sid, sql))
    for n, descricao, ok, detalhe in res:
        if n in BLOQUEIAM_DISPARO and not ok:
            motivos.append(f"E19, conferencia {n} ({descricao}): {detalhe}")

    props = api.chamar("get_survey_properties",
                       [sid, ["adminemail", "bounce_email", "active",
                              "access_mode"]])
    if props.get("active") != "Y":
        motivos.append("questionario inativo")
    if props.get("access_mode") != "C":
        motivos.append("acesso nao e fechado por endereco individual")
    remetente = f"{CAIXA_REMETENTE}@{DOMINIO}"
    retorno = f"{CAIXA_DEVOLUCOES}@{DOMINIO}"
    if props.get("adminemail") != remetente:
        motivos.append(f"remetente {props.get('adminemail')!r}, esperado "
                       f"{remetente!r}")
    if props.get("bounce_email") != retorno:
        motivos.append(f"retorno {props.get('bounce_email')!r}, esperado "
                       f"{retorno!r}")
    for endereco in (props.get("adminemail") or "", props.get("bounce_email") or ""):
        if not endereco.endswith(".test"):
            motivos.append(f"{endereco!r} fora do dominio reservado (P7, 9.1)")

    coluna = colunas_dos_atributos(api, sid).get(ATRIBUTO_VARIANTE)
    if coluna is None:
        motivos.append(f"sem atributo {ATRIBUTO_VARIANTE}")
    else:
        existe = sql("SELECT COUNT(*) n FROM information_schema.COLUMNS WHERE "
                     f"TABLE_NAME='lime_tokens_{sid}' AND "
                     f"TABLE_SCHEMA=DATABASE() AND COLUMN_NAME='{coluna}'")
        if existe[0]["n"] != "1":
            motivos.append(f"{coluna} sem coluna na tabela de participantes")
        idioma = api.chamar("get_language_properties",
                            [sid, ["surveyls_email_remind"], None])
        n = coluna.split("_")[1]
        if f"TOKEN:ATTRIBUTE_{n} ==" not in (idioma.get(
                "surveyls_email_remind") or ""):
            motivos.append(f"o lembrete nao escolhe o ramo por {coluna}")
    return motivos


def le_participantes(api, sql, sid):
    """O estado de cada participante: campos do participante pela API (que
    decifra, se a E23 cifrar), recusa da base central e respostas pelo banco,
    so leitura."""
    colunas = colunas_dos_atributos(api, sid)
    col_ano = colunas.get("ano_conclusao")
    col_sem = colunas.get("semestre_conclusao")
    if not col_ano or not col_sem:
        raise Bloqueio("sem atributos de ano e semestre de conclusao (ancora)")
    campos = ["participant_id", "emailstatus", "sent", "remindersent",
              "remindercount", "completed", "validuntil", "blacklisted",
              col_ano, col_sem]

    registros, inicio = [], 0
    while True:
        try:
            pagina = api.chamar("list_participants",
                                [sid, inicio, 500, False, campos])
        except ErroAPI as e:
            if "No survey participants" in str(e):
                break
            raise
        if not isinstance(pagina, list) or not pagina:
            break
        registros.extend(pagina)
        # O inicio e o menor tid, e nao um deslocamento (conferido no codigo).
        inicio = int(pagina[-1]["tid"]) + 1
        if len(pagina) < 500:
            break

    bloqueados = {l["participant_id"] for l in sql(
        "SELECT participant_id FROM lime_participants WHERE blacklisted='Y'")}

    con1 = sql(f"SELECT qid FROM lime_questions WHERE sid={sid} "
               "AND title='CON1' AND parent_qid=0")
    if len(con1) != 1:
        raise Bloqueio("CON1 nao encontrado no questionario")
    # Coluna de resposta Q<qid> (E15).
    respostas = {}
    for l in sql(f"SELECT token, submitdate, Q{con1[0]['qid']} AS con1 "
                 f"FROM lime_responses_{sid}"):
        respostas.setdefault(l["token"], []).append(cadencia.Resposta(
            submetida=l["submitdate"] is not None, con1=l["con1"]))

    return [cadencia.Participante(
        tid=int(r["tid"]), participant_id=r.get("participant_id") or None,
        sent=r.get("sent"), remindersent=r.get("remindersent"),
        remindercount=int(r.get("remindercount") or 0),
        completed=r.get("completed"), emailstatus=r.get("emailstatus"),
        blacklisted=r.get("blacklisted"), validuntil=r.get("validuntil"),
        ano_conclusao=r.get(col_ano), semestre_conclusao=r.get(col_sem),
        recusa_base_central=(r.get("participant_id") or None) in bloqueados,
        respostas=respostas.get(r.get("token"), []))
        for r in registros]


def _resultados(retorno):
    """{tid: (ok, erro)} a partir do que invite/remind devolvem — o dicionario
    traz tambem a chave 'status', que nao e participante."""
    saida = {}
    if isinstance(retorno, dict):
        for chave, valor in retorno.items():
            if str(chave).isdigit() and isinstance(valor, dict):
                saida[int(chave)] = (valor.get("status") == "OK",
                                     valor.get("error"))
    return saida


def envia(api, conexao, execucao, sid, acoes, metodo, parametros, agenda):
    """Envia em lotes, registra participante a participante. Quem a plataforma
    nao devolver no resultado conta como falha: nao se presume envio."""
    enviados, falhas = [], []
    for i in range(0, len(acoes), agenda.lote):
        lote = acoes[i:i + agenda.lote]
        tids = [a.tid for a in lote]
        try:
            res = _resultados(api.chamar(metodo, parametros(tids)))
            erro_lote = None
        except ErroAPI as e:
            res, erro_lote = {}, str(e)
        for a in lote:
            ok, erro = res.get(a.tid, (False, erro_lote or "sem resultado"))
            registra_envio(conexao, execucao, a, "enviado" if ok else "falha",
                           erro, quando=agora(agenda))
            (enviados if ok else falhas).append(a)
    return enviados, falhas


def executa(agenda, simular, origem, execucao=None, previsto=None):
    """Uma execucao completa. Devolve a situacao final."""
    sid = int(QUESTIONARIO)
    ciclo_ano = int(CICLO)
    conexao = conecta()
    try:
        garante_tabelas(conexao)
        modo = "simulado" if simular else "real"
        inicio = agora(agenda)
        if execucao is None:
            execucao = abre_execucao(conexao, "disparo", modo, origem,
                                     iniciado=inicio)
        else:
            fecha_execucao(conexao, execucao, "em_execucao", iniciado=inicio)
        print(f"[{local(inicio)}] disparo {modo} ({origem}) · questionario "
              f"{sid} · ciclo {CICLO} · execucao {execucao}"
              + (f" · previsto para {local(previsto)}" if previsto else ""),
              flush=True)

        limite = (previsto or inicio) + timedelta(
            minutes=agenda.tolerancia_minutos)
        sql = consulta_texto(conexao)
        api = espera_plataforma(max(limite, inicio + timedelta(minutes=1)))
        try:
            motivos = guarda(api, sql, sid)
            if motivos:
                for m in motivos:
                    print(f"  BLOQUEADO: {m}", flush=True)
                fecha_execucao(conexao, execucao, "bloqueada",
                               {"motivos": motivos}, terminado=agora(agenda))
                return "bloqueada"
            print("  guarda: E19 (1 a 7) e condicoes da E20 conferidas",
                  flush=True)

            participantes = le_participantes(api, sql, sid)
            no_ciclo, fora = historico(conexao)
            momento = agora(agenda)
            p = cadencia.plano(participantes, agenda, ciclo_ano, momento,
                               no_ciclo, fora)
            resumo = p.resumo()
            print(f"  {len(participantes)} participantes · por estado: "
                  f"{json.dumps(resumo['por_estado'], ensure_ascii=False)}",
                  flush=True)
            print(f"  plano: {len(p.convites)} convite(s), "
                  f"{len(p.lembretes)} lembrete(s), {len(p.janelas)} janela(s)"
                  f" · sem envio: "
                  f"{json.dumps(resumo['sem_envio'], ensure_ascii=False)}",
                  flush=True)

            if simular:
                fecha_execucao(conexao, execucao, "simulada", resumo,
                               terminado=agora(agenda))
                return "simulada"

            falhas = 0
            coluna = colunas_dos_atributos(api, sid)[ATRIBUTO_VARIANTE]

            # 1. Convites. Depois de cada um, a janela de 60 dias, contada do
            # envio que a plataforma gravou — e nao do relogio desta rotina.
            ok, erro = envia(api, conexao, execucao, sid, p.convites,
                             "invite_participants",
                             lambda tids: [sid, tids, True, True], agenda)
            falhas += len(erro)
            for a in ok:
                gravado = api.chamar("get_participant_properties",
                                     [sid, a.tid, ["sent"]])
                envio = cadencia.instante_utc(gravado.get("sent"))
                if envio is None:
                    # Convite dado como enviado sem `sent` gravado: nao ha de
                    # onde contar a janela. Fica no log, para revisao.
                    print(f"  ATENCAO: tid {a.tid} convidado sem envio "
                          "gravado; janela nao aplicada", flush=True)
                    continue
                # Em UTC: a plataforma le validuntil em UTC (corrigido na E22).
                fim = envio + timedelta(days=agenda.janela_dias)
                api.chamar("set_participant_properties",
                           [sid, a.tid, {"validuntil": cadencia.texto_utc(fim)}])

            # 2. Janelas que faltavam (convite feito sem a janela gravada).
            for a in p.janelas:
                api.chamar("set_participant_properties",
                           [sid, a.tid, {"validuntil": a.validuntil}])

            # 3. Lembretes. O ramo e gravado ANTES, participante a
            # participante; quem nao teve o ramo gravado nao recebe, porque
            # sairia com o texto de quem nao iniciou (E20).
            prontos = []
            for a in p.lembretes:
                try:
                    api.chamar("set_participant_properties",
                               [sid, a.tid, {coluna: a.variante}])
                    prontos.append(a)
                except ErroAPI as e:
                    registra_envio(conexao, execucao, a, "falha",
                                   f"ramo nao gravado: {e}",
                                   quando=agora(agenda))
                    falhas += 1
            n = len(agenda.lembretes_dias)
            ok_l, erro_l = envia(api, conexao, execucao, sid, prontos,
                                 "remind_participants",
                                 lambda tids: [sid, None, n, tids, True],
                                 agenda)
            falhas += len(erro_l)

            resumo["enviados"] = {"convites": len(ok), "lembretes": len(ok_l)}
            resumo["falhas"] = falhas
            situacao = "concluida" if not falhas else "concluida_com_falhas"
            print(f"  enviados: {len(ok)} convite(s), {len(ok_l)} lembrete(s);"
                  f" falhas: {falhas}", flush=True)
            fecha_execucao(conexao, execucao, situacao, resumo,
                           terminado=agora(agenda))
            return situacao
        finally:
            api.fechar()
    except Bloqueio as e:
        print(f"  BLOQUEADO: {e}", flush=True)
        fecha_execucao(conexao, execucao, "bloqueada", {"motivos": [str(e)]},
                       terminado=agora(agenda))
        return "bloqueada"
    except Exception as e:  # noqa: BLE001 — registra qualquer falha e propaga
        if execucao is not None:
            fecha_execucao(conexao, execucao, "falha", erro=repr(e),
                           terminado=agora(agenda))
        raise
    finally:
        conexao.close()


def main():
    ap = argparse.ArgumentParser(description="Rotina de disparo (E21).")
    ap.add_argument("--simular", action="store_true",
                    help="calcula e registra o plano, sem enviar nem gravar "
                         "na plataforma")
    ap.add_argument("--execucao", type=int,
                    help="execucao ja reservada pelo agendador")
    ap.add_argument("--previsto-para",
                    help="horario previsto da execucao agendada (ISO)")
    args = ap.parse_args()

    if not QUESTIONARIO or not CICLO or not CICLO.isdigit():
        print("defina ROTINA_QUESTIONARIO e ROTINA_CICLO (ano do ciclo)",
              file=sys.stderr)
        return 2
    agenda = cadencia.carrega_agenda(AGENDA)
    for aviso in agenda.avisos:
        print(f"AVISO: {aviso}")

    origem = "agendada" if args.execucao else "manual"
    previsto = (datetime.fromisoformat(args.previsto_para)
                if args.previsto_para else None)
    if origem == "manual" and not args.simular and not agenda.dia_util(
            agora(agenda).date()):
        print("recusado: disparo real fora de dia util (secao 5.3)",
              file=sys.stderr)
        return 2
    situacao = executa(agenda, args.simular, origem, args.execucao, previsto)
    return 0 if situacao in ("concluida", "simulada") else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ErroAPI, pymysql.Error, cadencia.ErroAgenda) as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(1)
