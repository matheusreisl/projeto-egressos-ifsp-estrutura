#!/usr/bin/env python3
"""
Cenarios de simulacao pelo caminho real do respondente (E26).

Responde o questionario como um navegador sem JavaScript, por HTTP, pagina a
pagina, a partir do endereco individual — o mesmo caminho das conferencias da
E21 e da E22 (Formulario e Respondente de confere-consentimento.py). O que o
navegador faria pelo script da pagina, faz-se aqui de proposito: os campos de
relevancia (relevance<qid>) das perguntas que aparecem ou somem na mesma pagina,
porque sem eles a plataforma descarta a resposta em silencio (E21).

O que isto verifica, e o que nao. Os blocos que a PLATAFORMA serve — a pagina
seguinte e decidida no servidor, pelas regras de grupo — e o que ela GRAVA. A
exibicao dinamica dentro da pagina e do navegador, e e verificada no navegador
(matriz, R04.3). Os enunciados sao marcadores (CLAUDE.md, decisao 5); as
respostas sao sinteticas.

Cada cenario imprime os blocos servidos, o que ficou gravado e o estado que a
rotina da E21 le — sem nome, endereco nem token. Os cenarios estao em
docs/especificacao/simulacao.md, ligados aos itens da matriz de verificacao.

Uso, a partir da pasta infra/:

    python3 cenarios.py candidatos [--nivel tecnico|graduacao|pos_graduacao] [--n 5]
    python3 cenarios.py caminho C3 --identificador SIN-000123 [--sid N]
    python3 cenarios.py <cenario> --identificador SIN-000123 [--sid N]
    python3 cenarios.py lista
"""

import argparse
import importlib.util
import json
import os
import re
import sys
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))
sys.path.insert(0, os.path.join(AQUI, "instrumento"))

import instrumento  # noqa: E402


def _carrega(nome, arquivo):
    spec = importlib.util.spec_from_file_location(
        nome, os.path.join(AQUI, arquivo))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


cc = _carrega("confere_consentimento", "confere-consentimento.py")
cm = cc.cm                       # banco e caixas (E20)
sql = cm.sql
ENV = cc.ENV
DOMINIO = cc.DOMINIO

# Ordem dos blocos (navegacao-condicional.md, secao 2) e o prefixo do codigo.
BLOCOS = ["CON", "IDA", "AF", "AP", "SA", "EF", "PM", "MI", "AV", "EQ", "CT"]
# Perguntas que aparecem ou somem conforme outra da mesma pagina, ou do nivel
# confirmado: o navegador poria relevance=0 quando somem (secao 3.2).
CONDICIONAIS = {"CON2", "AP2", "SA2", "EF1", "EF2", "EF3"}
TEXTO_AF4 = "Sugestão sintética de ensaio: mais prática em laboratório e ênfase em projetos."

# ---------------------------------------------------------------------------
# Os dez caminhos (navegacao-condicional.md, secoes 5 e 11.1). As respostas
# que decidem o caminho estao nos comentarios; as demais variam so para que
# o registro nao seja todo igual.
# ---------------------------------------------------------------------------

COMUNS = {"AF1": "8", "AF2": "MEL", "AF3": "7", "AF4": TEXTO_AF4, "AV1": "7"}
EQUIDADE = {"EQ1": "PND", "EQ2": "PAR", "EQ3": "N", "EQ4": "6"}
PM = {"PM1": "TOT", "PM2": "8", "PM3": "F2", "PM4": "6", "PM5": "8",
      "PM6": "SER"}

CAMINHOS = {
    # recusas na pagina 1
    "C1": {"nivel": None, "r": {"CON1": "RCONS"}},
    "C2": {"nivel": None, "r": {"CON1": "RCONT"}},
    # tecnico; trabalhando, assalariado com carteira -> V; equidade
    "C3": {"nivel": "tecnico", "r": dict(
        COMUNS, **PM, **EQUIDADE, CON1="CONC", CON2="CONC", AP1="S",
        AP2="ACC", SA1="TRA", SA2="ACC", EF1="CON", EF2="IFSP", EF3="TOT",
        EF4=["ESP"])},
    # graduacao; so estudando -> VI; equidade
    "C4": {"nivel": "graduacao", "r": dict(
        COMUNS, **EQUIDADE, CON1="CONC", CON2="CONC", AP1="N", SA1="EST",
        EF1="MAT", EF2="OUT", EF3="PAR", EF4=["MD"], MI1="EST")},
    # pos; estudando e trabalhando, estagio remunerado -> V; IV so EF4
    "C5": {"nivel": "pos_graduacao", "r": dict(
        COMUNS, **PM, **EQUIDADE, CON1="CONC", CON2="CONC", AP1="N",
        SA1="ETR", SA2="ESTR", EF4=["MD"])},
    # pos; trabalhando em negocio familiar sem remuneracao -> VI (correcao E13)
    "C6": {"nivel": "pos_graduacao", "r": dict(
        COMUNS, **EQUIDADE, CON1="CONC", CON2="CONC", AP1="S", AP2="FAMN",
        SA1="TRA", SA2="FAMN", EF4=["EXT"], MI1="OUT")},
    # tecnico; CON2 nao; autonomo -> V; EF1 = nao (EF2 e EF3 somem)
    "C7": {"nivel": "tecnico", "r": dict(
        COMUNS, **PM, CON1="CONC", CON2="NCONC", AP1="N", SA1="TRA",
        SA2="AUT", EF1="NAO", EF4=["GRA"])},
    # graduacao; CON2 nao; nem trabalhando nem estudando -> VI
    "C8": {"nivel": "graduacao", "r": dict(
        COMUNS, CON1="CONC", CON2="NCONC", AP1="N", SA1="NEN", EF1="NAO",
        EF4=["NEN"], MI1="OFE")},
    # pos; CON2 nao; microempresario -> V; campus antecessor
    "C9": {"nivel": "pos_graduacao", "r": dict(
        COMUNS, **PM, CON1="CONC", CON2="NCONC", AP1="S", AP2="MICR",
        SA1="TRA", SA2="MICR", EF4=["NEN"], IDA3="ETFSP")},
    # pos; CON2 nao; estagio nao remunerado -> VI (correcao E13)
    "C10": {"nivel": "pos_graduacao", "r": dict(
        COMUNS, CON1="CONC", CON2="NCONC", AP1="N", SA1="TRA", SA2="ESTN",
        EF4=["ESP"], MI1="EXP")},
}


def blocos_esperados(r, nivel_confirmado):
    """Os blocos da secao 5, a partir das respostas que decidem."""
    if r.get("CON1") != "CONC":
        return ["CON"]
    remunerada = (r.get("SA1") in ("TRA", "ETR")
                  and r.get("SA2") not in ("ESTN", "FAMN"))
    saida = ["CON", "IDA", "AF", "AP", "SA", "EF",
             "PM" if remunerada else "MI", "AV"]
    if r.get("CON2") == "CONC":
        saida.append("EQ")
    return saida + ["CT"]


# ---------------------------------------------------------------------------
# A instancia: codigos, qids e nomes dos campos do formulario
# ---------------------------------------------------------------------------

class Instrumento:
    def __init__(self, sid):
        self.sid = sid
        linhas = sql(f"SELECT qid, parent_qid, title, type, gid FROM "
                     f"lime_questions WHERE sid={sid}")
        ordem = [l["gid"] for l in sql(
            f"SELECT gid FROM lime_groups WHERE sid={sid} ORDER BY group_order")]
        # O indice do grupo na ordem e o que a pagina marca em relevanceG<n>.
        self.grupo = {l["title"]: ordem.index(l["gid"]) for l in linhas
                      if l["parent_qid"] == "0"}
        self.qid = {l["title"]: l["qid"] for l in linhas
                    if l["parent_qid"] == "0"}
        self.codigo = {v: k for k, v in self.qid.items()}
        self.tipo = {l["title"]: l["type"] for l in linhas
                     if l["parent_qid"] == "0"}
        self.sub = {}   # codigo da pergunta -> {codigo da subpergunta: sqid}
        for l in linhas:
            if l["parent_qid"] != "0":
                pai = self.codigo.get(l["parent_qid"])
                self.sub.setdefault(pai, {})[l["title"]] = l["qid"]

    def coluna(self, codigo, sub=None):
        q = self.qid[codigo]
        return f"Q{q}_S{self.sub[codigo][sub]}" if sub else f"Q{q}"

    def grupo_da_pagina(self, html):
        """Indice do grupo servido, pelo marcador relevanceG<n>; None na
        pagina de encerramento. A pagina traz tambem campos de relevancia de
        perguntas de outras paginas que as regras citam (CON1, na pagina 2), e
        por isso o grupo nao sai das perguntas."""
        g = re.findall(r'name=["\']relevanceG(\d+)["\']', html)
        return int(g[0]) if g else None

    def na_pagina(self, html):
        """Codigos das perguntas do grupo servido."""
        g = self.grupo_da_pagina(html)
        qids = set(re.findall(r'name=["\']relevance(\d+)["\']', html))
        return [self.codigo[q] for q in qids if q in self.codigo
                and self.grupo[self.codigo[q]] == g]


# ---------------------------------------------------------------------------
# O respondente
# ---------------------------------------------------------------------------

class Percurso:
    """Uma sessao do respondente sobre o instrumento, pagina a pagina."""

    def __init__(self, inst, token):
        self.inst = inst
        self.r = cc.Respondente(token)
        self.r.abridor.addheaders = [("Accept-Language", "pt-BR")]
        self.servidos = []          # blocos na ordem em que foram servidos
        self.base = f"http://127.0.0.1:{cc.PORTA}/index.php"

    def abre(self):
        self.r.pagina = self.r.abridor.open(
            f"{self.base}/{self.inst.sid}?token={self.r.token}&lang=pt-BR"
            "&newtest=Y", timeout=60).read().decode("utf-8", "replace")
        self._anota()
        return self

    def codigos(self):
        return self.inst.na_pagina(self.r.pagina)

    def bloco(self):
        g = self.inst.grupo_da_pagina(self.r.pagina)
        return BLOCOS[g] if g is not None else None

    def _anota(self):
        b = self.bloco()
        if b:
            self.servidos.append(b)

    def ultima(self):
        return "movesubmit" in self.r.pagina

    def _campos(self, respostas):
        campos = dict(cc.le_formulario(self.r.pagina).campos)
        for cod in self.codigos():
            if cod in ("CONV", "CONDH", "IDA2"):
                continue
            q = self.inst.qid[cod]
            if cod in respostas:
                valor = respostas[cod]
                if isinstance(valor, list):
                    for s in self.inst.sub.get(cod, {}):
                        campos.pop(self.inst.coluna(cod, s), None)
                    for s in valor:
                        campos[self.inst.coluna(cod, s)] = "Y"
                else:
                    campos[f"Q{q}"] = valor
                campos[f"relevance{q}"] = "1"
            elif cod in CONDICIONAIS:
                campos[f"relevance{q}"] = "0"
                campos.pop(f"Q{q}", None)
        return campos

    def envia(self, respostas, move=None):
        """Envia a pagina atual com as respostas que lhe cabem."""
        move = move or ("movesubmit" if self.ultima() else "movenext")
        campos = self._campos(respostas)
        campos["move"] = move
        antes = self.bloco()
        self.r.pagina = self.r.abridor.open(urllib.request.Request(
            f"{self.base}/{self.inst.sid}",
            data=urllib.parse.urlencode(campos).encode()),
            timeout=60).read().decode("utf-8", "replace")
        depois = self.bloco()
        if move != "moveprev" and depois == antes and antes is not None:
            raise SystemExit(f"a pagina {antes} nao avancou: resposta "
                             "obrigatoria faltando ou validacao")
        self._anota()
        return self

    def volta(self, respostas):
        """Volta uma pagina, enviando a atual com os valores que ela tem —
        como o navegador, que nao apaga o que esta na tela ao voltar."""
        return self.envia(respostas, move="moveprev")

    def ate(self, respostas, parar_antes_de=None):
        """Responde pagina a pagina ate o fim, ou ate o bloco indicado ser
        servido (sem envia-lo)."""
        while self.bloco() is not None:
            if parar_antes_de and self.bloco() == parar_antes_de:
                return self
            self.envia(respostas)
        return self


# ---------------------------------------------------------------------------
# Leitura do que ficou
# ---------------------------------------------------------------------------

def participante(sid, identificador):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", identificador):
        raise SystemExit("identificador fora da regra do leiaute")
    linhas = sql(f"SELECT tid, token, participant_id, attribute_2 curso, "
                 f"attribute_3 nivel, attribute_4 campus, attribute_5 ano, "
                 f"sent, completed, emailstatus FROM lime_tokens_{sid} "
                 f"WHERE attribute_1='{identificador}'")
    if len(linhas) != 1:
        raise SystemExit(f"{len(linhas)} participante(s) com {identificador}")
    return linhas[0]


def respostas_gravadas(inst, token):
    """As respostas do participante, por codigo, so os campos preenchidos."""
    colunas = ["id", "submitdate", "lastpage"]
    nomes = {}
    for cod, q in inst.qid.items():
        if cod in inst.sub:
            for s in inst.sub[cod]:
                nomes[f"{cod}_{s}"] = f"Q{q}_S{inst.sub[cod][s]}"
        else:
            nomes[cod] = f"Q{q}"
    existentes = {l["Field"] for l in sql(
        f"SHOW COLUMNS FROM lime_responses_{inst.sid}")}
    sel = ", ".join(colunas + [f"{c} AS `{k}`" for k, c in nomes.items()
                               if c in existentes])
    saida = []
    for l in sql(f"SELECT {sel} FROM lime_responses_{inst.sid} "
                 f"WHERE token='{token}' ORDER BY id"):
        preenchidos = {k: v for k, v in l.items()
                       if k not in colunas and v not in (None, "")}
        saida.append({"id": l["id"], "enviada": bool(l["submitdate"]),
                      "lastpage": l["lastpage"], "campos": preenchidos})
    return saida


def blocos_gravados(campos):
    return sorted({re.sub(r"(\d+)(_\w+)?$", "", k) for k in campos
                   if not k.startswith(("CONV", "CONDH"))},
                  key=lambda b: BLOCOS.index(b) if b in BLOCOS else 99)


def estado(sid, tid):
    return cc.estados_da_rotina([int(tid)]).get(int(tid))


def relata(titulo, p, percurso, inst, extra=None):
    gravadas = respostas_gravadas(inst, p["token"])
    print(f"\n== {titulo}")
    print(f"  participante: tid {p['tid']} · nivel {p['nivel']}")
    if percurso:
        print(f"  blocos servidos: {' > '.join(percurso.servidos)}")
    for g in gravadas:
        cifr = {k: ("(texto)" if k == "AF4" else v)
                for k, v in g["campos"].items()
                if not k.startswith(("CT1", "CT2", "CT3"))}
        print(f"  resposta {g['id']}: {'enviada' if g['enviada'] else 'nao enviada'}"
              f", lastpage {g['lastpage']}; blocos gravados: "
              f"{' '.join(blocos_gravados(g['campos']))}")
        print(f"    {json.dumps(cifr, ensure_ascii=False, sort_keys=True)}")
    print(f"  estado na rotina: {estado(inst.sid, p['tid'])}")
    for linha in extra or []:
        print(f"  {linha}")
    return gravadas


# ---------------------------------------------------------------------------
# Cenarios
# ---------------------------------------------------------------------------

def caminho(inst, p, nome):
    c = CAMINHOS[nome]
    if c["nivel"] and p["nivel"] != c["nivel"]:
        raise SystemExit(f"{nome} pede nivel {c['nivel']}; o participante e "
                         f"{p['nivel']}")
    perc = Percurso(inst, p["token"]).abre().ate(c["r"])
    esperado = blocos_esperados(c["r"], p["nivel"])
    g = relata(f"caminho {nome}", p, perc, inst)
    falhas = []
    if perc.servidos != esperado:
        falhas.append(f"servidos {perc.servidos}, esperados {esperado}")
    final = [x for x in g if x["enviada"]]
    if len(final) != 1:
        falhas.append(f"{len(final)} respostas enviadas")
    else:
        b = blocos_gravados(final[0]["campos"])
        if "PM" in b and "MI" in b:
            falhas.append("Blocos V e VI gravados ao mesmo tempo")
        fora = [x for x in b if x not in esperado]
        if fora:
            falhas.append(f"gravado fora do caminho: {fora}")
    print("  RESULTADO: " + ("conforme" if not falhas else "; ".join(falhas)))
    return not falhas


def parcial(inst, p, _=None):
    """R05.2: envia ate o Bloco II (AP) e fecha, sem salvar."""
    r = dict(CAMINHOS["C3"]["r"]) if p["nivel"] == "tecnico" else dict(
        CAMINHOS["C4"]["r"])
    perc = Percurso(inst, p["token"]).abre().ate(r, parar_antes_de="SA")
    relata("parcial, sem salvar (interrompido depois do Bloco II)", p, perc,
           inst)


def reabre(inst, p, _=None):
    """R05.3: depois do parcial, abre o endereco em sessao nova e envia so a
    pagina 1 — sem carregar o salvo."""
    perc = Percurso(inst, p["token"]).abre()
    perc.envia({"CON1": "CONC", "CON2": "CONC"})
    relata("reabertura sem carregar: pagina 1 enviada de novo", p, perc, inst)


def volta_situacao(inst, p, _=None):
    """R04.6 (a): chega ao Bloco V, volta ate a situacao atual, muda para so
    estudando, e conclui."""
    r = dict(CAMINHOS["C3"]["r"])
    perc = Percurso(inst, p["token"]).abre().ate(r, parar_antes_de="AV")
    while perc.bloco() != "SA":        # PM -> EF -> SA
        perc.volta(r)
    novo = dict(r, SA1="EST", MI1="EST")
    novo.pop("SA2")
    for k in PM:
        novo.pop(k)
    perc.ate(novo)
    relata("voltar mudando a situacao atual (V -> VI)", p, perc, inst)


def volta_recusa(inst, p, _=None):
    """R04.6 (b): chega ao Bloco III, volta a pagina 1 e recusa o termo."""
    r = dict(CAMINHOS["C3"]["r"])
    perc = Percurso(inst, p["token"]).abre().ate(r, parar_antes_de="EF")
    while perc.bloco() != "CON":
        perc.volta(r)
    perc.envia({"CON1": "RCONS"})
    relata("voltar a pagina 1 e recusar o termo", p, perc, inst)


def volta_con2(inst, p, _=None):
    """R04.6 (c): chega ao contato com CON2 = concordo, volta a pagina 1, muda
    CON2 para nao concordo e conclui."""
    r = dict(CAMINHOS["C3"]["r"])
    perc = Percurso(inst, p["token"]).abre().ate(r, parar_antes_de="CT")
    while perc.bloco() != "CON":
        perc.volta(r)
    novo = {k: v for k, v in r.items() if k not in EQUIDADE}
    novo["CON2"] = "NCONC"
    perc.ate(novo)
    relata("voltar e retirar o consentimento especifico (CON2)", p, perc, inst)


def parcial_sensivel(inst, p, _=None):
    """R05.5: chega aos recortes de equidade e os envia; volta, muda a situacao
    e CON2, e abandona."""
    r = dict(CAMINHOS["C3"]["r"])
    perc = Percurso(inst, p["token"]).abre().ate(r, parar_antes_de="CT")
    while perc.bloco() != "SA":
        perc.volta(r)
    novo = {k: v for k, v in r.items() if k not in PM and k != "SA2"}
    novo.update(SA1="NEN")
    while perc.bloco() != "CON":
        perc.volta(novo)
    novo["CON2"] = "NCONC"
    perc.envia(novo)                   # pagina 1 enviada; abandona na 2
    relata("parcial com campos fora do caminho e dado sensivel retirado", p,
           perc, inst)


def correcao(inst, p, destino):
    """R03.4, R03.5 e R04.4: corrige o curso na pagina 2 (para o nivel
    `destino`) e o ano de conclusao, e conclui."""
    cursos = [c for c in instrumento.le_csv("cursos")
              if c["nivel"] == destino and c["codigo"] != p["curso"]]
    if not cursos:
        raise SystemExit(f"sem curso de nivel {destino}")
    r = dict(CAMINHOS["C3"]["r"], IDA1=cursos[0]["codigo"],
             IDA4=str(int(p["ano"]) - 1))
    if destino == "pos_graduacao":
        for k in ("EF1", "EF2", "EF3"):
            r.pop(k)
    perc = Percurso(inst, p["token"]).abre().ate(r)
    depois = participante(inst.sid, p["identificador"])
    relata(f"correcao do curso para {destino} e do ano", p, perc, inst, [
        f"atributos do participante depois: curso {depois['curso']}, nivel "
        f"{depois['nivel']}, ano {depois['ano']} (antes: {p['curso']}, "
        f"{p['nivel']}, {p['ano']})"])


def ct4(inst, p, _=None):
    """R09.4: conclui o caminho C3 marcando CT4 (recusa de contato nos
    proximos ciclos)."""
    r = dict(CAMINHOS["C3"]["r"], CT4=["RECT"])
    if p["nivel"] != "tecnico":
        raise SystemExit("ct4 usa o caminho C3: escolha um participante tecnico")
    perc = Percurso(inst, p["token"]).abre().ate(r)
    relata("conclusao com CT4 (recusa de contato nos proximos ciclos)", p,
           perc, inst)


def recusa_mensagem(inst, p, _=None):
    """R09.5: abre o endereco de recusa da mensagem que chegou a caixa e
    confirma."""
    msgs = cm.mensagens_do_token(cm.CAIXA_ENTREGUES, p["token"])
    if not msgs:
        raise SystemExit("nenhuma mensagem do participante na caixa")
    import email
    import email.policy
    html = cm.corpo_html(email.message_from_bytes(
        msgs[-1], policy=email.policy.default))
    links = [l.replace("&amp;", "&") for l in re.findall(r'href="([^"]+)"', html)
             if "optout" in l]
    if not links:
        raise SystemExit("a mensagem nao tem endereco de recusa")
    sessao = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(
        __import__("http.cookiejar").cookiejar.CookieJar()))
    url = links[0].replace("http://localhost", "http://127.0.0.1")
    pagina = sessao.open(url, timeout=60).read().decode("utf-8", "replace")
    antes = participante(inst.sid, p["identificador"])["emailstatus"]
    form = cc.le_formulario(pagina)
    acao = next((a for a in form.acoes if "removetoken" in a), None)
    if not acao:
        raise SystemExit(f"sem formulario de confirmacao: {form.acoes}")
    sessao.open(urllib.request.Request(
        f"http://127.0.0.1:{cc.PORTA}" + acao.replace("&amp;", "&"),
        data=urllib.parse.urlencode(form.campos).encode()), timeout=60).read()
    depois = participante(inst.sid, p["identificador"])["emailstatus"]
    b = sql("SELECT blacklisted FROM lime_participants WHERE participant_id="
            f"'{p['participant_id']}'")[0]["blacklisted"]
    relata("recusa pelo endereco da mensagem recebida", p, None, inst, [
        f"estado de entrega: {antes} ao abrir -> {depois} ao confirmar; "
        f"base central bloqueada: {b}"])


CENARIOS = {
    "parcial": parcial, "reabre": reabre, "volta-situacao": volta_situacao,
    "volta-recusa": volta_recusa, "volta-con2": volta_con2,
    "parcial-sensivel": parcial_sensivel, "ct4": ct4,
    "correcao-graduacao": lambda i, p, _: correcao(i, p, "graduacao"),
    "correcao-pos": lambda i, p, _: correcao(i, p, "pos_graduacao"),
    "recusa-mensagem": recusa_mensagem,
}


def candidatos(sid, nivel, n):
    """Convidados com entrega, sem resposta, sem endereco compartilhado."""
    filtro = f"AND t.attribute_3='{nivel}'" if nivel else ""
    return sql(
        f"SELECT t.tid, t.attribute_1 identificador, t.attribute_3 nivel "
        f"FROM lime_tokens_{sid} t WHERE t.sent<>'N' AND t.completed='N' AND "
        f"t.emailstatus='OK' AND t.email LIKE '%@{DOMINIO}' {filtro} AND "
        f"(SELECT COUNT(*) FROM lime_tokens_{sid} u WHERE u.email=t.email)=1 "
        f"AND NOT EXISTS (SELECT 1 FROM lime_responses_{sid} r WHERE "
        f"r.token=t.token) ORDER BY t.tid LIMIT {int(n)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("acao", help="candidatos, lista, caminho ou um cenario")
    ap.add_argument("caminho", nargs="?", help="C1 a C10, com a acao caminho")
    ap.add_argument("--identificador")
    ap.add_argument("--sid", type=int, default=int(
        ENV.get("ROTINA_QUESTIONARIO", "202615")))
    ap.add_argument("--nivel")
    ap.add_argument("--n", type=int, default=5)
    args = ap.parse_args()

    if args.acao == "lista":
        print("caminhos: " + ", ".join(CAMINHOS))
        print("cenarios: " + ", ".join(CENARIOS))
        return 0
    if args.acao == "candidatos":
        for l in candidatos(args.sid, args.nivel, args.n):
            print(f"  {l['identificador']}  tid {l['tid']}  {l['nivel']}")
        return 0
    if not args.identificador:
        raise SystemExit("--identificador e obrigatorio")
    inst = Instrumento(args.sid)
    p = participante(args.sid, args.identificador)
    p["identificador"] = args.identificador
    if args.acao == "caminho":
        return 0 if caminho(inst, p, args.caminho) else 1
    if args.acao not in CENARIOS:
        raise SystemExit(f"cenario desconhecido: {args.acao}")
    CENARIOS[args.acao](inst, p, None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
