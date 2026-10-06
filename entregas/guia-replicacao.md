# Guia de replicação

Mecanismo digital de acompanhamento de egressos em instância própria de
LimeSurvey, com rastreabilidade de participantes, automação de contato e
controles de conformidade.

**Estado deste guia.** As Partes I a III estão completas e foram verificadas por
execução. Da Parte VI, estão escritas as recomendações que dependem de ação
institucional. O restante será escrito quando as etapas correspondentes existirem —
cada parte indica a sua. Esta versão permite **reproduzir o ambiente**; ela ainda
não descreve o instrumento nem a automação.

| Parte | Assunto | Estado |
|---|---|---|
| I | Requisitos e hospedeiro | completa |
| II | Instalação | completa |
| III | Segurança do ambiente | completa |
| IV | Estrutura do instrumento | pendente (E15) |
| V | Automação de contato | pendente (E21) |
| VI | Conformidade e recomendações | recomendações completas (E24); conformidade pendente (E22 e E23) |

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

# Parte I — Requisitos, repositório e hospedeiro

## 1. O que é preciso ter

| Requisito | Observação |
|---|---|
| **Docker Engine** e o plugin **Compose** | é tudo o que a composição exige |
| cerca de **8 GB** de disco | ver a medição abaixo |
| acesso à internet **na construção** | para baixar imagens e o pacote do LimeSurvey; depois de construído, o ambiente roda isolado |
| `git` | para obter o repositório |
| `python3` | para dois dos verificadores |

**Disco, medido.** As imagens ocupam cerca de **2,8 GB** no total: LimeSurvey
1,98 GB, MariaDB 455 MB, correio 211 MB e rotinas 190 MB. O cache de construção
acrescenta alguns gigabytes, e os volumes crescem com o uso — daí a folga de 8 GB.

A imagem do LimeSurvey é grande porque as dependências de compilação das
extensões do PHP **são mantidas de propósito**: purgá-las economizaria centenas de
megabytes ao custo de um bloco difícil de ler, e essa imagem é antes de tudo um
documento de instalação destinado a ser lido. Numa implantação real o ajuste é
legítimo.

**Memória, medida em repouso.** Os quatro contêineres somam cerca de **200 MB**:
banco 96 MB, LimeSurvey 76 MB, correio 28 MB e rotinas 1,6 MB. Sob carga de
simulação isso cresce, mas a ordem de grandeza é essa — o consumo dos contêineres
não é o fator limitante. Num hospedeiro WSL, o que pesa é a memória que a própria
máquina virtual reserva, metade da RAM da máquina por padrão, ajustável em
`.wslconfig`.

**Não é preciso**: conta em provedor de nuvem, meio de pagamento, servidor,
domínio, certificado, nem acesso a qualquer sistema institucional.

**Não se usa o Docker Desktop.** Ele é gratuito para uso pessoal, educacional e
para organizações abaixo de 250 funcionários e de US$ 10 milhões de receita
anual, e exige assinatura paga acima de qualquer um desses limiares — um
instituto federal não cabe no limiar de porte. O **Docker Engine** é distribuído
sob licença Apache 2.0, sem limiar algum, e é o que este guia usa. A decisão está
registrada em [ADR-0002](../docs/decisoes/0002-ambiente-execucao.md).

## 2. Obter o repositório

Isto vem antes do hospedeiro, porque o script que instala o Docker está no
repositório:

```bash
git clone https://github.com/matheusreisl/projeto-egressos-ifsp-estrutura.git
cd projeto-egressos-ifsp-estrutura
```

## 3. Obtendo um hospedeiro Docker

Esta seção é a única do guia que depende do seu sistema operacional. **A
composição é a mesma em todos os casos** — o hospedeiro é a peça trocável.

### 3.1 Linux (Debian ou Ubuntu)

O repositório traz o script:

```bash
sudo ./infra/hospedeiro/provisiona-docker.sh
```

Ele instala o Docker Engine a partir do repositório oficial do Docker, é
idempotente e, se detectar WSL, habilita o `systemd`. Em outras distribuições
Linux, instale o Docker Engine pela documentação oficial do Docker e siga daqui.

### 3.2 macOS

Instale o Docker Engine por um gerenciador de contêineres que não seja o Docker
Desktop, ou aceite as condições de licença dele se a sua organização couber nos
limiares. Daqui em diante o procedimento é idêntico.

### 3.3 Windows, com WSL2

Primeiro a distribuição:

```powershell
wsl --install -d Ubuntu-24.04
```

Depois o Docker, de dentro dela, com o script da seção 3.1. Se ele disser que
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

### 3.4 Servidor institucional

É o caso mais simples e o mais adequado a uso contínuo: instale o Docker Engine e
siga para a Parte II. Leia a **Parte III, seção 8** antes de expor o serviço a
qualquer rede.

### 3.5 Conferindo o hospedeiro

```bash
docker --version
docker compose version
docker run --rm hello-world
```

---

# Parte II — Instalação

Todos os comandos desta parte correm de dentro de `infra/`, no repositório que
você clonou na seção 2:

```bash
cd infra
```

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
| **Sem TLS**, em nenhum serviço — inclusive no banco | a rede é fechada, nada trafega fora dela e nenhum serviço além do painel publica porta | certificado válido e HTTPS obrigatório no painel e no acesso do respondente; e TLS no banco, se ele passar a ser alcançável por outra máquina |
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

## 9. Conformidade

*Pendente. Será escrita na E30, a partir das etapas E22 e E23.*

Cobrirá: consentimento eletrônico com as duas manifestações de recusa,
anonimização e trilha de auditoria.

## 10. Recomendações que dependem de ação institucional

O mecanismo deste guia entrega o que se configura: lista fechada de participantes,
endereço individual, convite, lembrete só a quem não respondeu, registro da recusa.
Parte do que a literatura e a norma associam à participação dos egressos não se
configura em plataforma alguma. Depende de quem coordena o curso, de quem administra
um grupo de turma, de quem organiza a colação de grau ou um encontro de ex-alunos.
Esta seção reúne essas ações como **recomendação de implantação**. Nenhuma foi
executada no ensaio, que não contatou ninguém.

As referências normativas são as do IFSP: o Regulamento do Programa de
Acompanhamento de Egressos (Portaria Normativa nº 128/2025), citado só pelo artigo,
e a Política de Acompanhamento de Egressos (Resolução Normativa nº 13/2022), citada
como PAEg. Outra instituição troca-as pelas suas; as recomendações não dependem
delas.

### 10.1 Como ler

Cada recomendação traz a evidência que a sustenta, com o estado na escala do
[quadro de engajamento](../docs/pesquisa/quadro-engajamento.md), acrescida de um
rótulo:

| Estado | Significado |
|---|---|
| **medido** | número de resposta com denominador declarado, atribuível à estratégia, entre egressos |
| **medido em outra população** | efeito estimado por ensaio randomizado, com participantes que não são egressos — rótulo da revisão de [Edwards et al. (2023)](../docs/pesquisa/fichamentos/edwards-2023.md), acrescentado ao quadro na seção 1.3 |
| **relatado** | a fonte afirma ou sugere o efeito, sem medir, ou sem separar de outras ações |
| **não avaliado** | a fonte descreve a prática e não trata do efeito |

Duas advertências valem para todas. **Nenhuma recomendação tem efeito medido entre
egressos**, e nenhuma fonte as compara: a ordem abaixo não é ranking. E **nenhuma
permite projetar taxa de resposta.** O que oferecem é condição — contato correto,
convite esperado e reconhecível, egresso que sabe para que responde — que a
literatura associa à participação. É o mesmo limite do mecanismo, que entrega
capacidade instalada de cobrança sistemática, e não taxa.

### 10.2 A regra que vale para todas: canal coletivo avisa, não leva endereço

Quase toda ação desta seção passa por canal coletivo — cerimônia, grupo, rede
social, portal, cartaz. Há duas formas de, por ele, desfazer o mecanismo sem
perceber.

**Publicar um endereço comum de resposta** — no grupo, na postagem, no código QR do
cartaz, no telão da colação, na página de egressos. Quem responde por ele fica fora
da lista fechada: não entra no denominador, não tem unicidade nem elegibilidade
conferidas, e continua recebendo lembrete, porque para o mecanismo não respondeu. Os
dois relatórios da Rede Federal no conjunto mostram o resultado: o
[Ifes](../docs/pesquisa/fichamentos/ifes-2025.md) difundiu o link em grupos de
WhatsApp e chegou a 1.840 respostas sem denominador; o
[IFAL](../docs/pesquisa/fichamentos/ifal-2024.md) difundiu o seu no Instagram e em
grupos, e teve de descartar respostas de formados fora do recorte.

**Publicar endereços individuais em lista** — a mensagem de grupo com o link de cada
um. O endereço individual é transportável por desenho
([ADR-0003](../docs/decisoes/0003-canal-alternativo-nao-automatizado.md)), e quem o
tem responde como o egresso: vê os dados acadêmicos pré-preenchidos dele e pode, na
tela inicial, registrar em nome dele a recusa de contato, que o mecanismo trata como
permanente até revogação.

O que o canal coletivo leva é **aviso**: o convite individual foi enviado em tal
data, pelo remetente tal, com o assunto tal; procure também no lixo eletrônico; se
não recebeu, escreva para o endereço de retorno. O endereço de resposta só vai em
mensagem a uma pessoa — o convite por e-mail, ou a entrega da R3.

### 10.3 Quadro-resumo

| | Recomendação | Quem executa, no IFSP | Evidência | Estado mais forte |
|---|---|---|---|---|
| R1 | Colação de grau: avisar do convite e acertar o contato | coordenador de curso e setor indicado pelo campus (arts. 10 e 22) | IFAL (2024); Coelho e Silva (2017); Edwards et al. (2023) | medido em outra população, inconclusivo no eletrônico |
| R2 | Grupos de turma: o grupo avisa, não distribui | coordenadores, colegiados e CEICs; quem administra o grupo (arts. 9º, 19 e 26) | Ifes (2025); IFAL (2024); Edwards et al. (2023) | medido em outra população |
| R3 | Canal alternativo: uma pessoa entrega o endereço individual | setor indicado pelo campus (arts. 10 e 16, §1º) | Coelho e Silva (2017); Ifes (2025) | relatado |
| R4 | Turmas antigas: ver a não resposta por turma e reparar o contato | setor indicado pelo campus; Diretoria-Geral, nos Jubileus (art. 10; PAEg, art. 19) | Ifes (2025); IFAL (2024); Coelho e Silva (2017); Alvares et al. (2020) | relatado |
| R5 | Divulgação institucional e Portal do Egresso sem link aberto | comunicação dos campi; COPAEG (arts. 22, 26 e 29) | Ifes (2025); IFAL (2024); linha de base; Edwards et al. (2023) | medido em outra população |
| R6 | Contrapartidas oferecidas por fora, e resultados devolvidos | setor indicado pelo campus; COPAEG (art. 3º; arts. 23, 24, 26 e 27) | Edwards et al. (2023); IFAL (2024); Alumni USP; Cabral et al. (2016) | medido em outra população, só para a devolução dos resultados |
| R7 | Colaboração voluntária com termo próprio, fora do questionário | servidor efetivo do campus (art. 40; PAEg, art. 18) | Alumni USP; Cabral et al. (2016) | relatado, por ligação indireta |
| R8 | Portal de relacionamento, quando couber | COPAEG (arts. 8º, item 4, 28 e 29) | Cabral et al. (2016); Alumni USP | relatado |

### 10.4 R1 — Colação de grau: avisar do convite e acertar o contato

**O que fazer.** Na colação de grau, ou na mensagem que o coordenador envia aos
concluintes:

1. **anunciar o convite** — ao término do semestre de conclusão chegará, por e-mail,
   um convite individual, deste remetente e com este assunto (os da P7, em
   [`parametros-contato.md`](../docs/especificacao/parametros-contato.md));
2. **pedir que o concluinte confira o contato no sistema acadêmico** — e-mail,
   segundo e-mail e telefone — e o corrija lá, com um endereço que continue em uso
   depois da conclusão;
3. **não exibir endereço nem código QR do questionário.**

O contato corrigido no sistema acadêmico chega ao mecanismo pela extração seguinte,
porque valor novo na origem prevalece sobre o anterior
([`importacao-base.md`](../docs/especificacao/importacao-base.md), seção 5). Coletar
contato por formulário paralelo criaria uma segunda origem, sem regra. O segundo
e-mail é o `email_alternativo` do leiaute de entrada: a única via de reparo que o
mecanismo prevê sem ação humana.

**Quando.** A colação fica perto da âncora do primeiro ciclo — o término do
semestre de conclusão (P5) —, antes ou depois do convite, conforme o calendário do
campus. Se vier depois, o aviso diz que o convite **já** foi enviado.

**Evidência.**

- [IFAL (2024)](../docs/pesquisa/fichamentos/ifal-2024.md) — *relatado*. Dos 5.472
  diplomados, nem todos tinham e-mail ativo no sistema acadêmico. O relatório
  atribui a perda ao e-mail da matrícula que ninguém revisa, ao e-mail de familiar e
  ao endereço inválido, e recomenda atualizar o cadastro **no momento da conclusão**.
  É observação da operação; o efeito da atualização não foi medido.
- [Coelho e Silva (2017)](../docs/pesquisa/fichamentos/coelho-2017.md) — *relatado*.
  Caixas postais inativas obrigaram à busca ativa por telefone e redes sociais para
  refazer os e-mails: o custo da correção tardia, viável para 79 egressos e não para
  milhares.
- [Edwards et al. (2023)](../docs/pesquisa/fichamentos/edwards-2023.md) — *medido em
  outra população*. O contato prévio ao envio aumentou a resposta a questionários
  postais (59 ensaios; OR 1,36; IC 95% 1,23–1,51). No questionário eletrônico, a
  estimativa vai no mesmo sentido, mas é **inconclusiva** (3 ensaios; OR 1,85; IC 95%
  0,99–3,45). Nenhum ensaio testou aviso feito em cerimônia.

**Norma.** O Regulamento já manda divulgar aos pré-egressos, pelo coordenador, no
momento da colação (art. 22), e pede ao egresso que mantenha o contato atualizado
(art. 13, item 1). A recomendação diz **o que** a divulgação leva.

### 10.5 R2 — Grupos de turma: o grupo avisa, não distribui

**O que fazer.** Quem integra ou administra o grupo — coordenador, docente,
representante de turma — publica o aviso da regra comum, nas datas do convite e dos
lembretes. A quem pedir o endereço no grupo, a resposta vai em mensagem privada, pela
via da R3. O próprio convite diz ao egresso que o endereço é individual e não deve
ser repassado ([`modelos-mensagem.md`](../docs/especificacao/modelos-mensagem.md)).

**Evidência.**

- [Ifes (2025)](../docs/pesquisa/fichamentos/ifes-2025.md) — *relatado*. Link
  difundido em grupos de WhatsApp de ex-alunos, junto com outras três ações, sem
  medição separada. Cerca de 80% dos respondentes tinham de 18 a 35 anos, e a maioria
  concluíra nos últimos dez anos: o grupo alcança quem continua nele.
- [IFAL (2024)](../docs/pesquisa/fichamentos/ifal-2024.md) — *relatado*. Link público
  em grupos e no Instagram; 20,9% dos respondentes citaram grupos de WhatsApp como
  fonte de notícias do instituto — medido entre quem respondeu, e por isso circular.
- [Edwards et al. (2023)](../docs/pesquisa/fichamentos/edwards-2023.md) — *medido em
  outra população*. Saudação e carta personalizadas aumentaram a resposta a
  questionários eletrônicos (12 ensaios; OR 1,24; IC 95% 1,17–1,32). É o argumento
  para que a mensagem coletiva **aponte** para o convite pessoal, e não o substitua.

**Norma.** O acompanhamento é por turma (art. 19), e o Regulamento já nomeia como
canais a comunicação interpessoal, a coordenação de curso e o WhatsApp dos campi
(art. 26, parágrafo único). A recomendação trata do que passa por eles.

### 10.6 R3 — Canal alternativo: uma pessoa entrega o endereço individual

**O que fazer.** Para o participante em `contato inválido` sem via alternativa que
funcione (P8), uma pessoa designada copia o endereço individual dele da base de
participantes e o envia por mensagem instantânea **privada** ao telefone registrado:
uma mensagem por pessoa, com o texto do convite, uma vez por ciclo, como o reconvite
(P4). Se o egresso responder com e-mail novo, a correção segue o reparo de contato do
mecanismo, e não edição avulsa na plataforma — o contato precisa mudar na base central
e no questionário ([`importacao-base.md`](../docs/especificacao/importacao-base.md),
seção 11).

**Quem.** O setor indicado pelo campus, que executa o programa (art. 10). A
[ADR-0003](../docs/decisoes/0003-canal-alternativo-nao-automatizado.md) deixou o canal
sem automação e pediu responsável definido; este é o responsável natural, porque já
trata os dados do programa. Convém que a mensagem saia de conta institucional, e não
de telefone pessoal, para que nome e número não fiquem em aparelho particular —
recomendação de projeto, pelo princípio da necessidade da LGPD, sem fonte que a
avalie.

**Evidência.**

- [Coelho e Silva (2017)](../docs/pesquisa/fichamentos/coelho-2017.md) — *relatado*.
  Busca ativa por telefone e redes sociais, parte dos 35,4% sem separação.
- [Ifes (2025)](../docs/pesquisa/fichamentos/ifes-2025.md) — *relatado*. Contato
  telefônico quando havia telefone, uma das quatro ações sem medição separada.

**Norma.** O art. 16, §1º, manda usar mensagens instantâneas quando o e-mail não for
possível. A conformidade do mecanismo a ele é parcial e declarada: entrega a
condição — o endereço transportável —, e não o envio.

### 10.7 R4 — Turmas antigas: ver a não resposta por turma e reparar o contato

**O problema.** O [Ifes](../docs/pesquisa/fichamentos/ifes-2025.md) teve respondentes
concentrados nas turmas da última década e atribuiu isso à proximidade dos canais —
descrição do viés, e não controle. O [IFAL](../docs/pesquisa/fichamentos/ifal-2024.md)
tomou o caminho oposto: restringiu a análise ao biênio e descartou os formados antes.

**O que o mecanismo muda, e o que não muda.** Com lista fechada, a não resposta por
turma fica **visível**: `ano_conclusao` e `semestre_conclusao` acompanham cada
participante, e convites, devoluções e respostas podem ser contados por turma. O Ifes
não podia, sem denominador; o IFAL, só para o biênio. Isso mostra onde a cobertura
cai, e não a eleva.

**O que fazer.**

1. **Não recortar em silêncio.** A população-alvo do Regulamento não tem limite de
   tempo (art. 18). Se a instituição recortar turmas, o recorte é decisão declarada,
   e não efeito do contato que envelheceu.
2. **Reparar antes de insistir.** Onde a contagem mostrar devoluções concentradas, a
   ação é busca ativa reparadora — por quem conhece a turma, como ex-coordenadores e
   docentes —, e não mais lembretes. É operação manual: priorizar as turmas com mais
   devoluções.
3. **Usar as ocasiões que a norma já cria** para atualizar o contato, pelo sistema
   acadêmico, e não para colher respostas: encontros de egressos (art. 10, item 5),
   premiações (art. 10, item 6) e os Jubileus de Prata e de Ouro, aos 25 e aos 50 anos
   de formado (PAEg, art. 19).

**Evidência.**

- [Ifes (2025)](../docs/pesquisa/fichamentos/ifes-2025.md) e
  [IFAL (2024)](../docs/pesquisa/fichamentos/ifal-2024.md) — *relatado*: o viés e as
  duas reações a ele.
- [Coelho e Silva (2017)](../docs/pesquisa/fichamentos/coelho-2017.md) — *relatado*:
  a busca ativa reparadora.
- [Alvares et al. (2020)](../docs/pesquisa/fichamentos/alvares-2020.md) — *não
  avaliado*: o distanciamento entre instituição e formado diminui com encontros
  regulares, contato por rede social e e-mails personalizados. Observação de passagem,
  vinda de quem optou por não contatar egressos.

**O que não se pode afirmar.** Que as turmas antigas respondem menos: nenhuma fonte
do conjunto mediu taxa por turma. O que há é a composição dos respondentes do Ifes.

### 10.8 R5 — Divulgação institucional e Portal do Egresso sem link aberto

**O que fazer.** A campanha institucional — sítio, redes, cartaz, a campanha dos dois
anos após a formatura (art. 22) — anuncia o ciclo, diz que o convite é individual e
por e-mail, diz para que servem as respostas e oferece a via do "não recebi": o
endereço de retorno ou o setor do campus. Assim a campanha alimenta o reparo de
contato, em vez de abrir uma segunda porta de resposta.

Ao adotar o mecanismo, **a página de egressos deixa de oferecer o questionário
aberto.** A do IFSP oferece hoje o instrumento vigente por link público (conferido
em 06/10/2026; ver a [linha de base](../docs/pesquisa/linha-de-base.md)). Com os dois
convivendo, a mesma pessoa responde duas vezes, as respostas abertas ficam sem
denominador, e quem respondeu pela porta aberta segue recebendo lembretes.

**Uma tensão na norma.** O Regulamento manda o link individual (art. 16), mas também
manda o questionário disponível **de forma contínua** no Portal do Egresso (art. 19,
§1º), acessível **a qualquer momento** depois da conclusão (art. 21), e põe entre as
finalidades do Portal disponibilizar o formulário (art. 29, item 4). Lidos ao pé da
letra, os três pedem uma porta aberta, e conflitam também com a janela de 60 dias da
P5. A linha de base confrontou o link aberto com o art. 16 e não registrou estes três
dispositivos. Três saídas, para a instituição decidir:

| Saída | Como fica | Custo |
|---|---|---|
| **Portal como porta de pedido** (recomendada) | o Portal explica o ciclo e recebe pedidos do endereço individual; quem opera confere a base e reenvia | fora da janela, o pedido espera o ciclo seguinte: reabrir a janela é exceção que o mecanismo hoje não prevê |
| Dois instrumentos separados | um questionário aberto no Portal, nunca somado aos indicadores do rastreável | duas bases, dois consentimentos, a mesma pessoa nas duas, e um número sem denominador ao lado do outro |
| Revisão da norma | a COPAEG ajusta os arts. 19, §1º, 21 e 29, item 4, ao art. 16, na revisão bienal (art. 39), com aprovação do Conselho de Extensão (PAEg, art. 13, §2º) | depende de deliberação |

A primeira resolve agora; a terceira resolve de vez.

**Evidência.**

- [Ifes (2025)](../docs/pesquisa/fichamentos/ifes-2025.md) — *relatado*: canais
  oficiais e cartaz, sem medição separada, e a perda de denominador do link público.
- [IFAL (2024)](../docs/pesquisa/fichamentos/ifal-2024.md) — *relatado*: o Instagram
  como canal de 87,9% dos respondentes — medido entre quem a campanha alcançou — e as
  respostas fora do recorte trazidas pelo link público.
- [Linha de base](../docs/pesquisa/linha-de-base.md) — a "Campanha de Egressos" do
  IFSP em 2018, sem avaliação registrada, e os 2.519 registros desde 2015 sem
  denominador.
- [Edwards et al. (2023)](../docs/pesquisa/fichamentos/edwards-2023.md) — *medido em
  outra população*: dizer o benefício da resposta para a sociedade aumentou a
  resposta a questionário eletrônico (OR 1,38; IC 95% 1,07–1,78). Sustenta o "para
  que servem as respostas" da campanha.

### 10.9 R6 — Contrapartidas oferecidas por fora, e resultados devolvidos

**O que fazer.**

1. **Devolver os resultados.** Publicar o resultado agregado e dizer ao egresso, no
   convite, onde ele estará. O Regulamento já manda divulgar os dados (arts. 15,
   item 4, 20, §3º, e 23) e produzir relatório bienal (art. 24); falta prometê-lo ao
   egresso e cumprir.

   **Onde.** No IFSP, a norma já indica um lugar: o Relatório de Perfil dos Egressos,
   feito com os dados da pesquisa, é publicado pelos meios do Portal do Egresso
   (art. 31, §1º, item 2, e §2º, item 6). Se a instituição mantiver um painel de
   indicadores, a camada pública dele — só com agregados, sem recorte que permita
   reconhecer alguém — pode ser o lugar, ou apontar para ele. Outra instituição
   escolhe o seu. A frase do convite entra em
   [`mensagens.py`](../infra/instrumento/mensagens.py) **só quando o lugar existir.**
   No ensaio ela não entra: os números da simulação não são resultado sobre egressos.
2. **Oferecer as ações de relacionamento que a norma lista, sem condicioná-las à
   resposta**: formação continuada, vagas de emprego, empreendedorismo, eventos e
   redes de relacionamento (art. 3º, itens 9, 10, 11, 13 e 14; arts. 26 e 27). O
   convite já nomeia as três contrapartidas que o IFSP anuncia.
3. **Não embutir o cadastro desses serviços no questionário.** O IFAL ofereceu
   cadastro de vagas no próprio formulário e passou a dirigir as vagas a quem
   respondeu. Isso mistura duas finalidades — o termo do questionário declara que as
   respostas não servem a nenhuma outra
   ([`consentimento.md`](../docs/especificacao/consentimento.md)) — e transforma o
   serviço em prêmio pela resposta.

**Evidência.**

- [Edwards et al. (2023)](../docs/pesquisa/fichamentos/edwards-2023.md) — *medido em
  outra população*: oferecer os resultados aumentou a resposta a questionário
  eletrônico (2 ensaios; OR 1,36; IC 95% 1,16–1,59). É a contrapartida com evidência
  mais direta, e a mais barata.
- [IFAL (2024)](../docs/pesquisa/fichamentos/ifal-2024.md) — *relatado*: os autores
  creem que o cadastro de vagas aumentou o engajamento, sem medir; e 84,6% dos
  respondentes não conheciam o serviço de vagas que já existia.
- [Alumni USP](../docs/pesquisa/fichamentos/usp-alumni.md) — *relatado*: mais de 150
  mil inscritos por contrapartida, sem denominador e com autosseleção pelo benefício.
- [Cabral et al. (2016)](../docs/pesquisa/fichamentos/cabral-2016.md) — *não
  avaliado*: nenhum dos portais analisados oferecia canal de oportunidades.

### 10.10 R7 — Colaboração voluntária: termo próprio, fora do questionário

**O que fazer.** A colaboração voluntária do egresso em ensino, pesquisa e extensão
exige termo de adesão com objeto e condições (art. 40, item 4), plano de trabalho com
identificação e contato (Anexo II), acompanhamento por servidor efetivo do campus
(art. 40, item 5) e observância da Lei nº 9.608/1998 (art. 40, item 1; PAEg,
art. 18). É relacionamento, e não medida: o
[bloco de contato](../docs/especificacao/blocos-instrumento.md) a deixou de fora por
isso. O questionário não inscreve voluntários nem empresta seu consentimento a essa
adesão; o convite nomeia a possibilidade, e o setor do campus a conduz.

**Evidência.** Nenhuma fonte do conjunto avalia a colaboração voluntária de egressos.
A ligação com a literatura é pela distinção entre camada de relacionamento e camada
de coleta: o [Alumni USP](../docs/pesquisa/fichamentos/usp-alumni.md) opera adesão
voluntária com cadastro próprio (*relatado*), e
[Cabral et al. (2016)](../docs/pesquisa/fichamentos/cabral-2016.md) tratam o portal de
relacionamento como canal à parte (*não avaliado*).

### 10.11 R8 — Portal de relacionamento, quando couber

**O que fazer.** O ambiente virtual de relacionamento com e entre os egressos é
competência da COPAEG (art. 8º, item 4; PAEg, art. 11, II), e o Portal do Egresso tem
finalidades de relacionamento — formação continuada, eventos, vagas, encontros
(art. 29). Ele é o lugar natural da publicação dos resultados (R6) e da porta de
pedido (R5). **Não é o mecanismo**, e não hospeda o questionário rastreável por
endereço comum. Um formulário de atualização de contato no Portal atende ao art. 13,
item 1, mas é nova origem de contato: entra pela importação e pela regra de
precedência, e não por edição na plataforma.

**Evidência.**

- [Cabral et al. (2016)](../docs/pesquisa/fichamentos/cabral-2016.md) — *não
  avaliado*: portal centralizado em 4 das 10 universidades analisadas — número que mede
  visibilidade em buscador — e portais dispersos por unidade nas demais. Para uma
  instituição multicampi, o argumento é de centralização, e o Regulamento já a prevê,
  com páginas locais dentro da principal (art. 29, §§ 1º e 2º).
- [Alumni USP](../docs/pesquisa/fichamentos/usp-alumni.md) — *relatado*: o arranjo em
  operação e em escala, com escritório próprio — contexto que não se transfere por
  configuração.

### 10.12 Cada recomendação e a sua fonte

| | Fontes | Estado mais forte | Observação |
|---|---|---|---|
| R1 | IFAL; Coelho e Silva; Edwards et al. | medido em outra população | a pré-notificação eletrônica é inconclusiva; a recomendação de acertar o contato na conclusão é da própria fonte (IFAL) |
| R2 | Ifes; IFAL; Edwards et al. | medido em outra população | o efeito medido é o da personalização, que o aviso preserva |
| R3 | Coelho e Silva; Ifes | relatado | a conta institucional é decisão de projeto, sem fonte |
| R4 | Ifes; IFAL; Coelho e Silva; Alvares et al. | relatado | nenhuma fonte mede taxa por turma |
| R5 | Ifes; IFAL; linha de base; Edwards et al. | medido em outra população | a tensão normativa é leitura deste projeto; a decisão é da instituição |
| R6 | Edwards et al.; IFAL; Alumni USP; Cabral et al. | medido em outra população | só a devolução dos resultados tem efeito medido |
| R7 | Alumni USP; Cabral et al. | relatado | ligação indireta, pela distinção entre camadas |
| R8 | Cabral et al.; Alumni USP | relatado | — |

Nenhuma alcança *medido*. É o estado do campo que o quadro de engajamento já
registrara, e a revisão de Edwards et al. só o desloca para fora da população de
egressos.

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

A distribuição está sendo encerrada por ociosidade. Ver a seção 3.3.

### O IMAP recusa conexão, com o contêiner saudável

Salto de relógio da máquina virtual, depois de suspensão do hospedeiro. O serviço
tem supervisão que o recria — verificado: matando o Dovecot, o contêiner volta em
cerca de 20 segundos. Se persistir, `wsl --shutdown` e subir de novo.

### O `.wslconfig` parece não ter efeito

Provavelmente está malformado, e o WSL o ignora **sem avisar**. A causa mais comum
é marcador de ordem de bytes no início do arquivo.

### O banco fica insalubre, e `root` não autentica

Procure nos registros do banco por **`certificate is not yet valid`**:

```bash
docker compose logs banco | grep -i "not yet valid"
```

Se aparecer, a inicialização foi interrompida no passo de segurança e o banco está
**pela metade** — nem `root` nem a verificação de saúde autenticam. A causa é o
relógio da máquina virtual saltar **para trás** durante a inicialização, o que faz
o certificado que o próprio banco acabou de gerar parecer ainda não válido.

Isso não se recupera reiniciando. É preciso recriar:

```bash
docker compose down -v && docker compose up -d
```

A composição já desliga o TLS do banco justamente para remover esse modo de falha.
Se o sintoma ocorrer mesmo assim, é sinal de que o relógio do hospedeiro está
instável; ver a seção 3.3.

### Uma segunda cópia do repositório interfere na primeira

A composição declara um nome de projeto fixo (`egressos`). Dois clones na mesma
máquina, portanto, **compartilham contêineres e volumes**: subir a partir do
segundo mexe no ambiente do primeiro, e um `down -v` em qualquer um deles apaga os
dados de ambos.

Se você precisa de dois ambientes lado a lado, defina nomes distintos com a
variável `COMPOSE_PROJECT_NAME` no `.env` de cada um, e portas diferentes em
`PORTA_HTTP`.

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
| [quadro-engajamento.md](../docs/pesquisa/quadro-engajamento.md) | estratégias de engajamento de egressos e o estado da evidência de cada uma |
| [parametros-contato.md](../docs/especificacao/parametros-contato.md) | cadência, tratamento da recusa, verificação de entrega |
| [capacidades-plataforma.md](../docs/especificacao/capacidades-plataforma.md) | o que a plataforma suporta, conferido contra a instância |
| [leitura-devolucoes.md](../docs/especificacao/leitura-devolucoes.md) | desenho do correio de ensaio e classificação do retorno |
| [infra/README.md](../infra/README.md) | referência operacional do ambiente |
| [scripts/README.md](../scripts/README.md) | as rotinas do projeto |
