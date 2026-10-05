# Rotina agendada de disparo

**Etapa:** E21 — configurar a rotina agendada de lembretes
**Data:** 05/10/2026
**Implementa:** P1 a P5 e a máquina de estados da seção 12 de
[`parametros-contato.md`](parametros-contato.md); responde ao ponto de verificação
da seção 13.1
**Decisão:** [ADR-0008](../decisoes/0008-agendamento-da-cadencia.md)
**Onde está:** [`scripts/cadencia.py`](../../scripts/cadencia.py) (regras) ·
[`scripts/disparar.py`](../../scripts/disparar.py) (disparo) ·
[`scripts/agendador.py`](../../scripts/agendador.py) (agendador) ·
[`infra/rotinas/configuracao/agenda.json`](../../infra/rotinas/configuracao/agenda.json)
(agenda) · [`infra/confere-rotina.py`](../../infra/confere-rotina.py) (conferência)
· procedimento em [`infra/README.md`](../../infra/README.md), seção "Rotina agendada"

## 1. O que esta etapa entrega

| Item | Valor |
|---|---|
| Rotina | agendador no contêiner `rotinas`, ativo, processo principal do contêiner |
| Disparo | 10:00, segunda a sexta, menos os feriados da agenda; tolerância de 30 min |
| Leitura de devoluções | a cada 30 min, todo dia, separada do disparo |
| Cadência | lembretes em D+4, D+7 e D+14 do envio efetivo do convite a cada participante, com pelo menos 3 dias entre dois envios; teto de 3 |
| Janela | `validuntil` = envio do convite + 60 dias, gravada pela rotina |
| Convite | na âncora da turma (término do semestre de conclusão, no calendário da agenda); nunca a menos de 12 meses do anterior; reconvite uma vez no ciclo depois do reparo |
| Guarda | conferências 1 a 7 da E19 e condições da E20, antes de cada disparo |
| Registro | `egressos_execucoes` (previsto, real, situação, inclusive `perdida`) e `egressos_disparos` (cada envio, sem token, nome nem endereço) |
| Modo no ensaio | **simulado** até a E26: roda no horário, confere, calcula e registra o plano, **não envia** — decisão do orientando |
| Hospedeiro | tarefa de logon do Windows que só liga a distribuição do WSL |

## 2. O ponto de verificação da seção 13.1

**O que a plataforma faz, conferido no código do LimeSurvey 7.2.** O lembrete
nativo — pelo painel e pela API — tem dois parâmetros: intervalo mínimo desde o
último envio (`minreminderdelay` no painel, `iMinDaysBetween` na API) e número
máximo de lembretes. É o primeiro modelo que a E05 previa. A plataforma não tem
agendador para isso: nenhum plugin assina o evento `cron`.

**Decisão:** a cadência fica **fora da rotina nativa**, e o P3 não muda. Traduzir
D+4/D+7/D+14 em intervalo uniforme seria a ferramenta decidindo o parâmetro, e não
resolveria o resto — a rotina nativa não sabe quem está em preenchimento nem grava o
ramo do lembrete. Justificativa completa na ADR-0008.

**Como a plataforma é usada, e as armadilhas que isso trouxe** (todas conferidas
no código):

| Achado | Consequência na rotina |
|---|---|
| `sent` e `remindersent` gravados em **UTC** (`gmdate`), `validuntil` lido no fuso do PHP (America/Sao_Paulo) | a cadência converte `sent` de UTC antes de contar os dias; a janela é gravada em hora local |
| cada chamada envia **no máximo 50** (`maxemails`) e ignora o resto da lista | lotes de até 50 (`lote` na agenda) |
| sem `continueOnError`, o lote **para na primeira falha** | sempre `continueOnError`, e o resultado é lido participante a participante |
| "N left to send" conta todos os candidatos do questionário, e não os da lista | não serve para saber se a lista acabou; não é usado |
| o envio pela API **não grava `date_invited`** da base central — só o painel o faz | a data do último convite vem do registro próprio (`egressos_disparos`) |
| `list_participants` recebe o **menor `tid`**, e não um deslocamento | a leitura pagina pelo último `tid` lido |
| o lembrete nativo filtra `emailstatus = 'OK'`, `completed = 'N'` e a lista de bloqueio da base central, mas **não** `blacklisted` do participante | o estado calculado exclui também o bloqueio do participante; a plataforma é a segunda camada, não a única |
| a janela (`validuntil`) é respeitada no envio: fora dela, falha com "Token not valid anymore" | segunda camada para o `expirado` |

## 3. O estado de cada participante

A rotina **calcula** o estado a cada execução; não grava estado. "Não respondente"
não é estado da base (seção 12 do P5), e nada novo foi marcado.

| Sinal | De onde vem |
|---|---|
| recusa de contato | base central (`lime_participants.blacklisted`), `emailstatus = 'OptOut'` ou `blacklisted` do participante, ou CON1 = `RCONT` em resposta enviada |
| resposta enviada | `submitdate` preenchido, e o estado sai de **CON1**: `CONC` é respondente, `RCONS` é recusa de consentimento (E14, E15) |
| contato inválido | `emailstatus` diferente de `OK` e de `OptOut` — o `invalido` que a rotina de devoluções grava (E09) |
| pendente | `sent = 'N'` |
| expirado | `validuntil` no passado; sem ele gravado, envio + 60 dias |
| em preenchimento | resposta **não** enviada com CON1 gravado |
| convidado | o resto |

A ordem acima é a precedência, e três escolhas nela merecem registro:

1. **A recusa de contato vence tudo**, inclusive resposta de outro ciclo.
2. **O estado da resposta sai de CON1, e não da marca de concluído.** A recusa sai
   marcada como concluída (E15). Participante marcado como concluído sem resposta
   enviada que o explique não é estado da máquina: é inconsistência, aparece como
   `concluído sem resposta` no plano e não recebe nada.
3. **Respondente com contato inválido continua respondente.** Concluir importa mais
   que o endereço ter devolvido depois.

### 3.1 `lastpage = 0`: abrir o endereço não é iniciar

A E20 achou que abrir o endereço já cria resposta parcial, com `lastpage = 0`, e
deixou a decisão para cá. **Decisão: quem só abriu continua `convidado`.**
"Iniciado" é ter enviado a página 1, isto é, ter CON1 gravado.

Medido nesta etapa, pelo caminho real, no 202615:

| O que o participante fez | O que fica na resposta | Estado |
|---|---|---|
| abriu o endereço | `lastpage = 0`, CON1 vazio, sem `submitdate` | `convidado` |
| enviou a página 1 concordando | `lastpage = 1`, CON1 = `CONC`, sem `submitdate` | `em preenchimento` |
| enviou a página 1 recusando | CON1 = `RCONS` ou `RCONT`, `submitdate` preenchido, participante concluído | recusa |

Por quê: coerente com a E08 — na plataforma, iniciar é submeter página — e com a
decisão da E05 de não rastrear abertura (seção 10.3). E o ramo de retomada do
lembrete fala de "continuar de onde parou" e de "carregar o questionário não
finalizado": dito a quem só abriu o endereço, seria texto errado.

**Caso de borda, registrado.** Se a página 1 for postada e não avançar — por
exemplo, CON2 obrigatório sem resposta —, fica CON1 gravado com `lastpage = 0`. Pela
regra, é `em preenchimento`: o egresso já manifestou o consentimento. Foi observado
nesta etapa, por script sem JavaScript.

## 4. O que vence

### 4.1 Convite

Um participante `pendente` recebe convite quando **todas** valem:

- a **âncora** já chegou: o término do semestre de conclusão no ano do ciclo,
  pelo calendário da agenda (`padrao`: 15/07 e 15/12, valores de ensaio; `excecoes`
  fixa um ano-semestre);
- concluiu no ano do ciclo ou antes;
- não houve convite a ele, em **outro** questionário ou ciclo, nos últimos 12
  meses (pelo registro próprio — ver a seção 2).

**Reconvite.** Quem volta a `pendente` depois de já convidado no ciclo é o reparo
de contato da P8: reconvite imediato, sem esperar âncora, e nova contagem de
lembretes (seção 6.1 do P4). **Uma vez por ciclo**: na segunda volta, nada, e o
plano registra "teto de reparo atingido". A operação de reparo em si — trocar o
endereço nos dois lugares — não é desta etapa (seção 10).

**A âncora móvel da ADR-0005** sai sozinha: a rotina relê ano e semestre a cada
execução, e o participante ainda não convidado passa a esperar a âncora nova. O
ciclo aberto não muda.

### 4.2 Lembretes

Para `convidado` e `em preenchimento`, com *k* lembretes já enviados (< 3):

- o lembrete *k*+1 vence em **D + `lembretes_dias[k]`**, contado da data local do
  envio do convite — e não do lembrete anterior nem de uma data do ciclo;
- e não antes de **3 dias** do lembrete anterior.

A rotina grava o ramo (`variante_lembrete`) **antes** de cada envio, participante
a participante; se a gravação falhar, aquele participante não recebe — sairia com o
texto de quem não iniciou (E20).

**Fim de semana e feriado.** A rotina só roda em dia útil, e a cadência é por
vencimento: um D+4 que cai no sábado sai na segunda. O intervalo mínimo impede que
o atraso de um lembrete encoste no seguinte. Exemplo conferido: convite na terça;
D+4 (sábado) sai na segunda; D+7 (terça) espera até quinta. O D+*n* é o **mínimo**,
não a data exata — e o último lembrete continua dentro de D+21 nos casos de fim de
semana. Com o hospedeiro desligado por dias, deixa de estar: a faixa da seção 5.1
limita a configuração, não garante o calendário de uma máquina parada.

### 4.3 Janela

Logo depois do convite, a rotina lê o `sent` que a plataforma gravou e grava
`validuntil` = `sent` + 60 dias, em hora local. Convidado sem janela gravada — por
exemplo, convidado pelo painel — ganha a janela na execução seguinte, a partir do
envio. A janela não é aplicada antes do convite: o endereço não é conhecido de
ninguém antes dele.

## 5. O agendador

- **Laço próprio**, processo principal do contêiner `rotinas`, acordando a cada
  20 s e relendo o relógio. Não dorme até o horário: um salto do relógio, que o WSL
  produz ao suspender, não o desorienta.
- **Reserva do horário:** antes de rodar, grava a execução com chave única
  (tarefa, horário previsto). Reiniciar o contêiner não repete o disparo do dia, e
  dois agendadores não disparam o mesmo horário.
- **Tolerância de 30 min:** a execução que começa até 30 min depois do horário vale.
  Depois disso, o horário vira registro **`perdida`**, e **não é executado fora da
  hora**. O que venceu sai no próximo dia útil, no horário (seção 4.2).
- **Subprocesso com limite de tempo** para cada tarefa: a falha de uma não derruba o
  agendador. Se o processo morre sem fechar a execução, o agendador a fecha como
  `falha`.
- **Ordem de subida.** Depois de um reinício, o Docker religa os contêineres sem a
  ordem da composição. O agendador insiste no banco, e o disparo insiste na
  plataforma até o fim da tolerância. Observado nesta etapa: o agendador subiu antes
  do banco, esperou e entrou.
- **Batimento:** um arquivo atualizado a cada passo alimenta a verificação de saúde
  do contêiner. Laço travado aparece como `unhealthy`, o que o processo vivo não
  revelaria.
- **Modo.** `ROTINA_DISPARO=simulado` é o padrão: roda no horário, confere a guarda,
  calcula e registra o plano, e não envia nem grava na plataforma. A leitura de
  devoluções, em simulado, lê sem consumir a caixa.

## 6. A guarda

Antes de cada disparo, e **sem disparo** se algo falhar (situação `bloqueada`):

- conferências 1 a 7 da E19 — a lógica passou para
  [`scripts/conferencia_participantes.py`](../../scripts/conferencia_participantes.py),
  e `infra/confere-participantes.py` virou a linha de comando sobre ela (conferido:
  mesmo resultado, 8 de 8). A 8 — grupos de e-mail compartilhado — fica de fora: pede
  revisão, mas não torna o disparo incorreto;
- questionário ativo e com acesso fechado por endereço individual;
- remetente e retorno do questionário iguais às caixas do `.env`, sob `.test`;
- atributo `variante_lembrete` descrito, com coluna, e o lembrete escolhendo o
  ramo por ele.

A identidade textual dos modelos com os versionados não entra na guarda: o
contêiner não alcança `infra/instrumento/mensagens.py`, e essa conferência continua
com `infra/confere-mensagens.py`, no hospedeiro.

## 7. Registro próprio

| Tabela | Uma linha por | Campos |
|---|---|---|
| `egressos_execucoes` | execução de tarefa | tarefa, modo, origem (agendada, manual), questionário, ciclo, horário previsto, início, fim, situação (`simulada`, `concluida`, `concluida_com_falhas`, `bloqueada`, `falha`, `perdida`), resumo em JSON |
| `egressos_disparos` | envio tentado | execução, questionário, ciclo, `tid`, `participant_id`, convite ou lembrete, número, motivo, ramo, estado de partida, resultado, erro |

Nenhuma guarda token, nome ou endereço. São insumo da trilha de auditoria (E23), ao
lado de `egressos_devolucoes` (E09) e `egressos_importacoes` (E17). O resumo da
leitura de devoluções guarda só as contagens; os endereços devolvidos ficam na
tabela da E09.

## 8. O hospedeiro

A E21 encontrou a distribuição do WSL **parada** depois de um reinício do Windows.
O `instanceIdleTimeout = -1` (E07) impede que ela morra ociosa, mas não a liga.
Parada, a rotina não roda — a falha silenciosa que a E07 temia.

**Tratamento, com autorização do orientando:** tarefa de logon do Windows,
registrada por
[`infra/hospedeiro/liga-wsl-ao-entrar.ps1`](../../infra/hospedeiro/liga-wsl-ao-entrar.ps1),
que só executa `wsl -d Ubuntu-24.04 --exec /bin/true`. O agendamento continua na
composição.

**Conferido:** distribuição encerrada, tarefa disparada, e 90 s depois, sem sessão
aberta, distribuição de pé e quatro contêineres saudáveis.
**Não conferido:** o logon depois de um reinício de fato.
**Não coberto:** suspensão e hibernação. Com o hospedeiro suspenso no horário, a
execução é registrada como `perdida` quando a rotina volta.

## 9. Verificação do critério de conclusão

*Critério: o disparo executar no horário e atingir só os não respondentes.*

**Atendido.** Três frentes, todas por execução.

### 9.1 A rotina ativa, no horário de operação

A primeira execução agendada do ciclo corrente foi a das **10:00 de 05/10/2026**:
prevista para 10:00:00, começou às **10:00:08**, em modo simulado. Guarda conferida;
500 participantes, todos `pendente`; plano de 255 convites — os de conclusão no 1º
semestre, cuja âncora (15/07) já passou — e 245 antes da âncora (15/12). Nada
enviado, nada gravado na plataforma. A leitura de devoluções rodou separada, às
10:00:08, sem consumir a caixa.

### 9.2 O disparo real, no horário, pelo agendador

`python3 confere-rotina.py --agendada`, **14 de 14**. Catorze participantes do
202615 plantados, um por situação; o agendador recriado em modo real, num ciclo de
teste (2099, âncora de todos no futuro), com horário às 10:06. Os outros 486 são o
controle negativo.

| # | Conferência | Resultado |
|---|---|---|
| 1–7 | regras da cadência, sem plataforma (seção 9.3) | ok |
| 8 | a rotina ativa rodou no horário em simulado e nada enviou | 10:00:00 previsto, 10:00:08 real |
| 9 | as situações plantadas pelo caminho real saem como a plataforma as produz | abrir: `lastpage 0`, CON1 vazio; página 1: `lastpage 1`, `CONC`; recusas: enviadas e concluídas |
| 10 | **o disparo executou no horário** | previsto 10:06:00, começou 10:06:11, `concluida` |
| 11 | **lembretes só para não respondentes, com o ramo certo** | ver a tabela abaixo |
| 12 | contador e ramo só de quem recebeu; janela de 60 dias de cada convidado | 486 não plantados intactos; janela gravada nos 8 convidados |
| 13 | as mensagens chegaram, uma por destinatário, e nenhuma a mais | 5 novas na caixa: 4 lembretes e 1 convite |
| 14 | limpeza | 500 participantes como antes; nenhuma resposta, envio registrado ou recusa; agendador de volta a simulado · 2026 |

| Plantado | Estado calculado | Esperado | Recebeu |
|---|---|---|---|
| A — convite há 4 dias | convidado | lembrete 1, ramo de primeira resposta | **lembrete 1, convidado** |
| B — abriu o endereço sem enviar página, convite há 4 dias | convidado | lembrete 1, ramo de primeira resposta | **lembrete 1, convidado** |
| C — enviou a página 1, convite há 7 dias, lembrete 1 há 3 | em preenchimento | lembrete 2, ramo de retomada | **lembrete 2, em_preenchimento** — o texto ensina a carregar o salvo |
| D — convite há 14 dias, lembrete 2 há 7 | convidado | lembrete 3 | **lembrete 3, convidado** |
| E — convite há 2 dias | convidado | nada: D+4 não venceu | nada |
| F — convite há 8 dias, lembrete 1 ontem | convidado | nada: intervalo mínimo | nada |
| G — três lembretes já enviados | convidado | nada: teto | nada |
| H — concluiu | respondente | nada | nada |
| I — recusou o termo | recusa de consentimento | nada | nada |
| J — recusou contato em CON1 | recusa de contato | nada | nada |
| K — contato inválido | contato inválido | nada | nada |
| L — janela encerrada | expirado | nada | nada |
| M — voltou a pendente após um convite no ciclo | pendente | reconvite, janela nova | **convite, reconvite**; `validuntil` = envio + 60 dias |
| N — voltou a pendente pela segunda vez | pendente | nada: teto de reparo | nada |
| os outros 486 | pendente | nada: âncora no futuro | nada |

**A primeira execução desta conferência falhou na limpeza, e fica registrado.** O
disparo e as conferências de 10 a 13 passaram. Depois, o servidor IMAP recusou
login por alguns segundos: às 10:02:37 o relógio da máquina virtual do WSL **voltou
7,3 s**, sem suspensão nenhuma, e o Dovecot, como na E09, não lança serviço durante
o intervalo. O auxiliar de caixa da E20 acusa a falha com `SystemExit`, que a
limpeza não capturava, e os passos seguintes não rodaram: participantes e respostas
já tinham sido restaurados, mas ficaram uma mensagem de teste na caixa e o registro
do ciclo 2099. Tudo foi desfeito à mão e conferido. A conferência passou a insistir
na caixa, a capturar também `SystemExit` em cada passo de limpeza e a mostrar o log
do agendador de teste antes de recriar o contêiner, que apaga o log anterior. A
segunda execução passou inteira.

### 9.3 As regras, e a conferência delas

`python3 confere-rotina.py`, **7 de 7**, sem plataforma: 16 casos de estado, 19 de
vencimento, o fim de semana, a janela, dia útil e feriado, a faixa da agenda (9
configurações recusadas, 1 aceita com registro) e os ramos iguais aos da E20.

**Testada por mutação**, como as conferências da E16 e da E19: 16 defeitos
plausíveis plantados na cadência, **16 reprovados**. Um deles passou na primeira
rodada e mostrou dois furos da conferência, corrigidos: ler `sent` como hora local,
e não UTC, não mudava o resultado porque todos os casos tinham convite às 10h, quando
3 horas não mudam o dia; e a janela esperada era calculada pela própria função
conferida, o que é circular. Entrou um convite às 22h locais — já o dia seguinte em
UTC — e a janela passou a ser calculada à parte.

### 9.4 A execução perdida

`python3 confere-rotina.py --perdida`, **8 de 8**: o agendador, subido com o horário
de hoje já vencido além da tolerância (09:33, tolerância de 30 min), registrou a
execução como `perdida`, acusou no log e **não** a executou fora da hora.

### 9.5 O relógio, achado desta etapa

O relógio da máquina virtual do WSL, que os contêineres usam, foi medido **7,3 s
atrás** do relógio do Windows (três medidas, ida e volta de 70 ms), e é corrigido aos
saltos: o correio registrou um salto de 7,3 s para trás, e o log do agendador de
teste mostra outro, de 8 s, entre duas linhas consecutivas. É a raiz da E07, da E09
e da E10, agora sem suspensão. Para a rotina, no grão de minuto, é irrelevante: a
reserva é por horário previsto, e o laço relê o relógio a cada passo. Para a
conferência, um início registrado poucos segundos antes do horário é o relógio sendo
corrigido, e ela tolera até 30 s.

## 10. O que fica fora desta etapa

- **A operação de reparo de contato** — trocar o endereço inválido pelo
  alternativo no participante e na base central, esta só por console no
  hospedeiro. A rotina **respeita** o reparo (reconvite uma vez, nova contagem); a
  operação é da E26, onde o cenário a exige — decisão do orientando.
- **A virada de ciclo** — criar o questionário do ano seguinte. A rotina opera
  sobre o questionário configurado; o procedimento é da E30.
- **O efeito do bloqueio global** em disparos futuros: a rotina o lê e o respeita,
  mas exercitar a recusa pelo endereço de recusa é da E22.

## 11. O que esta etapa não permite afirmar

1. **Nada sobre taxa de resposta.** A rotina entrega a capacidade instalada de
   cobrança sistemática; se três lembretes em D+4, D+7 e D+14 rendem mais respostas,
   não há como saber sem aplicação real.
2. **A cadência real ainda não correu dias de calendário.** A verificação comprimiu
   o tempo pondo as datas de envio no passado, pela API — declarado, na linha da
   seção 7.2 do P5. A rotina viu cada situação **num** disparo; a sequência de três
   lembretes ao mesmo participante, em dias diferentes, é cenário da E26.
3. **O respondente foi plantado pela API.** A abertura, a página 1 e as duas
   recusas foram pelo caminho real; a conclusão completa, pelas onze páginas, é da
   E26.
4. **Um reinício do Windows não foi feito.** A tarefa de logon foi exercitada
   disparando-a à mão sobre a distribuição encerrada.
5. **A regra dos doze meses entre ciclos** foi conferida só pelas regras: o ensaio
   tem um questionário só.

## 12. O que determina para as etapas seguintes

- **E22** — exercitar a recusa pelo endereço de recusa e conferir que a rotina a
  lê da base central; CON1 = `RCONT` já é lido como recusa de contato.
- **E23** — `egressos_execucoes` e `egressos_disparos` são trilha; **respostas
  anônimas quebram o estado**: sem o token na resposta, a rotina não distingue
  `convidado` de `em preenchimento` nem vê a conclusão. Se a anonimização tocar a
  tabela de respostas, precisa preservar esse vínculo ou substituí-lo. E as datas
  da resposta estão em UTC.
- **E25** — "seletividade do lembrete" e "disparo no horário" têm procedimento
  pronto: `confere-rotina.py --agendada`; a execução perdida, `--perdida`.
- **E26** — ligar o modo real (`ROTINA_DISPARO=real`), sabendo que a primeira
  execução convida todos cuja âncora já passou (255 de 500 em 05/10/2026);
  implementar a operação de reparo nos dois lugares; correr a cadência em dias de
  calendário ou declarar a compressão.
- **E28** — as datas da resposta (`startdate`, `submitdate`) estão em **UTC**; o
  registro próprio dá, por participante, quantas mensagens recebeu e quando.
- **E30** — Parte V do guia a partir de `infra/README.md`; a tarefa de logon no
  Windows; trocar feriados e calendário pelos da instituição; a advertência de que
  disparo pelo painel não grava o ramo nem entra no registro.
- **E31** — a conformidade ao "horário fixo" depende do hospedeiro ligado, e a
  rotina o declara em vez de presumir.
