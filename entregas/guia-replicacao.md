# Guia de replicação

Mecanismo digital de acompanhamento de egressos em instância própria de
LimeSurvey, com rastreabilidade de participantes, automação de contato e
controles de conformidade.

**Estado deste guia.** As Partes I a III estão completas e foram verificadas por
execução. As Partes IV a VI serão escritas quando as etapas correspondentes
existirem — cada uma indica a sua. Esta versão permite **reproduzir o ambiente**;
ela ainda não descreve o instrumento nem a automação.

| Parte | Assunto | Estado |
|---|---|---|
| I | Requisitos e hospedeiro | completa |
| II | Instalação | completa |
| III | Segurança do ambiente | completa |
| IV | Estrutura do instrumento | pendente (E15) |
| V | Automação de contato | pendente (E21) |
| VI | Conformidade e recomendações | pendente (E22 a E24) |

---

## Antes de começar

### O que este guia entrega

Um ambiente completo e reproduzível: LimeSurvey em instância própria, banco de
dados, serviço de correio capaz de **devolver** erro, e um lugar de onde as
rotinas do projeto rodam. Tudo declarado em arquivos, subindo por comando, sem
conta em provedor e sem custo.

### O que ele não entrega, e é importante saber antes

**Este ambiente é de ensaio, e não de produção.** Ele foi desenhado para validar
o mecanismo sobre **base sintética**, em rede fechada, sem alcançar endereço real.
Vários ajustes deliberados o tornam impróprio para dados reais — estão todos
listados na **Parte III, seção 8**, que é a seção que você não deve pular.

**Ele não é a instância institucional.** O trabalho original ocorreu em ambiente
próprio porque a alteração do questionário institucional em produção não foi
autorizada. Replicar este guia produz um ambiente paralelo, não uma modificação
do que já existe na sua instituição.

**Nenhum dado pessoal real deve passar por aqui** enquanto os ajustes da seção 8
não forem feitos e, tratando-se de pesquisa com egressos, enquanto não houver
apreciação ética prévia.

### Convenções

Os comandos em bloco são para executar como estão, salvo onde houver
`<algo-entre-sinais>`, que você substitui. Comandos de PowerShell aparecem
marcados como tal; os demais são de shell Unix.

---

# Parte I — Requisitos e hospedeiro

## 1. O que é preciso ter

| Requisito | Observação |
|---|---|
| **Docker Engine** e o plugin **Compose** | é tudo o que a composição exige |
| cerca de **4 GB** de memória livre | os quatro serviços juntos |
| cerca de **8 GB** de disco | imagens e volumes |
| acesso à internet **na construção** | para baixar imagens e o pacote do LimeSurvey; depois de construído, o ambiente roda isolado |
| `git` | para obter o repositório |
| `python3` | para dois dos verificadores |

**Não é preciso**: conta em provedor de nuvem, meio de pagamento, servidor,
domínio, certificado, nem acesso a qualquer sistema institucional.

**Não se usa o Docker Desktop.** Ele é gratuito para uso pessoal, educacional e
para organizações abaixo de 250 funcionários e de US$ 10 milhões de receita
anual, e exige assinatura paga acima de qualquer um desses limiares — um
instituto federal não cabe no limiar de porte. O **Docker Engine** é distribuído
sob licença Apache 2.0, sem limiar algum, e é o que este guia usa. A decisão está
registrada em [ADR-0002](../docs/decisoes/0002-ambiente-execucao.md).

## 2. Obtendo um hospedeiro Docker

Esta seção é a única do guia que depende do seu sistema operacional. **A
composição é a mesma em todos os casos** — o hospedeiro é a peça trocável.

### 2.1 Linux (Debian ou Ubuntu)

O repositório traz o script:

```bash
sudo ./infra/hospedeiro/provisiona-docker.sh
```

Ele instala o Docker Engine a partir do repositório oficial do Docker, é
idempotente e, se detectar WSL, habilita o `systemd`. Em outras distribuições
Linux, instale o Docker Engine pela documentação oficial do Docker e siga daqui.

### 2.2 macOS

Instale o Docker Engine por um gerenciador de contêineres que não seja o Docker
Desktop, ou aceite as condições de licença dele se a sua organização couber nos
limiares. Daqui em diante o procedimento é idêntico.

### 2.3 Windows, com WSL2

Primeiro a distribuição:

```powershell
wsl --install -d Ubuntu-24.04
```

Depois o Docker, de dentro dela, com o script da seção 2.1. Se ele disser que
habilitou o `systemd`, reinicie com `wsl --shutdown` antes de seguir.

**Um ajuste que o WSL exige e que não é opcional.** O WSL encerra a distribuição
quando ela fica ociosa — por padrão, 15 segundos sem sessão. Com os contêineres
dentro dela, o ambiente cai sozinho. Crie `%UserProfile%\.wslconfig`:

```ini
[general]
instanceIdleTimeout = -1
```

E reinicie com `wsl --shutdown`. Vale para todas as distribuições da máquina; para
desfazer, apague o arquivo e reinicie.

Três coisas a saber sobre esse ajuste, todas aprendidas por erro:

- **É `instanceIdleTimeout`, da seção `[general]`.** Existe uma configuração
  parecida, `vmIdleTimeout`, na seção `[wsl2]`: aquela governa a máquina virtual,
  só aceita milissegundos e não tem como desligar. A que governa a **distribuição**
  é a primeira, e é a única que aceita `-1`.
- **Grave o arquivo sem marcador de ordem de bytes.** O WSL trata um `.wslconfig`
  malformado como inexistente e **não avisa**. O sintoma é indistinguível de "a
  configuração não funcionou".
- **Para conferir, espere do lado do Windows.** Um teste que espera *dentro* da
  distribuição mantém uma sessão ativa e dá falso positivo:

  ```powershell
  $a = [int]((wsl -d Ubuntu-24.04 -u root -- cat /proc/uptime).Split(".")[0])
  Start-Sleep -Seconds 220
  $b = [int]((wsl -d Ubuntu-24.04 -u root -- cat /proc/uptime).Split(".")[0])
  "antes=$a depois=$b"
  ```

  Se o valor cresceu, a distribuição sobreviveu.

**O que esse ajuste não resolve.** Se o Windows suspender ou hibernar, a máquina
virtual suspende de todo modo e, na retomada, o **relógio dela salta**. Isso faz o
servidor IMAP recusar conexões com o contêiner aparentemente saudável. O serviço
de correio deste projeto mantém supervisão própria justamente por isso. Em Linux
nativo nada disso ocorre.

### 2.4 Servidor institucional

É o caso mais simples e o mais adequado a uso contínuo: instale o Docker Engine e
siga para a Parte II. Leia a **Parte III, seção 8** antes de expor o serviço a
qualquer rede.

### 2.5 Conferindo o hospedeiro

```bash
docker --version
docker compose version
docker run --rm hello-world
```

---

# Parte II — Instalação

## 3. Obter o repositório

```bash
git clone https://github.com/matheusreisl/projeto-egressos-ifsp-estrutura.git
cd projeto-egressos-ifsp-estrutura/infra
```

Todos os comandos das seções seguintes correm de dentro de `infra/`.

## 4. Configurar

```bash
cp .env.exemplo .env
```

Abra o `.env` e defina as quatro senhas. Para gerar cada uma:

```bash
openssl rand -base64 24
```

| Variável | Para quê |
|---|---|
| `BANCO_SENHA` | usuário do banco usado pela aplicação |
| `BANCO_SENHA_ROOT` | administrador do banco |
| `ADMIN_SENHA` | administrador do LimeSurvey, criado na instalação |
| `CORREIO_SENHA` | caixas do serviço de correio, lidas pela rotina de devoluções |

As demais variáveis têm valores de trabalho e estão comentadas no próprio
arquivo. **Duas merecem atenção:**

- **`CORREIO_DOMINIO` e as duas irmãs** estão sob o TLD reservado `.test`, que não
  resolve na internet pública. **Não troque por domínio real.** Os três domínios
  não são decorativos: cada um produz um resultado diferente e necessário — entrega
  normal, devolução permanente e devolução temporária.
- **`ENDERECO_BIND`** vem em `127.0.0.1`, o que significa que só a própria máquina
  alcança o painel. Trocar por `0.0.0.0` em hospedeiro Linux **expõe o painel na
  rede**.

O `.env` **não é versionado**. O repositório é público, e só o `.env.exemplo`, sem
valores reais, entra nele.

## 5. Subir

```bash
docker compose up -d --build
```

A primeira construção baixa o pacote do LimeSurvey — cerca de 123 MB — e compila
as extensões do PHP. Leva alguns minutos; as seguintes reaproveitam o cache.

**A instalação do LimeSurvey é desatendida.** Não há instalador web a percorrer: a
inicialização do contêiner gera o `application/config/config.php` a partir do
`.env` e executa o instalador de console quando o banco está vazio. As duas
operações são idempotentes, de modo que `docker compose down -v` seguido de
`up -d` devolve uma instância pronta, sem passo manual no meio.

Acompanhe até os serviços ficarem saudáveis:

```bash
docker compose ps
```

O painel responde em `http://127.0.0.1:8080`, com o usuário e a senha definidos no
`.env`.

## 6. Conferir

São três verificações, e elas conferem coisas diferentes. Rode as três.

```bash
./verifica-ambiente.sh
```

Confere as propriedades do ambiente: serviços de pé, porta publicada, contenção de
rede e extensões do PHP presentes. **Resultado esperado: 21 conferências, todas
passando.**

```bash
python3 confere-capacidades.py
```

Confere que a instância tem as capacidades de que a especificação depende, criando
um questionário de teste descartável e removendo-o ao final. **Resultado esperado:
7 capacidades atendidas e 3 parciais** — as parciais são conhecidas e estão
detalhadas em
[`capacidades-plataforma.md`](../docs/especificacao/capacidades-plataforma.md).

```bash
docker compose exec rotinas python3 verifica_correio.py
```

Confere o correio **nas duas direções** — envio e devolução — e a classificação do
retorno. **Resultado esperado: 7 conferências, todas passando.** Leva alguns
minutos, porque o aviso de atraso que produz a devolução temporária não é
imediato.

```bash
python3 confere-envio.py
```

Confere a integração: a instância dispara os convites, a devolução volta, a rotina
classifica e o estado do participante muda. **Resultado esperado: 7 conferências,
todas passando.**

### Voltando ao estado zero

```bash
docker compose down        # para os serviços, preserva os dados
docker compose down -v     # APAGA os volumes: banco, configuração e envios
```

O segundo é o que devolve o ambiente ao nada. É ele que torna verificável a
afirmação de que o ambiente sobe a partir apenas do que está versionado.

---

# Parte III — Segurança do ambiente

## 7. O que está aplicado

| Controle | Como |
|---|---|
| Painel não exposto na rede | porta vinculada a `127.0.0.1` |
| Banco não alcançável de fora | nenhuma porta publicada |
| Correio não alcançável de fora | nenhuma porta publicada |
| Banco, correio e rotinas **sem rota para a internet** | rede declarada como `internal` |
| Credenciais fora do repositório | somente em `.env`, ignorado pelo Git |
| Senha do administrador não persistida | usada só na instalação, por arquivo temporário removido em seguida |
| Versões fixadas | imagens por digest; pacote do LimeSurvey por versão **e** soma SHA-256, conferida antes de descompactar |
| Mensagens de erro não expostas | `debug = 0` |

**A contenção do correio merece uma frase própria**, porque é o que impede o pior
acidente possível num ambiente de ensaio. O serviço de correio fica **somente** na
rede interna, que não tem rota de saída. Consequência: nenhuma mensagem deixa a
máquina, **qualquer que seja o endereço de destino** — inclusive um endereço real
digitado por engano no arquivo de participantes. A proteção é do ambiente, não da
atenção de quem opera.

O contêiner do LimeSurvey é o único que mantém saída HTTP, porque publicar porta
exige rede não interna. Ele não origina mensagem por conta própria: entrega pelo
serviço de correio configurado.

## 8. O que precisa mudar antes de tocar dado real

**Esta é a seção que não se pula.** O ambiente acima é adequado a ensaio com base
sintética e **inadequado a dados pessoais reais**. Cada item abaixo é um ajuste
deliberado que torna o ensaio possível e que precisa ser desfeito.

| O que está assim | Por que, no ensaio | O que fazer antes de dado real |
|---|---|---|
| **Sem TLS**, em nenhum serviço | a rede é fechada e nada trafega fora dela | certificado válido e HTTPS obrigatório no painel e no acesso do respondente |
| **Correio sem autenticação** | só a própria composição o alcança | correio institucional, com autenticação, e remetente identificável |
| **Interface RPC habilitada** | as rotinas do projeto dependem dela | avaliar restringir o acesso, ou desabilitar quando não houver rotina em uso |
| **Domínios sob `.test`** | garantem que nada saia | domínios reais, e então a contenção deixa de existir — a partir daí, todo endereço de destino é um endereço de verdade |
| **Rede sem saída** | é a contenção | uma implantação real precisa entregar mensagens, logo terá saída. **A proteção contra disparo indevido passa a ser processual**, e precisa ser desenhada |
| **Senhas geradas localmente** | descartáveis | segredos sob gestão institucional, com rotação |
| **Hospedeiro que pode ser desligado** | o ensaio não precisa de continuidade | hospedeiro que permanece ligado, com rotina de atualização e de cópia de segurança |
| **Imagem construída localmente** | dá cadeia de confiança até o código oficial | a manutenção das correções de segurança do PHP e do LimeSurvey passa a ser sua: defina quem reconstrói e quando |

**Duas advertências que não são de configuração.**

A primeira: **o mecanismo trata dados pessoais de egressos.** Uma implantação real
exige base legal definida sob a LGPD, registro de consentimento, política de
retenção e trilha de auditoria — e o trabalho original recomenda expressamente
**apreciação ética prévia** a qualquer aplicação junto a egressos reais.

A segunda: **não use capturador de SMTP no lugar do serviço de correio.** É o
atalho natural de quem monta ambiente de ensaio, e ele funciona para ver mensagens
saindo. Mas capturadores aceitam tudo e **nunca devolvem erro**, de modo que a
verificação de entrega — que é o que permite identificar contato inválido — fica
impossível. O ambiente parece funcionar e o mecanismo fica sem uma de suas partes.
A explicação está em
[`leitura-devolucoes.md`](../docs/especificacao/leitura-devolucoes.md).

---

# Parte IV — Estrutura do instrumento

*Pendente. Será escrita na E30, a partir da estrutura definida na E15.*

Cobrirá: blocos do instrumento, domínios de valores, obrigatoriedade, navegação
condicional e como importar a estrutura versionada numa instância nova.

# Parte V — Automação de contato

*Pendente. Será escrita na E30, a partir da automação definida na E21.*

Cobrirá: base de participantes, endereços individuais, modelos de mensagem,
cadência de disparo, rotina agendada e leitura de devoluções em operação.

# Parte VI — Conformidade e recomendações

*Pendente. Será escrita na E30, a partir das etapas E22 a E24.*

Cobrirá: consentimento eletrônico com as duas manifestações de recusa,
anonimização, trilha de auditoria, e as recomendações que dependem de ação
institucional — divulgação em colação de grau, mobilização por turmas e ações
dirigidas a turmas antigas.

---

# Apêndice A — Quando algo não funciona

Reunidas aqui as falhas que de fato ocorreram durante o desenvolvimento, com o
que as causa. Todas têm em comum o sintoma enganar.

### O painel não responde em `localhost`, mas responde pelo IP da distribuição

Encaminhamento obsoleto do WSL, depois de a distribuição ser reaberta no meio de
uma sessão. **Não é o endereço de vínculo** — trocar `ENDERECO_BIND` faz o painel
voltar pelo IP e dá a impressão de resolver. O que resolve:

```powershell
wsl --shutdown
```

### Os contêineres reaparecem com poucos segundos de atividade

A distribuição está sendo encerrada por ociosidade. Ver a seção 2.3.

### O IMAP recusa conexão, com o contêiner saudável

Salto de relógio da máquina virtual, depois de suspensão do hospedeiro. O serviço
tem supervisão que o recria — verificado: matando o Dovecot, o contêiner volta em
cerca de 20 segundos. Se persistir, `wsl --shutdown` e subir de novo.

### O `.wslconfig` parece não ter efeito

Provavelmente está malformado, e o WSL o ignora **sem avisar**. A causa mais comum
é marcador de ordem de bytes no início do arquivo.

### A devolução de erro não chega

Três causas possíveis, e nenhuma é óbvia:

1. **A recusa veio síncrona, no diálogo SMTP**, e não houve devolução a ler. O
   parâmetro `local_recipient_maps` precisa estar **vazio**, o que faz o servidor
   aceitar a mensagem e falhar na entrega.
2. **O domínio indisponível não está em `relay_domains`.** Sem isso o servidor
   responde `454 Relay access denied` no diálogo, e de novo não há devolução.
3. **Você está esperando a devolução temporária de imediato.** Ela não é imediata:
   sai depois do aviso de atraso, reduzido a um minuto no ambiente de ensaio e
   medido em horas numa implantação real.

### `No candidate tokens` ao disparar convites

Chamada com lista **vazia** de participantes, que a API traduz num conjunto vazio
em vez de "todos". Omita o parâmetro.

### Uma consulta ao banco não encontra a tabela de respostas

No LimeSurvey 7 ela é `lime_responses_<id>`, e não `lime_survey_<id>`, que é o nome
usado pela documentação e pelos tutoriais antigos.

---

# Apêndice B — Onde está o quê

| Documento | Assunto |
|---|---|
| [ADR-0002](../docs/decisoes/0002-ambiente-execucao.md) | por que conteinerização local, e não nuvem ou máquina virtual |
| [ADR-0003](../docs/decisoes/0003-canal-alternativo-nao-automatizado.md) | por que o convite por mensagem instantânea não é automatizado |
| [ADR-0004](../docs/decisoes/0004-imagem-propria-e-leitura-de-devolucoes.md) | por que imagem própria, e por que a leitura de devoluções é rotina do projeto |
| [parametros-contato.md](../docs/especificacao/parametros-contato.md) | cadência, tratamento da recusa, verificação de entrega |
| [capacidades-plataforma.md](../docs/especificacao/capacidades-plataforma.md) | o que a plataforma suporta, conferido contra a instância |
| [leitura-devolucoes.md](../docs/especificacao/leitura-devolucoes.md) | desenho do correio de ensaio e classificação do retorno |
| [infra/README.md](../infra/README.md) | referência operacional do ambiente |
| [scripts/README.md](../scripts/README.md) | as rotinas do projeto |
