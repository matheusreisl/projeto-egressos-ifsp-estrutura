"""
Estrutura do instrumento, como dados.

Transcreve para a plataforma o que a especificacao decidiu:

  - os onze blocos de docs/especificacao/blocos-instrumento.md (E12), cada um
    um grupo de questoes, na ordem da secao 2 de navegacao-condicional.md (E14);
  - os 35 campos da secao 12.3 de blocos-instrumento.md (E13), com codigo,
    tipo, dominio e obrigatoriedade;
  - as regras de exibicao da secao 3 de navegacao-condicional.md (E14).

O texto das perguntas NAO e daqui: vem do projeto correlato (CLAUDE.md,
decisao 5). Cada enunciado e um marcador que nomeia o campo e o dado, para que
o instrumento seja percorrivel sem que este projeto redija conteudo tematico.
O dominio das respostas, ao contrario, e estrutura, e entra completo.

Os codigos de opcao tem no maximo cinco caracteres: e o tamanho da coluna
`lime_answers.code` na instancia (varchar(5)), conferido na E15.
"""

# ---------------------------------------------------------------------------
# Expressoes de exibicao (navegacao-condicional.md, secao 3)
# ---------------------------------------------------------------------------

# Consentimento dado. Toda pagina depois da primeira depende disto.
CONSENTIU = "CON1 == 'CONC'"

# Atividade remunerada — a condicao R da secao 2 de navegacao-condicional.md:
# SA1 inclui "trabalhando" E SA2 nao e estagiario nao remunerado nem negocio
# familiar sem remuneracao. Definida uma vez so, porque decide dois grupos.
#
# SA2 vai com o sufixo .NAOK, e isso nao e detalhe. No Expression Manager, uma
# expressao de exibicao que cita questao OCULTA retorna falso, qualquer que
# seja o resto (em_core_helper.php, conferido na E15). Sem o sufixo, quem esta
# so estudando — e por isso nao ve SA2 — teria "nao R" avaliado como falso, e o
# Bloco VI sumiria justamente para quem deve ve-lo. Com .NAOK, SA2 oculto vale
# vazio e a expressao segue a regra da especificacao.
R = ("((SA1 == 'TRA' or SA1 == 'ETR') "
     "and SA2.NAOK != 'ESTN' and SA2.NAOK != 'FAMN')")

# Nivel confirmado na pagina 2 (secao 3.3): o valor de IDA2, que acompanha o
# curso escolhido, e nunca o atributo pre-preenchido.
TEC_OU_GRAD = "(IDA2 == 'tecnico' or IDA2 == 'graduacao')"


def escala(extra=None):
    """Escala de 1 a 10 (regra geral 5 da secao 12.2): dez valores, 1 o menor
    grau e 10 o maior. Os rotulos dos extremos sao texto e vem com as
    perguntas — aqui ficam so os numeros."""
    opcoes = [(str(i), str(i)) for i in range(1, 11)]
    return opcoes + ([extra] if extra else [])


VINCULO = [
    ("ACC", "Assalariado de empresa ou organização privada com carteira assinada"),
    ("ASC", "Assalariado sem carteira assinada"),
    ("PUB", "Empregado ou servidor público"),
    ("AUT", "Autônomo"),
    ("MICR", "Microempresário"),
    ("AGR", "Proprietário agrícola"),
    ("ESTR", "Estagiário remunerado"),
    ("ESTN", "Estagiário não remunerado"),
    ("FAMN", "Em negócio familiar sem remuneração"),
]

RELACAO_AREA = [
    ("TOT", "Sim, totalmente"),
    ("PAR", "Sim, parcialmente"),
    ("NAO", "Não"),
    ("NS", "Não sei"),
]

SIM_NAO = [("S", "Sim"), ("N", "Não")]

# ---------------------------------------------------------------------------
# Grupos e campos
# ---------------------------------------------------------------------------
#
# Tipos usados, e o tipo da plataforma em que cada um se materializa:
#
#   lista        escolha unica, botoes de opcao            (L, listradio)
#   suspensa     escolha unica, lista suspensa             (!, list_dropdown)
#   multipla     escolha multipla                          (M, multiplechoice)
#   inteiro      numero inteiro                            (N, numerical)
#   texto_curto  texto com validacao                       (S, shortfreetext)
#   texto_longo  texto livre                               (T, longfreetext)
#   equacao      valor derivado, calculado na pagina       (*, equation)
#
# A lista suspensa entra onde o dominio e longo — cursos e unidades —, e e
# escolha unica do mesmo modo.
#
# Em `opcoes`, a string "config:<nome>" indica dominio de configuracao
# versionada (secao 12.2, regra 6), lido de configuracao/.

GRUPOS = [
    {
        "codigo": "CON",
        "nome": "Consentimento",
        "relevancia": "1",
        "campos": [
            {"codigo": "CON1", "dado": "manifestação sobre o termo",
             "tipo": "lista", "obrigatorio": True,
             "opcoes": [
                 ("CONC", "Concordo"),
                 ("RCONS", "Não concordo com o termo neste ciclo"),
                 ("RCONT", "Não quero mais ser contatado"),
             ]},
            {"codigo": "CON2",
             "dado": "consentimento específico para os recortes de equidade",
             "tipo": "lista", "obrigatorio": True, "relevancia": CONSENTIU,
             "opcoes": [("CONC", "Concordo"), ("NCONC", "Não concordo")]},
        ],
    },
    {
        "codigo": "IDA",
        "nome": "Identificação acadêmica",
        "relevancia": CONSENTIU,
        # Pre-preenchimento (E18): "pre_preenchido" nomeia o atributo do
        # participante que da o valor inicial. O respondente confirma ou corrige
        # dentro do dominio; a resposta guarda o confirmado, e o atributo fica com
        # o original (blocos-instrumento.md, secao 12.5). O numero do atributo
        # (ATTRIBUTE_n) vem da ordem em instrumento.py, ATRIBUTOS_QUESTIONARIO.
        "campos": [
            {"codigo": "IDA1", "dado": "curso", "tipo": "suspensa",
             "obrigatorio": True, "opcoes": "config:cursos",
             "pre_preenchido": "curso"},
            # IDA2 nao se edita: acompanha o curso, na propria pagina
            # (secao 12.3 e E18). O nivel vem do prefixo do codigo do curso,
            # que o gerador confere contra a coluna `nivel` da configuracao.
            #
            # As chaves sao obrigatorias. O atributo `equation` e TEXTO com
            # trechos de expressao, e nao expressao: sem chaves, a plataforma
            # grava literalmente "if(substr(...", e o Bloco IV nunca reconhece
            # tecnico nem graduacao. Achado no percurso da E15.
            {"codigo": "IDA2", "dado": "nível, derivado do curso",
             "tipo": "equacao",
             "equacao": ("{if(substr(IDA1, 0, 1) == 'T', 'tecnico', "
                         "if(substr(IDA1, 0, 1) == 'G', 'graduacao', "
                         "if(substr(IDA1, 0, 1) == 'P', 'pos_graduacao', '')))}")},
            {"codigo": "IDA3", "dado": "campus", "tipo": "suspensa",
             "obrigatorio": True, "opcoes": "config:unidades",
             "pre_preenchido": "campus"},
            {"codigo": "IDA4", "dado": "ano de conclusão", "tipo": "inteiro",
             "obrigatorio": True, "pre_preenchido": "ano_conclusao"},
            {"codigo": "IDA5", "dado": "semestre de conclusão", "tipo": "lista",
             "obrigatorio": True, "opcoes": [("1", "1"), ("2", "2")],
             "pre_preenchido": "semestre_conclusao"},
        ],
    },
    {
        "codigo": "AF",
        "nome": "Bloco I — Avaliação da Formação",
        "relevancia": CONSENTIU,
        "campos": [
            {"codigo": "AF1", "dado": "satisfação com a formação recebida no IFSP",
             "tipo": "lista", "opcoes": escala()},
            {"codigo": "AF2",
             "dado": "situação profissional atual comparada à do ingresso",
             "tipo": "lista",
             "opcoes": [("MEL", "Melhor"), ("IGU", "Igual"), ("PIO", "Pior")]},
            {"codigo": "AF3",
             "dado": "contribuição do curso para a situação de trabalho atual",
             "tipo": "lista", "opcoes": escala()},
            {"codigo": "AF4", "dado": "sugestões para a melhoria do curso",
             "tipo": "texto_longo", "max_caracteres": 1000},
        ],
    },
    {
        "codigo": "AP",
        "nome": "Bloco II — Atividade Profissional Anterior",
        "relevancia": CONSENTIU,
        "campos": [
            {"codigo": "AP1", "dado": "trabalhava quando entrou no curso",
             "tipo": "lista", "opcoes": SIM_NAO},
            {"codigo": "AP2", "dado": "vínculo quando entrou no curso",
             "tipo": "lista", "relevancia": "AP1 == 'S'", "opcoes": VINCULO},
        ],
    },
    {
        "codigo": "SA",
        "nome": "Bloco III — Situação Atual",
        "relevancia": CONSENTIU,
        "campos": [
            {"codigo": "SA1", "dado": "situação atual", "tipo": "lista",
             "obrigatorio": True,
             "opcoes": [
                 ("EST", "Estudando"),
                 ("TRA", "Trabalhando"),
                 ("ETR", "Estudando e trabalhando"),
                 ("NEN", "Nem trabalhando, nem estudando"),
             ]},
            {"codigo": "SA2", "dado": "vínculo de trabalho atual",
             "tipo": "lista", "obrigatorio": True,
             "relevancia": "SA1 == 'TRA' or SA1 == 'ETR'", "opcoes": VINCULO},
        ],
    },
    {
        "codigo": "EF",
        "nome": "Bloco IV — Evolução na Formação",
        "relevancia": CONSENTIU,
        "campos": [
            {"codigo": "EF1",
             "dado": "situação no nível seguinte ao do curso concluído",
             "tipo": "lista", "relevancia": TEC_OU_GRAD,
             "opcoes": [("CON", "Concluí"), ("MAT", "Estou matriculado"),
                        ("NAO", "Não")]},
            {"codigo": "EF2", "dado": "instituição desse curso", "tipo": "lista",
             "relevancia": f"{TEC_OU_GRAD} and (EF1 == 'CON' or EF1 == 'MAT')",
             "opcoes": [("IFSP", "IFSP"), ("OUT", "Outra instituição")]},
            {"codigo": "EF3", "dado": "esse curso é na mesma área de formação",
             "tipo": "lista",
             "relevancia": f"{TEC_OU_GRAD} and (EF1 == 'CON' or EF1 == 'MAT')",
             "opcoes": RELACAO_AREA},
            {"codigo": "EF4", "dado": "demandas de formação", "tipo": "multipla",
             "exclusiva": "NEN",
             "opcoes": [
                 ("TEC", "Curso técnico"),
                 ("GRA", "Graduação"),
                 ("ESP", "Especialização"),
                 ("MD", "Mestrado ou doutorado"),
                 ("EXT", "Curso de extensão ou de curta duração"),
                 ("NEN", "Nenhuma no momento"),
             ]},
        ],
    },
    {
        "codigo": "PM",
        "nome": "Bloco V — Perfil do Egresso no Mercado de Trabalho",
        "relevancia": f"{CONSENTIU} and {R}",
        "campos": [
            {"codigo": "PM1", "dado": "relação da atividade com a área de formação",
             "tipo": "lista", "obrigatorio": True, "opcoes": RELACAO_AREA},
            {"codigo": "PM2",
             "dado": "afinidade entre as atividades e o conteúdo do curso",
             "tipo": "lista", "obrigatorio": True, "opcoes": escala()},
            {"codigo": "PM3", "dado": "remuneração bruta mensal", "tipo": "lista",
             "opcoes": "config:faixas-rendimento"},
            {"codigo": "PM4", "dado": "satisfação com a remuneração",
             "tipo": "lista", "opcoes": escala()},
            {"codigo": "PM5", "dado": "satisfação com a atividade profissional",
             "tipo": "lista", "opcoes": escala()},
            {"codigo": "PM6", "dado": "setor de atividade", "tipo": "lista",
             "opcoes": [
                 ("IND", "Indústria"),
                 ("COM", "Comércio"),
                 ("TRA", "Transportes"),
                 ("CON", "Construção civil"),
                 ("AGR", "Agricultura e pecuária"),
                 ("SOC", "Serviços sociais (saúde, educação, assistência)"),
                 ("FIN", "Serviços financeiros"),
                 ("UTI", "Serviços de utilidade pública (água, energia, "
                         "saneamento, limpeza urbana)"),
                 ("SER", "Demais serviços"),
                 ("OUT", "Outro"),
             ]},
        ],
    },
    {
        "codigo": "MI",
        "nome": "Bloco VI — Motivos da Não Inserção no Mercado de Trabalho",
        "relevancia": f"{CONSENTIU} and !{R}",
        "campos": [
            {"codigo": "MI1",
             "dado": "principal motivo de não exercer atividade remunerada",
             "tipo": "lista",
             "opcoes": [
                 ("EST", "Decidi só estudar"),
                 ("SAL", "Os salários oferecidos são baixos"),
                 ("OFE", "Há pouca oferta de trabalho na região onde moro"),
                 ("ARE", "Não encontrei trabalho na área do curso realizado no IFSP"),
                 ("QUA", "Não tenho a qualificação exigida"),
                 ("EXP", "Não tenho a experiência exigida"),
                 ("PES", "Motivos pessoais"),
                 ("OUT", "Outro"),
             ]},
        ],
    },
    {
        "codigo": "AV",
        "nome": "Bloco VII — Avaliação da PAEG",
        "relevancia": CONSENTIU,
        "campos": [
            {"codigo": "AV1",
             "dado": "avaliação das ações do programa de acompanhamento",
             "tipo": "lista",
             "opcoes": escala(("NC", "Não conheço as ações do programa"))},
        ],
    },
    {
        "codigo": "EQ",
        "nome": "Recortes de equidade",
        "relevancia": f"{CONSENTIU} and CON2 == 'CONC'",
        "campos": [
            {"codigo": "EQ1", "dado": "gênero", "tipo": "lista",
             "opcoes": [
                 ("MUL", "Mulher"),
                 ("HOM", "Homem"),
                 ("NB", "Pessoa não binária"),
                 ("OUT", "Outra identidade"),
                 ("PND", "Prefiro não declarar"),
             ]},
            {"codigo": "EQ2", "dado": "raça/cor", "tipo": "lista",
             "opcoes": [
                 ("PRE", "Preta"),
                 ("PAR", "Parda"),
                 ("IND", "Indígena"),
                 ("AMA", "Amarela"),
                 ("BRA", "Branca"),
                 ("PND", "Prefiro não declarar"),
             ]},
            {"codigo": "EQ3", "dado": "pessoa com deficiência", "tipo": "lista",
             "opcoes": [("S", "Sim"), ("N", "Não"),
                        ("PND", "Prefiro não declarar")]},
            {"codigo": "EQ4",
             "dado": "avaliação das políticas de ações afirmativas",
             "tipo": "lista",
             "opcoes": escala(("NC", "Não conheço as políticas"))},
        ],
    },
    {
        "codigo": "CT",
        "nome": "Contato e manifestações",
        "relevancia": CONSENTIU,
        "campos": [
            {"codigo": "CT1", "dado": "e-mail principal atualizado",
             "tipo": "texto_curto", "validacao": "email"},
            {"codigo": "CT2", "dado": "e-mail alternativo atualizado",
             "tipo": "texto_curto", "validacao": "email",
             # Diferente do principal, sem distincao de caixa (leiaute, 4.6).
             "validacao_em": ("is_empty(CT2) or is_empty(CT1) or "
                              "strtolower(CT2) != strtolower(CT1)"),
             "validacao_em_dica": "O e-mail alternativo precisa ser diferente "
                                  "do principal."},
            {"codigo": "CT3", "dado": "telefone atualizado",
             "tipo": "texto_curto", "validacao": "telefone"},
            # Caixa de marcacao: escolha multipla com uma so opcao. O campo
            # gravado e CT4_RECT, marcado 'Y'.
            {"codigo": "CT4",
             "dado": "não quero mais ser contatado nos próximos ciclos",
             "tipo": "multipla",
             "opcoes": [("RECT", "Não quero mais ser contatado nos próximos ciclos")]},
        ],
    },
]

# ---------------------------------------------------------------------------
# Validacoes de contato no modo de ensaio (leiaute-entrada.md, secoes 4.6, 4.7
# e 7)
# ---------------------------------------------------------------------------
#
# A plataforma aplica a expressao no servidor (PHP) e no navegador
# (JavaScript), entao ela usa so o que os dois dialetos tem em comum. Os
# caracteres especiais do dot-atom que confundiriam o delimitador ou o
# Expression Manager — barra e chaves — vao como escape hexadecimal.
#
# MODO DE ENSAIO: o dominio precisa estar sob .test, e o telefone precisa ser
# +55 com codigo de area terminado em 0. Numa implantacao real, estas duas
# expressoes mudam — e ponto do guia (E30).

_ATEXT = r"[A-Za-z0-9!#$%&'*+\x2f=?^_`\x7b|\x7d~-]"
_LOCAL = rf"{_ATEXT}+(\.{_ATEXT}+)*"
_DOMINIO_ENSAIO = r"([A-Za-z0-9-]+\.)+[Tt][Ee][Ss][Tt]"

VALIDACOES = {
    "email": {
        "preg": rf"/^(?=[^@]{{1,64}}@)(?=.{{3,254}}$){_LOCAL}@{_DOMINIO_ENSAIO}$/",
        "max_caracteres": 254,
    },
    "telefone": {
        "preg": r"/^\+55[1-9]0(9[0-9]{8}|[0-9]{8})$/",
        "max_caracteres": 16,
    },
}
