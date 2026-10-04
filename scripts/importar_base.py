#!/usr/bin/env python3
"""
Importa o arquivo de entrada na base central de participantes e no questionario
(E17).

O desenho esta em docs/especificacao/importacao-base.md, e a decisao de manter
base persistente, na ADR-0007. Em sequencia:

  1. VALIDA o arquivo contra o leiaute (valida_entrada.py). Arquivo rejeitado
     nao importa nada.
  2. CONFERE que a configuracao de cursos e unidades e o mesmo dominio que o
     instrumento oferece em IDA1 e IDA3 — se diferissem, o pre-preenchimento
     exibiria valor fora das opcoes (E11, secao 4.3).
  3. GRAVA na base central, uma pessoa por identificador, pelo comando de
     console `importarbasecentral` — dentro da plataforma, porque nome, e-mail e
     contatos sao cifrados, e a regra de precedencia precisa decifra-los. O
     participant_id e derivado do identificador (UUID v5), e e assim que a
     reimportacao reencontra a pessoa sem criar outra. A recusa permanente nunca
     e tocada.
  4. CRIA ou ATUALIZA o participante do questionario, pela API, ligado a base
     central pelo participant_id — o elo que a recusa global da plataforma usa.
     Quem tem recusa permanente nao e acrescentado. Os atributos academicos vao
     com o CODIGO do instrumento (curso T01, campus SPO).
  5. ELIMINA o arquivo, terminado o tratamento (LGPD, art. 16), e REGISTRA a
     importacao na trilha egressos_importacoes: data, SHA-256 do arquivo e
     contagens por regra.

Roda no HOSPEDEIRO, da raiz do repositorio, porque chama o console da plataforma
(`docker compose exec`), que o conteiner `rotinas` nao alcanca:

    python3 scripts/importar_base.py --arquivo dados/sinteticos/base-sintetica.csv \\
        --questionario 202615

O arquivo e eliminado ao fim, importado ou rejeitado; abortada a importacao,
ele fica, para que se repita. O relatorio nao reproduz nome, endereco nem
telefone.
"""

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime

from limesurvey_api import ErroAPI
from limesurvey_console import api_do_hospedeiro, console
from valida_entrada import le_configuracao, relatorio, valida

# Espaco de nomes do participant_id derivado. Fixo: muda-lo faria toda pessoa
# ja importada voltar como pessoa nova.
ESPACO_PARTICIPANTE = uuid.uuid5(
    uuid.NAMESPACE_URL,
    "https://github.com/matheusreisl/projeto-egressos-ifsp-estrutura/identificador")

ACADEMICOS = ("curso", "nivel", "campus", "ano_conclusao", "semestre_conclusao")
IDIOMA = "pt-BR"
LOTE = 100


class Abortado(Exception):
    pass


def participant_id(identificador):
    """Derivado do identificador, sem distinguir caixa — a mesma regra de
    unicidade do leiaute (secao 4.1). Nao e segredo, e nunca e o token."""
    return str(uuid.uuid5(ESPACO_PARTICIPANTE, identificador.lower()))


# ---------------------------------------------------------------------------
# Conferencias contra o instrumento
# ---------------------------------------------------------------------------

def opcoes_do_instrumento(api, questionario, codigo_questao):
    for q in api.chamar("list_questions", [questionario]):
        if q["title"] == codigo_questao and int(q["parent_qid"]) == 0:
            p = api.chamar("get_question_properties", [int(q["qid"])])
            return {o["answer"]: c for c, o in p["answeroptions"].items()}
    raise Abortado(f"questao {codigo_questao} nao encontrada no questionario")


def confere_dominio(api, questionario, cfg):
    """A configuracao e o mesmo dominio do instrumento? Devolve os mapas
    nome -> codigo de curso e de unidade."""
    cursos = opcoes_do_instrumento(api, questionario, "IDA1")
    unidades = opcoes_do_instrumento(api, questionario, "IDA3")
    if (cursos != {n: c["codigo"] for n, c in cfg["cursos"].items()}
            or unidades != {n: u["codigo"] for n, u in cfg["unidades"].items()}):
        raise Abortado("a configuracao de cursos e unidades difere das opcoes do "
                       "instrumento — reimplante o instrumento ou corrija a "
                       "configuracao antes de importar")
    return cursos, unidades


def atributos_do_questionario(api, questionario):
    """Descricao -> coluna (attribute_N), pela configuracao gravada."""
    p = api.chamar("get_survey_properties", [questionario, ["attributedescriptions"]])
    descricoes = json.loads(p.get("attributedescriptions") or "{}")
    mapa = {info.get("description"): coluna for coluna, info in descricoes.items()}
    faltando = [a for a in ("identificador",) + ACADEMICOS if a not in mapa]
    if faltando:
        raise Abortado(f"a tabela de participantes nao tem os atributos {faltando}"
                       " — rode instrumento.py preparar-participantes")
    return mapa


# ---------------------------------------------------------------------------
# Importacao
# ---------------------------------------------------------------------------

def grava_base_central(aceitos):
    registros = [dict(r, participant_id=participant_id(r["identificador"]))
                 for _, r in aceitos]
    r = console("importarbasecentral",
                entrada=json.dumps({"idioma": IDIOMA, "registros": registros},
                                   ensure_ascii=False))
    if r.returncode != 0:
        raise Abortado(f"base central: {r.stderr.strip() or r.stdout[:300]}")
    return registros, json.loads(r.stdout)


def grava_questionario(api, questionario, registros, base, cursos, unidades,
                       colunas):
    contas = dict(participantes_criados=0, participantes_atualizados=0,
                  bloqueados_por_recusa=0)
    existentes = {p.get("participant_id"): p for p in api.participantes(
        questionario, limite=100000, atributos=["participant_id", "email"])}
    novos = []
    for r in registros:
        pid = r["participant_id"]
        final = base["participantes"][pid]
        dados = {"firstname": r["nome"], "lastname": "", "email": final["email"],
                 "language": IDIOMA,
                 colunas["identificador"]: r["identificador"],
                 colunas["curso"]: cursos[r["curso"]],
                 colunas["nivel"]: r["nivel"],
                 colunas["campus"]: unidades[r["campus"]],
                 colunas["ano_conclusao"]: r["ano_conclusao"],
                 colunas["semestre_conclusao"]: r["semestre_conclusao"]}
        atual = existentes.get(pid)
        if atual is None:
            if final["blacklisted"] == "Y":
                # Recusa permanente: nao entra no ciclo — o equivalente do
                # blockaddingtosurveys da plataforma, que so vale pela tela.
                contas["bloqueados_por_recusa"] += 1
                continue
            novos.append(dict(dados, participant_id=pid))
            continue
        if (atual.get("email") or "").lower() != final["email"].lower():
            # Endereco novo: o estado de entrega era do endereco anterior.
            dados["emailstatus"] = "OK"
        api.chamar("set_participant_properties",
                   [questionario, {"tid": int(atual["tid"])}, dados])
        contas["participantes_atualizados"] += 1

    for i in range(0, len(novos), LOTE):
        criados = api.chamar("add_participants",
                             [questionario, novos[i:i + LOTE], True])
        erros = [c for c in criados if isinstance(c, dict) and c.get("errors")]
        if erros:
            raise Abortado(f"{len(erros)} participantes recusados pela plataforma:"
                           f" {erros[0]['errors']}")
        contas["participantes_criados"] += len(criados)
    return contas


def registra_trilha(linha):
    r = console("registrarimportacao", entrada=json.dumps(linha, ensure_ascii=False))
    if r.returncode != 0:
        raise RuntimeError(f"trilha nao registrada: {r.stderr.strip()}")
    return r.stdout.strip()


def main():
    p = argparse.ArgumentParser(description="Importa o arquivo de entrada (E17).")
    p.add_argument("--arquivo", required=True)
    p.add_argument("--questionario", type=int, required=True)
    args = p.parse_args()

    with open(args.arquivo, "rb") as fh:
        conteudo = fh.read()
    sha = hashlib.sha256(conteudo).hexdigest()
    cfg = le_configuracao()
    res = valida(conteudo, cfg)
    print(f"arquivo sha256: {sha}")
    print(relatorio(res))

    linha = {"importado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             "arquivo_sha256": sha, "questionario": args.questionario,
             "modo": "ensaio", "registros": res.linhas,
             "aceitos": len(res.aceitos), "aceitos_com_alerta": res.com_alerta(),
             "rejeitados": len(res.rejeitados),
             "contagens_por_regra": json.dumps(res.contagens(), ensure_ascii=False)}
    codigo = 0
    if res.arquivo_rejeitado:
        linha.update(situacao="arquivo_rejeitado", motivo=res.arquivo_rejeitado)
        codigo = 1
    else:
        try:
            with api_do_hospedeiro() as api:
                cursos, unidades = confere_dominio(api, args.questionario, cfg)
                colunas = atributos_do_questionario(api, args.questionario)
                registros, base = grava_base_central(res.aceitos)
                linha.update(
                    base_central_criados=base["criados"],
                    base_central_atualizados=base["atualizados"],
                    origem_substituiu_correcao=base["origem_substituiu_correcao"])
                linha.update(grava_questionario(api, args.questionario, registros,
                                                base, cursos, unidades, colunas))
            linha["situacao"] = "importado"
        except (Abortado, ErroAPI) as e:
            # Abortada, a importacao nao elimina o arquivo: o tratamento nao
            # terminou, e ele precisa estar la para repetir. A base central e
            # gravada numa transacao, e a repeticao e idempotente.
            linha.update(situacao="abortado", motivo=str(e))
            print(f"ABORTADO: {e}")
            print(f"trilha: egressos_importacoes #{registra_trilha(linha)}; "
                  "arquivo mantido")
            return 2

    # Terminado o tratamento — importado ou rejeitado —, o arquivo e eliminado
    # (LGPD, art. 16), e a trilha registra se foi.
    try:
        os.remove(args.arquivo)
        linha["arquivo_eliminado"] = 1
    except OSError as e:
        print(f"ATENCAO: o arquivo nao pode ser eliminado ({e})")
        linha["arquivo_eliminado"] = 0
    id_trilha = registra_trilha(linha)

    if not res.arquivo_rejeitado:
        for chave in ("base_central_criados", "base_central_atualizados",
                      "participantes_criados", "participantes_atualizados",
                      "bloqueados_por_recusa", "origem_substituiu_correcao"):
            print(f"{chave.replace('_', ' ')}: {linha[chave]}")
    print(f"trilha: egressos_importacoes #{id_trilha}; arquivo "
          + ("eliminado" if linha["arquivo_eliminado"] else "MANTIDO"))
    return codigo


if __name__ == "__main__":
    sys.exit(main())
