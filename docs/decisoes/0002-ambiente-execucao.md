# ADR-0002 — Ambiente de execução da instância LimeSurvey

**Status:** aceita
**Data:** 21/09/2026
**Etapa de origem:** E06 — decidir o ambiente de execução

## Contexto

A Fase 2 exige instância própria do LimeSurvey. O documento do projeto, fonte de
verdade, não fecha o ambiente: prevê "conteinerização em máquina local ou serviços
de hospedagem em camada gratuita, conforme se mostrar mais adequado à continuidade
do trabalho". A escolha foi deliberadamente deixada para esta etapa, e é ela que
esta ADR registra.

Três conjuntos de exigências recaem sobre a decisão.

**Os critérios da E06:** custo zero, facilidade de reprodução por terceiros,
suporte a tarefa agendada, viabilidade de envio de e-mail e portabilidade.

**O que a E05 acrescentou.** A especificação de parâmetros de contato fixou, antes
de existir instância, dez capacidades que a plataforma precisa suportar (C1 a C10,
seção 13) e um requisito que o ambiente precisa comportar: a verificação de
entrega exige **caixa de retorno legível pela rotina** — envio e devolução, as
duas direções (seção 10.4). Uma configuração que envia corretamente e não permite
ler devoluções inviabiliza o parâmetro P8.

**As restrições invioláveis do projeto**, das quais duas incidem diretamente aqui:
nunca disparar mensagens para endereços reais, e nunca versionar credenciais em
repositório público.

**Estado da máquina de trabalho, verificado em 21/09/2026:** WSL versão 2.7.10.0,
kernel 6.18.33.2, virtualização de hardware ativa, **sem distribuição instalada**,
Docker ausente, 31,7 GB de memória e 145 GB livres em disco. A via conteinerizada
é comportada pela máquina; nada dela está provisionado — isso é a E07.

## Critérios de decisão

Os cinco primeiros são os sugeridos pela E06. Os dois últimos foram acrescentados
por esta etapa, e a justificativa de cada acréscimo vem logo abaixo da tabela.

| # | Critério | Origem | O que reprova |
|---|---|---|---|
| K1 | Custo zero, sem limiar de porte e sem meio de pagamento | E06; restrição do projeto | exigir cartão de crédito no cadastro, ou assinatura acima de um porte institucional |
| K2 | Reprodução por terceiros a partir do que está versionado | E06; critério de conclusão da E07 | ambiente cuja reprodução é sequência de cliques, e não arquivo |
| K3 | Tarefa agendada versionável | E06; E21 | agendamento que só existe no painel do provedor |
| K4 | Envio **e** leitura de devolução | E05, seção 10.4; E09 | bloqueio de SMTP de saída, ou ausência de caixa de retorno |
| K5 | Portabilidade | E06 | ambiente preso a um provedor ou a um sistema operacional |
| K6 | **Contenção do disparo** — impossibilidade física de alcançar endereço real | restrição inviolável do projeto | qualquer ambiente com rota aberta para a internet durante os ensaios |
| K7 | Operação integral por linha de comando | o guia da E30 é feito de comandos reproduzíveis, não de capturas de tela | configuração essencial que só existe em interface gráfica |

**Por que K6 entrou.** A restrição "nunca disparar para endereços reais" vinha
sendo tratada como regra de conduta — algo que se cumpre por atenção. É possível
convertê-la em propriedade do ambiente, e a escolha do ambiente é o único momento
em que essa conversão pode ser feita. Um projeto cujo objeto é conformidade não
deveria depender de disciplina para não violar a própria restrição, sobretudo
quando a Fase 6 exercita repetidamente rotinas de disparo sobre base de centenas
de registros.

**Por que K7 entrou.** É pré-condição de K2, não preferência de operação. O
entregável da E30 é um guia que um terceiro executa; passo expresso como comando é
verificável e copiável, passo expresso como captura de tela envelhece com a
próxima versão da interface e não é testável.

## Alternativas avaliadas

| Alternativa | K1 | K2 | K3 | K4 | K5 | K6 | K7 | Observação determinante |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **Conteinerização declarativa em máquina local** (Docker Engine + Compose, sobre WSL2 neste equipamento) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | rede fechada e serviço de correio no próprio compose |
| Docker Desktop no Windows | ~ | ✔ | ✔ | ✔ | ✔ | ✔ | ~ | mesmo resultado técnico, com ressalva de licença desnecessária |
| VM local (VirtualBox) | ✔ | ✖ | ✔ | ✔ | ~ | ✔ | ~ | reprodução manual; o artefato vira imagem, não arquivo |
| Nuvem em camada gratuita (IaaS) | ✖ | ~ | ✔ | ✖ | ✖ | ✖ | ✔ | disponibilidade contínua ao custo de todas as outras colunas |
| Hospedagem gerida do próprio LimeSurvey | ✖ | ✖ | ✖ | ~ | ✖ | ✖ | ✖ | não é instância própria no sentido que o projeto exige |

Legenda: ✔ atende · ~ atende com ressalva · ✖ não atende.

## Decisão

O ambiente de execução é **conteinerização declarativa em máquina local**: Docker
Engine e Docker Compose, com toda a composição — LimeSurvey, banco de dados,
serviço de correio e rotina agendada — **declarada em arquivos versionados em
`infra/`**, em rede fechada, sem rota de saída para a internet durante os ensaios.

Neste equipamento, o hospedeiro do Docker Engine é uma distribuição Linux sobre
WSL2. **O WSL2 é substrato local, não parte da decisão**: é a forma de obter um
hospedeiro Docker nesta máquina Windows, e é a peça trocável do arranjo.

Fica decidido também que **não se adota o Docker Desktop**, e sim o Docker Engine
instalado na distribuição.

## Justificativa

**1. K6 decide sozinho, e é o argumento mais forte.** Em rede de contêineres
fechada, com serviço de correio do próprio projeto, a mensagem não tem para onde
sair. A restrição "nunca disparar para endereços reais" deixa de ser conduta e
passa a ser propriedade do ambiente: um endereço equivocado no arquivo de entrada
produz uma devolução interna, e não uma mensagem real para um desconhecido. Em
qualquer ambiente com rota de saída, o mesmo equívoco é irreversível — mensagem
enviada não volta. Nenhuma outra linha da tabela de critérios justifica sozinha
uma escolha; esta justifica.

A contenção ainda se reforça pelo nome de domínio: os ensaios usam domínio sob o
TLD reservado `.test` (RFC 2606, formalizado pela RFC 6761), que por definição não
resolve na internet pública e não pode colidir com domínio de terceiro. É o que dá
conteúdo concreto à expressão "domínio controlado pelo projeto", usada desde a E05
sem que houvesse ambiente para materializá-la.

**2. K4 é onde a nuvem gratuita falha de modo não contornável.** Provedores de
infraestrutura em camada gratuita bloqueiam, por padrão, o tráfego SMTP de saída —
medida antiabuso, não configuração. E ler devoluções exige caixa de retorno real,
que a camada gratuita tipicamente não oferece. O serviço de correio no próprio
compose resolve as duas direções: aceita o envio e devolve erro permanente para
caixa inexistente do domínio controlado, que é exatamente o retorno que a E09
precisa ler e que a P8 precisa classificar.

**Ponto de verificação que a E09 herda.** Capturadores de SMTP de uso corrente em
desenvolvimento aceitam toda mensagem e **não devolvem erro algum**. Servem para
inspecionar o que foi enviado e não servem para P8. A E09 precisa de um serviço
que devolva, e precisa verificar isso explicitamente — não basta ver a mensagem
chegar ao capturador e dar o critério por atendido. É a mesma ressalva que a E05
levantou, agora com o ambiente definido.

**3. K1 sem ressalva, e é por isso que o Docker Desktop cai.** O Docker Engine é
distribuído sob licença Apache 2.0, sem limiar de porte nem de receita. O Docker
Desktop é gratuito para uso pessoal, educacional e para organizações abaixo de 250
funcionários **e** US$ 10 milhões de receita anual, e exige assinatura paga acima
de qualquer um dos dois limiares. Um Instituto Federal não cabe no limiar de
porte; e a instituição que vier a replicar este trabalho não pode ser presumida
cabendo. O resultado técnico das duas opções é o mesmo — a diferença é que uma
delas obrigaria o guia da E30 a carregar uma ressalva de licenciamento que a outra
simplesmente não tem. Entre duas opções tecnicamente equivalentes, escolhe-se a
que não precisa de nota de rodapé.

**4. O que é a decisão e o que é o substrato — K2 e K5.** A decisão é
*conteinerização declarativa*. O mesmo arquivo de composição sobe em Linux nativo,
em macOS e em servidor institucional; o WSL2 aparece apenas porque esta máquina é
Windows. Essa separação é o que preserva a portabilidade e o que organiza o guia
da E30: há uma parte que o guia **ensina** — a composição, idêntica em qualquer
lugar — e uma parte que ele apenas **oferece como opção**, que é obter um
hospedeiro Docker em cada sistema operacional.

Isso responde à objeção previsível de que uma instituição replicante implantaria
em servidor, e não em equipamento pessoal, e que validar em máquina local estaria
ensinando a coisa errada. Não está: o artefato entregue é a composição, e ela
chega ao servidor institucional sem alteração. O que muda é o hospedeiro, que é
justamente a parte que o guia trata como escolha do replicante.

**5. Por que a VM local não serve, apesar de atender K1 e K6.** Ela falha em K2, e
a falha é de natureza, não de grau: o artefato de uma VM é uma imagem de disco ou
uma sequência de instalação manual. Nenhum dos dois é versionável em repositório
público — imagem por tamanho, sequência manual por não ser executável. Um
instantâneo de VM não é documentação de instalação, e o critério de conclusão da
E07 exige que o ambiente suba do zero **a partir do que está versionado**.

**6. Por que a nuvem gratuita não serve, além de K4 e K6.** Três razões
adicionais, cada uma suficiente para desconforto:

- **Continuidade.** A conta seria pessoal do estudante. O projeto termina em
  dezembro de 2026 e o artefato deve sobreviver a ele; amarrá-lo a uma conta
  pessoal contraria a mesma lógica que levou o projeto a preferir software livre
  por sucessão técnica.
- **Estabilidade da oferta.** Camadas gratuitas são revogáveis por decisão
  unilateral do fornecedor, com precedente conhecido na área. Um guia de
  replicação ancorado em camada gratuita tem prazo de validade que não depende de
  quem o escreveu.
- **Local de tratamento.** Hospedar fora do Brasil introduz transferência
  internacional de dados (LGPD, arts. 33 a 36). Aqui a base é sintética e o ponto é
  inócuo para *este* projeto — mas o guia da E30 recomenda a instituições que
  tratarão dados reais de egressos, e seria incoerente que um trabalho cujo objeto
  é conformidade recomendasse, sem necessidade, um arranjo que obriga o replicante
  a uma análise adicional de base legal.

**7. Por que a hospedagem gerida do próprio LimeSurvey não serve.** Não é instância
própria no sentido que o projeto exige. Sem acesso ao servidor não há rotina
agendada própria, não há configuração de correio sob controle do projeto e não há o
que documentar como procedimento de instalação — que é, ele mesmo, um dos
entregáveis (E10). O objeto do trabalho desapareceria dentro do serviço.

## Consequências

### Passa a ser verdade

- **`infra/` é o entregável do ambiente.** Passa a conter o arquivo de composição,
  um `.env.exemplo` sem valores reais e o procedimento. O critério de conclusão da
  E07 — subir do zero a partir do que está versionado — torna-se verificável.
- **Nenhuma conta externa, nenhum meio de pagamento, nenhuma credencial de
  terceiro.** A restrição de não versionar credenciais fica trivialmente atendida:
  as únicas senhas existentes são locais, descartáveis e recriáveis, e vivem em
  `.env`, já ignorado pelo Git.
- **A contenção do disparo é propriedade do ambiente**, e não regra de conduta.
  Passa a ser verificável na matriz da E25 como característica do ambiente.
- **O ambiente é efêmero e recriável.** O que precisa sobreviver é o que está
  versionado: a composição, os scripts e a estrutura do questionário exportada na
  E15. Isso vira requisito de método — nenhuma configuração relevante pode existir
  apenas dentro do contêiner.

### Esta decisão custa

- **Disponibilidade contínua.** A rotina agendada só executa com a máquina ligada.
  É o preço real da escolha e não se disfarça. O que o torna aceitável é que a
  validação da Fase 6 é **simulação controlada com compressão temporal declarada**
  (E26): não se espera 60 dias de relógio para observar um ciclo. Disponibilidade
  contínua é propriedade de implantação real, não de prova de conceito.
- **Uma limitação a declarar na E31.** Não se poderá afirmar, a partir desta
  validação, que a rotina se sustenta ao longo de um ciclo anual em relógio real.
  Atesta-se o comportamento sob compressão temporal, e isso precisa ser enunciado
  assim, na mesma linha das demais limitações já declaradas.
- **Dependência de imagem comunitária.** Não há imagem de contêiner publicada pelo
  projeto LimeSurvey; as de uso corrente são mantidas por terceiros. É risco de
  sustentação e precisa de decisão explícita na E07: adotar a imagem comunitária de
  referência ou construir imagem própria a partir do código oficial. Em qualquer
  dos casos, **fixar a versão por digest** e registrá-la — sem isso, "subir do zero
  a partir do que está versionado" não produz o mesmo ambiente duas vezes.

### O que esta decisão determina para as etapas seguintes

- **E07 (provisionamento)** — instalar a distribuição Linux no WSL2 com `systemd`
  habilitado, instalar o Docker Engine na distribuição, escrever a composição e
  fixar as imagens por digest. Recolhe ainda o que já lhe estava atribuído: o
  `.gitattributes` e a ferramenta de extração de texto e OCR para a releitura de
  Ferreira (2026) e Davis (1989).
- **E08 (instalação)** — registrar a versão exata do LimeSurvey e conferir, contra
  a instância viva, as capacidades C1 a C10 da seção 13 de
  [`parametros-contato.md`](../especificacao/parametros-contato.md). É a primeira
  etapa em que essa conferência deixa de ser especulação.
- **E09 (mensagens)** — serviço de correio no próprio compose, com domínio sob
  `.test`; verificar as **duas direções**, com a ressalva do item 2 da
  justificativa: capturador que nunca devolve erro não atende P8.
- **E10 e E30 (guia)** — separar o que o guia ensina (a composição, igual em toda
  parte) do que ele oferece como opção (como obter um hospedeiro Docker em cada
  sistema operacional), e registrar o que muda numa implantação real: hospedeiro
  que permanece ligado, correio institucional e rede não isolada.
- **E25 (matriz de verificação)** — a contenção do disparo passa a ser
  característica verificável do ambiente.

## Revisão

Decisão revisável em duas hipóteses, nenhuma das quais exige refazer o que esta
etapa fixa:

1. **A instituição replicante dispõe de servidor institucional.** Muda o
   hospedeiro; a composição permanece. É o caso previsto, não uma exceção.
2. **A validação passa a exigir relógio real por ciclo completo.** Exigiria
   hospedeiro permanentemente ligado, e aí a comparação com a nuvem seria refeita —
   com a ressalva de que K6 continuaria valendo e obrigaria a isolar a rede por
   outro meio.
