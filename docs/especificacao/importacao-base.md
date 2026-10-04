# Importação da base de participantes

**Etapa:** E17 — importar a base e ativar a tabela de participantes
**Data:** 04/10/2026
**Decorre de:** [`leiaute-entrada.md`](leiaute-entrada.md) (E11),
[`blocos-instrumento.md`](blocos-instrumento.md), seção 12.5 (E13),
[`infra/instrumento/`](../../infra/instrumento/README.md) (E15) e a base sintética
da E16 · **Decisão:** [ADR-0007](../decisoes/0007-base-persistente-de-participantes.md)

Como o arquivo de entrada vira pessoas no mecanismo: validação prévia, gravação
na base central de participantes, criação dos participantes do questionário,
trilha e eliminação do arquivo — e a regra que decide o que prevalece quando a
mesma pessoa chega de novo.

## 1. Objeto e método

**Objeto.** A conversão do questionário 202615 para acesso controlado e a carga
da base sintética da E16 — 500 egressos — na instância.

**Método.** Implementação e verificação por execução, contra a instância viva.
Cada propriedade do critério — sem duplicidade, reimportação idempotente, recusa
preservada, precedência aplicada, arquivo inválido barrado — foi exercitada, e não
presumida (seção 9).

**Decisões tomadas** (confirmadas com o orientando antes da execução):

1. **Base persistente na base central de participantes** do LimeSurvey — a
   [ADR-0007](../decisoes/0007-base-persistente-de-participantes.md), contra a
   opção do RAEG de não manter base fixa.
2. **Precedência de contato: prevalece a correção até a origem mudar** (seção 5).
3. **A ativação do questionário fica para depois da E18.** Ativar trava a
   estrutura (E15), e a E18 ainda configura o pré-preenchimento nas questões. Esta
   etapa fecha o acesso — só por endereço individual — e cria a tabela de
   participantes: é o "acesso controlado" do objetivo.
4. **O participante do questionário recebe o código do instrumento** (curso `T01`,
   campus `SPO`), e a base central guarda o nome, como no arquivo. A tradução que a
   E15 deixou para a E18 é feita aqui, pela configuração.

## 2. O desenho, e por que mudou no meio da etapa

| Onde | O que guarda | Quem grava |
|---|---|---|
| base central (`lime_participants` e atributos) | a pessoa: nome, e-mail, recusa, os outros oito campos do leiaute e o último contato visto na origem | comando de console `importarbasecentral` |
| participante do questionário (`lime_tokens_202615`) | o que o questionário usa: nome, e-mail, token, `participant_id`, identificador e os cinco atributos acadêmicos em código | API (`add_participants`, `set_participant_properties`) |
| trilha (`egressos_importacoes`) | cada importação: data, SHA-256, contagens por regra, situação, se o arquivo foi eliminado | comando de console `registrarimportacao` |

**O desenho inicial era outro, e a instância o desmentiu.** A primeira versão
rodava inteira no contêiner `rotinas`, gravava a base central pela API e lia o
estado atual por SQL para aplicar a precedência. A primeira importação funcionou —
e a conferência mostrou que **a plataforma cifra nome, sobrenome e e-mail da base
central por padrão** (`encrypted = Y` nos atributos centrais, desde a instalação).
Duas consequências:

1. a regra de precedência leria o e-mail **cifrado**, o compararia com o valor de
   origem e, na reimportação, o regravaria — e a plataforma cifraria o texto já
   cifrado: **corrupção do contato**, que a primeira importação, só de pessoas
   novas, não chegava a exercitar;
2. os atributos de contato do projeto tinham sido criados em claro, ao lado de um
   e-mail cifrado — o que esvaziava a proteção que a plataforma dá por padrão.

O desenho corrigido: **todo contato da base central cifrado**, e a comparação feita
**onde a decifração é possível** — num comando de console, com os modelos da
própria plataforma; a chave não sai do contêiner do LimeSurvey. Como o `rotinas`
não alcança o console, a importação passou a rodar no **hospedeiro**, como o
`instrumento.py` da E15. A carga da primeira versão foi apagada antes da correção
(seção 9.1).

## 3. Correspondência com a plataforma — verificada

A E11 deixou a correspondência proposta e não verificada. Verificada agora:

| Campo do leiaute | Base central | Participante do questionário |
|---|---|---|
| `identificador` | atributo `identificador`, em claro; e a origem do `participant_id` | `attribute_1`, em claro — **nunca** o token |
| `nome` | `firstname`, inteiro, **cifrado**; `lastname` vazio | `firstname`, inteiro; `lastname` vazio |
| `email_principal` | `email`, **cifrado** | `email` |
| `curso`, `campus` | atributos, com o nome do arquivo | `attribute_2` e `attribute_4`, com o **código** do instrumento |
| `nivel`, `ano_conclusao`, `semestre_conclusao` | atributos | `attribute_3`, `attribute_5`, `attribute_6` |
| `email_alternativo`, `telefone` | atributos **cifrados** | **não vão** — o questionário não precisa deles |
| — | `email_principal_origem`, `email_alternativo_origem`, `telefone_origem`, **cifrados**: o último contato visto na origem (seção 5) | — |

**Tamanhos.** A base central limita nome a 150 caracteres e e-mail a 254
(`Participant::rules`) — exatamente os limites do leiaute, que os tirou da norma e
da RFC 5321. O `participant_id` tem até 50, e o derivado tem 36. Na tabela do
questionário, nome, e-mail e atributos são `text`. **Nenhum campo do leiaute
trunca.** O filtro que a plataforma aplica aos atributos só escapa `&`, `<` e `>`,
que o leiaute não admite; apóstrofo e hífen passam intactos.

**O elo entre as duas.** É o `participant_id` gravado no participante do
questionário. É por ele que a recusa global nativa encontra a pessoa na base
central (`ParticipantBlacklistHandler::getCentralParticipantFromToken`), e a API o
aceita na criação. A tabela `lime_survey_links`, que a ligação pela tela também
preenche, **não é populada**: ela só registra datas de convite e conclusão, e a
plataforma só a atualiza se já existir. Nenhuma etapa adiante depende dela.

## 4. Validação prévia

`scripts/valida_entrada.py` implementa as seções 3 a 7 do leiaute, em modo de
ensaio, com os três níveis de consequência da seção 6 e as mensagens que nomeiam a
causa provável — planilha em codificação regional, separador ponto e vírgula. A
regra de coerência entre `curso` e `nivel`, ativada na E13, rejeita o registro.

Três leituras do leiaute que a implementação precisou fazer, e que ficam
declaradas:

1. **As restrições do ensaio (seção 7) valem para os valores bem formados.** Um
   telefone malformado é tratado pela seção 6 — descartado, com alerta —, e só um
   telefone válido fora de `+55` com código de área terminado em 0 rejeita o
   arquivo. Sem essa leitura, um erro de digitação derrubaria o arquivo como se
   fosse vazamento.
2. **O arquivo rejeitado também é eliminado.** O tratamento terminou; a
   instituição tem o original, e o relatório diz o que corrigir pela linha e pelo
   identificador.
3. **A importação abortada não elimina.** Se a plataforma falha no meio, o
   tratamento não terminou, e o arquivo precisa estar lá para a repetição — que é
   idempotente, e a base central é gravada numa transação.

Antes de importar, o importador confere também que a configuração de cursos e
unidades é **o mesmo domínio** das opções de IDA1 e IDA3 no instrumento — a
divergência que a E11 temia, em que o pré-preenchimento exibiria valor fora das
opções. Divergindo, aborta.

## 5. Regra de precedência na reimportação

| Dado | Prevalece | Fundamento |
|---|---|---|
| nome e atributos acadêmicos | a origem | E13, seção 12.5 — a fonte é o sistema acadêmico; a correção do egresso fica na resposta e na fila de revisão |
| contato — e-mail principal, alternativo e telefone | **a correção feita pelo mecanismo, até a origem mudar** | decisão da E17 |
| recusa permanente | **nunca é alterada pela importação** | P6 |

**Como se aplica ao contato.** A base central guarda, cifrado, o último valor
visto na origem. Na reimportação:

- se o arquivo traz **o mesmo** valor de antes, a origem não tem nada de novo, e
  fica o valor atual — que pode ter sido corrigido por busca ativa;
- se traz valor **diferente**, a origem tem informação nova — a instituição
  atualizou o cadastro — e ela prevalece; se havia correção, a substituição é
  contada na trilha (`origem_substituiu_correcao`).

Quando o e-mail do participante do questionário muda, o seu estado de entrega
volta a `OK`: o estado anterior era do endereço anterior.

**Por que não "sempre a origem" nem "sempre a correção".** A primeira desfaria o
reparo da P8 a cada extração, enquanto o sistema acadêmico guardasse o endereço
antigo. A segunda ignoraria a atualização legítima feita depois na instituição.

## 6. Trilha e eliminação

Cada execução grava uma linha em `egressos_importacoes`, com: data, SHA-256 do
arquivo, questionário, modo, situação (`importado`, `arquivo_rejeitado` ou
`abortado`), motivo, contagens — registros, aceitos, com alerta, rejeitados e por
regra —, pessoas criadas e atualizadas, participantes criados e atualizados,
bloqueados por recusa, substituições de correção pela origem e se o arquivo foi
eliminado. **Nenhum dado pessoal:** o arquivo é identificado pelo resumo, e o
relatório da execução identifica registros pela linha e pelo identificador.

A tabela fica na base da plataforma, com prefixo próprio, como a
`egressos_devolucoes` da E09.

## 7. Procedimento

Da raiz do repositório, com a composição de pé e o instrumento implantado (E15):

```bash
python3 infra/instrumento/instrumento.py preparar-participantes
python3 scripts/importar_base.py --arquivo dados/sinteticos/base-sintetica.csv --questionario 202615
```

A **preparação** roda uma vez, e é idempotente: cria os atributos da base central
— os de contato, cifrados —, fecha o acesso e cria a tabela de participantes com os
seis atributos nomeados. Não ativa o questionário. Recusa trocar a marca de
cifragem de um atributo que já tem valores gravados, e essa recusa foi exercitada
(seção 9.1).

A **importação** roda a cada arquivo recebido. Para validar sem importar:

```bash
python3 scripts/valida_entrada.py dados/sinteticos/base-sintetica.csv
```

## 8. Armadilhas encontradas

Todas falham sem erro aparente.

1. **A atualização pela API apaga a recusa.** `cpd_importParticipants`, com
   atualização, grava `blacklisted = 'N'` quando o campo não vem no registro. Uma
   reimportação ingênua desfaria a recusa permanente de todos.
2. **A base central é cifrada por padrão** — nome, sobrenome e e-mail —, e a
   leitura direta devolve o texto cifrado (seção 2).
3. **No console, a decifração do participante precisa do Expression Manager**, que
   só a aplicação web carrega. Sem importá-lo, o comando falha — e foi o que abortou
   a importação #2 da trilha, que ficou registrada como tal, com o arquivo mantido.
4. **`activate_tokens` responde "OK" também quando a tabela já existe** — e, nesse
   caso, não a recria (`Token::createTable` ignora o erro de tabela existente).
   Rodar a preparação de novo não apaga participantes; mas a mensagem não diz o que
   aconteceu.
5. **A cifragem da plataforma é determinística**: o mesmo valor produz o mesmo
   texto cifrado. É o que permite a busca exata, e revela igualdade — os três pares
   de e-mail compartilhado aparecem como 497 cifrados distintos para 500 pessoas.

## 9. Verificação do critério

O critério é que **todos os registros sejam criados sem duplicidade**.

### 9.1 O que ficou na trilha, e por quê

| # | Situação | O que foi |
|---|---|---|
| 1 | importado | primeira versão do desenho, com contatos em claro; a carga foi **apagada** em seguida, por SQL, para a correção — limpeza pontual de ensaio, e não parte do procedimento. A preparação recusou trocar a cifragem com os dados presentes, como deve |
| 2 | abortado | armadilha 3: o comando de console sem o Expression Manager; arquivo mantido |
| 3 | importado | primeira carga do desenho corrigido: 500 pessoas, 500 participantes |
| 4 | importado | **reimportação do mesmo arquivo** (T1) |
| 5 | importado | precedência, origem inalterada (T2a) |
| 6 | importado | precedência, origem alterada (T2b) |
| 7 | importado | recusa preservada (T3) |
| 8 | arquivo rejeitado | arquivo com endereço fora de `.test` (T5) |
| 9 | importado | restauração do estado de trabalho, com a base da E16 inalterada |

### 9.2 Resultados

- **Carga.** 500 registros aceitos, nenhum rejeitado; os alertas esperados pela
  E16 — 139 sem via alternativa e os três pares com e-mail principal compartilhado
  —, e os dez domínios em maiúsculas normalizados.
- **T1 — idempotência.** A segunda importação do mesmo arquivo não criou ninguém e
  atualizou os 500; os participantes ficaram **idênticos byte a byte** —
  `participant_id`, token e e-mail. É também a prova de que a decifração funciona:
  um e-mail lido cifrado e regravado mudaria a assinatura.
- **T2 — precedência.** Uma correção por busca ativa foi simulada na base central,
  por comando de teste não versionado, porque a busca ativa é da E21 e da E26.
  Reimportado o mesmo arquivo, **a correção permaneceu**, e o participante do
  questionário passou a usá-la. Com a origem trazendo endereço novo, **a origem
  prevaleceu**, a substituição foi contada e o estado de entrega voltou a `OK`.
- **T3 — recusa.** Uma pessoa marcada com recusa permanente, e retirada do
  questionário como num ciclo novo, **continuou com a recusa** depois da
  reimportação e **não foi recolocada** — "bloqueados por recusa: 1".
- **T4 — validador.** **27 casos plantados, 27 com o desfecho esperado**: os seis
  de arquivo (codificação, separador, coluna a mais, coluna opcional ausente,
  coluna repetida, aspas abertas), os três do ensaio (e-mail principal e
  alternativo fora de `.test`, código de área em uso), dois tolerados (marcador de
  ordem de bytes, linhas vazias), treze de registro e três de alerta — e em nenhum
  o relatório reproduziu nome, endereço ou telefone.
- **T5 — arquivo rejeitado.** Nada mudou na instância, a trilha registrou a
  rejeição com o motivo e o arquivo foi eliminado.
- **Estado final.** 500 pessoas na base central, 500 participantes no 202615;
  `participant_id`, tokens e identificadores distintos — os identificadores também
  sem distinguir maiúsculas —; nenhum participante sem pessoa na base central;
  nenhuma recusa; questionário inativo e com acesso fechado. **Critério atendido.**

## 10. O que esta etapa não permite afirmar

1. **A recusa global nativa não foi exercitada.** O elo que ela usa — o
   `participant_id` no participante — está gravado e conferido, mas a recusa pelo
   endereço individual exige questionário ativo. É da E22 e da E23.
2. **A tabela do questionário não é cifrada.** Nome e e-mail do participante ficam
   em claro ali, como a plataforma faz por padrão. Decidir a cifragem dos
   participantes do questionário é da E23.
3. **A busca ativa foi simulada.** A precedência foi exercitada com uma correção
   gravada por comando de teste, e não pela rotina que a fará.
4. **A remoção de quem sai do arquivo não foi tratada.** Quem estava numa extração
   e não está na seguinte continua na base central; a política de retenção é da
   E23.
5. **Nada aqui envolveu dado de pessoa real.**

## 11. O que esta etapa determina para as etapas seguintes

- **E18 (pré-preenchimento)** — os atributos do participante já estão em código:
  `attribute_2` é o código de IDA1 e `attribute_4` o de IDA3; `attribute_3`,
  `attribute_5` e `attribute_6` são nível, ano e semestre. A ativação do
  questionário fica com a E18, depois de configurar o pré-preenchimento.
- **E19 (unicidade)** — a base tem os três pares de e-mail compartilhado plantados
  pela E16; o `participant_id` derivado torna o identificador repetido impossível
  na base central, e a verificação deve conferi-lo também no participante.
- **E21 (rotina)** — o e-mail atual da pessoa está cifrado na base central, e no
  participante do questionário em claro; a correção por busca ativa precisa gravar
  nos dois, e na base central só por comando de console, como a importação.
- **E22 e E23 (conformidade)** — exercitar a recusa global nativa com o questionário
  ativo; decidir a cifragem dos participantes do questionário; declarar a cifragem
  determinística; política de retenção da base central; a trilha
  `egressos_importacoes` como insumo de auditoria.
- **E25 (matriz)** — os 27 casos do validador são ponto de partida dos arquivos
  inválidos de propósito, e a recusa preservada na reimportação é requisito
  verificável.
- **E30 (guia)** — a preparação e a importação são dois comandos; o guia precisa
  dizer que a importação roda no hospedeiro e por quê.
