#!/usr/bin/env python3
"""
Confere as capacidades C1 a C10 contra a instancia viva do LimeSurvey.

As dez capacidades estao na secao 13 de docs/especificacao/parametros-contato.md.
O resultado desta conferencia, com o detalhamento, esta em
docs/especificacao/capacidades-plataforma.md.

O que este script faz: cria um questionario de teste a partir do exemplo que
acompanha o LimeSurvey, ativa a tabela de participantes, insere dois
participantes sinteticos sob dominio .test, inspeciona esquema e comportamento,
e remove tudo ao final.

O que NAO faz: nao envia mensagem alguma, nao usa dado de pessoa real e nao
altera configuracao da instancia.

Uso, a partir da pasta infra/:

    python3 confere-capacidades.py

Requer que a composicao esteja de pe e que RPCInterface esteja habilitada no
.env (LIMESURVEY_RPC=json).
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Infraestrutura
# ---------------------------------------------------------------------------

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


def rpc(metodo, params, chave=None):
    """Chamada JSON-RPC a API RemoteControl."""
    if chave is not None:
        params = [chave] + params
    corpo = json.dumps({"method": metodo, "params": params, "id": 1}).encode()
    req = urllib.request.Request(
        API, data=corpo, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            dados = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise Erro(f"{metodo}: instancia inacessivel em {API} ({e})")
    if dados.get("error"):
        raise Erro(f"{metodo}: {dados['error']}")
    r = dados.get("result")
    # A API sinaliza sucesso com {"status": "OK"} e falha com {"status": ...},
    # as vezes com "error_code" junto. Nao condicionar ao numero de chaves.
    if isinstance(r, dict) and "status" in r:
        if str(r["status"]).upper() not in ("OK", "SUCCESS"):
            raise Erro(f"{metodo}: {r.get('status')} {r.get('error_code', '')}".strip())
    return r


def sql(consulta):
    """Consulta direta ao banco, para inspecionar esquema."""
    p = subprocess.run(
        ["docker", "compose", "exec", "-T", "banco", "mariadb",
         f"-u{ENV['BANCO_USUARIO']}", f"-p{ENV['BANCO_SENHA']}",
         f"-D{ENV['BANCO_NOME']}", "-N", "-B", "-e", consulta],
        cwd=AQUI, capture_output=True, text=True)
    if p.returncode != 0:
        raise Erro(f"sql: {p.stderr.strip()}")
    return [l.split("\t") for l in p.stdout.strip().split("\n") if l]


def no_conteiner(*args):
    p = subprocess.run(
        ["docker", "compose", "exec", "-T", "limesurvey", *args],
        cwd=AQUI, capture_output=True, text=True)
    return p.stdout


VERDE, VERMELHO, AMARELO, FIM = "\033[32m", "\033[31m", "\033[33m", "\033[0m"
resultados = []


def registra(cid, descricao, veredito, evidencia):
    resultados.append((cid, descricao, veredito))
    cor = {"atende": VERDE, "parcial": AMARELO, "nao": VERMELHO}[veredito]
    print(f"  {cor}[{veredito.upper():7}]{FIM} {cid}  {evidencia}")


# ---------------------------------------------------------------------------

def main():
    print("Conferencia das capacidades C1 a C10 — LimeSurvey\n")

    chave = rpc("get_session_key", [ENV["ADMIN_USUARIO"], ENV["ADMIN_SENHA"]])
    if not isinstance(chave, str):
        raise Erro(f"sessao nao obtida: {chave}")

    sid = None
    try:
        # --- montagem do cenario de teste --------------------------------
        lss = no_conteiner("base64", "-w0",
                           "docs/demosurveys/ls205_sample_survey_english.lss").strip()
        if not lss:
            raise Erro("questionario de exemplo nao encontrado na instancia")
        sid = rpc("import_survey", [lss, "lss"], chave)
        rpc("activate_survey", [sid], chave)
        rpc("activate_tokens", [sid, [1, 2]], chave)
        criados = rpc("add_participants", [sid, [
            {"email": "egresso.um@egressos.test", "lastname": "Sintetico",
             "firstname": "Um", "attribute_1": "2018-1", "attribute_2": "ADS"},
            {"email": "egresso.dois@egressos.test", "lastname": "Sintetico",
             "firstname": "Dois", "attribute_1": "2020-2", "attribute_2": "ADS"},
        ], True], chave)
        tokens = [c["token"] for c in criados]

        TOK = f"lime_tokens_{sid}"
        # Atencao: no LimeSurvey 7 a tabela de respostas e lime_responses_<sid>,
        # e nao lime_survey_<sid>, que e o nome usado pela documentacao antiga.
        RESP = f"lime_responses_{sid}"
        colunas = {c[0]: c[1] for c in sql(f"SHOW COLUMNS FROM {TOK};")}
        resp_cols = {c[0]: c[1] for c in sql(f"SHOW COLUMNS FROM {RESP};")}

        print(f"cenario de teste: sid={sid}, {len(tokens)} participantes sinteticos\n")

        # --- C1 -----------------------------------------------------------
        unicos = len(set(tokens)) == len(tokens)
        comprimento = len(tokens[0])
        indice = bool(sql(f"SHOW INDEX FROM {TOK} WHERE Column_name='token';"))
        url = f"http://127.0.0.1:{PORTA}/index.php/{sid}?token={tokens[0]}"
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                alcancavel = r.status == 200
        except Exception:
            alcancavel = False
        registra("C1", "endereco individual",
                 "atende" if (unicos and comprimento >= 15 and indice and alcancavel)
                 else "parcial",
                 f"token {colunas.get('token')}, {comprimento} caracteres, "
                 f"unicos={unicos}, indexado={indice}, responde={alcancavel}")

        # --- C2 -----------------------------------------------------------
        registra("C2", "estado de conclusao",
                 "atende" if "completed" in colunas else "nao",
                 f"coluna completed={colunas.get('completed', 'AUSENTE')}, "
                 f"contador token_completed no get_summary")

        # --- C3 -----------------------------------------------------------
        sql(f"INSERT INTO {RESP} (token, startdate, datestamp, lastpage, startlanguage) "
            f"VALUES ('{tokens[0]}', '2026-01-01 10:00:00', "
            f"'2026-01-01 10:00:00', 2, 'en');")
        s = rpc("get_summary", [sid], chave)
        ok3 = (s.get("incomplete_responses") == 1 and s.get("completed_responses") == 0)
        registra("C3", "iniciado vs nao iniciado",
                 "atende" if ok3 else "parcial",
                 f"submitdate nulo + startdate preenchido -> "
                 f"incompletas={s.get('incomplete_responses')}, "
                 f"completas={s.get('completed_responses')}")

        # --- C4 -----------------------------------------------------------
        tem = [c for c in ("sent", "remindersent", "remindercount") if c in colunas]
        registra("C4", "contagem e data de disparo",
                 "atende" if len(tem) == 3 else "parcial",
                 f"colunas: {', '.join(tem) or 'nenhuma'}")

        # --- C5 -----------------------------------------------------------
        fonte = no_conteiner(
            "grep", "-c", "-E",
            "public function (invite_participants|remind_participants)",
            "application/helpers/remotecontrol/remotecontrol_handle.php").strip()
        registra("C5", "disparo seletivo por rotina",
                 "atende" if fonte == "2" else "parcial",
                 f"metodos de API invite_participants e remind_participants: "
                 f"{fonte} de 2")

        # --- C6 -----------------------------------------------------------
        cpdb = {c[0] for c in sql("SHOW COLUMNS FROM lime_participants;")}
        sql(f"UPDATE {TOK} SET emailstatus='OptOut' WHERE token='{tokens[1]}';")
        s6 = rpc("get_summary", [sid], chave)
        registra("C6", "recusa persistente entre ciclos", "parcial",
                 f"token.blacklisted existe (morre com o ciclo); "
                 f"participants.blacklisted="
                 f"{'existe' if 'blacklisted' in cpdb else 'AUSENTE'} (persistente); "
                 f"o contador opted_out responde a emailStatus='OptOut', nao a "
                 f"blacklisted (opted_out={s6.get('token_opted_out')})")

        # --- C7 -----------------------------------------------------------
        tem = [c for c in ("validfrom", "validuntil") if c in colunas]
        registra("C7", "validade temporal do acesso",
                 "atende" if len(tem) == 2 else "parcial",
                 f"colunas: {', '.join(tem) or 'nenhuma'}")

        # --- C8 -----------------------------------------------------------
        falhas = {c[0] for c in sql("SHOW COLUMNS FROM lime_failed_emails;")}
        registra("C8", "estado de entrega", "parcial",
                 f"emailstatus no token e lime_failed_emails "
                 f"({len(falhas)} colunas); a LEITURA da devolucao e rotina "
                 f"propria, por decisao da ADR-0004")

        # --- C9 -----------------------------------------------------------
        attrs = sorted(c for c in colunas if c.startswith("attribute_"))
        registra("C9", "atributos por participante",
                 "atende" if attrs else "nao",
                 f"criados sob demanda: {', '.join(attrs) or 'nenhum'}")

        # --- C10 ----------------------------------------------------------
        plugin = sql("SELECT name, active FROM lime_plugins WHERE name='AuditLog';")
        tabelas = sql("SHOW TABLES LIKE '%audit%';")
        registra("C10", "trilha de auditoria",
                 "parcial" if plugin else "nao",
                 f"plugin AuditLog {'presente' if plugin else 'ausente'}, "
                 f"ativo={plugin[0][1] if plugin else '-'}; tabelas de auditoria: "
                 f"{len(tabelas)}. Ativacao nao e alcancavel por console — ver E23")

    finally:
        if sid is not None:
            try:
                rpc("delete_survey", [sid], chave)
                sobra = [t[0] for t in sql("SHOW TABLES;") if str(sid) in t[0]]
                print(f"\ncenario removido; tabelas remanescentes: {sobra or 'nenhuma'}")
            except Erro as e:
                print(f"\nAVISO: falha ao remover o cenario de teste: {e}")
        rpc("release_session_key", [], chave)

    # -----------------------------------------------------------------------
    atende = sum(1 for _, _, v in resultados if v == "atende")
    parcial = sum(1 for _, _, v in resultados if v == "parcial")
    nao = sum(1 for _, _, v in resultados if v == "nao")
    print(f"\nResultado: {atende} atendem, {parcial} parciais, {nao} nao atendem")
    print("Detalhamento em docs/especificacao/capacidades-plataforma.md")
    return 1 if nao else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Erro as e:
        print(f"\nERRO: {e}", file=sys.stderr)
        sys.exit(2)
