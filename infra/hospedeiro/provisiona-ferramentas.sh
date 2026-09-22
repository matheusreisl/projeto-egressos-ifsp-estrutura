#!/usr/bin/env bash
#
# Ferramentas de apoio ao trabalho de pesquisa.
#
# NAO fazem parte do ambiente da instancia LimeSurvey e NAO sao necessarias a
# quem apenas replica o mecanismo. Estao versionadas porque tornam reproduzivel
# o trabalho de leitura de fontes e o desenvolvimento das rotinas do projeto:
#
#   poppler-utils   extracao de texto de PDF com camada de texto (pdftotext)
#   tesseract-ocr   reconhecimento optico, para PDF que e so imagem
#   ocrmypdf        aplica OCR e devolve um PDF pesquisavel
#   python3 + venv  rotinas do projeto (base sintetica, extracao, devolucoes)
#
# Uso:  sudo ./provisiona-ferramentas.sh

set -euo pipefail

msg() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }

if [ "$(id -u)" -ne 0 ]; then
    printf '\033[31m!!! Execute como root: sudo %s\033[0m\n' "$0" >&2
    exit 1
fi

export DEBIAN_FRONTEND=noninteractive

msg "Atualizando indices de pacote"
apt-get update -qq

msg "Extracao de texto e OCR"
apt-get install -y -qq \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    ocrmypdf \
    qpdf \
    unzip

msg "Python"
apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-venv

msg "Versoes instaladas"
printf '%-14s %s\n' "python3"   "$(python3 --version 2>&1)"
printf '%-14s %s\n' "pdftotext" "$(pdftotext -v 2>&1 | head -1)"
printf '%-14s %s\n' "tesseract" "$(tesseract --version 2>&1 | head -1)"
printf '%-14s %s\n' "ocrmypdf"  "$(ocrmypdf --version 2>&1 | head -1)"
printf '%-14s %s\n' "idiomas"   "$(tesseract --list-langs 2>&1 | tail -n +2 | tr '\n' ' ')"

msg "Concluido"
