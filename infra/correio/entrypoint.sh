#!/usr/bin/env bash
#
# Inicializacao do servico de correio de ensaio.
#
# Idempotente: cria as caixas se faltarem, escreve a configuracao e sobe os dois
# servicos. Ver comentarios no Dockerfile para o desenho dos tres dominios.

set -euo pipefail

log() { printf '[correio] %s\n' "$*"; }

: "${DOMINIO:=egressos.test}"
: "${DOMINIO_INVALIDO:=invalido.test}"
: "${DOMINIO_INDISPONIVEL:=indisponivel.test}"
: "${CAIXA_DEVOLUCOES:=devolucoes}"
: "${CAIXA_ENTREGUES:=entregues}"
: "${SENHA_CAIXA:?SENHA_CAIXA nao definida}"

# Endereco IP reservado para documentacao (RFC 5737, TEST-NET-1). Nao e
# roteavel, e por isso a tentativa de entrega falha de imediato com erro
# temporario — que e exatamente o que se quer exercitar.
: "${IP_INALCANCAVEL:=192.0.2.1}"

log "dominio de entrega   : ${DOMINIO}"
log "dominio invalido     : ${DOMINIO_INVALIDO}"
log "dominio indisponivel : ${DOMINIO_INDISPONIVEL}"

# ---------------------------------------------------------------------------
# 1. Caixas
# ---------------------------------------------------------------------------
#
# Duas caixas locais, e a separacao importa: a rotina de leitura precisa ver
# SOMENTE devolucoes, sem as mensagens entregues no meio.

for caixa in "$CAIXA_DEVOLUCOES" "$CAIXA_ENTREGUES"; do
    if id "$caixa" >/dev/null 2>&1; then
        log "caixa ${caixa} ja existe"
    else
        useradd --create-home --shell /usr/sbin/nologin "$caixa"
        log "caixa ${caixa} criada"
    fi
    echo "${caixa}:${SENHA_CAIXA}" | chpasswd
    mkdir -p "/home/${caixa}/Maildir"/{cur,new,tmp}
    chown -R "${caixa}:${caixa}" "/home/${caixa}/Maildir"
    chmod -R 700 "/home/${caixa}/Maildir"
done

# ---------------------------------------------------------------------------
# 2. Postfix
# ---------------------------------------------------------------------------

log "configurando o Postfix"

# Mapa de reescrita. A ordem importa: a primeira expressao que casar vence.
# A caixa de devolucoes vem antes do curinga, senao as devolucoes cairiam
# junto com as mensagens entregues.
cat > /etc/postfix/reescrita.pcre <<PCRE
/^${CAIXA_DEVOLUCOES}@${DOMINIO}\$/   ${CAIXA_DEVOLUCOES}
/^[^@]+@${DOMINIO}\$/                 ${CAIXA_ENTREGUES}
PCRE

# O dominio "indisponivel" e entregue a um endereco nao roteavel, de proposito.
cat > /etc/postfix/transporte <<TRANSPORTE
${DOMINIO_INDISPONIVEL}   smtp:[${IP_INALCANCAVEL}]:25
TRANSPORTE
postmap /etc/postfix/transporte

postconf -e "myhostname = correio.${DOMINIO}"
postconf -e "mydomain = ${DOMINIO}"
postconf -e "myorigin = \$mydomain"

# O dominio invalido e destino FINAL deste servidor, e e por isso que ele
# devolve: a mensagem e aceita e depois falha na entrega, por usuario
# inexistente. Sem isso a recusa viria sincrona, no proprio dialogo SMTP, e
# nao haveria devolucao a ler — que e o que o P8 exige.
postconf -e "mydestination = \$myhostname, localhost, ${DOMINIO}, ${DOMINIO_INVALIDO}"

# Vazio de proposito: faz o Postfix aceitar qualquer destinatario local e
# devolver na entrega, em vez de recusar no dialogo.
postconf -e "local_recipient_maps ="

postconf -e "virtual_alias_maps = pcre:/etc/postfix/reescrita.pcre"
postconf -e "transport_maps = hash:/etc/postfix/transporte"

# O dominio "indisponivel" nao e destino final deste servidor: ele precisa ser
# RETRANSMITIDO para o endereco inalcancavel, e e a tentativa frustrada de
# retransmissao que gera a devolucao temporaria. Sem declara-lo aqui, o Postfix
# recusa a mensagem no proprio dialogo, com "Relay access denied", e nao ha
# devolucao a ler — que e o oposto do que se quer exercitar.
postconf -e "relay_domains = ${DOMINIO_INDISPONIVEL}"

postconf -e "home_mailbox = Maildir/"
postconf -e "inet_interfaces = all"
postconf -e "inet_protocols = ipv4"
postconf -e "mynetworks_style = subnet"

# Rede fechada: nao ha TLS a negociar nem por que exigi-lo.
postconf -e "smtpd_tls_security_level = none"
postconf -e "smtp_tls_security_level = none"

# Sem relayhost: o que este servidor nao conhece, ele nao entrega.
postconf -e "relayhost ="
postconf -e "smtp_dns_support_level = disabled"
postconf -e "smtp_host_lookup = native"

# Aviso de atraso rapido, para que a devolucao TEMPORARIA apareca em tempo de
# ensaio em vez de horas depois. Em producao esses valores seriam outros.
postconf -e "delay_warning_time = 1m"
postconf -e "maximal_queue_lifetime = 1h"
postconf -e "bounce_queue_lifetime = 1h"
postconf -e "queue_run_delay = 30s"
postconf -e "minimal_backoff_time = 30s"
postconf -e "maximal_backoff_time = 2m"

# Registro em stdout, para aparecer em `docker compose logs`.
postconf -e "maillog_file = /dev/stdout"

newaliases 2>/dev/null || true

# ---------------------------------------------------------------------------
# 3. Dovecot
# ---------------------------------------------------------------------------

log "configurando o Dovecot"

cat > /etc/dovecot/dovecot.conf <<DOVECOT
# Configuracao minima, para rede fechada. Sem TLS, com autenticacao simples:
# o servico nao e alcancavel de fora da rede interna da composicao.
dovecot_config_version = 2.4.1
dovecot_storage_version = 2.4.0

protocols = imap
listen = *

mail_driver = maildir
mail_path = ~/Maildir

auth_mechanisms = plain login

passdb pam {
}

userdb passwd {
}

ssl = no
auth_allow_cleartext = yes

log_path = /dev/stdout
info_log_path = /dev/stdout

service imap-login {
  inet_listener imap {
    port = 143
  }
}
DOVECOT

# ---------------------------------------------------------------------------
# 4. Partida
# ---------------------------------------------------------------------------

log "iniciando o Dovecot"
dovecot

log "iniciando o Postfix"
postfix start

# ---------------------------------------------------------------------------
# 5. Supervisao
# ---------------------------------------------------------------------------
#
# Sao dois servicos num conteiner, e sem isto nenhum deles seria vigiado: se o
# Dovecot morresse, o conteiner seguiria "de pe" com o IMAP fora do ar, e a
# rotina de leitura de devolucoes falharia sem motivo aparente.
#
# O motivo de isso deixar de ser hipotetico: num hospedeiro WSL, o relogio da
# maquina virtual SALTA quando a distribuicao suspende e retoma. O Dovecot
# detecta o salto — "Time moved backwards" — e se recusa a lancar servicos
# durante aquele intervalo, por precaucao legitima. O resultado observado foi
# IMAP recusando conexao com o conteiner aparentemente saudavel.
#
# A saida adotada e a convencional em conteiner: se qualquer um dos dois cair,
# este processo termina em erro e a politica de reinicio da composicao recria o
# conteiner inteiro, com os dois de volta. Nao se tenta remendar o servico caido
# — reiniciar por inteiro e mais previsivel do que consertar pela metade.

encerrar() {
    log "encerrando"
    postfix stop  >/dev/null 2>&1 || true
    doveadm stop  >/dev/null 2>&1 || true
    exit 0
}
trap encerrar TERM INT

# Sonda funcional do IMAP: faz LOGIN de verdade, e nao apenas abre a porta.
#
# A diferenca nao e preciosismo. Depois de um salto de relogio, observou-se o
# Dovecot com a porta aberta, a autenticacao interna funcionando (`doveadm auth
# test` passava) e ainda assim recusando toda sessao de rede, porque o repasse
# da conexao ao processo imap falhava. Uma sonda que so verifica a porta declara
# esse estado saudavel, e a rotina de leitura falha sem motivo aparente.
sonda_imap() {
    local resposta
    resposta="$(printf 'a LOGIN %s %s\r\na LOGOUT\r\n' \
                    "$CAIXA_DEVOLUCOES" "$SENHA_CAIXA" \
                | timeout 10 nc -w 5 localhost 143 2>/dev/null)"
    printf '%s' "$resposta" | grep -q '^a OK'
}

falhas_seguidas=0

while true; do
    sleep 15

    if ! postfix status >/dev/null 2>&1; then
        log "ERRO: o Postfix caiu — encerrando para que o conteiner reinicie"
        exit 1
    fi

    if ! pgrep -x dovecot >/dev/null 2>&1; then
        log "ERRO: o Dovecot caiu — encerrando para que o conteiner reinicie"
        exit 1
    fi

    if sonda_imap; then
        falhas_seguidas=0
    else
        falhas_seguidas=$((falhas_seguidas + 1))
        log "AVISO: a sonda de IMAP falhou (${falhas_seguidas} vez(es) seguidas)"
        # Duas falhas seguidas, para nao reagir a um tropeco isolado.
        if [ "$falhas_seguidas" -ge 2 ]; then
            log "ERRO: IMAP nao responde a LOGIN — encerrando para que o conteiner reinicie"
            exit 1
        fi
    fi
done
