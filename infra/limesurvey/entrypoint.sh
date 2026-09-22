#!/usr/bin/env bash
#
# Inicializacao do conteiner do LimeSurvey.
#
# Faz duas coisas, ambas idempotentes — podem ser repetidas sem efeito colateral:
#
#   1. gera application/config/config.php a partir de variaveis de ambiente,
#      se ele ainda nao existir;
#   2. executa a instalacao pelo console do LimeSurvey, se o banco ainda nao
#      estiver povoado.
#
# Por que desatendida, e nao pelo instalador web: o guia de replicacao (E10) e
# feito de comandos reproduziveis, nao de capturas de tela — criterio K7 da
# ADR-0002. Alem disso, `docker compose down -v` seguido de `up` precisa
# devolver uma instancia pronta, sem passo manual no meio.
#
# A senha do administrador NAO e gravada em config.php. Ela e usada apenas
# durante a instalacao, por arquivo temporario removido em seguida.

set -euo pipefail

RAIZ="/var/www/html"
CONFIG="${RAIZ}/application/config/config.php"

log() { printf '[inicializacao] %s\n' "$*"; }

# ---------------------------------------------------------------------------
# Variaveis esperadas, com padroes onde faz sentido
# ---------------------------------------------------------------------------

: "${BANCO_HOST:=banco}"
: "${BANCO_PORTA:=3306}"
: "${BANCO_NOME:?BANCO_NOME nao definido}"
: "${BANCO_USUARIO:?BANCO_USUARIO nao definido}"
: "${BANCO_SENHA:?BANCO_SENHA nao definido}"
: "${BANCO_PREFIXO:=lime_}"

: "${ADMIN_USUARIO:=admin}"
: "${ADMIN_SENHA:?ADMIN_SENHA nao definido}"
: "${ADMIN_EMAIL:=admin@egressos.test}"

: "${LIMESURVEY_DEBUG:=0}"
: "${LIMESURVEY_RPC:=json}"

# ---------------------------------------------------------------------------
# 1. config.php
# ---------------------------------------------------------------------------

if [ -f "$CONFIG" ]; then
    log "config.php ja existe — preservado"
else
    log "gerando config.php"
    cat > "$CONFIG" <<PHP
<?php
if (!defined('BASEPATH')) {
    exit('No direct script access allowed');
}

/*
 * Gerado automaticamente pela inicializacao do conteiner, a partir das
 * variaveis de ambiente definidas no .env. Nao editar a mao: a proxima
 * recriacao do volume sobrescreve. Para mudar, altere o .env e recrie.
 */

return array(
    'components' => array(
        'db' => array(
            'connectionString' => 'mysql:host=${BANCO_HOST};port=${BANCO_PORTA};dbname=${BANCO_NOME};',
            'emulatePrepare'   => true,
            'username'         => '${BANCO_USUARIO}',
            'password'         => '${BANCO_SENHA}',
            'charset'          => 'utf8mb4',
            'tablePrefix'      => '${BANCO_PREFIXO}',
        ),
        'urlManager' => array(
            // 'path' e exigido pela API REST e pelo editor novo. Nao trocar
            // para 'get' sem saber o que deixa de funcionar.
            'urlFormat'      => 'path',
            'rules'          => array(),
            'showScriptName' => true,
        ),
    ),
    'config' => array(
        'debug'    => ${LIMESURVEY_DEBUG},
        'debugsql' => 0,

        // Interface RPC. O projeto depende dela: a extracao de resultados
        // (E28) e a rotina de devolucoes (ADR-0004) conversam com a instancia
        // por aqui, e nao por tela. Em implantacao real, avaliar restringir.
        'RPCInterface' => '${LIMESURVEY_RPC}',
    )
);
PHP
    chown www-data:www-data "$CONFIG"
    chmod 640 "$CONFIG"
fi

# ---------------------------------------------------------------------------
# 2. Instalacao
# ---------------------------------------------------------------------------
#
# A deteccao e feita pela existencia da tabela de usuarios, e nao por um
# arquivo-sentinela: o estado que importa esta no banco, e e ele que deve
# responder se a instalacao ja ocorreu. Sentinela em disco mente quando o
# volume do banco e apagado e o da aplicacao, nao.

log "aguardando o banco responder"
for tentativa in $(seq 1 30); do
    if php -r "
        \$d = new PDO('mysql:host=${BANCO_HOST};port=${BANCO_PORTA}', '${BANCO_USUARIO}', '${BANCO_SENHA}');
        exit(0);
    " 2>/dev/null; then
        log "banco respondeu na tentativa ${tentativa}"
        break
    fi
    if [ "$tentativa" -eq 30 ]; then
        log "ERRO: o banco nao respondeu em 30 tentativas"
        exit 1
    fi
    sleep 2
done

JA_INSTALADO=$(php -r "
    try {
        \$d = new PDO('mysql:host=${BANCO_HOST};port=${BANCO_PORTA};dbname=${BANCO_NOME}', '${BANCO_USUARIO}', '${BANCO_SENHA}');
        \$q = \$d->query(\"SHOW TABLES LIKE '${BANCO_PREFIXO}users'\");
        echo \$q->rowCount() > 0 ? 'sim' : 'nao';
    } catch (Exception \$e) {
        echo 'nao';
    }
" 2>/dev/null || echo "nao")

if [ "$JA_INSTALADO" = "sim" ]; then
    log "instalacao ja presente no banco — nada a fazer"
else
    log "banco vazio — instalando o LimeSurvey"

    # Arquivo temporario: e a unica forma de passar usuario e senha ao
    # installfromconfig, e por isso ele e removido logo apos o uso.
    TEMP_INSTALL="$(mktemp /tmp/instala-XXXXXX.php)"
    {
        echo "<?php"
        echo "return array("
        echo "  'components' => array('db' => array("
        echo "     'connectionString' => 'mysql:host=${BANCO_HOST};port=${BANCO_PORTA};dbname=${BANCO_NOME};',"
        echo "     'emulatePrepare' => true,"
        echo "     'username' => '${BANCO_USUARIO}',"
        echo "     'password' => '${BANCO_SENHA}',"
        echo "     'charset' => 'utf8mb4',"
        echo "     'tablePrefix' => '${BANCO_PREFIXO}',"
        echo "  )),"
        echo "  'config' => array("
        echo "     'defaultuser' => '${ADMIN_USUARIO}',"
        echo "     'defaultpass' => '${ADMIN_SENHA}',"
        echo "     'siteadminemail' => '${ADMIN_EMAIL}',"
        echo "  )"
        echo ");"
    } > "$TEMP_INSTALL"
    chown www-data:www-data "$TEMP_INSTALL"

    if su -s /bin/bash www-data -c \
        "cd ${RAIZ} && php application/commands/console.php installfromconfig ${TEMP_INSTALL}"; then
        log "instalacao concluida"
    else
        rm -f "$TEMP_INSTALL"
        log "ERRO: a instalacao falhou"
        exit 1
    fi

    rm -f "$TEMP_INSTALL"
fi

# ---------------------------------------------------------------------------
# 3. Permissoes e partida
# ---------------------------------------------------------------------------

chown -R www-data:www-data "${RAIZ}/tmp" "${RAIZ}/upload" 2>/dev/null || true

log "iniciando o Apache"
exec "$@"
