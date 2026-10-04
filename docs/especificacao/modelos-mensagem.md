# Modelos de mensagem

**Etapa:** E20 — configurar convites e modelos de mensagem
**Data:** 04/10/2026
**Implementa:** P7 (remetente e assunto), a via de recusa de contato do P6 e a
seção 4.1 do P2 de [`parametros-contato.md`](parametros-contato.md)
**Onde está:** [`infra/instrumento/mensagens.py`](../../infra/instrumento/mensagens.py)
· subcomando `aplicar-mensagens` de `instrumento.py` ·
[`infra/confere-mensagens.py`](../../infra/confere-mensagens.py)

## 1. O que esta etapa entrega

| Item | Valor de ensaio |
|---|---|
| Remetente | `Acompanhamento de Egressos do IFSP (ensaio) <acompanhamento@egressos.test>` |
| Retorno (Return-Path) | `devolucoes@egressos.test`, lido pela rotina da E09 |
| Resposta humana | chega à caixa `acompanhamento`, separada das entregues e das devoluções |
| Assunto do convite | `IFSP — Acompanhamento de Egressos: convite para o questionário anual` |
| Assunto do lembrete | `IFSP — Acompanhamento de Egressos: lembrete do questionário anual` |
| Formato | HTML, com alternativa em texto gerada pela plataforma |

Os textos estão em `mensagens.py`, que é a fonte única: o gerador do `.lss` os
inclui, o `aplicar-mensagens` os grava no instrumento ativo e a conferência compara
a instância com o arquivo. O `instrumento.lss` versionado foi reexportado com eles.

**Redação.** O texto é operacional: convite, acesso, retomada e recusa. Não toca o
conteúdo temático das perguntas, que vem do projeto correlato (CLAUDE.md, decisão 5).

## 2. Remetente: por que não `naoresponda`

A E09 configurou o remetente de ensaio como `naoresponda@egressos.test`. **Isso
contrariava o P7**, que veda `no-reply` e exige caixa de retorno monitorada para
devoluções **e respostas humanas**. No correio de ensaio, uma resposta a
`naoresponda@` caía na caixa `entregues`, junto das mensagens entregues, onde
ninguém a veria.

**Decisão** (confirmada com o orientando antes da execução): o remetente de ensaio
passa a ser `acompanhamento@egressos.test`, que é nominal ao programa, e ganha
caixa própria no correio (`CORREIO_CAIXA_REMETENTE`). A regra da seção 9.1 continua
valendo: tudo sob `.test`, e o remetente institucional fica como especificação de
implantação real (E30). O que mudou foi só o nome do endereço de ensaio.

**O remetente é do questionário, e não do sítio.** O LimeMailer dá precedência ao
`adminemail` e ao `bounce_email` do questionário sobre o `siteadminemail` e o
`siteadminbounce` da configuração (conferido no código, em `setSurvey`). Por isso o
remetente vai no `.lss`, junto do instrumento, e não depende do `config.php`, que
só é escrito na primeira criação do volume. O padrão do compose também foi
atualizado, mas numa instalação existente ele não muda nada. É o remetente das
mensagens de sistema, e não das mensagens aos egressos.

## 3. Conteúdo exigido, e onde está

| Exigência | Origem | No modelo |
|---|---|---|
| saudação neutra com o nome inteiro | E11 | `Olá, {FIRSTNAME}.`; `firstname` é o `nome` do leiaute, já social quando houver registro, e `lastname` fica vazio |
| endereço individual, que não deve ser repassado | P1, P9 | `{SURVEYURL}` com aviso de que é individual |
| identificação pré-preenchida, para confirmar ou corrigir | E18 | parágrafo próprio, no convite e no lembrete |
| salvar e retomar | E14 | convite cita “Retomar mais tarde”, rótulo conferido na tradução pt-BR da instância |
| contrapartida institucional existente | P7; quadro, linha E5 | as três que o IFSP anuncia: educação continuada, integração acadêmica e colaboração voluntária |
| via própria de recusa de contato | P6 | `{GLOBALOPTOUTURL}`, ver seção 4 |
| sem rastreamento de abertura | P8, 10.3 | nenhuma imagem, nenhum redirecionamento instrumentado |
| assunto estável, com a instituição | P7 | sem ano e sem número do lembrete |

## 4. Recusa de contato: `GLOBALOPTOUTURL`, e não `OPTOUTURL`

A plataforma oferece dois endereços de recusa (conferido no `LimeMailer` e no
`OptoutController`):

- `{OPTOUTURL}` marca `OptOut` **só neste questionário**;
- `{GLOBALOPTOUTURL}` põe o participante na **lista de bloqueio da base central**,
  que vale para todos os questionários.

A recusa de contato do P6 é permanente e vale para todos os ciclos. Por isso o
modelo usa a segunda. Abrir o endereço **não** registra a recusa: a página pede
confirmação, e a recusa só acontece por POST. A conferência abre a página e não
confirma.

**Não verificado aqui, e é da E22 e da E23:** que o bloqueio na base central de fato
impeça convites e lembretes futuros. Isso depende de configuração global da lista
de bloqueio. Também fica para lá a via de revogação, que o modelo hoje indica como
"responder a esta mensagem".

## 5. O lembrete com dois ramos

A seção 4.1 do P2 exige redações distintas para `convidado` (pedido de primeira
resposta) e `em preenchimento` (instrução de retomada). O LimeSurvey tem **um único**
modelo de lembrete.

**Como foi resolvido:** o corpo da mensagem passa pelo Expression Manager antes do
envio (conferido: `LimeMailer::doReplacements` chama `ProcessString`). O lembrete
tem um `{if(...)}` sobre o atributo `variante_lembrete` do participante
(`attribute_7`):

- `em_preenchimento` → retomada: abrir o endereço, usar “Carregar questionário não
  finalizado” com o nome e a senha escolhidos; abrir sem carregar **começa outro
  preenchimento** (E15); sem senha, recomeça do início (E14);
- qualquer outro valor, inclusive vazio → pedido de primeira resposta.

**Decisão** (confirmada com o orientando): atributo gravado pela rotina, e não
substituição feita por comando próprio de envio. Assim o `remind_participants`
nativo continua servindo, com os contadores `remindercount` e `remindersent`. O
atributo **não é estado**: é parâmetro do disparo, sobrescrito a cada lembrete. O
estado continua derivado da conclusão e de CON1 (seção 12 do P5; E14). Isso não
contraria a vedação de "marcação redundante": nada é lido dele para decidir quem
recebe.

**Consequência para a E21:** a rotina **tem de gravar o atributo antes de cada
lembrete**. Um lembrete disparado pelo painel, sem essa gravação, sai com o ramo de
quem não iniciou, e quem está em preenchimento recebe o texto errado.

### 5.1 Acrescentar coluna a instrumento ativo

O instrumento já estava ativo, com 500 participantes. O `activate_tokens` da API não
acrescenta coluna a tabela existente (E17). Por isso foi criado o comando de console
`completaratributos`, que faz o mesmo que o painel: `ALTER TABLE` com coluna `text`,
sem tocar participantes. Num ambiente do zero, a coluna já nasce na preparação, pela
lista `ATRIBUTOS_QUESTIONARIO`.

**Armadilha encontrada e tratada.** Depois do `ALTER`, a API continuou recusando
gravar na coluna nova (`Property "Token_202615.attribute_7" is not defined`). A web
guarda o esquema das tabelas em cache de arquivo por uma hora, e o cache do console
não alcança esse arquivo: no console o componente é `CDummyCache` e o `flush()` dele
não faz nada (observado). O comando esvazia o `CFileCache` da web pelo caminho do
diretório de runtime. Isso é inofensivo, porque é cache, e é feito sempre, para que
uma execução interrompida depois do `ALTER` se resolva rodando de novo.

## 6. O convite de teste

`python3 confere-mensagens.py --enviar` faz o caminho real com **um** participante
sintético do 202615, sob `egressos.test`, ainda sem envio, e desfaz tudo ao fim.
Foi a decisão confirmada com o orientando: no próprio instrumento, com limpeza,
como na E18.

**Resultado: 9 de 9.**

| # | Conferência | Evidência |
|---|---|---|
| 1 | remetente e retorno | os de `mensagens.py`, iguais às caixas do `.env`; nenhum `no-reply`; tudo sob `.test` |
| 2 | modelos da instância = versionados | os quatro campos idênticos |
| 3 | elementos exigidos | nome, endereço individual, recusa de contato, sem imagem nem marcador desconhecido |
| 4 | atributo do ramo | `attribute_7` descrito como `variante_lembrete`, com coluna |
| 5 | convite chega formatado | From, Return-Path e assunto certos; HTML com alternativa em texto; nome inteiro com acentos; nenhum marcador por resolver |
| 6 | endereços da mensagem | o de acesso é o do participante e abre o termo (CON1); o de recusa é o da lista de bloqueio e abre a confirmação, que não é confirmada |
| 7 | lembrete, um por ramo | `convidado` pede resposta e não fala de retomada; `em_preenchimento` ensina a retomar e não pede primeira resposta |
| 8 | resposta humana | chega à caixa `acompanhamento`, e não às entregues |
| 9 | limpeza | participante restaurado, mensagens apagadas, nenhuma resposta, nenhuma recusa |

A mensagem também foi lida renderizada (`--guardar` grava os `.eml` fora do
repositório). Estado final do 202615: 500 participantes, nenhum envio, nenhum
lembrete, nenhuma resposta, nenhum bloqueio, nenhuma falha de envio.

**A primeira execução falhou, e a falha está registrada** porque mostrou duas
coisas. A conferência 6 errou na leitura do `&amp;` do link, que era defeito da
conferência, e não do modelo. A gravação do atributo esbarrou no cache de esquema
(seção 5.1). A interrupção deixou o participante com `sent` preenchido e uma
resposta parcial, e as duas coisas foram desfeitas à mão. Depois disso, a limpeza
passou a executar cada passo de forma independente, para que uma falha num deles
não impeça os outros.

## 7. Achado: abrir o endereço já cria resposta

Abrir o endereço individual, **sem responder nada**, cria uma resposta parcial
(`lastpage = 0`, sem `submitdate`). Isso foi observado na conferência 6, e a limpeza
apaga essa resposta. A consequência vai para a E21: pela tabela de respostas, quem
apenas abriu o link já aparece como `em preenchimento`. A rotina precisa decidir se
`lastpage = 0` conta como acesso iniciado (C3) ou como `convidado`. O texto de
retomada cobre os dois casos: "se você não salvou… basta responder novamente". A
escolha, porém, muda qual ramo a pessoa recebe.

## 8. O que esta etapa não permite afirmar

1. **Nada sobre eficácia da redação.** O texto segue a especificação. Se ele
   rende mais respostas, não há como saber sem aplicação real.
2. **Não se verificou o efeito da recusa.** Só que o link existe, é do participante
   e abre a confirmação (seção 4).
3. **O endereço nas mensagens é o do hospedeiro de ensaio** (`127.0.0.1:8080`),
   porque a plataforma monta a URL a partir do host da requisição. Em implantação
   real, a URL pública precisa estar configurada. É item do guia (E30).
4. **A janela de 60 dias não está na mensagem.** O texto não promete prazo, porque
   `validfrom` e `validuntil` são da E21.

## 9. O que determina para as etapas seguintes

- **E21:** gravar `variante_lembrete` antes de cada lembrete (seção 5); decidir o
  tratamento de `lastpage = 0` (seção 7); disparar pelo `remind_participants` com
  lista explícita de participantes. Com `iMinDaysBetween` nulo ele não filtra por
  intervalo, e a cadência D+*n* fica com a rotina.
- **E22 e E23:** confirmar que a lista de bloqueio da base central impede disparos
  futuros; definir a via de revogação, que hoje o texto indica como resposta à
  mensagem; e registrar a recusa na trilha.
- **E26:** o cenário de preenchimento parcial pode usar `confere-mensagens.py` como
  ponto de partida do recebimento do lembrete de retomada.
- **E30:** remetente institucional, caixa de retorno monitorada por pessoa, URL
  pública da instância e o aviso de que lembrete disparado pelo painel sai sem a
  gravação do ramo.
