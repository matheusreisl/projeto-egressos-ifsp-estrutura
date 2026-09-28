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
| 3 | I — Avaliação da Formação | avaliação, pelo egresso, da formação recebida e do seu impacto | Ind19; impacto do curso (E13) | Anexo I; objetivo + projeto (art. 3º, item 3) | todos |
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

**O nome e o conteúdo documentado não coincidem.** *Atualizado na E13.* No
instrumento descrito pelo Relatório 2 da PAE, o Bloco I não avalia a formação: reúne
sexo, raça/cor, escolaridade, campus, tipo de curso e modalidade. Esses campos vão
para a identificação acadêmica, para os recortes de equidade ou saem, e o Bloco I
recebe as duas questões de impacto que o instrumento documentado guardava no
Bloco VII (seções 4.7 e 12.3).

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

**Limite de leitura — resolvido na E13.** O nome do bloco não diz "anterior a quê",
e a E12 adotou "anterior ao ingresso no curso" sem ter relido o conteúdo. O
Relatório 2 da PAE confirma a leitura: a questão 7, que abre o bloco, é "Você
trabalhava quando entrou no curso do IFSP?".

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
os peça. A E13 os justifica ou os retira. *Resolvido na E13:* a área de atuação é
registrada pelo setor de atividade, com o domínio da questão 20 do instrumento
documentado, e a localidade sai (seção 12.3).

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

**O conteúdo documentado é outro.** *Atualizado na E13.* No instrumento descrito
pelo Relatório 2 da PAE, o Bloco VII — ali "Avaliação da PAE" — não avalia o
programa. Suas duas questões medem o impacto do curso: a situação profissional atual
comparada à do ingresso (questão 29) e uma nota de 1 a 10 para a contribuição do
curso ao trabalho atual (questão 30). Decidido com o orientando: as duas vão para o
Bloco I, que avalia a formação pelo impacto (art. 3º, item 3), e o Bloco VII fica com
a avaliação do programa, como a E12 e a ADR-0006 estabeleceram, em campo novo
(seção 12.3).

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

| Bloco | Questões no instrumento documentado | O que muda — *atualizado na E13* |
|---|---|---|
| I | 1 a 6 | sexo e raça/cor vão para os recortes de equidade; campus e tipo de curso, para a identificação acadêmica, pré-preenchidos; escolaridade e modalidade saem; o bloco recebe as questões 29 e 30 e o Ind19 |
| II | 7 a 14 | ficam a 7 e o vínculo anterior (10); saem setor, porte, benefícios, horas e renda anteriores |
| III | 15 | ganha o vínculo atual (22), que decide quem tem atividade remunerada |
| IV | 16 | reestruturado nas três distinções das descrições do Anexo I, mais as demandas de formação |
| V | 19 a 28 | ficam a relação com a área (24) e o setor (20); a renda passa a faixas; entram as escalas dos Ind14 a Ind18; saem as demais |
| VI | 17 e 18 | as duas viram um campo só |
| VII | 29 e 30 | as duas vão para o Bloco I; entra a avaliação do programa |

A numeração é a da [linha de base](../pesquisa/linha-de-base.md), seção 2. *Atualizado
na E13:* a E12 não releu o conteúdo das questões; a E13 o leu no Relatório 2 da PAE,
que descreve o instrumento de 2019 a 2023, e o detalhe está na seção 12.

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
| I | Ind19; impacto do curso (E13) | Anexo I; objetivo + projeto |
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
   questões atuais. É limitação sobretudo para o Bloco II (seção 4.2). *Atualizado
   na E13:* o conteúdo documentado foi lido no Relatório 2 da PAE. Confirmou a
   leitura do Bloco II e mostrou que os Blocos I e VII tinham conteúdo diferente do
   nome (seções 4.1 e 4.7). A versão hoje no ar não foi percorrida, e já difere
   da documentada (seção 12.1).
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

**Etapa:** E13 — definir domínios, obrigatoriedade e validações
**Data:** 28/09/2026
**Conclusão quando:** todo campo padronizável tiver domínio fechado

Esta seção completa o arquivo: que campos cada bloco tem, de que tipo, com que
domínio, obrigatoriedade e regra de validação; como o pré-preenchimento se comporta
quando o dado de origem está desatualizado; e o que saiu do instrumento. O **texto**
de cada pergunta continua fora — vem do projeto correlato. Código, tipo e domínio
são estrutura.

### 12.1 Ponto de partida: o instrumento documentado

O Relatório 2 da PAE, que cobre 2019 a 2023, publica as trinta questões do
instrumento institucional com todas as opções de resposta. É o **instrumento
documentado**, e não necessariamente o vigente: a tela inicial observada em 2026
([fichamento do portal](../pesquisa/fichamentos/ifsp-portal-egressos-2022.md)) tem
uma pergunta de nome do curso em texto livre que o relatório não mostra. A versão no
ar não foi percorrida, porque percorrê-la criaria registros na base real.

**O que o relatório mostrou, em três pontos.**

1. **Nome e conteúdo divergem em dois blocos** — o I, que não avalia a formação, e
   o VII, que mede impacto e não avalia o programa (seções 4.1 e 4.7). O Bloco II
   confirmou a leitura da E12 (seção 4.2).
2. **O instrumento documentado calcula pouco do Anexo I**, que é de 2025:

   | Indicadores | O que o instrumento documentado permite |
   |---|---|
   | Ind3 | só combinando duas questões: "trabalhando" (questão 15) inclui trabalho sem remuneração — a questão 22 tem "estagiário não remunerado" e "negócio familiar sem remuneração" |
   | Ind4 | a questão 24 serve |
   | Ind5 a Ind12 | a questão 16 só pergunta a quem está matriculado agora, não tem opção de pós-graduação e não pergunta a área: os indicadores de graduação, os de área correlata e a conclusão do nível seguinte ficam sem dado |
   | Ind13 | a renda era pergunta aberta, e o próprio relatório só publicou menor e maior valor, "por ser uma pergunta aberta que recebeu respostas em diversos formatos" |
   | Ind14 a Ind19 | nenhuma escala de 1 a 10; a questão 30 mede a contribuição do curso para o trabalho, que é outro constructo |

   É o padrão que a linha de base já havia encontrado: a norma à frente do suporte
   técnico.
3. **Parte do instrumento documentado serve, e é reaproveitada** para preservar a
   série histórica: questões 2, 7, 10, 15, 17, 20, 22, 24, 29 e 30.

**Escala de origem do domínio.** Na mesma lógica da seção 1.2:

| Rótulo | Significado |
|---|---|
| **Anexo I** | o domínio é fixado pelo Anexo I do Regulamento — escalas de 1 a 10 e faixas de rendimento |
| **documentado** | o domínio reproduz o do instrumento documentado, com o número da questão |
| **oficial** | o domínio segue classificação ou definição de norma externa |
| **E11** | o domínio é o do arquivo de entrada |
| **projeto** | domínio definido por este projeto |

### 12.2 Regras gerais

1. **Campo precisa de consumidor** — indicador do Anexo I, objetivo expresso do
   Regulamento com indicador proposto, ou controle —, com a mesma escala da seção
   1.2. É o critério da ADR-0006 aplicado aos campos.
2. **Campo padronizável tem domínio fechado.** Onde a exaustividade exige, há uma
   categoria residual — "outro" —, **sem** campo de texto acoplado: é a diretriz do
   documento do projeto de substituir texto livre por domínio fechado.
3. **Campos não padronizáveis são quatro** — os três de contato, validados pela
   sintaxe da [E11](leiaute-entrada.md), e um de sugestões, o único texto livre do
   instrumento (seção 12.3).
4. **Obrigatoriedade**, pela regra do documento do projeto: são obrigatórios os
   campos de situação ocupacional (Bloco III) e de aderência à formação (os dois
   primeiros do Bloco V), além das manifestações do consentimento e da confirmação
   da identificação. **Os demais são opcionais**, "de modo a não onerar o
   respondente nem induzir abandono". Campo condicional só é obrigatório quando
   exibido.
5. **Escalas de 1 a 10** são escolha única entre dez valores, em que 1 é o menor grau
   e 10 o maior. Os rótulos dos extremos são texto, e vêm com as perguntas.
6. **Três domínios são configuração** da instituição, versionada por ciclo: a lista
   de cursos, a lista de unidades e as faixas de rendimento, cujos valores em reais
   envelhecem.
7. **Os códigos são propostos**: alfanuméricos, começando por letra, com prefixo do
   bloco. A E15 confere se a plataforma os aceita.

### 12.3 Campos por bloco

**Consentimento** — público: todos.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| CON1 | manifestação sobre o termo | escolha única | concordo · não concordo com o termo neste ciclo · não quero mais ser contatado | sim | registro do consentimento; P6 | projeto (P6) |
| CON2 | consentimento específico para os recortes de equidade | escolha única | concordo · não concordo | sim, se exibido | LGPD, art. 11, I | projeto |

CON2 só é exibido se CON1 for "concordo". Data, hora e versão do termo são
metadados registrados pela plataforma, e não campos — é a E22 que os implementa.

**Identificação acadêmica** — público: todos. Os cinco campos vêm pré-preenchidos
(seção 12.5).

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| IDA1 | curso | escolha única | lista de cursos da instituição, cada curso com o seu nível | sim | Ind2; recortes; qualidade da base | E11 |
| IDA2 | nível | derivado do curso | técnico · graduação · pós-graduação | — | Ind2; Ind5 a Ind12; exibição do Bloco IV | E11 |
| IDA3 | campus | escolha única | lista de unidades, **com as instituições antecessoras** | sim | Ind2; recortes | E11; documentado (4) |
| IDA4 | ano de conclusão | número inteiro | quatro dígitos, do limite configurado ao ano corrente | sim | Ind2; coorte | E11 |
| IDA5 | semestre de conclusão | escolha única | 1 · 2 | sim | coorte; turma do art. 19 | E11 |

**Decisão que a E11 deixou para cá: a lista de cursos registra o nível de cada
curso.** Com isso, o nível deixa de ser editável por conta própria — ele acompanha o
curso escolhido —, e a coerência entre `curso` e `nivel` vira regra de validação do
arquivo de entrada, como a seção 4.4 do leiaute previa.

**A lista de unidades inclui as instituições antecessoras.** O instrumento
documentado já as oferece — Escola Industrial de São Paulo e Escola Técnica de São
Paulo, Escola Técnica Federal de São Paulo, CEFET-SP (questão 4) —, porque há
egressos delas no universo do programa. Uma lista só com os campi atuais deixaria
esses egressos sem valor possível.

**Bloco I — Avaliação da Formação** — público: todos.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| AF1 | satisfação com a formação recebida no IFSP | escala | 1 a 10 | não | Ind19 | Anexo I |
| AF2 | situação profissional atual comparada à do ingresso | escolha única | melhor · igual · pior | não | impacto do curso (art. 3º, item 3) | documentado (29) |
| AF3 | contribuição do curso para a situação de trabalho atual | escala | 1 a 10 | não | impacto do curso (art. 3º, item 3) | documentado (30) |
| AF4 | sugestões para a melhoria do curso | texto livre | até 1.000 caracteres | não | direito do egresso (Regulamento, art. 12, item 4) | projeto |

AF2 e AF3 vieram do Bloco VII documentado (seção 4.7). Os indicadores propostos para
eles são a distribuição da comparação e a média da contribuição — origem
objetivo + projeto. **AF4 é o único texto livre do instrumento**, e é o campo com
maior risco de conter dado pessoal não previsto, inclusive de terceiros: é tratado
antes de qualquer exportação (E23).

**Bloco II — Atividade Profissional Anterior** — público: todos.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| AP1 | trabalhava quando entrou no curso | escolha única | sim · não | não | indicador do Bloco II | documentado (7) |
| AP2 | vínculo quando entrou no curso | escolha única | o mesmo de SA2 | não | indicador do Bloco II; comparação entre antes e agora | documentado (10) |

AP2 só é exibido se AP1 for "sim". É ele que diz se a atividade anterior era
**remunerada** — o que o indicador do bloco exige, e que "trabalhava" sozinho não
diz.

**Bloco III — Situação Atual** — público: todos. É o bloco direcional.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| SA1 | situação atual | escolha única | estudando · trabalhando · estudando e trabalhando · nem trabalhando, nem estudando | sim | Ind3; exibição dos Blocos V e VI | documentado (15) |
| SA2 | vínculo de trabalho atual | escolha única | assalariado de empresa ou organização privada com carteira assinada · assalariado sem carteira assinada · empregado ou servidor público · autônomo · microempresário · proprietário agrícola · estagiário remunerado · estagiário não remunerado · em negócio familiar sem remuneração | sim, se exibido | Ind3; espaços de inserção (art. 3º, item 16); comparação com AP2 | documentado (22) |

SA2 é exibido se SA1 incluir "trabalhando". **Tem atividade remunerada** quem está
trabalhando **e** não é estagiário não remunerado nem trabalha em negócio familiar
sem remuneração. O estágio remunerado conta, pela letra do Anexo I: "alguma
atividade remunerada".

**O vínculo sobe do Bloco V para o III** — no instrumento documentado era a questão
22. Precisa vir antes da bifurcação, porque é ele que decide quem tem atividade
remunerada, e portanto quem segue para o V e quem segue para o VI.

**Lacuna registrada.** O domínio documentado não nomeia pessoa jurídica,
microempreendedor individual nem trabalho por plataforma, que ficam absorvidos por
"autônomo" e "microempresário". Mantém-se o domínio pela série; desdobrá-lo é
decisão que a instituição pode tomar, declarando o indicador.

**Bloco IV — Evolução na Formação** — público: todos; EF1 a EF3 só para técnico e
graduação.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| EF1 | situação no nível seguinte ao do curso concluído | escolha única | concluí · estou matriculado · não | não | Ind5 a Ind12 | projeto (descrições do Anexo I) |
| EF2 | instituição desse curso | escolha única | IFSP · outra instituição | não | Ind5 a Ind8 | documentado (16), agregado |
| EF3 | esse curso é na mesma área de formação | escolha única | sim, totalmente · sim, parcialmente · não · não sei | não | Ind11, Ind12 | documentado (escala da 24) |
| EF4 | demandas de formação | escolha múltipla | curso técnico · graduação · especialização · mestrado ou doutorado · curso de extensão ou de curta duração · nenhuma no momento | não | demandas de formação (art. 3º, item 12; art. 14, item 3) | projeto |

**"Nível seguinte"** é o superior, para o egresso técnico, e a pós-graduação, para o
de graduação. EF2 e EF3 só são exibidos se EF1 não for "não". Em EF4, "nenhuma no
momento" exclui as demais opções.

**EF2 agrega o domínio documentado.** A questão 16 separava instituição pública de
privada, distinção que nenhum indicador usa. A série se preserva pela união das duas.

**EF3 usa a mesma escala da relação com a área** (PM1), pela coerência: "mesma área"
conta só com "sim, totalmente", como no Ind4.

**Bloco V — Perfil do Egresso no Mercado de Trabalho** — público: quem tem atividade
remunerada.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| PM1 | relação da atividade com a área de formação | escolha única | sim, totalmente · sim, parcialmente · não · não sei | sim | Ind4; corte dos Ind15 e Ind16 | documentado (24) |
| PM2 | afinidade entre as atividades e o conteúdo do curso | escala | 1 a 10 | sim | Ind18 | Anexo I |
| PM3 | remuneração bruta mensal | escolha única | as cinco faixas do Anexo I | não | Ind13 | Anexo I, como configuração |
| PM4 | satisfação com a remuneração | escala | 1 a 10 | não | Ind14; Ind15 e Ind16 pelo corte de PM1 | Anexo I |
| PM5 | satisfação com a atividade profissional | escala | 1 a 10 | não | Ind17 | Anexo I |
| PM6 | setor de atividade | escolha única | indústria · comércio · transportes · construção civil · agricultura e pecuária · serviços sociais (saúde, educação, assistência) · serviços financeiros · serviços de utilidade pública (água, energia, saneamento, limpeza urbana) · demais serviços · outro | não | áreas de atuação e remuneração (art. 3º, item 6) | documentado (20) |

**PM1 e o Ind4.** "Diretamente relacionada à área de formação" conta **só** "sim,
totalmente". "Sim, parcialmente" fica fora do numerador e é informado à parte, como
análise de sensibilidade. É leitura estrita e declarada, e é decisão de projeto.

**PM3 e o Ind13.** As faixas são as do Anexo I — até R$ 2.259,20; de R$ 2.259,21 a
R$ 2.826,65; de R$ 2.826,66 a R$ 3.751,05; de R$ 3.751,06 a R$ 4.664,68; acima de
R$ 4.664,68 —, guardadas como configuração versionada por ciclo. Com elas, o Ind13
dá a faixa mais frequente e as faixas extremas observadas. **A média não é
calculável com rigor**, porque a última faixa é aberta. É adaptação declarada, e
entra na comunicação ao Comitê Permanente (seção 6).

**PM6 unifica o residual.** O domínio documentado tinha "outro" e "outros" como duas
categorias. Aqui é uma só.

**Bloco VI — Motivos da Não Inserção no Mercado de Trabalho** — público: quem não tem
atividade remunerada.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| MI1 | principal motivo de não exercer atividade remunerada | escolha única | decidi só estudar · os salários oferecidos são baixos · há pouca oferta de trabalho na região onde moro · não encontrei trabalho na área do curso realizado no IFSP · não tenho a qualificação exigida · não tenho a experiência exigida · motivos pessoais · outro | não | elementos limitadores (art. 3º, item 5) | documentado (17 e 18) |

O instrumento documentado tinha duas versões da mesma pergunta — a 18 sem "decidi
só estudar". Aqui é um campo só.

**Bloco VII — Avaliação da PAEG** — público: todos.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| AV1 | avaliação das ações do programa de acompanhamento | escolha única | 1 a 10 · não conheço as ações do programa | não | avaliação do programa (art. 34, item 1) | projeto |

O indicador tem duas partes: a média entre quem conhece as ações e a proporção de
quem não as conhece — que é, por si, medida do alcance do programa.

**Recortes de equidade** — público: quem deu o consentimento específico (CON2).

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| EQ1 | gênero | escolha única | mulher · homem · pessoa não binária · outra identidade · prefiro não declarar | não | recortes de gênero (art. 3º, item 16) | projeto |
| EQ2 | raça/cor | escolha única | preta · parda · indígena · amarela · branca · prefiro não declarar | não | recortes de raça (art. 3º, item 16) | oficial; documentado (2) |
| EQ3 | pessoa com deficiência | escolha única | sim · não · prefiro não declarar | não | recortes de deficiência (art. 4º, item 4) | projeto; conceito oficial |
| EQ4 | avaliação das políticas de ações afirmativas | escolha única | 1 a 10 · não conheço as políticas | não | percepção das ações afirmativas (art. 3º, item 17) | projeto |

- **EQ1 — gênero, e não sexo.** O objetivo do art. 3º, item 16 fala em gênero, e o
  gênero é autodeclarado. O instrumento documentado perguntava sexo — feminino,
  masculino, outro (questão 1) —, e **as duas séries não são equivalentes**: a
  correspondência entre "mulher" e "feminino", ou entre "homem" e "masculino", é
  aproximação, e deve ser declarada como tal em qualquer comparação.
- **EQ2 — raça/cor** reproduz as cinco categorias do quesito cor ou raça do IBGE, a
  que o Estatuto da Igualdade Racial remete para definir a população negra — pretos
  e pardos (Lei nº 12.288/2010, art. 1º, parágrafo único, IV). É o mesmo domínio do
  instrumento documentado; o rótulo "não desejo declarar" vira "prefiro não
  declarar", sem mudar a categoria.
- **EQ3 — deficiência** é autodeclaração binária, no conceito da Lei Brasileira de
  Inclusão: impedimento de longo prazo que, em interação com barreiras, pode obstruir
  a participação plena (Lei nº 13.146/2015, art. 2º). O recorte da diretriz não pede o
  tipo de deficiência.

**Contato e manifestações** — público: todos.

| Código | Dado | Tipo | Domínio | Obrig. | Consumidor | Origem |
|---|---|---|---|---|---|---|
| CT1 | e-mail principal atualizado | texto com validação | sintaxe da seção 4.6 do leiaute | não | P8, por prevenção | E11 |
| CT2 | e-mail alternativo atualizado | texto com validação | a mesma sintaxe, diferente de CT1 | não | P8 | E11 |
| CT3 | telefone atualizado | texto com validação | E.164, seção 4.7 do leiaute | não | P8; P9 | E11 |
| CT4 | não quero mais ser contatado nos próximos ciclos | caixa de marcação | marcada · não marcada | não | P6 | projeto (P6) |

Os campos de contato **não** vêm pré-preenchidos: são preenchidos só por quem quer
atualizar, o que evita exibir dado pessoal sem necessidade. No modo de ensaio,
valem as restrições da seção 7 do leiaute — endereço sob `.test` e código de área
terminado em 0 —, e a E15 as aplica também no questionário.

### 12.4 Como os campos compõem os indicadores

A verificação de suficiência desce aqui ao nível do campo. Os denominadores são os
respondentes do nível correspondente — a mesma leitura que a seção 6 fixou para o
Ind3.

| Indicador | Numerador | Denominador |
|---|---|---|
| Ind2 | respondentes por IDA1, IDA2, IDA3 e IDA4 | — |
| Ind3 | com atividade remunerada (SA1 e SA2) | respondentes |
| Ind4 | PM1 = sim, totalmente | com atividade remunerada |
| Ind5 / Ind6 | EF1 = matriculado e EF2 = IFSP | técnicos / graduados |
| Ind7 / Ind8 | EF1 = matriculado e EF2 = IFSP | técnicos / graduados com EF1 = concluí ou matriculado |
| Ind9 / Ind10 | EF1 = concluí ou matriculado | técnicos / graduados |
| Ind11 / Ind12 | EF1 = concluí ou matriculado e EF3 = sim, totalmente | técnicos / graduados com EF1 = concluí ou matriculado |
| Ind13 | distribuição de PM3 | com atividade remunerada |
| Ind14 | média de PM4 | com atividade remunerada |
| Ind15 / Ind16 | média de PM4 | com PM1 = sim, totalmente / com PM1 = não |
| Ind17 | média de PM5 | com atividade remunerada |
| Ind18 | média de PM2 | com atividade remunerada |
| Ind19 | média de AF1 | respondentes |

"Técnicos" e "graduados" são os respondentes com IDA2 igual a técnico ou a
graduação. No Ind16, "sim, parcialmente" e "não sei" ficam fora dos dois cortes, e
isso é declarado. Os indicadores propostos pelo projeto compõem-se do mesmo modo:
Bloco II, com AP1, AP2, SA1 e SA2; impacto, com AF2 e AF3; demandas, com EF4;
elementos limitadores, com MI1; programa, com AV1; e percepção das ações
afirmativas, com EQ4.

### 12.5 Pré-preenchimento com dado de origem desatualizado

O entregável da E13 pede, expressamente, este comportamento.

1. **Os cinco atributos aparecem com o valor da base**, e o respondente confirma ou
   corrige **dentro do domínio fechado**. Não há correção em texto livre.
2. **O valor original é preservado.** A resposta guarda o valor confirmado; o
   atributo do participante continua com o valor da base. É a "auditoria da
   qualidade da base" do documento do projeto (seção 3.2).
3. **A navegação usa o valor confirmado.** Se o respondente corrige o curso, e com
   ele o nível, é o nível corrigido que decide se a parte de continuidade do Bloco
   IV aparece (E14).
4. **Os indicadores "relativos aos respondentes" usam o valor confirmado**; os
   indicadores "no sistema", o da base.
5. **A correção não move o ciclo em andamento.** Ano e semestre de conclusão são a
   âncora da P5, e a âncora vem da base, não da autodeclaração: o mecanismo não
   reescreve o registro acadêmico por conta do que o respondente disse — o
   respondente pode errar, e a fonte é o sistema acadêmico. A correção entra na
   fila de revisão; se a extração seguinte trouxer o valor corrigido, a âncora muda
   então, pela regra da ADR-0005.
6. **A fila de revisão não é estrutura nova.** É a consulta dos registros em que o
   valor confirmado difere do original, por atributo — como a fila de correção de
   contato da E09. O que prevalece numa reimportação é a decisão que a E17 já tem
   pendente para o contato, agora estendida a estes atributos.
7. **A taxa de correção por atributo é o indicador de qualidade da base** da seção
   3.2.

### 12.6 Continuidade com a série documentada

| Questão documentada | Campo | Relação |
|---|---|---|
| 2 — raça/cor | EQ2 | idêntica; muda só o rótulo da recusa |
| 7 — trabalhava ao entrar | AP1 | idêntica |
| 10 — vínculo ao entrar | AP2 | idêntica |
| 15 — situação atual | SA1 | idêntica |
| 22 — vínculo atual | SA2 | idêntica; muda de bloco |
| 24 — trabalha na área | PM1 | idêntica |
| 20 — setor de atividade | PM6 | idêntica; residual unificado |
| 17 e 18 — por que não trabalha | MI1 | unificadas |
| 29 — situação comparada ao ingresso | AF2 | idêntica; muda de bloco |
| 30 — contribuição do curso | AF3 | idêntica; muda de bloco |
| 16 — tipo de curso em que está matriculado | EF1 e EF2 | reestruturada; a série parcial é "superior no IFSP" para técnicos matriculados |
| 4 e 5 — campus e tipo de curso | IDA3, IDA1 e IDA2 | de autodeclarados a pré-preenchidos; agregáveis |
| 1 — sexo | EQ1 | **não equivalente** |
| 27 e 28 — renda aberta | PM3 | sem série a preservar: o relatório não conseguiu apurar |

### 12.7 O que ficou de fora

Decidido com o orientando: os campos do instrumento documentado sem consumidor
ficam fora, pelo mesmo critério aplicado aos blocos.

| Questão ou candidato | Por que fica fora |
|---|---|
| 3 — escolaridade atual | EF1 pergunta diretamente o que os indicadores pedem |
| 6 — modalidade | sem consumidor; deriva do curso |
| 8 — setor anterior | sem consumidor; a comparação entre antes e agora usa o vínculo |
| 9 e 21 — porte da empresa | sem consumidor |
| 11 e 25 — benefícios | sem consumidor |
| 12 e 26 — horas semanais | sem consumidor |
| 13 e 14 — renda anterior | sem consumidor, e é dado sensível para o respondente |
| 19 — mesma empresa de antes | sem consumidor que AF2, AP1 e AP2 não atendam |
| 23 — tipo de atividade | sem consumidor; a área de atuação é o setor (PM6) |
| nome do curso em texto livre (versão no ar) | substituído pela lista fechada (IDA1) |
| localidade (documento do projeto) | sem consumidor |
| forma de ingresso por ação afirmativa | o indicador proposto é de percepção; avaliar resultados por condição de beneficiário exigiria o dado, que o sistema acadêmico tem — decisão da instituição |

A instituição pode reintroduzir qualquer um deles **declarando o indicador que ele
alimenta** — é a mesma porta que a ADR-0006 deixa aberta para os blocos.

### 12.8 Verificação do critério

**Trinta e cinco campos**: trinta e um padronizáveis, todos com domínio fechado; e
quatro não padronizáveis — os três de contato, validados por sintaxe, e o de
sugestões, com limite de tamanho e consumidor declarado. Todo campo tem consumidor,
e todo indicador do Anexo I, exceto o Ind1, se compõe dos campos (seção 12.4).
**Critério atendido.**

### 12.9 O que esta seção não permite afirmar

1. **A comparação é com o instrumento documentado de 2019 a 2023**, não com a versão
   no ar, que não foi percorrida.
2. **O texto das perguntas e os rótulos dos extremos das escalas não são daqui.**
3. **Os indicadores propostos pelo projeto continuam propostas** (ADR-0006).
4. **Nada foi implementado na plataforma.** Códigos e tipos são propostos; a E15
   confere.
5. **A média do Ind13 não é calculável com rigor por faixas.**

### 12.10 O que esta seção determina para as etapas seguintes

- **E14 (navegação)** — CON2 só se CON1 for "concordo"; recortes de equidade só se
  CON2 for "concordo"; AP2 só se AP1 for "sim"; SA2 só se SA1 incluir "trabalhando";
  Bloco V só com atividade remunerada, e Bloco VI no caso contrário; EF1 a EF3 só
  para técnico e graduação; EF2 e EF3 só se EF1 não for "não"; e toda regra que
  dependa de atributo usa o **valor confirmado** na identificação.
- **E15 (implementação)** — os 35 campos, com os códigos e tipos propostos; a lista
  de cursos com nível, a lista de unidades com as antecessoras e as faixas de
  rendimento como configuração versionada; as restrições do modo de ensaio também
  nos campos de contato.
- **E17 (importação)** — ativar a regra de coerência entre `curso` e `nivel` no
  arquivo de entrada; e a decisão de precedência na reimportação passa a cobrir os
  cinco atributos corrigidos, além do contato.
- **E18 (pré-preenchimento)** — cinco atributos, com o nível derivado do curso e o
  valor original preservado.
- **E22 (consentimento)** — CON1 e CON2, com os metadados de data, hora e versão.
- **E23 (conformidade)** — AF4, o texto livre, tratado antes de qualquer
  exportação; faixa de renda e recortes de equidade na anonimização; correções da
  identificação na trilha.
- **E25 (matriz)** — "pré-preenchimento" inclui a correção com preservação do
  original; "navegação condicional", as regras acima.
- **E26 (cenários)** — incluir quem trabalha sem remuneração, que segue para o Bloco
  VI, e a correção de nível que muda a exibição do Bloco IV.
- **E28 (extração)** — os indicadores pelas composições da seção 12.4; o Ind4 com
  "sim, totalmente" e a parcela "parcialmente" como sensibilidade; o Ind13 por
  faixas.
- **E30 (guia)** — a atualização das faixas de rendimento a cada ciclo, com versão.
- **E31 (relatório final)** — comunicar ao Comitê Permanente que o instrumento
  documentado não calcula a maior parte do Anexo I (seção 12.1) e as adaptações do
  Ind13 e do Ind4; declarar que a série de sexo e a de gênero não são equivalentes.
