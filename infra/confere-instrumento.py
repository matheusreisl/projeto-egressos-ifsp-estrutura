#!/usr/bin/env python3
"""
Confere o instrumento implantado na instancia contra a especificacao (E15).

A conferencia e INDEPENDENTE do gerador: nao le instrumento/estrutura.py. Le a
especificacao direto dos documentos — a secao 12.3 de blocos-instrumento.md
(E13) e as secoes 2 e 5 de navegacao-condicional.md (E14) — e o que a
instancia guardou, pela API. Um erro de transcricao no gerador aparece aqui
como divergencia, em vez de se confirmar a si mesmo.

O que confere:

  1. os onze grupos, na ordem da secao 2 da E14;
  2. os 35 campos da secao 12.3 da E13: codigo, grupo, tipo, obrigatoriedade e
     dominio — opcao por opcao, pelo rotulo;
  3. as listas de configuracao versionada contra configuracao/;
  4. o nivel derivado do curso (IDA2) para cada curso da lista;
  5. as expressoes de validacao de contato contra exemplos validos e invalidos;
  6. os dez caminhos da secao 5 da E14, avaliando as expressoes de exibicao QUE
     ESTAO NA INSTANCIA sobre todas as combinacoes das respostas que decidem o
     caminho — a mesma enumeracao da secao 8 da E14, que deu 2.802;
  7. o pre-preenchimento (E18): cada campo da identificacao aponta para o
     atributo do participante que tem o seu nome, e o derivado nao tem padrao.

Na avaliacao, reproduz a regra do Expression Manager conferida em
em_core_helper.php: expressao de exibicao que cita questao OCULTA, sem o sufixo
.NAOK, vale falso.

O que NAO confere: a exibicao dinamica na mesma pagina e o comportamento do
preenchimento — sao do percurso manual (navegacao-condicional.md, secao 11).

Uso, a partir da pasta infra/:

    python3 confere-instrumento.py [--sid 202615]
"""

import argparse
import csv
import itertools
import json
import os
import re
import sys
import unicodedata
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from limesurvey_api import API, ErroAPI  # noqa: E402

ESPEC_BLOCOS = os.path.join(RAIZ, "docs", "especificacao", "blocos-instrumento.md")
ESPEC_NAVEGACAO = os.path.join(RAIZ, "docs", "especificacao",
                               "navegacao-condicional.md")
CONFIG = os.path.join(AQUI, "instrumento", "configuracao")

resultados = []


def registra(numero, descricao, ok, detalhe=""):
    resultados.append(ok)
    marca = "OK  " if ok else "FALHA"
    print(f"[{marca}] {numero}. {descricao}" + (f" — {detalhe}" if detalhe else ""))


# ---------------------------------------------------------------------------
# Leitura da especificacao
# ---------------------------------------------------------------------------

def limpa(texto):
    return re.sub(r"\*\*|`", "", texto).strip()


def linhas_de_tabela(bloco_texto):
    linhas = []
    for l in bloco_texto.splitlines():
        if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l):
            linhas.append([limpa(c) for c in l.strip().strip("|").split("|")])
    return linhas[1:]  # sem o cabecalho


def secao(texto, inicio, fim):
    a = texto.index(inicio)
    b = texto.index(fim, a + len(inicio))
    return texto[a:b]


def le_campos_especificados():
    """Secao 12.3: devolve [(grupo, codigo, tipo, dominio, obrigatoriedade)]."""
    texto = open(ESPEC_BLOCOS, encoding="utf-8").read()
    s = secao(texto, "### 12.3 Campos por bloco", "### 12.4")
    campos, grupo = [], None
    for paragrafo in re.split(r"\n(?=\*\*[^*]+\*\* — público)", s):
        m = re.match(r"\*\*([^*]+)\*\* — público", paragrafo)
        if m:
            grupo = m.group(1).strip()
        tabela = re.search(r"\| Código \|.*?(?:\n\n|\Z)", paragrafo, re.S)
        if not tabela:
            continue
        for c in linhas_de_tabela(tabela.group(0)):
            campos.append({"grupo": grupo, "codigo": c[0], "dado": c[1],
                           "tipo": c[2], "dominio": c[3], "obrig": c[4]})
    return campos


def le_ordem_dos_grupos():
    """Secao 2 da E14: a ordem das paginas, com a 7 desdobrada em V e VI."""
    texto = open(ESPEC_NAVEGACAO, encoding="utf-8").read()
    s = secao(texto, "## 2. Ordem e paginação", "Quem recusa")
    ordem = []
    for c in linhas_de_tabela(s):
        ordem.extend(p.strip() for p in c[1].split(" ou "))
    return ordem


def le_caminhos():
    """Secao 5 da E14: a tabela dos dez caminhos."""
    texto = open(ESPEC_NAVEGACAO, encoding="utf-8").read()
    s = secao(texto, "## 5. Os caminhos", "\"IV completo\"")
    caminhos = {}
    for c in linhas_de_tabela(s):
        caminhos[c[0]] = {"CON1": c[1], "CON2": c[2], "nivel": c[3], "R": c[4],
                          "blocos": tuple(b.strip() for b in c[5].split(","))}
    s8 = secao(texto, "| C1 | C2 |", "A primeira execução")
    tabela = [l for l in s8.splitlines() if l.startswith("|")]
    nomes = [x.strip() for x in tabela[0].strip("|").split("|")]
    contagens = [int(x.strip().replace(".", "")) for x in
                 tabela[2].strip("|").split("|")]
    return caminhos, dict(zip(nomes, contagens))


def le_csv(nome):
    with open(os.path.join(CONFIG, nome + ".csv"), encoding="utf-8",
              newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Avaliador do subconjunto do Expression Manager usado no instrumento
# ---------------------------------------------------------------------------

TOKEN = re.compile(r"\s*(?:(?P<s>'[^']*'|\"[^\"]*\")|(?P<n>\d+)|"
                   r"(?P<op>==|!=|!|\(|\)|,)|(?P<id>[A-Za-z_][A-Za-z0-9_.]*))")


def traduz(expr):
    """Traduz a expressao para Python. Variavel vira v('NOME')."""
    saida, pos = [], 0
    expr = expr.strip()
    while pos < len(expr):
        m = TOKEN.match(expr, pos)
        if not m or m.end() == pos:
            raise ValueError(f"expressao fora do subconjunto: {expr[pos:]!r}")
        pos = m.end()
        if m.group("s"):
            saida.append(repr(m.group("s")[1:-1]))
        elif m.group("n"):
            saida.append(repr(m.group("n")))
        elif m.group("op"):
            saida.append(" not " if m.group("op") == "!" else m.group("op"))
        else:
            ident = m.group("id")
            if ident in ("and", "or"):
                saida.append(f" {ident} ")
            elif ident in ("if", "substr"):
                saida.append("_" + ident)
            else:
                saida.append(f"v({ident!r})")
    return "".join(saida)


def variaveis(expr):
    return {m.group("id") for m in TOKEN.finditer(expr)
            if m.group("id") and m.group("id") not in ("and", "or", "if",
                                                       "substr")}


def avalia(expr, valores, relevantes):
    """Avalia com a semantica do EM para exibicao: questao oculta citada sem
    .NAOK torna a expressao falsa.

    A verificacao e feita sobre TODAS as variaveis citadas, antes de avaliar,
    como o EM faz (GetVarsUsed em em_core_helper.php) — e nao so sobre as que a
    avaliacao chega a ler. Um avaliador com curto-circuito deixaria passar
    exatamente o defeito que esta regra produz: a primeira versao desta
    conferencia nao acusou o Bloco VI sem .NAOK por isso.
    """
    if expr.strip() in ("", "1"):
        return True
    for nome in variaveis(expr):
        base, _, sufixo = nome.partition(".")
        if sufixo != "NAOK" and not relevantes.get(base, False):
            return False

    def v(nome):
        base = nome.partition(".")[0]
        return valores.get(base, "") if relevantes.get(base, False) else ""

    ambiente = {"v": v,
                "_if": lambda c, a, b: a if c else b,
                "_substr": lambda s, i, n: str(s)[int(i):int(i) + int(n)]}
    return bool(eval(traduz(expr), {"__builtins__": {}}, ambiente))


# ---------------------------------------------------------------------------
# Leitura da instancia
# ---------------------------------------------------------------------------

def le_instancia(sessao, sid):
    grupos = sorted(sessao.chamar("list_groups", [sid]),
                    key=lambda g: int(g["group_order"]))
    nome_grupo = {int(g["gid"]): g["group_name"] for g in grupos}
    questoes = {}
    for q in sessao.chamar("list_questions", [sid]):
        if int(q["parent_qid"]) != 0:
            continue
        p = sessao.chamar("get_question_properties", [int(q["qid"])])
        opcoes = p.get("answeroptions")
        if isinstance(opcoes, dict):
            opcoes = sorted(((c, o["answer"]) for c, o in opcoes.items()),
                            key=lambda co: p["answeroptions"][co[0]]["order"])
        else:
            opcoes = []
        subq = p.get("subquestions")
        if isinstance(subq, dict):
            subq = [(s["title"], s["question"]) for _, s in
                    sorted(subq.items(), key=lambda kv: int(kv[0]))]
        else:
            subq = []
        questoes[q["title"]] = {
            "tipo": q["type"], "grupo": nome_grupo[int(q["gid"])],
            "gid": int(q["gid"]), "ordem": int(q["question_order"]),
            "obrigatorio": q["mandatory"], "relevancia": q["relevance"] or "1",
            "preg": q["preg"] or "", "opcoes": opcoes, "subq": subq,
            "atributos": p.get("attributes") or {},
            "padrao": p.get("defaultvalue") or ""}
    return grupos, questoes


# ---------------------------------------------------------------------------
# Conferencias
# ---------------------------------------------------------------------------

TIPOS = {
    "escolha única": {"L", "!"},
    "escala": {"L"},
    "escolha múltipla": {"M"},
    "texto livre": {"T"},
    "texto com validação": {"S"},
    "caixa de marcação": {"M"},
    "número inteiro": {"N"},
    "derivado do curso": {"*"},
}


def dominio_esperado(campo, especificados):
    """Rotulos esperados, em minusculas, ou None quando o dominio nao e lista."""
    d = campo["dominio"]
    if d.startswith("lista de cursos"):
        return [c["nome"].lower() for c in le_csv("cursos")]
    if d.startswith("lista de unidades"):
        return [u["nome"].lower() for u in le_csv("unidades")]
    if d.startswith("as cinco faixas do Anexo I"):
        return [f["rotulo"].lower() for f in le_csv("faixas-rendimento")]
    if d.startswith("o mesmo de "):
        alvo = d.split()[-1]
        return dominio_esperado(
            next(c for c in especificados if c["codigo"] == alvo), especificados)
    if campo["tipo"] in ("texto livre", "texto com validação",
                         "número inteiro", "derivado do curso",
                         "caixa de marcação"):
        return None
    itens = []
    for parte in d.split(" · "):
        if parte.strip() == "1 a 10":
            itens.extend(str(i) for i in range(1, 11))
        else:
            itens.append(parte.strip().lower())
    return itens


def confere_campos(questoes, especificados, ordem_grupos):
    divergencias = []
    for c in especificados:
        q = questoes.get(c["codigo"])
        if q is None:
            divergencias.append(f"{c['codigo']}: ausente")
            continue
        if q["grupo"] != c["grupo"]:
            divergencias.append(f"{c['codigo']}: no grupo {q['grupo']!r}, "
                                f"especificado {c['grupo']!r}")
        if q["tipo"] not in TIPOS.get(c["tipo"], set()):
            divergencias.append(f"{c['codigo']}: tipo {q['tipo']} para "
                                f"{c['tipo']!r}")
        obrig = c["obrig"]
        if obrig == "sim":
            ok = q["obrigatorio"] == "Y" and q["relevancia"] == "1"
        elif obrig == "sim, se exibido":
            ok = q["obrigatorio"] == "Y" and q["relevancia"] != "1"
        else:  # "não" ou "—"
            ok = q["obrigatorio"] == "N"
        if not ok:
            divergencias.append(f"{c['codigo']}: obrigatoriedade "
                                f"{q['obrigatorio']} para {obrig!r}")
        esperado = dominio_esperado(c, especificados)
        if esperado is not None:
            obtido = [r.lower() for _, r in (q["opcoes"] or q["subq"])]
            if obtido != esperado:
                divergencias.append(f"{c['codigo']}: dominio {obtido} "
                                    f"diferente de {esperado}")
        if c["tipo"] == "caixa de marcação" and len(q["subq"]) != 1:
            divergencias.append(f"{c['codigo']}: caixa de marcacao com "
                                f"{len(q['subq'])} opcoes")
        if c["tipo"] == "texto livre":
            m = re.search(r"até ([\d.]+) caracteres", c["dominio"])
            if m and str(q["atributos"].get("maximum_chars")) != \
                    m.group(1).replace(".", ""):
                divergencias.append(f"{c['codigo']}: limite de caracteres")
        if c["tipo"] == "número inteiro":
            if str(q["atributos"].get("num_value_int_only")) != "1":
                divergencias.append(f"{c['codigo']}: nao restrito a inteiro")
        if c["tipo"] == "texto com validação" and not q["preg"]:
            divergencias.append(f"{c['codigo']}: sem expressao de validacao")
        if c["tipo"] == "escolha múltipla":
            # Secao 12.3: em EF4, "nenhuma no momento" exclui as demais.
            nenhuma = [cod for cod, r in q["subq"]
                       if r.lower().startswith("nenhuma")]
            if nenhuma and q["atributos"].get("exclude_all_others") != nenhuma[0]:
                divergencias.append(f"{c['codigo']}: 'nenhuma' nao exclui "
                                    "as demais")
    return divergencias


def expressao_da_equacao(eq):
    """O atributo `equation` e texto com trechos {expressao}, e nao expressao:
    sem chaves, a plataforma grava o proprio texto. Devolve a expressao, ou
    None se o atributo nao for uma expressao entre chaves."""
    eq = (eq or "").strip()
    if not (eq.startswith("{") and eq.endswith("}")):
        return None
    return eq[1:-1]


def confere_nivel(questoes):
    """IDA2 deriva o nivel certo para cada curso da lista de configuracao."""
    eq = expressao_da_equacao(questoes["IDA2"]["atributos"].get("equation"))
    if eq is None:
        return ["IDA2: equacao sem chaves — a plataforma gravaria o texto "
                "literal, e nao o nivel"]
    erradas = []
    for c in le_csv("cursos"):
        obtido = eval(traduz(eq), {"__builtins__": {}}, {
            "v": lambda n, cod=c["codigo"]: cod if n.split(".")[0] == "IDA1" else "",
            "_if": lambda t, a, b: a if t else b,
            "_substr": lambda s, i, n: str(s)[int(i):int(i) + int(n)]})
        if obtido != c["nivel"]:
            erradas.append(f"{c['codigo']}: {obtido!r} != {c['nivel']!r}")
    return erradas


# Os invalidos sao invalidos DE PROPOSITO, e nenhum pode pertencer a alguem: os
# dominios fora de .test sao reservados (RFC 2606) e os numeros com codigo de
# area real tem assinante iniciado por 0, que nao existe na numeracao brasileira.
EXEMPLOS_CONTATO = {
    "CT1": {"validos": ["pessoa.exemplo1@egressos.test", "a@b.test",
                        "x+tag@sub.egressos.TEST", "o'neil@egressos.test"],
            "invalidos": ["pessoa@example.com", "pessoa@egressos.test.example",
                          ".pessoa@egressos.test", "pes..soa@egressos.test",
                          "pessoa@test", "pessoa egressos.test",
                          "a" * 65 + "@egressos.test"]},
    "CT3": {"validos": ["+5520912345678", "+552012345678", "+559012345678"],
            "invalidos": ["+551100000000", "+552100000000", "5520912345678",
                          "+55 20 91234-5678", "+5520812345678",
                          "+10000000000"]},
}


def confere_validacoes(questoes):
    erradas = []
    for cod, ex in EXEMPLOS_CONTATO.items():
        preg = questoes[cod]["preg"]
        m = re.match(r"^/(.*)/([a-z]*)$", preg, re.S)
        rx = re.compile(m.group(1), re.I if "i" in m.group(2) else 0)
        for v in ex["validos"]:
            if not rx.search(v):
                erradas.append(f"{cod} recusou {v!r}")
        for v in ex["invalidos"]:
            if rx.search(v):
                erradas.append(f"{cod} aceitou {v!r}")
    if questoes["CT2"]["preg"] != questoes["CT1"]["preg"]:
        erradas.append("CT2 com sintaxe diferente de CT1")
    return erradas


def nome_de_campo(dado):
    """'ano de conclusão' -> 'ano_conclusao': o nome do campo no leiaute (E11),
    derivado do texto da especificacao, e nao de estrutura.py."""
    s ="".join(c for c in unicodedata.normalize("NFD", dado)
                if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"\s+", "_", s.replace(" de ", " ").strip())


def confere_pre_preenchimento(questoes, especificados, descricoes):
    """Secao 12.3 da E13: os campos da identificacao vem pre-preenchidos com o
    atributo do participante correspondente; IDA2 e derivado, e nao tem padrao.
    Confere que cada padrao aponta para a coluna cuja descricao e o campo."""
    erradas = []
    if not descricoes:
        return ["o questionario nao tem descricao de atributos do participante"
                " — rode instrumento.py preparar-participantes"]
    coluna_por_nome = {info.get("description"): col.upper()
                       for col, info in descricoes.items()}
    for c in especificados:
        if c["grupo"] != "Identificação acadêmica":
            continue
        q = questoes[c["codigo"]]
        if c["tipo"] == "derivado do curso":
            if q["padrao"]:
                erradas.append(f"{c['codigo']}: derivado nao deveria ter padrao")
            continue
        esperado = coluna_por_nome.get(nome_de_campo(c["dado"]))
        if esperado is None:
            erradas.append(f"{c['codigo']}: nenhum atributo do participante "
                           f"descrito como {nome_de_campo(c['dado'])!r}")
        elif q["padrao"].strip() != "{TOKEN:%s}" % esperado:
            erradas.append(f"{c['codigo']}: padrao {q['padrao']!r}, esperado "
                           f"{{TOKEN:{esperado}}}")
    return erradas


# Rotulo de bloco usado na tabela de caminhos da E14 -> nome do grupo
BLOCO_DO_CAMINHO = {
    "Consentimento": "Consentimento",
    "Identificação": "Identificação acadêmica",
    "I": "Bloco I", "II": "Bloco II", "III": "Bloco III", "IV": "Bloco IV",
    "V": "Bloco V", "VI": "Bloco VI", "VII": "Bloco VII",
    "Equidade": "Recortes de equidade", "Contato": "Contato e manifestações",
}


def rotulo_do_grupo(nome):
    for rotulo, prefixo in BLOCO_DO_CAMINHO.items():
        if nome == prefixo or nome.startswith(prefixo + " —"):
            return rotulo
    return nome


def codigo_por_rotulo(opcoes, texto):
    """Acha a opcao pelo inicio do rotulo: a tabela de caminhos abrevia
    ("nao concordo neste ciclo" para "nao concordo com o termo neste ciclo")."""
    texto = texto.lower()
    exatas = [c for c, r in opcoes if r.lower() == texto]
    if exatas:
        return exatas[0]
    duas = " ".join(texto.split()[:2])
    candidatas = [c for c, r in opcoes if r.lower().startswith(duas)
                  and r.lower() != duas]
    if len(candidatas) != 1:
        raise ValueError(f"rotulo ambiguo ou ausente: {texto!r}")
    return candidatas[0]


def percorre(grupos, questoes):
    """Enumera as combinacoes das respostas que decidem o caminho, pela ordem
    das paginas, e devolve, para cada uma, a linha do caminho."""
    ordem = [(g["group_name"], g["grelevance"] or "1") for g in grupos]
    por_grupo = {}
    for cod, q in questoes.items():
        por_grupo.setdefault(q["grupo"], []).append((q["ordem"], cod))
    for g in por_grupo:
        por_grupo[g].sort()

    cursos = {}
    for c in le_csv("cursos"):
        cursos.setdefault(c["nivel"], c["codigo"])  # um curso por nivel
    # Sem chaves, o valor gravado e o proprio texto da equacao (que nao casa
    # com nenhum nivel) — e assim que a plataforma se comporta.
    eq_ida2 = (expressao_da_equacao(questoes["IDA2"]["atributos"].get("equation"))
               or repr(questoes["IDA2"]["atributos"].get("equation", "")))

    decisivas = ["CON1", "CON2", "IDA1", "AP1", "AP2", "SA1", "SA2", "EF1"]

    def ramos(valores, relevantes, i):
        if i == len(decisivas):
            yield dict(valores), dict(relevantes)
            return
        cod = decisivas[i]
        q = questoes[cod]
        g_rel = dict(ordem)[q["grupo"]]
        mostra = (avalia(g_rel, valores, relevantes)
                  and avalia(q["relevancia"], valores, relevantes))
        if not mostra:
            relevantes[cod] = False
            yield from ramos(valores, relevantes, i + 1)
            relevantes.pop(cod)
            return
        relevantes[cod] = True
        dominio = (list(cursos.values()) if cod == "IDA1"
                   else [c for c, _ in q["opcoes"]])
        for valor in dominio:
            valores[cod] = valor
            if cod == "IDA1":
                relevantes["IDA2"] = True
                valores["IDA2"] = eval(traduz(eq_ida2), {"__builtins__": {}}, {
                    "v": lambda n: valor if n.split(".")[0] == "IDA1" else "",
                    "_if": lambda t, a, b: a if t else b,
                    "_substr": lambda s, i, n: str(s)[int(i):int(i) + int(n)]})
            yield from ramos(valores, relevantes, i + 1)
        valores.pop(cod, None)
        relevantes.pop(cod)

    for valores, relevantes in ramos({}, {}, 0):
        blocos = []
        for nome, rel in ordem:
            if not avalia(rel, valores, relevantes):
                continue
            rotulo = rotulo_do_grupo(nome)
            if rotulo == "IV":
                ef1 = avalia(questoes["EF1"]["relevancia"], valores, relevantes)
                rotulo = "IV completo" if ef1 else "IV só EF4"
            blocos.append(rotulo)
        yield valores, relevantes, tuple(blocos)


def confere_caminhos(grupos, questoes):
    caminhos, contagens = le_caminhos()
    con1 = questoes["CON1"]["opcoes"]
    con2 = questoes["CON2"]["opcoes"]
    niveis = {"técnico ou graduação": {"tecnico", "graduacao"},
              "pós-graduação": {"pos_graduacao"}}

    def casa(linha, valores, relevantes, blocos):
        if valores.get("CON1") != codigo_por_rotulo(con1, linha["CON1"]):
            return False
        if linha["CON2"] == "—":
            if relevantes.get("CON2"):
                return False
        elif valores.get("CON2") != codigo_por_rotulo(con2, linha["CON2"]):
            return False
        if linha["nivel"] != "—" and \
                valores.get("IDA2") not in niveis[linha["nivel"]]:
            return False
        if linha["R"] != "—":
            tem_v = "V" in blocos
            if tem_v != (linha["R"] == "sim"):
                return False
        return blocos == linha["blocos"]

    contados = Counter()
    problemas = []
    total = 0
    for valores, relevantes, blocos in percorre(grupos, questoes):
        total += 1
        achados = [n for n, l in caminhos.items()
                   if casa(l, valores, relevantes, blocos)]
        if len(achados) != 1:
            problemas.append(f"{valores} -> {blocos}: {achados or 'nenhum'}")
            continue
        contados[achados[0]] += 1
        if "V" in blocos and "VI" in blocos:
            problemas.append(f"{valores}: V e VI juntos")
    return total, contados, contagens, problemas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sid", type=int, default=202615)
    args = ap.parse_args()

    env = {}
    with open(os.path.join(AQUI, ".env"), encoding="utf-8") as fh:
        for linha in fh:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                env[k.strip()] = v.strip()
    porta = env.get("PORTA_HTTP", "8080")

    especificados = le_campos_especificados()
    ordem_esperada = le_ordem_dos_grupos()

    with API(url=f"http://127.0.0.1:{porta}", usuario=env["ADMIN_USUARIO"],
             senha=env["ADMIN_SENHA"]) as sessao:
        grupos, questoes = le_instancia(sessao, args.sid)
        descricoes = json.loads(sessao.chamar("get_survey_properties", [
            args.sid, ["attributedescriptions"]]).get(
                "attributedescriptions") or "{}")

    print(f"Questionario {args.sid}: {len(grupos)} grupos, {len(questoes)} "
          f"campos na instancia; {len(especificados)} campos especificados.\n")

    # A tabela da secao 2 abrevia o nome do Bloco VI; compara-se pelo rotulo
    # do bloco. O nome completo e conferido campo a campo, contra a 12.3.
    obtida = [rotulo_do_grupo(g["group_name"]) for g in grupos]
    esperada = [rotulo_do_grupo(n) for n in ordem_esperada]
    registra(1, "onze grupos, na ordem da secao 2 da E14",
             obtida == esperada and len(obtida) == 11,
             "" if obtida == esperada else f"{obtida} != {esperada}")

    sobra = sorted(set(questoes) - {c["codigo"] for c in especificados})
    div = confere_campos(questoes, especificados, ordem_esperada)
    registra(2, f"{len(especificados)} campos da secao 12.3 da E13 — codigo, "
             "grupo, tipo, obrigatoriedade e dominio",
             not div and not sobra and len(especificados) == 35,
             "; ".join(div + [f"campo nao especificado: {s}" for s in sobra]))

    cfg = []
    for cod, nome in (("IDA1", "cursos"), ("IDA3", "unidades"),
                      ("PM3", "faixas-rendimento")):
        esperado = [l["codigo"] for l in le_csv(nome)]
        obtido = [c for c, _ in questoes[cod]["opcoes"]]
        if obtido != esperado:
            cfg.append(f"{cod} != configuracao/{nome}.csv")
    antecessoras = [u for u in le_csv("unidades") if u["situacao"] == "antecessora"]
    if len(antecessoras) < 1:
        cfg.append("lista de unidades sem antecessoras")
    registra(3, "listas de configuracao versionada — codigos e ordem, com as "
             f"antecessoras ({len(antecessoras)})", not cfg, "; ".join(cfg))

    erradas = confere_nivel(questoes)
    registra(4, f"IDA2 deriva o nivel de cada um dos {len(le_csv('cursos'))} "
             "cursos", not erradas, "; ".join(erradas))

    erradas = confere_validacoes(questoes)
    n = sum(len(e["validos"]) + len(e["invalidos"])
            for e in EXEMPLOS_CONTATO.values())
    registra(5, f"validacao de contato do modo de ensaio ({n} exemplos)",
             not erradas, "; ".join(erradas))

    total, contados, esperadas, problemas = confere_caminhos(grupos, questoes)
    ok = (not problemas and dict(contados) == esperadas
          and total == sum(esperadas.values()))
    detalhe = (f"{total} combinacoes; por caminho: "
               + ", ".join(f"{k}={contados.get(k, 0)}" for k in esperadas))
    if problemas:
        detalhe += f"; {len(problemas)} sem caminho unico, ex.: {problemas[0]}"
    registra(6, "dez caminhos da secao 5 da E14, pelas expressoes da instancia",
             ok, detalhe)

    erradas = confere_pre_preenchimento(questoes, especificados, descricoes)
    registra(7, "pre-preenchimento da identificacao pelos atributos do "
             "participante (E18)", not erradas, "; ".join(erradas))

    print(f"\n{sum(resultados)} de {len(resultados)} conferencias passaram.")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ErroAPI as e:
        print(f"erro de API: {e}", file=sys.stderr)
        sys.exit(2)
