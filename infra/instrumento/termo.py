"""
Termo de consentimento do instrumento (E22): o texto do termo, o consentimento
especifico do dado sensivel, o encerramento e a versao que fica gravada em cada
resposta.

Fonte unica, como mensagens.py: o instrumento.py poe os textos no .lss, e duas
equacoes ocultas da pagina 1 gravam em cada resposta a versao do termo (CONV) e
o momento da manifestacao (CONDH). A especificacao esta em
docs/especificacao/consentimento.md.

VERSAO DE ENSAIO. O texto segue os elementos do art. 9 da LGPD e diz o que o
mecanismo faz, conforme as especificacoes do projeto. Os contatos do
encarregado e o prazo de guarda sao marcadores: o primeiro e da instituicao; o
segundo, da E23. Antes de qualquer uso com egressos reais, o termo precisa ser
validado pelo encarregado de dados do IFSP. A base legal adotada para as
respostas — consentimento — e decisao do projeto, e nao conclusao da lei
(fichamento da LGPD, limitacoes).

O texto e operacional e informativo. Nao trata do conteudo tematico das
perguntas, que nao e deste projeto (CLAUDE.md, decisao 5).

Versionamento. VERSAO nomeia o texto. A resposta grava "VERSAO sha256:<resumo>",
e o resumo e o do DOCUMENTO DA PAGINA 1 — o termo, as opcoes de CON1, o texto e
as opcoes de CON2, tudo o que o respondente ve antes de se manifestar. Cada
versao fica arquivada, imutavel, em termos/<VERSAO>.html: o gerador recusa a
mesma VERSAO com documento diferente, e mudar o texto exige VERSAO nova. E esse
arquivo que torna o aceite recuperavel — a resposta diz qual versao, e o resumo
prova que o texto arquivado e o que foi mostrado.

Restricao de forma, a mesma de mensagens.py: o encerramento tem ramos em
expressao if() do Expression Manager, com os textos entre aspas duplas. Por isso
o HTML deles nao tem atributo nem aspas duplas retas.
"""

import hashlib
import html
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(AQUI, "termos")

VERSAO = "ensaio-1"

# Marcadores do que a instituicao, ou outra etapa, preenche. Ficam visiveis no
# texto de proposito: um termo com lacuna disfarcada seria pior que um termo
# com lacuna declarada.
ENCARREGADO = "[nome e contato do encarregado de dados do IFSP — a preencher " \
              "pela instituição]"
PRAZO_DE_GUARDA = "[prazo definido na política de retenção do programa — E23]"

# --- Pagina 1: o termo (enunciado de CON1) ------------------------------------

TEXTO_TERMO = "\n".join([
    "<p><strong>Termo de consentimento — Acompanhamento de Egressos do IFSP"
    "</strong></p>",
    "<p><em>Versão de ensaio, sujeita à validação do encarregado de dados do "
    "IFSP antes de qualquer uso com egressos reais.</em></p>",

    "<p><strong>Para que serve.</strong> O Instituto Federal de Educação, "
    "Ciência e Tecnologia de São Paulo (IFSP) acompanha a trajetória de quem "
    "concluiu seus cursos, conforme o Regulamento do Programa de Acompanhamento "
    "de Egressos (Portaria Normativa nº 128/2025). As suas respostas servem para "
    "calcular os indicadores do programa e para avaliar e planejar os cursos. "
    "Não são usadas para nenhuma outra finalidade.</p>",

    "<p><strong>Que dados são tratados.</strong> Do registro acadêmico: nome, "
    "endereço eletrônico e telefone de contato, curso, nível, campus, ano e "
    "semestre de conclusão — usados para enviar o convite e os lembretes e para "
    "vir preenchidos na página seguinte. Deste questionário: a sua manifestação "
    "sobre este termo, com data, hora e versão do texto, e as suas respostas, "
    "inclusive as correções que você fizer nos dados acadêmicos e de contato. "
    "Gênero, raça/cor e deficiência só são perguntados se você der o "
    "consentimento específico mais abaixo. Não registramos se você abriu as "
    "mensagens, nem o endereço de rede do seu acesso.</p>",

    "<p><strong>Como e por quanto tempo.</strong> Os dados ficam numa instalação "
    "própria do IFSP, com acesso restrito à equipe do programa, e não são "
    "compartilhados com terceiros. Os resultados são divulgados apenas de forma "
    f"agregada, sem identificar quem respondeu. Prazo de guarda: "
    f"{PRAZO_DE_GUARDA}.</p>",

    "<p><strong>Quem responde pelo tratamento.</strong> O IFSP é o controlador "
    f"dos dados. Encarregado: {ENCARREGADO}.</p>",

    "<p><strong>Seus direitos.</strong> Você pode confirmar se há tratamento dos "
    "seus dados, acessá-los, corrigi-los, pedir a eliminação, saber com quem são "
    "compartilhados e revogar este consentimento a qualquer momento (LGPD, art. "
    "18). Os dados acadêmicos e de contato podem ser corrigidos neste próprio "
    "questionário; para o restante, fale com o encarregado.</p>",

    "<p><strong>Se você não concordar.</strong> Há duas formas de recusa, com "
    "efeitos diferentes:</p>",
    "<ul>",
    "<li><strong>Não concordo com o termo neste ciclo:</strong> você não "
    "responde ao questionário e não recebe mais lembretes deste convite. No "
    "próximo ano, receberá um novo convite.</li>",
    "<li><strong>Não quero mais ser contatado:</strong> você não responde ao "
    "questionário e não recebe mais nenhuma mensagem do acompanhamento de "
    "egressos, neste nem nos próximos anos. Se mudar de ideia, basta responder a "
    "uma das mensagens que recebeu.</li>",
    "</ul>",
    "<p>Nas duas, fica registrada apenas a sua manifestação, com data, hora e "
    "versão deste termo — e nenhuma outra resposta. Recusar não traz nenhuma "
    "outra consequência. Se você concordar e depois "
    "mudar de ideia, volte a esta página e escolha uma das recusas: o que você "
    "tiver respondido é descartado.</p>",

    "<p><strong>Você concorda com o tratamento dos seus dados nos termos acima?"
    "</strong></p>",
])

# --- Pagina 1: o consentimento especifico (enunciado de CON2) -----------------
#
# LGPD, art. 11, I: dado sensivel por consentimento so "de forma especifica e
# destacada, para finalidades especificas". Por isso e manifestacao propria, com
# texto proprio, e nao clausula do termo geral (blocos-instrumento.md, 3.1).

TEXTO_CON2 = "\n".join([
    "<p><strong>Consentimento específico para dados sensíveis</strong></p>",
    "<p>No fim do questionário há um bloco opcional sobre gênero, raça/cor e "
    "deficiência, e sobre a sua percepção das ações afirmativas do IFSP. "
    "Raça/cor e deficiência são dados pessoais sensíveis (LGPD, art. 5º, II). "
    "Eles servem só para verificar se os resultados dos egressos diferem entre "
    "grupos — por exemplo, se a inserção no trabalho é desigual — e são "
    "divulgados apenas de forma agregada. Cada pergunta do bloco tem a opção "
    "“prefiro não declarar”.</p>",
    "<p>Se você não concordar, o bloco não é exibido e o restante do "
    "questionário segue normalmente. Se concordar e depois mudar de ideia, volte "
    "a esta página antes de enviar: as respostas do bloco são descartadas.</p>",
    "<p><strong>Você concorda com o tratamento desses dados para essa "
    "finalidade?</strong></p>",
])

# --- Encerramento ---------------------------------------------------------------
#
# Tres ramos, pelo CON1 (navegacao-condicional.md, secao 4): quem concluiu, quem
# recusou o termo neste ciclo e quem recusou contato.

_FIM_CONCORDO = (
    "<p><strong>Obrigado por responder.</strong></p>"
    "<p>As suas respostas foram registradas. No próximo ano, você receberá um "
    "novo convite para o questionário anual.</p>")

_FIM_RECUSA_CICLO = (
    "<p><strong>A sua manifestação foi registrada.</strong></p>"
    "<p>Você não concordou com o termo neste ciclo, e nenhuma resposta foi "
    "coletada. Você não receberá mais lembretes deste convite. No próximo ano, "
    "receberá um novo convite.</p>")

_FIM_RECUSA_CONTATO = (
    "<p><strong>A sua manifestação foi registrada.</strong></p>"
    "<p>Nenhuma resposta foi coletada, e você não receberá mais mensagens do "
    "acompanhamento de egressos do IFSP, neste nem nos próximos anos. Se mudar "
    "de ideia, basta responder a uma das mensagens que recebeu.</p>")

ENCERRAMENTO = (
    '{if(CON1 == "RCONT", "' + _FIM_RECUSA_CONTATO + '", if(CON1 == "RCONS", "'
    + _FIM_RECUSA_CICLO + '", "' + _FIM_CONCORDO + '"))}')

# --- Metadados gravados em cada resposta ----------------------------------------
#
# Duas equacoes ocultas, sempre relevantes — para que a recusa, que descarta o
# resto do preenchimento, as mantenha. A plataforma recalcula equacao relevante
# no servidor, a cada envio da pagina, e grava o resultado (em_manager_helper,
# conferido na E22); no modo de uma pagina por vez, o envio de outra pagina nao
# recalcula as da pagina 1.
#
#   CONV   a versao e o resumo do documento da pagina 1. Texto literal, sem
#          chaves: a plataforma grava o texto como esta.
#   CONDH  o momento da manifestacao, em ISO 8601 com o deslocamento do fuso
#          (date('c')). A plataforma roda em UTC — o LimeSurvey o fixa em
#          application/config/internal.php —, e por isso o valor sai com
#          +00:00, explicito: sem ambiguidade, ao contrario das datas da
#          resposta, que tambem estao em UTC mas nao o dizem. Vazio enquanto
#          CON1 nao for respondido. Se o respondente voltar a pagina 1 e
#          reenvia-la, passa a ser o momento da ultima manifestacao.

EQUACAO_CONDH = "{if(is_empty(CON1), '', date('c'))}"


def _opcoes(opcoes):
    return "<ul>\n" + "\n".join(
        f"<li>{html.escape(rotulo, quote=False)}</li>" for _, rotulo in opcoes
    ) + "\n</ul>"


def documento(opcoes_con1, opcoes_con2):
    """O documento da pagina 1, canonico: tudo o que o respondente ve antes de
    se manifestar. E o que se arquiva e o que se resume."""
    return "\n".join([
        f"<!-- termo de consentimento, versao {VERSAO} -->",
        TEXTO_TERMO,
        _opcoes(opcoes_con1),
        TEXTO_CON2,
        _opcoes(opcoes_con2),
    ]) + "\n"


def resumo(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def identificacao(texto):
    """O valor que CONV grava: versao e resumo do documento."""
    return f"{VERSAO} sha256:{resumo(texto)}"


def caminho_do_arquivo(versao=VERSAO):
    return os.path.join(ARQUIVO, f"{versao}.html")


def arquiva(texto):
    """Garante o arquivo da versao. Escreve se nao existir; se existir com
    documento diferente, recusa — mudar o texto exige VERSAO nova. Devolve o
    caminho."""
    caminho = caminho_do_arquivo()
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8", newline="") as fh:
            if fh.read() != texto:
                raise ValueError(
                    f"o termo mudou e a versao continua {VERSAO}: arquive o "
                    "texto novo com VERSAO nova em termo.py; o arquivo de uma "
                    "versao nao se reescreve")
        return caminho
    os.makedirs(ARQUIVO, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        fh.write(texto)
    return caminho


def le_arquivado(versao):
    """O documento arquivado de uma versao, ou None."""
    caminho = caminho_do_arquivo(versao)
    if not os.path.exists(caminho):
        return None
    with open(caminho, encoding="utf-8", newline="") as fh:
        return fh.read()
