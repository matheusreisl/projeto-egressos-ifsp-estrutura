# syntax=docker/dockerfile:1
#
# Onde as rotinas do projeto rodam.
#
# Existe por uma razao de topologia, e nao de conveniencia: o servico de correio
# fica somente na rede interna, que nao tem rota de saida e nao e alcancavel
# pelo hospedeiro. Uma rotina que precise ler a caixa de devolucoes tem,
# portanto, de rodar de dentro dessa rede. Este conteiner e esse lugar.
#
# Daqui as rotinas alcancam:
#   correio:143      IMAP, para ler devolucoes (E09)
#   limesurvey:80    API RemoteControl, para consultar e atualizar estado
#   banco:3306       banco, quando a consulta direta for necessaria
#
# Os scripts NAO ficam dentro da imagem: sao montados a partir de scripts/, no
# repositorio. Assim se editam e versionam sem reconstruir imagem, e a imagem
# nao carrega copia que possa divergir do que esta versionado.
#
# A E21 substitui o comando desta imagem pelo agendador. Ate lá ela fica de pe,
# ociosa, servindo de ponto de execucao.

FROM python:3.13-slim@sha256:7c61056e61ac89e852de05f3dc6fa51a6dd2181797bceed46aa725dd7cb2cd3b

LABEL org.opencontainers.image.title="Rotinas — projeto egressos IFSP" \
      org.opencontainers.image.description="Ponto de execucao das rotinas do projeto, dentro da rede interna"

# A biblioteca padrao do Python cobre quase tudo de que estas rotinas precisam:
# imaplib e email para a caixa de devolucoes, urllib e json para a API. Nao se
# instala dependencia que ela ja cubra.
#
# A excecao e o acesso ao banco. O parametro P8 exige contar ocorrencias de erro
# temporario por participante e por ciclo, e essa contagem precisa de tabela
# propria — a biblioteca padrao nao fala com MySQL. Entra PyMySQL, que e Python
# puro, sem extensao compilada, e fica fixado por versao.
#
# tzdata entra porque a rotina grava data e hora em registro de auditoria, e
# esses registros precisam de fuso interpretavel.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends tzdata; \
    rm -rf /var/lib/apt/lists/*; \
    pip install --no-cache-dir --root-user-action=ignore "PyMySQL==1.2.3"

# Nota, porque custa tempo a quem for conferir: `pymysql.__version__` reporta
# "2.2.8", que e a versao do protocolo de cliente MySQL que a biblioteca emula,
# e NAO a versao do pacote. A versao do pacote e a fixada acima, e e a que
# `pip show PyMySQL` mostra.

ENV TZ=America/Sao_Paulo \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /rotinas

CMD ["sleep", "infinity"]
