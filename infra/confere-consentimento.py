#!/usr/bin/env python3
"""
Confere o consentimento eletronico (E22) contra o criterio da etapa: o aceite
persistido e recuperavel, com data e versao do termo.

Sem --exercitar, so le:

  1. o termo na instancia e o versionado em instrumento/termo.py: texto do
     termo, texto do consentimento especifico, opcoes de CON1 e CON2 e
     encerramento;
  2. a versao: o documento da pagina 1 RECONSTRUIDO A PARTIR DA INSTANCIA tem o
     mesmo resumo SHA-256 que a equacao CONV grava e que o arquivo da versao em
     instrumento/termos/ — a instancia mostra exatamente o texto arquivado.

Com --exercitar, o caminho real, por HTTP, na interface do respondente, com
seis participantes sinteticos do instrumento, e desfaz tudo ao fim:

  3. aceite com o consentimento especifico: CON1, CON2, versao e momento
     gravados, o momento em ISO 8601 com o fuso e dentro da janela do envio;
  4. aceite sem o consentimento especifico;
  5. o momento nao muda quando a pagina seguinte e enviada;
  6. recusa do termo neste ciclo: resposta encerrada que guarda a manifestacao,
     a versao e o momento, e o encerramento com o ramo certo;
  7. recusa de contato na tela: o mesmo, com o seu ramo;
  8. tudo recuperavel por consulta-consentimento.py, com o texto de cada versao
     conferido pelo resumo;
  9. a recusa pelo endereco da mensagem: abrir nao registra nada; confirmar
     (POST) marca o participante e a base central;
 10. o bloqueio impede convite e lembrete pela propria plataforma, neste e em
     OUTRO questionario — uma copia de ensaio com a mesma pessoa;
 11. a rotina da E21 le cada situacao no estado certo;
 12. limpeza.

Nada sai da maquina: o correio fica so na rede interna, e os enderecos estao sob
.test. Nenhum dado e de pessoa real.

Uso, a partir da pasta infra/:

    python3 confere-consentimento.py               (so leitura)
    python3 confere-consentimento.py --exercitar   (caminho real, e desfaz)
"""

import argparse
import contextlib
import hashlib
import http.cookiejar
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))
sys.path.insert(0, os.path.join(AQUI, "instrumento"))

import cadencia  # noqa: E402
import instrumento  # noqa: E402
import termo  # noqa: E402
from limesurvey_api import ErroAPI  # noqa: E402
from limesurvey_console import api_do_hospedeiro, carrega_env  # noqa: E402


def _carrega(nome, arquivo):
    spec = importlib.util.spec_from_file_location(
        nome, os.path.join(AQUI, arquivo))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


cm = _carrega("confere_mensagens", "confere-mensagens.py")      # banco e caixa
cc = _carrega("consulta_consentimento", "consulta-consentimento.py")

SID = instrumento.SID_INSTRUMENTO
ENV = carrega_env()
PORTA = ENV.get("PORTA_HTTP", "8080")
DOMINIO = ENV.get("CORREIO_DOMINIO", "egressos.test")
BASE = f"http://127.0.0.1:{PORTA}/index.php"
VERDE, VERMELHO, FIM = "\033[32m", "\033[31m", "\033[0m"

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
# Leitura
# ===========================================================================

def le_consentimento(sessao):
    """Textos, opcoes e equacoes do grupo do consentimento, como a instancia os
    guardou."""
    saida = {}
    for q in sessao.chamar("list_questions", [SID]):
        if q["title"] in ("CON1", "CON2", "CONV", "CONDH") and \
                int(q["parent_qid"]) == 0:
            p = sessao.chamar("get_question_properties", [int(q["qid"])])
            opcoes = p.get("answeroptions")
            if isinstance(opcoes, dict):
                opcoes = [(c, o["answer"]) for c, o in sorted(
                    opcoes.items(), key=lambda co: int(co[1]["order"]))]
            else:
                opcoes = []
            saida[q["title"]] = {"texto": p.get("question") or "",
                                 "opcoes": opcoes,
                                 "atributos": p.get("attributes") or {}}
    idioma = sessao.chamar("get_language_properties",
                           [SID, ["surveyls_endtext"], instrumento.IDIOMA])
    saida["fim"] = idioma.get("surveyls_endtext") or ""
    return saida


def confere_leitura(sessao):
    print(f"\nleitura (questionario {SID})")
    inst = le_consentimento(sessao)

    falhas = []
    if inst["CON1"]["texto"] != termo.TEXTO_TERMO:
        falhas.append("texto do termo (CON1) difere de termo.py")
    if inst["CON2"]["texto"] != termo.TEXTO_CON2:
        falhas.append("texto do consentimento especifico (CON2) difere")
    for cod in ("CON1", "CON2"):
        esperado = instrumento.resolve_opcoes(instrumento.campo(cod))
        if inst[cod]["opcoes"] != list(esperado):
            falhas.append(f"opcoes de {cod}: {inst[cod]['opcoes']}")
    if inst["fim"] != termo.ENCERRAMENTO:
        falhas.append("encerramento difere de termo.py")
    registra("termo, consentimento especifico, opcoes e encerramento iguais "
             "aos versionados", falhas, f"termo {termo.VERSAO}")

    # O documento reconstruido do que a instancia mostra, e nao de termo.py:
    # e isso que prova que o respondente ve o texto arquivado.
    doc = termo.documento(inst["CON1"]["opcoes"], inst["CON2"]["opcoes"])
    arquivado = termo.le_arquivado(termo.VERSAO)
    conv = (inst["CONV"]["atributos"].get("equation") or "").strip()
    falhas = []
    if arquivado is None:
        falhas.append(f"sem arquivo da versao {termo.VERSAO}")
    elif hashlib.sha256(arquivado.encode()).hexdigest() != termo.resumo(doc):
        falhas.append("o documento da instancia difere do arquivado")
    if conv != termo.identificacao(doc):
        falhas.append(f"CONV grava {conv!r}, e o documento da instancia da "
                      f"{termo.identificacao(doc)!r}")
    if inst["CONDH"]["atributos"].get("equation") != termo.EQUACAO_CONDH:
        falhas.append("equacao do momento (CONDH) difere")
    registra("versao: instancia, equacao e arquivo com o mesmo resumo", falhas,
             f"{conv[:24]}... = {os.path.relpath(termo.caminho_do_arquivo(), AQUI)}")


# ===========================================================================
# Caminho real
# ===========================================================================

class Formulario(HTMLParser):
    """Os campos de um formulario como o navegador os enviaria sem mexer em
    nada: ocultos (inclusive os de relevancia, com aspas simples), valores
    preenchidos, opcoes marcadas e selecionadas."""

    def __init__(self):
        super().__init__()
        self.campos, self.acoes, self._select = {}, [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "form":
            self.acoes.append(a.get("action") or "")
        elif tag == "input" and a.get("name"):
            tipo = (a.get("type") or "text").lower()
            if tipo in ("radio", "checkbox"):
                if "checked" in a:
                    self.campos[a["name"]] = a.get("value") or ""
            elif tipo not in ("submit", "button"):
                self.campos[a["name"]] = a.get("value") or ""
        elif tag == "select":
            self._select = a.get("name")
        elif tag == "option" and self._select and "selected" in a:
            self.campos[self._select] = a.get("value") or ""

    def handle_endtag(self, tag):
        if tag == "select":
            self._select = None


def le_formulario(html):
    f = Formulario()
    f.feed(html)
    return f


class Respondente:
    """Uma sessao do respondente, com os cookies, como um navegador sem
    JavaScript."""

    def __init__(self, token):
        self.token = token
        self.abridor = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.pagina = ""

    def abre(self):
        self.pagina = self.abridor.open(
            f"{BASE}/{SID}?token={self.token}&lang=pt-BR&newtest=Y",
            timeout=60).read().decode("utf-8", "replace")
        return self

    def envia(self, **valores):
        campos = dict(le_formulario(self.pagina).campos, move="movenext",
                      **valores)
        self.pagina = self.abridor.open(urllib.request.Request(
            f"{BASE}/{SID}", data=urllib.parse.urlencode(campos).encode()),
            timeout=60).read().decode("utf-8", "replace")
        return self


def nomes():
    """Q<qid> de cada codigo do consentimento: o campo do formulario e a coluna
    da resposta levam o qid, e nao o codigo (E15)."""
    return {l["title"]: f"Q{l['qid']}" for l in cm.sql(
        f"SELECT qid, title FROM lime_questions WHERE sid={SID} AND title IN "
        "('CON1','CON2','CONV','CONDH') AND parent_qid=0")}


def pagina_1(token, con1, con2=None):
    """Responde a pagina 1. Sem JavaScript, o navegador nao marcaria CON2 como
    relevante ao escolher "concordo" em CON1 — e a plataforma descartaria CON2
    em silencio. Marca-se, como o script da pagina faria."""
    n = nomes()
    valores = {n["CON1"]: con1}
    if con2 is not None:
        valores[n["CON2"]] = con2
        valores["relevance" + n["CON2"][1:]] = "1"
    return Respondente(token).abre().envia(**valores)


def texto_visivel(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(
        r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)))


def resposta(token):
    q = nomes()
    linhas = cm.sql(
        f"SELECT id, lastpage, submitdate, {q['CON1']} con1, {q['CON2']} con2, "
        f"{q['CONV']} conv, {q['CONDH']} condh FROM lime_responses_{SID} "
        f"WHERE token='{token}' ORDER BY id")
    return linhas


def estados_da_rotina(tids):
    """O estado de cada tid pela rotina da E21, de dentro do conteiner."""
    codigo = (
        "import json, cadencia, disparar\n"
        "from datetime import datetime\n"
        "from limesurvey_api import API\n"
        "c = disparar.conecta(); sql = disparar.consulta_texto(c)\n"
        "ag = cadencia.carrega_agenda(disparar.AGENDA)\n"
        "with API() as api:\n"
        f"    ps = disparar.le_participantes(api, sql, {SID})\n"
        "agora = datetime.now(ag.fuso)\n"
        f"alvo = {sorted(tids)!r}\n"
        "print(json.dumps({p.tid: cadencia.estado(p, agora, ag) "
        "for p in ps if p.tid in alvo}))\n")
    r = subprocess.run(["docker", "compose", "exec", "-T", "rotinas", "python3",
                        "-"], cwd=AQUI, input=codigo, capture_output=True,
                       text=True)
    if r.returncode != 0:
        raise SystemExit(f"rotina: {r.stderr.strip()}")
    return {int(k): v for k, v in json.loads(
        r.stdout.strip().splitlines()[-1]).items()}


CAMPOS = ("tid, token, participant_id, sent, remindersent, remindercount, "
          "completed, emailstatus, validuntil, usesleft, attribute_1, "
          "attribute_7")


def momento_ok(condh, antes, depois, falhas, quem):
    try:
        m = datetime.fromisoformat(condh)
    except (TypeError, ValueError):
        falhas.append(f"{quem}: momento {condh!r} nao e ISO 8601")
        return
    # A plataforma roda em UTC (internal.php): o momento sai com +00:00, e o que
    # importa e que o deslocamento esteja escrito.
    if m.utcoffset() is None:
        falhas.append(f"{quem}: momento sem deslocamento de fuso")
    elif m.utcoffset() != timedelta(0):
        falhas.append(f"{quem}: deslocamento {m.utcoffset()}, esperado +00:00")
    if not antes - timedelta(seconds=2) <= m <= depois + timedelta(seconds=2):
        falhas.append(f"{quem}: momento {condh} fora da janela do envio")


def fora_da_virada(minutos=10):
    """A rotina de conformidade (E23) roda a cada 30 minutos e age sobre as
    recusas plantadas aqui. Espera a virada passar, para que ela nao caia no
    meio do teste. A limpeza desfaz o efeito de qualquer modo."""
    passo = cadencia.carrega_agenda(os.path.join(
        AQUI, "rotinas", "configuracao", "agenda.json")
    ).conformidade_intervalo_minutos * 60
    falta = passo - time.time() % passo
    if falta < minutos * 60:
        print(f"  aguardando {falta + 60:.0f} s: a rotina de conformidade "
              "agendada cai durante o teste", flush=True)
        time.sleep(falta + 60)


def confere_exercicio(sessao):
    print(f"\ncaminho real (questionario {SID}, seis participantes sinteticos)")
    fora_da_virada()
    escolhidos = cm.sql(
        f"SELECT {CAMPOS} FROM lime_tokens_{SID} t WHERE email LIKE "
        f"'%@{DOMINIO}' AND sent='N' AND completed='N' AND emailstatus='OK' "
        f"AND (SELECT COUNT(*) FROM lime_tokens_{SID} u WHERE u.email=t.email)"
        "=1 ORDER BY tid LIMIT 6")
    if len(escolhidos) != 6:
        raise SystemExit("participantes insuficientes")
    por = dict(zip("ABCDEF", escolhidos))
    antes = {l["tid"]: l for l in cm.sql(f"SELECT {CAMPOS} FROM "
                                         f"lime_tokens_{SID}")}
    bloqueados_antes = cm.sql("SELECT COUNT(*) n FROM lime_participants "
                              "WHERE blacklisted='Y'")[0]["n"]
    print("  participantes (tid): " + ", ".join(
        f"{k}={v['tid']}" for k, v in por.items()))
    ident = termo.identificacao(termo.le_arquivado(termo.VERSAO))
    copia = None

    try:
        # --- 3 e 4. aceite, com e sem o consentimento especifico ----------
        falhas = []
        t0 = datetime.now(timezone.utc)
        pagina_1(por["A"]["token"], "CONC", "CONC")
        pagina_1(por["B"]["token"], "CONC", "NCONC")
        t1 = datetime.now(timezone.utc)
        for letra, con2 in (("A", "CONC"), ("B", "NCONC")):
            rs = [r for r in resposta(por[letra]["token"]) if r["con1"]]
            if len(rs) != 1:
                falhas.append(f"{letra}: {len(rs)} manifestacoes gravadas")
                continue
            r = rs[0]
            if (r["con1"], r["con2"], r["conv"]) != ("CONC", con2, ident):
                falhas.append(f"{letra}: gravado {r['con1']}/{r['con2']}/"
                              f"{r['conv']}")
            if r["submitdate"]:
                falhas.append(f"{letra}: resposta encerrada no aceite")
            momento_ok(r["condh"], t0, t1, falhas, letra)
        registra("aceite com e sem o consentimento especifico, com versao e "
                 "momento", falhas,
                 f"A: CONC/CONC, B: CONC/NCONC, termo {termo.VERSAO}, momento "
                 f"{resposta(por['A']['token'])[-1]['condh']}")

        # --- 5. o momento nao muda com a pagina seguinte ------------------
        falhas = []
        r = pagina_1(por["C"]["token"], "CONC", "CONC")
        primeiro = [x for x in resposta(por["C"]["token"]) if x["con1"]][0]
        time.sleep(3)
        r.envia()      # pagina 2, como veio: identificacao pre-preenchida
        depois = [x for x in resposta(por["C"]["token"]) if x["con1"]][0]
        if depois["lastpage"] in (None, "0", "1"):
            falhas.append(f"a pagina 2 nao foi aceita (lastpage "
                          f"{depois['lastpage']})")
        if depois["condh"] != primeiro["condh"]:
            falhas.append(f"momento mudou: {primeiro['condh']} -> "
                          f"{depois['condh']}")
        registra("o momento da manifestacao nao muda quando a pagina seguinte e "
                 "enviada", falhas,
                 f"{depois['condh']} mantido com lastpage {depois['lastpage']}")

        # --- 6 e 7. as duas recusas na tela -------------------------------
        for letra, con1, trecho, rotulo in (
                ("D", "RCONS", "No próximo ano, receberá um novo convite",
                 "recusa do termo neste ciclo"),
                ("E", "RCONT", "não receberá mais mensagens",
                 "recusa de contato na tela")):
            falhas = []
            t0 = datetime.now(timezone.utc)
            fim = texto_visivel(pagina_1(por[letra]["token"], con1).pagina)
            t1 = datetime.now(timezone.utc)
            rs = [x for x in resposta(por[letra]["token"]) if x["con1"]]
            if len(rs) != 1:
                falhas.append(f"{len(rs)} manifestacoes gravadas")
            else:
                x = rs[0]
                if (x["con1"], x["con2"], x["conv"]) != (con1, None, ident):
                    falhas.append(f"gravado {x['con1']}/{x['con2']}/{x['conv']}")
                if not x["submitdate"]:
                    falhas.append("resposta nao encerrada")
                momento_ok(x["condh"], t0, t1, falhas, letra)
            tok = cm.sql(f"SELECT completed FROM lime_tokens_{SID} WHERE "
                         f"tid={por[letra]['tid']}")[0]
            if tok["completed"] in ("N", None):
                falhas.append("participante nao marcado como concluido")
            if trecho not in fim:
                falhas.append("encerramento sem o ramo desta recusa")
            registra(f"{rotulo}: encerrada, com manifestacao, versao e momento "
                     "guardados", falhas,
                     f"{con1}, versao e momento mantidos; encerramento: "
                     f"\"{trecho}\"")

        # --- 8. recuperavel -------------------------------------------------
        falhas = []
        esperados = {"A": ("CONC", "CONC"), "B": ("CONC", "NCONC"),
                     "C": ("CONC", "CONC"), "D": ("RCONS", None),
                     "E": ("RCONT", None)}
        registros = {}
        for letra, (c1, c2) in esperados.items():
            reg = cc.consulta(sessao, SID, por[letra]["attribute_1"])
            registros[letra] = reg
            ms = reg["manifestacoes"] if reg else []
            if len(ms) != 1:
                falhas.append(f"{letra}: {len(ms)} manifestacoes recuperadas")
                continue
            m = ms[0]
            if (m["con1"], m["con2"]) != (c1, c2) or not m["momento"]:
                falhas.append(f"{letra}: recuperado {m['con1']}/{m['con2']}/"
                              f"{m['momento']}")
            if not m["texto_confere"]:
                falhas.append(f"{letra}: texto da versao nao confere")
        registra("recuperavel por identificador, com o texto da versao "
                 "conferido pelo resumo", falhas,
                 "5 de 5 por consulta-consentimento.py, pela exportacao da "
                 "plataforma")
        print("  exemplo de consulta:")
        for linha in _imprime(registros.get("A")):
            print(f"    | {linha}")

        # --- 9. recusa pelo endereco da mensagem ---------------------------
        f_tok, f_tid = por["F"]["token"], int(por["F"]["tid"])
        pid = por["F"]["participant_id"]

        def situacao_f():
            t = cm.sql(f"SELECT emailstatus FROM lime_tokens_{SID} WHERE "
                       f"tid={f_tid}")[0]["emailstatus"]
            b = cm.sql("SELECT blacklisted FROM lime_participants WHERE "
                       f"participant_id='{pid}'")[0]["blacklisted"]
            return t, b

        falhas = []
        sessao_f = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        pagina = sessao_f.open(f"{BASE}/optout/participants?surveyid={SID}"
                               f"&langcode=pt-BR&token={f_tok}",
                               timeout=60).read().decode("utf-8", "replace")
        if situacao_f() != ("OK", "N"):
            falhas.append(f"abrir registrou: {situacao_f()}")
        form = le_formulario(pagina)
        acao = next((a for a in form.acoes if "removetoken" in a), None)
        if not acao or "global=1" not in acao:
            falhas.append(f"sem formulario de confirmacao global: {form.acoes}")
        else:
            sessao_f.open(urllib.request.Request(
                "http://127.0.0.1:" + PORTA + acao.replace("&amp;", "&"),
                data=urllib.parse.urlencode(form.campos).encode()),
                timeout=60).read()
            if situacao_f() != ("OptOut", "Y"):
                falhas.append(f"confirmar registrou: {situacao_f()}")
        idioma = "Please confirm" in pagina
        registra("recusa pelo endereco da mensagem: abrir nao registra; "
                 "confirmar marca participante e base central", falhas,
                 "GET sem efeito; POST: OptOut e bloqueio"
                 + ("; a pagina pede a confirmacao em ingles" if idioma else ""))

        # --- 10. o bloqueio na plataforma, aqui e noutro questionario ------
        falhas = []

        def recusado(metodo, params):
            try:
                r = sessao.chamar(metodo, params)
                return f"enviou: {r}"
            except ErroAPI as e:
                return None if "No candidate tokens" in str(e) else str(e)

        erro = recusado("invite_participants", [SID, [f_tid], True, True])
        if erro:
            falhas.append(f"convite: {erro}")
        sessao.chamar("set_participant_properties",
                      [SID, f_tid, {"sent": "2026-01-01 10:00"}])
        erro = recusado("remind_participants", [SID, None, None, [f_tid], True])
        if erro:
            falhas.append(f"lembrete: {erro}")
        r = subprocess.run([sys.executable, os.path.join(
            AQUI, "instrumento", "instrumento.py"), "copia-de-ensaio"],
            cwd=AQUI, capture_output=True, text=True)
        m = re.search(r"questionario (\d+)", r.stdout)
        if r.returncode != 0 or not m:
            falhas.append(f"copia de ensaio: {r.stderr.strip()[-200:]}")
        else:
            copia = int(m.group(1))
            novo = sessao.chamar("add_participants", [copia, [{
                "firstname": "Ensaio", "lastname": "Recusa global",
                "email": f"recusa-global@{DOMINIO}",
                "participant_id": pid}], True])
            tid_copia = int(novo[0]["tid"])
            ligado = cm.sql(f"SELECT participant_id FROM lime_tokens_{copia} "
                            f"WHERE tid={tid_copia}")[0]["participant_id"]
            if ligado != pid:
                falhas.append("a copia nao guardou o elo com a base central")
            erro = recusado("invite_participants",
                            [copia, [tid_copia], True, True])
            if erro:
                falhas.append(f"outro questionario: {erro}")
        registra("o bloqueio impede convite e lembrete pela propria plataforma, "
                 "neste e em outro questionario", falhas,
                 "convite e lembrete no 202615 e convite na copia: "
                 "\"No candidate tokens\"")

        # --- 11. a rotina da E21 ------------------------------------------
        falhas = []
        estados = estados_da_rotina([int(v["tid"]) for v in por.values()])
        esperado = {"D": "recusa de consentimento", "E": "recusa de contato",
                    "F": "recusa de contato"}
        for letra, e in esperado.items():
            obtido = estados.get(int(por[letra]["tid"]))
            if obtido != e:
                falhas.append(f"{letra}: {obtido}, esperado {e}")
        registra("a rotina le as tres recusas no estado certo", falhas,
                 "D: recusa de consentimento; E (tela) e F (mensagem): "
                 "recusa de contato")
    finally:
        limpa(sessao, por, antes, bloqueados_antes, copia)


def _imprime(reg):
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        if reg:
            cc.imprime(reg)
    return saida.getvalue().splitlines()


def limpa(sessao, por, antes, bloqueados_antes, copia):
    """Cada passo independente: uma falha num nao impede os outros."""
    falhas = []
    tokens = [v["token"] for v in por.values()]
    pid_f = por["F"]["participant_id"]
    passos = [
        ("copia de ensaio", lambda: copia and subprocess.run(
            [sys.executable, os.path.join(AQUI, "instrumento",
                                          "instrumento.py"), "remover",
             "--sid", str(copia)], cwd=AQUI, check=True, capture_output=True)),
        ("respostas", lambda: [
            sessao.chamar("delete_response", [SID, int(r["id"])])
            for r in cm.sql(f"SELECT id FROM lime_responses_{SID} WHERE token "
                            "IN (" + ",".join(f"'{t}'" for t in tokens) + ")")]),
        ("participantes", lambda: [sessao.chamar(
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
        # A plataforma nao tem via de API para tirar alguem da lista de
        # bloqueio. Desfazer o teste, so ele, e por gravacao direta — de todos
        # os plantados, e nao so de F: a rotina de conformidade (E23) pode ter
        # levado a recusa de contato de E a base central no meio do teste.
        ("base central", lambda: cm.sql(
            "UPDATE lime_participants SET blacklisted='N' WHERE "
            "participant_id IN (" + ",".join(
                f"'{v['participant_id']}'" for v in por.values()) + ")")),
        ("registro de recusas", lambda: cm.sql(
            f"DELETE FROM egressos_recusas WHERE questionario={SID} AND tid IN ("
            + ",".join(v["tid"] for v in por.values()) + ")")
            if cm.sql("SHOW TABLES LIKE 'egressos_recusas'") else None),
        ("caixa", lambda: [cm.apaga(cm.CAIXA_ENTREGUES,
                                    ["HEADER", "X-tokenid", t]) for t in tokens]),
    ]
    for rotulo, passo in passos:
        try:
            passo()
        except (Exception, SystemExit) as ex:  # noqa: BLE001 — registra e segue
            falhas.append(f"limpeza de {rotulo}: {ex}")
    depois = {l["tid"]: l for l in cm.sql(f"SELECT {CAMPOS} FROM "
                                          f"lime_tokens_{SID}")}
    for tid, a in antes.items():
        for c in ("sent", "remindersent", "remindercount", "completed",
                  "emailstatus", "validuntil", "usesleft", "attribute_7"):
            if (depois[tid][c] or None) != (a[c] or None):
                falhas.append(f"tid {tid}: {c} {a[c]} -> {depois[tid][c]}")
    sobra = cm.sql(
        f"SELECT (SELECT COUNT(*) FROM lime_responses_{SID}) r, "
        "(SELECT COUNT(*) FROM lime_participants WHERE blacklisted='Y') b")[0]
    if sobra != {"r": "0", "b": bloqueados_antes}:
        falhas.append(f"sobrou: {sobra}")
    if copia and cm.sql(f"SELECT COUNT(*) n FROM lime_surveys WHERE "
                        f"sid={copia}")[0]["n"] != "0":
        falhas.append(f"a copia {copia} ficou")
    registra("limpeza", falhas,
             "500 participantes como antes, nenhuma resposta, nenhum bloqueio, "
             "copia removida")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--exercitar", action="store_true",
                    help="caminho real com seis participantes, e desfaz")
    args = ap.parse_args()
    print(f"consentimento eletronico do questionario {SID}")
    try:
        with api_do_hospedeiro() as sessao:
            confere_leitura(sessao)
            if args.exercitar:
                confere_exercicio(sessao)
    except ErroAPI as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    print(f"\n  {sum(resultados)} de {len(resultados)} conferencias passaram")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
