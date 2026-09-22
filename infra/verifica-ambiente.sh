#!/usr/bin/env bash
#
# Confere se o ambiente tem as propriedades que a documentacao afirma.
#
# Nao substitui a matriz de verificacao da E25, que trata do mecanismo. Este
# script trata do ambiente: servicos de pe, porta publicada, contencao de rede
# e extensoes do PHP presentes. Serve tambem a quem replica, para confirmar que
# chegou ao mesmo lugar.
#
# Uso:  ./verifica-ambiente.sh        (a partir da pasta infra/)

set -uo pipefail

cd "$(dirname "$0")"

VERDES=0
VERMELHOS=0

ok()    { printf '  \033[32m[ok]\033[0m    %s\n' "$*"; VERDES=$((VERDES+1)); }
falha() { printf '  \033[31m[FALHA]\033[0m %s\n' "$*"; VERMELHOS=$((VERMELHOS+1)); }
titulo(){ printf '\n\033[1m%s\033[0m\n' "$*"; }

PORTA="$(grep -E '^PORTA_HTTP=' .env 2>/dev/null | cut -d= -f2)"
PORTA="${PORTA:-8080}"

# ---------------------------------------------------------------------------
titulo "1. Servicos"
# ---------------------------------------------------------------------------

for servico in banco limesurvey; do
    estado="$(docker compose ps --format '{{.Service}} {{.Status}}' 2>/dev/null \
              | awk -v s="$servico" '$1==s {$1=""; print}' | sed 's/^ //')"
    case "$estado" in
        Up*healthy*) ok "$servico: $estado" ;;
        Up*)         falha "$servico esta de pe mas nao saudavel: $estado" ;;
        *)           falha "$servico nao esta de pe ($estado)" ;;
    esac
done

# ---------------------------------------------------------------------------
titulo "2. Porta publicada"
# ---------------------------------------------------------------------------

CODIGO="$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "http://127.0.0.1:${PORTA}/" || echo 000)"
if [ "$CODIGO" = "200" ] || [ "$CODIGO" = "302" ]; then
    ok "LimeSurvey responde em 127.0.0.1:${PORTA} (HTTP ${CODIGO})"
else
    falha "LimeSurvey nao respondeu em 127.0.0.1:${PORTA} (HTTP ${CODIGO})"
fi

# ---------------------------------------------------------------------------
titulo "3. Contencao de rede"
# ---------------------------------------------------------------------------
#
# A propriedade que sustenta o criterio K6 da ADR-0002. Confere-se pelo efeito,
# nao pela declaracao no arquivo.

if docker compose exec -T banco getent hosts example.com >/dev/null 2>&1; then
    falha "o banco RESOLVE nome externo — a rede interna nao esta contendo"
else
    ok "o banco nao resolve nome externo"
fi

if docker compose exec -T banco bash -c 'timeout 5 bash -c "</dev/tcp/1.1.1.1/53"' >/dev/null 2>&1; then
    falha "o banco ALCANCA a internet — a rede interna nao esta contendo"
else
    ok "o banco nao alcanca a internet"
fi

if docker compose exec -T limesurvey bash -c 'timeout 5 bash -c "</dev/tcp/banco/3306"' >/dev/null 2>&1; then
    ok "o LimeSurvey alcanca o banco pela rede interna"
else
    falha "o LimeSurvey NAO alcanca o banco"
fi

# Atencao: 'docker compose ps' mostra tanto a porta EXPOSTA pela imagem
# (ex.: "3306/tcp") quanto a PUBLICADA no hospedeiro (ex.: "0.0.0.0:3306->3306/tcp").
# So a segunda importa aqui, e ela se distingue pela seta.
PORTAS_BANCO="$(docker compose ps --format '{{.Service}}|{{.Ports}}' 2>/dev/null \
                | awk -F'|' '$1=="banco"{print $2}')"
if printf '%s' "$PORTAS_BANCO" | grep -q -- '->'; then
    falha "o banco esta publicando porta no hospedeiro: $PORTAS_BANCO"
else
    ok "o banco nao publica porta no hospedeiro (exposta: ${PORTAS_BANCO:-nenhuma})"
fi

# ---------------------------------------------------------------------------
titulo "4. Extensoes do PHP"
# ---------------------------------------------------------------------------

MODULOS="$(docker compose exec -T limesurvey php -m 2>/dev/null | tr 'A-Z' 'a-z')"

for ext in mbstring pdo_mysql curl gd zip intl ldap session fileinfo simplexml openssl zlib; do
    if printf '%s\n' "$MODULOS" | grep -qx "$ext"; then
        ok "extensao presente: $ext"
    else
        falha "extensao AUSENTE: $ext"
    fi
done

# O OPcache nao aparece na lista de modulos comuns: e extensao Zend, listada
# como "Zend OPcache" numa secao propria de 'php -m'. Conferir pelo carregamento
# e mais confiavel do que casar o nome.
if docker compose exec -T limesurvey php -r 'exit(extension_loaded("Zend OPcache") ? 0 : 1);' >/dev/null 2>&1; then
    ok "extensao presente: Zend OPcache"
else
    falha "extensao AUSENTE: Zend OPcache"
fi

# A ausencia de imap e deliberada — ver ADR-0004. Verifica-se para que uma
# mudanca silenciosa de base nao passe despercebida.
if printf '%s\n' "$MODULOS" | grep -qx imap; then
    falha "extensao imap PRESENTE — a ADR-0004 decidiu que nao estaria; confira a base"
else
    ok "extensao imap ausente, conforme ADR-0004"
fi

# ---------------------------------------------------------------------------
titulo "5. Versoes"
# ---------------------------------------------------------------------------

printf '  php        %s\n' "$(docker compose exec -T limesurvey php -r 'echo PHP_VERSION;' 2>/dev/null)"
printf '  banco      %s\n' "$(docker compose exec -T banco mariadb --version 2>/dev/null | sed 's/.*Distrib //;s/,.*//')"
VERSAO_LS="$(docker compose exec -T limesurvey sh -c 'grep -o "\"versionnumber\"[^,]*" application/config/version.php 2>/dev/null | head -1' 2>/dev/null)"
printf '  limesurvey %s\n' "${VERSAO_LS:-(a registrar na E08)}"

# ---------------------------------------------------------------------------
printf '\n\033[1mResultado:\033[0m %d conferencias passaram, %d falharam\n' "$VERDES" "$VERMELHOS"
[ "$VERMELHOS" -eq 0 ] || exit 1
