"""
Roda, no conteiner do LimeSurvey, os comandos de console proprios do projeto.

Existe para as operacoes que a API RemoteControl nao oferece — exportar a
estrutura (E15), criar atributos da base central e gravar nela com decifracao
(E17), registrar a importacao na trilha. Os comandos estao em
infra/instrumento/comandos/ e sao copiados para o conteiner a cada chamada, de
modo que a imagem nao muda. O console do LimeSurvey os carrega do diretorio
indicado em YII_CONSOLE_COMMANDS.

Roda no HOSPEDEIRO, porque chama `docker compose exec`. O conteiner `rotinas`
nao tem acesso ao Docker, de proposito.
"""

import os
import subprocess

from limesurvey_api import API

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFRA = os.path.join(RAIZ, "infra")
COMANDOS = os.path.join(INFRA, "instrumento", "comandos")
DESTINO = "/tmp/egressos-comandos"


def carrega_env():
    """Le infra/.env, que nao e versionado."""
    caminho = os.path.join(INFRA, ".env")
    if not os.path.exists(caminho):
        raise RuntimeError("infra/.env ausente — copie .env.exemplo e preencha")
    env = {}
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                chave, valor = linha.split("=", 1)
                env[chave.strip()] = valor.strip()
    return env


def api_do_hospedeiro():
    """Sessao da API pela porta publicada no hospedeiro."""
    env = carrega_env()
    return API(url=f"http://127.0.0.1:{env.get('PORTA_HTTP', '8080')}",
               usuario=env.get("ADMIN_USUARIO"), senha=env.get("ADMIN_SENHA"))


def console(comando, *argumentos, entrada=None):
    """Executa `php console.php <comando> <argumentos>` no conteiner, com
    `entrada` (texto) pela entrada padrao. Devolve o CompletedProcess."""
    subprocess.run(["docker", "compose", "exec", "-T", "limesurvey",
                    "mkdir", "-p", DESTINO], cwd=INFRA, check=True)
    for arquivo in sorted(os.listdir(COMANDOS)):
        if arquivo.endswith("Command.php"):
            subprocess.run(["docker", "compose", "cp",
                            os.path.join(COMANDOS, arquivo),
                            f"limesurvey:{DESTINO}/"], cwd=INFRA, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return subprocess.run(
        ["docker", "compose", "exec", "-T", "-e",
         f"YII_CONSOLE_COMMANDS={DESTINO}", "limesurvey", "php",
         "application/commands/console.php", comando, *map(str, argumentos)],
        cwd=INFRA, input=entrada, capture_output=True, text=True)
