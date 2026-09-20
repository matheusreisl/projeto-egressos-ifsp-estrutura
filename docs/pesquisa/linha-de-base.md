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

**Constatação.** Não existem. Não há convite individual, não há lembrete, não há
disparo automatizado, não há acompanhamento de não respondentes. A busca nos dois
relatórios por "convite", "lembrete", "e-mail" e "periodicidade" não retorna
nenhuma ocorrência.

**O que existe no lugar.** Divulgação por difusão: o link publicado na página
institucional de egressos e, segundo o Relatório 1, uma "Campanha de Egressos"
prevista para o final de outubro de 2018, articulada com a Comunicação Social.
Campanha é ação pontual de divulgação, não cobrança sistemática — atinge quem
estiver exposto ao canal no momento, e atinge de novo quem já respondeu.

**Por que a cobrança é impossível neste desenho.** Cobrar exige saber de quem
cobrar. Sem identificação do participante (seção 4), não há lista de não
respondentes, e portanto não há a quem dirigir lembrete. A ausência de cobrança não
é omissão administrativa: é consequência necessária do modo de acesso adotado.

**O que a instituição planeja.** O Relatório 2 registra, entre as metas do PDI
2019-2024, "atualizar pesquisa de tipo Survey a cada dois anos", implantar o
acompanhamento no SUAP, criar aplicativo e criar perfil em plataformas
profissionais. Periodicidade de atualização do instrumento, contudo, é coisa
distinta de periodicidade de cobrança do respondente.

## 7. Registro de consentimento

**Constatação.** Não há registro de consentimento em nenhuma das camadas
examinadas.

| Camada | Situação |
|---|---|
| Instrumento | a tela inicial abre diretamente na primeira questão; não há termo, aceite nem informação sobre tratamento de dados |
| Relatórios 1 e 2 | nenhuma ocorrência de "consentimento", "LGPD", "dados pessoais", "sigilo", "anonimização" ou "anônimo" |
| Resolução Normativa nº 13/2022 | nenhuma menção a proteção de dados, embora preveja coleta por questionário eletrônico, banco de dados de egressos e divulgação "a toda comunidade interna e externa" |

**Ressalva necessária.** A RN 13/2022 delega ao Regulamento do Programa dispor
sobre "coleta, tratamento e divulgação de dados sobre os egressos" (art. 14,
parágrafo único, II). Esse Regulamento foi aprovado pela Portaria Normativa nº
128/2025 e **não pôde ser lido**: o PDF publicado é digitalizado, sem camada de
texto, e não há OCR disponível no ambiente deste projeto. Não se pode, portanto,
afirmar que a matéria esteja ausente de toda a normativa — apenas que não aparece
nas camadas verificadas. Ver a seção 9.

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

- **O Regulamento do Programa não foi lido.** A Portaria Normativa nº 128/2025 está
  publicada como PDF digitalizado sem camada de texto. É a camada normativa que a
  RN 13/2022 indica como responsável pelas regras de coleta e tratamento de dados,
  e é onde a questão do consentimento poderia estar resolvida. **Pendência: obter
  versão com texto pesquisável ou submeter o arquivo a OCR.**
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
| 1 | Acesso por link aberto, sem token | admite resposta múltipla e de não egressos; respondente autosselecionado | [IFES (2025)](fichamentos/ifes-2025.md) — mesma limitação com Google Forms, e o relatório afirma representatividade sem poder calculá-la |
| 2 | Sem identificação do participante | não há denominador, logo não há taxa de resposta nem perfil de não resposta | [COELHO e SILVA (2017)](fichamentos/coelho-2017.md) — única fonte do conjunto com taxa real (35,4%), justamente por partir de lista fechada de 79 egressos extraída do sistema acadêmico |
| 3 | Nome do curso em texto livre | impede agregação por curso sem tratamento manual, em instituição com 39 campi | [PRAGA DE SOUZA et al. (2025)](fichamentos/praga-de-souza-2025.md) — gestores relatam que perguntas redundantes e dados já existentes em base devem ser evitados |
| 4 | Dados institucionais perguntados ao egresso | alonga o instrumento e introduz erro onde a instituição já tem o dado | [RANTHUM e SANTOS JUNIOR (2023)](fichamentos/ranthum-2023.md) — a ferramenta extrai dos sistemas acadêmicos o que já se sabe e pergunta só o resto |
| 5 | Sem convite, lembrete ou cobrança | insistência só por difusão ampla, que realcança quem já respondeu | [IFES (2025)](fichamentos/ifes-2025.md) — mobilização por difusão e janela de cinco meses e meio como substituto da cobrança dirigida |
| 6 | Sem tratamento de contato inválido | contato desatualizado é perda definitiva | [COELHO e SILVA (2017)](fichamentos/coelho-2017.md) — busca ativa por telefone e redes para atualizar o e-mail; [PRAGA DE SOUZA et al. (2025)](fichamentos/praga-de-souza-2025.md) — desatualização cadastral como obstáculo de primeira ordem |
| 7 | Sem registro de consentimento | aceite não é persistido nem recuperável | [BRASIL — LGPD](fichamentos/brasil-lei-13709-2018.md), arts. 8º e 9º; [COELHO e SILVA (2017)](fichamentos/coelho-2017.md) — precedente de TCLE eletrônico com desvio condicional |
| 8 | Sem finalidade declarada nem base legal | o egresso não sabe para que fornece o dado | [IFTO (2023)](fichamentos/ifto-ppdp-2023.md) — declara o acompanhamento de egressos como finalidade expressa de tratamento, no art. 10, §3º, III |

## 11. O que este diagnóstico determina para as etapas seguintes

- **E05** — os parâmetros de contato precisam vir da literatura, porque a normativa
  institucional não fixa nenhum: nem número de lembretes, nem intervalo, nem
  tratamento de recusa.
- **E11** — o leiaute de entrada deve trazer o que a instituição já possui (campus,
  curso, ano de conclusão, modalidade), para pré-preenchimento, e mais de uma via
  de contato.
- **E12** — os sete blocos vigentes são a referência estrutural de partida,
  observado que o conteúdo temático das questões vem de projeto correlato.
- **E13** — o campo de curso é o caso-teste do fechamento de domínio.
- **E14** — a bifurcação da questão 15 entre "inserido" e "não inserido" é o caminho
  condicional a reproduzir, e está quantitativamente confirmada.
- **E22** — a tela de consentimento corrige uma ausência observada, não um requisito
  acrescentado por zelo.
- **E25** — o Indicador 3.7 do INEP oferece critério externo e oficial para redigir
  os requisitos de verificação.
