# syntax=docker/dockerfile:1
#
# Imagem propria do LimeSurvey para o mecanismo de acompanhamento de egressos.
#
# Por que imagem propria, e nao uma imagem comunitaria: ver ADR-0004. Em resumo,
# nao existe imagem publicada pelo projeto LimeSurvey, e este arquivo e, ele
# mesmo, o procedimento de instalacao — executavel, versionado e conferivel,
# que e o entregavel da etapa E10.
#
# Tres fixacoes deliberadas, exigidas pela ADR-0002:
#   1. a imagem base e fixada por digest, nao por rotulo movel;
#   2. o pacote do LimeSurvey e fixado por versao E por soma de verificacao;
#   3. nada e baixado de fonte que nao seja a oficial.
#
# Para atualizar a versao do LimeSurvey, ver infra/README.md.

# Debian 13 (trixie), PHP 8.3.33.
# Sobre a escolha de PHP 8.3 e a ausencia da extensao imap, ver ADR-0004.
FROM php:8.3-apache@sha256:257dcf070787a1ffc782d90bd589297b63a007064d024cdfb6d30464836ded56

ARG LIMESURVEY_VERSAO="7.2.0+260921"
ARG LIMESURVEY_URL="https://download.limesurvey.org/latest-master/limesurvey7.2.0%2B260921.zip"
ARG LIMESURVEY_SHA256="4300ae529f893b8079bbb6a31721d2628ea436106b2e67f67a0f46a0829bc728"

LABEL org.opencontainers.image.title="LimeSurvey — projeto egressos IFSP" \
      org.opencontainers.image.description="Instancia de prova de conceito para acompanhamento de egressos" \
      org.opencontainers.image.version="${LIMESURVEY_VERSAO}" \
      org.opencontainers.image.licenses="GPL-2.0-or-later" \
      org.opencontainers.image.source="https://github.com/matheusreisl/projeto-egressos-ifsp-estrutura"

# ---------------------------------------------------------------------------
# 1. Extensoes do PHP
# ---------------------------------------------------------------------------
#
# Ja presentes na imagem base: curl, iconv, json, mbstring, sodium, zlib.
#
# Acrescentadas aqui, com a finalidade de cada uma segundo o manual do
# LimeSurvey:
#   gd        captcha, graficos de estatistica e envio de imagens
#   zip       importacao e exportacao de modelos e recursos
#   intl      internacionalizacao
#   ldap      importacao de participantes por diretorio (uso institucional)
#   pdo_mysql acesso ao banco
#   opcache   desempenho
#
# NAO se instala a extensao imap. Ela seria o caminho nativo de leitura de
# devolucoes de e-mail, mas depende da biblioteca UW-IMAP, que o Debian removeu
# por falta de manutencao, e foi retirada do nucleo do PHP na versao 8.4. A
# leitura de devolucoes do parametro P8 e feita por rotina propria. Ver ADR-0004.
#
# Os pacotes -dev sao mantidos na imagem final de proposito. Purga-los reduziria
# o tamanho em algumas centenas de megabytes ao custo de um bloco de apt-mark
# dificil de ler e facil de errar. Como esta imagem e, antes de tudo, um
# documento de instalacao destinado a ser lido e replicado, a legibilidade
# prevalece sobre o tamanho. Numa implantacao real, o ajuste e legitimo.

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        libfreetype-dev \
        libjpeg62-turbo-dev \
        libpng-dev \
        libwebp-dev \
        libzip-dev \
        libicu-dev \
        libldap2-dev \
        unzip; \
    docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp; \
    docker-php-ext-install -j"$(nproc)" \
        gd \
        zip \
        intl \
        ldap \
        pdo_mysql \
        opcache; \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# 2. Ajustes do PHP
# ---------------------------------------------------------------------------
#
# Os limites abaixo atendem a importacao da base de participantes e a exportacao
# de resultados. O fuso horario e fixado para que os registros de data e hora da
# trilha de auditoria (E23) e a cadencia de disparo (E21) sejam interpretaveis
# sem ambiguidade.

RUN { \
        echo 'memory_limit = 512M'; \
        echo 'max_execution_time = 300'; \
        echo 'upload_max_filesize = 64M'; \
        echo 'post_max_size = 64M'; \
        echo 'max_input_vars = 5000'; \
        echo 'date.timezone = America/Sao_Paulo'; \
    } > /usr/local/etc/php/conf.d/limesurvey.ini

# ---------------------------------------------------------------------------
# 3. Apache
# ---------------------------------------------------------------------------
#
# O LimeSurvey depende de reescrita de URL e de diretivas em .htaccess, o que
# exige AllowOverride. ServerName fixo suprime o aviso de inicializacao.

RUN set -eux; \
    a2enmod rewrite headers; \
    printf 'ServerName localhost\n' > /etc/apache2/conf-available/servername.conf; \
    a2enconf servername; \
    printf '%s\n' \
        '<Directory /var/www/html>' \
        '    Options -Indexes +FollowSymLinks' \
        '    AllowOverride All' \
        '    Require all granted' \
        '</Directory>' \
        > /etc/apache2/conf-available/limesurvey.conf; \
    a2enconf limesurvey

# ---------------------------------------------------------------------------
# 4. LimeSurvey
# ---------------------------------------------------------------------------
#
# A soma de verificacao e conferida ANTES de descompactar. Se a conferencia
# falhar, a construcao para — e essa e a intencao: um pacote que nao confere
# nao deve virar imagem em silencio.

RUN set -eux; \
    curl -fsSL -o /tmp/limesurvey.zip "${LIMESURVEY_URL}"; \
    echo "${LIMESURVEY_SHA256}  /tmp/limesurvey.zip" | sha256sum -c -; \
    mkdir -p /tmp/extraido; \
    unzip -q /tmp/limesurvey.zip -d /tmp/extraido; \
    rm -rf /var/www/html; \
    if [ -d /tmp/extraido/limesurvey ]; then \
        mv /tmp/extraido/limesurvey /var/www/html; \
    else \
        mv /tmp/extraido /var/www/html; \
    fi; \
    rm -rf /tmp/limesurvey.zip /tmp/extraido; \
    test -f /var/www/html/index.php; \
    test -d /var/www/html/application

# ---------------------------------------------------------------------------
# 5. Permissoes
# ---------------------------------------------------------------------------
#
# O LimeSurvey precisa escrever em tres lugares. Os dois primeiros recebem
# volume no compose; o terceiro guarda o config.php que o instalador gera.

RUN set -eux; \
    mkdir -p \
        /var/www/html/tmp \
        /var/www/html/upload \
        /var/www/html/application/config; \
    chown -R www-data:www-data /var/www/html

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=5 \
    CMD curl -fsS http://localhost/index.php -o /dev/null || exit 1

EXPOSE 80
