#!/usr/bin/env python3
"""
Recupera o registro de consentimento de um participante (E22).

O aceite so serve de prova se puder ser recuperado: o onus de demonstrar que o
consentimento foi obtido e do controlador (LGPD, art. 8, par. 2). Para um
identificador, este comando mostra cada manifestacao registrada no questionario
— o que foi escolhido em CON1 e CON2, quando, e sob que versao do termo — e
CONFERE que o texto arquivado daquela versao e o que o respondente viu: a
resposta guarda o resumo SHA-256 do documento da pagina 1, e o arquivo de
instrumento/termos/ tem de produzir o mesmo resumo.

Le a resposta pela exportacao da propria plataforma (export_responses_by_token),
e nao pelo esquema interno das tabelas. A recusa pelo endereco da mensagem e lida
no participante, pela API, e na base central, so leitura. Nao imprime nome,
endereco nem token.

Uso, a partir da pasta infra/:

    python3 consulta-consentimento.py --identificador SIN-000123 [--sid 202615]
"""

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))
sys.path.insert(0, os.path.join(AQUI, "instrumento"))

import estrutura  # noqa: E402
import termo  # noqa: E402
from limesurvey_api import ErroAPI  # noqa: E402
from limesurvey_console import api_do_hospedeiro  # noqa: E402

# A consulta so de leitura ao banco, a mesma da conferencia da E19.
_spec = importlib.util.spec_from_file_location(
    "confere_participantes", os.path.join(AQUI, "confere-participantes.py"))
_cp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cp)
sql = _cp.sql

SID = 202615


def rotulos(codigo):
    for g in estrutura.GRUPOS:
        for c in g["campos"]:
            if c["codigo"] == codigo:
                return dict(c.get("opcoes") or [])
    return {}


def _registros(dados):
    """A exportacao em JSON traz {"responses": [...]}, e cada item vem ora como o
    registro, ora como {id: registro}. Devolve sempre a lista de registros."""
    saida = []
    for item in dados.get("responses", []):
        if isinstance(item, dict) and len(item) == 1:
            unico = next(iter(item.values()))
            if isinstance(unico, dict):
                saida.append(unico)
                continue
        saida.append(item)
    return saida


def confere_versao(conv):
    """(versao, resumo, arquivo, confere) a partir do valor gravado em CONV."""
    versao, _, resto = (conv or "").partition(" ")
    resumo = resto.removeprefix("sha256:") if resto.startswith("sha256:") else ""
    arquivado = termo.le_arquivado(versao) if versao else None
    confere = bool(arquivado) and bool(resumo) and hashlib.sha256(
        arquivado.encode("utf-8")).hexdigest() == resumo
    arquivo = os.path.relpath(termo.caminho_do_arquivo(versao), AQUI) \
        if arquivado is not None else None
    return versao, resumo, arquivo, confere


def consulta(sessao, sid, identificador):
    """O registro de consentimento de uma pessoa, como dicionario."""
    descricoes = json.loads(sessao.chamar("get_survey_properties", [
        sid, ["attributedescriptions"]]).get("attributedescriptions") or "{}")
    coluna = next((col for col, info in descricoes.items()
                   if info.get("description") == "identificador"), None)
    if coluna is None:
        raise SystemExit("o questionario nao tem atributo 'identificador'")
    alvo = next((p for p in sessao.participantes(
        sid, limite=100000, atributos=[coluna, "emailstatus", "participant_id"])
        if str(p.get(coluna, "")).lower() == identificador.lower()), None)
    if alvo is None:
        return None

    try:
        bruto = sessao.chamar("export_responses_by_token", [
            sid, "json", alvo["token"], None, "all", "code", "short"])
        respostas = _registros(json.loads(base64.b64decode(bruto)))
    except ErroAPI as e:
        if "No Response found" not in str(e) and "No Data" not in str(e):
            raise
        respostas = []

    r1, r2 = rotulos("CON1"), rotulos("CON2")
    manifestacoes, aberturas = [], 0
    for r in sorted(respostas, key=lambda x: int(x.get("id") or 0)):
        con1 = (r.get("CON1") or "").strip()
        if not con1:
            aberturas += 1
            continue
        versao, resumo, arquivo, confere = confere_versao(r.get("CONV"))
        manifestacoes.append({
            "resposta": r.get("id"),
            "enviada": bool(r.get("submitdate")),
            "con1": con1, "con1_rotulo": r1.get(con1, con1),
            "con2": (r.get("CON2") or "").strip() or None,
            "con2_rotulo": r2.get((r.get("CON2") or "").strip()),
            "momento": r.get("CONDH") or None,
            "versao": versao or None, "resumo": resumo or None,
            "arquivo": arquivo, "texto_confere": confere,
        })

    pid = alvo.get("participant_id") or ""
    base = sql("SELECT blacklisted FROM lime_participants WHERE "
               f"participant_id='{pid}'")
    # O registro das recusas (E23): o que a pessoa recusou, por que via,
    # quando, sob que versao, quando chegou a base central, e a revogacao.
    recusas = sql(
        "SELECT questionario, ciclo, tipo, via, manifestada_em, "
        "fonte_do_momento, versao_termo, base_central_em, revogada_em, "
        "revogacao FROM egressos_recusas WHERE participant_id="
        f"'{pid}' ORDER BY id") \
        if sql("SHOW TABLES LIKE 'egressos_recusas'") else []
    return {
        "identificador": identificador, "questionario": sid,
        "tid": int(alvo["tid"]), "manifestacoes": manifestacoes,
        "aberturas_sem_manifestacao": aberturas,
        "recusa_pela_mensagem": {
            "participante": str(alvo.get("emailstatus", "")).startswith("OptOut"),
            "base_central": bool(base) and base[0]["blacklisted"] == "Y",
        },
        "recusas_registradas": recusas,
    }


def imprime(reg):
    print(f"Identificador {reg['identificador']} · questionario "
          f"{reg['questionario']} · participante tid {reg['tid']}")
    if not reg["manifestacoes"]:
        print("  nenhuma manifestacao sobre o termo registrada")
    for i, m in enumerate(reg["manifestacoes"], 1):
        situacao = "enviada" if m["enviada"] else "nao enviada (em preenchimento)"
        con2 = f" · CON2 {m['con2_rotulo']}" if m["con2"] else ""
        print(f"  manifestacao {i} (resposta {m['resposta']}, {situacao}): "
              f"CON1 {m['con1_rotulo']}{con2}")
        conferido = (f"texto conferido em {m['arquivo']}" if m["texto_confere"]
                     else "TEXTO NAO CONFERE com o arquivado")
        print(f"    em {m['momento'] or '(sem momento registrado)'} · termo "
              f"{m['versao'] or '(sem versao)'} · {conferido}"
              + (f" (sha256 {m['resumo'][:12]}...)" if m["resumo"] else ""))
    if reg["aberturas_sem_manifestacao"]:
        print(f"  aberturas do endereco sem manifestacao: "
              f"{reg['aberturas_sem_manifestacao']}")
    rm = reg["recusa_pela_mensagem"]
    print("  bloqueio agora: "
          + f"participante {'OptOut' if rm['participante'] else 'sem recusa'}; "
          f"base central {'bloqueada' if rm['base_central'] else 'sem bloqueio'}")
    recusas = reg.get("recusas_registradas") or []
    if not recusas:
        print("  recusas registradas: nenhuma")
    for i, r in enumerate(recusas, 1):
        print(f"  recusa {i}: {r['tipo']} pela {r['via']} (questionario "
              f"{r['questionario']}, ciclo {r['ciclo']}) em "
              f"{r['manifestada_em']} [{r['fonte_do_momento']}] · termo "
              f"{(r['versao_termo'] or '-').split(' ')[0]}")
        estado = (f"revogada em {r['revogada_em']} — {r['revogacao']}"
                  if r["revogada_em"] else
                  f"na base central desde {r['base_central_em']}"
                  if r["base_central_em"] else
                  "vale so neste ciclo" if r["tipo"] == "consentimento"
                  else "ainda nao levada a base central")
        print(f"    {estado}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--identificador", required=True)
    ap.add_argument("--sid", type=int, default=SID)
    args = ap.parse_args()
    with api_do_hospedeiro() as sessao:
        reg = consulta(sessao, args.sid, args.identificador)
    if reg is None:
        print(f"identificador {args.identificador} nao encontrado no "
              f"questionario {args.sid}", file=sys.stderr)
        return 1
    imprime(reg)
    ok = all(m["texto_confere"] for m in reg["manifestacoes"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
