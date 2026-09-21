# Parâmetros de contato automatizado

Especificação da cadência de disparo e das regras de contato do mecanismo de
acompanhamento de egressos: quantas mensagens, em que intervalos, até que limite,
sob que tratamento de recusa e de contato inválido, com que remetente e com que
verificação de entrega.

Produto da etapa E05. É insumo direto da E11 (leiaute de entrada), da E20
(convites e mensagens), da E21 (rotina agendada de lembretes), da E22
(consentimento), da E23 (recusa e trilha de auditoria) e da E25 (matriz de
verificação).

> **Nota de notação.** O [quadro de engajamento](../pesquisa/quadro-engajamento.md)
> identifica as estratégias como **E1** a **E11**, com um dígito. As etapas do
> projeto são **E01** a **E31**, com dois. Para evitar leitura ambígua, este
> documento sempre escreve "linha E*n* do quadro" ao se referir a estratégias.

## 1. Objeto e método

**Objeto.** Os sete parâmetros de contato automatizado enunciados no documento do
projeto, mais dois que a [E04](../pesquisa/quadro-engajamento.md) apontou como
necessários e que o documento não enuncia: a janela do ciclo e o tratamento do
canal alternativo previsto no art. 16, §1º do Regulamento.

**Método.** Derivação documental. Cada parâmetro recebe um valor, uma origem
declarada e uma justificativa. Nada aqui é medido, testado ou configurado: a
etapa produz especificação, e a verificação do comportamento real é da Fase 6.

**O que esta etapa não faz.** Não redige mensagem — a redação do convite e do
lembrete é da E20. Não configura rotina — a implementação é da E21. Não escolhe
recurso de plataforma: a instância ainda não existe, e afirmar aqui o que o
LimeSurvey faz nativamente seria asserção sem conferência. A seção 13 lista o que
a plataforma precisa suportar e remete a verificação às etapas próprias.

### 1.1 A advertência que condiciona a leitura de todo o documento

O documento do projeto apresenta os parâmetros de contato como "derivados das
experiências sistematizadas na revisão da literatura". **A E04 mostrou que três
deles não têm essa origem.** Nenhuma das dezessete fontes fichadas informa número
de lembretes, intervalo entre disparos ou limite de tentativas — o
[quadro de engajamento](../pesquisa/quadro-engajamento.md) registra isso
expressamente na seção 8, e a razão é estrutural: das onze estratégias
sistematizadas, uma tem efeito medido, cinco são relatadas sem separação e cinco
não foram avaliadas.

A consequência para esta etapa é de método, não de valor. **Os valores propostos
no documento do projeto são mantidos** — são compromisso registrado e não há
fundamento melhor disponível para substituí-los. O que muda é a atribuição de
origem: eles entram como **decisão de projeto declarada**, e não como derivação de
efeito medido. A seção 14 registra o ajuste de redação que o documento do projeto
deverá receber em sua próxima versão.

Esta distinção não é zelo formal. Um parâmetro apresentado como "derivado da
literatura" convida o leitor a supor que existe evidência de que três lembretes
rendem mais que dois, e essa evidência não existe. Declarar a origem correta é o
que permite, adiante, revisar o parâmetro sem contradizer a fundamentação.

### 1.2 Escala de origem do parâmetro

Análoga à escala de estado da evidência da E04, e com a mesma função: impedir que
as etapas seguintes atribuam a um parâmetro fundamento que ele não tem.

| Rótulo | Significado |
|---|---|
| **norma** | determinado por dispositivo expresso na norma vigente no IFSP; não é escolha do projeto |
| **quadro** | derivado de prática documentada na E04, com o estado da evidência daquela linha |
| **projeto** | decisão deste trabalho, sem fonte que a sustente; justificada por princípio, coerência interna ou restrição operacional |

Dos nove parâmetros, quatro têm dispositivo normativo na origem (P1, P2, P5, P9),
três derivam de linha do quadro (P1, P6, P8) e três são decisão de projeto sem
outra origem (P3, P4, P7). As somas não fecham em nove porque P1 tem dupla origem.
E há um dado mais relevante que a distribuição: **oito dos nove parâmetros têm
algum componente de decisão de projeto** — só P1 é integralmente determinado por
fora. Nenhum deriva de efeito medido sobre participação, porque não há efeito
medido no conjunto de fontes.

## 2. Quadro-resumo

| # | Parâmetro | Valor | Origem | Rastreio |
|---|---|---|---|---|
| **P1** | Convite inicial | Um envio por ciclo, com endereço individual de acesso | norma + quadro | Regulamento, art. 16, caput; quadro, linha E6 (única linha *medida*) |
| **P2** | Número de lembretes | Até três, dirigidos a quem não concluiu o preenchimento | norma (existência) + projeto (quantidade) | Regulamento, art. 16, §2º e art. 22; quantidade sem fonte |
| **P3** | Cadência | D+4, D+7 e D+14 do envio efetivo do convite, configuráveis dentro de faixa declarada | projeto | Documento do projeto; contraste da linha E9 do quadro |
| **P4** | Limite de tentativas | Quatro mensagens por participante por ciclo, incluído o convite | projeto | Decorrência de P1 e P2 |
| **P5** | Janela do ciclo e calendário | 60 dias corridos de validade do acesso; ciclos anuais ancorados na turma | norma (periodicidade) + projeto (janela) | Regulamento, arts. 14, 19 e 22; janela sem fonte |
| **P6** | Tratamento da recusa | Recusa de contato: permanente até revogação. Recusa de consentimento: encerra o ciclo corrente | quadro + projeto | Quadro, linha E2; a distinção entre as duas recusas é decisão nova |
| **P7** | Remetente e assunto | Endereço institucional identificável, com caixa de retorno monitorada; assunto padronizado e estável | projeto | Decorrência de P8; risco de leitura como fraude |
| **P8** | Verificação de entrega | Registro de retorno de erro, marcação do contato como inválido e fila de correção; sem rastreamento de abertura | quadro + projeto | Quadro, linha E1 (busca ativa reparadora); LGPD, art. 6º, III |
| **P9** | Canal alternativo | Endereço individual transportável; envio por mensagem instantânea fora do disparo automatizado | norma (exigência) + projeto (tratamento) | Regulamento, art. 16, §1º; restrição de custo zero |

## 3. P1 — Convite inicial

**Valor.** Um envio por ciclo e por participante, contendo **endereço individual
de acesso**, não reaproveitável entre participantes e não publicável.

**Origem.** Norma e quadro, convergentes.

- O art. 16, caput do Regulamento determina questionário acessível por "link
  disponibilizado para cada egresso". Não é opção de desenho: é o texto da norma.
- A linha E6 do quadro — convite individual sobre lista fechada — é a **única
  linha com efeito medido** de todo o conjunto: 28 respondentes sobre 79 egressos,
  35,4%, em [Coelho e Silva (2017)](../pesquisa/fichamentos/coelho-2017.md).

**Justificativa.** O endereço individual não é refinamento técnico: é a condição
de existência de todos os demais parâmetros. Sem ele não há lista de não
respondentes, e sem lista de não respondentes não há lembrete dirigido — é a
cadeia que a [linha de base](../pesquisa/linha-de-base.md) descreve na seção 6.3 e
que explica por que o art. 16 é hoje inexequível no IFSP.

**Ressalva obrigatória ao citar os 35,4%.** O número vem de um único programa de
mestrado, com população pequena e recente, e inclui o efeito da busca ativa
posterior, que a fonte não separa. Serve como ordem de grandeza e como prova de
que o cálculo é possível — **não como meta deste projeto**, que não fará aplicação
real e não produzirá taxa alguma.

**Incompatibilidade a registrar.** O endereço individual e o endereço divulgado em
canal aberto **não podem ser o mesmo**. Difundir uma URL única em campanha
institucional ou em grupo de turma devolve o instrumento ao modo aberto e anula o
denominador — é a advertência das seções 3.4 e 4.3 do quadro, e precisa constar do
guia de replicação (E30) porque é o tipo de detalhe que uma instituição desfaz sem
perceber.

## 4. P2 — Número de lembretes

**Valor.** Até três lembretes por ciclo, dirigidos **exclusivamente a quem não
concluiu o preenchimento**.

**Origem.** Mista, e convém separar as duas metades.

| Aspecto | Origem | Fundamento |
|---|---|---|
| Que existam lembretes repetidos | **norma** | art. 16, §2º — aplicação automatizada com disparos **repetidos** por sistema de mala direta; art. 22 — campanha com **envio de mensagens de lembrete** |
| Que sejam **três** | **projeto** | nenhuma fonte quantifica; valor do documento do projeto |

**Justificativa da quantidade.** Não há efeito medido a invocar. O que sustenta o
três é um argumento de limite, não de otimização:

1. A norma exige repetição e não a quantifica, de modo que qualquer número maior
   que um a satisfaz. O parâmetro é livre por omissão normativa, não por escolha
   entre alternativas avaliadas.
2. O teto é dado por princípio. Cada disparo adicional a quem já ignorou três é
   custo de incômodo sem retorno verificável; em população real, a insistência
   indefinida aproxima-se do constrangimento, que é o oposto do tratamento leal
   previsto na [LGPD](../pesquisa/fichamentos/brasil-lei-13709-2018.md).
3. O piso é dado pelo diagnóstico. A prática de referência na Rede Federal — a
   mala direta da linha E3 do quadro, no [Ifes](../pesquisa/fichamentos/ifes-2025.md)
   — não consegue enviar **nenhum** lembrete dirigido, porque não sabe quem não
   respondeu. Qualquer número maior que zero já é a diferença que o mecanismo
   introduz.

**Declaração expressa.** O número três é revisável. Não deriva de comparação entre
alternativas e não deve ser citado, no relatório final, como se derivasse. Havendo
aplicação real futura, é o primeiro parâmetro a ser reavaliado contra dados
próprios.

### 4.1 "Não concluiu" não é o mesmo que "não iniciou"

O critério de destinatário é **não conclusão**, não ausência de início. Quem abriu
o instrumento e parou no meio continua elegível a lembrete. São dois estados
distintos (seção 12) e a distinção tem duas consequências:

- **Para a E20.** A mensagem dirigida a quem já iniciou não pode ser a mesma
  dirigida a quem nunca abriu. Uma pede retomada; a outra, primeira resposta.
  Enviar "responda ao questionário" a quem respondeu metade é erro visível para o
  destinatário e corrói a credibilidade do restante da cobrança.
- **Para a E26.** O cenário de preenchimento parcial com retomada, já previsto na
  matriz do projeto, precisa verificar também que o participante em preenchimento
  **recebeu** lembrete, e não apenas que suas respostas foram preservadas.

## 5. P3 — Cadência dos disparos

**Valor.** Lembretes em **D+4**, **D+7** e **D+14**, em dias corridos, contados do
**envio efetivo do convite àquele participante**. Os três são parâmetros
configuráveis da rotina, dentro da faixa admissível declarada abaixo.

**Origem.** Projeto. Nenhuma fonte do conjunto informa intervalo entre disparos.

**Contagem por participante, não por data do ciclo.** A cadência é individual: D0
é o instante do envio a cada participante, e não uma data única de abertura do
ciclo. A distinção parece burocrática e não é — quem entra por reparo de contato
(P8) recebe o convite dias ou semanas depois dos demais, e uma cadência ancorada
em data fixa do ciclo lhe entregaria lembretes antes do convite, ou nenhum. É
requisito direto para a E21.

**O desenho, e o que ele assume.** Dois toques na primeira semana, enquanto o
convite ainda é recente e recuperável na caixa de entrada, e um terceiro mais
distante, para alcançar quem estava indisponível no período inicial.

*Observação de coerência interna, registrada sem alteração de valor.* Contados do
convite, os intervalos **entre disparos consecutivos** são de 4, 3 e 7 dias — o
segundo é mais curto que o primeiro. A progressão não é monotônica. Mantém-se o
valor do documento do projeto; registra-se a observação para que a revisão, se
houver, seja decisão consciente e não correção silenciosa.

### 5.1 Faixa admissível

Como P3 é configurável, a especificação precisa dizer o que é ajuste e o que é
descaracterização. Os limites abaixo são decisão de projeto, justificados por
princípio:

| Limite | Valor | Por quê |
|---|---|---|
| Primeiro lembrete não antes de | D+3 | abaixo disso o disparo alcança quem ainda não teve dia útil para responder, e lê-se como insistência |
| Primeiro lembrete não depois de | D+7 | acima disso o convite já saiu do campo de visão da caixa de entrada e o lembrete opera como novo convite |
| Intervalo mínimo entre disparos consecutivos | 3 dias | mesma razão do primeiro limite, aplicada a cada par |
| Último lembrete não depois de | D+21 | precisa restar folga dentro da janela de 60 dias (P5) para o ciclo de reparo de contato |

**Configuração fora da faixa** é admissível, mas deixa de ser ajuste operacional e
passa a exigir registro próprio — em ADR, se durante o projeto; no guia de
replicação (E30), se por instituição replicante.

### 5.2 O contraste que orienta a forma do parâmetro

A linha E9 do quadro — janela longa de coleta — documenta a alternativa: o Ifes
manteve o formulário aberto de 17/07 a 31/12/2024, cinco meses e meio. Não é
escolha de desenho; é o recurso disponível a quem não tem lista de não
respondentes. Sem saber a quem cobrar, resta esperar.

**Com cobrança dirigida, o parâmetro relevante deixa de ser a duração e passa a
ser a cadência.** É exatamente o que P3 fixa, e é uma das diferenças verificáveis
entre o mecanismo e a prática de referência — verificável no sentido de que a
seletividade do lembrete é item da matriz de verificação (E25), não no sentido de
produzir taxa de resposta, que este projeto não produzirá.

### 5.3 Parâmetro operacional complementar

O horário de execução da rotina não é um dos parâmetros do documento do projeto,
mas a cadência não se realiza sem ele. Especifica-se aqui o mínimo, deixando a
implementação à E21: **horário fixo e único, em dia útil**, registrado na
documentação da rotina. Disparo em massa noturno ou de fim de semana desloca a
mensagem para o fundo da caixa de entrada de segunda-feira, e disparo em horário
variável impede a verificação prevista na matriz ("disparo executado no horário
definido").

## 6. P4 — Limite de tentativas

**Valor.** **Quatro mensagens por participante e por ciclo**, incluído o convite
inicial. É teto, não meta: quem responde ao convite recebe uma só mensagem.

**Origem.** Projeto. Decorrência aritmética de P1 (um convite) e P2 (até três
lembretes); o valor consta do documento do projeto.

**O limite é por ciclo.** Cada ciclo anual reinicia a contagem. Não se fixa aqui
limite acumulado entre ciclos, por duas razões: a periodicidade anual é
determinação da norma (art. 14) e não comporta teto imposto pelo projeto; e os dois
estados que efetivamente interrompem a sequência — recusa de contato (P6) e
contato inválido (P8) — atuam por estado do participante, não por contagem.

### 6.1 O reconvite após reparo de contato

Questão que a aritmética simples não resolve: o participante cujo endereço
retornou erro, teve o contato corrigido e foi reconvidado dentro do mesmo ciclo —
as mensagens anteriores contam no limite?

**Decisão: não contam.** O reparo abre nova contagem dentro do mesmo ciclo, com
teto próprio de quatro mensagens.

**Justificativa.** O limite existe para conter incômodo ao destinatário. Mensagem
que retornou erro não foi entregue e não incomodou ninguém — contá-la puniria o
participante pela desatualização do cadastro institucional, que é exatamente o
problema que a busca ativa reparadora (linha E1 do quadro) existe para corrigir.

**Contenção.** No máximo **uma** rodada de reparo por participante e por ciclo. Se
o endereço corrigido também retornar erro, o participante permanece em "contato
inválido" até o ciclo seguinte. Sem esse teto, o par reparo–reconvite admite laço
sem término.

## 7. P5 — Janela do ciclo e calendário

### 7.1 Janela

**Valor.** O endereço individual de acesso é válido por **60 dias corridos**
contados do envio do convite àquele participante. Encerrada a janela, o acesso
expira e o participante passa ao estado `expirado` (seção 12).

**Origem.** Projeto. Nem a norma nem o quadro fixam duração de janela. A E04
registra expressamente que a E05 precisa fixar "a janela do ciclo e a cadência
dentro dela", e só a segunda tinha valor proposto.

**Justificativa.** Três medidas, nesta ordem:

1. **Folga após o último lembrete.** Com o último disparo em D+14, restam 46 dias
   de janela. Quem recebeu o terceiro lembrete e não respondeu de imediato ainda
   encontra o acesso válido semanas depois.
2. **Espaço para o ciclo de reparo.** Um retorno de erro detectado no convite
   precisa caber inteiro na janela: detecção, correção do contato, reconvite e
   cadência própria de até 21 dias. Com D+21 como teto do último lembrete (seção
   5.1), o reparo pode iniciar-se até cerca de D+39 e ainda completar o ciclo. Foi
   esta medida que fixou os 60 dias, e não a primeira.
3. **Distância do desenho que serve de contraste.** Os 60 dias são pouco mais de
   um terço dos cinco meses e meio do Ifes. A diferença é o ponto: janela longa é
   substituto de cobrança, e aqui há cobrança.

### 7.2 Calendário e ancoragem

O Regulamento fixa três gatilhos, que à primeira leitura parecem três rotinas
distintas:

| Dispositivo | Determinação |
|---|---|
| Art. 14 | pesquisas periódicas, **anuais** |
| Art. 19 | acompanhamento por turma ao término do **semestre de conclusão**, e **anualmente** depois |
| Art. 22 | nova campanha **dois anos após a formatura**, com envio de mensagens de lembrete |

**Decisão: ciclo ancorado na turma.** O D0 do primeiro ciclo de cada participante
é o término do seu semestre de conclusão (art. 19); os ciclos seguintes ocorrem a
cada doze meses a partir dele.

**Justificativa.** Uma única regra satisfaz os três dispositivos. O art. 19 fixa a
âncora, o art. 14 fixa o passo, e a campanha de dois anos do art. 22 **é** o
terceiro ciclo dessa mesma sequência — não acrescenta disparo, apenas nomeia um
ciclo que a regra já produz. A leitura evita que a E21 implemente três rotinas
sobrepostas e que um mesmo egresso receba três convites concorrentes no mesmo ano.

**Regra de não sobreposição.** Nenhum participante recebe convite de novo ciclo
enquanto houver ciclo aberto para ele, e nenhum recebe mais de um convite a cada
doze meses.

**Alternativa admissível, registrada.** Uma instituição replicante pode preferir
**data fixa única** para toda a base — um ciclo por ano, mesma janela para todos.
É operacionalmente mais simples e igualmente conforme aos arts. 14 e 16; perde a
aderência ao art. 19, que fala em turma. A escolha entre as duas ancoragens deve
constar do guia de replicação (E30) como ponto de configuração, não como
pressuposto.

**Nota para a simulação.** A ancoragem por turma exige, na base sintética da E16,
que o semestre de conclusão esteja presente e distribuído — a base prevista já
cobre dez anos de conclusão. A E26 poderá exercitar a regra em tempo comprimido,
desde que o registro do cenário declare a compressão.

## 8. P6 — Tratamento da recusa

O documento do projeto define "exclusão imediata de novos disparos e registro da
manifestação". A E04 deixou uma pergunta em aberto: se a recusa apenas encerra o
preenchimento ou se também interrompe disparos futuros.

**A resposta é que existem duas recusas, e o mecanismo precisa das duas.** A
distinção é decisão deste documento e não consta de nenhuma fonte.

| | **Recusa de consentimento** | **Recusa de contato** |
|---|---|---|
| O que o egresso manifesta | não concordo com o termo, neste ciclo | não quero mais ser contatado |
| Onde se manifesta | tela inicial de consentimento (E22) | tela inicial **e** via própria na mensagem (E20) |
| Efeito no ciclo corrente | encerra o preenchimento; nenhum lembrete adicional | encerra o preenchimento; nenhum lembrete adicional |
| Efeito nos ciclos seguintes | **nenhum** — o participante é convidado no ciclo seguinte | **permanente** — nenhum disparo, em nenhum ciclo |
| Reversão | não se aplica; basta consentir em ciclo posterior | via de revogação tão simples quanto a manifestação |

**Justificativa da distinção.** Tratar as duas como uma só erra em qualquer das
direções. Se toda não concordância com o termo bloqueasse permanentemente, uma
hesitação pontual — termo longo, momento ruim, dúvida sobre a finalidade —
excluiria o egresso do acompanhamento para sempre, e a instituição perderia
respondente que nunca pediu para sair. Se nenhuma bloqueasse, quem declarou não
querer contato receberia convite todo ano, e a manifestação de vontade seria
decorativa.

**Precedente parcial.** A linha E2 do quadro — aceite eletrônico em
[Coelho e Silva (2017)](../pesquisa/fichamentos/coelho-2017.md) — registra
"concordo" e "não concordo" e direciona ao questionário apenas quem concorda. É
precedente de **desenho de interação** para a recusa de consentimento; não trata de
disparos futuros, porque a coleta foi de rodada única. A recusa de contato não tem
precedente no conjunto de fontes.

**Silêncio não é recusa.** Não responder ao convite e aos três lembretes produz o
estado de não resposta, que é dado do acompanhamento — é ele que sustenta o
indicador de cobertura. Convertê-lo em recusa presumida destruiria o denominador,
que é justamente o que o mecanismo existe para construir.

**Registro da manifestação.** Toda recusa registra data, hora, ciclo, versão do
termo vigente e via de manifestação. O ônus da prova do consentimento é do
controlador (LGPD, art. 8º, §2º), e o mesmo vale, por simetria, para a prova de
que a recusa foi respeitada. É requisito da trilha de auditoria da E23.

**Revogação.** A via de revogação da recusa de contato deve ser tão simples quanto
a manifestação — analogia direta com a LGPD, art. 8º, §5º, que exige revogação do
consentimento por procedimento gratuito e facilitado. O mecanismo não pode admitir
saída em um clique e exigir processo administrativo para o retorno.

## 9. P7 — Remetente e assunto

**Valor.**

| Item | Especificação |
|---|---|
| Remetente | endereço institucional **identificável**, nominal ao programa de acompanhamento de egressos |
| Caixa de retorno | monitorada, capaz de receber e registrar devoluções e respostas humanas |
| `no-reply` | **vedado** |
| Assunto | padronizado, estável entre ciclos, com identificação explícita da instituição |

**Origem.** Projeto, por decorrência de P8.

**Justificativa.**

1. **Sem caixa de retorno não há P8.** A verificação de entrega depende de receber
   a devolução. Um remetente `no-reply` sem caixa monitorada torna o parâmetro de
   verificação de entrega inexequível — e "contato inválido" é item da matriz de
   verificação do projeto.
2. **Identificabilidade é contenção de risco, não cortesia.** A mensagem pede
   clique em endereço individual e único, que é a forma exata de uma fraude por
   mensagem eletrônica. Remetente reconhecível, assunto estável e domínio
   institucional são o que distingue o convite legítimo da fraude que o imita — e
   o destinatário, em aplicação real, não tem outro critério à mão.
3. **Estabilidade entre ciclos** é o que permite ao egresso reconhecer, no segundo
   ano, a mensagem que já recebeu no primeiro. Assunto variável a cada campanha
   desfaz esse reconhecimento a cada ciclo.

**O que a mensagem pode nomear.** A linha E5 do quadro — contrapartidas ao egresso
— é integralmente dependente de ação institucional e vai para a E24. O que cabe ao
mecanismo é modesto e verificável: **nomear, no convite, a contrapartida que a
instituição já oferece**. O IFSP anuncia três em portal — educação continuada,
integração acadêmica e colaboração voluntária. É decisão de redação da E20, e é o
limite do que este projeto faz nesse eixo.

### 9.1 Restrição de simulação — obrigatória

Este projeto **não** usa endereço institucional real como remetente nos testes.

- O remetente institucional identificável é **especificação para implantação
  real**, a constar do guia de replicação (E30).
- Nos ensaios das Fases 5 e 6, remetente e destinatários ficam **sob domínio
  controlado pelo projeto**, sem exceção.
- Usar um endereço `@ifsp.edu.br` como remetente de teste seria, além de violação
  da restrição do projeto, uso indevido de identidade institucional em mensagem
  automatizada.

A restrição é inviolável e não comporta exceção "só para um teste". A E09
configura o envio e a E20 aplica o remetente; ambas herdam esta regra.

## 10. P8 — Verificação de entrega e contato inválido

**Valor.** Registro do retorno de erro, classificação, marcação do contato como
inválido e entrada em fila de correção. **Sem rastreamento de abertura.**

**Origem.** Quadro (linha E1, busca ativa reparadora) e projeto.

### 10.1 Classificação do retorno

| Tipo | O que é | Tratamento |
|---|---|---|
| **Erro permanente** | endereço inexistente, domínio inválido, conta removida | marca o contato como inválido **na primeira ocorrência**; interrompe o disparo ao participante e abre fila de correção |
| **Erro temporário** | caixa cheia, indisponibilidade momentânea do servidor de destino | não marca; nova tentativa no disparo seguinte da cadência. Marca como inválido após **três** ocorrências no mesmo ciclo |
| **Sem retorno** | mensagem aceita pelo servidor de destino | segue a cadência normalmente |

O limiar de três ocorrências para erro temporário é decisão de projeto, sem fonte.
Justifica-se por simetria com P2: se a cadência prevê quatro mensagens, exigir as
três primeiras antes de declarar o contato perdido consome a sequência sem
desperdiçá-la.

### 10.2 Contato inválido não é recusa

Distinção com efeito prático relevante, e que a E04 já antecipava:

| | **Contato inválido** | **Recusa de contato** |
|---|---|---|
| O que significa | a instituição não sabe onde encontrar o egresso | o egresso não quer ser encontrado |
| Efeito no ciclo corrente | interrompe o disparo; abre fila de correção | interrompe o disparo |
| Efeito nos ciclos seguintes | **nenhum** — o participante volta ao fluxo normal se o contato for corrigido | permanente |
| Manifestação de vontade | **não há** | há |

Tratar contato inválido como recusa converteria falha de cadastro em manifestação
de vontade que ninguém expressou, e degradaria a base a cada ciclo: endereços
envelhecem, e uma base que nunca readmite quem teve endereço desatualizado tende,
no limite, à lista vazia. É a razão pela qual a E04 separou **busca ativa
reparadora** — corrige o cadastro e devolve o participante ao fluxo — de **contato
por canal alternativo** — entrega o convite por outra via sem corrigir a base. O
mecanismo precisa dos dois, e P8 trata do primeiro.

**Consequência para a E11.** A fila de correção só tem para onde recorrer se
houver **mais de uma via de contato** no leiaute de entrada. Um único endereço de
e-mail por participante torna o reparo impossível e o parâmetro, decorativo.

### 10.3 O que não se verifica: abertura

**Decisão: não implementar rastreamento de abertura** — nem pixel, nem
redirecionamento instrumentado, nem qualquer registro de leitura da mensagem.

**Justificativa.** Entrega e leitura são coisas diferentes, e só a primeira é
necessária. Nenhum dos dezenove indicadores do Anexo I do Regulamento —
reproduzidos no [Anexo A da linha de base](../pesquisa/linha-de-base.md) — depende
de saber se a mensagem foi aberta. Registrar abertura acrescentaria tratamento de
dado comportamental sem finalidade determinada, contra o princípio da necessidade
da LGPD (art. 6º, III); e a [linha de base](../pesquisa/linha-de-base.md) já mostra
que a conformidade do IFSP é declarada e não implementada — o mecanismo não
deveria ampliar a coleta no exato eixo em que a instituição ainda não fechou o
básico.

O dado de que o mecanismo precisa é **conclusão do preenchimento**, que ele obtém
diretamente, sem inferência e sem rastreamento.

### 10.4 Pré-requisito técnico

A verificação de entrega depende de caixa de retorno legível pela rotina. É
requisito da **E09** — configuração e verificação do envio de mensagens — e deve
ser conferido lá, não presumido aqui: uma configuração de SMTP que envie
corretamente e não permita ler devoluções satisfaz o critério de conclusão da E09
tal como hoje redigido e ainda assim inviabiliza P8. **A E09 precisa verificar as
duas direções.**

## 11. P9 — Canal alternativo

**A exigência.** O art. 16, §1º do Regulamento determina convite por e-mail e,
"não sendo possível", por aplicativos de mensagens instantâneas.

**Decisão: fora do disparo automatizado deste projeto.** Integração com serviço de
mensagens instantâneas exige, na prática corrente, contratação de interface paga —
o que colide com a restrição de custo zero — ou automação não oficial, que é
frágil e contrária aos termos de uso das plataformas.

**O que o mecanismo entrega em lugar disso.** O requisito técnico que torna o
canal alternativo possível sem integração: **o endereço individual é
transportável**. Pode ser extraído da base de participantes e entregue por
qualquer via, mantendo a individualidade do acesso e, portanto, a rastreabilidade.
O envio por essa via é ação humana, e não rotina.

**O que vai para outras etapas.**

- **E24** — recomendação de implantação: como operar o canal alternativo sem
  automação, e por quem.
- **E30** — a advertência, no guia de replicação: entregar por mensagem
  instantânea o **endereço individual de cada egresso** é compatível; difundir um
  **endereço comum** em grupo de turma anula a rastreabilidade e desfaz o
  mecanismo. A forma segura é o canal da turma avisar que o convite individual foi
  enviado.
- **E31** — registro de que a conformidade ao art. 16, §1º é **parcial e
  declarada**: o projeto entrega a condição técnica, não a automação do canal.

## 12. Estados do participante

Os parâmetros acima pressupõem uma máquina de estados. Ela é a especificação que a
E21 implementa e a E23 audita, e está aqui porque nenhum dos parâmetros é
verificável sem ela.

| Estado | Definição | Recebe lembrete? |
|---|---|---|
| `pendente` | na base, convite ainda não enviado no ciclo corrente | não |
| `convidado` | convite enviado, acesso não iniciado | **sim** |
| `em preenchimento` | acesso iniciado, preenchimento não concluído | **sim** — com mensagem própria (seção 4.1) |
| `respondente` | preenchimento concluído no ciclo corrente | não |
| `contato inválido` | retorno de erro conforme P8; aguarda correção | não — entra em fila de correção |
| `recusa de consentimento` | não concordou com o termo no ciclo corrente | não — volta a `pendente` no ciclo seguinte |
| `recusa de contato` | manifestou recusa permanente | **nunca**, em nenhum ciclo, até revogação |
| `expirado` | janela de 60 dias encerrada sem conclusão | não |

**Transições que merecem registro explícito:**

- `contato inválido` → `convidado`, pela fila de correção, uma vez por ciclo (6.1);
- `recusa de consentimento` → `pendente`, na virada do ciclo anual;
- `recusa de contato` → `pendente`, **somente** por revogação expressa do egresso;
- `convidado` e `em preenchimento` → `expirado`, ao fim da janela de 60 dias;
- qualquer estado → `recusa de contato`, a qualquer tempo.

**"Não respondente" não é estado próprio.** O termo, usado no documento do projeto
e na matriz de verificação, designa o conjunto de `convidado`, `em preenchimento` e
`expirado`. Registrar isso evita que a E21 implemente uma marcação redundante e que
a E25 redija requisito sobre um estado que não existe na base.

## 13. O que a plataforma precisa suportar

Lista de capacidades, **não** de recursos de produto. A instância ainda não existe
— a decisão de ambiente é a E06 e a instalação é a E08 —, e afirmar aqui o que o
LimeSurvey faz nativamente seria asserção sem conferência.

| # | Capacidade | Parâmetro que depende dela |
|---|---|---|
| C1 | endereço de acesso individual por participante, único e não adivinhável | P1 |
| C2 | estado de conclusão do preenchimento, por participante | P2, seção 12 |
| C3 | distinção entre acesso iniciado e não iniciado | P2 (seção 4.1) |
| C4 | contagem e data do último disparo, por participante | P3, P4 |
| C5 | disparo seletivo por estado, executável sem interação humana | P2, P3 |
| C6 | marcação persistente de recusa, respeitada entre ciclos | P6 |
| C7 | validade temporal do acesso, com início e fim | P5 |
| C8 | registro do estado de entrega do endereço | P8 |
| C9 | atributos por participante, para pré-preenchimento | E18 (fora desta etapa) |
| C10 | trilha de auditoria das operações sobre a base | P6, E23 |

### 13.1 Ponto de verificação que precisa constar da E21

Há uma forma de descompasso que vale antecipar. Rotinas nativas de lembrete de
plataformas de questionário tendem a expressar cadência como *intervalo mínimo
desde o último disparo* mais *número máximo de lembretes* — que não é o mesmo
modelo de P3, ancorado em D+*n* desde o convite.

Os dois modelos coincidem quando os intervalos são uniformes e divergem quando não
são, que é exatamente o caso de D+4, D+7, D+14. **A E21 precisa verificar qual
modelo a rotina disponível expressa** e, se for o primeiro, decidir entre traduzir
a cadência para intervalos uniformes — o que altera P3 dentro da faixa da seção
5.1 — ou implementar o agendamento fora da rotina nativa.

Registra-se como ponto de verificação, e não como diagnóstico: qualquer afirmação
sobre o comportamento da plataforma só pode ser feita depois da E08.

## 14. Ajuste devido ao documento do projeto

O documento do projeto afirma que os parâmetros de contato são "derivados das
experiências sistematizadas na revisão da literatura". **A E04 demonstrou que três
deles não são**, e esta etapa mantém os valores enquanto corrige a atribuição.

| Onde | Redação atual | Redação que a E04 e a E05 sustentam |
|---|---|---|
| Quadro de parâmetros de contato | "derivados das experiências sistematizadas na revisão da literatura" | parâmetros fixados como decisão de projeto, informados pela norma institucional e pelas práticas sistematizadas na revisão, com registro expresso de que número de lembretes, intervalo e limite de tentativas não derivam de efeito medido |
| Fase 5 | "definidos a partir do quadro comparativo produzido na Fase 1" | mesma correção; o quadro fornece o repertório e as restrições, não os valores |

**Não há alteração de valor, de escopo nem de cronograma.** O ajuste é de
fundamentação, e vale menos pelo documento do que pelo relatório final: um
parâmetro apresentado como derivado da literatura é atacável por uma pergunta
simples — *qual fonte?* — e a resposta honesta é que não há. Declarado como decisão
de projeto, com o limite do conhecimento disponível explicitado, o mesmo parâmetro
é defensável.

Fica registrado como pendência da **E31**, junto com as demais conferências de
referência.

## 15. O que este documento determina para as etapas seguintes

- **E09 (envio de mensagens)** — verificar as **duas direções**: envio e leitura de
  devoluções. Sem caixa de retorno legível, P8 é inexequível (10.4).
- **E11 (leiaute de entrada)** — **mais de uma via de contato**, sem o que a fila de
  correção de P8 não tem para onde recorrer; e o **semestre de conclusão**, que é a
  âncora do ciclo em P5.
- **E20 (mensagens)** — duas redações distintas de lembrete, para `convidado` e para
  `em preenchimento` (4.1); remetente e assunto conforme P7; via própria de
  manifestação de recusa de contato na própria mensagem (P6); possibilidade de
  nomear a contrapartida institucional existente.
- **E21 (rotina agendada)** — cadência contada **por participante**, não por data do
  ciclo (seção 5); horário fixo em dia útil (5.3); ancoragem por turma com regra de
  não sobreposição (7.2); e o ponto de verificação de 13.1, que pode obrigar a
  escolher entre traduzir P3 e implementar o agendamento fora da rotina nativa.
- **E22 (consentimento)** — a tela precisa oferecer **duas manifestações separadas**:
  não concordar com o termo neste ciclo e não querer mais ser contatado (P6). Uma
  única opção de recusa não atende à especificação.
- **E23 (conformidade)** — os dois estados que interrompem disparo são `recusa de
  contato` (permanente) e `contato inválido` (do ciclo corrente), com efeitos
  distintos (10.2); registro de data, hora, ciclo, versão do termo e via de
  manifestação; e via de revogação tão simples quanto a manifestação.
- **E25 (matriz de verificação)** — os requisitos "seletividade do lembrete",
  "tratamento da recusa" e "contato inválido" precisam ser redigidos contra a máquina
  de estados da seção 12, e não contra a noção genérica de "não respondente", que não
  é estado da base.
- **E26 (cenários)** — o cenário de preenchimento parcial deve verificar também o
  **recebimento de lembrete** pelo participante em preenchimento (4.1); o cenário de
  contato inválido deve exercitar o **ciclo de reparo** com o teto de uma rodada
  (6.1); e a compressão temporal usada para simular ciclos anuais deve ser declarada
  no registro do cenário.
- **E30 (guia de replicação)** — a escolha entre ancoragem por turma e data fixa
  única como ponto de configuração (7.2); a advertência sobre endereço comum (P1,
  P9); e o remetente institucional como especificação de implantação, distinta do
  remetente de teste (9.1).
- **E31 (relatório final)** — o ajuste de fundamentação da seção 14; o registro de
  que a conformidade ao art. 16, §1º é parcial e declarada (P9); e a formulação que
  vale para todo o trabalho: o mecanismo entrega **capacidade instalada de cobrança
  sistemática**, não elevação de taxa de resposta, que este projeto não tem como
  verificar.

## 16. O que esta especificação não permite afirmar

Registro explícito, na linha da seção 7 do quadro de engajamento.

1. **Não se pode afirmar que três lembretes rendem mais que dois, ou que D+4 rende
   mais que D+3.** Nenhuma fonte compara cadências. Os valores são decisão
   declarada, e a única coisa que se sustenta sobre eles é a coerência interna.
2. **Não se pode apresentar estes parâmetros como boa prática consolidada da área.**
   O que a E04 encontrou foi ausência de parâmetro publicado, não convergência em
   torno de um.
3. **A verificação da Fase 6 atesta que o mecanismo se comporta conforme esta
   especificação** — que o lembrete alcança só quem não concluiu, que a recusa
   interrompe o disparo, que o contato inválido é registrado. **Não atesta que a
   especificação é a melhor possível**, e a simulação não tem como produzir essa
   evidência.
4. **Nenhum número produzido sob estes parâmetros é resultado sobre egressos.** A
   base é sintética e os destinatários estão sob domínio controlado pelo projeto.
