#!/usr/bin/env python3
"""
Valida o arquivo de entrada contra o leiaute (E11), antes de qualquer importacao.

Implementa as secoes 3 a 7 de docs/especificacao/leiaute-entrada.md, no modo de
ensaio, com os tres niveis de consequencia da secao 6:

    rejeita o arquivo    o problema e da extracao — nada e importado
    rejeita o registro   o problema e do dado — o resto segue
    aceita com alerta    o dado faltante ou invalido e opcional

E as normalizacoes que o leiaute manda fazer: espacos nas pontas removidos,
espacos internos repetidos do nome reduzidos a um, dominio dos enderecos em
minusculas, marcador de ordem de bytes descartado.

O relatorio identifica cada registro afetado pela LINHA e pelo IDENTIFICADOR, e
nunca reproduz nome, endereco ou telefone (secao 6): dado pessoal copiado para
registro de execucao e dado pessoal fora do lugar onde e protegido.

Uso direto, da raiz do repositorio, so para validar — nao importa nem elimina
nada:

    python3 scripts/valida_entrada.py dados/sinteticos/base-sintetica.csv

Usado como modulo por importar_base.py, que faz a importacao (E17). As listas
de cursos e unidades vem de infra/instrumento/configuracao/ — o mesmo dominio
do instrumento.
"""

import csv
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date

CONFIGURACAO = os.environ.get("CONFIGURACAO", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "infra", "instrumento", "configuracao"))

CAMPOS = ["identificador", "nome", "curso", "nivel", "campus", "ano_conclusao",
          "semestre_conclusao", "email_principal", "email_alternativo",
          "telefone"]
OBRIGATORIOS = ["identificador", "nome", "curso", "nivel", "campus",
                "ano_conclusao", "semestre_conclusao", "email_principal"]
NIVEIS = ("tecnico", "graduacao", "pos_graduacao")

# Secao 4.6: dot-atom da RFC 5322 na parte local; dominio com ao menos um ponto.
_ATEXT = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]"
RX_LOCAL = re.compile(rf"{_ATEXT}+(\.{_ATEXT}+)*")
RX_DOMINIO = re.compile(r"[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+")
RX_IDENTIFICADOR = re.compile(r"[A-Za-z0-9._-]{1,64}")


class Resultado:
    def __init__(self):
        self.arquivo_rejeitado = None   # motivo, se o arquivo inteiro cai
        self.linhas = 0                 # registros lidos (sem linhas vazias)
        self.aceitos = []               # (linha, registro normalizado)
        self.rejeitados = []            # (linha, identificador, regra)
        self.alertas = []               # (linha, identificador, regra)

    def contagens(self):
        c = Counter()
        for _, _, regra in self.rejeitados:
            c["rejeita registro: " + regra] += 1
        for _, _, regra in self.alertas:
            c["alerta: " + regra] += 1
        return dict(sorted(c.items()))

    def com_alerta(self):
        return len({linha for linha, _, _ in self.alertas
                    if linha in {l for l, _ in self.aceitos}})


# ---------------------------------------------------------------------------
# Regras de campo
# ---------------------------------------------------------------------------

def tem_forma_de_cpf(valor):
    """Secao 4.1: onze digitos, desconsiderados ponto e hifen, cujos dois
    ultimos conferem como verificadores de CPF."""
    d = re.sub(r"[.\-]", "", valor)
    if not re.fullmatch(r"\d{11}", d):
        return False
    x = [int(c) for c in d]
    for n in (9, 10):
        soma = sum(x[i] * (n + 1 - i) for i in range(n))
        if (soma * 10) % 11 % 10 != x[n]:
            return False
    return True


def normaliza_email(valor):
    """Devolve o endereco com o dominio em minusculas, ou None se a sintaxe da
    secao 4.6 nao for atendida. A parte local e preservada como veio."""
    if len(valor) > 254 or valor.count("@") != 1:
        return None
    local, dominio = valor.split("@")
    if not (1 <= len(local) <= 64) or len(dominio) > 255:
        return None
    if not RX_LOCAL.fullmatch(local) or not RX_DOMINIO.fullmatch(dominio):
        return None
    return f"{local}@{dominio.lower()}"


def telefone_valido(valor):
    """Secao 4.7: E.164; no Brasil, codigo de area e 8 digitos, ou 9 iniciados
    por 9."""
    if not re.fullmatch(r"\+\d{1,15}", valor):
        return False
    if valor.startswith("+55"):
        return bool(re.fullmatch(r"\+55\d{2}(9\d{8}|\d{8})", valor))
    return True


def nome_valido(valor):
    """Secao 4.2: 2 a 150 caracteres; comeca por letra; so letras de qualquer
    alfabeto, espaco, apostrofo, hifen e ponto; ao menos duas letras."""
    return (2 <= len(valor) <= 150 and valor[0].isalpha()
            and all(c.isalpha() or c in " '-." for c in valor)
            and sum(c.isalpha() for c in valor) >= 2)


# Secao 7 — so no modo de ensaio, que e o unico deste projeto.
def fora_do_ensaio_email(endereco):
    return not endereco.lower().endswith(".test")


def fora_do_ensaio_telefone(numero):
    return not re.fullmatch(r"\+55[1-9]0\d{8,9}", numero)


# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------

def le_configuracao(diretorio=CONFIGURACAO):
    def csv_de(nome):
        with open(os.path.join(diretorio, nome + ".csv"), encoding="utf-8",
                  newline="") as fh:
            return list(csv.DictReader(fh))
    with open(os.path.join(diretorio, "parametros.json"), encoding="utf-8") as fh:
        parametros = json.load(fh)
    return {
        "cursos": {c["nome"]: c for c in csv_de("cursos")},
        "unidades": {u["nome"]: u for u in csv_de("unidades")},
        "ano_minimo": int(parametros["ano_conclusao_minimo"]),
    }


# ---------------------------------------------------------------------------
# Validacao
# ---------------------------------------------------------------------------

def valida(conteudo, configuracao=None, ano_corrente=None):
    """Valida os bytes do arquivo. Devolve um Resultado."""
    cfg = configuracao or le_configuracao()
    ano_corrente = ano_corrente or date.today().year
    res = Resultado()

    # --- arquivo: codificacao -------------------------------------------
    try:
        texto = conteudo.decode("utf-8")
    except UnicodeDecodeError:
        res.arquivo_rejeitado = (
            "o arquivo nao decodifica como UTF-8 — causa provavel: planilha "
            "exportada em codificacao regional (secao 3)")
        return res
    if texto.startswith("﻿"):
        texto = texto[1:]  # marcador de ordem de bytes: tolerado e descartado

    # --- arquivo: estrutura CSV -----------------------------------------
    try:
        leitor = csv.reader(io.StringIO(texto, newline=""), strict=True)
        linhas = []
        for campos in leitor:
            linhas.append((leitor.line_num, campos))
    except csv.Error as e:
        res.arquivo_rejeitado = (f"CSV malformado ({e}) — aspas nao fechadas "
                                 "ate o fim do arquivo? (secao 3)")
        return res
    if not linhas:
        res.arquivo_rejeitado = "arquivo vazio"
        return res

    # --- arquivo: cabecalho ---------------------------------------------
    cabecalho = [c.strip() for c in linhas[0][1]]
    if len(cabecalho) == 1 and ";" in cabecalho[0]:
        res.arquivo_rejeitado = (
            "cabecalho nao se divide em campos por virgula — causa provavel: "
            "planilha exportada com ponto e virgula (secao 3)")
        return res
    repetidos = sorted(c for c, n in Counter(cabecalho).items() if n > 1)
    faltando = sorted(set(CAMPOS) - set(cabecalho))
    sobrando = sorted(set(cabecalho) - set(CAMPOS))
    if repetidos or faltando or sobrando:
        partes = []
        if faltando:
            partes.append(f"faltam {faltando}")
        if sobrando:
            partes.append(f"colunas fora do leiaute {sobrando}")
        if repetidos:
            partes.append(f"repetidas {repetidos}")
        res.arquivo_rejeitado = ("cabecalho fora do leiaute fechado: "
                                 + "; ".join(partes) + " (secao 3)")
        return res

    # --- registros ------------------------------------------------------
    candidatos = []  # (linha, registro) que passaram nas regras de campo
    for numero, campos in linhas[1:]:
        if not any(c.strip() for c in campos):
            continue  # linha inteiramente vazia: ignorada
        res.linhas += 1
        ident_bruto = (campos[cabecalho.index("identificador")].strip()
                       if len(campos) > cabecalho.index("identificador") else "")
        if len(campos) != len(cabecalho):
            res.rejeitados.append((numero, ident_bruto,
                                   "numero de campos diferente do cabecalho"))
            continue
        if any("\n" in c or "\r" in c for c in campos):
            res.rejeitados.append((numero, ident_bruto,
                                   "campo com quebra de linha"))
            continue
        r = {k: v.strip() for k, v in zip(cabecalho, campos)}
        ident = r["identificador"]

        vazio = [k for k in OBRIGATORIOS if not r[k]]
        if vazio:
            res.rejeitados.append((numero, ident,
                                   f"campo obrigatorio vazio: {vazio[0]}"))
            continue
        if not RX_IDENTIFICADOR.fullmatch(ident):
            res.rejeitados.append((numero, ident, "identificador fora da regra"))
            continue
        if tem_forma_de_cpf(ident):
            res.rejeitados.append((numero, ident, "identificador com forma de CPF"))
            continue
        r["nome"] = re.sub(r" {2,}", " ", r["nome"])
        if not nome_valido(r["nome"]):
            res.rejeitados.append((numero, ident, "nome fora da regra"))
            continue
        curso = cfg["cursos"].get(r["curso"])
        if curso is None:
            res.rejeitados.append((numero, ident, "curso fora da lista"))
            continue
        if r["nivel"] not in NIVEIS:
            res.rejeitados.append((numero, ident, "nivel fora do dominio"))
            continue
        if curso["nivel"] != r["nivel"]:
            # Regra ativada pela E13: a lista de cursos registra o nivel.
            res.rejeitados.append((numero, ident,
                                   "nivel incoerente com o curso"))
            continue
        if r["campus"] not in cfg["unidades"]:
            res.rejeitados.append((numero, ident, "campus fora da lista"))
            continue
        if not re.fullmatch(r"\d{4}", r["ano_conclusao"]) or not (
                cfg["ano_minimo"] <= int(r["ano_conclusao"]) <= ano_corrente):
            res.rejeitados.append((numero, ident, "ano de conclusao fora da regra"))
            continue
        if r["semestre_conclusao"] not in ("1", "2"):
            res.rejeitados.append((numero, ident, "semestre fora do dominio"))
            continue
        principal = normaliza_email(r["email_principal"])
        if principal is None:
            res.rejeitados.append((numero, ident, "email principal fora da sintaxe"))
            continue
        r["email_principal"] = principal

        # Opcionais: fora da regra, o valor e descartado e o registro entra.
        if r["email_alternativo"]:
            alternativo = normaliza_email(r["email_alternativo"])
            if alternativo is None:
                res.alertas.append((numero, ident,
                                    "email alternativo fora da sintaxe, descartado"))
                r["email_alternativo"] = ""
            elif alternativo.lower() == principal.lower():
                res.alertas.append((numero, ident,
                                    "email alternativo igual ao principal, descartado"))
                r["email_alternativo"] = ""
            else:
                r["email_alternativo"] = alternativo
        if r["telefone"] and not telefone_valido(r["telefone"]):
            res.alertas.append((numero, ident, "telefone fora da regra, descartado"))
            r["telefone"] = ""
        candidatos.append((numero, r))

    # --- secao 7: restricoes do ensaio — rejeitam o ARQUIVO -------------
    # Aplicadas aos valores que sobreviveram a sintaxe: valor malformado ja foi
    # tratado pela secao 6. Um endereco real numa base sintetica e sinal de
    # vazamento, e nao defeito pontual.
    for numero, r in candidatos:
        for campo in ("email_principal", "email_alternativo"):
            if r[campo] and fora_do_ensaio_email(r[campo]):
                res.arquivo_rejeitado = (
                    f"modo de ensaio: endereco fora de .test na linha {numero} "
                    f"(identificador {r['identificador']}) — o arquivo inteiro "
                    "e rejeitado (secao 7)")
                res.aceitos, res.alertas = [], []
                return res
        if r["telefone"] and fora_do_ensaio_telefone(r["telefone"]):
            res.arquivo_rejeitado = (
                f"modo de ensaio: telefone fora de +55 com codigo de area "
                f"terminado em 0 na linha {numero} (identificador "
                f"{r['identificador']}) — o arquivo inteiro e rejeitado (secao 7)")
            res.aceitos, res.alertas = [], []
            return res

    # --- secao 5: regras entre registros --------------------------------
    por_ident = defaultdict(list)
    for numero, r in candidatos:
        por_ident[r["identificador"].lower()].append(numero)
    repetidos = {k for k, v in por_ident.items() if len(v) > 1}
    for numero, r in candidatos:
        if r["identificador"].lower() in repetidos:
            # Todos os registros do identificador repetido caem: nao ha como
            # saber qual esta certo.
            res.rejeitados.append((numero, r["identificador"],
                                   "identificador repetido no arquivo"))
        else:
            res.aceitos.append((numero, r))

    por_principal = defaultdict(set)
    for numero, r in res.aceitos:
        por_principal[r["email_principal"].lower()].add(r["identificador"])
    for numero, r in res.aceitos:
        if len(por_principal[r["email_principal"].lower()]) > 1:
            res.alertas.append((numero, r["identificador"],
                                "email principal compartilhado com outro identificador"))
        if not r["email_alternativo"] and not r["telefone"]:
            res.alertas.append((numero, r["identificador"],
                                "sem via alternativa de contato"))
    res.rejeitados.sort()
    res.alertas.sort()
    return res


def relatorio(res):
    """Texto do relatorio — linha e identificador, nunca dado de contato."""
    if res.arquivo_rejeitado:
        return f"ARQUIVO REJEITADO: {res.arquivo_rejeitado}"
    saida = [
        f"registros lidos: {res.linhas}",
        f"aceitos: {len(res.aceitos)} (com alerta: {res.com_alerta()})",
        f"rejeitados: {len(res.rejeitados)}",
    ]
    for regra, n in res.contagens().items():
        saida.append(f"  {regra}: {n}")
    for numero, ident, regra in res.rejeitados:
        saida.append(f"  rejeitado — linha {numero}, identificador {ident}: {regra}")
    return "\n".join(saida)


def main():
    if len(sys.argv) != 2:
        print("uso: valida_entrada.py <arquivo.csv>", file=sys.stderr)
        return 2
    with open(sys.argv[1], "rb") as fh:
        res = valida(fh.read())
    print(relatorio(res))
    return 1 if res.arquivo_rejeitado else 0


if __name__ == "__main__":
    sys.exit(main())
