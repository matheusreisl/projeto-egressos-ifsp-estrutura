# syntax=docker/dockerfile:1
#
# Servico de correio do ambiente de ensaio.
#
# NAO e um capturador de SMTP. A distincao e a razao de este servico existir:
# capturadores de uso corrente em desenvolvimento aceitam toda mensagem e nunca
# devolvem erro, o que satisfaz "vi a mensagem chegar" e NAO satisfaz o
# parametro P8, que exige ler e classificar a devolucao. Aqui roda um MTA de
# verdade (Postfix), que devolve, mais um servidor IMAP (Dovecot), para que a
# rotina de leitura converse com a caixa do mesmo modo que conversaria com uma
# caixa institucional numa implantacao real.
#
# Contencao: este servico fica SOMENTE na rede interna da composicao, que nao
# tem rota de saida. Mensagem nenhuma sai da maquina, qualquer que seja o
# endereco de destino — inclusive um endereco real digitado por engano. E o que
# sustenta o criterio K6 da ADR-0002.
#
# Tres dominios, cada um produzindo uma linha da tabela de classificacao do P8:
#
#   <DOMINIO>              entrega normal, na caixa coletora
#   <DOMINIO_INVALIDO>     devolucao PERMANENTE (5.x.x) — usuario inexistente
#   <DOMINIO_INDISPONIVEL> devolucao TEMPORARIA (4.x.x) — servidor inalcancavel
#
# Todos sob o TLD reservado .test (RFC 2606 / 6761), que nao resolve na internet
# publica e nao pode colidir com dominio de terceiro.

FROM debian:13-slim@sha256:a99cfc517144bc59b1978475ec53b46ecabec7e43635402ee5b77cc54cd1b20a

LABEL org.opencontainers.image.title="Correio de ensaio — projeto egressos IFSP" \
      org.opencontainers.image.description="Postfix e Dovecot em rede fechada, para exercitar envio e devolucao"

ENV DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        postfix \
        postfix-pcre \
        dovecot-imapd \
        dovecot-core \
        ca-certificates \
        procps \
        netcat-openbsd; \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# 25  SMTP, para o LimeSurvey entregar
# 143 IMAP, para a rotina de leitura de devolucoes
EXPOSE 25 143

# A verificacao de saude faz LOGIN de verdade no IMAP, e nao apenas abre a porta.
# A razao esta comentada em entrypoint.sh, na funcao sonda_imap: ja se observou o
# servico com a porta aberta e recusando toda sessao de rede.
HEALTHCHECK --interval=30s --timeout=15s --start-period=30s --retries=4 \
    CMD nc -z localhost 25 \
        && printf 'a LOGIN %s %s\r\na LOGOUT\r\n' "$CAIXA_DEVOLUCOES" "$SENHA_CAIXA" \
           | nc -w 5 localhost 143 | grep -q '^a OK' \
        || exit 1

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
