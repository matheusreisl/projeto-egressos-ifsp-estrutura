#!/usr/bin/env python3
"""
Gera, implanta e exporta o instrumento na instancia LimeSurvey (E15).

A estrutura vem de estrutura.py, que transcreve a especificacao das etapas E12
a E14; os dominios de configuracao vem de configuracao/. Este script monta o
.lss, importa-o pela API, exporta de volta o que a instancia guardou e cuida
das copias descartaveis usadas na conferencia.

Subcomandos, a partir da pasta infra/:

  python3 instrumento/instrumento.py gerar [--saida F]
      monta o .lss sem tocar a instancia.

  python3 instrumento/instrumento.py implantar [--substituir]
      gera, importa com o sid fixo do instrumento e exporta a estrutura que a
      instancia guardou para instrumento/instrumento.lss — o artefato versionado.
      Recusa se o sid ja existir, salvo --substituir, que so remove questionario
      INATIVO.

  python3 instrumento/instrumento.py exportar --sid N [--saida F]
      exporta a estrutura de um questionario da instancia.

  python3 instrumento/instrumento.py copia-de-ensaio
      importa o mesmo .lss com outro sid, fecha o acesso, ativa e cria
      participantes sinteticos sob .test. Imprime os enderecos individuais.
      E onde se percorrem os caminhos sem tocar o instrumento.

  python3 instrumento/instrumento.py remover --sid N
      remove uma copia de ensaio. Recusa o sid do instrumento.

  python3 instrumento/instrumento.py preparar-participantes
      prepara o acesso controlado do instrumento (E17): cria os atributos da
      base central, fecha o acesso e cria a tabela de participantes com os
      atributos nomeados. Nao ativa o questionario. Idempotente.

  python3 instrumento/instrumento.py ativar
      ativa o instrumento (E18), depois da preparacao e da importacao. Recusa
      sem acesso fechado ou sem participantes. Depois disto a estrutura trava.

  python3 instrumento/instrumento.py aplicar-mensagens
      aplica ao instrumento os modelos de convite e lembrete, o remetente e o
      retorno (E20, instrumento/mensagens.py), e garante a coluna do atributo
      que escolhe o ramo do lembrete. Funciona com o questionario ativo.
      Idempotente. Nao envia mensagem.

  Ordem completa, do zero: implantar, preparar-participantes, importacao
  (scripts/importar_base.py) e ativar. Os modelos ja vao no .lss; o
  aplicar-mensagens existe para o instrumento ja ativo.

Requer a composicao de pe e o .env de infra/. Nao envia mensagem alguma e nao
usa dado de pessoa real: os participantes da copia sao sinteticos e os
enderecos estao sob o TLD reservado .test.
"""

import argparse
import base64
import csv
import json
import os
import random
import re
import sys
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
INFRA = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(os.path.dirname(INFRA), "scripts"))

from limesurvey_api import API, ErroAPI  # noqa: E402
from limesurvey_console import console  # noqa: E402

import estrutura  # noqa: E402
import mensagens  # noqa: E402

# Sid fixo do instrumento, para que as etapas seguintes possam nomea-lo.
# A tabela de respostas, quando ativado, sera lime_responses_<SID> — e NAO
# lime_survey_<SID> (E08).
SID_INSTRUMENTO = 202615
IDIOMA = "pt-BR"
SAIDA_PADRAO = os.path.join(AQUI, "instrumento.lss")

# Tipo da especificacao -> (tipo da plataforma, tema da questao)
TIPOS = {
    "lista": ("L", "listradio"),
    "suspensa": ("!", "list_dropdown"),
    "multipla": ("M", "multiplechoice"),
    "inteiro": ("N", "numerical"),
    "texto_curto": ("S", "shortfreetext"),
    "texto_longo": ("T", "longfreetext"),
    "equacao": ("*", "equation"),
}

PREFIXO_NIVEL = {"T": "tecnico", "G": "graduacao", "P": "pos_graduacao"}
ROTULO_NIVEL = {"tecnico": "Técnico", "graduacao": "Graduação",
                "pos_graduacao": "Pós-graduação"}


class Erro(Exception):
    pass


# ---------------------------------------------------------------------------
# Configuracao versionada
# ---------------------------------------------------------------------------

def le_csv(nome):
    with open(os.path.join(AQUI, "configuracao", nome + ".csv"),
              encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def le_parametros():
    with open(os.path.join(AQUI, "configuracao", "parametros.json"),
              encoding="utf-8") as fh:
        return json.load(fh)


def opcoes_de_configuracao(nome):
    linhas = le_csv(nome)
    if nome == "cursos":
        for l in linhas:
            nivel = PREFIXO_NIVEL.get(l["codigo"][:1])
            # O nivel vem do prefixo do codigo (estrutura.py, IDA2). Se o
            # prefixo e a coluna divergirem, o instrumento mostraria um nivel e
            # a base de entrada teria outro.
            if nivel != l["nivel"]:
                raise Erro(f"curso {l['codigo']}: prefixo indica {nivel}, "
                           f"coluna nivel diz {l['nivel']}")
        return [(l["codigo"], l["nome"]) for l in linhas]
    if nome == "unidades":
        return [(l["codigo"], l["nome"]) for l in linhas]
    if nome == "faixas-rendimento":
        return [(l["codigo"], l["rotulo"]) for l in linhas]
    raise Erro(f"dominio de configuracao desconhecido: {nome}")


# ---------------------------------------------------------------------------
# Conferencias locais antes de gerar
# ---------------------------------------------------------------------------

CODIGO_QUESTAO = re.compile(r"^[A-Za-z][A-Za-z0-9]{0,19}$")
CODIGO_OPCAO = re.compile(r"^[A-Za-z0-9]{1,5}$")


def resolve_opcoes(campo):
    opcoes = campo.get("opcoes")
    if isinstance(opcoes, str) and opcoes.startswith("config:"):
        return opcoes_de_configuracao(opcoes.split(":", 1)[1])
    return opcoes or []


def confere_estrutura():
    vistos = set()
    for g in estrutura.GRUPOS:
        for c in g["campos"]:
            cod = c["codigo"]
            if not CODIGO_QUESTAO.match(cod):
                raise Erro(f"codigo de questao invalido: {cod}")
            if cod in vistos:
                raise Erro(f"codigo de questao repetido: {cod}")
            vistos.add(cod)
            if c["tipo"] not in TIPOS:
                raise Erro(f"{cod}: tipo desconhecido {c['tipo']}")
            opcoes = resolve_opcoes(c)
            codigos = [o[0] for o in opcoes]
            for o in codigos:
                if not CODIGO_OPCAO.match(o):
                    raise Erro(f"{cod}: codigo de opcao invalido {o!r} "
                               "(ate 5 alfanumericos — lime_answers.code)")
            if len(set(codigos)) != len(codigos):
                raise Erro(f"{cod}: codigo de opcao repetido")
            if c["tipo"] in ("lista", "suspensa", "multipla") and not opcoes:
                raise Erro(f"{cod}: sem opcoes")
    return len(vistos)


# ---------------------------------------------------------------------------
# Montagem do .lss
# ---------------------------------------------------------------------------

def enunciado(campo):
    """Marcador no lugar do enunciado. Nomeia o campo e o dado — que sao
    estrutura — e diz de onde o texto vira."""
    return (f"<p><strong>[{campo['codigo']}]</strong> {campo['dado']}</p>"
            "<p><em>Enunciado a definir pelo projeto correlato.</em></p>")


def enunciado_consentimento():
    return ("<p><strong>[CON1]</strong> manifestação sobre o termo</p>"
            "<p><em>Texto do termo de consentimento e enunciado a definir na "
            "E22 e pelo projeto correlato.</em></p>")


def enunciado_nivel():
    rotulo = ("if(IDA2 == 'tecnico', 'Técnico', if(IDA2 == 'graduacao', "
              "'Graduação', if(IDA2 == 'pos_graduacao', 'Pós-graduação', "
              "'escolha o curso acima')))")
    return ("<p><strong>[IDA2]</strong> nível, derivado do curso: "
            f"<strong>{{{rotulo}}}</strong></p>")


def secao(raiz, nome, campos, linhas):
    s = ET.SubElement(raiz, nome)
    f = ET.SubElement(s, "fields")
    for c in campos:
        ET.SubElement(f, "fieldname").text = c
    r = ET.SubElement(s, "rows")
    for linha in linhas:
        row = ET.SubElement(r, "row")
        for c in campos:
            v = linha.get(c)
            ET.SubElement(row, c).text = "" if v is None else str(v)


CAMPOS_QUESTAO = ["qid", "parent_qid", "sid", "gid", "type", "title", "preg",
                  "other", "mandatory", "encrypted", "question_order",
                  "scale_id", "same_default", "relevance",
                  "question_theme_name", "modulename", "same_script"]


def monta_lss(sid):
    confere_estrutura()
    parametros = le_parametros()

    grupos, grupos_l10n = [], []
    questoes, subquestoes, questoes_l10n = [], [], []
    respostas, respostas_l10n, atributos = [], [], []
    padroes, padroes_l10n = [], []
    gid = qid = aid = lid = dvid = 0

    for ordem_g, g in enumerate(estrutura.GRUPOS, start=1):
        gid += 1
        grupos.append({"gid": gid, "sid": sid, "group_order": ordem_g,
                       "randomization_group": "", "grelevance": g["relevancia"]})
        lid += 1
        grupos_l10n.append({"id": lid, "gid": gid, "group_name": g["nome"],
                            "description": "", "language": IDIOMA})

        for ordem_q, c in enumerate(g["campos"], start=1):
            qid += 1
            tipo, tema = TIPOS[c["tipo"]]
            preg = ""
            if c.get("validacao"):
                preg = estrutura.VALIDACOES[c["validacao"]]["preg"]
            questoes.append({
                "qid": qid, "parent_qid": 0, "sid": sid, "gid": gid,
                "type": tipo, "title": c["codigo"], "preg": preg,
                "other": "N", "mandatory": "Y" if c.get("obrigatorio") else "N",
                "encrypted": "N", "question_order": ordem_q, "scale_id": 0,
                "same_default": 0, "relevance": c.get("relevancia", "1"),
                "question_theme_name": tema, "modulename": "",
                "same_script": 0})
            if c["codigo"] == "CON1":
                texto = enunciado_consentimento()
            elif c["codigo"] == "IDA2":
                texto = enunciado_nivel()
            else:
                texto = enunciado(c)
            lid += 1
            questoes_l10n.append({"id": lid, "qid": qid, "question": texto,
                                  "help": "", "script": "", "language": IDIOMA})

            if c.get("pre_preenchido"):
                # Valor padrao = atributo do participante (E18). A plataforma
                # processa o padrao como expressao e so o aceita se for resposta
                # valida — o codigo do curso ou da unidade, que a importacao da
                # E17 ja grava no participante.
                dvid += 1
                padroes.append({"dvid": dvid, "qid": qid, "scale_id": 0,
                                "sqid": 0, "specialtype": ""})
                lid += 1
                padroes_l10n.append({
                    "id": lid, "dvid": dvid, "language": IDIOMA,
                    "defaultvalue": "{TOKEN:%s}" % coluna_do_atributo(
                        c["pre_preenchido"]).upper()})

            def atributo(nome, valor, idioma=""):
                atributos.append({"qid": qid, "attribute": nome,
                                  "value": valor, "language": idioma})

            opcoes = resolve_opcoes(c)
            if tipo == "M":
                # Opcoes da escolha multipla sao subquestoes.
                qid_pai = qid
                for ordem_s, (codigo, rotulo) in enumerate(opcoes, start=1):
                    qid += 1
                    subquestoes.append({
                        "qid": qid, "parent_qid": qid_pai, "sid": sid,
                        "gid": gid, "type": tipo, "title": codigo, "preg": "",
                        "other": "N", "mandatory": "N", "encrypted": "N",
                        "question_order": ordem_s, "scale_id": 0,
                        "same_default": 0, "relevance": "1",
                        "question_theme_name": "", "modulename": "",
                        "same_script": 0})
                    lid += 1
                    questoes_l10n.append({"id": lid, "qid": qid,
                                          "question": rotulo, "help": "",
                                          "script": "", "language": IDIOMA})
                if c.get("exclusiva"):
                    atributos.append({"qid": qid_pai,
                                      "attribute": "exclude_all_others",
                                      "value": c["exclusiva"], "language": ""})
                continue

            for ordem_a, (codigo, rotulo) in enumerate(opcoes):
                aid += 1
                respostas.append({"aid": aid, "qid": qid, "code": codigo,
                                  "sortorder": ordem_a, "assessment_value": 0,
                                  "scale_id": 0})
                lid += 1
                respostas_l10n.append({"id": lid, "aid": aid,
                                       "answer": rotulo, "language": IDIOMA})

            if tipo == "*":
                atributo("equation", c["equacao"])
            if tipo == "N" and c["codigo"] == "IDA4":
                # Do limite configurado ao ano corrente (secao 12.3). O maximo
                # e expressao, avaliada no preenchimento: o ano corrente nao
                # fica gravado na estrutura.
                atributo("num_value_int_only", "1")
                atributo("min_num_value_n",
                         str(parametros["ano_conclusao_minimo"]))
                atributo("max_num_value_n", "date('Y')")
                atributo("maximum_chars", "4")
            if tipo == "T" and c.get("max_caracteres"):
                atributo("maximum_chars", str(c["max_caracteres"]))
            if tipo == "S" and c.get("validacao"):
                v = estrutura.VALIDACOES[c["validacao"]]
                atributo("maximum_chars", str(v["max_caracteres"]))
            if c.get("validacao_em"):
                atributo("em_validation_q", c["validacao_em"])
                atributo("em_validation_q_tip", c["validacao_em_dica"], IDIOMA)

    # Questoes e subquestoes compartilham a numeracao de qid; a l10n da
    # subquestao vai na mesma secao question_l10ns.
    raiz = ET.Element("document")
    ET.SubElement(raiz, "LimeSurveyDocType").text = "Survey"
    ET.SubElement(raiz, "DBVersion").text = "716"
    langs = ET.SubElement(raiz, "languages")
    ET.SubElement(langs, "language").text = IDIOMA

    secao(raiz, "answers", ["aid", "qid", "code", "sortorder",
                            "assessment_value", "scale_id"], respostas)
    secao(raiz, "answer_l10ns", ["id", "aid", "answer", "language"],
          respostas_l10n)
    secao(raiz, "defaultvalues", ["dvid", "qid", "scale_id", "sqid",
                                  "specialtype"], padroes)
    secao(raiz, "defaultvalue_l10ns", ["id", "dvid", "language",
                                       "defaultvalue"], padroes_l10n)
    secao(raiz, "groups", ["gid", "sid", "group_order", "randomization_group",
                           "grelevance"], grupos)
    secao(raiz, "group_l10ns", ["id", "gid", "group_name", "description",
                                "language"], grupos_l10n)
    secao(raiz, "questions", CAMPOS_QUESTAO, questoes)
    secao(raiz, "subquestions", CAMPOS_QUESTAO, subquestoes)
    secao(raiz, "question_l10ns", ["id", "qid", "question", "help", "script",
                                   "language"], questoes_l10n)
    secao(raiz, "question_attributes", ["qid", "attribute", "value",
                                        "language"], atributos)
    secao(raiz, "surveys", list(CONFIG_QUESTIONARIO) + ["sid"],
          [dict(CONFIG_QUESTIONARIO, sid=sid)])
    modelos = mensagens.propriedades_de_idioma(numero_da_variante())
    secao(raiz, "surveys_languagesettings",
          ["surveyls_survey_id", "surveyls_language", "surveyls_title",
           "surveyls_description", "surveyls_welcometext", "surveyls_endtext",
           "surveyls_dateformat", "surveyls_numberformat"] + list(modelos),
          [{**modelos, "surveyls_survey_id": sid, "surveyls_language": IDIOMA,
            "surveyls_title": "Acompanhamento de Egressos do IFSP — "
                              "instrumento (ensaio)",
            "surveyls_description": "",
            "surveyls_welcometext": "",
            "surveyls_endtext": "<p><em>Texto de encerramento a definir na "
                                "E22 e pelo projeto correlato.</em></p>",
            # 5 = dd/mm/aaaa; 1 = virgula decimal.
            "surveyls_dateformat": 5, "surveyls_numberformat": 1}])

    ET.indent(raiz, space=" ")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            + ET.tostring(raiz, encoding="unicode") + "\n")


# Configuracoes do questionario. Cada uma tem o motivo no README desta pasta.
CONFIG_QUESTIONARIO = {
    "gsid": 1,
    **mensagens.propriedades_do_questionario(),  # remetente e retorno (E20)
    "language": IDIOMA,
    "additional_languages": "",
    "template": "fruity_twentythree",
    "format": "G",                  # um bloco por pagina (E14, decisao 1)
    "allowprev": "Y",               # voltar permitido (E14, decisao 2)
    "allowsave": "Y",               # salvar e retomar (E14, decisao 3)
    "tokenanswerspersistence": "N", # retomada NAO pelo endereco (E14, 7.3)
    "usecaptcha": "N",
    "anonymized": "N",              # o estado sai de CON1 ligado ao token
    "datestamp": "Y",               # data e hora da manifestacao (P6)
    "ipaddr": "N",                  # minimizacao: sem consumidor
    "ipanonymize": "N",
    "refurl": "N",                  # minimizacao: sem consumidor
    "savetimings": "N",             # minimizacao: sem consumidor
    "usecookie": "N",
    "allowregister": "N",
    "autoredirect": "N",
    "printanswers": "N",
    "publicstatistics": "N",
    "publicgraphs": "N",
    "listpublic": "N",
    "htmlemail": "Y",
    "sendconfirmation": "N",        # sem confirmacao ao respondente (E20)
    "assessments": "N",
    "tokenlength": 15,
    "showxquestions": "N",
    "showgroupinfo": "N",           # nome do bloco, sem descricao
    "shownoanswer": "N",            # dominio exatamente o especificado
    "showqnumcode": "X",
    "showwelcome": "N",             # o consentimento e a primeira pagina
    "showprogress": "Y",
    "questionindex": 0,             # sem indice: nao se salta paginas
    "navigationdelay": 0,
    "alloweditaftercompletion": "N",
    "bounceprocessing": "N",        # devolucoes sao rotina propria (E09)
    "showsurveypolicynotice": 0,    # consentimento e grupo proprio (E22)
    "access_mode": "O",             # acesso controlado e da E17
}


# ---------------------------------------------------------------------------
# Instancia
# ---------------------------------------------------------------------------

def carrega_env():
    caminho = os.path.join(INFRA, ".env")
    if not os.path.exists(caminho):
        raise Erro("arquivo infra/.env ausente — copie .env.exemplo e preencha")
    env = {}
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                chave, valor = linha.split("=", 1)
                env[chave.strip()] = valor.strip()
    return env


def api():
    env = carrega_env()
    porta = env.get("PORTA_HTTP", "8080")
    return API(url=f"http://127.0.0.1:{porta}",
               usuario=env.get("ADMIN_USUARIO"), senha=env.get("ADMIN_SENHA"))


def existe(sessao, sid):
    try:
        lista = sessao.chamar("list_surveys", [])
    except ErroAPI as e:
        if "No surveys found" in str(e):
            return None
        raise
    for s in lista or []:
        if int(s["sid"]) == sid:
            return s
    return None


def importa(sessao, conteudo, sid):
    dados = base64.b64encode(conteudo.encode("utf-8")).decode()
    novo = sessao.chamar("import_survey", [dados, "lss", None, sid])
    if not isinstance(novo, int):
        raise Erro(f"importacao falhou: {novo}")
    return novo


def exporta(sid):
    """Exporta pela funcao interna da plataforma, via console (comandos/)."""
    r = console("exportarestrutura", sid)
    if r.returncode != 0 or not r.stdout.lstrip().startswith("<?xml"):
        raise Erro(f"exportacao falhou: {r.stderr.strip() or r.stdout[:300]}")
    return r.stdout


# ---------------------------------------------------------------------------
# Subcomandos
# ---------------------------------------------------------------------------

def cmd_gerar(args):
    conteudo = monta_lss(SID_INSTRUMENTO)
    with open(args.saida, "w", encoding="utf-8") as fh:
        fh.write(conteudo)
    n = confere_estrutura()
    print(f"gerado: {args.saida} ({len(estrutura.GRUPOS)} grupos, {n} campos)")


def cmd_implantar(args):
    conteudo = monta_lss(SID_INSTRUMENTO)
    with api() as sessao:
        atual = existe(sessao, SID_INSTRUMENTO)
        if atual:
            if not args.substituir:
                raise Erro(f"o questionario {SID_INSTRUMENTO} ja existe; use "
                           "--substituir para recria-lo")
            if atual.get("active") == "Y":
                raise Erro(f"o questionario {SID_INSTRUMENTO} esta ATIVO; "
                           "recusado — ativo tem respostas")
            sessao.chamar("delete_survey", [SID_INSTRUMENTO])
        sid = importa(sessao, conteudo, SID_INSTRUMENTO)
    if sid != SID_INSTRUMENTO:
        raise Erro(f"a instancia atribuiu o sid {sid}, e nao {SID_INSTRUMENTO}")
    exportado = exporta(sid)
    with open(SAIDA_PADRAO, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(exportado)
    print(f"implantado: questionario {sid}")
    print(f"exportado:  {SAIDA_PADRAO}")


def cmd_exportar(args):
    conteudo = exporta(args.sid)
    with open(args.saida, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(conteudo)
    print(f"exportado: {args.saida}")


# Participantes sinteticos da copia de ensaio. Um por nivel, para que a
# identificacao possa ser pre-preenchida coerente com cada um quando a E18
# existir. Nomes e enderecos ficticios, sob .test.
PARTICIPANTES_ENSAIO = [
    {"firstname": "Ensaio", "lastname": f"Percurso {i:02d}",
     "email": f"percurso{i:02d}@egressos.test"}
    for i in range(1, 13)
]


def cmd_copia(args):
    # Sid proprio para a copia, para que ela nunca ocupe o do instrumento.
    sid_copia = random.randint(100000, 999999)
    while sid_copia == SID_INSTRUMENTO:
        sid_copia = random.randint(100000, 999999)
    conteudo = monta_lss(sid_copia)
    with api() as sessao:
        sid = importa(sessao, conteudo, sid_copia)
        if sid == SID_INSTRUMENTO:
            raise Erro("a copia recebeu o sid do instrumento — abortado")
        # Acesso fechado: so com endereco individual. E o modo da E17, que a
        # copia antecipa para poder conferir o comportamento com participantes
        # identificados.
        sessao.chamar("set_survey_properties", [sid, {"access_mode": "C"}])
        sessao.chamar("activate_survey", [sid])
        sessao.chamar("activate_tokens", [sid, []])
        criados = sessao.chamar("add_participants",
                                [sid, PARTICIPANTES_ENSAIO, True])
    env = carrega_env()
    porta = env.get("PORTA_HTTP", "8080")
    print(f"copia de ensaio: questionario {sid} (ativo, acesso fechado)")
    for p in criados:
        print(f"  {p['lastname']:<12} http://127.0.0.1:{porta}/index.php/"
              f"{sid}?token={p['token']}&lang={IDIOMA}")


# Atributos da base central de participantes (E17). Os da origem sao os campos
# do leiaute alem de nome e e-mail principal, que tem coluna propria; os
# "_origem" guardam o ultimo valor de contato visto no arquivo, e e com eles que
# a importacao decide se uma correcao feita pelo mecanismo prevalece
# (docs/especificacao/importacao-base.md, secao 5). Os de contato sao cifrados,
# como a plataforma ja cifra nome e e-mail da base central.
ATRIBUTOS_BASE_CENTRAL = [
    "identificador", "curso", "nivel", "campus", "ano_conclusao",
    "semestre_conclusao", "email_alternativo:cifrado", "telefone:cifrado",
    "email_principal_origem:cifrado", "email_alternativo_origem:cifrado",
    "telefone_origem:cifrado",
]

# Atributos do participante do questionario, na ordem attribute_1, 2, ...
# So o que o questionario usa: o identificador, para reencontro, e os cinco
# atributos academicos do pre-preenchimento (E18). Via alternativa e telefone
# ficam so na base central (leiaute, secao 11).
ATRIBUTOS_QUESTIONARIO = [
    ("identificador", "identificador da instituição (nunca o token)"),
    ("curso", "código do curso no instrumento (IDA1)"),
    ("nivel", "nível do curso (IDA2)"),
    ("campus", "sigla da unidade no instrumento (IDA3)"),
    ("ano_conclusao", "ano de conclusão (IDA4)"),
    ("semestre_conclusao", "semestre de conclusão (IDA5)"),
    # Parametro do disparo, e nao estado: escolhe o ramo do lembrete e e
    # gravado pela rotina imediatamente antes de cada lembrete (E20, E21).
    (mensagens.ATRIBUTO_VARIANTE, "ramo do lembrete, gravado a cada disparo"),
]


def coluna_do_atributo(nome):
    """attribute_N do participante, pela ordem acima. E o unico lugar que liga
    o nome do atributo ao numero: a preparacao (E17) cria as colunas nesta
    ordem, e o pre-preenchimento (E18) as referencia pelo mesmo calculo."""
    nomes = [n for n, _ in ATRIBUTOS_QUESTIONARIO]
    if nome not in nomes:
        raise Erro(f"atributo do participante desconhecido: {nome}")
    return f"attribute_{nomes.index(nome) + 1}"


def numero_da_variante():
    """N de attribute_N do atributo que escolhe o ramo do lembrete."""
    return coluna_do_atributo(mensagens.ATRIBUTO_VARIANTE).split("_")[1]


def descricoes_dos_atributos():
    return {f"attribute_{i}": {"description": nome, "mandatory": "N",
                               "encrypted": "N", "show_register": "N",
                               "cpdbmap": ""}
            for i, (nome, _) in enumerate(ATRIBUTOS_QUESTIONARIO, start=1)}


def cmd_preparar(args):
    """Prepara o acesso controlado do instrumento (E17): atributos da base
    central, acesso fechado e tabela de participantes com atributos nomeados.
    Nao ativa o questionario — a ativacao trava a estrutura, e a E18 ainda
    configura o pre-preenchimento. Idempotente."""
    r = console("prepararbasecentral", ",".join(ATRIBUTOS_BASE_CENTRAL))
    if r.returncode != 0:
        raise Erro(f"atributos da base central: {r.stderr.strip() or r.stdout}")
    print("base central:")
    for linha in r.stdout.strip().splitlines():
        print("  " + linha)

    with api() as sessao:
        atual = existe(sessao, SID_INSTRUMENTO)
        if not atual:
            raise Erro(f"o questionario {SID_INSTRUMENTO} nao existe; implante antes")
        if atual.get("active") == "Y":
            raise Erro("o questionario ja esta ativo; a preparacao e anterior a "
                       "ativacao")
        sessao.chamar("set_survey_properties",
                      [SID_INSTRUMENTO, {"access_mode": "C"}])
        # A API responde "OK" tambem quando a tabela ja existe, e nesse caso
        # NAO a recria: Token::createTable captura o erro de tabela existente
        # e segue (conferido na E17). Rodar de novo nao apaga participantes.
        sessao.chamar("activate_tokens", [SID_INSTRUMENTO, list(
            range(1, len(ATRIBUTOS_QUESTIONARIO) + 1))])
        print(f"tabela de participantes do {SID_INSTRUMENTO}: criada ou mantida")
        sessao.chamar("set_survey_properties", [SID_INSTRUMENTO, {
            "attributedescriptions": json.dumps(descricoes_dos_atributos(),
                                                ensure_ascii=False)}])
        propriedades = sessao.chamar("get_survey_properties", [
            SID_INSTRUMENTO, ["access_mode", "active", "attributedescriptions"]])
    print(f"acesso: {propriedades.get('access_mode')}; ativo: "
          f"{propriedades.get('active')}")
    for chave, info in sorted(json.loads(
            propriedades.get("attributedescriptions") or "{}").items()):
        print(f"  {chave} = {info.get('description')}")


def cmd_ativar(args):
    """Ativa o instrumento (E18): cria a tabela de respostas e abre o acesso
    por endereco individual. Depois disto a estrutura fica travada — por isso
    vem por ultimo, depois do pre-preenchimento, da preparacao e da importacao.
    Recusa se o acesso nao estiver fechado ou se nao houver participantes."""
    with api() as sessao:
        atual = existe(sessao, SID_INSTRUMENTO)
        if not atual:
            raise Erro(f"o questionario {SID_INSTRUMENTO} nao existe")
        if atual.get("active") == "Y":
            print(f"questionario {SID_INSTRUMENTO}: ja ativo")
            return
        props = sessao.chamar("get_survey_properties",
                              [SID_INSTRUMENTO, ["access_mode"]])
        if props.get("access_mode") != "C":
            raise Erro("o acesso nao esta fechado — rode preparar-participantes")
        if not sessao.participantes(SID_INSTRUMENTO, limite=1):
            raise Erro("o questionario nao tem participantes — importe a base")
        resposta = sessao.chamar("activate_survey", [SID_INSTRUMENTO])
        resumo = sessao.chamar("get_summary", [SID_INSTRUMENTO])
    print(f"questionario {SID_INSTRUMENTO}: ativado ({resposta.get('status')})")
    print(f"participantes: {resumo.get('token_count')}; respostas: "
          f"{resumo.get('completed_responses')} completas, "
          f"{resumo.get('incomplete_responses')} incompletas")


def cmd_mensagens(args):
    """Aplica ao instrumento os modelos de mensagem, o remetente e o retorno
    (E20), e garante a coluna do atributo que escolhe o ramo do lembrete.
    Funciona com o questionario ATIVO: nada disso e estrutura travada pela
    ativacao — modelos e remetente sao propriedades, e a tabela de
    participantes recebe coluna nova como o painel faz. Idempotente. Nao
    envia mensagem alguma."""
    n = len(ATRIBUTOS_QUESTIONARIO)
    r = console("completaratributos", SID_INSTRUMENTO, n)
    if r.returncode != 0:
        raise Erro(f"atributos do participante: {r.stderr.strip() or r.stdout}")
    print(r.stdout.strip())
    with api() as sessao:
        if not existe(sessao, SID_INSTRUMENTO):
            raise Erro(f"o questionario {SID_INSTRUMENTO} nao existe")
        sessao.chamar("set_survey_properties", [SID_INSTRUMENTO, {
            **mensagens.propriedades_do_questionario(),
            "attributedescriptions": json.dumps(descricoes_dos_atributos(),
                                                ensure_ascii=False)}])
        sessao.chamar("set_language_properties", [
            SID_INSTRUMENTO, mensagens.propriedades_de_idioma(
                numero_da_variante()), IDIOMA])
        props = sessao.chamar("get_survey_properties", [
            SID_INSTRUMENTO, ["admin", "adminemail", "bounce_email"]])
        idioma = sessao.chamar("get_language_properties", [
            SID_INSTRUMENTO, ["surveyls_email_invite_subj",
                              "surveyls_email_remind_subj"], IDIOMA])
    print(f"remetente: {props.get('admin')} <{props.get('adminemail')}>; "
          f"retorno: {props.get('bounce_email')}")
    print(f"assunto do convite:  {idioma.get('surveyls_email_invite_subj')}")
    print(f"assunto do lembrete: {idioma.get('surveyls_email_remind_subj')}")
    print(f"ramo do lembrete: {coluna_do_atributo(mensagens.ATRIBUTO_VARIANTE)}"
          f" ({mensagens.ATRIBUTO_VARIANTE})")


def cmd_remover(args):
    if args.sid == SID_INSTRUMENTO:
        raise Erro("recusado: este e o sid do instrumento, nao de uma copia")
    with api() as sessao:
        sessao.chamar("delete_survey", [args.sid])
    print(f"removido: questionario {args.sid}")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gerar")
    g.add_argument("--saida", default="/tmp/instrumento-gerado.lss")
    g.set_defaults(f=cmd_gerar)
    i = sub.add_parser("implantar")
    i.add_argument("--substituir", action="store_true")
    i.set_defaults(f=cmd_implantar)
    e = sub.add_parser("exportar")
    e.add_argument("--sid", type=int, required=True)
    e.add_argument("--saida", required=True)
    e.set_defaults(f=cmd_exportar)
    c = sub.add_parser("copia-de-ensaio")
    c.set_defaults(f=cmd_copia)
    pp = sub.add_parser("preparar-participantes")
    pp.set_defaults(f=cmd_preparar)
    at = sub.add_parser("ativar")
    at.set_defaults(f=cmd_ativar)
    me = sub.add_parser("aplicar-mensagens")
    me.set_defaults(f=cmd_mensagens)
    r = sub.add_parser("remover")
    r.add_argument("--sid", type=int, required=True)
    r.set_defaults(f=cmd_remover)
    args = p.parse_args()
    try:
        args.f(args)
    except (Erro, ErroAPI) as ex:
        print(f"erro: {ex}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
