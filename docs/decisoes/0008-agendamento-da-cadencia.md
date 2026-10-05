# ADR-0008 — Agendamento da cadência dentro da composição

**Status:** aceita
**Data:** 05/10/2026
**Etapa de origem:** E21 — configurar a rotina agendada de lembretes

## Contexto

A E21 precisa fazer a cobrança acontecer sozinha: convite na âncora da turma,
lembretes em D+4, D+7 e D+14 contados do envio a cada participante, janela de 60
dias, leitura de devoluções — tudo sem ninguém ao teclado. Duas perguntas ficaram
abertas pelas etapas anteriores, e esta decisão responde às duas.

**A primeira é a da seção 13.1 da E05:** a rotina nativa da plataforma expressa a
cadência do mesmo modo que o P3? Conferido no código do LimeSurvey 7, a resposta
é não. O lembrete nativo — pelo painel e pela API (`remind_participants`) — tem
dois parâmetros: **intervalo mínimo desde o último envio** e **número máximo de
lembretes**. É o primeiro modelo que a E05 previa. Ele só coincide com D+*n* desde o
convite quando os intervalos são uniformes, e 4, 3 e 7 dias não são. E a
plataforma não tem agendador: nenhum plugin assina o evento `cron`, e o comando
de console correspondente só repassa o evento a plugins.

A conferência do código achou mais quatro coisas que pesam na decisão:

- toda data da plataforma está em **UTC** — `sent` e `remindersent` (`gmdate`),
  `validuntil` e as datas da resposta —, porque o LimeSurvey fixa o fuso do PHP em
  UTC na própria configuração. *Corrigido na E22:* a primeira redação dizia que
  `validuntil` era lido no fuso do PHP da imagem, America/Sao_Paulo, e a rotina o
  gravava em hora local ([`rotina-disparo.md`](../especificacao/rotina-disparo.md),
  seção 4.3);
- cada chamada envia **no máximo 50** (`maxemails`) e ignora o resto da lista;
- sem `continueOnError`, o lote **para na primeira falha**;
- o envio pela API **não grava `date_invited`** na base central. Só o painel o faz.
  A regra de "nenhum convite a menos de doze meses do anterior" (P5, 7.2) não pode
  se apoiar nesse campo.

**A segunda é a do registro da E07:** onde o agendador vive. O WSL encerrava a
distribuição ociosa, e com ela os contêineres; o ajuste `instanceIdleTimeout = -1`
tratou a ociosidade, mas a E21 encontrou a máquina com a distribuição **parada
depois de um reinício do Windows** — e, parada, nada roda. A E07 já tinha fixado o
rumo: o agendamento fica **dentro da composição**, e não no Agendador de Tarefas do
Windows, que amarraria o mecanismo a um sistema operacional.

## Alternativas avaliadas

**Quanto à cadência:**

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Cadência calculada pela rotina; a plataforma só envia** | D+*n* por participante, exato; estado pela máquina da seção 12; o teto de lembretes da plataforma vira rede de segurança | a lógica é do projeto e precisa de conferência própria |
| Traduzir P3 para intervalo uniforme (por exemplo, a cada 4 dias, três vezes: D+4, D+8, D+12) e usar a rotina nativa | menos código | altera um parâmetro do projeto por limitação de ferramenta; a rotina nativa ainda precisaria de quem a acione no horário; não distingue `em preenchimento` para gravar o ramo do lembrete (E20) |

**Quanto ao agendador:**

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Laço próprio em Python, processo principal do contêiner `rotinas`** | biblioteca padrão; recebe o ambiente do contêiner, onde estão as credenciais; registra execução prevista, real e **perdida** no mesmo banco; reserva cada horário com chave única | é código do projeto |
| `cron` dentro do contêiner | ferramenta conhecida | o cron do Debian não repassa as variáveis de ambiente aos trabalhos — as credenciais teriam de ir para arquivo; não sabe o que é execução perdida; mais um processo e um pacote na imagem |
| Agendador de binário único (tipo *supercronic*) | resolve o ambiente | binário de fora, a fixar e verificar; continua sem execução perdida |
| Agendador de Tarefas do Windows ou `cron` do hospedeiro | nada a escrever | prende o mecanismo ao sistema do hospedeiro, contra a ADR-0002 e o registro da E07; o hospedeiro não alcança a rede interna, onde estão o correio e o banco |

## Decisão

1. **A cadência é calculada pelo projeto, fora da rotina nativa**, e o P3 não muda.
   `scripts/cadencia.py` decide, por participante, o estado e o que vence; a rotina
   de disparo chama `invite_participants` e `remind_participants` com lista
   explícita, em lotes de até 50, com `continueOnError`, intervalo nulo e teto igual
   ao número de lembretes.
2. **O agendador é um laço próprio no contêiner `rotinas`**, com horário fixo em
   dia útil para o disparo e intervalo próprio para a leitura de devoluções.
3. **O registro próprio** (`egressos_execucoes`, `egressos_disparos`) é a memória de
   execução e de convite: dele saem a execução perdida, o reconvite do reparo e a
   regra dos doze meses.
4. **No hospedeiro Windows, uma tarefa de logon só liga a distribuição**
   (`infra/hospedeiro/liga-wsl-ao-entrar.ps1`). Ela não agenda nada: é o
   equivalente ao Docker subir no boot de um Linux. Criada na máquina do ensaio com
   autorização do orientando.

## Justificativa

Traduzir o P3 para caber na ferramenta seria a ferramenta decidindo um parâmetro
que a E05 fixou por razão própria — dois toques na primeira semana e um terceiro
mais distante. E não resolveria o resto: a rotina nativa não sabe quem está em
preenchimento, não grava o ramo do lembrete e não tem quem a acione. A lógica teria
de ser escrita de qualquer modo — o mesmo argumento da ADR-0004 para a leitura de
devoluções.

O laço próprio ganha do `cron` pelo que o `cron` não faz: ele sabe o que deveria ter
rodado e não rodou. É exatamente a falha que a E07 temia — "funcionou nos testes" e
não dispara no horário — e que só aparece se houver registro do previsto ao lado do
executado.

## Consequências

**Passa a ser verdade:**

- O horário é **fixo e único em dia útil** (10:00, segunda a sexta, menos os
  feriados da agenda). Um lembrete que vence em fim de semana sai no dia útil
  seguinte, e o intervalo mínimo de 3 dias continua valendo: o D+*n* é o mínimo, não
  a data exata.
- **Horário perdido não é executado fora da hora.** Passada a tolerância (30
  minutos), vira registro `perdida`, e o que venceu sai no próximo dia útil, no
  horário. A cadência é por vencimento, e por isso tolera o dia perdido.
- **O hospedeiro precisa estar ligado e acordado no horário.** A tarefa de logon
  cobre o reinício; não cobre suspensão nem hibernação, que continuam produzindo
  execução perdida — agora registrada.
- A rotina sobe em modo **simulado** por padrão: calcula, confere e registra o plano
  sem enviar. O modo real é escolha explícita do `.env`.
- Disparo pelo painel, fora da rotina, **não grava o ramo do lembrete** nem entra no
  registro próprio. Um convite feito assim fica sem janela até a próxima execução
  da rotina, que a grava a partir do envio.

**Esta decisão impede:**

- Operar a cadência pelo painel da plataforma sem perder o ramo do lembrete, o
  reconvite do reparo e a regra dos doze meses.

## Revisão

Revisável se a plataforma passar a expressar cadência por D+*n* desde o convite e a
oferecer agendamento próprio — o que, no LimeSurvey 7.2, não acontece.
