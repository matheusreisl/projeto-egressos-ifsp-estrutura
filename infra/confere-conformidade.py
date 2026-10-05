#!/usr/bin/env python3
"""
Confere a conformidade (E23) contra o criterio da etapa: a recusa de CONTATO
interrompe novos disparos em todos os ciclos, e a de CONSENTIMENTO, so no ciclo
corrente.

Sem --exercitar, so le:

  1. a trilha de auditoria ativa, a lista de bloqueio nos padroes exigidos e a
     correcao do AuditLog na imagem (infra/conformidade.py aplicar);
  2. a pagina de confirmacao da recusa em portugues.

Com --exercitar, oito participantes sinteticos do instrumento, e desfaz tudo:

  3. a cifragem em repouso: a resposta gravada no banco nao e o valor, e a
     exportacao da plataforma devolve o valor;
  4. a rotina de conformidade registra as tres vias de recusa de contato — tela,
     conclusao (CT4) e mensagem — e a de consentimento, com momento e versao do
     termo; e nao registra o contato invalido, que nao e recusa;
  5. leva a recusa de contato a base central pela via da plataforma, e a
     trilha registra; a de consentimento e o contato invalido ficam fora;
  6. o CICLO SEGUINTE — um questionario novo com as mesmas pessoas: a
     plataforma recusa convidar quem recusou contato, por qualquer via, e
     convida quem recusou o consentimento e quem tinha contato invalido;
  7. no ciclo corrente, a recusa de consentimento interrompe a cadencia;
  8. o dado sensivel guardado sem consentimento e apagado, e o guardado com
     consentimento fica;
  9. a rotina e idempotente;
 10. a revogacao pelo operador tira o bloqueio, fica registrada, e a rotina nao
     volta a bloquear;
 11. tudo recuperavel por consulta-consentimento.py;
 12. limpeza.

Nada sai da maquina: o correio fica so na rede interna, e os enderecos estao sob
.test. Nenhum dado e de pessoa real.

Uso, a partir da pasta infra/:

    python3 confere-conformidade.py               (so leitura)
    python3 confere-conformidade.py --exercitar   (caminho real, e desfaz)
"""

import argparse
import base64
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))
sys.path.insert(0, os.path.join(AQUI, "instrumento"))

import cadencia  # noqa: E402
import termo  # noqa: E402
from limesurvey_api import ErroAPI  # noqa: E402
from limesurvey_console import api_do_hospedeiro, carrega_env  # noqa: E402


def _carrega(nome, arquivo):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(AQUI, arquivo))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


cm = _carrega("confere_mensagens", "confere-mensagens.py")          # banco, caixa
cc = _carrega("consulta_consentimento", "consulta-consentimento.py")
ccs = _carrega("confere_consentimento", "confere-consentimento.py")  # respondente

SID = 202615
ENV = carrega_env()
PORTA = ENV.get("PORTA_HTTP", "8080")
DOMINIO = ENV.get("CORREIO_DOMINIO", "egressos.test")
AGENDA = cadencia.carrega_agenda(
    os.path.join(AQUI, "rotinas", "configuracao", "agenda.json"))
VERDE, VERMELHO, FIM = "\033[32m", "\033[31m", "\033[0m"

resultados = []


def registra(rotulo, falhas, evidencia=""):
    ok = not falhas
    resultados.append(ok)
    cor = VERDE if ok else VERMELHO
    print(f"  {cor}[{'ok' if ok else 'FALHA':5}]{FIM} {len(resultados)}. "
          f"{rotulo}" + (f": {evidencia}" if ok and evidencia else ""))
    for f in falhas:
        print(f"           - {f}")


def texto_visivel(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(
        r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)))


# ===========================================================================
# Leitura
# ===========================================================================

def confere_leitura(sessao):
    print(f"\nleitura (questionario {SID})")
    r = subprocess.run([sys.executable, os.path.join(AQUI, "conformidade.py"),
                        "aplicar"], cwd=AQUI, capture_output=True, text=True)
    falhas = [] if r.returncode == 0 else [r.stderr.strip()[-300:]]
    registra("trilha de auditoria ativa, lista de bloqueio nos padroes, correcao "
             "do AuditLog na imagem", falhas,
             "deleteblacklisted N, allowunblacklist N, blockaddingtosurveys Y")

    p = sessao.chamar("list_participants", [SID, 0, 1, False, ["emailstatus"]])[0]
    pagina = urllib.request.urlopen(
        f"http://127.0.0.1:{PORTA}/index.php/optout/participants?surveyid="
        f"{SID}&langcode=pt-BR&token={p['token']}", timeout=60).read().decode()
    texto = texto_visivel(pagina)
    falhas = []
    if "Please confirm" in texto or "central participant list" in texto:
        falhas.append("ainda ha frase em ingles na pagina")
    if "Confirme que você deseja ser retirado(a)" not in texto:
        falhas.append("sem a confirmacao em portugues")
    registra("pagina de confirmacao da recusa em portugues (so GET, sem efeito)",
             falhas, "\"Confirme que você deseja ser retirado(a) da lista "
             "central…\"")


# ===========================================================================
# Exercicio
# ===========================================================================

def colunas():
    c = {l["title"]: f"Q{l['qid']}" for l in cm.sql(
        f"SELECT qid, title FROM lime_questions WHERE sid={SID} AND "
        "parent_qid=0")}
    sub = cm.sql("SELECT q.qid, q.parent_qid FROM lime_questions q JOIN "
                 f"lime_questions p ON p.qid=q.parent_qid WHERE p.sid={SID} "
                 "AND p.title='CT4' AND q.title='RECT'")[0]
    c["CT4_RECT"] = f"Q{sub['parent_qid']}_S{sub['qid']}"
    return c


def rotina():
    """A rotina de conformidade, de verdade, no conteiner. Devolve o resumo."""
    r = subprocess.run(["docker", "compose", "exec", "-T", "rotinas", "python3",
                        "conformidade.py"], cwd=AQUI, capture_output=True,
                       text=True)
    linha = next((l for l in r.stdout.splitlines() if l.startswith("RESUMO ")),
                 None)
    if r.returncode != 0 or not linha:
        raise SystemExit(f"rotina de conformidade: {r.stdout}{r.stderr}")
    return json.loads(linha[7:])


def fora_da_virada(minutos=10):
    passo = AGENDA.conformidade_intervalo_minutos * 60
    falta = passo - time.time() % passo
    if falta < minutos * 60:
        print(f"  aguardando {falta + 60:.0f} s: a rotina de conformidade "
              "agendada cai durante o teste", flush=True)
        time.sleep(falta + 60)


def exporta(sessao, token):
    try:
        bruto = sessao.chamar("export_responses_by_token", [
            SID, "json", token, None, "all", "code", "short"])
    except ErroAPI:
        return []
    return cc._registros(json.loads(base64.b64decode(bruto)))


CAMPOS = ("tid, token, participant_id, sent, remindersent, remindercount, "
          "completed, emailstatus, validuntil, usesleft, attribute_1, "
          "attribute_7")


def confere_exercicio(sessao):
    print(f"\ncaminho real (questionario {SID}, oito participantes sinteticos)")
    fora_da_virada()
    c = colunas()
    escolhidos = cm.sql(
        f"SELECT {CAMPOS} FROM lime_tokens_{SID} t WHERE email LIKE "
        f"'%@{DOMINIO}' AND sent='N' AND completed='N' AND emailstatus='OK' "
        f"AND (SELECT COUNT(*) FROM lime_tokens_{SID} u WHERE u.email=t.email)"
        "=1 ORDER BY tid LIMIT 8")
    if len(escolhidos) != 8:
        raise SystemExit("participantes insuficientes")
    por = dict(zip("ABCDEFGH", escolhidos))
    antes = {l["tid"]: l for l in cm.sql(f"SELECT {CAMPOS} FROM "
                                         f"lime_tokens_{SID}")}
    bloqueados_antes = cm.sql("SELECT COUNT(*) n FROM lime_participants "
                              "WHERE blacklisted='Y'")[0]["n"]
    auditoria_antes = int(cm.sql("SELECT COALESCE(MAX(id),0) n FROM "
                                 "lime_auditlog_log")[0]["n"])
    print("  participantes (tid): " + ", ".join(
        f"{k}={v['tid']}" for k, v in por.items()))
    print("  A recusa de consentimento na tela · B recusa de contato na tela · "
          "C conclusao com CT4 · D recusa pela mensagem · E contato invalido · "
          "F parcial com dado sensivel sem consentimento · G e H parciais com "
          "consentimento (controle)")
    copia = None
    tid = {k: int(v["tid"]) for k, v in por.items()}
    pid = {k: v["participant_id"] for k, v in por.items()}
    eq = [c[e] for e in ("EQ1", "EQ2", "EQ3", "EQ4")]

    def bloqueado(letra):
        return cm.sql("SELECT blacklisted FROM lime_participants WHERE "
                      f"participant_id='{pid[letra]}'")[0]["blacklisted"] == "Y"

    try:
        # --- planta ----------------------------------------------------------
        ccs.pagina_1(por["A"]["token"], "RCONS")
        ccs.pagina_1(por["B"]["token"], "RCONT")
        sessao.chamar("set_participant_properties", [SID, tid["C"], {
            "sent": "2026-10-01 13:00", "completed": "2026-10-04 13:00"}])
        sessao.chamar("add_response", [SID, {
            "token": por["C"]["token"], c["CON1"]: "CONC", c["CON2"]: "CONC",
            c["CONV"]: termo.identificacao(termo.le_arquivado(termo.VERSAO)),
            c["CT4_RECT"]: "Y", "lastpage": 11}])
        aberto = ccs.Respondente(por["D"]["token"])
        pagina = aberto.abridor.open(
            f"http://127.0.0.1:{PORTA}/index.php/optout/participants?surveyid="
            f"{SID}&langcode=pt-BR&token={por['D']['token']}",
            timeout=60).read().decode()
        form = ccs.le_formulario(pagina)
        acao = next(a for a in form.acoes if "removetoken" in a)
        aberto.abridor.open(urllib.request.Request(
            f"http://127.0.0.1:{PORTA}" + acao.replace("&amp;", "&"),
            data=urllib.parse.urlencode(form.campos).encode()), timeout=60).read()
        sessao.chamar("set_participant_properties", [SID, tid["E"], {
            "sent": "2026-10-01 13:00", "emailstatus": "invalido"}])
        # Parciais: submitdate vazio deixa a resposta nao enviada (add_response
        # so preenche submitdate quando a chave falta — conferido na E22).
        sensivel = {eq[0]: "MUL", eq[1]: "PRE", eq[2]: "S", eq[3]: "7"}
        for letra, con2 in (("F", "NCONC"), ("G", "CONC"), ("H", "CONC")):
            sessao.chamar("add_response", [SID, dict(sensivel, **{
                "token": por[letra]["token"], c["CON1"]: "CONC",
                c["CON2"]: con2, c["AF4"]: "sugestao de teste da E23",
                "submitdate": "", "lastpage": 10})])

        # --- 3. cifragem em repouso ----------------------------------------
        falhas = []
        cru = cm.sql(f"SELECT {eq[1]} eq2, {eq[3]} eq4, {c['AF4']} af4 FROM "
                     f"lime_responses_{SID} WHERE token='{por['H']['token']}'")[0]
        if cru["eq2"] in (None, "PRE") or cru["af4"] in (
                None, "sugestao de teste da E23"):
            falhas.append(f"valor em claro no banco: {cru}")
        if cru["eq4"] != "7":
            falhas.append("EQ4, que nao e cifrado, nao ficou em claro")
        exportado = exporta(sessao, por["H"]["token"])
        if not exportado or (exportado[0].get("EQ2"), exportado[0].get(
                "AF4")) != ("PRE", "sugestao de teste da E23"):
            falhas.append("a exportacao nao devolveu o valor decifrado")
        registra("cifragem em repouso: no banco, cifrado; na exportacao da "
                 "plataforma, o valor", falhas,
                 f"EQ2 no banco \"{(cru['eq2'] or '')[:16]}…\", exportado "
                 "\"PRE\"; EQ4, nao cifrado, \"7\"")

        # --- a rotina ---------------------------------------------------------
        resumo = rotina()

        # --- 4. registro --------------------------------------------------------
        falhas = []
        reg = {int(l["tid"]): l for l in cm.sql(
            "SELECT tid, tipo, via, manifestada_em, fonte_do_momento, "
            "versao_termo, base_central_em FROM egressos_recusas WHERE "
            f"questionario={SID} AND tid IN ("
            + ",".join(str(t) for t in tid.values()) + ")")}
        esperado = {"A": ("consentimento", "tela", "CONDH"),
                    "B": ("contato", "tela", "CONDH"),
                    "C": ("contato", "conclusao", "submitdate"),
                    "D": ("contato", "mensagem", "auditoria")}
        for letra, (tipo, via, fonte) in esperado.items():
            r = reg.get(tid[letra])
            if not r:
                falhas.append(f"{letra}: sem registro")
                continue
            if (r["tipo"], r["via"], r["fonte_do_momento"]) != (tipo, via, fonte):
                falhas.append(f"{letra}: {r['tipo']}/{r['via']}/"
                              f"{r['fonte_do_momento']}")
            if not r["manifestada_em"].endswith("+00:00"):
                falhas.append(f"{letra}: momento sem UTC explicito")
            if not (r["versao_termo"] or "").startswith(termo.VERSAO):
                falhas.append(f"{letra}: versao {r['versao_termo']}")
        for letra in "EFGH":
            if tid[letra] in reg:
                falhas.append(f"{letra}: registrado sem ser recusa")
        registra("cada recusa registrada com tipo, via, momento e versao; "
                 "contato invalido, nao", falhas,
                 "A consentimento/tela, B contato/tela, C contato/conclusao, "
                 "D contato/mensagem (momento da trilha); E, F, G, H fora")

        # --- 5. base central ----------------------------------------------------
        falhas = []
        for letra in "BCD":
            if not bloqueado(letra):
                falhas.append(f"{letra}: nao bloqueado na base central")
            if not reg.get(tid[letra], {}).get("base_central_em"):
                falhas.append(f"{letra}: registro sem base_central_em")
        for letra in "AE":
            if bloqueado(letra):
                falhas.append(f"{letra}: bloqueado sem recusa de contato")
        trilha = {l["entityid"] for l in cm.sql(
            "SELECT entityid FROM lime_auditlog_log WHERE entity='participant' "
            f"AND id > {auditoria_antes} AND newvalues LIKE "
            "'%\"blacklisted\":\"Y\"%'")}
        for letra in "BCD":
            if pid[letra] not in trilha:
                falhas.append(f"{letra}: bloqueio sem registro na trilha")
        registra("recusa de contato levada a base central pela plataforma, com "
                 "trilha; consentimento e contato invalido, nao", falhas,
                 f"B, C e D bloqueados ({resumo['levadas_a_base_central']} "
                 "levados nesta passada); A e E livres")

        # --- 6. o ciclo seguinte ----------------------------------------------
        falhas = []
        r = subprocess.run([sys.executable, os.path.join(
            AQUI, "instrumento", "instrumento.py"), "copia-de-ensaio"],
            cwd=AQUI, capture_output=True, text=True)
        m = re.search(r"questionario (\d+)", r.stdout)
        if r.returncode != 0 or not m:
            raise SystemExit(f"copia de ensaio: {r.stderr.strip()[-200:]}")
        copia = int(m.group(1))
        novos = sessao.chamar("add_participants", [copia, [
            {"firstname": "Ensaio", "lastname": f"Ciclo seguinte {letra}",
             "email": f"ciclo-seguinte-{letra.lower()}@{DOMINIO}",
             "participant_id": pid[letra]} for letra in "ABCDE"], True])
        tid_copia = {letra: int(n["tid"]) for letra, n in zip("ABCDE", novos)}
        convidados = {}
        for letra in "ABCDE":
            try:
                res = sessao.chamar("invite_participants",
                                    [copia, [tid_copia[letra]], True, True])
                convidados[letra] = any(isinstance(v, dict) and v.get(
                    "status") == "OK" for v in res.values())
            except ErroAPI as e:
                convidados[letra] = False if "No candidate tokens" in str(e) \
                    else f"erro: {e}"
        quer = {"A": True, "B": False, "C": False, "D": False, "E": True}
        if convidados != quer:
            falhas.append(f"convites no ciclo seguinte {convidados}, "
                          f"esperados {quer}")
        registra("ciclo seguinte: quem recusou contato, por qualquer via, nao e "
                 "convidado; recusa de consentimento e contato invalido, sim",
                 falhas, "B, C e D: \"No candidate tokens\"; A e E convidados")

        # --- 7. ciclo corrente ------------------------------------------------
        falhas = []
        estados = ccs.estados_da_rotina([tid["A"], tid["B"], tid["C"],
                                         tid["D"], tid["E"]])
        quer = {"A": "recusa de consentimento", "B": "recusa de contato",
                "C": "recusa de contato", "D": "recusa de contato",
                "E": "contato inválido"}
        for letra, e in quer.items():
            if estados.get(tid[letra]) != e:
                falhas.append(f"{letra}: {estados.get(tid[letra])}, esperado {e}")
        registra("ciclo corrente: as recusas e o contato invalido interrompem a "
                 "cadencia da rotina", falhas,
                 "A recusa de consentimento; B, C, D recusa de contato; E "
                 "contato inválido")

        # --- 8. dado sensivel sem consentimento --------------------------------
        falhas = []
        linhas = {l["token"]: l for l in cm.sql(
            f"SELECT token, " + ", ".join(eq) + f" FROM lime_responses_{SID} "
            "WHERE token IN (" + ",".join(f"'{por[x]['token']}'" for x in "FGH")
            + ")")}
        if any(linhas[por["F"]["token"]][col] for col in eq):
            falhas.append("F: dado sensivel sem consentimento ficou")
        for letra in "GH":
            if not all(linhas[por[letra]["token"]][col] for col in eq):
                falhas.append(f"{letra}: dado com consentimento foi apagado")
        hig = cm.sql("SELECT campos FROM egressos_higienizacoes h JOIN "
                     f"lime_responses_{SID} r ON r.id=h.resposta_id WHERE "
                     f"r.token='{por['F']['token']}'")
        if len(hig) != 1:
            falhas.append(f"F: {len(hig)} registros de higienizacao")
        registra("dado sensivel sem consentimento apagado, e registrado; com "
                 "consentimento, mantido", falhas,
                 "F (CON2 nao concordo): EQ1 a EQ4 apagados; G e H mantidos")

        # --- 9. idempotencia --------------------------------------------------
        de_novo = rotina()
        falhas = [] if (de_novo["recusas_registradas"], de_novo[
            "levadas_a_base_central"], de_novo["respostas_higienizadas"]) == (
            0, 0, 0) else [f"segunda passada fez {de_novo}"]
        registra("a rotina e idempotente: a segunda passada nao faz nada",
                 falhas, "0 registros, 0 bloqueios, 0 higienizacoes")

        # --- 10. revogacao ----------------------------------------------------
        falhas = []
        r = subprocess.run([sys.executable, os.path.join(AQUI, "conformidade.py"),
                            "revogar", "--identificador",
                            por["B"]["attribute_1"], "--registro",
                            "teste da E23: pedido simulado"],
                           cwd=AQUI, capture_output=True, text=True)
        if r.returncode != 0:
            falhas.append(f"revogar: {r.stderr.strip()[-200:]}")
        if bloqueado("B"):
            falhas.append("B continua bloqueado")
        tok_b = cm.sql(f"SELECT emailstatus FROM lime_tokens_{SID} WHERE "
                       f"tid={tid['B']}")[0]["emailstatus"]
        if tok_b != "OK":
            falhas.append(f"participante B com {tok_b}")
        rotina()
        if bloqueado("B"):
            falhas.append("a rotina voltou a bloquear B depois da revogacao")
        rev = cm.sql("SELECT revogada_em, revogacao FROM egressos_recusas WHERE "
                     f"tid={tid['B']} AND questionario={SID}")
        if not rev or not rev[0]["revogada_em"]:
            falhas.append("revogacao nao registrada")
        trilha = cm.sql(
            "SELECT COUNT(*) n FROM lime_auditlog_log WHERE entity='participant' "
            f"AND entityid='{pid['B']}' AND id > {auditoria_antes} AND "
            "newvalues LIKE '%\"blacklisted\":\"N\"%'")[0]["n"]
        if trilha == "0":
            falhas.append("revogacao sem registro na trilha")
        registra("revogacao pelo operador: tira o bloqueio, fica registrada e na "
                 "trilha, e a rotina nao volta a bloquear", falhas,
                 "B livre; recusa marcada como revogada; RCONT antiga ignorada")

        # --- 11. recuperavel ----------------------------------------------------
        falhas = []
        exemplos = {}
        for letra, trecho in (("B", "revogada em"), ("D", "pela mensagem"),
                              ("A", "vale so neste ciclo")):
            reg_c = cc.consulta(sessao, SID, por[letra]["attribute_1"])
            linhas = ccs._imprime(reg_c)
            exemplos[letra] = linhas
            if not any(trecho in l for l in linhas):
                falhas.append(f"{letra}: consulta sem \"{trecho}\"")
        registra("recusas e revogacao recuperaveis por identificador", falhas,
                 "consulta-consentimento.py")
        print("  exemplo de consulta (D, recusa pela mensagem):")
        for linha in exemplos.get("D", []):
            print(f"    | {linha}")
    finally:
        limpa(sessao, por, antes, bloqueados_antes, copia)


def limpa(sessao, por, antes, bloqueados_antes, copia):
    """Cada passo independente: uma falha num nao impede os outros. A trilha de
    auditoria NAO e limpa: ela registra tambem os testes, e e o que uma trilha
    deve fazer."""
    falhas = []
    tokens = [v["token"] for v in por.values()]
    pids = [v["participant_id"] for v in por.values()]
    passos = [
        ("copia de ensaio", lambda: copia and subprocess.run(
            [sys.executable, os.path.join(AQUI, "instrumento",
                                          "instrumento.py"), "remover",
             "--sid", str(copia)], cwd=AQUI, check=True, capture_output=True)),
        ("respostas", lambda: [
            sessao.chamar("delete_response", [SID, int(r["id"])])
            for r in cm.sql(f"SELECT id FROM lime_responses_{SID} WHERE token "
                            "IN (" + ",".join(f"'{t}'" for t in tokens) + ")")]),
        ("participantes", lambda: [sessao.chamar(
            "set_participant_properties", [SID, int(v["tid"]), {
                "sent": antes[v["tid"]]["sent"],
                "remindersent": antes[v["tid"]]["remindersent"],
                "remindercount": int(antes[v["tid"]]["remindercount"]),
                "completed": antes[v["tid"]]["completed"],
                "emailstatus": antes[v["tid"]]["emailstatus"],
                "validuntil": antes[v["tid"]]["validuntil"],
                "usesleft": int(antes[v["tid"]]["usesleft"]),
                "attribute_7": antes[v["tid"]]["attribute_7"] or ""}])
            for v in por.values()]),
        ("base central", lambda: cm.sql(
            "UPDATE lime_participants SET blacklisted='N' WHERE participant_id "
            "IN (" + ",".join(f"'{p}'" for p in pids) + ")")),
        ("registro proprio", lambda: (
            cm.sql(f"DELETE FROM egressos_recusas WHERE questionario={SID} AND "
                   "tid IN (" + ",".join(v["tid"] for v in por.values()) + ")"),
            cm.sql("DELETE FROM egressos_higienizacoes WHERE questionario="
                   f"{SID} AND resposta_id NOT IN (SELECT id FROM "
                   f"lime_responses_{SID})"))),
        ("caixa", lambda: [cm.apaga(cm.CAIXA_ENTREGUES, crit) for crit in
                           [["TO", f"ciclo-seguinte-{x}@{DOMINIO}"]
                            for x in "abcde"]]),
    ]
    for rotulo, passo in passos:
        try:
            passo()
        except (Exception, SystemExit) as ex:  # noqa: BLE001
            falhas.append(f"limpeza de {rotulo}: {ex}")
    depois = {l["tid"]: l for l in cm.sql(f"SELECT {CAMPOS} FROM "
                                          f"lime_tokens_{SID}")}
    for tid_, a in antes.items():
        for c in ("sent", "remindersent", "remindercount", "completed",
                  "emailstatus", "validuntil", "usesleft", "attribute_7"):
            if (depois[tid_][c] or None) != (a[c] or None):
                falhas.append(f"tid {tid_}: {c} {a[c]} -> {depois[tid_][c]}")
    sobra = cm.sql(
        f"SELECT (SELECT COUNT(*) FROM lime_responses_{SID}) r, "
        "(SELECT COUNT(*) FROM lime_participants WHERE blacklisted='Y') b, "
        "(SELECT COUNT(*) FROM egressos_recusas) rec, "
        "(SELECT COUNT(*) FROM egressos_higienizacoes) hig")[0]
    if sobra != {"r": "0", "b": bloqueados_antes, "rec": "0", "hig": "0"}:
        falhas.append(f"sobrou: {sobra}")
    if copia and cm.sql(f"SELECT COUNT(*) n FROM lime_surveys WHERE "
                        f"sid={copia}")[0]["n"] != "0":
        falhas.append(f"a copia {copia} ficou")
    registra("limpeza", falhas,
             "500 participantes como antes; nenhuma resposta, bloqueio, recusa "
             "ou higienizacao; copia removida; a trilha fica, por ser trilha")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--exercitar", action="store_true",
                    help="caminho real com oito participantes, e desfaz")
    args = ap.parse_args()
    print(f"conformidade do questionario {SID}")
    try:
        with api_do_hospedeiro() as sessao:
            confere_leitura(sessao)
            if args.exercitar:
                confere_exercicio(sessao)
    except ErroAPI as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    print(f"\n  {sum(resultados)} de {len(resultados)} conferencias passaram")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
