#!/usr/bin/env python3
"""
Agendador das rotinas do projeto (E21). E o processo principal do conteiner
rotinas: a composicao o sobe, e a politica de reinicio o mantem de pe.

Duas tarefas, independentes uma da outra:

  disparo      uma vez por dia util, no horario fixo da agenda (secao 5.3 do
               P3): convites e lembretes, por disparar.py
  devolucoes   a cada N minutos, em qualquer dia: le a caixa de devolucoes, por
               ler_devolucoes.py. Separada do disparo porque a devolucao
               temporaria chega depois do disparo que a originou (E09)

Por que um laco proprio, e nao o cron (ADR-0008): o cron do Debian nao passa as
variaveis de ambiente do conteiner aos trabalhos — e e por elas que chegam as
credenciais, que nao podem ir para arquivo versionado —, nao sabe o que e
execucao perdida e acrescentaria processo e pacote a imagem. O laco cabe na
biblioteca padrao e registra o que acontece no mesmo banco que a rotina usa.

O que o torna confiavel, e nao so funcional:

  - cada horario e RESERVADO por uma linha com chave unica em
    egressos_execucoes, antes de rodar: reiniciar o conteiner nao repete o
    disparo do dia, e dois agendadores nao disparam o mesmo horario;
  - o laco acorda a cada 20 s e rele o relogio, em vez de dormir ate o
    horario: um salto do relogio, que o WSL produz ao suspender e retomar (E07,
    E09, E10), nao o desorienta;
  - horario passado alem da tolerancia sem execucao vira linha `perdida`. Era
    a falha silenciosa da E07 — maquina desligada ou distribuicao parada no
    horario, e nada acontece sem que nada acuse. Agora fica o rastro. O que
    venceu sai no proximo dia util, no horario: a cadencia e por vencimento;
  - cada tarefa roda em subprocesso, com limite de tempo: a falha de uma nao
    derruba o agendador;
  - um arquivo de batimento alimenta a verificacao de saude do conteiner.

Ambiente:

  ROTINA_QUESTIONARIO   questionario do ciclo corrente
  ROTINA_CICLO          ano do ciclo
  ROTINA_DISPARO        `simulado` (padrao) calcula e registra o plano sem
                        enviar; `real` envia
  ROTINA_HORARIO        sobrescreve o horario da agenda. Existe so para a
                        verificacao do criterio da E21 e e anunciado no log
  ROTINA_AGENDA         caminho do agenda.json (padrao /configuracao/agenda.json)
"""

import dataclasses
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta

import pymysql

import cadencia
import disparar

MODO = os.environ.get("ROTINA_DISPARO", "simulado").strip().lower()
HORARIO = os.environ.get("ROTINA_HORARIO", "").strip()
BATIMENTO = "/tmp/agendador-vivo"
PASSO = 20
# Quantos dias para tras se procura horario perdido. Mais que isso, o registro
# ja acusou na passagem anterior, ou a rotina nem existia.
DIAS_PERDIDAS = 14
LIMITE_DISPARO = 3600
LIMITE_DEVOLUCOES = 900
AQUI = os.path.dirname(os.path.abspath(__file__))


def log(agenda, texto):
    print(f"[{datetime.now(agenda.fuso):%Y-%m-%d %H:%M:%S}] {texto}", flush=True)


def conecta(agenda):
    """Insiste ate o banco aceitar: depois de um reinicio do hospedeiro, o
    agendador pode subir antes dele."""
    while True:
        try:
            conexao = disparar.conecta()
            disparar.garante_tabelas(conexao)
            return conexao
        except pymysql.Error as e:
            log(agenda, f"banco indisponivel; nova tentativa em {PASSO} s ({e})")
            time.sleep(PASSO)


def viva(agenda, conexao):
    """A mesma conexao, se responde; outra, se caiu. O banco pode reiniciar
    por baixo do agendador, e o PyMySQL deixou de reconectar sozinho."""
    try:
        conexao.ping()
        return conexao
    except pymysql.Error:
        try:
            conexao.close()
        except pymysql.Error:
            pass
        return conecta(agenda)


def registrada(conexao, tarefa, previsto):
    with conexao.cursor() as cur:
        cur.execute("SELECT 1 FROM egressos_execucoes WHERE tarefa=%s AND "
                    "previsto_para=%s", (tarefa, disparar.local(previsto)))
        return cur.fetchone() is not None


def reserva(conexao, tarefa, previsto, situacao="reservada"):
    """Reserva o horario. None se ja estava reservado — por este agendador
    antes de um reinicio, ou por outro."""
    try:
        return disparar.abre_execucao(conexao, tarefa, MODO, "agendada",
                                      previsto=previsto, situacao=situacao)
    except pymysql.err.IntegrityError:
        return None


def registra_perdidas(conexao, agenda, agora):
    """Horario de disparo passado alem da tolerancia, sem execucao, vira
    `perdida`. So conta horario posterior ao primeiro registro da rotina —
    antes dele ela nao existia, e nao ha o que acusar."""
    with conexao.cursor() as cur:
        cur.execute("SELECT MIN(COALESCE(iniciado_em, previsto_para)) "
                    "FROM egressos_execucoes")
        primeiro = cur.fetchone()[0]
    if primeiro is None:
        return
    primeiro = primeiro.replace(tzinfo=agenda.fuso)
    tolerancia = timedelta(minutes=agenda.tolerancia_minutos)
    for d in range(DIAS_PERDIDAS, -1, -1):
        previsto = cadencia.previsto_para(agenda, agora.date() - timedelta(days=d))
        if previsto is None or previsto <= primeiro or previsto + tolerancia >= agora:
            continue
        if reserva(conexao, "disparo", previsto, situacao="perdida"):
            log(agenda, f"disparo de {previsto:%d/%m/%Y %H:%M} PERDIDO: o "
                        "agendador nao estava de pe no horario")


def fecha_se_aberta(conexao, execucao, situacao, erro):
    """Fecha a execucao que o subprocesso deixou aberta ao morrer."""
    with conexao.cursor() as cur:
        cur.execute("SELECT situacao FROM egressos_execucoes WHERE id=%s",
                    (execucao,))
        linha = cur.fetchone()
    if linha and linha[0] in ("reservada", "em_execucao"):
        disparar.fecha_execucao(conexao, execucao, situacao, erro=erro,
                                terminado=datetime.now())


def roda_disparo(conexao, agenda, execucao, previsto):
    log(agenda, f"disparo das {previsto:%H:%M}: inicio ({MODO})")
    comando = [sys.executable, os.path.join(AQUI, "disparar.py"),
               "--execucao", str(execucao),
               "--previsto-para", previsto.isoformat()]
    if MODO != "real":
        comando.append("--simular")
    try:
        r = subprocess.run(comando, timeout=LIMITE_DISPARO)
        codigo = r.returncode
    except subprocess.TimeoutExpired:
        codigo = "tempo esgotado"
    conexao = viva(agenda, conexao)
    fecha_se_aberta(conexao, execucao, "falha", f"disparar.py: {codigo}")
    log(agenda, f"disparo das {previsto:%H:%M}: fim (saida {codigo})")
    return conexao


def roda_devolucoes(conexao, agenda, execucao):
    inicio = datetime.now(agenda.fuso)
    comando = [sys.executable, os.path.join(AQUI, "ler_devolucoes.py"),
               "--ciclo", disparar.CICLO,
               "--questionario", disparar.QUESTIONARIO]
    if MODO != "real":
        comando.append("--simular")
    try:
        r = subprocess.run(comando, capture_output=True, text=True,
                           timeout=LIMITE_DEVOLUCOES)
        saida = (r.stdout + r.stderr).strip().splitlines()
        situacao = "concluida" if r.returncode == 0 else "falha"
    except subprocess.TimeoutExpired:
        saida, situacao = ["tempo esgotado"], "falha"
    conexao = viva(agenda, conexao)
    # Nao se guarda a saida inteira: ela traz enderecos devolvidos. Fica a
    # contagem, que e o que o registro precisa; o detalhe esta na tabela de
    # devolucoes da E09.
    resumo = {"linhas": [l for l in saida
                         if l.startswith(("mensagens nao lidas", "permanentes=",
                                          "nada a aplicar", "fila de correcao",
                                          "nenhum contato", "ERRO"))]}
    disparar.fecha_execucao(conexao, execucao, situacao, resumo,
                            iniciado=inicio,
                            terminado=datetime.now(agenda.fuso))
    if situacao != "concluida" or not any("nada a aplicar" in l
                                          for l in resumo["linhas"]):
        log(agenda, f"devolucoes: {situacao} · "
                    + " · ".join(resumo["linhas"] or saida[-2:]))
    return conexao


def main():
    if MODO not in ("real", "simulado"):
        print(f"ROTINA_DISPARO={MODO!r}: use 'real' ou 'simulado'",
              file=sys.stderr)
        return 2
    if not disparar.QUESTIONARIO or not (disparar.CICLO or "").isdigit():
        print("defina ROTINA_QUESTIONARIO e ROTINA_CICLO (ano do ciclo)",
              file=sys.stderr)
        return 2
    agenda = cadencia.carrega_agenda(disparar.AGENDA)
    if HORARIO:
        agenda = dataclasses.replace(
            agenda, horario=datetime.strptime(HORARIO, "%H:%M").time())

    dias = "".join("STQQSSD"[d] for d in sorted(agenda.dias_da_semana))
    log(agenda, f"agendador de pe · modo {MODO} · questionario "
                f"{disparar.QUESTIONARIO} · ciclo {disparar.CICLO}")
    log(agenda, f"disparo as {agenda.horario:%H:%M} ({dias}, menos "
                f"{len(agenda.feriados)} feriados), tolerancia "
                f"{agenda.tolerancia_minutos} min · lembretes D+"
                + ", D+".join(map(str, agenda.lembretes_dias))
                + f" · janela {agenda.janela_dias} dias · devolucoes a cada "
                f"{agenda.devolucoes_intervalo_minutos} min")
    if HORARIO:
        log(agenda, f"ATENCAO: horario sobrescrito por ROTINA_HORARIO={HORARIO}"
                    " — uso de verificacao, nao de operacao")
    for aviso in agenda.avisos:
        log(agenda, f"AVISO: {aviso}")

    conexao = conecta(agenda)
    ultima_busca_perdidas = None
    tolerancia = timedelta(minutes=agenda.tolerancia_minutos)
    passo_devolucoes = agenda.devolucoes_intervalo_minutos * 60

    while True:
        with open(BATIMENTO, "w") as fh:
            fh.write(datetime.now(agenda.fuso).isoformat())
        try:
            conexao = viva(agenda, conexao)
            agora = datetime.now(agenda.fuso)

            if (ultima_busca_perdidas is None
                    or agora - ultima_busca_perdidas >= timedelta(minutes=1)):
                registra_perdidas(conexao, agenda, agora)
                ultima_busca_perdidas = agora

            previsto = cadencia.previsto_para(agenda, agora.date())
            if (previsto is not None and previsto <= agora <= previsto + tolerancia
                    and not registrada(conexao, "disparo", previsto)):
                execucao = reserva(conexao, "disparo", previsto)
                if execucao:
                    conexao = roda_disparo(conexao, agenda, execucao, previsto)

            marco = datetime.fromtimestamp(
                (int(agora.timestamp()) // passo_devolucoes) * passo_devolucoes,
                agenda.fuso)
            if not registrada(conexao, "devolucoes", marco):
                execucao = reserva(conexao, "devolucoes", marco)
                if execucao:
                    conexao = roda_devolucoes(conexao, agenda, execucao)
        except pymysql.Error as e:
            log(agenda, f"banco: {e}; segue no proximo passo")
        time.sleep(PASSO)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except cadencia.ErroAgenda as e:
        print(f"agenda invalida: {e}", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        sys.exit(130)
