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
| `instrumento/` | a estrutura do questionário: exportação versionada, gerador e configuração (E15) — ver o [README](instrumento/README.md) |
| `confere-instrumento.py` | confere o instrumento implantado contra a especificação das E13 e E14 |
| `confere-participantes.py` | confere a unicidade dos tokens e identificadores e o elo com a base central (E19) |
| `limesurvey/traducoes/` | traduções pt-BR que faltavam nas páginas de recusa e revogação, acrescentadas na construção da imagem (E23) |
| `conformidade.py` | operação de conformidade: `aplicar` ativa a trilha e confere a lista de bloqueio; `revogar` desfaz uma recusa de contato a pedido do egresso (E23) |
| `confere-conformidade.py` | confere a recusa em todos os ciclos, o registro, a trilha, a cifragem e a revogação (E23) |
| `confere-consentimento.py` | confere o termo e a versão na instância e, com `--exercitar`, aceite, recusas e recusa pela mensagem (E22) |
| `consulta-consentimento.py` | recupera, por identificador, cada manifestação sobre o termo, com data e versão, e confere o texto arquivado (E22) |
| `rotinas/configuracao/agenda.json` | a agenda da rotina de disparo: cadência, horário, feriados, calendário (E21) |
| `confere-rotina.py` | confere a rotina agendada: regras da cadência e o disparo real no horário (E21) |
| `hospedeiro/liga-wsl-ao-entrar.ps1` | só Windows: liga a distribuição do WSL ao entrar na sessão (E21) |
| `reparo-contato.py` | operação de reparo de contato: troca o principal pelo alternativo na base central (comando `repararcontato`) e no participante, que volta a `pendente`; `--fila` lista a fila de correção (E26) |
| `cenarios.py` | o respondente pelo caminho real, por HTTP: os dez caminhos e os cenários da simulação (E26) |

Os quatro serviços da composição:

| Serviço | Papel | Redes |
|---|---|---|
| `banco` | MariaDB | só interna |
| `limesurvey` | a instância | interna **e** externa (porta publicada) |
| `correio` | MTA de ensaio, Postfix e Dovecot | **só interna** |
| `rotinas` | o agendador do disparo e da leitura de devoluções (E21) | **só interna** |

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

#### Um ajuste do WSL que o projeto exige

O WSL **encerra a distribuição quando ela fica ociosa** — por padrão, depois de
15 segundos sem sessão ativa. Com os contêineres dentro dela, isso significa que
o ambiente cai sozinho, e é preciso desligar esse comportamento. Crie
`%UserProfile%\.wslconfig` com:

```ini
[general]
instanceIdleTimeout = -1
```

E reinicie com `wsl --shutdown`. O ajuste vale para **todas** as distribuições da
máquina; para desfazer, apague o arquivo e reinicie de novo.

**Como conferir que pegou.** Anote o tempo de atividade da distribuição, espere
alguns minutos **sem nenhuma sessão aberta no WSL** e compare:

```powershell
$a = [int]((wsl -d <distro> -u root -- cat /proc/uptime).Split(".")[0])
Start-Sleep -Seconds 220
$b = [int]((wsl -d <distro> -u root -- cat /proc/uptime).Split(".")[0])
"antes=$a depois=$b"
```

Se o tempo cresceu, a distribuição sobreviveu. Se voltou a um valor baixo, ela foi
encerrada e reiniciada. Medido aqui: 401 s → 621 s, crescimento de exatamente os
220 s de espera.

**Atenção ao desenhar esse teste:** ele precisa esperar **do lado do Windows**. Um
script que espera *dentro* da distribuição mantém uma sessão ativa e dá falso
positivo — foi o primeiro erro cometido aqui.

**E atenção ao escrever o arquivo:** o WSL ignora um `.wslconfig` malformado **em
silêncio**, sem aviso. Um marcador de ordem de bytes no início basta para isso, e
o sintoma é indistinguível de "a configuração não funciona". Grave em texto puro,
sem BOM.

**Atenção à configuração certa.** Há duas parecidas, e só uma serve: a que
controla a **distribuição** é `instanceIdleTimeout`, na seção `[general]`, e é a
única que aceita `-1` para desligar. A que controla a **máquina virtual** é
`vmIdleTimeout`, na seção `[wsl2]`, e só aceita um número de milissegundos. Como
a máquina virtual não fica ociosa enquanto a distribuição está de pé, a primeira
resolve as duas.

**O que isso não resolve.** Se o Windows suspender ou hibernar, a máquina virtual
suspende de todo modo, e na retomada o relógio dela **salta**. Esse salto faz o
servidor IMAP recusar conexões — ver a seção sobre o correio de ensaio. É por
isso que o serviço de correio mantém supervisão própria: o ajuste reduz a causa
mais frequente, não todas.

**E o relógio salta mesmo sem suspensão.** Medido na E21: o relógio da máquina
virtual, que os contêineres usam, estava 7,3 s atrás do Windows, e foi corrigido
aos saltos de 7 a 8 s para trás, com a máquina acordada. Num desses saltos o IMAP
recusou login por alguns segundos. As rotinas do projeto toleram isso — o
agendador relê o relógio a cada passo e reserva o disparo pelo horário previsto —,
mas quem escrever rotina nova precisa contar com um relógio que anda para trás.

#### E um segundo ajuste, para a rotina agendada

O ajuste acima impede que a distribuição **morra** ociosa. Ele não a **liga**:
depois de reiniciar o Windows, ela fica parada até que algo a invoque — e, parada,
o agendador da rotina não roda. Foi o estado em que a E21 encontrou a máquina. Para
ligá-la ao entrar na sessão, no PowerShell do próprio usuário, sem administrador:

```powershell
.\hospedeiro\liga-wsl-ao-entrar.ps1
```

O script registra uma tarefa de logon que só executa `wsl -d Ubuntu-24.04 --exec
/bin/true`. O `systemd` sobe o Docker, a política de reinício religa os
contêineres, e o agendamento continua **dentro da composição** — a tarefa não
agenda disparo nenhum ([ADR-0008](../docs/decisoes/0008-agendamento-da-cadencia.md)).
É idempotente; para desfazer, `Unregister-ScheduledTask -TaskName "Egressos -
ligar WSL ao entrar" -Confirm:$false`.

**Conferido na E21:** distribuição encerrada com `wsl --terminate`, tarefa
disparada, e 90 s depois, sem nenhuma sessão aberta, a distribuição estava de pé e
os quatro contêineres saudáveis. O agendador subiu antes do banco, esperou e
entrou. **Não conferido:** um reinício do Windows de fato, que dispara a tarefa
pelo logon.

Nada disso é necessário em hospedeiro Linux nativo.

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

**Três caixas, e a separação importa.** `devolucoes` recebe as devoluções e
`entregues` recebe as mensagens entregues. Sem separá-las, a rotina de leitura
veria mensagens comuns no meio das devoluções. `acompanhamento` é a caixa do
remetente e recebe as respostas humanas ao convite (E20): o parâmetro P7 veda
remetente sem retorno monitorado, e sem caixa própria a resposta cairia junto das
mensagens entregues. O remetente das mensagens aos egressos é propriedade do
questionário, e não do sítio — ver
[`docs/especificacao/modelos-mensagem.md`](../docs/especificacao/modelos-mensagem.md).

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

**As duas esvaziam as caixas do correio**, e por isso, desde a E26, **recusam rodar
com `ROTINA_DISPARO=real`**: no período de simulação, as caixas são evidência. E
`confere-envio.py` só remove o questionário que ele mesmo cria — até a E26, apagava
todos os da instância, e apagou o instrumento
([`simulacao.md`](../docs/especificacao/simulacao.md), seção 3.2).

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

## Rotina agendada

Desde a E21, o processo principal do contêiner `rotinas` é o **agendador**
(`scripts/agendador.py`). Ele cuida de três tarefas, independentes umas das outras:

| Tarefa | Quando | O que roda |
|---|---|---|
| disparo | **10:00, segunda a sexta**, menos os feriados da agenda | `disparar.py`: guarda, estado de cada participante, convites e lembretes que venceram |
| devoluções | a cada 30 minutos, todo dia | `ler_devolucoes.py`, da E09 |
| conformidade | a cada 30 minutos, todo dia, **sempre de verdade** | `conformidade.py`, da E23: registra recusas, leva a de contato à base central, apaga dado sensível sem consentimento |

São separadas porque a devolução temporária chega depois do disparo que a
originou (E09). A especificação está em
[`rotina-disparo.md`](../docs/especificacao/rotina-disparo.md), e a decisão de
agendar dentro da composição, e não pela rotina nativa da plataforma, na
[ADR-0008](../docs/decisoes/0008-agendamento-da-cadencia.md).

### Configuração

O que é **parâmetro do projeto** fica versionado em
`rotinas/configuracao/agenda.json`, montado no contêiner em `/configuracao`:
lembretes em D+4, D+7 e D+14, intervalo mínimo de 3 dias, janela de 60 dias,
horário, dias da semana, feriados, calendário de término de semestre (a âncora da
turma), tolerância e intervalo das devoluções. A rotina **recusa** cadência fora da
faixa admissível da seção 5.1 de
[`parametros-contato.md`](../docs/especificacao/parametros-contato.md), a menos que
`registro_fora_da_faixa` aponte o registro que a seção exige. Os feriados e o
calendário são **valores de ensaio**, a substituir pelos da instituição.

O que **muda de um ambiente para outro** fica no `.env`:

| Variável | Valor no ensaio | Para quê |
|---|---|---|
| `ROTINA_DISPARO` | `simulado` | `simulado` roda no horário, confere a guarda, calcula e registra o plano, e **não envia**; `real` envia |
| `ROTINA_QUESTIONARIO` | `202615` | questionário do ciclo corrente |
| `ROTINA_CICLO` | `2026` | ano do ciclo, que transforma a âncora da turma em data |
| `ROTINA_HORARIO` | vazio | sobrescreve o horário; **só para verificação** |

Depois de mudar o `.env` ou a agenda, recrie o contêiner:

```bash
docker compose up -d rotinas
```

**Atenção ao ligar o modo real numa base recém-importada:** a primeira execução
convida todos cuja âncora já passou no ciclo. No ensaio, em 05/10/2026, eram 255 dos
500 — os de conclusão no 1º semestre; os do 2º têm âncora em 15/12.

### Acompanhando

O log do agendador diz o que fez, sem nome nem endereço:

```bash
docker compose logs -f rotinas
```

Cada execução fica em `egressos_execucoes`: tarefa, modo, horário **previsto** e
**real**, situação e resumo. Cada envio tentado fica em `egressos_disparos`:
participante (`tid` e `participant_id`), convite ou lembrete, número, ramo, estado de
partida e resultado. Nenhuma das duas guarda token, nome ou endereço. Uma execução
que não aconteceu no horário — máquina desligada, distribuição parada, hospedeiro
suspenso — aparece como `perdida`:

```sql
SELECT previsto_para, iniciado_em, situacao, modo
  FROM egressos_execucoes WHERE tarefa = 'disparo' ORDER BY id DESC LIMIT 10;
```

Para ver o plano de agora sem esperar o horário, e sem enviar nada:

```bash
docker compose exec rotinas python3 disparar.py --simular
```

O disparo manual em modo real (`python3 disparar.py`, sem `--simular`) existe para
emergência, fica registrado como `manual` e é recusado fora de dia útil.

### A guarda

Antes de cada disparo, a rotina confere e **não dispara** se algo falhar: as
conferências 1 a 7 da E19 (a mesma lógica de `confere-participantes.py`, que desde
a E21 vive em `scripts/conferencia_participantes.py`), o questionário ativo e de
acesso fechado, o remetente e o retorno nas caixas do `.env`, sob `.test`, e o
lembrete escolhendo o ramo pelo atributo `variante_lembrete`. O resultado vai para o
log e para `egressos_execucoes`, com a situação `bloqueada`.

### Conferindo

```bash
python3 confere-rotina.py                 # regras da cadência, sem plataforma
python3 confere-rotina.py --agendada      # o disparo real, no horário, e desfaz
python3 confere-rotina.py --perdida       # o registro de execução perdida, e desfaz
```

`--agendada` planta catorze participantes do instrumento, um por situação, aponta o
agendador para um **ciclo de teste** (2099, âncora no futuro, de modo que os outros
486 não vencem convite) em modo real, com horário daqui a poucos minutos, e confere
que a execução começou no horário e que receberam mensagem exatamente os que
deviam. Desfaz tudo e devolve o agendador ao que o `.env` diz. Os valores de teste
entram pelo ambiente do comando, que tem precedência sobre o arquivo: o `.env`
**não é editado**. Precisa de dia útil e da rotina já ter feito ao menos uma
execução agendada do ciclo corrente.

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

## Conformidade (E23)

Depois de implantar e ativar o instrumento, **numa instalação do zero**:

```bash
python3 conformidade.py aplicar
```

Ativa a trilha de auditoria da plataforma (`AuditLog`) por comando de console — sem
tela —, confere a lista de bloqueio nos padrões que o mecanismo exige
(`deleteblacklisted = N`, `allowunblacklist = N`, `blockaddingtosurveys = Y`) e
confere que a imagem tem a correção do `AuditLog` (seção 4.2 do
`limesurvey/Dockerfile`), sem a qual gravar na base central por console quebra com a
trilha ativa. Idempotente.

A revogação de uma recusa de contato, a pedido do egresso por resposta a uma
mensagem:

```bash
python3 conformidade.py revogar --identificador SIN-000123 \
    --registro "pedido por resposta de 05/10/2026 na caixa acompanhamento"
```

E a conferência:

```bash
python3 confere-conformidade.py               # só leitura
python3 confere-conformidade.py --exercitar   # as três vias, o ciclo seguinte, a revogação, e desfaz
```

Especificação em
[`docs/especificacao/conformidade.md`](../docs/especificacao/conformidade.md), e a
decisão na [ADR-0010](../docs/decisoes/0010-conformidade-no-mecanismo.md).

## O que ainda não está aqui

- **O reparo automático.** A operação de reparo existe desde a E26
  (`reparo-contato.py`), mas roda à mão, no hospedeiro, sobre a fila de correção: a
  base central só se grava por console, que o contêiner `rotinas` não alcança.
  Agendá-la é decisão de implantação (E30).
- **A virada de ciclo** — o questionário do ano seguinte. A rotina opera sobre o
  questionário configurado; o procedimento de abrir um ciclo novo é da E30.
- **A eliminação por prazo** — a política de retenção está escrita
  (`conformidade.md`, seção 8), com os anos a cargo da instituição; a rotina que
  elimina é da E30.

## Regras que valem para tudo o que entrar aqui

- O ambiente deve subir do zero usando **apenas o que está versionado** nesta pasta.
- Credenciais nunca entram. Só o `.env.exemplo`, sem valores reais.
- Imagens fixadas por digest; pacotes, por soma de verificação.
- Nenhuma configuração relevante pode existir **apenas** dentro do contêiner — o
  ambiente é efêmero e recriável por decisão, não por acidente.
