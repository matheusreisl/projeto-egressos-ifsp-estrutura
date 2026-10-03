#!/usr/bin/env python3
"""
Gera a base sintetica de egressos que valida o mecanismo (E16).

Produz um arquivo no leiaute de docs/especificacao/leiaute-entrada.md (E11):
dez campos, uma linha por pessoa (ADR-0005), UTF-8 e virgula (RFC 4180).
Nenhum valor vem de pessoa real:

  - os nomes sao INVENTADOS, por silabas, e o gerador recusa qualquer prenome ou
    sobrenome que coincida com os mais frequentes no Brasil. Isso torna muito
    improvavel — nao impossivel — que um nome inteiro coincida com o de alguem;
  - os enderecos estao todos sob o TLD reservado .test (RFC 2606 e 6761), nos
    tres dominios do correio de ensaio (E09), cada um produzindo uma linha da
    tabela de classificacao do P8;
  - os telefones sao +55 com codigo de area terminado em 0, que nao existe: os
    67 codigos em uso foram reconferidos na fonte oficial da Anatel na E16;
  - os identificadores sao SIN-000001 em diante — sinteticos, estaveis e sem
    forma de CPF.

Cursos e unidades vem de infra/instrumento/configuracao/ (E15), que e o mesmo
dominio do instrumento: o arquivo leva o NOME, e o nivel e o do curso na lista.

O gerador e deterministico: a mesma semente e os mesmos parametros produzem o
mesmo arquivo, byte a byte. E isso que da ao identificador a estabilidade entre
"extracoes" que o leiaute exige (secao 4.1).

Roda no hospedeiro, e nao no conteiner `rotinas`, porque grava em dados/, que o
conteiner nao monta. Uso, da raiz do repositorio:

    python3 scripts/gerar_base_sintetica.py
    python3 scripts/gerar_base_sintetica.py --semente 7 --quantidade 500

O arquivo vai para dados/sinteticos/, que nao e versionado. O resumo impresso
nao reproduz nome, endereco nem telefone (leiaute, secao 6).
"""

import argparse
import csv
import hashlib
import io
import os
import random
import re
import sys
import unicodedata
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIGURACAO = os.path.join(RAIZ, "infra", "instrumento", "configuracao")
SAIDA_PADRAO = os.path.join(RAIZ, "dados", "sinteticos", "base-sintetica.csv")

SEMENTE_PADRAO = 2016
QUANTIDADE_PADRAO = 500
ANO_INICIAL_PADRAO = 2016
ANOS_PADRAO = 10

CAMPOS = ["identificador", "nome", "curso", "nivel", "campus", "ano_conclusao",
          "semestre_conclusao", "email_principal", "email_alternativo",
          "telefone"]

# ---------------------------------------------------------------------------
# Composicao da base. Proporcoes de ensaio, e nao estimativa de populacao:
# os numeros desta base nao comportam interpretacao substantiva.
# ---------------------------------------------------------------------------

NIVEIS = [("tecnico", 0.50), ("graduacao", 0.40), ("pos_graduacao", 0.10)]

# Os tres dominios do correio de ensaio (leitura-devolucoes.md, secao 2).
DOMINIO_ENTREGA = "egressos.test"         # sem retorno: segue a cadencia
DOMINIO_PERMANENTE = "invalido.test"      # erro permanente (5.x.x)
DOMINIO_TEMPORARIO = "indisponivel.test"  # erro temporario (4.x.x)
DOMINIOS_PRINCIPAL = [(DOMINIO_ENTREGA, 0.85), (DOMINIO_PERMANENTE, 0.10),
                      (DOMINIO_TEMPORARIO, 0.05)]
DOMINIOS_ALTERNATIVO = [(DOMINIO_ENTREGA, 0.90), (DOMINIO_PERMANENTE, 0.10)]

P_ALTERNATIVO = 0.40
P_TELEFONE = 0.55
P_DOMINIO_MAIUSCULO = 0.02   # o leiaute normaliza o dominio para minusculas
PARES_COMPARTILHADOS = 3     # mesmo e-mail principal em dois identificadores

# Codigos de area terminados em 0: nenhum esta em uso (E11; reconferido na E16
# contra o painel oficial da Anatel).
DDD_ENSAIO = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]

# ---------------------------------------------------------------------------
# Nomes inventados
# ---------------------------------------------------------------------------

ATAQUES = ["b", "c", "d", "f", "g", "j", "l", "m", "n", "p", "r", "s", "t",
           "v", "z", "br", "cr", "dr", "fl", "gr", "pr", "tr", "ch", "lh", "nh",
           "qu", "x"]
ATAQUES_INICIAIS = [a for a in ATAQUES if a not in ("lh", "nh")]
VOGAIS = ["a", "e", "i", "o", "u"] * 4 + ["á", "é", "í", "ó", "ú", "â", "ê",
                                          "ô", "ã"]
CODAS = [""] * 6 + ["n", "r", "s", "l"]
FINAIS_PRENOME = ["a", "o", "e", "is", "el", "ana", "ino", "ara", "ilde",
                  "ão", "iel", "ícia"]
FINAIS_SOBRENOME = ["es", "o", "a", "ar", "ado", "eira", "ento", "inho", "al",
                    "ães", "ez"]
PARTICULAS = ["da", "de", "do", "das", "dos"]

# Guarda: prenomes e sobrenomes mais frequentes no Brasil. Um nome inventado que
# coincida com qualquer um deles e descartado e sorteado de novo. Nao e lista de
# pessoas: e a lista do que NAO pode sair.
PROIBIDOS = {
    "maria", "jose", "ana", "joao", "antonio", "francisco", "carlos", "paulo",
    "pedro", "lucas", "luiz", "luis", "marcos", "gabriel", "rafael", "daniel",
    "marcelo", "bruno", "eduardo", "felipe", "raimundo", "rodrigo", "manoel",
    "manuel", "mateus", "matheus", "andre", "fernando", "fabio", "leonardo",
    "gustavo", "guilherme", "leandro", "tiago", "thiago", "ricardo", "marcio",
    "jorge", "sebastiao", "alexandre", "roberto", "edson", "diego", "vitor",
    "sergio", "claudio", "geraldo", "adriano", "luciano", "julio", "renato",
    "vinicius", "rogerio", "samuel", "ronaldo", "mario", "flavio", "douglas",
    "igor", "davi", "juliana", "marcia", "fernanda", "patricia", "aline",
    "sandra", "camila", "amanda", "bruna", "jessica", "leticia", "julia",
    "luciana", "vanessa", "mariana", "gabriela", "vera", "vitoria", "larissa",
    "claudia", "beatriz", "rita", "luana", "sonia", "renata", "eliane",
    "josefa", "adriana", "simone", "natalia", "francisca", "cristiane",
    "carla", "debora", "rosangela", "daniela", "raquel", "lucia", "isabela",
    "silva", "santos", "oliveira", "souza", "sousa", "rodrigues", "ferreira",
    "alves", "pereira", "lima", "gomes", "costa", "ribeiro", "martins",
    "carvalho", "almeida", "lopes", "soares", "fernandes", "vieira", "barbosa",
    "rocha", "dias", "nascimento", "andrade", "moreira", "nunes", "marques",
    "machado", "mendes", "freitas", "cardoso", "ramos", "goncalves", "santana",
    "teixeira", "araujo", "castro", "pinto", "moura", "correia", "cavalcanti",
    "melo", "barros", "campos", "reis", "batista", "monteiro", "duarte",
}


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn")


def silabas(rng, n, inicial=True):
    partes = []
    for i in range(n):
        ataque = rng.choice(ATAQUES_INICIAIS if (i == 0 and inicial) else ATAQUES)
        partes.append(ataque + rng.choice(VOGAIS) + rng.choice(CODAS))
    return "".join(partes)


def palavra(rng, finais, minimo, maximo):
    while True:
        p = (silabas(rng, rng.randint(minimo, maximo)) + rng.choice(finais))
        # No maximo um acento por palavra, como no portugues.
        acentos = [i for i, c in enumerate(p) if sem_acento(c) != c]
        for i in acentos[1:]:
            p = p[:i] + sem_acento(p[i]) + p[i + 1:]
        p = p.capitalize()
        if sem_acento(p).lower() not in PROIBIDOS and len(p) >= 3:
            return p


def nome_inventado(rng):
    """Prenome, as vezes dois, e sobrenomes. Uma fracao de cada forma que a
    secao 4.2 do leiaute admite: particula, apostrofo, hifen e abreviatura com
    ponto."""
    prenomes = [palavra(rng, FINAIS_PRENOME, 1, 2)]
    if rng.random() < 0.30:
        prenomes.append(palavra(rng, FINAIS_PRENOME, 1, 2))
    sobrenomes = []
    for _ in range(rng.choice([1, 2, 2, 2, 3])):
        s = palavra(rng, FINAIS_SOBRENOME, 1, 2)
        sorteio = rng.random()
        if sorteio < 0.05:
            s = "D'" + s  # apostrofo
        elif sorteio < 0.10:
            s = s + "-" + palavra(rng, FINAIS_SOBRENOME, 1, 2)  # hifen
        sobrenomes.append(s)
    # No maximo uma particula, antes do ultimo sobrenome.
    if rng.random() < 0.35 and not sobrenomes[-1].startswith("D'"):
        sobrenomes.insert(len(sobrenomes) - 1, rng.choice(PARTICULAS))
    if rng.random() < 0.05:
        prenomes.append(rng.choice("BCDFGLMNPRSTV") + ".")  # abreviatura
    return " ".join(prenomes + sobrenomes)


# ---------------------------------------------------------------------------
# Contatos
# ---------------------------------------------------------------------------

def parte_local(nome, sufixo):
    """Parte local a partir do nome, sem acento, so com o que o dot-atom
    admite; o sufixo numerico garante unicidade."""
    tokens = [re.sub(r"[^a-z0-9]", "", sem_acento(t).lower())
              for t in nome.split()]
    tokens = [t for t in tokens if t and t not in PARTICULAS and len(t) > 1]
    return f"{tokens[0]}.{tokens[-1]}.{sufixo}"


def escolhe(rng, pesos):
    valores, p = zip(*pesos)
    return rng.choices(valores, weights=p, k=1)[0]


def telefone(rng):
    ddd = rng.choice(DDD_ENSAIO)
    if rng.random() < 0.75:
        numero = "9" + "".join(rng.choice("0123456789") for _ in range(8))
    else:
        numero = rng.choice("2345") + "".join(rng.choice("0123456789")
                                              for _ in range(7))
    return f"+55{ddd}{numero}"


# ---------------------------------------------------------------------------
# Guardas: o que o gerador nunca pode produzir
# ---------------------------------------------------------------------------

def tem_forma_de_cpf(valor):
    """Leiaute, secao 4.1: onze digitos, desconsiderados ponto e hifen, cujos
    dois ultimos conferem como verificadores de CPF."""
    d = re.sub(r"[.\-]", "", valor)
    if not re.fullmatch(r"\d{11}", d):
        return False
    numeros = [int(c) for c in d]
    for n in (9, 10):
        soma = sum(numeros[i] * (n + 1 - i) for i in range(n))
        digito = (soma * 10) % 11 % 10
        if digito != numeros[n]:
            return False
    return True


def guarda(registro):
    erros = []
    if tem_forma_de_cpf(registro["identificador"]):
        erros.append("identificador com forma de CPF")
    for campo in ("email_principal", "email_alternativo"):
        v = registro[campo]
        if v and not v.lower().endswith(".test"):
            erros.append(f"{campo} fora de .test")
    t = registro["telefone"]
    if t and not re.fullmatch(r"\+55[1-9]0(9\d{8}|\d{8})", t):
        erros.append("telefone fora da regra do ensaio")
    if erros:
        raise SystemExit(f"defeito do gerador em {registro['identificador']}: "
                         + "; ".join(erros))


# ---------------------------------------------------------------------------
# Geracao
# ---------------------------------------------------------------------------

def le_csv(nome):
    with open(os.path.join(CONFIGURACAO, nome + ".csv"), encoding="utf-8",
              newline="") as fh:
        return list(csv.DictReader(fh))


def distribui(rng, total, partes):
    """Divide `total` em `partes` contagens em torno da media, com variacao,
    somando exatamente o total."""
    pesos = [rng.uniform(0.8, 1.2) for _ in range(partes)]
    brutas = [total * p / sum(pesos) for p in pesos]
    contagens = [int(b) for b in brutas]
    restos = sorted(range(partes), key=lambda i: brutas[i] - contagens[i],
                    reverse=True)
    for i in restos[:total - sum(contagens)]:
        contagens[i] += 1
    return contagens


def gera(semente, quantidade, ano_inicial, anos):
    rng = random.Random(semente)
    cursos = le_csv("cursos")
    campi = [u["nome"] for u in le_csv("unidades") if u["situacao"] == "campus"]
    por_nivel = {n: [c["nome"] for c in cursos if c["nivel"] == n]
                 for n, _ in NIVEIS}

    anos_lista = []
    for ano, n in zip(range(ano_inicial, ano_inicial + anos),
                      distribui(rng, quantidade, anos)):
        anos_lista.extend([ano] * n)

    registros = []
    for i, ano in enumerate(anos_lista, start=1):
        nivel = escolhe(rng, NIVEIS)
        nome = nome_inventado(rng)
        local = parte_local(nome, i)
        dominio = escolhe(rng, DOMINIOS_PRINCIPAL)
        if rng.random() < P_DOMINIO_MAIUSCULO:
            dominio = dominio.capitalize().replace(".test", ".TEST")
        alternativo = ""
        if rng.random() < P_ALTERNATIVO:
            alternativo = f"{local}.alt@{escolhe(rng, DOMINIOS_ALTERNATIVO)}"
        registros.append({
            "identificador": f"SIN-{i:06d}",
            "nome": nome,
            "curso": rng.choice(por_nivel[nivel]),
            "nivel": nivel,
            "campus": rng.choice(campi),
            "ano_conclusao": str(ano),
            "semestre_conclusao": rng.choice(["1", "2"]),
            "email_principal": f"{local}@{dominio}",
            "email_alternativo": alternativo,
            "telefone": telefone(rng) if rng.random() < P_TELEFONE else "",
        })

    # Pares com o mesmo e-mail principal sob identificadores distintos: aceito
    # com alerta pelo leiaute (secao 5), e e o sintoma de pessoa duplicada que a
    # E19 verifica. O segundo do par recebe o endereco do primeiro.
    indices = rng.sample(range(len(registros)), PARES_COMPARTILHADOS * 2)
    for a, b in zip(indices[0::2], indices[1::2]):
        registros[b]["email_principal"] = registros[a]["email_principal"]
        if registros[b]["email_alternativo"].lower() == \
                registros[b]["email_principal"].lower():
            registros[b]["email_alternativo"] = ""

    for r in registros:
        guarda(r)
    return registros


def serializa(registros):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CAMPOS, lineterminator="\r\n")
    w.writeheader()
    w.writerows(registros)
    return buf.getvalue().encode("utf-8")


def resumo(registros, conteudo, caminho):
    """Contagens, sem reproduzir nome, endereco nem telefone."""
    def dominio(e):
        return e.split("@")[1].lower() if e else "(nenhum)"
    sem_via = sum(1 for r in registros
                  if not r["email_alternativo"] and not r["telefone"])
    principais = Counter(r["email_principal"].lower() for r in registros)
    nomes = [r["nome"] for r in registros]
    linhas = [
        f"arquivo: {os.path.relpath(caminho, RAIZ)}",
        f"sha256:  {hashlib.sha256(conteudo).hexdigest()}",
        f"registros: {len(registros)}",
        "por ano: " + ", ".join(f"{a}={n}" for a, n in sorted(
            Counter(r["ano_conclusao"] for r in registros).items())),
        "por nivel: " + ", ".join(f"{a}={n}" for a, n in sorted(
            Counter(r["nivel"] for r in registros).items())),
        "por semestre: " + ", ".join(f"{a}={n}" for a, n in sorted(
            Counter(r["semestre_conclusao"] for r in registros).items())),
        f"cursos distintos: {len({r['curso'] for r in registros})}; "
        f"campi distintos: {len({r['campus'] for r in registros})}",
        "e-mail principal por dominio: " + ", ".join(
            f"{a}={n}" for a, n in sorted(Counter(
                dominio(r["email_principal"]) for r in registros).items())),
        "e-mail alternativo por dominio: " + ", ".join(
            f"{a}={n}" for a, n in sorted(Counter(
                dominio(r["email_alternativo"]) for r in registros).items())),
        f"com telefone: {sum(1 for r in registros if r['telefone'])}",
        f"sem via alternativa (alerta): {sem_via}",
        f"principal compartilhado (alerta): "
        f"{sum(n for n in principais.values() if n > 1)} registros em "
        f"{sum(1 for n in principais.values() if n > 1)} enderecos",
        f"principal invalido com alternativo entregavel (reparo possivel): "
        f"{sum(1 for r in registros if dominio(r['email_principal']) != DOMINIO_ENTREGA and dominio(r['email_alternativo']) == DOMINIO_ENTREGA)}",
        "nomes com particula / apostrofo / hifen / ponto / acento: "
        f"{sum(1 for n in nomes if re.search(r' d(a|e|o|as|os) ', n))} / "
        f"{sum(1 for n in nomes if chr(39) in n)} / "
        f"{sum(1 for n in nomes if '-' in n)} / "
        f"{sum(1 for n in nomes if '.' in n)} / "
        f"{sum(1 for n in nomes if sem_acento(n) != n)}",
    ]
    return "\n".join(linhas)


def main():
    p = argparse.ArgumentParser(description="Gera a base sintetica (E16).")
    p.add_argument("--semente", type=int, default=SEMENTE_PADRAO)
    p.add_argument("--quantidade", type=int, default=QUANTIDADE_PADRAO)
    p.add_argument("--ano-inicial", type=int, default=ANO_INICIAL_PADRAO)
    p.add_argument("--anos", type=int, default=ANOS_PADRAO)
    p.add_argument("--saida", default=SAIDA_PADRAO)
    args = p.parse_args()

    registros = gera(args.semente, args.quantidade, args.ano_inicial, args.anos)
    conteudo = serializa(registros)
    os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
    with open(args.saida, "wb") as fh:
        fh.write(conteudo)
    print(resumo(registros, conteudo, os.path.abspath(args.saida)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
