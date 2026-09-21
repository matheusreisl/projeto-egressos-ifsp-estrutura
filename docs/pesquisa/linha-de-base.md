# Linha de base — o instrumento vigente de acompanhamento de egressos do IFSP

Caracterização das limitações do questionário institucional em operação, que é o
ponto de partida deste projeto. Cada limitação é associada, ao final, à dificuldade
correspondente na literatura fichada em [`fichamentos/`](fichamentos/).

Produto da etapa E03.

## 1. Objeto e método

**Objeto.** O instrumento de acompanhamento de egressos do IFSP, disponível em
`enquetes.ifsp.edu.br/889783`, vinculado à Política de Acompanhamento de Egressos
(PAEg) aprovada pela Resolução Normativa nº 13/2022 e divulgado na página
institucional de egressos.

**Método.** Análise documental. Nenhuma resposta foi preenchida e nada foi
submetido ao instrumento, conforme a delimitação do projeto. As fontes foram:

| Fonte | O que forneceu |
|---|---|
| Relatório 1 da PAE — 26/06/2015 a 31/12/2018 | estrutura de blocos, enunciados, domínios de resposta, contagens |
| Relatório 2 da PAE — 01/01/2019 a 31/12/2023 | os mesmos dados no período seguinte, e as metas do PDI 2019-2024 |
| Página institucional de egressos | modo de divulgação, normativos vigentes, endereço do instrumento |
| Resolução Normativa nº 13/2022 (PAEg) | governança, instrumentos da política, objetivos |
| Portaria Normativa nº 128/2025 (Regulamento do Programa) | o desenho normativo da coleta: convite, periodicidade, blocos, população-alvo |
| Tela inicial do instrumento | plataforma, modo de acesso, ausência de consentimento, tipos de campo |
| Instrumento de Avaliação Institucional Externa do INEP (2017) | o Indicador 3.7, que é a régua oficial |

**Por que não se percorreu o instrumento.** Avançar entre as páginas de um
questionário LimeSurvey exige submissão (`POST`), e a instância tem salvamento
parcial ativo — há "Retomar mais tarde" e "Carregar questionário não finalizado" na
tela inicial. Percorrer o instrumento criaria registros de resposta fictícios na
base real da instituição, contaminando a série histórica da pesquisa institucional.
A estrutura foi, portanto, reconstruída pelos dois relatórios oficiais, que
publicam os enunciados e os domínios de cada questão.

## 2. Caracterização do instrumento

**Plataforma.** LimeSurvey, declarado na metatag `generator` da página e nomeado
nos dois relatórios, que intitulam suas seções de resultados "Síntese de dados
descritivos - LimeSurvey".

Este é o primeiro achado relevante, e reposiciona o projeto: a instituição **já
opera a mesma plataforma** que este trabalho adota. O que se propõe não é migração
de ferramenta, mas configuração diferente da ferramenta já mantida.

**Estrutura.** Trinta questões distribuídas em sete blocos:

| Bloco | Tema | Questões |
|---|---|---|
| I | Avaliação da Formação | 1–6 |
| II | Atividade profissional anterior | 7–14 |
| III | Situação atual (**Direcional**) | 15 |
| IV | Evolução na formação | 16 |
| V | Perfil do egresso no Mercado de Trabalho | 19–28 |
| VI | Motivos da não inserção laboral | 17–18 |
| VII | Avaliação da PAE | 29–30 |

A estrutura é confirmada normativamente: o art. 17, §1º do Regulamento declara que
"o questionário está estruturado em **sete blocos de perguntas no LimeSurvey**,
dispostas de forma **lógica-condicional**", e o §2º nomeia os sete blocos, na mesma
ordem em que aparecem nos relatórios.

**População-alvo.** O art. 18 do Regulamento a define como todos os egressos dos
cursos técnicos (integrado, subsequente e concomitante), de graduação e de
pós-graduação lato e stricto sensu.

**Navegação condicional confirmada.** O Bloco III é rotulado "Direcional" nos
relatórios, e a numeração fora de sequência — o Bloco V reúne as questões 19 a 28 e
o Bloco VI as questões 17 e 18 — revela a bifurcação. Os dados confirmam:

| | Relatório 1 | Relatório 2 |
|---|---|---|
| Registros no período | 715 | 1.503 |
| Questão 15 (direcional), respondentes | 715 | 1.503 |
| Ramo "trabalhando" (Q20 / Q19) | 454 | 1.081 |
| Ramo "não trabalhando" (Q17) | 227 | 381 |
| **Soma dos dois ramos** | **681** | **1.462** |

A soma dos ramos se aproxima do total de registros, o que é a assinatura
quantitativa de uma bifurcação exaustiva: quem passa pela Q15 segue por um caminho
ou pelo outro.

**Volume.** O total acumulado no questionário, desde 26/06/2015, é de **2.519
registros**: 715 no período do PDI 2014-2018 (28,38%) e 1.503 no período seguinte
(59,67%). Os dois períodos somam 88,05% do total.

## 3. Modo de acesso

**Constatação.** Acesso aberto por link público único, sem token e sem
autenticação. A tela inicial não apresenta campo de código de acesso, e a URL não
carrega parâmetro de identificação.

**Isso contraria a própria norma.** O Regulamento do Programa, aprovado pela
Portaria Normativa nº 128/2025, determina no art. 16 que o questionário seja
"acessível por meio de um **link disponibilizado para cada egresso**". O que está
em operação é o oposto: um único link, igual para todos, publicado em página
aberta. A divergência entre o que a norma determina e o que a instância entrega é
o achado central desta linha de base, e reaparece nas seções 6 e 8.

**Consequências.**

1. Qualquer pessoa com o endereço pode responder, sem verificação de que é egresso
   do IFSP.
2. Não há controle de unicidade: a mesma pessoa pode responder mais de uma vez, e
   não há como detectar duplicidade.
3. O conjunto de respondentes é autosselecionado entre quem encontrou o link.

**O que importa aqui.** A limitação **não é da ferramenta**. O LimeSurvey oferece
nativamente tabela de participantes, acesso por token individual, controle de quem
respondeu e convites vinculados. Nenhum desses recursos está acionado. O
instrumento vigente usa uma plataforma capaz de rastreabilidade em um modo que a
dispensa.

Essa distinção é o eixo do projeto: não se trata de demonstrar que outra plataforma
resolveria, mas que a configuração adequada da plataforma já instalada resolve.

## 4. Identificação do respondente

**Constatação.** Não há identificação individual do convidado. Sem tabela de
participantes, o sistema não distingue quem foi convidado, quem abriu o instrumento
e quem respondeu.

**Consequência central: não existe denominador.** Os 2.519 registros são um
numerador sem base de comparação. Não é possível calcular taxa de resposta, porque
não se sabe quantos egressos foram alcançados — nem, a rigor, quantos egressos
existem no universo pretendido. Os relatórios apresentam percentuais de
distribuição interna (quanto cada período representa do total acumulado), não
cobertura da população.

Em consequência, as três perguntas que uma política de acompanhamento precisa
responder ficam sem resposta possível:

- Que proporção dos egressos foi alcançada?
- Quem não respondeu?
- A distribuição dos respondentes se parece com a dos egressos?

**Nota metodológica sobre os dados.** A introdução do Relatório 1 menciona, em
outubro de 2018, "aproximadamente 10.000 registros e mais de 850 respostas
completas", número que não se concilia com os 2.519 registros totais reportados
nas seções de dados. Provavelmente "registros" designa coisas distintas nos dois
lugares — acessos em um caso, respostas gravadas no outro. A ambiguidade em si é
sintoma: sem identificação do participante, os próprios termos de contagem ficam
instáveis.

**Observação sobre a leitura dos números.** Contagens menores em algumas questões
não indicam abandono. O Relatório 1 adverte que "algumas questões foram incluídas
posteriormente", o que explica, por exemplo, a questão 1 ter 205 respostas em 715
registros no primeiro período e 1.503 em 1.503 no segundo. Atribuir esses valores a
desistência seria erro de leitura.

## 5. Padronização dos campos

**Constatação.** A padronização é majoritária, mas não uniforme, e falha
justamente onde mais importa para agregação.

**O que está padronizado.** A maior parte das questões usa domínio fechado com
códigos estáveis (`A1`, `A2`, `A3`…), como se vê nos relatórios: a questão de sexo
oferece Feminino, Masculino e Outro; a de raça/cor oferece Preta, Parda, Indígena,
Amarela, Branca e "Não desejo declarar". Domínio fechado permite contagem direta,
e é o que torna os relatórios possíveis.

**Onde falha.**

| Campo | Problema |
|---|---|
| Nome do primeiro curso | **texto livre**, obrigatório |
| Campus e tipo de curso | domínio fechado, mas com opção "Outros" acompanhada de campo aberto |
| Questão 14 | dissertativa e opcional |

O campo de curso em texto livre é o caso mais consequente. Em uma instituição com
39 campi e oferta em oito modalidades, o nome do curso digitado livremente impede
agregação por curso sem tratamento posterior — que é exatamente o recorte de que a
revisão de projetos pedagógicos precisa. O dado existe, mas não é utilizável sem
trabalho manual.

**Agravante evitável.** O campo de ajuda da primeira questão exibe o texto padrão
de exemplo da plataforma, não substituído. É indício de configuração não revisada,
e não de limitação de desenho.

**O que a padronização não resolve sozinha.** Dados que a instituição já possui —
campus, curso, ano de conclusão, modalidade — são perguntados ao egresso em vez de
carregados previamente. Além de alongar o instrumento, isso transfere ao
respondente o ônus de informar o que o sistema acadêmico já sabe, e introduz erro
onde não havia.

## 6. Mecanismos de cobrança

Esta é a seção em que norma e prática mais se distanciam, e convém separá-las.

### 6.1 O que o Regulamento determina

A Portaria Normativa nº 128/2025 é explícita e detalhada. O Capítulo VI descreve um
mecanismo de cobrança completo:

| Dispositivo | Determinação |
|---|---|
| Art. 14 | pesquisas periódicas, **anuais** |
| Art. 16, caput | questionário acessível por **link disponibilizado para cada egresso** |
| Art. 16, §1º | **convite por e-mail**; não sendo possível, por **aplicativos de mensagens instantâneas** |
| Art. 16, §2º | aplicação **automatizada**, com disparos **repetidos** por sistema de mala direta |
| Art. 19 | acompanhamento por turma ao término do semestre de conclusão, e **anualmente** depois |
| Art. 22 | divulgação aos pré-egressos **no momento da colação de grau** e nova campanha **dois anos após a formatura, com envio de mensagens de lembrete** |

Ou seja: convite individual, canal alternativo para contato inválido, disparo
automatizado e repetido, lembretes e periodicidade definida. Praticamente o
conjunto de requisitos que este projeto se propõe a implementar já está
normatizado.

### 6.2 O que está em operação

Nada disso. O instrumento é um link único publicado em página aberta, e a busca
nos dois relatórios por "convite", "lembrete", "e-mail" e "periodicidade" não
retorna nenhuma ocorrência. O que os relatórios registram é divulgação por
difusão e, no Relatório 1, uma "Campanha de Egressos" prevista para outubro de
2018, articulada com a Comunicação Social — ação pontual, que atinge quem estiver
exposto ao canal e realcança quem já respondeu.

### 6.3 Por que a implementação não acompanha a norma

A cadeia é técnica, não administrativa. Cobrar exige saber de quem cobrar; saber
de quem cobrar exige identificação individual do convidado; identificação
individual exige tabela de participantes e acesso por token. Sem acionar esse
recurso — que a plataforma já oferece —, o art. 16 é inexequível: não há como
"disponibilizar um link para cada egresso" nem como disparar lembrete "aos que não
responderam", porque não existe a lista.

**Consequência para o projeto.** A lacuna não é de norma, é de suporte técnico.
O mecanismo proposto não acrescenta exigências à instituição: implementa o que o
Regulamento vigente já determina e que hoje não tem como ser cumprido. Isso
desloca o trabalho de "proposta de melhoria" para "viabilização de norma vigente",
que é uma posição bem mais forte no relatório final e no guia de replicação.

## 7. Registro de consentimento

**Constatação.** Não há registro de consentimento em nenhuma das camadas
examinadas.

| Camada | Situação |
|---|---|
| Instrumento | a tela inicial abre diretamente na primeira questão; não há termo, aceite nem informação sobre tratamento de dados |
| Relatórios 1 e 2 | nenhuma ocorrência de "consentimento", "LGPD", "dados pessoais", "sigilo", "anonimização" ou "anônimo" |
| Resolução Normativa nº 13/2022 | nenhuma menção a proteção de dados, embora preveja coleta por questionário eletrônico, banco de dados de egressos e divulgação "a toda comunidade interna e externa" |
| Portaria Normativa nº 128/2025 (Regulamento) | **há previsão normativa** — o art. 25 declara conformidade com a LGPD e com o Marco Civil da Internet |

**O que o Regulamento diz.** O art. 25 estabelece que "todos os processos de
coleta e processamento de dados estarão em conformidade com a Lei Geral de
Proteção de Dados (LGPD - Lei nº 13.709/2018) e com o Marco Civil da Internet
(Lei nº 12.965/2014), garantindo a privacidade e segurança das informações". Há
ainda uma remissão no Anexo I, na descrição do Indicador 1, que condiciona a
divulgação de listagens nominais a "respeitando a lei de proteção de dados".

**O que isso resolve e o que não resolve.** Resolve a questão da vontade
normativa: a instituição declara submissão à LGPD, e não se pode afirmar que a
matéria esteja ausente da norma. Não resolve nada da operação. O art. 25 é
cláusula de remissão genérica — declara conformidade sem estabelecer **como**:

- não indica a base legal do art. 7º sob a qual o tratamento se dá;
- não institui coleta de consentimento nem forma de registrá-lo;
- não fixa prazo de retenção nem procedimento de eliminação;
- não trata de anonimização, apesar de o art. 15, item 4, prever "divulgar dados
  sobre os egressos da instituição";
- não define o registro das operações de tratamento exigido pelo art. 37 da LGPD.

**Conclusão do eixo.** O padrão aqui é o mesmo dos demais: a norma determina o
destino certo e não há suporte técnico que o alcance. Declarar conformidade com a
LGPD não produz conformidade — produz uma obrigação a cumprir. O instrumento em
operação não coleta consentimento, não informa finalidade e não registra
tratamento, de modo que o art. 25 é hoje uma promessa sem implementação. É
precisamente essa distância que as etapas E22 e E23 fecham.

**O que a LGPD exigiria.** Aplicado a egressos reais, o mecanismo precisaria de
aceite registrado e recuperável, porque o ônus da prova é do controlador (art. 8º,
§2º); de finalidade determinada, sob pena de nulidade (art. 8º, §4º); do conteúdo
informativo do art. 9º; de via de revogação tão fácil quanto o aceite (art. 8º,
§5º); e de registro das operações de tratamento (art. 37).

## 8. Posicionamento na régua oficial

O Instrumento de Avaliação Institucional Externa do INEP (2017) traz o **Indicador
3.7 — Política institucional de acompanhamento dos egressos**, com cinco níveis:

| Conceito | Critério de análise |
|---|---|
| 1 | Não há política institucional de acompanhamento dos egressos |
| 2 | A política institucional não garante mecanismo de acompanhamento de egressos |
| 3 | A política garante mecanismo **e a atualização sistemática de informações** sobre continuidade na vida acadêmica ou inserção profissional |
| 4 | O anterior, mais **estudo comparativo** entre atuação do egresso e formação recebida, subsidiando ações de melhoria |
| 5 | O anterior, mais outras ações reconhecidamente exitosas ou inovadoras |

Registre-se uma correção de leitura corrente: a **Lei nº 10.861/2004 não menciona
egresso** em nenhum dispositivo. A exigência de acompanhamento está neste indicador
infralegal, e não na lei do SINAES. No instrumento de avaliação **de cursos**, por
sua vez, "egresso" aparece quase sempre na expressão "perfil profissional do
egresso", que designa o perfil previsto no projeto pedagógico — não o
acompanhamento de formados. São coisas distintas e costumam ser confundidas.

**Onde o IFSP se situa.** A instituição tem política formalizada e tem mecanismo em
operação, o que a coloca além dos conceitos 1 e 2. O ponto de travamento é a
expressão **"atualização sistemática de informações"** do conceito 3: um
instrumento de acesso aberto, sem convite, sem cobrança e sem periodicidade de
aplicação definida coleta o que chega, quando chega. A sistematicidade depende de
saber a quem perguntar e de perguntar de novo a quem não respondeu — que é
precisamente o que a rastreabilidade de participantes e a automação de lembretes
entregam.

O enquadramento definitivo cabe à comissão avaliadora, não a este documento. O que
se afirma aqui é mais restrito e verificável: o desenho atual não produz a
evidência que o conceito 3 descreve.

## 9. Limitações desta análise

- **O Regulamento foi recuperado por inteiro**, por descompressão dos fluxos do
  PDF, incluindo os anexos. As únicas perdas são as expressões matemáticas dos
  indicadores, publicadas como imagem — supridas pelas descrições textuais
  reproduzidas no Anexo A — e o Apêndice I, o Plano de Acompanhamento de Egressos,
  que não foi examinado por estar fora do recorte desta etapa.
- **A estrutura foi reconstruída por fonte secundária.** Os relatórios são
  documentos oficiais da própria DAEST e publicam enunciados e domínios, mas não
  substituem a inspeção da configuração do questionário. Aspectos como
  obrigatoriedade campo a campo, regras de validação e o texto exato das condições
  de desvio não são verificáveis por essa via.
- **Os relatórios cobrem até 31/12/2023.** Não há dados publicados sobre 2024 em
  diante, e o instrumento continua no ar.
- **O universo de egressos do IFSP não é conhecido.** Sem esse número, nem este
  documento nem a instituição podem converter os 2.519 registros em taxa de
  cobertura. A indisponibilidade é, ela própria, parte do diagnóstico.

## 10. Síntese — limitação, efeito e correspondência na literatura

| # | Limitação observada | Efeito | Correspondência na literatura |
|---|---|---|---|
| 1 | Acesso por link aberto, sem token — **contra o art. 16 do próprio Regulamento**, que exige link por egresso | admite resposta múltipla e de não egressos; respondente autosselecionado | [IFES (2025)](fichamentos/ifes-2025.md) — mesma limitação com Google Forms, e o relatório afirma representatividade sem poder calculá-la |
| 2 | Sem identificação do participante | não há denominador, logo não há taxa de resposta nem perfil de não resposta | [COELHO e SILVA (2017)](fichamentos/coelho-2017.md) — única fonte do conjunto com taxa real (35,4%), justamente por partir de lista fechada de 79 egressos extraída do sistema acadêmico |
| 3 | Nome do curso em texto livre | impede agregação por curso sem tratamento manual, em instituição com 39 campi | [PRAGA DE SOUZA et al. (2025)](fichamentos/praga-de-souza-2025.md) — gestores relatam que perguntas redundantes e dados já existentes em base devem ser evitados |
| 4 | Dados institucionais perguntados ao egresso | alonga o instrumento e introduz erro onde a instituição já tem o dado | [RANTHUM e SANTOS JUNIOR (2023)](fichamentos/ranthum-2023.md) — a ferramenta extrai dos sistemas acadêmicos o que já se sabe e pergunta só o resto |
| 5 | Sem convite, lembrete ou cobrança — **embora o art. 16, §§1º e 2º os determine** | insistência só por difusão ampla, que realcança quem já respondeu | [IFES (2025)](fichamentos/ifes-2025.md) — mobilização por difusão e janela de cinco meses e meio como substituto da cobrança dirigida |
| 6 | Sem tratamento de contato inválido — **embora o art. 16, §1º preveja fallback por mensagens instantâneas** | contato desatualizado é perda definitiva | [COELHO e SILVA (2017)](fichamentos/coelho-2017.md) — busca ativa por telefone e redes para atualizar o e-mail; [PRAGA DE SOUZA et al. (2025)](fichamentos/praga-de-souza-2025.md) — desatualização cadastral como obstáculo de primeira ordem |
| 7 | Sem registro de consentimento — **embora o art. 25 declare conformidade com a LGPD** | aceite não é persistido nem recuperável | [BRASIL — LGPD](fichamentos/brasil-lei-13709-2018.md), arts. 8º e 9º; [COELHO e SILVA (2017)](fichamentos/coelho-2017.md) — precedente de TCLE eletrônico com desvio condicional |
| 8 | Conformidade declarada em cláusula genérica, sem base legal, retenção ou anonimização definidas | o egresso não sabe sob que fundamento fornece o dado nem por quanto tempo será guardado | [IFTO (2023)](fichamentos/ifto-ppdp-2023.md) — como uma política de IF desce ao operacional: finalidade expressa (art. 10, §3º, III), registro das operações (art. 8º, §4º), não identificação por padrão (art. 8º, §16) |

**Padrão das oito limitações — e o que ele determina sobre o artefato.** Nenhuma
das oito decorre de omissão da norma. Em seis delas (1, 5, 6, 7, 8) há
dispositivo expresso no Regulamento determinando o contrário do que está em
operação; nas outras duas (3, 4) o recurso já existe na plataforma e não foi
acionado.

A conclusão é mais forte do que a de um diagnóstico de lacunas: **o IFSP já
normatizou, em 2025, quase tudo o que este projeto se propõe a construir.** O que
falta é suporte técnico para cumprir o que está posto. Isso desloca o trabalho de
"proposta de melhoria" para "viabilização de norma vigente", e dá ao guia de
replicação (E30) um destinatário concreto: a instituição não precisa decidir se
quer; precisa de como fazer.

A exceção a registrar é de grau, não de natureza: no eixo da conformidade, a norma
declara o destino (art. 25) sem especificar o percurso, enquanto no eixo da
cobrança o art. 16 especifica o percurso em detalhe. Por isso as etapas E22 e E23
têm de tomar decisões de projeto — base legal, conteúdo do termo, prazo de
retenção — que a E20 e a E21 não precisam tomar.

## 11. O que este diagnóstico determina para as etapas seguintes

- **E05** — a normativa institucional fixa parte dos parâmetros e deve ser
  respeitada: periodicidade anual (arts. 14 e 19), primeiro contato no semestre de
  conclusão, nova campanha dois anos após a formatura (art. 22), e-mail como canal
  primário com mensagens instantâneas como alternativa (art. 16, §1º). O que a
  norma **não** fixa e terá de vir da literatura: número de lembretes por ciclo,
  intervalo entre eles, limite de tentativas e tratamento da recusa.
- **E11** — o leiaute de entrada deve trazer o que a instituição já possui (campus,
  curso, ano de conclusão, modalidade), para pré-preenchimento, e mais de uma via
  de contato.
- **E12** — os sete blocos vigentes são a referência estrutural de partida,
  observado que o conteúdo temático das questões vem de projeto correlato. O
  critério de conclusão da etapa — nenhum bloco sem indicador correspondente —
  tem agora referência institucional pronta: os dezenove indicadores do Anexo I do
  Regulamento, reproduzidos no Anexo A deste documento.
- **E13** — o campo de curso é o caso-teste do fechamento de domínio.
- **E14** — a bifurcação da questão 15 entre "inserido" e "não inserido" é o caminho
  condicional a reproduzir, e está quantitativamente confirmada.
- **E22** — a tela de consentimento corrige uma ausência observada, não um requisito
  acrescentado por zelo.
- **E25** — o Indicador 3.7 do INEP oferece critério externo e oficial para redigir
  os requisitos de verificação.

## Anexo A — Os dezenove indicadores institucionais

O Anexo I do Regulamento define dezenove indicadores, com descrição e propósito.
São a referência oficial para o critério de conclusão da E12 — nenhum bloco sem
indicador correspondente — e para o painel da E29, caso executado.

| # | Indicador | Como é definido |
|---|---|---|
| Ind1 | Acompanhamento de gestão operacional | listagens nominal e quantitativa de atividades realizadas para egressos, por ano, tipo e campus, "respeitando a lei de proteção de dados" |
| Ind2 | Número de egressos | total e por ano, campus, nível e curso, no sistema e entre os respondentes |
| Ind3 | **IMT** — Inserção no Mundo do Trabalho | egressos com atividade remunerada ÷ total de respondentes |
| Ind4 | **IEMPAF** — Empregabilidade na Área de Formação | egressos em atividade diretamente relacionada à formação ÷ egressos com atividade remunerada |
| Ind5 | **IVET** — Verticalização, técnicos | egressos técnicos cursando nível superior **no IFSP** ÷ total de egressos técnicos |
| Ind6 | **IVEG** — Verticalização, graduação | egressos de graduação cursando pós **no IFSP** ÷ total de egressos de graduação |
| Ind7 | **IVQET** — Verticalização Qualificada, técnicos | egressos técnicos em superior no IFSP ÷ egressos técnicos em superior **em qualquer instituição** |
| Ind8 | **IVQEG** — Verticalização Qualificada, graduação | análogo ao Ind7, para pós-graduação |
| Ind9 | **ICFT** — Continuidade da Formação, técnicos | egressos técnicos em superior em qualquer instituição ÷ total de egressos técnicos |
| Ind10 | **ICFG** — Continuidade da Formação, graduação | análogo ao Ind9, para pós-graduação |
| Ind11 | **ICFACT** — Continuidade em Área Correlata, técnicos | continuaram **na mesma área** ÷ total que continuou |
| Ind12 | **ICFACG** — Continuidade em Área Correlata, graduação | análogo ao Ind11 |
| Ind13 | Nível de remuneração | média, maior, menor e valor mais frequente, por faixas de rendimento |
| Ind14 | Satisfação financeira | média em escala de 1 a 10 |
| Ind15 | Satisfação financeira, atuantes na área de formação | média em escala de 1 a 10 |
| Ind16 | Satisfação financeira, atuantes fora da área | média em escala de 1 a 10 |
| Ind17 | Satisfação com a atividade profissional | média em escala de 1 a 10 |
| Ind18 | Associação entre atividade exercida e curso | afinidade em escala de 1 a 10 |
| Ind19 | Satisfação com a formação recebida no IFSP | média em escala de 1 a 10 |

**Sobre as fórmulas.** O Regulamento apresenta a expressão matemática de cada
índice como imagem, que a extração de texto não recupera. A perda é imaterial: a
descrição textual que precede cada fórmula é inequívoca quanto ao numerador e ao
denominador, e a coluna acima a reproduz. Caso a E12 exija a notação exata, basta
consultar as páginas 20 a 27 do PDF.

**Três observações úteis para a E12.**

1. **A distinção entre verticalização e continuidade é a chave do conjunto.** Os
   pares Ind5/Ind9 e Ind6/Ind10 medem a mesma trajetória com denominadores
   diferentes: o primeiro pergunta se o egresso continuou **no IFSP**, o segundo
   se continuou **em qualquer instituição**. Coletar isso exige distinguir, no
   instrumento, a instituição em que o egresso prosseguiu — campo que precisa
   existir com domínio adequado.
2. **Sete dos dezenove indicadores usam escala de 1 a 10** (Ind14 a Ind19, mais o
   Ind18 de afinidade). Isso fixa um tipo de campo padronizado para vários blocos.
3. **Ind4 e Ind18 dependem de julgamento sobre "área de formação"** — se a
   atividade é ou não relacionada ao curso. Convém decidir na E13 se isso é
   autodeclaração do egresso ou classificação posterior, porque muda o campo.
