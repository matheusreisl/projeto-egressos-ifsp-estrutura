#!/usr/bin/env python3
"""
Confere que a instancia do LimeSurvey entrega pelo correio do ambiente, e que a
regra do parametro P8 se aplica ponta a ponta.

Divisao de trabalho entre os dois verificadores desta etapa:

    scripts/verifica_correio.py   o CORREIO, por SMTP direto, sem o LimeSurvey
                                  no caminho — isola o comportamento do MTA
    infra/confere-envio.py        a INTEGRACAO: o LimeSurvey dispara, a
                                  devolucao volta, a rotina classifica e o
                                  estado do participante muda

Este script roda no hospedeiro, como o confere-capacidades.py, e usa
`docker compose exec` para alcancar o que so existe dentro da rede interna.
A rotina de leitura NAO e reimplementada aqui: chama-se a de verdade, que e o
que se quer verificar.

Monta um questionario de teste descartavel, com tres participantes sinteticos
sob dominio controlado, e remove tudo ao final.

Uso, a partir da pasta infra/:

    python3 confere-envio.py
    python3 confere-envio.py --manter    (deixa o questionario para inspecao)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
VERDE, VERMELHO, AMARELO, FIM = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


class Erro(Exception):
    pass


def carrega_env():
    caminho = os.path.join(AQUI, ".env")
    if not os.path.exists(caminho):
        raise Erro("arquivo .env ausente — copie .env.exemplo e preencha")
    env = {}
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                chave, valor = linha.split("=", 1)
                env[chave.strip()] = valor.strip()
    return env


ENV = carrega_env()
PORTA = ENV.get("PORTA_HTTP", "8080")
API = f"http://127.0.0.1:{PORTA}/index.php/admin/remotecontrol"
DOMINIO = ENV.get("CORREIO_DOMINIO", "egressos.test")
DOMINIO_INVALIDO = ENV.get("CORREIO_DOMINIO_INVALIDO", "invalido.test")
DOMINIO_INDISPONIVEL = ENV.get("CORREIO_DOMINIO_INDISPONIVEL",
                               "indisponivel.test")
CAIXA_ENTREGUES = ENV.get("CORREIO_CAIXA_ENTREGUES", "entregues")
CAIXA_DEVOLUCOES = ENV.get("CORREIO_CAIXA_DEVOLUCOES", "devolucoes")

resultados = []


def registra(rotulo, ok, evidencia):
    resultados.append(ok)
    cor = VERDE if ok else VERMELHO
    print(f"  {cor}[{'ok' if ok else 'FALHA':5}]{FIM} {rotulo}: {evidencia}")


# ---------------------------------------------------------------------------

def rpc(metodo, params, chave=None):
    if chave is not None:
        params = [chave] + params
    corpo = json.dumps({"method": metodo, "params": params, "id": 1}).encode()
    pedido = urllib.request.Request(
        API, data=corpo, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(pedido, timeout=90) as resp:
            dados = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise Erro(f"{metodo}: instancia inacessivel em {API} ({e})")
    if dados.get("error"):
        raise Erro(f"{metodo}: {dados['error']}")
    r = dados.get("result")
    # O campo `status` NAO significa erro por si so: carrega tambem mensagem
    # informativa de sucesso, como "0 left to send" de invite_participants
    # quando todos os convites sairam. O sinal confiavel e `error_code`.
    if isinstance(r, dict) and "status" in r:
        texto = str(r.get("status", "")).strip().upper()
        if r.get("error_code") or texto.startswith(
                ("ERROR", "INVALID", "NO PERMISSION", "NO DATA", "FAILED")):
            raise Erro(f"{metodo}: {r.get('status')} "
                       f"{r.get('error_code', '')}".strip())
    return r


def rpc_tolerante(metodo, params, chave):
    """Como rpc(), mas trata ausencia de dados como lista vazia.

    A API sinaliza "nao ha nada" com erro — "No surveys found",
    "No survey participants found" — e isso nao e falha. Confundir as duas
    coisas faz a conferencia abortar num ambiente recem-criado.
    """
    try:
        r = rpc(metodo, params, chave)
    except Erro as e:
        if "ERR_NO_DATA" in str(e) or "No surveys found" in str(e) \
                or "No survey participants" in str(e):
            return []
        raise
    return r if isinstance(r, list) else []


def no_conteiner(servico, *args, entrada=None):
    p = subprocess.run(["docker", "compose", "exec", "-T", servico, *args],
                       cwd=AQUI, capture_output=True, text=True, input=entrada)
    return p.returncode, p.stdout, p.stderr


def conta_caixa(nome):
    """Quantas mensagens ha na caixa. Precisa correr de dentro da rede interna."""
    codigo, saida, erro = no_conteiner(
        "rotinas", "python3", "-", entrada=f"""
import imaplib, os
imap = imaplib.IMAP4(os.environ['CORREIO_IMAP_HOST'], 143)
imap.login({nome!r}, os.environ['CORREIO_SENHA'])
imap.select('INBOX')
_, d = imap.search(None, 'ALL')
print(len(d[0].split()))
imap.logout()
""")
    if codigo != 0:
        raise Erro(f"leitura da caixa {nome}: {erro.strip()}")
    return int(saida.strip() or 0)


def esvazia_caixas():
    for nome in (CAIXA_ENTREGUES, CAIXA_DEVOLUCOES):
        no_conteiner("rotinas", "python3", "-", entrada=f"""
import imaplib, os
imap = imaplib.IMAP4(os.environ['CORREIO_IMAP_HOST'], 143)
imap.login({nome!r}, os.environ['CORREIO_SENHA'])
imap.select('INBOX')
_, d = imap.search(None, 'ALL')
for mid in d[0].split():
    imap.store(mid, '+FLAGS', '\\\\Deleted')
imap.expunge(); imap.logout()
""")


def aguarda_caixa(nome, quantas, limite_seg, intervalo=10):
    inicio = time.time()
    while True:
        n = conta_caixa(nome)
        if n >= quantas:
            return n, int(time.time() - inicio)
        if time.time() - inicio >= limite_seg:
            return n, int(time.time() - inicio)
        time.sleep(intervalo)


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manter", action="store_true",
                    help="nao remove o questionario de teste ao final")
    args = ap.parse_args()

    print("Conferencia do envio pela instancia — etapa E09\n")

    chave = rpc("get_session_key", [ENV["ADMIN_USUARIO"], ENV["ADMIN_SENHA"]])
    if not isinstance(chave, str):
        raise Erro(f"sessao nao obtida: {chave}")

    questionario = None
    try:
        for s in rpc_tolerante("list_surveys", [], chave):
            if isinstance(s, dict) and s.get("sid"):
                rpc("delete_survey", [int(s["sid"])], chave)

        print("limpando as caixas")
        esvazia_caixas()

        codigo, lss, erro = no_conteiner(
            "limesurvey", "base64", "-w0",
            "docs/demosurveys/ls205_countifop_sumifop.lss")
        if codigo != 0 or not lss.strip():
            raise Erro(f"questionario de exemplo nao lido: {erro.strip()}")
        questionario = rpc("import_survey", [lss.strip(), "lss"], chave)
        rpc("activate_survey", [questionario], chave)
        rpc("activate_tokens", [questionario, [1]], chave)

        enderecos = [
            (f"egresso.valido@{DOMINIO}", "Valido"),
            (f"nao.existe@{DOMINIO_INVALIDO}", "Inexistente"),
            (f"alguem@{DOMINIO_INDISPONIVEL}", "Indisponivel"),
        ]
        rpc("add_participants", [questionario, [
            {"email": e, "firstname": n, "lastname": "Sintetico",
             "attribute_1": "2020-1"} for e, n in enderecos
        ], True], chave)
        print(f"questionario de teste {questionario}, "
              f"{len(enderecos)} participantes sinteticos\n")

        # --- disparo pela propria rotina do LimeSurvey --------------------
        print("DISPARO — pela rotina de convite do LimeSurvey")
        try:
            # Somente o identificador do questionario: os demais parametros
            # ficam nos padroes do metodo. Passar lista VAZIA de tokens nao
            # significa "todos" — o LimeSurvey a traduz num conjunto vazio e
            # responde "No candidate tokens", que parece falha de configuracao
            # e e engano de chamada.
            r = rpc("invite_participants", [questionario], chave)
            print(f"  resposta: {json.dumps(r, ensure_ascii=False)[:300]}")
            registra("a instancia aceitou disparar", True, "sem erro de API")
        except Erro as e:
            registra("a instancia aceitou disparar", False, str(e)[:200])

        # --- direcao 1 ----------------------------------------------------
        print("\nDIRECAO 1 — a mensagem sai da instancia e chega?")
        n, seg = aguarda_caixa(CAIXA_ENTREGUES, 1, 90)
        registra("entrega em dominio controlado", n >= 1,
                 f"{n} mensagem(ns) em {CAIXA_ENTREGUES} apos {seg}s")

        # --- direcao 2 ----------------------------------------------------
        print("\nDIRECAO 2 — a devolucao volta para uma caixa legivel?")
        n, seg = aguarda_caixa(CAIXA_DEVOLUCOES, 1, 120)
        registra("devolucao permanente chega", n >= 1,
                 f"{n} devolucao(oes) em {CAIXA_DEVOLUCOES} apos {seg}s")

        # --- a rotina de verdade, em simulacao ----------------------------
        print("\nCLASSIFICACAO — chamando a rotina de leitura em simulacao")
        codigo, saida, erro = no_conteiner(
            "rotinas", "python3", "ler_devolucoes.py",
            "--ciclo", "conferencia", "--questionario", str(questionario),
            "--simular")
        print("".join(f"    {l}\n" for l in saida.strip().splitlines()))
        if erro.strip():
            print(f"    (erro) {erro.strip()[:300]}")
        registra("a rotina le e classifica", codigo == 0 and "permanente" in saida,
                 "classificou erro permanente" if "permanente" in saida
                 else "nao classificou")

        # --- a rotina de verdade, aplicando ------------------------------
        print("APLICACAO — agora gravando e marcando")
        codigo, saida, erro = no_conteiner(
            "rotinas", "python3", "ler_devolucoes.py",
            "--ciclo", "conferencia", "--questionario", str(questionario))
        print("".join(f"    {l}\n" for l in saida.strip().splitlines()))
        if erro.strip():
            print(f"    (erro) {erro.strip()[:300]}")
        registra("a rotina aplica a regra do P8", codigo == 0,
                 "executou sem erro" if codigo == 0 else "falhou")

        # --- o estado do participante mudou? -----------------------------
        print("\nESTADO — o contato invalido ficou marcado na instancia?")
        marcados = []
        for p in rpc_tolerante("list_participants",
                               [questionario, 0, 100, False,
                                ["email", "emailstatus"]], chave):
            # Estrutura MISTA: `email` vem aninhado sob `participant_info`,
            # `emailstatus` vem no nivel de cima. Ler os dois do mesmo lugar
            # devolve campo vazio sem erro — engano que custou um diagnostico.
            aninhado = p.get("participant_info") or {}
            endereco = str(aninhado.get("email") or p.get("email") or "")
            estado = str(p.get("emailstatus") or "")
            print(f"    {endereco:34} emailstatus={estado or '(vazio)'}")
            if estado.strip().lower() == "invalido":
                marcados.append(endereco)
        registra("marcacao de contato invalido",
                 any(DOMINIO_INVALIDO in (m or "") for m in marcados),
                 f"marcados: {', '.join(m for m in marcados if m) or 'nenhum'}")

        # --- e a recusa NAO foi tocada? ----------------------------------
        # Secao 10.2 do P8: contato invalido nao e recusa. A rotina nao deve
        # ter mexido em blacklisted, que e onde a recusa vive.
        print("\nDISTINCAO — contato invalido nao e recusa (secao 10.2)")
        resumo = rpc("get_summary", [questionario], chave)
        registra("recusa intacta",
                 resumo.get("token_opted_out", 0) == 0,
                 f"token_opted_out={resumo.get('token_opted_out')} "
                 f"(deve ser 0: a rotina nao pode converter falha de cadastro "
                 f"em manifestacao de vontade)")

    finally:
        if questionario is not None and not args.manter:
            try:
                rpc("delete_survey", [questionario], chave)
                print(f"\nquestionario {questionario} removido")
            except Erro as e:
                print(f"\nAVISO: falha ao remover: {e}")
        elif questionario is not None:
            print(f"\nquestionario {questionario} mantido para inspecao")
        try:
            rpc("release_session_key", [], chave)
        except Erro:
            pass

    print(f"\nResultado: {sum(1 for r in resultados if r)} de "
          f"{len(resultados)} conferencias passaram")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Erro as e:
        print(f"\nERRO: {e}", file=sys.stderr)
        sys.exit(2)
