#!/usr/bin/env python3
"""
Rotina de conformidade (E23). Tres deveres, nesta ordem:

  1. REGISTRAR cada recusa, com o que a P6 exige: data e hora, ciclo, versao do
     termo e via de manifestacao (parametros-contato.md, secao 8). As vias:

       tela        CON1 = "nao concordo neste ciclo" (consentimento) ou "nao
                   quero mais ser contatado" (contato), na pagina 1
       conclusao   CT4 marcado ao concluir: respondeu, e nao quer contato nos
                   proximos ciclos
       mensagem    o endereco de recusa do convite ou do lembrete (E20, E22)
       base central  bloqueio vindo de outro questionario ou ciclo

  2. LEVAR A RECUSA DE CONTATO A BASE CENTRAL. A recusa pela mensagem a
     plataforma ja leva; a feita na tela e por CT4 valia so no questionario do
     ciclo. Sem isto, quem pediu para nao ser mais contatado seria convidado no
     ciclo seguinte — e o termo promete o contrario. A rotina aplica a recusa
     PELA VIA DA PROPRIA PLATAFORMA: o mesmo endereco de confirmacao que a
     mensagem leva, confirmado por POST. Assim a base central e o participante
     sao marcados pelos modelos da plataforma, e a trilha de auditoria registra.
     A recusa de CONSENTIMENTO nao vai a base central: vale so no ciclo (P6).

  3. APAGAR DADO SENSIVEL GUARDADO SEM CONSENTIMENTO. A resposta interrompida
     guarda o que foi enviado, inclusive os recortes de equidade de quem deu o
     consentimento especifico, preencheu e depois o retirou — o descarte da
     plataforma so ocorre no envio final (E15). Resposta nao enviada com CON2
     diferente de "concordo" tem os campos do bloco apagados.

O que NAO faz: nao trata contato invalido, que nao e recusa (P8, secao 10.2) —
a rotina de devolucoes cuida dele e nao toca a base central; e nao revoga
recusa, que e do operador (infra/conformidade.py revogar).

Registro proprio, sem token, nome nem endereco:

  egressos_recusas         uma linha por manifestacao: participante (tid e
                           participant_id), tipo, via, momento e de onde ele
                           veio, versao do termo, quando chegou a base central,
                           e a revogacao
  egressos_higienizacoes   uma linha por resposta que teve dado sensivel apagado

Todo instante e gravado em ISO 8601 com o deslocamento, em UTC, como a
plataforma grava os seus (E22).

Duas escolhas de implementacao, com o motivo:

  - O momento da recusa pela mensagem vem da trilha de auditoria (AuditLog),
    que registra a mudanca do participante com data. A plataforma, sozinha, nao
    guarda quando a recusa aconteceu. Sem trilha, fica o momento em que a rotina
    a viu, marcado como "deteccao".
  - O apagamento do dado sensivel e por gravacao direta no banco: a API recusa
    alterar resposta quando o questionario nao permite edicao depois de
    concluido — e o instrumento nao permite, de proposito (update_response,
    conferido no codigo). Fica registrado em egressos_higienizacoes.

Roda sempre de verdade, qualquer que seja ROTINA_DISPARO: nao contata ninguem,
so protege. Uso, no conteiner rotinas:

    python3 conformidade.py               aplica
    python3 conformidade.py --simular     mostra o que faria, sem gravar
"""

import argparse
import http.cookiejar
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser

import pymysql

from disparar import BANCO, CICLO, QUESTIONARIO, consulta_texto

LIMESURVEY_URL = os.environ.get("LIMESURVEY_URL", "http://limesurvey").rstrip("/")
UTC = timezone.utc

DDL = [
    """CREATE TABLE IF NOT EXISTS egressos_recusas (
      id                INT AUTO_INCREMENT PRIMARY KEY,
      registrada_em     VARCHAR(32)  NOT NULL,
      questionario      INT          NOT NULL,
      ciclo             VARCHAR(20)  NOT NULL,
      tid               INT          NOT NULL,
      participant_id    VARCHAR(50)  NULL,
      resposta_id       INT          NOT NULL DEFAULT 0,
      tipo              VARCHAR(15)  NOT NULL,
      via               VARCHAR(15)  NOT NULL,
      manifestada_em    VARCHAR(32)  NOT NULL,
      fonte_do_momento  VARCHAR(20)  NOT NULL,
      versao_termo      VARCHAR(120) NULL,
      base_central_em   VARCHAR(32)  NULL,
      revogada_em       VARCHAR(32)  NULL,
      revogacao         TEXT         NULL,
      UNIQUE KEY uma_por_manifestacao
        (questionario, via, tid, resposta_id, manifestada_em),
      KEY por_pessoa (participant_id, tipo, revogada_em)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""",
    """CREATE TABLE IF NOT EXISTS egressos_higienizacoes (
      id            INT AUTO_INCREMENT PRIMARY KEY,
      executada_em  VARCHAR(32)  NOT NULL,
      questionario  INT          NOT NULL,
      resposta_id   INT          NOT NULL,
      campos        VARCHAR(200) NOT NULL
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""",
]

EQUIDADE = ("EQ1", "EQ2", "EQ3", "EQ4")


def agora_iso():
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def iso_utc(texto):
    """Data da plataforma (UTC, sem fuso no texto) em ISO 8601 com +00:00."""
    texto = (texto or "").strip()
    if not texto:
        return None
    if "T" in texto:                       # ja e ISO, como CONDH
        return texto
    return datetime.strptime(texto[:19], "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=UTC).isoformat()


# --- Leitura -----------------------------------------------------------------

def colunas(sql, sid):
    """Q<qid> de cada codigo — os nomes mudam a cada reimplantacao (E22) — e a
    coluna da caixa de CT4, que e subquestao: Q<qid>_S<sqid>."""
    por_codigo = {l["title"]: f"Q{l['qid']}" for l in sql(
        f"SELECT qid, title FROM lime_questions WHERE sid={sid} AND "
        "parent_qid=0 AND title IN ('CON1','CON2','CONV','CONDH','CT4',"
        + ",".join(f"'{c}'" for c in EQUIDADE) + ")")}
    sub = sql(f"SELECT q.qid, q.parent_qid FROM lime_questions q JOIN "
              "lime_questions p ON p.qid=q.parent_qid WHERE p.sid="
              f"{sid} AND p.title='CT4' AND q.title='RECT'")
    if sub:
        por_codigo["CT4_RECT"] = f"Q{sub[0]['parent_qid']}_S{sub[0]['qid']}"
    return por_codigo


def le_estado(sql, sid):
    c = colunas(sql, sid)
    eq = [c[e] for e in EQUIDADE if e in c]
    respostas = sql(
        f"SELECT r.id, r.token, r.submitdate, r.{c['CON1']} con1, "
        f"r.{c['CON2']} con2, r.{c['CONV']} conv, r.{c['CONDH']} condh"
        + (f", r.{c['CT4_RECT']} ct4" if "CT4_RECT" in c else ", NULL ct4")
        + "".join(f", r.{col} {col}" for col in eq)
        + f" FROM lime_responses_{sid} r")
    participantes = {l["token"]: l for l in sql(
        f"SELECT tid, token, participant_id, emailstatus FROM lime_tokens_{sid}")}
    bloqueados = {l["participant_id"] for l in sql(
        "SELECT participant_id FROM lime_participants WHERE blacklisted='Y'")}
    vigente = sql(f"SELECT a.value FROM lime_question_attributes a JOIN "
                  f"lime_questions q ON q.qid=a.qid WHERE q.sid={sid} AND "
                  "q.title='CONV' AND a.attribute='equation'")
    return {"colunas": c, "equidade": eq, "respostas": respostas,
            "participantes": participantes, "bloqueados": bloqueados,
            "versao_vigente": (vigente[0]["value"] if vigente else None)}


def momentos_da_auditoria(sql, sid):
    """Ultimo momento em que a trilha viu cada participante passar a OptOut,
    e cada pessoa passar a bloqueada — o ultimo, e nao o primeiro, porque depois
    de uma revogacao a recusa nova e a que importa. Vazio se a trilha nao
    existir."""
    if not sql("SHOW TABLES LIKE 'lime_auditlog_log'"):
        return {}, {}
    tokens = {int(l["entityid"]): iso_utc(l["m"]) for l in sql(
        "SELECT entityid, MAX(created) m FROM lime_auditlog_log WHERE "
        f"entity='token_{sid}' AND newvalues LIKE '%\"emailstatus\":\"OptOut%' "
        "GROUP BY entityid")}
    pessoas = {l["entityid"]: iso_utc(l["m"]) for l in sql(
        "SELECT entityid, MAX(created) m FROM lime_auditlog_log WHERE "
        "entity='participant' AND newvalues LIKE '%\"blacklisted\":\"Y\"%' "
        "GROUP BY entityid")}
    return tokens, pessoas


# --- 1. Registro ---------------------------------------------------------------

def manifestacoes(estado, auditoria, registradas):
    """As manifestacoes NOVAS que o estado da plataforma mostra, cada uma como
    dicionario pronto para o registro.

    "Nova" e a que ainda nao esta no registro. A distincao importa depois de
    uma revogacao: a resposta com a recusa antiga continua na plataforma, e nao
    pode nem voltar a contar como recusa aberta nem impedir que uma recusa
    posterior, pela mensagem, seja registrada."""
    ja = {(l["via"], int(l["tid"]), int(l["resposta_id"]), l["manifestada_em"])
          for l in registradas}
    saida = []
    for r in estado["respostas"]:
        p = estado["participantes"].get(r["token"])
        if p is None or not r["submitdate"]:
            continue
        base = {"tid": int(p["tid"]), "participant_id": p["participant_id"],
                "resposta_id": int(r["id"]), "versao_termo": r["conv"]}
        if r["con1"] in ("RCONS", "RCONT"):
            momento = r["condh"] or iso_utc(r["submitdate"])
            saida.append(dict(base, via="tela", manifestada_em=momento,
                              tipo="consentimento" if r["con1"] == "RCONS"
                              else "contato",
                              fonte_do_momento="CONDH" if r["condh"]
                              else "submitdate"))
        elif r["con1"] == "CONC" and (r["ct4"] or "") == "Y":
            saida.append(dict(base, via="conclusao", tipo="contato",
                              manifestada_em=iso_utc(r["submitdate"]),
                              fonte_do_momento="submitdate"))
    saida = [d for d in saida if (d["via"], d["tid"], d["resposta_id"],
                                  d["manifestada_em"]) not in ja]

    # Quem ja tem recusa de contato aberta — registrada e nao revogada, ou nova
    # nesta passada — nao ganha outra por estar bloqueado: o bloqueio e efeito
    # dela.
    abertas = {int(l["tid"]) for l in registradas
               if l["tipo"] == "contato" and not l["revogada_em"]}
    abertas |= {d["tid"] for d in saida if d["tipo"] == "contato"}
    tokens_aud, pessoas_aud = auditoria
    for p in estado["participantes"].values():
        tid, pid = int(p["tid"]), p["participant_id"]
        optout = str(p["emailstatus"] or "").startswith("OptOut")
        bloqueado = pid in estado["bloqueados"]
        if not (optout or bloqueado) or tid in abertas:
            continue
        if optout:
            via, momento = "mensagem", tokens_aud.get(tid)
        else:
            via, momento = "base central", pessoas_aud.get(pid)
        saida.append({"tid": tid, "participant_id": pid, "resposta_id": 0,
                      "tipo": "contato", "via": via,
                      "manifestada_em": momento or agora_iso(),
                      "fonte_do_momento": "auditoria" if momento else "deteccao",
                      "versao_termo": estado["versao_vigente"]})
    return saida


def registra(cur, sid, novas):
    feitas = 0
    for m in novas:
        try:
            cur.execute(
                """INSERT INTO egressos_recusas (registrada_em, questionario,
                   ciclo, tid, participant_id, resposta_id, tipo, via,
                   manifestada_em, fonte_do_momento, versao_termo)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (agora_iso(), sid, CICLO, m["tid"], m["participant_id"],
                 m["resposta_id"], m["tipo"], m["via"], m["manifestada_em"],
                 m["fonte_do_momento"], m["versao_termo"]))
            feitas += 1
        except pymysql.err.IntegrityError:
            pass                       # ja registrada: a rotina e idempotente
    return feitas


# --- 2. Base central -------------------------------------------------------------

class _Formulario(HTMLParser):
    def __init__(self):
        super().__init__()
        self.acoes, self.campos = [], {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "form":
            self.acoes.append(a.get("action") or "")
        elif tag == "input" and a.get("type") == "hidden" and a.get("name"):
            self.campos[a["name"]] = a.get("value") or ""


def recusa_global(sid, token):
    """Aplica a recusa global pela via da propria plataforma: abre a pagina de
    confirmacao que a mensagem leva e confirma por POST, com o token de
    protecao do formulario. Devolve None, ou o motivo da falha."""
    abridor = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        pagina = abridor.open(
            f"{LIMESURVEY_URL}/index.php/optout/participants?surveyid={sid}"
            f"&langcode=pt-BR&token={token}", timeout=60).read().decode(
                "utf-8", "replace")
        f = _Formulario()
        f.feed(pagina)
        acao = next((a for a in f.acoes if "removetoken" in a
                     and "global=1" in a), None)
        if acao is None:
            return "pagina sem confirmacao global (ja bloqueado?)"
        abridor.open(urllib.request.Request(
            LIMESURVEY_URL + acao.replace("&amp;", "&"),
            data=urllib.parse.urlencode(f.campos).encode()), timeout=60).read()
        return None
    except OSError as e:
        return f"plataforma: {e}"


def leva_a_base_central(cur, sql, sid, estado, simular, novas):
    """Para cada recusa de contato aberta que ainda nao chegou a base central.
    Na simulacao, as que seriam registradas nesta passada contam como abertas
    — o registro pode nem existir ainda."""
    por_tid = {int(p["tid"]): p for p in estado["participantes"].values()}
    abertas = []
    if sql("SHOW TABLES LIKE 'egressos_recusas'"):
        cur.execute("""SELECT id, tid, participant_id FROM egressos_recusas
                        WHERE questionario=%s AND tipo='contato'
                          AND revogada_em IS NULL AND base_central_em IS NULL""",
                    (sid,))
        abertas = list(cur.fetchall())
    if simular:
        abertas += [(None, m["tid"], m["participant_id"]) for m in novas
                    if m["tipo"] == "contato"]
    levadas, falhas = 0, []
    for rid, tid, pid in abertas:
        if pid not in estado["bloqueados"]:
            if simular:
                levadas += 1
                continue
            p = por_tid.get(int(tid))
            erro = recusa_global(sid, p["token"]) if p else "sem participante"
            bloqueado = sql("SELECT blacklisted FROM lime_participants WHERE "
                            f"participant_id='{pid}'")
            if erro or not bloqueado or bloqueado[0]["blacklisted"] != "Y":
                falhas.append(f"tid {tid}: {erro or 'bloqueio nao conferiu'}")
                continue
            estado["bloqueados"].add(pid)
        if not simular:
            cur.execute("UPDATE egressos_recusas SET base_central_em=%s "
                        "WHERE id=%s", (agora_iso(), rid))
        levadas += 1
    return levadas, falhas


# --- 3. Dado sensivel sem consentimento -------------------------------------------

def higieniza(cur, sid, estado, simular):
    feitas = 0
    for r in estado["respostas"]:
        if r["submitdate"] or (r["con2"] or "") == "CONC":
            continue
        preenchidos = [col for col in estado["equidade"] if r.get(col)]
        if not preenchidos:
            continue
        if not simular:
            cur.execute(f"UPDATE lime_responses_{sid} SET "
                        + ", ".join(f"{col}=NULL" for col in preenchidos)
                        + " WHERE id=%s AND submitdate IS NULL", (int(r["id"]),))
            cur.execute("""INSERT INTO egressos_higienizacoes (executada_em,
                           questionario, resposta_id, campos)
                           VALUES (%s,%s,%s,%s)""",
                        (agora_iso(), sid, int(r["id"]),
                         ",".join(preenchidos)))
        feitas += 1
    return feitas


def executa(simular=False):
    sid = int(QUESTIONARIO)
    conexao = pymysql.connect(**dict(BANCO, autocommit=True))
    try:
        sql = consulta_texto(conexao)
        with conexao.cursor() as cur:
            if not simular:
                for ddl in DDL:
                    cur.execute(ddl)
            estado = le_estado(sql, sid)
            registradas = sql(
                "SELECT tid, tipo, via, resposta_id, manifestada_em, "
                f"revogada_em FROM egressos_recusas WHERE questionario={sid}") \
                if sql("SHOW TABLES LIKE 'egressos_recusas'") else []
            novas = manifestacoes(estado, momentos_da_auditoria(sql, sid),
                                  registradas)
            feitas = len(novas) if simular else registra(cur, sid, novas)
            levadas, falhas = leva_a_base_central(cur, sql, sid, estado,
                                                  simular, novas)
            higienizadas = higieniza(cur, sid, estado, simular)
        resumo = {"recusas_registradas": feitas,
                  "levadas_a_base_central": levadas,
                  "respostas_higienizadas": higienizadas,
                  "falhas": falhas}
        print(f"conformidade{' (simulada)' if simular else ''} · questionario "
              f"{sid} · ciclo {CICLO}")
        print(f"recusas registradas: {feitas}; levadas a base central: "
              f"{levadas}; respostas higienizadas: {higienizadas}; falhas: "
              f"{len(falhas)}")
        for f in falhas:
            print(f"  FALHA {f}")
        print("RESUMO " + json.dumps(resumo, ensure_ascii=False))
        return 0 if not falhas else 1
    finally:
        conexao.close()


def main():
    ap = argparse.ArgumentParser(description="Rotina de conformidade (E23).")
    ap.add_argument("--simular", action="store_true",
                    help="mostra o que faria, sem gravar")
    args = ap.parse_args()
    if not QUESTIONARIO or not CICLO:
        print("defina ROTINA_QUESTIONARIO e ROTINA_CICLO", file=sys.stderr)
        return 2
    return executa(args.simular)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except pymysql.Error as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(1)
