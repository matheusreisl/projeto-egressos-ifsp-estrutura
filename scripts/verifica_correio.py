#!/usr/bin/env python3
"""
Verifica o servico de correio nas DUAS direcoes — envio e devolucao.

A secao 10.4 de docs/especificacao/parametros-contato.md e explicita sobre por
que isto existe: uma configuracao que envia corretamente e nao permite ler
devolucoes satisfaz "vi a mensagem chegar" e ainda assim inviabiliza o parametro
P8. Capturadores de SMTP de uso corrente em desenvolvimento aceitam tudo e nunca
devolvem erro. Este script recusa esse atalho.

Exercita as tres linhas da tabela de classificacao da secao 10.1, uma por
dominio:

    <DOMINIO>               entrega normal          -> chega na caixa coletora
    <DOMINIO_INVALIDO>      usuario inexistente     -> devolucao PERMANENTE
    <DOMINIO_INDISPONIVEL>  servidor inalcancavel   -> devolucao TEMPORARIA

Depois passa cada devolucao pela mesma funcao de interpretacao que a rotina
ler_devolucoes.py usa, para conferir que a classificacao sai como o P8 espera.

Este script verifica o CORREIO, sem o LimeSurvey no caminho. A verificacao de
que a instancia entrega por esse correio esta em infra/confere-envio.py.

Nao usa dado de pessoa real e nao alcanca endereco real: o servico de correio
fica somente na rede interna, que nao tem rota de saida.

Uso:

    docker compose exec rotinas python3 verifica_correio.py
"""

import email
import email.policy
import imaplib
import os
import smtplib
import sys
import time
from email.message import EmailMessage

from ler_devolucoes import interpreta

DOMINIO = os.environ.get("CORREIO_DOMINIO", "egressos.test")
DOMINIO_INVALIDO = os.environ.get("CORREIO_DOMINIO_INVALIDO", "invalido.test")
DOMINIO_INDISPONIVEL = os.environ.get("CORREIO_DOMINIO_INDISPONIVEL",
                                      "indisponivel.test")
SMTP_HOST = os.environ.get("CORREIO_SMTP_HOST", "correio")
SMTP_PORTA = int(os.environ.get("CORREIO_SMTP_PORTA", "25"))
IMAP_HOST = os.environ.get("CORREIO_IMAP_HOST", "correio")
IMAP_PORTA = int(os.environ.get("CORREIO_IMAP_PORTA", "143"))
CAIXA_DEVOLUCOES = os.environ.get("CORREIO_CAIXA_DEVOLUCOES", "devolucoes")
CAIXA_ENTREGUES = os.environ.get("CORREIO_CAIXA_ENTREGUES", "entregues")
SENHA = os.environ.get("CORREIO_SENHA")

REMETENTE = f"{CAIXA_DEVOLUCOES}@{DOMINIO}"

VERDE, VERMELHO, FIM = "\033[32m", "\033[31m", "\033[0m"
resultados = []


def registra(rotulo, ok, evidencia):
    resultados.append(ok)
    cor = VERDE if ok else VERMELHO
    print(f"  {cor}[{'ok' if ok else 'FALHA':5}]{FIM} {rotulo}: {evidencia}")


# ---------------------------------------------------------------------------

def conecta_imap(nome, tentativas=8, espera=8):
    """Conecta ao IMAP, com retentativa.

    A retentativa nao e zelo excessivo. Num hospedeiro WSL o servico de correio
    pode se reiniciar no meio de uma espera longa, porque o relogio da maquina
    virtual salta quando a distribuicao suspende e retoma — ver a secao 6 de
    docs/especificacao/leitura-devolucoes.md. Sem retentativa, a verificacao
    aborta por uma falha do ambiente e nao por uma falha do mecanismo, que e
    justamente o que ela deveria distinguir.
    """
    ultimo = None
    for n in range(1, tentativas + 1):
        try:
            imap = imaplib.IMAP4(IMAP_HOST, IMAP_PORTA)
            imap.login(nome, SENHA)
            imap.select("INBOX")
            return imap
        except (imaplib.IMAP4.error, imaplib.IMAP4.abort, OSError) as e:
            ultimo = e
            if n < tentativas:
                print(f"    (IMAP indisponivel, tentativa {n}: "
                      f"{type(e).__name__}; aguardando {espera}s)", flush=True)
                time.sleep(espera)
    raise RuntimeError(f"IMAP inacessivel apos {tentativas} tentativas: {ultimo}")


def mensagens(nome):
    imap = conecta_imap(nome)
    try:
        _, dados = imap.search(None, "ALL")
        brutas = []
        for mid in dados[0].split():
            _, conteudo = imap.fetch(mid, "(BODY.PEEK[])")
            brutas.append(conteudo[0][1])
        return brutas
    finally:
        try:
            imap.logout()
        except Exception:
            pass


def esvazia(nome):
    imap = conecta_imap(nome)
    try:
        _, dados = imap.search(None, "ALL")
        for mid in dados[0].split():
            imap.store(mid, "+FLAGS", "\\Deleted")
        imap.expunge()
    finally:
        try:
            imap.logout()
        except Exception:
            pass


def envia(destino, assunto):
    msg = EmailMessage()
    msg["From"] = REMETENTE
    msg["To"] = destino
    msg["Subject"] = assunto
    msg.set_content(
        "Mensagem de verificacao do ambiente de ensaio.\n"
        "Base sintetica, dominio controlado, sem destinatario real.\n")
    with smtplib.SMTP(SMTP_HOST, SMTP_PORTA, timeout=30) as s:
        s.send_message(msg)


def aguarda(nome, quantas, limite_seg, intervalo=5):
    inicio = time.time()
    ultimas = []
    while True:
        try:
            ultimas = mensagens(nome)
            if len(ultimas) >= quantas:
                return ultimas, int(time.time() - inicio)
        except RuntimeError as e:
            # O ambiente pode oscilar durante uma espera longa. Isso nao encerra
            # a espera: encerra-la aqui confundiria falha do hospedeiro com
            # falha do mecanismo.
            print(f"    (aviso: {e})", flush=True)
        if time.time() - inicio >= limite_seg:
            return ultimas, int(time.time() - inicio)
        time.sleep(intervalo)


def assunto_de(bruta):
    return str(email.message_from_bytes(
        bruta, policy=email.policy.default).get("Subject", ""))


# ---------------------------------------------------------------------------

def main():
    if not SENHA:
        raise SystemExit("CORREIO_SENHA nao definida no ambiente")
    # Esvazia as caixas, logo abaixo. Com a rotina em modo real, elas sao a
    # evidencia da simulacao (E26): convites entregues e devolucoes por ler.
    if os.environ.get("ROTINA_DISPARO") == "real":
        raise SystemExit("recusado: a rotina esta em modo real, e esvaziar as "
                         "caixas apagaria a evidencia da simulacao")

    print("Verificacao do correio nas duas direcoes — etapa E09\n")
    print(f"  entrega      : {DOMINIO}")
    print(f"  invalido     : {DOMINIO_INVALIDO}")
    print(f"  indisponivel : {DOMINIO_INDISPONIVEL}\n")

    print("limpando as caixas")
    for c in (CAIXA_ENTREGUES, CAIXA_DEVOLUCOES):
        esvazia(c)

    marca = str(int(time.time()))

    # --- direcao 1 --------------------------------------------------------
    print("\nDIRECAO 1 — a mensagem chega ao destino?")
    envia(f"egresso.valido@{DOMINIO}", f"convite {marca}")
    entregues, seg = aguarda(CAIXA_ENTREGUES, 1, 60)
    registra("entrega em dominio controlado", len(entregues) >= 1,
             f"{len(entregues)} mensagem(ns) em {CAIXA_ENTREGUES} apos {seg}s"
             + (f", assunto={assunto_de(entregues[0])!r}" if entregues else ""))

    # --- direcao 2 --------------------------------------------------------
    print("\nDIRECAO 2 — a devolucao volta e e legivel?")
    envia(f"nao.existe@{DOMINIO_INVALIDO}", f"permanente {marca}")
    devolucoes, seg = aguarda(CAIXA_DEVOLUCOES, 1, 90)
    registra("devolucao permanente chega", len(devolucoes) >= 1,
             f"{len(devolucoes)} devolucao(oes) em {CAIXA_DEVOLUCOES} "
             f"apos {seg}s")

    # --- direcao 2b -------------------------------------------------------
    # O aviso de atraso sai apos delay_warning_time, fixado em 1 min no servico
    # de correio para caber em tempo de ensaio.
    print("\nDIRECAO 2b — e a devolucao TEMPORARIA?")
    envia(f"alguem@{DOMINIO_INDISPONIVEL}", f"temporaria {marca}")
    print("  aguardando o aviso de atraso, que nao e imediato...")
    devolucoes, seg = aguarda(CAIXA_DEVOLUCOES, 2, 240, intervalo=10)
    registra("devolucao temporaria chega", len(devolucoes) >= 2,
             f"{len(devolucoes)} devolucao(oes) apos {seg}s")

    # --- classificacao ----------------------------------------------------
    print("\nCLASSIFICACAO — o que a rotina de leitura entende de cada uma")
    interpretadas = []
    for bruta in devolucoes:
        interpretadas.extend(interpreta(bruta))
    for d in interpretadas:
        print(f"    {d.tipo:14} {d.destinatario:32} "
              f"status={d.status or '-':8} acao={d.acao or '-'}")

    tipos = {d.tipo for d in interpretadas}
    registra("classifica erro permanente", "permanente" in tipos,
             "identificado" if "permanente" in tipos else "NAO identificado")
    registra("classifica erro temporario", "temporario" in tipos,
             "identificado" if "temporario" in tipos else "NAO identificado")

    destinos = {d.destinatario for d in interpretadas}
    registra("recupera o destinatario original",
             any(DOMINIO_INVALIDO in x for x in destinos),
             f"enderecos recuperados: {', '.join(sorted(destinos)) or 'nenhum'}")

    # --- contencao --------------------------------------------------------
    print("\nCONTENCAO — o correio realmente nao alcanca a internet?")
    import socket
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=5).close()
        registra("rede fechada", False, "ALCANCOU a internet")
    except OSError:
        registra("rede fechada", True,
                 "sem rota de saida a partir da rede interna")

    print(f"\nResultado: {sum(resultados)} de {len(resultados)} "
          f"conferencias passaram")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
