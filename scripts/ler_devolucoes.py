#!/usr/bin/env python3
"""
Le a caixa de devolucoes, classifica cada retorno e aplica a regra do parametro
P8 de docs/especificacao/parametros-contato.md.

Por que esta rotina existe, e nao o recurso nativo do LimeSurvey: a extensao
`imap` do PHP, de que o rastreamento nativo depende, nao se constroi mais sobre
a base atual — decisao e justificativa na ADR-0004. O argumento que sustenta a
escolha e que as regras de classificacao do P8 sao do projeto e o recurso nativo
nao as implementa: a logica teria de ser escrita de qualquer modo.

A regra que esta rotina aplica, conforme a secao 10.1 do P8:

    erro permanente   marca o contato como invalido na PRIMEIRA ocorrencia
    erro temporario   nao marca; marca so na TERCEIRA ocorrencia do mesmo ciclo
    sem retorno       nada a fazer — nao chega devolucao

E a distincao da secao 10.2, que esta rotina respeita e que e facil de errar:
**contato invalido nao e recusa.** Interrompe o disparo do ciclo corrente e abre
fila de correcao, mas nao bloqueia ciclos futuros. Por isso a rotina grava o
estado de entrega no participante do ciclo corrente e NAO toca na marcacao
persistente da base central, que e onde vive a recusa. Confundir as duas
converteria falha de cadastro em manifestacao de vontade que ninguem expressou.

Divisao de responsabilidade entre as duas fontes que esta rotina usa:

    API do LimeSurvey   estado do participante — ler e marcar
    tabela propria      registro das devolucoes e contagem por ciclo

A contagem precisa de tabela propria porque o limiar de tres ocorrencias e
decisao deste projeto e o LimeSurvey nao tem onde guardar isso. A tabela e
tambem o registro que o P8 exige, e alimenta a trilha de auditoria da E23.

Uso:

    python3 ler_devolucoes.py --ciclo 2026-1 --questionario 123456
    python3 ler_devolucoes.py --ciclo 2026-1 --questionario 123456 --simular

`--simular` le e classifica sem gravar nem marcar, e sem consumir a caixa.
"""

import argparse
import email
import email.policy
import imaplib
import os
import re
import sys
from datetime import datetime

import pymysql

from limesurvey_api import API, ErroAPI

# ---------------------------------------------------------------------------
# Configuracao, toda por ambiente
# ---------------------------------------------------------------------------

IMAP_HOST = os.environ.get("CORREIO_IMAP_HOST", "correio")
IMAP_PORTA = int(os.environ.get("CORREIO_IMAP_PORTA", "143"))
CAIXA = os.environ.get("CORREIO_CAIXA_DEVOLUCOES", "devolucoes")
SENHA_CAIXA = os.environ.get("CORREIO_SENHA")

BANCO = {
    "host": os.environ.get("BANCO_HOST", "banco"),
    "port": int(os.environ.get("BANCO_PORTA", "3306")),
    "user": os.environ.get("BANCO_USUARIO"),
    "password": os.environ.get("BANCO_SENHA"),
    "database": os.environ.get("BANCO_NOME"),
    "charset": "utf8mb4",
    "autocommit": False,
}

TABELA = "egressos_devolucoes"

# Secao 10.1 do P8. Decisao de projeto, sem fonte: justifica-se por simetria com
# o P2 — se a cadencia preve quatro mensagens, exigir as tres primeiras antes de
# declarar o contato perdido consome a sequencia sem desperdicar.
LIMIAR_TEMPORARIO = 3

ESTADO_INVALIDO = "invalido"


# ---------------------------------------------------------------------------
# Classificacao
# ---------------------------------------------------------------------------

class Devolucao:
    """Um retorno lido da caixa, ja interpretado."""

    def __init__(self, destinatario, acao, status, diagnostico, mensagem_id):
        self.destinatario = (destinatario or "").strip().lower().strip("<>")
        self.acao = (acao or "").strip().lower()
        self.status = (status or "").strip()
        self.diagnostico = (diagnostico or "").strip()
        self.mensagem_id = (mensagem_id or "").strip()

    @property
    def tipo(self):
        """Classifica conforme a secao 10.1 do P8.

        A classe do codigo de estado manda, porque e o dado normalizado da
        RFC 3463: 5.x.x e permanente, 4.x.x e temporario. A acao declarada
        entra como desempate quando nao ha codigo.
        """
        if self.status:
            classe = self.status.split(".", 1)[0]
            if classe == "5":
                return "permanente"
            if classe == "4":
                return "temporario"
        if self.acao == "failed":
            return "permanente"
        if self.acao == "delayed":
            return "temporario"
        return "indeterminado"

    def __repr__(self):
        return (f"<{self.tipo} {self.destinatario} "
                f"status={self.status or '-'} acao={self.acao or '-'}>")


def interpreta(bruto):
    """Extrai de uma mensagem de devolucao os campos que interessam.

    Trata o formato normalizado da RFC 3464 — multipart/report com uma parte
    message/delivery-status — e recorre a leitura do texto quando a devolucao
    nao vem normalizada, o que acontece com servidores que devolvem em prosa.
    """
    msg = email.message_from_bytes(bruto, policy=email.policy.default)
    mensagem_id = msg.get("Message-ID", "")
    achados = []

    # --- caminho normalizado ---------------------------------------------
    for parte in msg.walk():
        if parte.get_content_type() != "message/delivery-status":
            continue
        texto = parte.get_payload(decode=True)
        if texto is None:
            # Alguns geradores aninham as secoes como submensagens.
            texto = "\n\n".join(
                str(s) for s in parte.get_payload()).encode()
        # A primeira secao e do servidor; as seguintes, uma por destinatario.
        for bloco in re.split(rb"\n\s*\n", texto):
            campos = {}
            for linha in bloco.decode("utf-8", "replace").splitlines():
                if ":" in linha:
                    chave, _, valor = linha.partition(":")
                    campos[chave.strip().lower()] = valor.strip()
            destino = (campos.get("final-recipient")
                       or campos.get("original-recipient"))
            if not destino:
                continue
            # "rfc822; alguem@dominio" -> "alguem@dominio"
            if ";" in destino:
                destino = destino.split(";", 1)[1]
            achados.append(Devolucao(
                destinatario=destino,
                acao=campos.get("action", ""),
                status=campos.get("status", ""),
                diagnostico=campos.get("diagnostic-code", ""),
                mensagem_id=mensagem_id,
            ))

    if achados:
        return achados

    # --- devolucao nao normalizada ---------------------------------------
    corpo = ""
    for parte in msg.walk():
        if parte.get_content_type() == "text/plain":
            carga = parte.get_payload(decode=True)
            if carga:
                corpo += carga.decode("utf-8", "replace")
    endereco = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", corpo)
    codigo = re.search(r"\b([45]\.\d{1,3}\.\d{1,3})\b", corpo)
    if endereco:
        achados.append(Devolucao(
            destinatario=endereco.group(0),
            acao="failed" if re.search(r"\b5\d\d\b", corpo) else "",
            status=codigo.group(1) if codigo else "",
            diagnostico=corpo[:500],
            mensagem_id=mensagem_id,
        ))
    return achados


# ---------------------------------------------------------------------------
# Caixa
# ---------------------------------------------------------------------------

def coleta(marcar_lidas):
    """Baixa as devolucoes ainda nao lidas. Devolve (devolucoes, n_mensagens)."""
    if not SENHA_CAIXA:
        raise SystemExit("CORREIO_SENHA nao definida no ambiente")
    imap = imaplib.IMAP4(IMAP_HOST, IMAP_PORTA)
    try:
        imap.login(CAIXA, SENHA_CAIXA)
        imap.select("INBOX")
        _, dados = imap.search(None, "UNSEEN")
        ids = dados[0].split()
        colhidas = []
        for mid in ids:
            # PEEK nao marca como lida. Quem decide isso e o chamador, para que
            # --simular possa ler sem consumir a caixa.
            _, conteudo = imap.fetch(mid, "(BODY.PEEK[])")
            colhidas.extend(interpreta(conteudo[0][1]))
            if marcar_lidas:
                imap.store(mid, "+FLAGS", "\\Seen")
        return colhidas, len(ids)
    finally:
        try:
            imap.logout()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Registro proprio
# ---------------------------------------------------------------------------

DDL = f"""
CREATE TABLE IF NOT EXISTS {TABELA} (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  lido_em       DATETIME     NOT NULL,
  ciclo         VARCHAR(20)  NOT NULL,
  questionario  INT          NOT NULL,
  token         VARCHAR(36)  NULL,
  destinatario  VARCHAR(254) NOT NULL,
  tipo          VARCHAR(15)  NOT NULL,
  codigo_status VARCHAR(15)  NULL,
  acao          VARCHAR(20)  NULL,
  diagnostico   TEXT         NULL,
  mensagem_id   VARCHAR(255) NULL,
  marcou        TINYINT(1)   NOT NULL DEFAULT 0,
  UNIQUE KEY unico_por_mensagem (mensagem_id, destinatario),
  KEY por_destinatario (destinatario),
  KEY por_ciclo (ciclo, questionario)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
"""


def conta_temporarias(cur, destinatario, ciclo, questionario):
    cur.execute(
        f"""SELECT COUNT(*) FROM {TABELA}
            WHERE destinatario=%s AND ciclo=%s AND questionario=%s
              AND tipo='temporario'""",
        (destinatario, ciclo, questionario))
    return cur.fetchone()[0]


# ---------------------------------------------------------------------------

def executa(devolucoes, ciclo, questionario, simular):
    resumo = {"permanentes": 0, "temporarias": 0, "indeterminadas": 0,
              "repetidas": 0, "marcados": [], "sem_participante": []}

    with API() as api:
        # Mapa endereco -> participante, numa consulta so.
        # api.participantes() ja devolve os registros achatados.
        por_endereco = {}
        for p in api.participantes(questionario):
            endereco = str(p.get("email", "")).strip().lower()
            if endereco:
                por_endereco[endereco] = {"tid": p.get("tid"),
                                          "token": p.get("token")}

        conexao = pymysql.connect(**BANCO)
        try:
            with conexao.cursor() as cur:
                if not simular:
                    cur.execute(DDL)

                for d in devolucoes:
                    resumo[{"permanente": "permanentes",
                            "temporario": "temporarias",
                            "indeterminado": "indeterminadas"}[d.tipo]] += 1

                    alvo = por_endereco.get(d.destinatario)
                    if alvo is None:
                        resumo["sem_participante"].append(d.destinatario)

                    if simular:
                        continue

                    try:
                        cur.execute(
                            f"""INSERT INTO {TABELA}
                                (lido_em, ciclo, questionario, token,
                                 destinatario, tipo, codigo_status, acao,
                                 diagnostico, mensagem_id)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (datetime.now(), ciclo, questionario,
                             alvo["token"] if alvo else None, d.destinatario,
                             d.tipo, d.status or None, d.acao or None,
                             d.diagnostico or None, d.mensagem_id or None))
                        id_inserido = cur.lastrowid
                    except pymysql.err.IntegrityError:
                        # A mesma devolucao lida duas vezes nao conta duas.
                        resumo["repetidas"] += 1
                        continue

                    if alvo is None:
                        continue

                    # --- a regra do P8 ---------------------------------------
                    if d.tipo == "permanente":
                        marcar = True
                    elif d.tipo == "temporario":
                        marcar = conta_temporarias(
                            cur, d.destinatario, ciclo,
                            questionario) >= LIMIAR_TEMPORARIO
                    else:
                        marcar = False

                    if marcar:
                        api.marcar_estado_de_entrega(
                            questionario, alvo["tid"], ESTADO_INVALIDO)
                        cur.execute(
                            f"UPDATE {TABELA} SET marcou=1 WHERE id=%s",
                            (id_inserido,))
                        resumo["marcados"].append((d.destinatario, d.tipo))

            if not simular:
                conexao.commit()
        finally:
            conexao.close()

        # A fila de correcao nao e estrutura nova: e uma consulta. Sao os
        # participantes cujo contato esta marcado como invalido.
        fila = []
        for p in api.participantes(questionario):
            if str(p.get("emailstatus", "")).strip().lower() == ESTADO_INVALIDO:
                fila.append(str(p.get("email", "")))
        resumo["fila"] = fila

    return resumo


def main():
    ap = argparse.ArgumentParser(
        description="Le e classifica devolucoes conforme o parametro P8.")
    ap.add_argument("--ciclo", required=True,
                    help="identificador do ciclo, por exemplo 2026-1")
    ap.add_argument("--questionario", required=True, type=int,
                    help="identificador do questionario no LimeSurvey")
    ap.add_argument("--simular", action="store_true",
                    help="le e classifica sem gravar, marcar nem consumir a caixa")
    args = ap.parse_args()

    print(f"caixa {CAIXA}@{IMAP_HOST}:{IMAP_PORTA} · ciclo {args.ciclo} · "
          f"questionario {args.questionario}"
          f"{' · SIMULACAO' if args.simular else ''}")

    devolucoes, quantas = coleta(marcar_lidas=not args.simular)
    print(f"mensagens nao lidas: {quantas}; "
          f"destinatarios devolvidos: {len(devolucoes)}")
    for d in devolucoes:
        print(f"  {d.tipo:14} {d.destinatario:34} "
              f"status={d.status or '-':8} acao={d.acao or '-'}")

    if not devolucoes:
        print("nada a aplicar")
        return 0

    resumo = executa(devolucoes, args.ciclo, args.questionario, args.simular)

    print(f"\npermanentes={resumo['permanentes']} "
          f"temporarias={resumo['temporarias']} "
          f"indeterminadas={resumo['indeterminadas']} "
          f"repetidas={resumo['repetidas']}")
    if resumo["sem_participante"]:
        print("sem participante correspondente no ciclo: "
              + ", ".join(resumo["sem_participante"]))
    if resumo["marcados"]:
        print("marcados como contato invalido:")
        for endereco, tipo in resumo["marcados"]:
            print(f"  {endereco}  (por erro {tipo})")
    elif not args.simular:
        print("nenhum contato marcado nesta passada")
    if not args.simular:
        print(f"\nfila de correcao: {len(resumo.get('fila', []))} participante(s)")
        for endereco in resumo.get("fila", []):
            print(f"  {endereco}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ErroAPI, pymysql.Error) as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
