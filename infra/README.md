# Infraestrutura

Artefatos de provisionamento da instância LimeSurvey do projeto.

O ambiente foi decidido na E06 e está registrado na
[ADR-0002](../docs/decisoes/0002-ambiente-execucao.md): **conteinerização
declarativa em máquina local**, com a composição inteira declarada em arquivo, em
rede fechada. A imagem própria do LimeSurvey foi decidida na E07 e está registrada
na [ADR-0004](../docs/decisoes/0004-imagem-propria-e-leitura-de-devolucoes.md).

## O que há aqui

| Arquivo | Papel |
|---|---|
| `compose.yml` | a composição: serviços, redes, volumes |
| `.env.exemplo` | modelo de configuração, sem valores reais |
| `limesurvey/Dockerfile` | a imagem própria — **é** o procedimento de instalação |
| `hospedeiro/provisiona-docker.sh` | instala o Docker Engine num hospedeiro Debian ou Ubuntu |

O `.env` real **não é versionado**. O repositório é público.

## Requisitos

Um hospedeiro com **Docker Engine** e o plugin **Compose**. Nada além disso: sem
conta em provedor, sem meio de pagamento, sem serviço externo.

A composição não sabe nem se importa com o sistema operacional embaixo. Ela sobe
igual em Linux nativo, em macOS e em servidor institucional. O que muda de um caso
para outro é apenas **como se obtém um hospedeiro Docker**, e isso é escolha de
quem replica.

### Obtendo o hospedeiro

**Linux (Debian ou Ubuntu)** — inclusive dentro do WSL2, no Windows:

```bash
sudo ./hospedeiro/provisiona-docker.sh
```

O script instala o Docker Engine a partir do repositório oficial do Docker e, se
detectar WSL, habilita o `systemd`. É idempotente. **Não instala o Docker
Desktop**: a razão está na ADR-0002, e é de licenciamento, não de técnica.

**No Windows**, antes de rodar o script, obtenha uma distribuição Linux:

```powershell
wsl --install -d Ubuntu-24.04
```

Se o script disser que habilitou o `systemd`, reinicie a distribuição com
`wsl --shutdown` no PowerShell antes de seguir.

**Em macOS ou em outras distribuições Linux**, instale o Docker Engine pela
documentação oficial do Docker. Daqui em diante o procedimento é idêntico.

## Subindo o ambiente

```bash
cp .env.exemplo .env
```

Edite o `.env` e defina as senhas. Para gerar uma:

```bash
openssl rand -base64 24
```

Depois:

```bash
docker compose up -d --build
```

A primeira construção baixa o pacote do LimeSurvey (cerca de 123 MB) e compila as
extensões do PHP. Leva alguns minutos. As seguintes reaproveitam o cache.

Acompanhe até os serviços ficarem saudáveis:

```bash
docker compose ps
```

O painel responde em `http://127.0.0.1:8080` — ou na porta que estiver em
`PORTA_HTTP`. A instalação propriamente dita do LimeSurvey é a etapa **E08**.

Para conferir que o ambiente ficou como a documentação afirma:

```bash
./verifica-ambiente.sh
```

### Acesso ao painel

O padrão vincula a porta a `127.0.0.1`: só a própria máquina alcança o painel.
Vale para hospedeiro Linux nativo, macOS, servidor **e também para o WSL2** — o
encaminhamento de `localhost` do WSL alcança serviço vinculado ao laço local de
dentro da distribuição. Verificado nesta etapa.

**Sintoma conhecido, e a razão de ele estar documentado aqui.** Se a distribuição
for encerrada e reaberta no meio de uma sessão, o encaminhamento de `localhost`
do Windows pode ficar obsoleto: o painel para de responder em
`http://localhost:8080` **embora continue respondendo pelo endereço IP da
distribuição**. Não é problema da composição nem do endereço de vínculo. A
correção é reiniciar o subsistema:

```powershell
wsl --shutdown
```

Ao reabrir a distribuição, o serviço do Docker sobe pelo `systemd` e os
contêineres voltam sozinhos, pela política de reinício declarada na composição.

Registra-se porque o diagnóstico natural é culpar o endereço de vínculo — e essa
pista é falsa. Trocar para `0.0.0.0` faz o painel voltar a responder pelo IP da
distribuição e dá a impressão de ter resolvido, quando o que resolve é o
reinício.

**Quando trocar o endereço de vínculo.** A variável `ENDERECO_BIND` existe para
hospedeiro em que o laço local não seja alcançável pelo caminho pretendido. Use
com consciência: **em hospedeiro Linux nativo, `0.0.0.0` expõe o painel na rede
em que a máquina estiver** — é exatamente por isso que não é o padrão.

## Derrubando

```bash
docker compose down        # para os serviços, preserva os dados
docker compose down -v     # APAGA os volumes: banco, configuração e envios
```

O segundo comando é o que devolve o ambiente ao estado zero. É ele que torna
verificável o critério da E07 — que o ambiente suba do nada usando apenas o que
está versionado.

## Contenção

A composição declara **duas redes**, e a separação não é decorativa: é o que
sustenta o critério K6 da ADR-0002, pelo qual a restrição de nunca alcançar
endereço real deixa de ser regra de conduta e passa a ser propriedade do ambiente.

| Rede | Quem está nela | Alcança a internet? |
|---|---|---|
| `interna` (`internal: true`) | banco, LimeSurvey e — a partir da E09 — o serviço de correio | **não** |
| `externa` | somente o LimeSurvey | sim |

**Verificado nesta etapa, não presumido:**

- contêiner apenas na rede interna **não alcança a internet e não resolve nome
  externo**;
- rede interna **não permite publicar porta** para o hospedeiro — foi por isso, e
  somente por isso, que a rede `externa` existe;
- contêiner em ambas as redes alcança normalmente os que estão só na interna.

**O que isso garante, dito com precisão.** O serviço de correio da E09 fica
**somente** na rede interna. Como ele não tem rota de saída, mensagem alguma sai
da máquina, qualquer que seja o endereço de destino — inclusive um endereço real
digitado por engano no arquivo de participantes. A contenção que importa está no
caminho do correio, e é integral.

**O que isso não garante.** O contêiner do LimeSurvey está também na rede externa,
porque publicar porta exige isso, e portanto mantém saída HTTP. Ele não origina
mensagem por conta própria — envia pelo serviço de correio configurado —, mas a
afirmação honesta é que a contenção é do caminho do correio, e não isolamento
total da aplicação.

## Atualizando a versão do LimeSurvey

Não há atualização implícita: a versão é fixada por número **e** por soma de
verificação, e trocá-la é operação declarada.

1. Localize a versão desejada na página oficial de descarga e copie a URL do
   pacote `.zip`.
2. Calcule a soma:

   ```bash
   curl -sL -o /tmp/ls.zip "<URL>" && sha256sum /tmp/ls.zip
   ```

3. Atualize os três argumentos no topo de `limesurvey/Dockerfile`:
   `LIMESURVEY_VERSAO`, `LIMESURVEY_URL` e `LIMESURVEY_SHA256`.
4. Atualize também a etiqueta da imagem em `compose.yml`.
5. Reconstrua:

   ```bash
   docker compose build --no-cache limesurvey && docker compose up -d
   ```

Se a soma não conferir, a construção **para**. É o comportamento desejado.

O mesmo vale para as imagens base: estão fixadas por digest, e não por rótulo
móvel. Sem isso, "subir do zero a partir do que está versionado" não produziria o
mesmo ambiente duas vezes.

## O que ainda não está aqui

- **Serviço de correio** — entra na E09, **somente** na rede `interna`, com
  domínio sob o TLD reservado `.test`. A E09 precisa verificar as duas direções:
  envio e leitura de devolução. Capturador de SMTP que aceita tudo e nunca devolve
  erro **não** atende ao parâmetro P8.
- **Rotina de leitura de devoluções** — decidida na ADR-0004, é rotina própria do
  projeto, e não o recurso nativo do LimeSurvey.
- **Rotina agendada de lembretes** — entra na E21.
- **Estrutura do questionário** — exportada e versionada na E15.

## Regras que valem para tudo o que entrar aqui

- O ambiente deve subir do zero usando **apenas o que está versionado** nesta pasta.
- Credenciais nunca entram. Só o `.env.exemplo`, sem valores reais.
- Imagens fixadas por digest; pacotes, por soma de verificação.
- Nenhuma configuração relevante pode existir **apenas** dentro do contêiner — o
  ambiente é efêmero e recriável por decisão, não por acidente.
