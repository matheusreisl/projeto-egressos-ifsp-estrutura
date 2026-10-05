#!/usr/bin/env python3
"""
Confere a unicidade e a integridade da base de participantes (E19).

So le: nao altera participante, token nem base central. As oito conferencias
estao descritas em scripts/conferencia_participantes.py, onde a logica vive
desde a E21 — a mesma logica e a guarda que a rotina de disparo roda antes de
cada disparo, de dentro do conteiner. Aqui fica a linha de comando, que le o
banco pelo cliente do proprio conteiner do banco.

Uso, a partir da pasta infra/:

    python3 confere-participantes.py [--sid 202615]
"""

import argparse
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))

from conferencia_participantes import carrega, confere  # noqa: E402


def carrega_env():
    env = {}
    with open(os.path.join(AQUI, ".env"), encoding="utf-8") as fh:
        for linha in fh:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def sql(consulta):
    """Consulta so de leitura, pelo cliente do proprio conteiner do banco."""
    env = carrega_env()
    r = subprocess.run(
        ["docker", "compose", "exec", "-T", "banco", "mariadb", "--skip-ssl",
         "-B", f"-u{env['BANCO_USUARIO']}", f"-p{env['BANCO_SENHA']}",
         env["BANCO_NOME"], "-e", consulta],
        cwd=AQUI, capture_output=True, text=True, check=True)
    linhas = [l.split("\t") for l in r.stdout.rstrip("\n").split("\n") if l]
    if not linhas:
        return []
    return [dict(zip(linhas[0], [None if v == "NULL" else v for v in l]))
            for l in linhas[1:]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sid", type=int, default=202615)
    args = ap.parse_args()
    d = carrega(args.sid, sql)
    res, compartilhados = confere(d)
    print(f"Questionario {args.sid}: {len(d['participantes'])} participantes; "
          f"base central: {len(d['base'])} pessoas.\n")
    for n, desc, ok, det in res:
        print(f"[{'OK  ' if ok else 'FALHA'}] {n}. {desc}" + (f" — {det}" if det else ""))
    print(f"\nALERTA para revisao humana — e-mail principal compartilhado por "
          f"identificadores distintos: {len(compartilhados)} grupo(s)")
    for g in compartilhados:
        print("  " + " · ".join(g))
    criterio = all(ok for n, _, ok, _ in res if n in (1, 2, 3, 5))
    print(f"\n{sum(1 for r in res if r[2])} de {len(res)} conferencias passaram.")
    print("Criterio da E19 (nenhum token repetido ou invalido): "
          + ("atendido" if criterio else "NAO atendido"))
    return 0 if all(r[2] for r in res) else 1


if __name__ == "__main__":
    sys.exit(main())
