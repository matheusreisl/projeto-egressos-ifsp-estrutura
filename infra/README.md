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
| `limesurvey/entrypoint.sh` | gera o `config.php` e instala o LimeSurvey sem interação |
| `correio/Dockerfile` | MTA de ensaio: Postfix que devolve e Dovecot que serve a caixa |
| `correio/entrypoint.sh` | configura os três domínios de ensaio e supervisiona os dois serviços |
| `rotinas/Dockerfile` | onde as rotinas do projeto rodam, dentro da rede interna |
| `hospedeiro/provisiona-docker.sh` | instala o Docker Engine num hospedeiro Debian ou Ubuntu |
| `hospedeiro/provisiona-ferramentas.sh` | ferramentas de apoio à pesquisa (não são do mecanismo) |
| `verifica-ambiente.sh` | confere as propriedades do ambiente |
| `confere-capacidades.py` | confere as capacidades C1 a C10 contra a instância |
| `confere-envio.py` | confere a integração: a instância dispara, a devolução volta, a regra se aplica |

Os quatro serviços da composição:

| Serviço | Papel | Redes |
|---|---|---|
| `banco` | MariaDB | só interna |
| `limesurvey` | a instância | interna **e** externa (porta publicada) |
| `correio` | MTA de ensaio, Postfix e Dovecot | **só interna** |
| `rotinas` | ponto de execução das rotinas do projeto | **só interna** |

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
`PORTA_HTTP`, com o usuário e a senha definidos no `.env`.

**A instalação do LimeSurvey é desatendida.** Não há instalador web a percorrer:
a inicialização do contêiner gera o `application/config/config.php` a partir do
`.env` e executa o instalador de console quando o banco está vazio. As duas
operações são idempotentes, de modo que `docker compose down -v` seguido de
`up -d` devolve uma instância pronta, sem passo manual no meio.

A senha do administrador **não** fica gravada no `config.php`: é usada só durante
a instalação, por arquivo temporário removido em seguida. Trocá-la no `.env`
depois da instalação não muda a senha — use o painel ou o comando
`resetpassword` do console do LimeSurvey.

Para conferir que o ambiente ficou como a documentação afirma:

```bash
./verifica-ambiente.sh
```

E para conferir que a instância tem as capacidades de que a especificação
depende:

```bash
python3 confere-capacidades.py
```

Esse segundo script cria um questionário de teste descartável, insere dois
participantes sintéticos sob domínio `.test`, inspeciona esquema e comportamento
e remove tudo ao final. Não envia mensagem alguma. O resultado esperado é **7
capacidades atendidas e 3 parciais**, com o detalhamento em
[`capacidades-plataforma.md`](../docs/especificacao/capacidades-plataforma.md).

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

## Correio de ensaio

O serviço `correio` **não é um capturador de SMTP**, e a distinção é a razão de
ele existir. Capturadores de uso corrente em desenvolvimento aceitam toda
mensagem e nunca devolvem erro: satisfazem "vi a mensagem chegar" e inviabilizam
o parâmetro P8, que exige **ler e classificar a devolução**. Aqui roda um MTA de
verdade — Postfix, que devolve — mais um servidor IMAP — Dovecot, para que a
rotina de leitura converse com a caixa do mesmo modo que conversaria com uma
caixa institucional numa implantação real.

**Três domínios, cada um produzindo uma linha da tabela de classificação da
seção 10.1 de [`parametros-contato.md`](../docs/especificacao/parametros-contato.md):**

| Domínio | O que acontece | Resultado |
|---|---|---|
| `egressos.test` | entrega normal | chega na caixa `entregues` |
| `invalido.test` | usuário inexistente | **devolução permanente** (5.x.x) |
| `indisponivel.test` | servidor inalcançável | **devolução temporária** (4.x.x) |

Todos sob o TLD reservado `.test` (RFC 2606 / 6761), que não resolve na internet
pública e não pode colidir com domínio de terceiro. É a segunda camada da mesma
proteção: a primeira é o serviço não ter rota de saída.

**Duas caixas, e a separação importa.** `devolucoes` recebe as devoluções e
`entregues` recebe as mensagens entregues. Sem separá-las, a rotina de leitura
veria mensagens comuns no meio das devoluções.

### Verificando as duas direções

```bash
docker compose exec rotinas python3 verifica_correio.py
```

Exercita o correio por SMTP direto, sem o LimeSurvey no caminho — isola o
comportamento do MTA. Leva alguns minutos, porque o aviso de atraso que produz a
devolução temporária não é imediato.

```bash
python3 confere-envio.py
```

Exercita a **integração**: a instância dispara os convites, a devolução volta, a
rotina classifica e o estado do participante muda. Chama a rotina de verdade, e
não uma reimplementação dela.

### Três detalhes que custaram tempo, registrados para quem for replicar

**`local_recipient_maps` vazio, de propósito.** Sem isso o Postfix recusa o
destinatário inexistente no próprio diálogo SMTP, com um 550 síncrono, e **não
há devolução a ler**. Com o parâmetro vazio ele aceita a mensagem e falha na
entrega, gerando a devolução assíncrona que o P8 pressupõe.

**`relay_domains` precisa nomear o domínio indisponível.** Ele não é destino
final deste servidor: precisa ser retransmitido para o endereço inalcançável, e é
a tentativa frustrada que gera a devolução temporária. Sem declará-lo, o Postfix
responde `454 4.7.1 Relay access denied` e, de novo, não há o que ler.

**Os dois serviços são supervisionados.** Num hospedeiro WSL o relógio da máquina
virtual **salta** quando a distribuição suspende e retoma; o Dovecot detecta o
salto e se recusa a lançar serviços durante aquele intervalo. O sintoma observado
foi IMAP recusando conexão com o contêiner aparentemente saudável. A inicialização
vigia os dois processos e encerra em erro se um cair, para que a política de
reinício recrie o contêiner inteiro.

## Rotinas do projeto

O serviço `rotinas` existe por topologia, não por conveniência: o correio fica
somente na rede interna, que o hospedeiro não alcança, de modo que qualquer
rotina que leia a caixa de devoluções precisa rodar de dentro dessa rede.

Os scripts vivem em [`scripts/`](../scripts/), no repositório, montados em modo
somente leitura. A imagem não carrega cópia deles — assim não há duas versões do
mesmo arquivo.

```bash
docker compose exec rotinas python3 ler_devolucoes.py \
    --ciclo 2026-1 --questionario 123456 --simular
```

`--simular` lê e classifica sem gravar, marcar nem consumir a caixa.

A E21 substitui o comando desse contêiner pelo agendador. Até lá ele fica de pé,
ocioso, servindo de ponto de execução.

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
