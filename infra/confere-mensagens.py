#!/usr/bin/env python3
"""
Confere os modelos de mensagem do instrumento (E20) e, com --enviar, o convite
de teste que chega a caixa.

Sem --enviar, so le. Confere:

  1. remetente e retorno do questionario: os de instrumento/mensagens.py, sob o
     dominio do .env, com caixa propria no correio — e nenhum deles "no-reply"
     nem endereco institucional (P7, secao 9.1);
  2. os modelos guardados na instancia sao exatamente os de mensagens.py;
  3. os modelos tem o que a especificacao exige: saudacao pelo nome, endereco
     individual, recusa de contato pela lista de bloqueio (P6), e nada de
     imagem nem de marcador desconhecido (sem rastreamento de abertura, P8);
  4. o atributo que escolhe o ramo do lembrete existe, com coluna, e o
     lembrete o referencia pelo numero certo.

Com --enviar, faz o caminho real com UM participante sintetico do instrumento,
sob o dominio de entrega, que ainda nao recebeu nada — e desfaz tudo ao fim:

  5. o convite chega a caixa coletora, com remetente, retorno e assunto certos,
     em HTML, com o nome do participante, sem marcador por resolver;
  6. o endereco individual da mensagem e o do participante e abre o
     questionario; o de recusa e o da lista de bloqueio, e abre a pagina de
     confirmacao — que nao e confirmada;
  7. o lembrete sai com o ramo certo para cada valor do atributo: pedido de
     primeira resposta para `convidado`, instrucao de retomada para
     `em_preenchimento`, e nunca os dois;
  8. a resposta humana ao remetente chega a caixa do remetente, e nao a das
     mensagens entregues;
  9. limpeza: o participante volta ao estado anterior (sem envio, sem
     lembrete, atributo original), nenhuma resposta criada, nenhuma recusa
     registrada e as mensagens de teste apagadas das caixas.

Nada sai da maquina: o correio fica so na rede interna, e o dominio e
reservado. Nenhum dado e de pessoa real.

Uso, a partir da pasta infra/:

    python3 confere-mensagens.py            (so leitura)
    python3 confere-mensagens.py --enviar   (com o convite de teste)
    python3 confere-mensagens.py --enviar --guardar DIR
                                            (guarda os .eml recebidos em DIR,
                                            fora do repositorio)
"""

import argparse
import base64
import email
import email.policy
import html as html_lib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))
sys.path.insert(0, os.path.join(AQUI, "instrumento"))

from limesurvey_api import ErroAPI  # noqa: E402
from limesurvey_console import api_do_hospedeiro, carrega_env  # noqa: E402

import instrumento  # noqa: E402
import mensagens  # noqa: E402

SID = instrumento.SID_INSTRUMENTO
IDIOMA = instrumento.IDIOMA
VERDE, VERMELHO, FIM = "\033[32m", "\033[31m", "\033[0m"

ENV = carrega_env()
DOMINIO = ENV.get("CORREIO_DOMINIO", "egressos.test")
CAIXA_ENTREGUES = ENV.get("CORREIO_CAIXA_ENTREGUES", "entregues")
CAIXA_DEVOLUCOES = ENV.get("CORREIO_CAIXA_DEVOLUCOES", "devolucoes")
CAIXA_REMETENTE = ENV.get("CORREIO_CAIXA_REMETENTE", "acompanhamento")
PORTA = ENV.get("PORTA_HTTP", "8080")

# Marcadores que os modelos podem usar. Qualquer outro e engano de digitacao,
# que a plataforma deixaria passar como texto literal.
MARCADORES = {"FIRSTNAME", "SURVEYURL", "GLOBALOPTOUTURL"}

resultados = []


def registra(numero, rotulo, falhas, evidencia=""):
    ok = not falhas
    resultados.append(ok)
    cor = VERDE if ok else VERMELHO
    print(f"  {cor}[{'ok' if ok else 'FALHA':5}]{FIM} {numero}. {rotulo}"
          + (f": {evidencia}" if ok and evidencia else ""))
    for f in falhas:
        print(f"           - {f}")


def sql(consulta):
    """Consulta pelo cliente do proprio conteiner do banco."""
    r = subprocess.run(
        ["docker", "compose", "exec", "-T", "banco", "mariadb", "--skip-ssl",
         "-B", f"-u{ENV['BANCO_USUARIO']}", f"-p{ENV['BANCO_SENHA']}",
         ENV["BANCO_NOME"], "-e", consulta],
        cwd=AQUI, capture_output=True, text=True, check=True)
    linhas = [l.split("\t") for l in r.stdout.rstrip("\n").split("\n") if l]
    if not linhas:
        return []
    return [dict(zip(linhas[0], [None if v == "NULL" else v for v in l]))
            for l in linhas[1:]]


# --- Caixas: so alcancaveis de dentro da rede interna ------------------------

def imap(caixa, codigo):
    """Roda `codigo` no conteiner rotinas com `m` logado em `caixa`; devolve o
    que o codigo imprimir em JSON."""
    programa = (
        "import imaplib, json, os, base64\n"
        "m = imaplib.IMAP4(os.environ['CORREIO_IMAP_HOST'], 143)\n"
        f"m.login({caixa!r}, os.environ['CORREIO_SENHA'])\n"
        "m.select('INBOX')\n" + codigo + "\nm.expunge(); m.logout()\n")
    r = subprocess.run(["docker", "compose", "exec", "-T", "rotinas",
                        "python3", "-"], cwd=AQUI, input=programa,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"caixa {caixa}: {r.stderr.strip()}")
    return json.loads(r.stdout.strip().splitlines()[-1])


def mensagens_do_token(caixa, token):
    """Mensagens da caixa com o cabecalho X-tokenid do participante, cruas."""
    return [base64.b64decode(c) for c in imap(caixa, (
        f"_, d = m.search(None, 'HEADER', 'X-tokenid', {token!r})\n"
        "out = []\n"
        "for i in d[0].split():\n"
        "    _, c = m.fetch(i, '(RFC822)')\n"
        "    out.append(base64.b64encode(c[0][1]).decode())\n"
        "print(json.dumps(out))"))]


def apaga(caixa, criterio):
    return imap(caixa, (
        f"_, d = m.search(None, *{criterio!r})\n"
        "ids = d[0].split()\n"
        "for i in ids: m.store(i, '+FLAGS', '\\\\Deleted')\n"
        "print(json.dumps(len(ids)))"))


def aguarda(caixa, token, quantas, limite=120):
    inicio = time.time()
    while True:
        achadas = mensagens_do_token(caixa, token)
        if len(achadas) >= quantas or time.time() - inicio > limite:
            return achadas
        time.sleep(5)


def corpo_html(msg):
    parte = msg.get_body(preferencelist=("html",))
    return parte.get_content() if parte is not None else ""


def texto_visivel(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.status, r.read().decode("utf-8", "replace")


# --- Conferencias de leitura -------------------------------------------------

def confere_leitura(sessao):
    props = sessao.chamar("get_survey_properties", [
        SID, ["admin", "adminemail", "bounce_email", "attributedescriptions",
              "htmlemail"]])
    idioma = sessao.chamar("get_language_properties", [SID, [
        "surveyls_email_invite_subj", "surveyls_email_invite",
        "surveyls_email_remind_subj", "surveyls_email_remind"], IDIOMA])

    # 1. Remetente e retorno
    falhas = []
    esperado = mensagens.propriedades_do_questionario()
    for campo, valor in esperado.items():
        if props.get(campo) != valor:
            falhas.append(f"{campo} = {props.get(campo)!r}, esperado {valor!r}")
    if mensagens.REMETENTE != f"{CAIXA_REMETENTE}@{DOMINIO}":
        falhas.append(f"remetente {mensagens.REMETENTE} nao e a caixa do "
                      f"remetente do .env ({CAIXA_REMETENTE}@{DOMINIO})")
    if mensagens.DEVOLUCOES != f"{CAIXA_DEVOLUCOES}@{DOMINIO}":
        falhas.append(f"retorno {mensagens.DEVOLUCOES} nao e a caixa de "
                      f"devolucoes do .env ({CAIXA_DEVOLUCOES}@{DOMINIO})")
    for endereco in (mensagens.REMETENTE, mensagens.DEVOLUCOES):
        if re.search(r"n[aã]o.?responda|no.?reply", endereco, re.I):
            falhas.append(f"{endereco}: remetente sem retorno e vedado (P7)")
        if not endereco.endswith(".test"):
            falhas.append(f"{endereco}: fora do dominio reservado (secao 9.1)")
    if props.get("htmlemail") != "Y":
        falhas.append("mensagens nao estao em HTML")
    registra(1, "remetente e retorno", falhas,
             f"{props.get('admin')} <{props.get('adminemail')}>, retorno "
             f"{props.get('bounce_email')}")

    # 2. Modelos guardados = modelos versionados
    n = instrumento.numero_da_variante()
    falhas = [f"{campo} difere de mensagens.py"
              for campo, valor in mensagens.propriedades_de_idioma(n).items()
              if idioma.get(campo) != valor]
    registra(2, "modelos da instancia iguais aos versionados", falhas,
             "convite e lembrete, assunto e corpo")

    # 3. Elementos exigidos
    falhas = []
    for nome, corpo in (("convite", mensagens.CORPO_CONVITE),
                        ("lembrete", mensagens.corpo_lembrete(n))):
        for marcador in ("{FIRSTNAME}", "{SURVEYURL}", "{GLOBALOPTOUTURL}"):
            if marcador not in corpo:
                falhas.append(f"{nome}: falta {marcador}")
        desconhecidos = set(re.findall(r"\{([A-Z_]+)\}", corpo)) - MARCADORES
        if desconhecidos:
            falhas.append(f"{nome}: marcador desconhecido {desconhecidos}")
        if re.search(r"<img|{OPTOUTURL}", corpo, re.I):
            falhas.append(f"{nome}: imagem ou recusa so deste questionario")
    for assunto in (mensagens.ASSUNTO_CONVITE, mensagens.ASSUNTO_LEMBRETE):
        if not assunto.startswith("IFSP") or re.search(r"\d", assunto):
            falhas.append(f"assunto sem instituicao ou com ano/numero: {assunto}")
    registra(3, "elementos exigidos pela especificacao", falhas,
             "nome, endereco individual, recusa de contato, sem imagem")

    # 4. Atributo do ramo
    falhas = []
    coluna = instrumento.coluna_do_atributo(mensagens.ATRIBUTO_VARIANTE)
    descricoes = json.loads(props.get("attributedescriptions") or "{}")
    if (descricoes.get(coluna) or {}).get("description") != \
            mensagens.ATRIBUTO_VARIANTE:
        falhas.append(f"{coluna} nao descrito como {mensagens.ATRIBUTO_VARIANTE}")
    colunas = {l["COLUMN_NAME"] for l in sql(
        "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE "
        f"TABLE_NAME='lime_tokens_{SID}' AND TABLE_SCHEMA=DATABASE()")}
    if coluna not in colunas:
        falhas.append(f"tabela de participantes sem a coluna {coluna}")
    if f"TOKEN:ATTRIBUTE_{n} ==" not in mensagens.corpo_lembrete(n):
        falhas.append("lembrete nao referencia o atributo do ramo")
    registra(4, "atributo que escolhe o ramo do lembrete", falhas,
             f"{coluna} = {mensagens.ATRIBUTO_VARIANTE}")


# --- Envio de teste ----------------------------------------------------------

CAMPOS = "tid, token, firstname, email, emailstatus, sent, remindersent, " \
         "remindercount, completed, usesleft"


def escolhe_participante(coluna):
    linhas = sql(
        f"SELECT {CAMPOS}, {coluna} AS variante FROM lime_tokens_{SID} "
        f"WHERE email LIKE '%@{DOMINIO}' AND emailstatus='OK' AND sent='N' "
        "AND remindersent='N' AND completed='N' ORDER BY tid LIMIT 1")
    if not linhas:
        raise SystemExit("nenhum participante sem envio sob o dominio de entrega")
    return linhas[0]


def confere_envio(sessao, guardar=None):
    coluna = instrumento.coluna_do_atributo(mensagens.ATRIBUTO_VARIANTE)
    p = escolhe_participante(coluna)
    tid, token, nome = int(p["tid"]), p["token"], p["firstname"]
    respostas_antes = sql(f"SELECT COUNT(*) n FROM lime_responses_{SID}")[0]["n"]
    ids_antes = {r["id"] for r in sql(
        f"SELECT id FROM lime_responses_{SID} WHERE token='{token}'")}
    bloqueados_antes = sql("SELECT COUNT(*) n FROM lime_participants "
                           "WHERE blacklisted='Y'")[0]["n"]
    print(f"\n  participante de teste: tid {tid} (sintetico, @{DOMINIO})")

    try:
        # 5. Convite
        sessao.chamar("invite_participants", [SID, [tid]])
        achadas = aguarda(CAIXA_ENTREGUES, token, 1)
        falhas = []
        if len(achadas) != 1:
            raise SystemExit(f"convite nao chegou ({len(achadas)} mensagens)")
        msg = email.message_from_bytes(achadas[0], policy=email.policy.default)
        de = msg["From"].addresses[0]
        if (de.display_name, de.addr_spec) != (mensagens.REMETENTE_NOME,
                                               mensagens.REMETENTE):
            falhas.append(f"From = {msg['From']}")
        if msg["Return-Path"] != f"<{mensagens.DEVOLUCOES}>":
            falhas.append(f"Return-Path = {msg['Return-Path']}")
        if str(msg["Subject"]) != mensagens.ASSUNTO_CONVITE:
            falhas.append(f"Subject = {msg['Subject']}")
        html = corpo_html(msg)
        if not html:
            falhas.append("sem parte HTML")
        visivel = texto_visivel(html)
        if f"Olá, {nome}." not in visivel:
            falhas.append("saudacao sem o nome inteiro do participante")
        if re.search(r"\{[A-Z:_]+\}|@@\w+@@", html):
            falhas.append("marcador por resolver no corpo")
        if "educação continuada" not in visivel:
            falhas.append("sem a contrapartida institucional")
        registra(5, "convite chega formatado", falhas,
                 f"de {de.addr_spec}, retorno {msg['Return-Path']}, "
                 f"\"{msg['Subject']}\"")

        # 6. Enderecos da mensagem
        falhas = []
        links = {html_lib.unescape(u)
                 for u in re.findall(r'href="([^"]+)"', html)}
        acesso = [u for u in links if f"/{SID}" in u and "token=" in u
                  and "optout" not in u]
        recusa = [u for u in links if "/optout/participants" in u]
        if len(acesso) != 1:
            falhas.append(f"enderecos de acesso: {len(acesso)}")
        else:
            q = urllib.parse.parse_qs(urllib.parse.urlparse(acesso[0]).query)
            if q.get("token") != [token] or q.get("lang") != [IDIOMA]:
                falhas.append(f"endereco de acesso nao e o do participante: "
                              f"{acesso[0]}")
            status, pagina = get(acesso[0])
            if status != 200 or "CON1" not in pagina:
                falhas.append(f"endereco de acesso nao abre o questionario "
                              f"(HTTP {status})")
            # Achado da E20: so ABRIR o endereco ja cria resposta parcial, com
            # lastpage 0 — o participante passa de `convidado` a `em
            # preenchimento` sem responder nada. A limpeza a apaga.
            criadas = sql(f"SELECT id, lastpage FROM lime_responses_{SID} "
                          f"WHERE token='{token}' AND submitdate IS NULL")
            if criadas:
                print(f"           (abrir o endereco criou {len(criadas)} "
                      f"resposta parcial, lastpage {criadas[0]['lastpage']})")
        if len(recusa) != 1 or f"token={token}" not in recusa[0].replace(
                "/token/", "token=").replace("token/", "token="):
            falhas.append(f"endereco de recusa ausente ou alheio: {recusa}")
        else:
            status, pagina = get(recusa[0])
            # So GET: a pagina pede confirmacao e a recusa exige POST, que
            # este teste nao faz (OptoutController, conferido no codigo).
            if status != 200 or "<form" not in pagina:
                falhas.append(f"recusa nao abre a confirmacao (HTTP {status})")
        registra(6, "endereco individual e endereco de recusa", falhas,
                 "acesso abre o termo; recusa abre a confirmacao, nao confirmada")

        # 7. Lembrete, um envio por ramo
        falhas = []
        ramos = {}
        for i, variante in enumerate((mensagens.VARIANTE_CONVIDADO,
                                      mensagens.VARIANTE_EM_PREENCHIMENTO), 2):
            sessao.chamar("set_participant_properties",
                          [SID, tid, {coluna: variante}])
            sessao.chamar("remind_participants", [SID, None, None, [tid]])
            achadas = aguarda(CAIXA_ENTREGUES, token, i)
            if len(achadas) != i:
                falhas.append(f"lembrete {variante} nao chegou")
                continue
            ultimas = [email.message_from_bytes(a, policy=email.policy.default)
                       for a in achadas]
            lembrete = [m for m in ultimas
                        if str(m["Subject"]) == mensagens.ASSUNTO_LEMBRETE]
            ramos[variante] = texto_visivel(corpo_html(lembrete[-1]))
        retomada = "Carregar questionário não finalizado"
        primeira = "ainda não recebemos a sua resposta"
        c = ramos.get(mensagens.VARIANTE_CONVIDADO, "")
        e = ramos.get(mensagens.VARIANTE_EM_PREENCHIMENTO, "")
        if primeira not in c or retomada in c:
            falhas.append("ramo convidado errado")
        if retomada not in e or primeira in e or "novo preenchimento" not in e:
            falhas.append("ramo em_preenchimento errado")
        for nome_ramo, texto in ramos.items():
            if f"Olá, {nome}." not in texto or "{" in texto:
                falhas.append(f"{nome_ramo}: saudacao ou marcador")
        registra(7, "lembrete com o ramo certo para cada valor", falhas,
                 "convidado pede resposta; em_preenchimento ensina a retomar")
        if guardar:
            os.makedirs(guardar, exist_ok=True)
            for i, cru in enumerate(mensagens_do_token(CAIXA_ENTREGUES,
                                                       token), 1):
                with open(os.path.join(guardar, f"mensagem-{i}.eml"),
                          "wb") as fh:
                    fh.write(cru)
            print(f"           (mensagens guardadas em {guardar})")

        # 8. Resposta humana ao remetente
        falhas = []
        marca = f"resposta-teste-{token}"
        r = subprocess.run(["docker", "compose", "exec", "-T", "rotinas",
                            "python3", "-"], cwd=AQUI, capture_output=True,
                           text=True, input=(
            "import smtplib\nfrom email.message import EmailMessage\n"
            "m = EmailMessage()\n"
            f"m['From'] = {p['email']!r}\nm['To'] = {mensagens.REMETENTE!r}\n"
            f"m['Subject'] = 'Re: ' + {mensagens.ASSUNTO_CONVITE!r}\n"
            f"m['X-tokenid'] = {marca!r}\n"
            "m.set_content('Resposta de teste.')\n"
            "with smtplib.SMTP('correio', 25) as s: s.send_message(m)\n"))
        if r.returncode != 0:
            falhas.append(f"envio da resposta: {r.stderr.strip()}")
        else:
            no_remetente = aguarda(CAIXA_REMETENTE, marca, 1, limite=60)
            nas_entregues = mensagens_do_token(CAIXA_ENTREGUES, marca)
            if len(no_remetente) != 1 or nas_entregues:
                falhas.append(f"resposta: {len(no_remetente)} na caixa do "
                              f"remetente, {len(nas_entregues)} nas entregues")
        registra(8, "resposta humana chega a caixa do remetente", falhas,
                 f"caixa {CAIXA_REMETENTE}, separada das entregues")
    finally:
        # 9. Limpeza — sempre, mesmo com falha no meio, e cada passo
        # independente dos outros: uma falha num nao pode deixar os demais
        # por fazer.
        falhas = []
        apagadas = 0
        passos = [
            ("participante", lambda: sessao.chamar(
                "set_participant_properties", [SID, tid, {
                    "sent": p["sent"], "remindersent": p["remindersent"],
                    "remindercount": int(p["remindercount"]),
                    coluna: p["variante"] or ""}])),
            ("respostas", lambda: [
                sessao.chamar("delete_response", [SID, int(r["id"])])
                for r in sql(f"SELECT id FROM lime_responses_{SID} "
                             f"WHERE token='{token}'")
                if r["id"] not in ids_antes]),
            ("caixa entregues", lambda: apaga(
                CAIXA_ENTREGUES, ["HEADER", "X-tokenid", token])),
            ("caixa do remetente", lambda: apaga(
                CAIXA_REMETENTE, ["HEADER", "X-tokenid",
                                  f"resposta-teste-{token}"])),
        ]
        for rotulo, passo in passos:
            try:
                r = passo()
                if isinstance(r, int):
                    apagadas += r
            except Exception as ex:  # noqa: BLE001 — registra e segue
                falhas.append(f"limpeza de {rotulo}: {ex}")
    depois = sql(f"SELECT {CAMPOS}, {coluna} AS variante FROM "
                 f"lime_tokens_{SID} WHERE tid={tid}")[0]
    # Atributo vazio e nulo sao o mesmo estado: a API grava "" onde a
    # importacao deixou NULL.
    for campo in ("sent", "remindersent", "remindercount", "emailstatus",
                  "completed", "usesleft", "variante"):
        if (depois.get(campo) or None) != (p.get(campo) or None):
            falhas.append(f"{campo}: {p.get(campo)} -> {depois.get(campo)}")
    if sql(f"SELECT COUNT(*) n FROM lime_responses_{SID}")[0]["n"] \
            != respostas_antes:
        falhas.append("o teste criou resposta")
    if sql("SELECT COUNT(*) n FROM lime_participants WHERE blacklisted='Y'"
           )[0]["n"] != bloqueados_antes:
        falhas.append("o teste registrou recusa de contato")
    if mensagens_do_token(CAIXA_ENTREGUES, token):
        falhas.append("mensagens de teste ficaram na caixa")
    registra(9, "limpeza", falhas,
             f"participante restaurado, {apagadas} mensagens apagadas, "
             "nenhuma resposta, nenhuma recusa")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--enviar", action="store_true",
                    help="faz o convite de teste e o desfaz")
    ap.add_argument("--guardar", metavar="DIR",
                    help="guarda as mensagens recebidas, antes da limpeza")
    args = ap.parse_args()
    print(f"modelos de mensagem do questionario {SID}")
    try:
        with api_do_hospedeiro() as sessao:
            confere_leitura(sessao)
            if args.enviar:
                confere_envio(sessao, args.guardar)
    except ErroAPI as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    print(f"\n  {sum(resultados)} de {len(resultados)} conferencias passaram")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
