"""
Modelos de mensagem do instrumento: convite e lembrete, com remetente e assunto
padronizados (E20).

A especificacao esta em docs/especificacao/modelos-mensagem.md, que decorre do
P7, do P6 e da secao 4.1 de parametros-contato.md. Aqui ficam os textos e as
propriedades do questionario que os acompanham, num lugar so: o instrumento.py
os poe no .lss e os aplica a instancia, e o confere-mensagens.py confere a
instancia contra este arquivo.

O texto e operacional — convite, acesso, retomada, recusa. Nao trata do
conteudo tematico das perguntas, que nao e deste projeto (CLAUDE.md, decisao 5).

Marcadores da plataforma, conferidos no codigo do LimeMailer do LimeSurvey 7:

  {FIRSTNAME}        o `nome` inteiro do leiaute — nome de tratamento, ja
                     social quando houver registro (E11); `lastname` e vazio
  {SURVEYURL}        o endereco individual, com o token
  {GLOBALOPTOUTURL}  recusa de contato: poe o participante na lista de bloqueio
                     da base central, que vale para todos os questionarios e
                     ciclos — e nao so para este, como {OPTOUTURL} (P6)

O corpo passa pelo Expression Manager antes do envio, e e isso que permite o
lembrete ter dois ramos num modelo so (secao 4.1 do P2): o ramo sai do atributo
`variante_lembrete` do participante, que a rotina da E21 grava imediatamente
antes de cada disparo.
"""

# --- Remetente --------------------------------------------------------------
#
# Valores de ENSAIO, sob o dominio controlado pelo projeto (secao 9.1 do P7).
# O remetente institucional identificavel e especificacao de implantacao real,
# e entra pelo guia de replicacao (E30), nao aqui. Precisam casar com o .env:
# <CORREIO_CAIXA_REMETENTE>@<CORREIO_DOMINIO> e <CORREIO_CAIXA_DEVOLUCOES>@...
# — o confere-mensagens.py confere.
#
# O remetente nao e "naoresponda": o P7 veda remetente sem retorno, e a resposta
# humana chega a caixa propria do remetente no correio de ensaio. A devolucao
# vai para outro endereco (Return-Path), lido pela rotina da E09.

REMETENTE_NOME = "Acompanhamento de Egressos do IFSP (ensaio)"
REMETENTE = "acompanhamento@egressos.test"
DEVOLUCOES = "devolucoes@egressos.test"

# --- Atributo que escolhe o ramo do lembrete --------------------------------
#
# Nao e estado do participante: e parametro do disparo, sobrescrito a cada
# lembrete. O estado continua derivado da conclusao e de CON1 (secao 12 do P5;
# E14). Vazio ou qualquer outro valor cai no ramo de quem nao iniciou.

ATRIBUTO_VARIANTE = "variante_lembrete"
VARIANTE_CONVIDADO = "convidado"
VARIANTE_EM_PREENCHIMENTO = "em_preenchimento"

# --- Assuntos ---------------------------------------------------------------
#
# Padronizados e estaveis entre ciclos (P7): sem ano, sem numero do lembrete,
# com a instituicao nomeada no inicio. E o que permite ao egresso reconhecer
# no segundo ano a mensagem que recebeu no primeiro.

ASSUNTO_CONVITE = ("IFSP — Acompanhamento de Egressos: convite para o "
                   "questionário anual")
ASSUNTO_LEMBRETE = ("IFSP — Acompanhamento de Egressos: lembrete do "
                    "questionário anual")

# --- Partes comuns ----------------------------------------------------------

_SAUDACAO = "<p>Olá, {FIRSTNAME}.</p>"

_ENDERECO = (
    "<p>Este é o seu endereço de acesso. Ele é individual: por favor, não o "
    "repasse a outras pessoas.<br>\n{SURVEYURL}</p>")

_IDENTIFICACAO = (
    "<p>Os dados do seu curso, do campus e do ano e semestre de conclusão já "
    "vêm preenchidos. Basta confirmá-los ou, se houver erro, corrigi-los.</p>")

_RECUSA = (
    "<p>Se você não quiser mais receber mensagens do acompanhamento de "
    "egressos, use este endereço:<br>\n{GLOBALOPTOUTURL}<br>\n"
    "A recusa vale também para os próximos anos. Se mudar de ideia, basta "
    "responder a esta mensagem.</p>")

_ASSINATURA = (
    "<p>Dúvidas podem ser enviadas em resposta a esta mensagem.</p>\n"
    "<p>Programa de Acompanhamento de Egressos<br>\n"
    "Instituto Federal de Educação, Ciência e Tecnologia de São Paulo "
    "(IFSP)</p>")

# --- Convite ----------------------------------------------------------------

CORPO_CONVITE = "\n".join([
    _SAUDACAO,
    "<p>O Instituto Federal de São Paulo acompanha a trajetória de quem "
    "concluiu seus cursos. Convidamos você a responder ao questionário anual "
    "de acompanhamento de egressos. As respostas orientam a avaliação dos "
    "cursos e o planejamento da instituição.</p>",
    _ENDERECO,
    _IDENTIFICACAO,
    "<p>A primeira página apresenta o termo de consentimento. Durante o "
    "preenchimento, você pode usar a opção “Retomar mais tarde” para salvar o "
    "que já respondeu e continuar depois.</p>",
    # A contrapartida que o IFSP ja anuncia, e so ela (P7; quadro, linha E5).
    "<p>Quem concluiu um curso no IFSP pode também participar das ações que a "
    "instituição oferece aos egressos: educação continuada, integração "
    "acadêmica e colaboração voluntária.</p>",
    _RECUSA,
    _ASSINATURA,
])

# --- Lembrete ---------------------------------------------------------------
#
# Dois ramos (secao 4.1 do P2): quem nao iniciou recebe pedido de primeira
# resposta; quem iniciou recebe instrucao de retomada. O ramo e uma expressao
# if() do Expression Manager; os textos entram como cadeias entre aspas
# duplas, e por isso nao podem conter aspas duplas retas — as citacoes de
# botao usam aspas tipograficas.

_RAMO_CONVIDADO = (
    "<p>Há alguns dias enviamos o convite para o questionário anual de "
    "acompanhamento de egressos do IFSP, e ainda não recebemos a sua "
    "resposta. A sua participação é importante para a avaliação dos cursos e "
    "o planejamento da instituição.</p>")

# Retomada (E14, E15): reabrir o endereco sem carregar o salvo comeca outro
# preenchimento, e senha esquecida nao se recupera.
_RAMO_EM_PREENCHIMENTO = (
    "<p>Você começou a responder ao questionário anual de acompanhamento de "
    "egressos do IFSP, e o preenchimento ainda não foi concluído.</p>"
    "<p>Para continuar de onde parou, abra o endereço abaixo e use a opção "
    "“Carregar questionário não finalizado”, informando o nome e a senha que "
    "você escolheu ao salvar. Atenção: abrir o endereço e responder sem "
    "carregar o que foi salvo começa um novo preenchimento, desde o início.</p>"
    "<p>Se você não salvou o preenchimento ou não se lembra da senha, não é "
    "possível recuperar as respostas anteriores: basta responder novamente, "
    "desde o início.</p>")

CORPO_LEMBRETE = "\n".join([
    _SAUDACAO,
    '{if(TOKEN:ATTRIBUTE_%(n)s == "' + VARIANTE_EM_PREENCHIMENTO + '", "'
    + _RAMO_EM_PREENCHIMENTO + '", "' + _RAMO_CONVIDADO + '")}',
    _ENDERECO,
    _IDENTIFICACAO,
    _RECUSA,
    _ASSINATURA,
])


def corpo_lembrete(numero_atributo):
    """O lembrete com o numero do atributo `variante_lembrete` resolvido. O
    numero vem de instrumento.coluna_do_atributo, o mesmo calculo que cria a
    coluna — a ligacao vive num lugar so, como no pre-preenchimento (E18)."""
    return CORPO_LEMBRETE % {"n": numero_atributo}


def propriedades_de_idioma(numero_atributo):
    """Campos de surveys_languagesettings que levam os modelos."""
    return {
        "surveyls_email_invite_subj": ASSUNTO_CONVITE,
        "surveyls_email_invite": CORPO_CONVITE,
        "surveyls_email_remind_subj": ASSUNTO_LEMBRETE,
        "surveyls_email_remind": corpo_lembrete(numero_atributo),
    }


def propriedades_do_questionario():
    """Campos de surveys que definem remetente e retorno das mensagens do
    questionario. Tem precedencia sobre o remetente do sitio (LimeMailer,
    setSurvey) — conferido no codigo."""
    return {
        "admin": REMETENTE_NOME,
        "adminemail": REMETENTE,
        "bounce_email": DEVOLUCOES,
    }
