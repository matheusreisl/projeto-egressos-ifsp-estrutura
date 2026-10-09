#!/usr/bin/env python3
"""
Operacao de reparo de contato, no hospedeiro (E26).

O P8 marca como invalido o contato que devolve (docs/especificacao/
leitura-devolucoes.md), e o participante entra na fila de correcao — que e a
consulta de quem esta com contato invalido. O reparo automatizavel e o do
leiaute da E11: trocar o e-mail principal pelo alternativo. Decisao do
orientando na E21: nos dois lugares, o participante do questionario pela API e a
base central por console (comando repararcontato), porque o contato da base
central e cifrado e so se decifra com os modelos da plataforma.

Depois do reparo o participante volta a `pendente` (sent = N, contagem de
lembretes zerada, entrega OK), e a rotina da E21 o reconvida no proximo disparo,
com nova contagem — uma vez por ciclo (P4, secao 6.1). A mensagem que devolveu
nao conta no limite, porque nao foi entregue.

Recusa, sem gravar nada:
  - participante sem contato invalido (nada a reparar);
  - participante que ja respondeu (respondente com contato invalido continua
    respondente, rotina-disparo.md, secao 3);
  - teto do ciclo: ja houve reconvite depois de reparo neste questionario e
    ciclo — fica em contato invalido ate o ciclo seguinte;
  - e as recusas do comando de console: pessoa com recusa de contato, sem
    alternativo, alternativo igual ao principal.

Ordem: a base central primeiro, depois o questionario. Se a segunda falhar, a
base central ja tem o contato novo, e a reimportacao seguinte o levaria ao
participante; o comando avisa.

Roda no hospedeiro porque chama o console da plataforma (docker compose exec).
Nao imprime nome, endereco nem token.

Uso, a partir da pasta infra/:

    python3 reparo-contato.py --identificador SIN-000123            (repara)
    python3 reparo-contato.py --identificador SIN-000123 --simular  (so confere)
    python3 reparo-contato.py --fila                                 (lista a fila)
"""

import argparse
import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))

import cadencia  # noqa: E402
from limesurvey_console import api_do_hospedeiro, carrega_env, console  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "confere_participantes", os.path.join(AQUI, "confere-participantes.py"))
_cp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cp)
sql = _cp.sql

ENV = carrega_env()
AGENDA = cadencia.carrega_agenda(os.path.join(
    AQUI, "rotinas", "configuracao", "agenda.json"))
VALIDOS = ("OK", "OptOut")   # estado de entrega que nao e contato invalido


def fila(sid):
    """A fila de correcao: participantes com contato invalido, sem resposta
    concluida. So identificadores — nada de endereco."""
    return sql(
        f"SELECT tid, attribute_1 AS identificador, emailstatus, completed "
        f"FROM lime_tokens_{sid} WHERE emailstatus NOT IN ('OK','OptOut') "
        "AND completed = 'N' ORDER BY tid")


def reconvites(sid, ciclo, tid):
    return int(sql(
        "SELECT COUNT(*) n FROM egressos_disparos WHERE questionario="
        f"{sid} AND ciclo='{ciclo}' AND tid={tid} AND tipo='convite' AND "
        "motivo='reconvite' AND resultado='enviado'")[0]["n"])


def repara(sid, identificador, simular):
    # A regra do identificador no leiaute (secao 4.1) — e o que impede que o
    # argumento chegue ao SQL com outra coisa dentro.
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", identificador):
        return "recusado: identificador fora da regra do leiaute"
    ciclo = ENV.get("ROTINA_CICLO", "")
    linhas = sql(
        "SELECT tid, participant_id, emailstatus, completed, sent "
        f"FROM lime_tokens_{sid} WHERE attribute_1 = '{identificador}'")
    if len(linhas) != 1:
        return f"recusado: {len(linhas)} participante(s) com o identificador"
    p = linhas[0]
    tid = int(p["tid"])
    if p["emailstatus"] in VALIDOS:
        return f"recusado: tid {tid} sem contato invalido ({p['emailstatus']})"
    if p["completed"] not in ("N", "", None):
        return f"recusado: tid {tid} ja respondeu; continua respondente"
    feitos = reconvites(sid, ciclo, tid)
    if feitos >= AGENDA.reconvites_por_ciclo:
        return (f"recusado: tid {tid} — teto de reparo atingido no ciclo "
                f"{ciclo} ({feitos} reconvite); fica em contato invalido ate "
                "o ciclo seguinte")
    if simular:
        return (f"simulado: tid {tid} reparavel pelas regras do questionario; "
                "a base central confere o alternativo so no reparo")

    r = console("repararcontato",
                entrada=json.dumps({"participant_id": p["participant_id"]}))
    try:
        saida = json.loads(r.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return f"falha no console: {r.stderr.strip()[:300]}"
    if not saida.get("reparado"):
        return f"recusado pela base central: tid {tid} — {saida.get('motivo')}"

    try:
        with api_do_hospedeiro() as api:
            api.chamar("set_participant_properties", [sid, tid, {
                "email": saida["email"], "emailstatus": "OK", "sent": "N",
                "remindersent": "N", "remindercount": 0}])
    except Exception as e:  # noqa: BLE001 — avisa o estado intermediario
        return (f"ATENCAO: tid {tid} reparado na base central, mas o "
                f"questionario nao foi atualizado ({e}). A reimportacao leva o "
                "contato novo ao participante; o retorno a pendente, nao — "
                "rode de novo depois de corrigir a causa.")
    return (f"reparado: tid {tid} ({identificador}) — principal trocado pelo "
            "alternativo na base central e no questionario; volta a pendente, e "
            "a rotina o reconvida no proximo disparo, com nova contagem")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sid", type=int, default=int(
        ENV.get("ROTINA_QUESTIONARIO", "202615")))
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--identificador")
    grupo.add_argument("--fila", action="store_true",
                       help="lista a fila de correcao, sem reparar")
    ap.add_argument("--simular", action="store_true",
                    help="confere as regras do questionario, sem gravar")
    args = ap.parse_args()
    if args.fila:
        linhas = fila(args.sid)
        print(f"fila de correcao do questionario {args.sid}: {len(linhas)}")
        for l in linhas:
            print(f"  tid {l['tid']}  {l['identificador']}  {l['emailstatus']}")
        return 0
    resultado = repara(args.sid, args.identificador, args.simular)
    print(resultado)
    return 0 if resultado.startswith(("reparado", "simulado")) else 1


if __name__ == "__main__":
    sys.exit(main())
