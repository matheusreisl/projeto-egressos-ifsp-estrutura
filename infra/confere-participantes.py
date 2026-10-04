#!/usr/bin/env python3
"""
Confere a unicidade e a integridade da base de participantes (E19).

So le: nao altera participante, token nem base central. Le a tabela de
participantes do questionario e a base central de participantes, e confere:

  1. todo participante tem token — o que a plataforma chama de token invalido
     (`token_invalid` no resumo da API) e exatamente o token nulo ou vazio;
  2. todo token tem o comprimento configurado no questionario e so caracteres
     alfanumericos, que e o que o gerador da plataforma produz;
  3. nenhum token repetido — nem exato, nem sem distinguir maiusculas: dois
     tokens que so diferem na caixa seriam confundidos por quem os digita;
  4. todo participante tem identificador, e nenhum identificador se repete, sem
     distinguir maiusculas (leiaute, secao 4.1);
  5. nenhum identificador e igual a um token (leiaute, secao 4.1, e C1);
  6. o elo com a base central: participant_id unico no questionario, presente na
     base central e igual ao UUID v5 do identificador — a regra da E17,
     recalculada aqui, e nao importada do importador;
  7. a base central: identificador unico, participant_id derivado dele, e toda
     pessoa sem recusa com participante no questionario;
  8. o e-mail principal compartilhado forma os MESMOS grupos de pessoas no
     questionario, onde esta em claro, e na base central, onde a cifragem
     deterministica da plataforma permite comparar sem decifrar.

O compartilhamento de e-mail nao e defeito: o leiaute o aceita com alerta,
porque endereco compartilhado existe de verdade. E listado para REVISAO HUMANA,
pelos identificadores, sem nome nem endereco — o mecanismo nao funde pessoas
(decisao da E19, docs/especificacao/unicidade-participantes.md).

Uso, a partir da pasta infra/:

    python3 confere-participantes.py [--sid 202615]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))

# A regra do participant_id da E17 (importacao-base.md, secao 3): UUID v5 do
# identificador em minusculas, neste espaco de nomes.
ESPACO = uuid.uuid5(
    uuid.NAMESPACE_URL,
    "https://github.com/matheusreisl/projeto-egressos-ifsp-estrutura/identificador")


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


def carrega(sid):
    comprimento = int(sql(f"SELECT tokenlength FROM lime_surveys WHERE sid={sid}")
                      [0]["tokenlength"])
    descricoes = sql(f"SELECT attributedescriptions FROM lime_surveys WHERE sid={sid}")
    colunas ={info.get("description"): col for col, info in json.loads(
        descricoes[0]["attributedescriptions"] or "{}").items()}
    col_ident = colunas.get("identificador")
    if col_ident is None:
        raise SystemExit("o questionario nao tem atributo 'identificador'")
    participantes = sql(
        f"SELECT tid, token, participant_id, email, {col_ident} AS identificador "
        f"FROM lime_tokens_{sid}")
    base = sql("""
        SELECT p.participant_id, p.email AS email_cifrado, p.blacklisted,
               a.value AS identificador
          FROM lime_participants p
          LEFT JOIN lime_participant_attribute a
            ON a.participant_id = p.participant_id
           AND a.attribute_id = (SELECT attribute_id
                                   FROM lime_participant_attribute_names
                                  WHERE defaultname = 'identificador')""")
    return {"comprimento": comprimento, "participantes": participantes,
            "base": base}


def repetidos(valores):
    contagem = defaultdict(int)
    for v in valores:
        contagem[v] += 1
    return sorted(v for v, n in contagem.items() if n > 1)


def confere(d):
    """Devolve (resultados, grupos de e-mail compartilhado). Cada resultado e
    (numero, descricao, ok, detalhe). Nao imprime dado pessoal."""
    res = []
    P, B, L = d["participantes"], d["base"], d["comprimento"]
    tokens = [p["token"] or "" for p in P]

    vazios = sum(1 for t in tokens if not t)
    res.append((1, "todo participante tem token (token invalido da plataforma: 0)",
                vazios == 0, f"{vazios} sem token" if vazios else f"{len(P)} participantes"))

    fora = [p["tid"] for p in P if p["token"] and
            not re.fullmatch(rf"[A-Za-z0-9]{{{L}}}", p["token"])]
    res.append((2, f"todo token com {L} caracteres alfanumericos",
                not fora, f"tid {fora[:5]}" if fora else ""))

    exatos = repetidos([t for t in tokens if t])
    sem_caixa = repetidos([t.lower() for t in tokens if t])
    res.append((3, "nenhum token repetido, nem sem distinguir maiusculas",
                not exatos and not sem_caixa,
                f"{len(exatos)} repetidos; {len(sem_caixa)} sem caixa"
                if exatos or sem_caixa else ""))

    idents = [(p["identificador"] or "").lower() for p in P]
    sem_ident = sum(1 for i in idents if not i)
    rep_ident = repetidos([i for i in idents if i])
    res.append((4, "todo participante tem identificador, sem repeticao",
                not sem_ident and not rep_ident,
                f"{sem_ident} sem identificador; repetidos {rep_ident[:5]}"
                if sem_ident or rep_ident else ""))

    iguais = sorted(set(idents) & {t.lower() for t in tokens if t})
    res.append((5, "nenhum identificador igual a token", not iguais,
                f"{len(iguais)} coincidencias" if iguais else ""))

    pids_base = {b["participant_id"] for b in B}
    pids = [p["participant_id"] or "" for p in P]
    problemas = []
    if repetidos([x for x in pids if x]):
        problemas.append("participant_id repetido")
    sem_pid = sum(1 for x in pids if not x)
    if sem_pid:
        problemas.append(f"{sem_pid} sem participant_id")
    orfaos = sum(1 for x in pids if x and x not in pids_base)
    if orfaos:
        problemas.append(f"{orfaos} sem pessoa na base central")
    nao_derivados = sum(1 for p in P if p["participant_id"] and p["identificador"]
                        and p["participant_id"] != str(uuid.uuid5(
                            ESPACO, p["identificador"].lower())))
    if nao_derivados:
        problemas.append(f"{nao_derivados} participant_id nao derivado do identificador")
    res.append((6, "elo com a base central: participant_id unico, presente e "
                   "derivado do identificador", not problemas, "; ".join(problemas)))

    problemas = []
    ib = [(b["identificador"] or "").lower() for b in B]
    if sum(1 for i in ib if not i):
        problemas.append(f"{sum(1 for i in ib if not i)} pessoas sem identificador")
    if repetidos([i for i in ib if i]):
        problemas.append("identificador repetido")
    nd = sum(1 for b in B if b["identificador"] and b["participant_id"] !=
             str(uuid.uuid5(ESPACO, b["identificador"].lower())))
    if nd:
        problemas.append(f"{nd} participant_id nao derivado")
    no_questionario = set(pids)
    fora_do_ciclo = sum(1 for b in B if b["blacklisted"] != "Y"
                        and b["participant_id"] not in no_questionario)
    if fora_do_ciclo:
        problemas.append(f"{fora_do_ciclo} pessoas sem recusa fora do questionario")
    recusas = sum(1 for b in B if b["blacklisted"] == "Y")
    res.append((7, "base central: identificador unico e derivado; toda pessoa sem "
                   "recusa no questionario", not problemas,
                "; ".join(problemas) or f"{len(B)} pessoas, {recusas} com recusa"))

    def grupos(registros, chave):
        g = defaultdict(set)
        for r in registros:
            if chave(r):
                g[chave(r)].add(r["participant_id"])
        return {frozenset(v) for v in g.values() if len(v) > 1}
    no_q = grupos(P, lambda r: (r["email"] or "").lower())
    na_b = grupos(B, lambda r: r["email_cifrado"] or "")
    res.append((8, "e-mail principal compartilhado: mesmos grupos no questionario "
                   "e na base central", no_q == na_b,
                f"{len(no_q)} grupos no questionario, {len(na_b)} na base central"))

    ident_por_pid = {p["participant_id"]: p["identificador"] for p in P}
    lista = sorted(sorted(ident_por_pid.get(pid, pid) for pid in g) for g in no_q)
    return res, lista


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sid", type=int, default=202615)
    args = ap.parse_args()
    d = carrega(args.sid)
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
