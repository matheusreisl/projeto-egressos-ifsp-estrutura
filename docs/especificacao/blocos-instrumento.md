# Blocos estruturais do instrumento

**Etapa:** E12 — especificar os blocos estruturais do instrumento
**Data:** 28/09/2026
**Ponto de partida:** art. 17 do Regulamento do Programa de Acompanhamento de Egressos (Portaria Normativa nº 128/2025) e blocos da Especificação Técnica Preliminar do [documento do projeto](../projeto/Projeto_de_Pesquisa_Egressos_IFSP.docx)
**Decorre de:** [linha de base](../pesquisa/linha-de-base.md) (E03), [`parametros-contato.md`](parametros-contato.md) (E05) e [`leiaute-entrada.md`](leiaute-entrada.md) (E11)

Especificação dos contêineres que acolherão as questões do instrumento: que blocos
existem, para que cada um existe, que indicador alimenta e a quem se destina.
**Estrutura apenas** — nenhum enunciado de questão entra aqui. O conteúdo temático
vem de projeto correlato e ingressa como requisito de entrada.

É insumo direto da E13 (domínios, obrigatoriedade e validações, que completam este
arquivo na seção 12), da E14 (navegação condicional), da E15 (implementação), da
E18 (pré-preenchimento), da E22 (consentimento), da E28 (extração) e da E29
(painel).

> **Nota de notação.** Os blocos do art. 17 aparecem em algarismos romanos, como
> no Regulamento (Bloco I a Bloco VII). Os indicadores do Anexo I aparecem como
> Ind1 a Ind19, como no [Anexo A da linha de base](../pesquisa/linha-de-base.md).

## 1. Objeto e método

**Objeto.** Os blocos do instrumento de coleta — no LimeSurvey, grupos de questões.

**Método.** Derivação documental. Cada bloco recebe finalidade estrutural,
indicador alimentado — com origem declarada — e **público**: o conjunto de
respondentes a quem o bloco se destina. O público não é regra de navegação, que é
da E14; é o dado de que ela precisa, e sai daqui porque decorre do indicador: quem
não está no denominador de nenhum indicador do bloco não precisa vê-lo.

**O que esta etapa não faz.** Não redige questões. Não fecha domínios nem
obrigatoriedade campo a campo, que são da E13. Não escreve as regras de navegação
(E14) nem implementa nada na plataforma (E15).

### 1.1 O ponto de partida: três referências que não coincidem

| Referência | O que estabelece | O que o teste mostrou |
|---|---|---|
| Documento do projeto | sete blocos — consentimento, identificação acadêmica, situação ocupacional, caracterização da atuação, aderência à formação, formação continuada, contato e manifestações —, cada um com "indicador alimentado" | é anterior ao Regulamento e deixa sem bloco seis indicadores do Anexo I: Ind13 a Ind17 e Ind19 |
| Regulamento, art. 17, §2º | sete blocos para o questionário do IFSP: I Avaliação da Formação · II Atividade Profissional Anterior · III Situação Atual · IV Evolução na Formação · V Perfil do Egresso no Mercado de Trabalho · VI Motivos da Não Inserção no Mercado de Trabalho · VII Avaliação da PAEG | não prevê consentimento nem contato; e três blocos (II, VI e VII) não alimentam nenhum indicador do Anexo I |
| Regulamento, Anexo I | dezenove indicadores, cada um com descrição, propósito e fórmula | define o que medir, não onde; e três fórmulas medem coisa diferente da própria descrição (seção 6) |

**Decisões tomadas** (confirmadas com o orientando antes da execução e registradas
na [ADR-0006](../decisoes/0006-estrutura-a-partir-do-art-17.md)):

1. **A estrutura parte do art. 17.** Os sete blocos do Regulamento entram com os
   nomes e na ordem da norma, acrescidos de três blocos de controle do mecanismo;
   os blocos do documento do projeto viram correspondência (seção 5). O art. 17
   estrutura o questionário institucional "em sete blocos de perguntas no
   LimeSurvey, dispostas de forma lógica-condicional", e é nesses blocos que o
   conteúdo do projeto correlato tende a chegar. Hospedá-los como estão é o que o
   documento do projeto pede: que instrumentos revisados possam ser incorporados
   "sem alteração estrutural da solução".
2. **"Indicador correspondente" é um indicador do Anexo I ou um objetivo expresso
   do Regulamento.** No segundo caso, o objetivo é operacionalizado por um
   indicador mínimo proposto por este projeto, com a origem declarada. O critério
   estrito — só o Anexo I — excluiria três blocos que a mesma norma prescreve e
   que servem a objetivos que ela mesma enuncia no art. 3º. A leitura adotada
   preserva a função do critério — nenhum bloco sem medida declarada — e rotula a
   origem, como a E05 fez com os parâmetros de contato.

### 1.2 Escala de origem do indicador

| Rótulo | Significado |
|---|---|
| **Anexo I** | indicador definido no Anexo I do Regulamento, com descrição, propósito e fórmula |
| **objetivo + projeto** | objetivo expresso do Regulamento sem indicador no Anexo I; o indicador mínimo que o torna mensurável é proposta deste projeto, e a instituição pode redefini-lo |
| **controle** | requisito do próprio mecanismo — conformidade com a LGPD ou manutenção da base —, verificável na matriz da E25 |

## 2. Quadro dos blocos

| Ordem | Bloco | Finalidade estrutural | Indicador alimentado | Origem | Público |
|---|---|---|---|---|---|
| 1 | Consentimento | registrar aceite, data, hora e versão do termo antes de qualquer coleta; oferecer as duas recusas da P6 e o consentimento específico do dado sensível | registro do consentimento; tratamento da recusa | controle | todos |
| 2 | Identificação acadêmica | exibir os cinco atributos pré-preenchidos, editáveis, registrando a correção e preservando o valor original | Ind2, entre os respondentes; recorte de todos os demais; qualidade da base | Anexo I + controle | todos |
| 3 | I — Avaliação da Formação | avaliação, pelo egresso, da formação recebida | Ind19 | Anexo I | todos |
| 4 | II — Atividade Profissional Anterior | situação profissional anterior ao ingresso no curso | proporção dos egressos com atividade remunerada que já a exerciam antes do curso | objetivo + projeto (art. 3º, item 3) | todos |
| 5 | III — Situação Atual | classificar o respondente quanto à atividade remunerada atual; é a bifurcação entre V e VI | Ind3 | Anexo I | todos |
| 6 | IV — Evolução na Formação | continuidade dos estudos no nível seguinte; demandas de formação | Ind5 a Ind12; distribuição das demandas de formação | Anexo I; objetivo + projeto (art. 3º, item 12) | todos; a parte de continuidade, só técnico e graduação |
| 7 | V — Perfil do Egresso no Mercado de Trabalho | caracterizar a atividade remunerada atual | Ind4 e Ind13 a Ind18 | Anexo I | com atividade remunerada |
| 8 | VI — Motivos da Não Inserção no Mercado de Trabalho | fatores que o egresso aponta para não exercer atividade remunerada | distribuição dos elementos limitadores | objetivo + projeto (art. 3º, item 5) | sem atividade remunerada |
| 9 | VII — Avaliação da PAEG | avaliação, pelo egresso, das ações do programa | avaliação das ações do programa pelos respondentes | objetivo + projeto (art. 34, item 1) | todos |
| 10 | Recortes de equidade | autodeclaração de gênero, raça/cor e deficiência, com opção de não declarar; percepção das ações afirmativas | recortes de inserção e de continuidade; percepção das ações afirmativas | objetivo + projeto (art. 3º, itens 16 e 17) | todos; resposta opcional |
| 11 | Contato e manifestações | atualizar as vias de contato do leiaute; manifestar recusa de contato para os ciclos seguintes | manutenção da base (P8); respeito à recusa (P6) | controle | todos; resposta opcional |

**Onze blocos:** sete do art. 17, três de controle e um de equidade.

**A ordem é de referência; a navegação é da E14.** O consentimento vem primeiro,
porque nada se coleta antes dele. A identificação vem em segundo, porque dá
contexto ao resto, permite corrigir o pré-preenchido antes de responder e porque
o nível decide o que o Bloco IV exibe. Os blocos do art. 17 seguem a ordem do
Regulamento. Os recortes de equidade ficam no fim, antes do contato, por serem
opcionais e sensíveis: se houver desistência diante deles, ela não custa os
blocos que sustentam os indicadores centrais. O contato fecha o instrumento, que é
onde o egresso sai.

## 3. Os blocos de controle

### 3.1 Consentimento

**Finalidade.** Registrar aceite, data, hora e versão do termo **antes** de
qualquer coleta. O instrumento vigente abre direto na primeira questão, sem termo
algum ([linha de base](../pesquisa/linha-de-base.md), seção 7): o bloco corrige uma
ausência observada, não acrescenta um requisito por zelo.

**Três manifestações, e não uma.**

- **As duas recusas da P6** ([`parametros-contato.md`](parametros-contato.md),
  seção 8): *não concordo com o termo neste ciclo*, que encerra o ciclo corrente,
  e *não quero mais ser contatado*, que é permanente até revogação. Uma opção única
  de recusa erra em qualquer das direções.
- **O consentimento específico do dado sensível.** O Bloco 10 coleta raça/cor e
  deficiência, e a LGPD só admite tratar dado sensível, por consentimento, quando
  o titular consentir "de forma específica e destacada, para finalidades
  específicas" (art. 11, I). É uma manifestação à parte do aceite geral. Negá-la
  não encerra o questionário — apenas dispensa o Bloco 10.

**Indicador.** Controle: os requisitos "registro do consentimento" e "tratamento
da recusa" da matriz de verificação do documento do projeto.

### 3.2 Identificação acadêmica

**Finalidade.** Exibir os cinco atributos que o arquivo de entrada pré-preenche —
curso, nível, campus, ano e semestre de conclusão ([`leiaute-entrada.md`](leiaute-entrada.md),
seção 11) —, editáveis pelo respondente. A alteração é registrada como correção e o
valor original é preservado, conforme o documento do projeto.

**O que sai do Bloco I.** No instrumento vigente, campus, tipo e nome do curso são
as primeiras perguntas do Bloco I
([fichamento do portal](../pesquisa/fichamentos/ifsp-portal-egressos-2022.md)).
Aqui deixam de ser perguntas e passam a confirmação do que a instituição já sabe —
a limitação 4 da linha de base.

**Indicadores.**

- **Ind2** conta os egressos por ano, câmpus, nível e curso "no sistema e relativo
  aos respondentes dos questionários". A primeira parte sai da base de
  participantes; a segunda, dos valores confirmados neste bloco.
- **Recorte de todos os demais.** É daqui que vêm os cortes por curso, campus, nível
  e coorte.
- **Qualidade da base.** A proporção de correções por atributo mede a
  desatualização do sistema de origem — é a "auditoria da qualidade da base" para
  a qual o documento do projeto manda preservar o valor original. E a LGPD garante
  ao titular a correção de dados "incompletos, inexatos ou desatualizados" (art.
  18, III), e não só a confirmação.

### 3.3 Contato e manifestações

**Finalidade.** Permitir ao egresso atualizar as vias de contato do leiaute — os
campos `email_principal`, `email_alternativo` e `telefone` da E11 — e manifestar
recusa de contato para os ciclos seguintes.

**Indicadores.** Controle, em duas frentes:

- **Manutenção da base.** O contato atualizado pelo próprio egresso previne a
  devolução que a P8 trataria depois. O Regulamento pede ao egresso, "de forma
  colaborativa", que mantenha seus dados de contato atualizados (art. 13, item 1), e
  inclui entre as atividades do programa a manutenção de banco de dados atualizado
  (Regulamento, art. 11, item 4).
- **Respeito à recusa.** É uma terceira via de manifestação da recusa de contato,
  além da tela inicial e da mensagem previstas na P6 — para quem respondeu e não
  quer ser procurado de novo.

**O que prevalece.** Quando o contato informado aqui diverge do que a próxima
extração institucional trouxer, a regra de precedência é a que a E17 ainda precisa
decidir (`leiaute-entrada.md`, seção 11).

**O que fica de fora: "adesão voluntária".** O bloco 7 do documento a previa. É
relacionamento, não medida, e a colaboração voluntária do egresso exige termo de
adesão próprio (Regulamento, art. 40, item 4). Vai para a E24.

## 4. Os blocos de coleta

### 4.1 Bloco I — Avaliação da Formação

**Indicador: Ind19** — "média do nível geral de satisfação dos egressos em relação à
formação recebida no Instituto", em escala de 1 a 10. Origem: Anexo I.

**Outras finalidades do Regulamento que desembocam aqui**, sem indicador próprio no
Anexo I: avaliar a formação a partir do impacto na vida profissional (art. 3º,
item 3), a importância do estágio para a inserção (art. 3º, item 4), oferecer ao egresso
ferramenta para avaliar o curso (art. 3º, item 7) e as questões sobre conteúdo
programático, estágios e atividades de extensão, pesquisa e inovação (art. 20,
§2º). O bloco já existe pelo Ind19; se cada um desses itens entra como campo é
decisão da E13, pelo mesmo critério aplicado aqui aos blocos.

**Público:** todos.

### 4.2 Bloco II — Atividade Profissional Anterior

**Sem indicador no Anexo I.** Objetivo que o bloco operacionaliza: "avaliar a
formação ofertada pelo IFSP, a partir do impacto na vida profissional dos
egressos" (art. 3º, item 3). Impacto pressupõe comparação, e a comparação pressupõe
saber o que o egresso fazia antes.

**Indicador mínimo proposto:** proporção dos egressos com atividade remunerada que
já a exerciam antes do ingresso no curso. Origem: objetivo + projeto.

**Por que este.** O Ind3 não distingue a inserção obtida depois do curso da que já
existia quando o egresso entrou. Dois cursos com o mesmo índice podem ter formado
trabalhadores ou apenas recebido trabalhadores já formados no mercado, e o índice
sozinho não separa os dois casos. O bloco dá ao Ind3 a linha de base individual
que ele não tem.

**Limite de leitura, declarado.** O nome do bloco não diz "anterior a quê". A
leitura que o faz servir a um objetivo expresso é "anterior ao ingresso no curso".
O conteúdo vigente do bloco — as questões 7 a 14 — não foi relido nesta etapa, e a
E13 precisa confrontar essa leitura com o conteúdo que o projeto correlato trouxer.

**Público:** todos.

### 4.3 Bloco III — Situação Atual

**Indicador: Ind3** — "percentual de egressos que exercem alguma atividade
remunerada em relação ao total de egressos respondentes". Origem: Anexo I.

**É o bloco direcional.** Sua resposta divide os respondentes entre o Bloco V e o
Bloco VI, e a bifurcação está confirmada nos dados do instrumento vigente
([linha de base](../pesquisa/linha-de-base.md), seção 2). É o único bloco cuja
resposta decide o que vem depois, o que o torna obrigatório por consequência —
matéria da E13 e da E14.

**"Atividade remunerada", não "emprego formal".** O Anexo I mede atividade
remunerada, o que inclui autônomos, pessoa jurídica, trabalho por plataforma e
atuação no exterior — exatamente as categorias que, segundo o documento do
projeto, o registro administrativo não capta e o instrumento declarado capta.

**Público:** todos.

### 4.4 Bloco IV — Evolução na Formação

**Indicadores: Ind5 a Ind12.** Origem: Anexo I. São quatro índices, cada um em
duas versões — técnicos (ímpares) e graduação (pares): verticalização no IFSP,
verticalização qualificada (no IFSP em relação a qualquer instituição),
continuidade em qualquer instituição e continuidade em área correlata.

**O que o bloco precisa distinguir, pelas descrições:**

1. se o egresso **concluiu** ou **está matriculado** em curso do nível seguinte —
   as descrições dos Ind9 a Ind12 contam os dois casos, e as fórmulas só o segundo;
2. se o curso é **no IFSP** ou em **outra instituição** — é o que separa
   verticalização de continuidade;
3. se é na **mesma área** de formação — o que os Ind11 e Ind12 exigem.

As três distinções são exigidas pelas descrições, e são mais do que as fórmulas
pedem (seção 6). Coletar o que as descrições exigem permite calcular as duas
versões; o contrário não.

**Público da parte de continuidade: egressos de nível técnico e de graduação.** O
Anexo I só define os Ind5 a Ind12 para esses dois níveis. Para o egresso de
pós-graduação, a parte de continuidade não alimenta indicador algum e não deve ser
exibida — decide o `nivel` pré-preenchido, e é regra para a E14.

**Demandas de formação: objetivo + projeto.** O Regulamento manda coletar dados
sobre "necessidades de formação continuada" (art. 14, item 3) e tem entre os objetivos
"identificar demandas de formação nas dimensões de ensino, pesquisa e extensão"
(art. 3º, item 12), sem indicador no Anexo I. **Indicador mínimo proposto:** a
distribuição das demandas de formação declaradas. É o que o bloco 6 do documento
do projeto chamava de "demanda por pós-graduação e extensão". **Público:** todos,
inclusive a pós-graduação.

### 4.5 Bloco V — Perfil do Egresso no Mercado de Trabalho

**Indicadores: Ind4 e Ind13 a Ind18.** Origem: Anexo I.

**Público: quem tem atividade remunerada** — o denominador do Ind4 e a população
dos Ind13 a Ind18. É o ramo do Bloco III.

**Sete indicadores, cinco dados.**

| Dado | Indicadores que o usam |
|---|---|
| relação da atividade com a área de formação | Ind4, e o corte dos Ind15 e Ind16 |
| remuneração | Ind13 |
| satisfação com a remuneração, de 1 a 10 | Ind14, Ind15 e Ind16 |
| satisfação com a atividade profissional, de 1 a 10 | Ind17 |
| afinidade entre a atividade e o curso, de 1 a 10 | Ind18 |

Os Ind15 e Ind16 não acrescentam campo: são o Ind14 cortado pela classificação do
Ind4. Não há, portanto, sete perguntas a fazer, e a E13 não deve criar campos
redundantes para eles.

**Duas decisões que a E13 herda.**

- **Ind4: autodeclaração ou classificação?** O Ind4 é binário — a atividade é
  "diretamente relacionada" à formação ou não —, e o Ind18 é um grau de afinidade.
  A linha de base já registrou que o Ind4 pode ser autodeclarado ou derivado, e que
  a escolha muda o campo.
- **Ind13: valor ou faixa?** A descrição pede "média da remuneração declarada;
  maior e menor remuneração; remuneração mais frequente", e o mesmo indicador fixa
  cinco faixas de rendimento, a última aberta ("acima de R$ 4.664,68"). Com faixas,
  obtém-se a mais frequente e uma média aproximada, mas não a maior nem a menor.
  Com valor declarado, obtêm-se as quatro estatísticas, ao preço de uma pergunta
  mais sensível para o respondente.

**Área de atuação.** O Regulamento tem entre os objetivos "identificar e relacionar
as áreas de atuação profissional com os níveis de remuneração" (art. 3º, item 6), o que
dá consumidor à área de atuação — o bloco 4 do documento do projeto. Setor e
localidade, que o mesmo bloco 4 também previa, não têm indicador nem objetivo que
os peça. A E13 os justifica ou os retira.

### 4.6 Bloco VI — Motivos da Não Inserção no Mercado de Trabalho

**Sem indicador no Anexo I.** Objetivo que o bloco operacionaliza: "identificar os
elementos limitadores do acesso dos egressos ao mundo do trabalho" (art. 3º, item 5).

**Indicador mínimo proposto:** a distribuição dos elementos limitadores apontados
pelos respondentes sem atividade remunerada. Origem: objetivo + projeto. É o
complemento natural do Ind3: o Ind3 diz quantos não estão inseridos; este bloco diz
por quê.

**Público: quem não tem atividade remunerada** — o outro ramo do Bloco III. Os
Blocos V e VI particionam os respondentes.

### 4.7 Bloco VII — Avaliação da PAEG

**Sem indicador no Anexo I.** Objetivo que o bloco operacionaliza: "avaliar o grau
de sucesso e a efetividade das políticas de acompanhamento de egressos" (art. 34,
item 1), cujos resultados o Comitê analisa (art. 38).

**Indicador mínimo proposto:** a avaliação das ações do programa pelos
respondentes. Origem: objetivo + projeto. A escala é da E13 — que deve prever a
opção de não conhecer as ações, porque avaliação de quem não conhece o programa
não mede o programa.

**Público:** todos.

### 4.8 Recortes de equidade

**Sem indicador no Anexo I.** Objetivos que o bloco operacionaliza:

- "monitorar os espaços de inserção no mundo do trabalho e/ou continuidade nos
  estudos com os recortes comparativos de gênero e raça entre egressos" (art. 3º,
  item 16);
- "avaliar as políticas de ações afirmativas da instituição e sua respectiva
  percepção dentre egressos" (art. 3º, item 17);
- as diretrizes de diversidade étnico-racial, sexual e de gênero e de pessoas com
  deficiência (art. 4º, itens 3 e 4).

**Indicadores.** Os recortes não são indicadores novos: são cortes aplicados aos
indicadores de inserção (Ind3, Ind4) e de continuidade (Ind5 a Ind12). O único
acréscimo é a percepção das políticas de ações afirmativas (art. 3º, item 17). Origem:
objetivo + projeto.

**Por que bloco, e não atributo de entrada.** A E11 já havia encaminhado a questão:
se o instrumento perguntasse sexo, gênero ou raça/cor, seria questão, com
consentimento — não atributo de entrada (`leiaute-entrada.md`, seção 8.3). A
autodeclaração é do momento da resposta, e pode diferir do registro feito na
matrícula.

**Dado sensível, com três consequências.** Raça/cor é dado pessoal sensível por
definição expressa da LGPD (art. 5º, II, "origem racial ou étnica"), e deficiência
também o é, como dado referente à saúde. Por isso:

1. o bloco depende do consentimento específico e destacado da seção 3.1 (LGPD,
   art. 11, I) — sem ele, não é exibido;
2. cada questão oferece "prefiro não declarar", como o instrumento vigente já faz
   para raça/cor ([linha de base](../pesquisa/linha-de-base.md), seção 5);
3. o bloco inteiro é opcional.

**Gênero, e não sexo.** O objetivo do art. 3º, item 16, fala em gênero, e o instrumento
vigente pergunta sexo. O domínio é da E13.

**Público:** todos, com resposta opcional.

## 5. Correspondências

### 5.1 Com os blocos do documento do projeto

| Bloco do documento | Nesta estrutura | Observação |
|---|---|---|
| 1. Consentimento | Consentimento | acrescidas as duas recusas da P6 e o consentimento específico do dado sensível |
| 2. Identificação acadêmica | Identificação acadêmica | cinco atributos, com o nível (E11); o documento nomeava curso, campus e ano |
| 3. Situação ocupacional | Bloco III | o indicador passa a ser o Ind3 |
| 4. Caracterização da atuação | Bloco V | a área de atuação serve ao art. 3º, item 6; setor e localidade ficam com a E13 |
| 5. Aderência à formação | Bloco V | Ind18 e, conforme a E13, Ind4 |
| 6. Formação continuada | Bloco IV | Ind5 a Ind12 e a demanda de formação |
| 7. Contato e manifestações | Contato e manifestações | sem a adesão voluntária, que vai à E24 |
| — | Bloco I | ausente do documento: Ind19 |
| — | Bloco V, remuneração e satisfações | ausentes do documento: Ind13 a Ind17 |
| — | Blocos II, VI e VII e recortes de equidade | ausentes do documento |

### 5.2 Com o instrumento vigente

| Bloco | Questões no instrumento vigente | O que muda |
|---|---|---|
| I | 1 a 6 | campus, tipo e nome do curso saem para a identificação acadêmica, pré-preenchidos |
| II | 7 a 14 | — |
| III | 15 | — |
| IV | 16 | a parte de continuidade passa a depender do nível |
| V | 19 a 28 | — |
| VI | 17 e 18 | — |
| VII | 29 e 30 | — |

A numeração é a da [linha de base](../pesquisa/linha-de-base.md), seção 2. O
conteúdo das questões não foi relido nesta etapa, porque a estrutura não depende
dele.

## 6. Divergências do Anexo I

As fórmulas do Anexo I são texto no PDF do Regulamento, e não imagem, como a linha
de base registrava. Extraídas e conferidas contra as páginas, várias divergem da
descrição do próprio indicador:

| Indicador | A descrição diz | A fórmula diz | Natureza |
|---|---|---|---|
| Ind7 | técnicos no superior do IFSP ÷ técnicos que concluíram ou cursam o superior **em qualquer instituição** | ÷ total de egressos técnicos do IFSP — a mesma fórmula do Ind5 | **mede outra coisa**: com a fórmula, o Ind7 é o Ind5 |
| Ind11 | técnicos no superior em área correlata ÷ técnicos que **concluíram ou cursam** o superior | ÷ total de egressos técnicos | **mede outra coisa** |
| Ind12 | graduados na pós **em área correlata** ÷ graduados que concluíram ou cursam a pós | a mesma fórmula do Ind10, sem área correlata | **mede outra coisa**: com a fórmula, o Ind12 é o Ind10 |
| Ind9 a Ind12 | contam quem **concluiu ou está matriculado** no nível seguinte | contam quem está **cursando** | alcance do numerador |
| Ind3 | ÷ total de egressos **respondentes** | ÷ "total de egressos" | ambiguidade, que a descrição resolve |
| Ind8 | — | rótulo "IVEqt", que é o do Ind7 | rótulo |
| Ind13 | média, maior e menor remuneração e a mais frequente | faixas de rendimento, a última aberta | tensão entre descrição e domínio (seção 4.5) |

A fórmula do Ind11 aparece, além disso, cortada na margem da página.

**Regra adotada: a descrição prevalece.** Por três razões:

1. a descrição é o texto que define o indicador, coerente com o nome e com o
   propósito — um "índice de verticalização qualificada" idêntico ao de
   verticalização simples não tem razão de existir;
2. as fórmulas do Ind7 e do Ind12 são cópias literais das do Ind5 e do Ind10, o
   que aponta erro de edição, e não intenção;
3. coletar o que as descrições exigem permite calcular as duas versões; o
   contrário não.

A regra é **decisão de projeto**: o Regulamento não a enuncia, e a instituição pode
decidir de outro modo. Por isso a divergência precisa chegar a quem pode
resolvê-la — o Comitê Permanente, a quem o art. 42 atribui os casos omissos.

## 7. Verificação do critério de conclusão

O critério é que nenhum bloco exista sem indicador correspondente. Verifica-se nos
dois sentidos, como na E11.

### 7.1 Nenhum bloco sem indicador

| Bloco | Indicador | Origem |
|---|---|---|
| Consentimento | registro do consentimento; tratamento da recusa | controle |
| Identificação acadêmica | Ind2; qualidade da base | Anexo I + controle |
| I | Ind19 | Anexo I |
| II | proporção dos inseridos que já exerciam atividade remunerada antes do curso | objetivo + projeto |
| III | Ind3 | Anexo I |
| IV | Ind5 a Ind12; demandas de formação | Anexo I; objetivo + projeto |
| V | Ind4, Ind13 a Ind18 | Anexo I |
| VI | distribuição dos elementos limitadores | objetivo + projeto |
| VII | avaliação das ações do programa | objetivo + projeto |
| Recortes de equidade | recortes de inserção e continuidade; percepção das ações afirmativas | objetivo + projeto |
| Contato e manifestações | manutenção da base; respeito à recusa | controle |

**Onze blocos, nenhum sem indicador.**

### 7.2 Todo indicador do Anexo I tem bloco

| Indicador | Bloco que o alimenta |
|---|---|
| Ind1 | **nenhum** — é a listagem das atividades realizadas para egressos, dado dos registros da instituição e não do questionário |
| Ind2 | base de participantes ("no sistema") e identificação acadêmica ("relativo aos respondentes") |
| Ind3 | III |
| Ind4 | V |
| Ind5 a Ind12 | IV, com o nível da identificação acadêmica |
| Ind13 a Ind18 | V |
| Ind19 | I |

**Dezoito dos dezenove indicadores são alimentados pelo instrumento**, e o Ind1 fica
fora por não ser dado de questionário.

### 7.3 Todo objetivo de coleta do art. 3º tem bloco

Dos dezessete objetivos do art. 3º, dez pedem dado do egresso, e todos têm bloco.
Os outros sete são ação institucional ou o próprio mecanismo, e não bloco de
questionário.

| Itens do art. 3º | Onde |
|---|---|
| 1 (inserção) e 2 (relação entre ocupação e formação) | Blocos III e V |
| 3 (impacto na vida profissional) | Blocos I e II |
| 4 (importância do estágio) e 7 (avaliar o curso) | Bloco I |
| 5 (elementos limitadores) | Bloco VI |
| 6 (áreas de atuação e remuneração) | Bloco V |
| 12 (demandas de formação) | Bloco IV |
| 16 (recortes de gênero e raça) e 17 (ações afirmativas) | Recortes de equidade |
| 8 (meios tecnológicos de contato) e 15 (banco de dados) | o próprio mecanismo |
| 9, 10, 11, 13 e 14 (formação continuada, emprego, empreendedorismo, eventos, redes) | ação institucional — E24 |

**Resultado.** Onze blocos, nenhum sem indicador; dezoito dos dezenove indicadores
do Anexo I alimentados; todos os objetivos de coleta do art. 3º com bloco.
**Critério atendido.**

## 8. Correspondência prevista com a plataforma

Hipótese de trabalho para a E15, **não verificada nesta etapa**:

- cada bloco é um grupo de questões do LimeSurvey, e o público de cada bloco vira a
  condição de exibição do grupo;
- a identificação acadêmica usa os atributos do participante, cuja existência a E08
  conferiu (C9), e a mecânica de exibir e corrigir o valor pré-preenchido é da E18;
- o consentimento pode ser grupo próprio ou recurso nativo da plataforma, e a E22
  decide depois de conferir o que a instância oferece.

## 9. O que esta especificação não permite afirmar

1. **Os indicadores propostos pelo projeto não são indicadores institucionais.**
   São a operacionalização mínima de objetivos expressos do Regulamento — Blocos
   II, VI e VII, demandas de formação e recortes de equidade — e a instituição pode
   redefini-los. Não devem ser apresentados como parte do Anexo I.
2. **O conteúdo vigente dos blocos não foi relido.** A finalidade de cada bloco
   parte do nome dado pelo art. 17 e do objetivo que ele operacionaliza, e não das
   questões atuais. É limitação sobretudo para o Bloco II (seção 4.2).
3. **"A descrição prevalece" é decisão de projeto**, não regra do Regulamento
   (seção 6).
4. **Nada foi implementado nem conferido na plataforma.**
5. **Nada aqui é resultado sobre egressos.**

## 10. O que mudou em relação ao documento do projeto

| Onde | Documento do projeto | Esta especificação |
|---|---|---|
| estrutura | sete blocos próprios | os sete do art. 17, três de controle e um de equidade |
| referência de indicador | indicadores definidos no próprio documento | Anexo I, ou objetivo expresso do Regulamento com origem declarada |
| cobertura do Anexo I | seis indicadores sem bloco | dezoito de dezenove, e o Ind1 fora por não ser dado de questionário |
| identificação acadêmica | curso, campus e ano | cinco atributos, com nível e semestre |
| adesão voluntária | no bloco de contato | fora; relacionamento, da E24 |

**Sem alteração de escopo, meta ou cronograma**: o documento prevê refinamento das
suas definições preliminares "mediante registro da justificativa no relatório
final". Fica como pendência da **E31**, junto com a comunicação das divergências do
Anexo I ao Comitê Permanente.

## 11. O que esta especificação determina para as etapas seguintes

- **E13 (domínios)** — aplicar aos campos o mesmo critério aplicado aqui aos
  blocos, com a mesma escala de origem; fechar no Bloco IV as três distinções da
  seção 4.4; decidir se o Ind4 é autodeclarado ou derivado e se o Ind13 é valor ou
  faixa; justificar ou retirar setor e localidade; prever "prefiro não declarar"
  nos recortes de equidade e "não conheço" no Bloco VII; decidir entre gênero e
  sexo; confirmar a leitura "anterior ao ingresso" do Bloco II contra o conteúdo do
  projeto correlato; e fixar a obrigatoriedade, a começar pelo Bloco III, que é
  obrigatório por consequência.
- **E14 (navegação)** — os públicos da seção 2 viram regras: Bloco V só com
  atividade remunerada; Bloco VI só sem; a parte de continuidade do Bloco IV só
  para técnico e graduação; recortes de equidade só com o consentimento
  específico; e as duas recusas do consentimento encerram o preenchimento.
- **E15 (implementação)** — bloco é grupo de questões; a estrutura exportada e
  versionada tem de reproduzir os onze.
- **E18 (pré-preenchimento)** — os cinco atributos do bloco de identificação, com a
  correção registrada e o valor original preservado.
- **E22 (consentimento)** — três manifestações: as duas recusas da P6 e o
  consentimento específico e destacado do dado sensível, cuja negativa só dispensa
  os recortes de equidade.
- **E23 (conformidade)** — a correção de atributo pré-preenchido e a atualização de
  contato entram na trilha de auditoria; o dado sensível exige tratamento próprio
  na anonimização.
- **E24 (recomendações)** — a adesão voluntária (art. 40) e os objetivos de ação
  institucional do art. 3º (itens 9, 10, 11, 13 e 14).
- **E25 (matriz)** — o requisito "registro do consentimento" passa a incluir o
  consentimento específico; o requisito "navegação condicional" é redigido contra
  os públicos da seção 2.
- **E28 (extração)** — calcular os indicadores pelas descrições, e registrar a
  divergência com as fórmulas; aplicar os recortes de equidade aos Ind3, Ind4 e
  Ind5 a Ind12.
- **E29 (painel)** — exibir separados os indicadores do Anexo I e os propostos pelo
  projeto, com o rótulo de origem.
- **E31 (relatório final)** — atualizar a tabela de blocos no documento do projeto;
  comunicar ao Comitê Permanente as divergências da seção 6; e declarar os
  indicadores propostos como propostas.

## 12. Domínios, obrigatoriedade e validações

*Seção a preencher pela **E13**, que completa este arquivo em vez de criar outro.*
