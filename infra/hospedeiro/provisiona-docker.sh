#!/usr/bin/env bash
#
# Provisiona o hospedeiro Docker para a instancia LimeSurvey do projeto.
#
# Instala o Docker Engine (Apache 2.0) a partir do repositorio oficial do Docker,
# em distribuicoes Debian e Ubuntu. NAO instala o Docker Desktop — a escolha esta
# justificada na ADR-0002 (docs/decisoes/0002-ambiente-execucao.md).
#
# Quando executado dentro do WSL2, tambem habilita o systemd, sem o que o Docker
# nao sobe sozinho no inicio da distribuicao.
#
# Uso:  sudo ./provisiona-docker.sh
#
# O script e idempotente: pode ser executado novamente sem efeito colateral.

set -euo pipefail

msg()  { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
aviso() { printf '\033[33m    %s\033[0m\n' "$*"; }
erro() { printf '\033[31m!!! %s\033[0m\n' "$*" >&2; }

if [ "$(id -u)" -ne 0 ]; then
    erro "Execute como root: sudo $0"
    exit 1
fi

# ---------------------------------------------------------------------------
# 1. Identificacao da distribuicao
# ---------------------------------------------------------------------------

if [ ! -r /etc/os-release ]; then
    erro "/etc/os-release ausente — distribuicao nao identificavel."
    exit 1
fi

# shellcheck disable=SC1091
. /etc/os-release

case "${ID:-}" in
    ubuntu) REPO_DISTRO="ubuntu" ;;
    debian) REPO_DISTRO="debian" ;;
    *)
        erro "Distribuicao '${ID:-desconhecida}' nao suportada por este script."
        erro "Ele cobre Debian e Ubuntu. Para outras, ver a documentacao do Docker."
        exit 1
        ;;
esac

CODINOME="${VERSION_CODENAME:-}"
if [ -z "$CODINOME" ]; then
    erro "VERSION_CODENAME ausente em /etc/os-release."
    exit 1
fi

msg "Distribuicao: ${PRETTY_NAME:-$ID} (codinome ${CODINOME})"

# ---------------------------------------------------------------------------
# 2. systemd no WSL2
# ---------------------------------------------------------------------------
#
# Fora do WSL este bloco nao faz nada. Dentro dele, e o que permite que o
# servico do Docker suba com a distribuicao, em vez de exigir partida manual.

EXIGE_REINICIO_WSL=0

if grep -qi microsoft /proc/version 2>/dev/null; then
    msg "Ambiente WSL detectado — verificando systemd"

    if [ -f /etc/wsl.conf ] && grep -qE '^\s*systemd\s*=\s*true' /etc/wsl.conf; then
        aviso "systemd ja habilitado em /etc/wsl.conf"
    else
        if [ -f /etc/wsl.conf ]; then
            cp /etc/wsl.conf "/etc/wsl.conf.bak.$(date +%Y%m%d%H%M%S)"
            aviso "/etc/wsl.conf existente preservado em copia com data"
        fi
        cat > /etc/wsl.conf <<'WSLCONF'
[boot]
systemd=true
WSLCONF
        EXIGE_REINICIO_WSL=1
        aviso "systemd habilitado — a distribuicao precisara ser reiniciada"
    fi
fi

# ---------------------------------------------------------------------------
# 3. Repositorio oficial do Docker
# ---------------------------------------------------------------------------

msg "Preparando o repositorio oficial do Docker"

export DEBIAN_FRONTEND=noninteractive

apt-get update -qq
apt-get install -y -qq ca-certificates curl gnupg

install -m 0755 -d /etc/apt/keyrings

if [ ! -f /etc/apt/keyrings/docker.asc ]; then
    curl -fsSL "https://download.docker.com/linux/${REPO_DISTRO}/gpg" \
        -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
fi

ARQUITETURA="$(dpkg --print-architecture)"
LINHA_REPO="deb [arch=${ARQUITETURA} signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/${REPO_DISTRO} ${CODINOME} stable"

echo "$LINHA_REPO" > /etc/apt/sources.list.d/docker.list

apt-get update -qq

# ---------------------------------------------------------------------------
# 4. Instalacao
# ---------------------------------------------------------------------------

msg "Instalando o Docker Engine e o plugin Compose"

apt-get install -y -qq \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

# ---------------------------------------------------------------------------
# 5. Usuario nao root no grupo docker
# ---------------------------------------------------------------------------
#
# SUDO_USER so existe quando o script foi chamado via sudo por um usuario comum.
# Numa distro WSL recem-criada, em que se opera como root, nao ha o que fazer.

if [ -n "${SUDO_USER:-}" ] && [ "${SUDO_USER}" != "root" ]; then
    msg "Adicionando '${SUDO_USER}' ao grupo docker"
    usermod -aG docker "${SUDO_USER}"
    aviso "A nova associacao de grupo so vale a partir da proxima sessao."
fi

# ---------------------------------------------------------------------------
# 6. Verificacao
# ---------------------------------------------------------------------------

msg "Versoes instaladas"
docker --version
docker compose version

if [ "$EXIGE_REINICIO_WSL" -eq 1 ]; then
    msg "Falta um passo, e ele e no Windows"
    cat <<'FINAL'
    O systemd foi habilitado agora e so passa a valer depois de reiniciar a
    distribuicao. No PowerShell do Windows, execute:

        wsl --shutdown

    Em seguida reabra a distribuicao e confirme com:

        docker run --rm hello-world
FINAL
else
    msg "Concluido"
    echo "    Confirme com: docker run --rm hello-world"
fi
