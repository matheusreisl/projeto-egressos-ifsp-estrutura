#!/usr/bin/env python3
"""
Operacao de conformidade, no hospedeiro (E23).

  aplicar   ativa a trilha de auditoria da plataforma (AuditLog) por comando de
            console, sem tela, e confere a configuracao de que o mecanismo
            depende: a lista de bloqueio nos padroes certos e a correcao do
            AuditLog presente na imagem. Idempotente.

  revogar   revoga a recusa de contato de uma pessoa, a pedido dela. O egresso
            pede respondendo a uma mensagem, como o termo diz; o operador roda
            este comando, que tira o bloqueio pela propria plataforma (comando
            de console revogarrecusa, com trilha) e registra a revogacao em
            egressos_recusas — quando e a pedido de que, no texto que o operador
            der. Antes, roda a rotina de conformidade uma vez, para que a recusa
            esteja registrada antes de ser revogada.

Roda no hospedeiro porque chama o console da plataforma (docker compose exec).
Nao imprime nome, endereco nem token.

Uso, a partir da pasta infra/:

    python3 conformidade.py aplicar
    python3 conformidade.py revogar --identificador SIN-000123 \\
        --registro "pedido por resposta de 05/10/2026 na caixa acompanhamento"
"""

import argparse
import importlib.util
import os
import subprocess
import sys
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))

from limesurvey_console import console  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "confere_participantes", os.path.join(AQUI, "confere-participantes.py"))
_cp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cp)
sql = _cp.sql

# A configuracao da lista de bloqueio que o mecanismo exige, com o padrao da
# plataforma (config-defaults.php). Ver docs/especificacao/consentimento.md, 6.2.
LISTA_DE_BLOQUEIO = {
    # nome: (padrao, exigido, por que)
    "deleteblacklisted": ("N", "N", "apagar quem recusou apagaria a memoria da "
                                    "recusa (ADR-0007)"),
    "allowunblacklist": ("N", "N", "a revogacao e pelo operador, a pedido do "
                                   "egresso (E23)"),
    "blockaddingtosurveys": ("Y", "Y", "bloqueado nao entra em questionario "
                                       "novo pela base central"),
}


def agora_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def aplicar(_args):
    falhas = []
    r = console("ativarauditoria")
    if r.returncode != 0:
        falhas.append(f"ativacao do AuditLog: {r.stderr.strip()[-300:]}")
    else:
        for linha in r.stdout.strip().splitlines():
            print(f"trilha: {linha}")

    globais = {l["stg_name"]: l["stg_value"] for l in sql(
        "SELECT stg_name, stg_value FROM lime_settings_global WHERE stg_name "
        "IN (" + ",".join(f"'{n}'" for n in LISTA_DE_BLOQUEIO) + ")")}
    no_config = subprocess.run(
        ["docker", "compose", "exec", "-T", "limesurvey", "grep", "-E",
         "|".join(LISTA_DE_BLOQUEIO), "application/config/config.php"],
        cwd=AQUI, capture_output=True, text=True).stdout.strip()
    if no_config:
        falhas.append(f"config.php sobrescreve a lista de bloqueio: {no_config}")
    for nome, (padrao, exigido, motivo) in LISTA_DE_BLOQUEIO.items():
        valor = globais.get(nome, padrao)
        origem = "configurado" if nome in globais else "padrao"
        marca = "ok" if valor == exigido else "FALHA"
        print(f"lista de bloqueio: {nome} = {valor} ({origem}) [{marca}] — {motivo}")
        if valor != exigido:
            falhas.append(f"{nome} = {valor}, exigido {exigido}")

    sobra = subprocess.run(
        ["docker", "compose", "exec", "-T", "limesurvey", "grep", "-c",
         "= $oCurrentUser->uid;",
         "application/core/plugins/AuditLog/AuditLog.php"],
        cwd=AQUI, capture_output=True, text=True).stdout.strip()
    if sobra != "0":
        falhas.append("a imagem nao tem a correcao do AuditLog (limesurvey/"
                      "Dockerfile, secao 4.2): gravar na base central por "
                      "console quebraria")
    else:
        print("trilha: correcao do AuditLog presente na imagem")

    for f in falhas:
        print(f"FALHA: {f}", file=sys.stderr)
    return 0 if not falhas else 1


def pessoa_por_identificador(identificador):
    linhas = sql(
        "SELECT a.participant_id FROM lime_participant_attribute a JOIN "
        "lime_participant_attribute_names n ON n.attribute_id=a.attribute_id "
        "WHERE n.defaultname='identificador' AND LOWER(a.value)=LOWER('"
        + identificador.replace("'", "") + "')")
    return linhas[0]["participant_id"] if linhas else None


def revogar(args):
    pid = pessoa_por_identificador(args.identificador)
    if pid is None:
        print(f"identificador {args.identificador} nao esta na base central",
              file=sys.stderr)
        return 1

    # A recusa registrada antes de ser revogada: sem isto, uma recusa pela
    # mensagem ainda nao vista pela rotina sumiria sem rastro.
    r = subprocess.run(["docker", "compose", "exec", "-T", "rotinas", "python3",
                        "conformidade.py"], cwd=AQUI, capture_output=True,
                       text=True)
    if r.returncode != 0:
        print(f"rotina de conformidade: {r.stderr.strip() or r.stdout.strip()}",
              file=sys.stderr)
        return 1

    r = console("revogarrecusa", pid)
    if r.returncode != 0:
        print(f"revogacao na plataforma: {r.stderr.strip()[-300:]}",
              file=sys.stderr)
        return 1
    for linha in r.stdout.strip().splitlines():
        print(f"plataforma: {linha}")

    abertas = sql("SELECT COUNT(*) n FROM egressos_recusas WHERE "
                  f"participant_id='{pid}' AND tipo='contato' AND "
                  "revogada_em IS NULL")[0]["n"]
    registro = args.registro.replace("'", "")
    sql(f"UPDATE egressos_recusas SET revogada_em='{agora_iso()}', "
        f"revogacao='{registro}' WHERE participant_id='{pid}' AND "
        "tipo='contato' AND revogada_em IS NULL")
    print(f"registro: {abertas} recusa(s) de contato marcada(s) como revogada(s)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("aplicar").set_defaults(f=aplicar)
    r = sub.add_parser("revogar")
    r.add_argument("--identificador", required=True)
    r.add_argument("--registro", required=True,
                   help="de onde veio o pedido: data, via, caixa")
    r.set_defaults(f=revogar)
    args = ap.parse_args()
    return args.f(args)


if __name__ == "__main__":
    sys.exit(main())
