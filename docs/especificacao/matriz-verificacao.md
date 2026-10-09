# Matriz de verificação

**Etapa:** E25 — montar a matriz de verificação executável
**Data:** 09/10/2026
**Decorre de:** a matriz da Fase 6 do [documento do projeto](../projeto/README.md) —
doze requisitos, com procedimento e resultado esperado —, desdobrada contra as
especificações das etapas E05 a E23 e contra o critério K6 da
[ADR-0002](../decisoes/0002-ambiente-execucao.md)
**Executam:** E26 (cenários), E27 (registro e correção), E28 (extração) — seção 2
**É:** o critério de aceite do mecanismo. Nas palavras do projeto, "considera-se
validado o artefato que atenda integralmente aos requisitos nela previstos".

> **Notação.** R01 a R12 são os doze requisitos do projeto, na ordem dele. Cada um se
> desdobra em itens (R01.1, R01.2…). VC1 a VC4 são verificações complementares, fora
> dos doze (seção 16). Casos negativos têm prefixo próprio por requisito (N, U, M).
> As consultas ao banco citadas como **C-xx** estão no Apêndice A.

## 1. Objeto e método

**Objeto.** A matriz do projeto tem doze linhas e três colunas — requisito,
procedimento e resultado esperado. Escrita antes de existir o mecanismo, ela diz
*o que* verificar, mas não *como*: "marcar parte da base como respondente" não
indica a marcação nem onde ler o resultado. Esta etapa a converte em roteiro
aplicável e acrescenta o campo de resultado obtido (seção 17).

**Método.** Cada requisito conserva a redação do projeto na primeira linha e é
desdobrado em itens, **cada item redigido contra a especificação da etapa que o
implementou**, e não contra a noção genérica. O exemplo que decide o método vem da
E05: "não respondente" não é estado da base
([`parametros-contato.md`](parametros-contato.md), seção 12). Uma verificação
escrita contra ele não teria o que ler. Por isso a seletividade do lembrete é
verificada contra os estados `convidado` e `em preenchimento`, e não contra
"não respondente".

Cada item tem procedimento, resultado esperado e o momento em que roda. Onde a regra
pode falhar sem erro aparente, há também **casos negativos**: defeitos plantados
que a conferência tem de reprovar. A razão é uma lição do próprio projeto. Na E16,
uma rodada de mutação "passou" em tudo porque a conferência tinha quebrado e não
imprimia nada. Na E21, a janela esperada era calculada pela mesma função conferida.
Conferência que só vê o caso bom não distingue "funciona" de "não confere nada". Pelo
mesmo motivo, as sondas de contenção (VC1) têm **controle positivo**.

**O que a matriz mede.** Comportamento observado do sistema, sob base sintética. Não
mede aceitação percebida, como o modelo de Davis (1989) usado por Silva et al. (2024)
para avaliar o SAVE, nem resultado de coleta real. Nenhum dos dois desenhos mede o
segundo ([fichamento de Silva 2024](../pesquisa/fichamentos/silva-2024.md), ponto 4).

**Onde a matriz encosta na régua oficial.** O Indicador 3.7 do INEP pede, no
conceito 3, "atualização sistemática de informações"
([linha de base](../pesquisa/linha-de-base.md), seção 8). R06, R07, R09 e R10 são a
parte da matriz que corresponde a essa expressão: a **capacidade instalada de
cobrança sistemática** — saber a quem perguntar, perguntar de novo a quem não
respondeu e parar quando se deve. Atendê-los não demonstra elevação de taxa de
resposta, que sem aplicação real não há como verificar.

## 2. Como usar

### 2.1 Quando cada item roda

| Momento | Quando | O que roda | Por quê |
|---|---|---|---|
| **A** | abertura da E26, **antes** de ligar o modo real (`ROTINA_DISPARO=real`) | contenção, arquivos inválidos, carga, idempotência e a bateria das conferências que exercitam e desfazem | ver abaixo |
| **C** | durante a E26 | o que depende do caminho real do respondente, do modo real, de dias de calendário ou da operação de reparo | é o que a E26 entrega |
| **F** | fechamento, na E27 | consultas e exportação sobre o estado que a E26 deixou | só leitura |
| **X** | E28 | a extração pela rotina própria e a anonimização | a rotina é da E28 |

**Por que a bateria roda em A, e não na E27.** As conferências que exercitam e
desfazem — `confere-rotina.py --agendada`, `confere-consentimento.py --exercitar`
e `confere-conformidade.py --exercitar` — foram calibradas para o 202615 limpo. As
limpezas delas conferem o estado final **contra zero**: nenhuma resposta no
questionário e, conforme a conferência, nenhum envio registrado, nenhuma recusa,
nenhuma higienização. Lido no código, não presumido. Depois que a E26 ligar o modo
real e o caminho real criar respostas, as três acusariam **falha falsa na limpeza**.
Não apagariam o que a E26 produziu: desfazem o que plantaram, e a de conformidade
também apaga registro de higienização cuja resposta não existe mais. A
`--agendada` ainda aponta o agendador para o ciclo de teste enquanto roda, o que, no
modo real, interferiria na cadência em curso. Daí a regra: **a bateria roda na
abertura da E26**. Se a E27 precisar reexecutá-la depois, as três limpezas terão de
passar a comparar com o estado anterior, e não com zero. É correção da E27, se for
preciso.

**Por que a carga (R01.1) também roda em A.** A carga completa só é possível com o
202615 sem resposta e sem envio. O `implantar --substituir` recusa no caso contrário,
e com razão: depois da E26, refazê-la apagaria o que a E28 vai extrair.

### 2.2 Pré-condições

1. **Composição de pé:** `./verifica-ambiente.sh` sem falha, a partir de `infra/`.
2. **Instrumento:** 202615 ativo, termo `ensaio-2`, trilha ativa
   (`python3 conformidade.py aplicar`, idempotente).
3. **Hospedeiro ligado às 10:00 em dia útil**, durante toda a E26. Achado desta
   etapa, na trilha: os disparos agendados de 07, 08 e 09/10/2026 foram registrados
   como `perdida`. Nesses três dias, nenhuma das três tarefas rodou entre 05:00 e
   11:27: o hospedeiro estava parado. A
   rotina fez o que devia: registrou a perda e não disparou fora da tolerância. Mas,
   com o modo real ligado, cada dia perdido atrasa a cadência inteira. **12/10/2026 é
   feriado na agenda.**
4. **Nenhum script fixa `Q<qid>` nem token:** o 202615 foi reimplantado duas vezes, e
   será de novo em A (R01.1). As conferências leem os nomes da instância.
5. **Uma conferência que exercita por vez.** Elas compartilham o agendador, as caixas
   e os participantes livres.
6. **Nada de dado real**, nem endereço fora de `.test`. Os casos negativos que
   precisam de um "valor real" usam domínio reservado (`example.com`, RFC 2606) ou
   número que o plano de numeração não atribui. Nunca dado de pessoa.

### 2.3 Onde cada comando roda

| Prefixo | Onde |
|---|---|
| `infra$` | no hospedeiro (a distribuição do WSL), a partir de `infra/` |
| `raiz$` | no hospedeiro, a partir da raiz do repositório |
| `rotinas$` | no contêiner `rotinas`, por `docker compose exec rotinas …`, a partir de `infra/` |

As consultas ao banco seguem o padrão do Apêndice A: o cliente do próprio contêiner
do banco, com a senha lida **do ambiente do contêiner**. A senha não aparece na
linha de comando do hospedeiro, nem em mensagem de erro. Na E22, uma quebra repetiu
a linha de comando no terminal, com a senha dentro.

### 2.4 Como registrar

Cada item executado ganha uma linha na seção 17: data, commit, resultado obtido e
situação. A situação é uma de quatro:

| Situação | Quando |
|---|---|
| **atende** | o resultado obtido é o esperado |
| **atende, com ressalva** | atende sob condição declarada que a matriz admite — tempo comprimido (P5, seção 7.2), emulação de dispositivo (R12) |
| **não atende** | diverge do esperado; a E27 corrige e reexecuta |
| **desvio justificado** | diverge, e a E27 registra por que o desvio não compromete o requisito, ou por que não pode ser corrigido no projeto |

O requisito **atende** quando todos os seus itens atendem, com ou sem ressalva;
tem **desvio justificado** quando algum item tem e nenhum "não atende"; e **não
atende** nos demais casos. É a leitura do critério da E27: "todos os requisitos
atendidos ou o desvio justificado".

## 3. Quadro-resumo

| Req. | Do projeto: procedimento → resultado esperado | Itens | Momentos | Procedimento pronto? |
|---|---|---|---|---|
| R01 | importar o arquivo sintético completo → todos os registros criados, sem duplicidade | 6 | A, C | sim (E17) |
| R02 | comparar os endereços individuais gerados → nenhum endereço repetido ou inválido | 4 | A | sim (E19) |
| R03 | abrir acessos individuais de amostra → atributos exibidos conforme a base de origem | 5 | A, C | parcial (E18) |
| R04 | percorrer os caminhos alternativos previstos → apenas os blocos pertinentes são exibidos | 8 | A, C | sim (E15) |
| R05 | interromper e reabrir o acesso → respostas anteriores preservadas | 5 | C | percurso (E15) |
| R06 | aguardar a janela de execução programada → disparo executado no horário definido | 4 | A, C, F | sim (E21) |
| R07 | marcar parte da base como respondente → lembrete enviado apenas aos não respondentes | 5 | A, C, F | sim (E21) |
| R08 | aceitar o termo em acesso de amostra → aceite, data e versão persistidos | 5 | A, C, F | sim (E22) |
| R09 | acionar a manifestação de recusa → nenhum disparo posterior ao participante | 7 | A, C, F | sim (E23) |
| R10 | incluir endereço inexistente na base → retorno registrado e contato marcado | 7 | A, C | sim (E09) |
| R11 | exportar o conjunto de respostas → arquivo íntegro e estruturado | 5 | F, X | **definido aqui** |
| R12 | abrir o instrumento em dispositivo móvel → instrumento utilizável sem perda de função | 4 | C | **definido aqui** |

Cada requisito tem uma seção abaixo. Em cada uma: o que o projeto pede, contra que
especificação o requisito é redigido, e os itens.

## 4. R01 — Importação da base

**Do projeto:** importar o arquivo sintético completo → todos os registros criados,
sem duplicidade.
**Redigido contra:** [`leiaute-entrada.md`](leiaute-entrada.md), seções 3 a 7, e
[`importacao-base.md`](importacao-base.md), seções 5, 6 e 9.
**Por que mais que a carga:** a carga do arquivo bom não exercita nenhuma regra de
rejeição (E11). E a importação tem duas propriedades que só aparecem na segunda vez,
a idempotência e a recusa preservada (E17).

**Valores esperados da base.** O gerador é determinístico, e a base regenerada com a
semente padrão tem SHA-256 `f2e5b698…202c2a455`. Conferido nesta etapa: o resumo é
o mesmo das importações nº 10, 11 e 12 da trilha. Os valores abaixo são dela:
500 registros; 255 técnicos, 202 de graduação, 43 de pós; 255 do 1º semestre e 245
do 2º; principal em `egressos.test` (436), `invalido.test` (45) e
`indisponivel.test` (19); alertas: 139 "sem via alternativa de contato" e 6 "email
principal compartilhado" (três pares), 144 registros com alerta.

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R01.1 | **Carga completa** | a sequência abaixo da tabela: regenerar, validar, reimplantar o 202615, preparar, importar, ativar e conferir | validador: 500 lidos, 500 aceitos (144 com alerta), 0 rejeitados, só os dois alertas esperados; nova linha em `egressos_importacoes`: `importado`, `participantes_criados = 500`, `base_central_criados = 0`, `base_central_atualizados = 500` (as 500 pessoas **reencontradas**, nenhuma duplicada), `arquivo_eliminado = 1`; arquivo ausente de `dados/sinteticos/`; conferência de unicidade 8 de 8 | A |
| R01.2 | **Reimportação idempotente** | impressão digital C-01 antes; regenerar a base (a importação elimina o arquivo) e importar de novo; C-01 depois | `participantes_criados = 0`, `participantes_atualizados = 500`, `base_central_criados = 0`; as duas digitais **iguais** antes e depois — `participant_id`, token, e-mail, estado de entrega e atributos, byte a byte | A |
| R01.3 | **Precedência na reimportação** | (a) corrigir o contato de uma pessoa pela operação de reparo da E26 e reimportar o mesmo arquivo; (b) reimportar com a origem trazendo endereço novo para outra pessoa | (a) a correção **permanece** na base central e no participante; (b) **a origem prevalece**, `origem_substituiu_correcao` conta 1 e o estado de entrega volta a `OK` | C |
| R01.4 | **Recusa preservada na reimportação** | com recusas de contato reais da E26 na base central: lista C-02 antes; reimportar; C-02 depois | o conjunto de pessoas com `blacklisted = 'Y'` é **idêntico** antes e depois; nenhuma pessoa bloqueada é recriada em questionário de que não participa (`bloqueados_por_recusa` no relatório). É a armadilha 1 da E17: a atualização pela API grava `blacklisted = 'N'` | C |
| R01.5 | **Arquivos inválidos de propósito** | os 31 casos da tabela abaixo, um arquivo por caso, cada um uma cópia da base com **um** defeito; `raiz$ python3 scripts/valida_entrada.py <cópia>` — só valida, não importa; cópias fora do repositório ou em `dados/sinteticos/`, que não é versionado, e apagadas ao fim | cada caso com o desfecho da tabela; **em nenhum** o relatório reproduz nome, endereço ou telefone | A |
| R01.6 | **Arquivo rejeitado sem efeito** | importar (`importar_base.py`) o caso N08; C-01 antes e depois | nada muda na instância (digitais iguais); linha `arquivo rejeitado` em `egressos_importacoes`, com o motivo; arquivo eliminado. É também item da contenção (VC1.6) | A |

**Sequência de R01.1.** É a das E22 e E23, que reimplantaram o 202615 sem nada a
perder, cada vez **com autorização do orientando**. A reimplantação troca os tokens,
e não há a quem isso importe: nenhuma mensagem foi enviada.

```bash
python3 scripts/gerar_base_sintetica.py                                  # raiz$
python3 scripts/valida_entrada.py dados/sinteticos/base-sintetica.csv    # raiz$
python3 infra/instrumento/instrumento.py implantar --substituir          # raiz$
python3 infra/instrumento/instrumento.py preparar-participantes          # raiz$
python3 scripts/importar_base.py --arquivo dados/sinteticos/base-sintetica.csv \
    --questionario 202615                                                # raiz$
python3 infra/instrumento/instrumento.py ativar                          # raiz$
python3 infra/confere-participantes.py                                   # raiz$
```

A carga **do zero** — com `docker compose down -v`, em que as 500 pessoas são
criadas também na base central (`base_central_criados = 500`) — é a variante que o
teste de replicação da E30 faz. Na abertura da E26, apagaria sem necessidade a trilha
das etapas anteriores.

**Casos negativos de R01.5.** Um por regra de `scripts/valida_entrada.py`. Salvo
indicação, o defeito vai na linha do identificador `SIN-000100`. "Lidos" e "aceitos"
contam registros.

| Caso | Defeito plantado | Desfecho esperado |
|---|---|---|
| N01 | arquivo regravado em codificação regional (Windows-1252) | **arquivo rejeitado**: "nao decodifica como UTF-8 — causa provavel: planilha exportada em codificação regional" |
| N02 | separador ponto e vírgula | **arquivo rejeitado**: "cabecalho nao se divide em campos por virgula" |
| N03 | coluna a mais (`cpf`, vazia) | **arquivo rejeitado**: "colunas fora do leiaute ['cpf']" |
| N04 | coluna opcional ausente (`telefone`) | **arquivo rejeitado**: "faltam ['telefone']" |
| N05 | coluna repetida (`email_alternativo` duas vezes) | **arquivo rejeitado**: "repetidas ['email_alternativo']" |
| N06 | aspas abertas e não fechadas até o fim | **arquivo rejeitado**: "CSV malformado" |
| N07 | arquivo vazio (0 bytes) | **arquivo rejeitado**: "arquivo vazio" |
| N08 | `email_principal` sintaticamente válido fora de `.test` (`…@example.com`) | **arquivo rejeitado** (seção 7): "endereco fora de .test na linha …" |
| N09 | `email_alternativo` fora de `.test` (`…@example.com`) | **arquivo rejeitado** (seção 7), idem |
| N10 | telefone com código de área em uso: `+551100000000` — o código 11 existe; o número `0000-0000` não é atribuível | **arquivo rejeitado** (seção 7): "telefone fora de +55 com codigo de area terminado em 0" |
| N11 | marcador de ordem de bytes no início | **tolerado**: 500 lidos, 500 aceitos, como sem o marcador |
| N12 | três linhas inteiramente vazias no meio | **tolerado**: 500 lidos |
| N13 | uma vírgula a mais na linha | registro rejeitado: "numero de campos diferente do cabecalho"; 499 aceitos |
| N14 | quebra de linha dentro do nome, entre aspas | registro rejeitado: "campo com quebra de linha" |
| N15 | `curso` vazio | registro rejeitado: "campo obrigatorio vazio: curso" |
| N16 | identificador com barra (`SIN/000100`) | registro rejeitado: "identificador fora da regra" |
| N17 | identificador com forma de CPF, **construído**: nove dígitos de base fixa (`000000001`) seguidos dos dois verificadores calculados pela regra de `tem_forma_de_cpf`. Nunca número tirado de documento | registro rejeitado: "identificador com forma de CPF" |
| N18 | nome com dígito | registro rejeitado: "nome fora da regra" |
| N19 | curso fora da lista | registro rejeitado: "curso fora da lista" |
| N20 | `nivel` = `mestrado` | registro rejeitado: "nivel fora do dominio" |
| N21 | curso técnico com `nivel` = `graduacao` | registro rejeitado: "nivel incoerente com o curso" |
| N22 | campus fora da lista | registro rejeitado: "campus fora da lista" |
| N23 | ano de conclusão posterior ao corrente | registro rejeitado: "ano de conclusao fora da regra" |
| N24 | semestre `3` | registro rejeitado: "semestre fora do dominio" |
| N25 | `email_principal` com dois `@` | registro rejeitado: "email principal fora da sintaxe" |
| N26 | identificador de `SIN-000101` trocado por `sin-000100` (repetido, outra caixa) | **os dois** registros rejeitados: "identificador repetido no arquivo"; 498 aceitos |
| N27 | `email_alternativo` com dois `@` | aceito, com alerta "email alternativo fora da sintaxe, descartado" |
| N28 | `email_alternativo` igual ao principal | aceito, com alerta "email alternativo igual ao principal, descartado" |
| N29 | telefone `11 9999` | aceito, com alerta "telefone fora da regra, descartado" |
| N30 | — (já na base) | 6 alertas "email principal compartilhado com outro identificador" |
| N31 | — (já na base) | 139 alertas "sem via alternativa de contato" |

**Origem dos casos.** N01 a N06 são os de arquivo que a E16 não tinha (codificação,
separador, cabeçalho, aspas). Os sete defeitos da E16 são N08, N10, N17, N18, N21, N26
e N28. A E17 exercitou 27 casos e os relatou por categoria, sem lista nominal. A
matriz enumera 31, um por regra do validador. A diferença está no arquivo vazio, nos
dois alertas que a própria base produz e numa regra de registro.

## 5. R02 — Unicidade dos acessos

**Do projeto:** comparar os endereços individuais gerados → nenhum endereço repetido
ou inválido.
**Redigido contra:** [`unicidade-participantes.md`](unicidade-participantes.md) e a
C1 de [`capacidades-plataforma.md`](capacidades-plataforma.md). "Inválido" tem
definição própria, da E19: o contador nativo `token_invalid` conta exatamente o
token nulo ou vazio.

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R02.1 | **Conferência de unicidade** | `infra$ python3 confere-participantes.py` | **8 de 8**; alerta de e-mail compartilhado com **3 grupos**, exatamente os pares da base: SIN-000230 · SIN-000461; SIN-000267 · SIN-000354; SIN-000345 · SIN-000408 | A |
| R02.2 | **O endereço da mensagem é o do participante** | `infra$ python3 confere-mensagens.py --enviar` (conferência 6) | o endereço individual da mensagem recebida é o do participante e abre o questionário; o de recusa abre a página de confirmação, que **não** é confirmada | A |
| R02.3 | **Controle de acesso** | numa cópia de ensaio (`raiz$ python3 infra/instrumento/instrumento.py copia-de-ensaio`), sessão nova a cada tentativa (`&newtest=Y`): sem token; token inexistente; token de participante que concluiu; token com `validuntil` no passado, em UTC, pela API; remover a cópia ao fim | sem token: a plataforma pede o código de acesso; inexistente: "não é válido ou já foi usado"; concluído: "Esse convite já foi utilizado"; vencido: acesso recusado | A |
| R02.4 | **Casos negativos** | os 15 defeitos abaixo, plantados um por vez numa **cópia em memória** dos dados — `carrega()` de `scripts/conferencia_participantes.py`, alterar a cópia, `confere()`. O banco não é tocado | cada defeito reprovado pela conferência da tabela; reprovações em cascata admitidas onde indicado | A |

| Caso | Defeito | Reprova |
|---|---|---|
| U01 | token vazio | 1 |
| U02 | token nulo | 1 |
| U03 | token curto | 2 |
| U04 | token com caractere fora do alfanumérico | 2 |
| U05 | token repetido | 3 |
| U06 | token repetido só na caixa | 3 |
| U07 | identificador repetido com outra caixa | 4 (e 6, em cascata: o `participant_id` deriva do identificador) |
| U08 | identificador ausente | 4 |
| U09 | identificador igual a um token | 5 |
| U10 | `participant_id` órfão | 6 |
| U11 | `participant_id` repetido | 6 |
| U12 | pessoa da base central, sem recusa, fora do questionário | 7 |
| U13 | identificador repetido na base central | 7 |
| U14 | quarto par de e-mail compartilhado só no questionário | 8 |
| U15 | par compartilhado só na base central | 8 |

Os quinze são os da seção 5.1 de `unicidade-participantes.md`. A tabela acrescenta a
conferência que cada um tem de reprovar.

## 6. R03 — Pré-preenchimento

**Do projeto:** abrir acessos individuais de amostra → atributos exibidos conforme a
base de origem.
**Redigido contra:** [`pre-preenchimento.md`](pre-preenchimento.md) e a seção 12.5
de [`blocos-instrumento.md`](blocos-instrumento.md). A E13 acrescentou o que o
projeto não dizia: corrigir um atributo preserva o original (E13, nota para a E25).

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R03.1 | **Ligação estrutural** | `infra$ python3 confere-instrumento.py` (conferência 7) | cada campo da identificação aponta para o atributo do participante de mesmo nome; o derivado IDA2 não tem padrão | A |
| R03.2 | **Acessos de amostra, um por nível** | três participantes do 1º semestre convidados na E26, um técnico, um de graduação e um de pós: pelo endereço da mensagem recebida, aceitar o termo e ler a página 2 | IDA1, IDA2, IDA3, IDA4 e IDA5 iguais à linha do identificador no arquivo regenerado, traduzida pela configuração (nome do curso → código, por exemplo). Precedente: a tabela da seção 6 de `pre-preenchimento.md` | C |
| R03.3 | **Os 500, e não só a amostra** | atributos dos participantes pela API, comparados com `infra/instrumento/configuracao/` | 500 de 500 com curso e campus entre as opções do instrumento, ano e semestre válidos e nível coerente com o curso: nenhum abrirá com campo vazio por padrão inválido | A |
| R03.4 | **Correção preserva o original** | num participante técnico da E26, trocar o curso por um de graduação na página 2, enviar e seguir; depois, a fila de revisão: exportação da resposta com cabeçalho por código, comparada com os atributos do participante | IDA2 passa a "Graduação" **na hora, sem envio**; a resposta guarda o curso e o nível corrigidos; o participante continua com os originais e sem marca de concluído; a fila aponta **exatamente** as divergências plantadas | C |
| R03.5 | **A correção não move o ciclo** | no mesmo participante, corrigir também o ano de conclusão; `rotinas$ python3 disparar.py --simular` antes e depois | o atributo de ano do participante não muda; o plano da rotina para ele é o mesmo antes e depois. A âncora vem da base, não da autodeclaração (seção 12.5, item 5). `disparar.py --simular` não envia nem grava na plataforma | C |

## 7. R04 — Navegação condicional

**Do projeto:** percorrer os caminhos alternativos previstos → apenas os blocos
pertinentes são exibidos.
**Redigido contra:** os públicos da seção 2 de `blocos-instrumento.md` (E12), as
regras de campo da seção 12.10 (E13) e os **dez caminhos** de
[`navegacao-condicional.md`](navegacao-condicional.md) (E14), na forma em que a E15
os conferiu (seção 11).

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R04.1 | **Conferência estrutural** | `infra$ python3 confere-instrumento.py` | **9 de 9**: onze grupos na ordem, 35 campos com tipo, obrigatoriedade e domínio, listas de configuração, nível derivado, validações de contato, **os dez caminhos sobre as 2.802 combinações** das respostas que decidem, pré-preenchimento, metadados do consentimento e cifragem | A |
| R04.2 | **Os dez caminhos pela interface** | cada caminho ao menos uma vez, pelo caminho real do respondente, com as respostas que decidem da tabela da seção 11.1 de `navegacao-condicional.md`; no 202615, com participantes convidados na E26, para que a E28 tenha o que extrair; a cópia de ensaio serve para repetir sem consumir convite | cada caminho exibe **exatamente** os blocos da seção 5; nenhuma resposta tem os Blocos V e VI preenchidos ao mesmo tempo | C |
| R04.3 | **Regras de campo na mesma página** | nos percursos de R04.2, mudar cada resposta que decide antes de enviar a página | CON2 aparece e some com CON1; AP2 com AP1; SA2 só com "trabalhando" ou "estudando e trabalhando"; EF2 e EF3 somem com EF1 = não; IDA2 acompanha o curso — tudo **sem envio** | C |
| R04.4 | **O valor confirmado decide** | participante técnico corrige o curso para um de pós-graduação na página 2 (e, noutro percurso, o inverso) | o Bloco IV passa a mostrar só EF4 (e, no inverso, EF1 a EF4): decide o nível enviado na página 2, e não o atributo | C |
| R04.5 | **Trabalho sem remuneração segue para o Bloco VI** | percursos C6 (negócio familiar sem remuneração) e C10 (estágio não remunerado) | Bloco VI, e não V — a correção da E13 sobre o instrumento documentado | C |
| R04.6 | **Voltar, com descarte** | (a) chegar ao Bloco V, voltar, mudar a situação para "só estudando" e concluir; (b) chegar ao Bloco III, voltar e mudar CON1 para recusa; (c) concluir com CON2 = concordo, voltar e mudar para não concordo, concluir | registro final: (a) sem SA2 nem PM1 a PM3; (b) **só** CON1, com a versão e o momento — identificação, avaliação e o texto de AF4 descartados; (c) sem EQ1 a EQ4. O descarte acontece **no envio final** (E15, seção 11.2 a): ver R05.5 | C |
| R04.7 | **Recusa na página 1 não conta como respondente** | percursos C1 e C2; plano da rotina; `get_summary` | a plataforma marca as duas como concluídas (`submitdate` preenchido); o plano as lê como `recusa de consentimento` e `recusa de contato`, e não como respondente. A contagem nativa de completas **inclui as recusas** (E15, seção 11.2 e) | C |
| R04.8 | **Validações barram o envio** | ano de conclusão posterior ao corrente; e-mail fora de `.test` em CT; telefone com código de área em uso; alternativo igual ao principal | a página não avança até a correção, com a mensagem junto ao campo | C |

## 8. R05 — Retomada de preenchimento

**Do projeto:** interromper e reabrir o acesso → respostas anteriores preservadas.
**Redigido contra:** a seção 7.3 de `navegacao-condicional.md`. A E14 decidiu que
retomar é **salvar, fechar e carregar com nome e senha**, e não a simples reabertura
do endereço, e registrou o motivo: o endereço é transportável, e as respostas salvas
podem conter dado sensível. Reabrir sem carregar é outro item (R05.3), com outro
resultado esperado.

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R05.1 | **Salvar, fechar e carregar** | no meio do Bloco III, "Retomar mais tarde" com nome e senha, sem e-mail; fechar o navegador; abrir o endereço em sessão nova, "Carregar questionário não finalizado" com nome e senha; concluir | volta à página em que parou, com as respostas; `lime_saved_control` guarda nome, senha **em hash bcrypt**, passo e IP vazio; a conclusão vai para **a mesma** resposta, e o registro de salvamento é apagado pela plataforma | C |
| R05.2 | **Interromper sem salvar** | enviar até o Bloco II e fechar | o enviado até a última página fica gravado (`submitdate` vazio, CON1 = concordo); o participante fica `em preenchimento` no plano da rotina; sem nome e senha, não há como recuperar — o custo declarado da decisão | C |
| R05.3 | **Reabrir sem carregar** | depois de R05.2, abrir o endereço em sessão nova e enviar a página 1 | a plataforma começa **outro** preenchimento: uma segunda resposta do mesmo participante; a primeira fica parcial órfã. A regra — uma concluída por participante e ciclo, órfãs descartadas na extração — é da E28 | C |
| R05.4 | **Lembrete de retomada** | o participante de R05.2 até o próximo lembrete vencido, em dias de calendário ou com o tempo comprimido e declarado | recebe o lembrete com o ramo `em_preenchimento`, que ensina a carregar o questionário não finalizado; o registro em `egressos_disparos` tem `estado = em preenchimento` e `variante = em_preenchimento` | C |
| R05.5 | **Parcial com campos fora do caminho** | chegar ao Bloco V e aos recortes de equidade, voltar, mudar a situação e CON2 para não concordo, e abandonar | a parcial **guarda** PM1 a PM3, fora do caminho (E15, seção 11.2 a). Os recortes de equidade gravados sem consentimento são **apagados** pela rotina de conformidade em até 30 minutos, com registro em `egressos_higienizacoes`. A extração (E28) reaplica as regras de exibição às parciais | C |

## 9. R06 — Rotina agendada

**Do projeto:** aguardar a janela de execução programada → disparo executado no
horário definido.
**Redigido contra:** [`rotina-disparo.md`](rotina-disparo.md), seções 5, 7 e 9, e a
[ADR-0008](../decisoes/0008-agendamento-da-cadencia.md). "Horário definido" é o da
agenda: 10:00, de segunda a sexta, menos os feriados, com tolerância de 30 minutos.
Depois dela, a execução é registrada como `perdida` e não acontece fora de hora.

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R06.1 | **O disparo real, no horário, pelo agendador** | `infra$ python3 confere-rotina.py --agendada` (dia útil; ao menos uma execução agendada do ciclo corrente já feita) | **14 de 14**; na conferência 10, a execução começou no horário de teste, em segundos (11 s na E21), e ficou `concluida` | A |
| R06.2 | **A execução perdida é registrada** | `infra$ python3 confere-rotina.py --perdida` | **8 de 8**: horário vencido além da tolerância vira `perdida`, acusada no log, e **não** executa fora da hora | A |
| R06.3 | **A rotina no período da E26, em dias de calendário** | C-03 sobre o período da E26, cruzada com a agenda | **uma** execução agendada de disparo por dia útil que não seja feriado: `concluida`, com atraso menor que a tolerância, ou `perdida` **com** o hospedeiro comprovadamente parado — lacuna nas outras tarefas no mesmo intervalo; **nenhuma** execução em fim de semana ou feriado (C-04); nenhuma duplicada (a chave única o impede) | C, F |
| R06.4 | **Devoluções e conformidade, independentes do disparo** | C-05 sobre o período da E26 | as duas tarefas a cada 30 minutos, todo dia, enquanto o hospedeiro está de pé, cada uma com o seu registro; a falha de uma não impede as outras. Horário que passa com o hospedeiro parado **não** vira `perdida` nessas duas: a primeira execução depois da volta recupera o intervalo (em 07/10/2026, a das 11:00 rodou às 11:27). Lacuna simultânea nas três tarefas é hospedeiro parado, e não falha da rotina | F |

A cadência D+4, D+7 e D+14 **em dias de calendário** é verificada em R07.5. Aqui se
verifica o relógio; lá, o que ele dispara.

## 10. R07 — Seletividade do lembrete

**Do projeto:** marcar parte da base como respondente → lembrete enviado apenas aos
não respondentes.
**Redigido contra:** a máquina de estados da seção 12 de `parametros-contato.md`.
"Não respondente" não é estado: é o conjunto de `convidado`, `em preenchimento` e
`expirado`, e **só os dois primeiros recebem lembrete**. O `expirado` não recebe,
porque a janela fechou. A "marcação" do projeto não é marca: é responder pelo caminho
real, ou recusar, ou ter contato inválido. A rotina **calcula** o estado e não grava
nenhum.

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R07.1 | **As regras, sem plataforma** | `infra$ python3 confere-rotina.py` | **7 de 7**: 16 casos de estado, 19 de vencimento, fim de semana, janela, dia útil e feriado, faixa da agenda, ramos | A |
| R07.2 | **Catorze situações no disparo real** | `infra$ python3 confere-rotina.py --agendada` (conferências 11 a 13) | receberam lembrete **só** os plantados `convidado` e `em preenchimento` vencidos (A, B, C e D), com o ramo certo; reconvite só para M; nada para E a L, N e os 486 de controle; uma mensagem por destinatário — a tabela da seção 9.2 de `rotina-disparo.md` | A |
| R07.3 | **Mutação da cadência** | os 18 defeitos abaixo, um por vez, em `scripts/cadencia.py`, com o serviço `rotinas` **parado** (`docker compose stop rotinas`), porque ele monta `scripts/` e leria o defeito; rodar `infra$ python3 confere-rotina.py`; desfazer com `git checkout -- scripts/cadencia.py`; ao fim, `git status` limpo e `docker compose up -d rotinas` | **cada** defeito reprovado por ao menos uma das sete conferências de regras. Defeito que passe é furo da conferência, e vira correção da E27 | A |
| R07.4 | **O lembrete leva o ramo certo** | `infra$ python3 confere-mensagens.py --enviar` (conferência 7) | ramo de primeira resposta para `convidado`, de retomada para `em_preenchimento`, e nunca os dois | A |
| R07.5 | **Ausência de resposta ao longo de sucessivos disparos** | modo real na E26; os convidados da primeira execução que não respondem; C-06 e C-07 ao fim | cada um recebe convite e até três lembretes, em D+4, D+7 e D+14 do **seu** convite — o D+*n* é o mínimo: fim de semana e feriado adiam, e o intervalo mínimo de 3 dias se mantém —, e **nada depois do terceiro**; C-06: todo lembrete enviado tem `estado` `convidado` ou `em preenchimento`; C-07: **nenhum** lembrete enviado depois de resposta enviada, na conferência independente do registro da rotina, pela data da resposta. Tempo comprimido pela API, se usado, é declarado (P5, seção 7.2) | C, F |

**Casos negativos de R07.3.** A E21 testou 16 mutações e a E22 acrescentou duas de
fuso, mas o registro não as enumera. A matriz fixa aqui o conjunto, um defeito por
regra. A coincidência com 18 é de número: não se afirma correspondência um a um com
as da E21.

| Caso | Defeito plantado na cadência |
|---|---|
| M01 | a recusa de contato deixa de vencer a resposta enviada |
| M02 | o estado sai da marca de concluído, e não de CON1 (recusa vira respondente) |
| M03 | `lastpage = 0` lido como iniciado (abrir vira `em preenchimento`) |
| M04 | contato inválido ignorado (`emailstatus` diferente de `OK` e `OptOut` não muda o estado) |
| M05 | `validuntil` ignorado (a janela nunca expira) |
| M06 | `pendente` recebe lembrete |
| M07 | `respondente` recebe lembrete |
| M08 | D+*n* contado do lembrete anterior, e não do convite |
| M09 | D+*n* contado de data única do ciclo, e não do envio efetivo |
| M10 | intervalo mínimo de 3 dias ignorado |
| M11 | teto de três lembretes passa a quatro |
| M12 | ramo trocado: `em preenchimento` recebe o de primeira resposta |
| M13 | sábado ou feriado tratado como dia útil |
| M14 | convite antes da âncora do semestre |
| M15 | reconvite sem teto (a segunda volta a `pendente` reconvida) |
| M16 | doze meses entre convites ignorados |
| M17 | `sent` lido em hora local, e não em UTC |
| M18 | `validuntil` gravado em hora local, e não em UTC |

## 11. R08 — Registro do consentimento

**Do projeto:** aceitar o termo em acesso de amostra → aceite, data e versão
persistidos.
**Redigido contra:** [`consentimento.md`](consentimento.md) e a
[ADR-0009](../decisoes/0009-registro-do-consentimento.md). Desde a E12, o requisito
inclui o **consentimento específico do dado sensível** (CON2), que o art. 11, I da
LGPD exige "de forma específica e destacada". "Persistido" inclui recuperável: o ônus
da prova é do controlador (art. 8º, §2º).

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R08.1 | **Termo e versão na instância** | `infra$ python3 confere-consentimento.py` | 2 de 2: termo, consentimento específico, opções e encerramento da instância iguais aos de `termo.py`; o documento da página 1 **reconstruído da instância** tem o mesmo SHA-256 que `CONV` grava e que `termos/ensaio-2.html` | A |
| R08.2 | **Aceite, recusas e recusa pela mensagem** | `infra$ python3 confere-consentimento.py --exercitar` | **11 de 11**: aceite com e sem CON2, versão e momento em ISO 8601 com `+00:00`, momento intacto com a página 2, as duas recusas na tela com o ramo do encerramento, recuperável, recusa pela mensagem (abrir não registra; confirmar marca participante e base central), bloqueio neste e em outro questionário, rotina lendo cada situação, limpeza | A |
| R08.3 | **Recuperação por identificador** | para cada participante da E26 que se manifestou: `infra$ python3 consulta-consentimento.py --identificador <SIN-…>` | cada manifestação com CON1, CON2, versão e momento, e o texto da versão **conferido pelo resumo**; sem nome, endereço nem token na saída | C, F |
| R08.4 | **O momento sobrevive à conclusão** | percurso completo até o envio final (R04.2) | `CONDH` continua o momento do aceite na página 1, e `CONV` a versão aceita, depois do envio final. A E22 o conferiu até a página 2 e, para o envio final, só pela leitura do código | C |
| R08.5 | **Consentimento específico do dado sensível** | C3 (CON2 = concordo) e C7 (CON2 = não concordo), até o fim | com CON2 = concordo, a página 9 aparece e EQ1 a EQ4 ficam gravados, EQ1 a EQ3 cifrados; com CON2 = não concordo, a página 9 não aparece e EQ1 a EQ4 ficam vazios. CON2 tem o mesmo `CONDH` de CON1: um só momento para a página 1 | C |

## 12. R09 — Tratamento da recusa

**Do projeto:** acionar a manifestação de recusa → nenhum disparo posterior ao
participante.
**Redigido contra:** o P6 (seção 8 de `parametros-contato.md`),
[`conformidade.md`](conformidade.md) e a
[ADR-0010](../decisoes/0010-conformidade-no-mecanismo.md). A recusa são duas, com
efeitos distintos (E05): a **de contato** interrompe todo disparo, em todos os
ciclos, até a revogação; a **de consentimento**, só no ciclo corrente. "Nenhum
disparo posterior" vale literalmente para a primeira, e para a segunda dentro do
ciclo.

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R09.1 | **Configuração** | `infra$ python3 confere-conformidade.py` | 2 de 2: trilha ativa, lista de bloqueio nos padrões (`deleteblacklisted = N`, `allowunblacklist = N`, `blockaddingtosurveys = Y`), correção do `AuditLog` na imagem; página de recusa em português | A |
| R09.2 | **As três vias, os dois ciclos e a revogação** | `infra$ python3 confere-conformidade.py --exercitar` | **12 de 12**, inclusive: cada via registrada — tela, conclusão (CT4) e mensagem — e a recusa de consentimento; contato inválido **não** registrado como recusa; no **ciclo seguinte**, num questionário novo, a plataforma recusa convidar quem recusou contato e convida quem recusou o consentimento e quem tinha contato inválido; revogação registrada, sem novo bloqueio | A |
| R09.3 | **Recusa de contato na tela, pelo caminho real** | percurso C2 na E26 | em até 30 minutos, linha em `egressos_recusas` (`contato`, `tela`, momento de `CONDH`, versão) e base central bloqueada; o plano da rotina passa a `recusa de contato` | C |
| R09.4 | **Recusa por CT4, pela conclusão real** | percurso completo com CT4 marcado | `respondente` neste ciclo; recusa registrada com via `conclusao`; base central bloqueada. A E23 a plantou pela API | C |
| R09.5 | **Recusa pela mensagem recebida** | abrir o endereço de recusa de uma mensagem que chegou à caixa e confirmar | `emailstatus = OptOut` e `blacklisted = Y`; recusa registrada com via `mensagem` e o momento tirado da trilha da plataforma | C |
| R09.6 | **Revogação pedida de verdade** | resposta a uma mensagem, na caixa `acompanhamento`, pedindo a revogação; `infra$ python3 conformidade.py revogar --identificador <SIN-…> --registro "<pedido de dd/mm/aaaa na caixa acompanhamento>"` | pessoa livre na base central; `revogada_em` e `revogacao` preenchidos; registro na trilha; a rotina não volta a bloquear | C |
| R09.7 | **Nenhum disparo posterior** | C-08 ao fim da E26; e, para a de consentimento, C-06 restrita aos participantes com `recusa de consentimento` | **zero linhas** em C-08: nenhum convite ou lembrete enviado depois do momento de uma recusa de contato não revogada; nenhum lembrete a quem recusou o consentimento no ciclo | F |

## 13. R10 — Contato inválido

**Do projeto:** incluir endereço inexistente na base → retorno registrado e contato
marcado.
**Redigido contra:** o P8 (seção 10 de `parametros-contato.md`),
[`leitura-devolucoes.md`](leitura-devolucoes.md) e o P4, seção 6.1 (reparo). Os
endereços inexistentes já estão na base: o domínio `invalido.test` produz erro
permanente, e `indisponivel.test`, temporário. Contato inválido **não é recusa**
(P8, seção 10.2).

**Números esperados na primeira execução real.** Antes de 15/12/2026, só o 1º
semestre tem a âncora vencida: **255 convites**. Cruzamento da base regenerada,
feito nesta etapa:

| Principal | Convidados | Com alternativo entregável | Com alternativo em `invalido.test` | Sem alternativo |
|---|---|---|---|---|
| `egressos.test` | 220 | — | — | — |
| `invalido.test` (permanente) | 23 | 6 | 0 | 17 |
| `indisponivel.test` (temporário) | 12 | 6 | 1 | 5 |

| Item | Verificação | Procedimento | Resultado esperado | Momento |
|---|---|---|---|---|
| R10.1 | **O correio, isolado** | `rotinas$ python3 verifica_correio.py` | **7 de 7**: entrega, devolução permanente e temporária, nas duas direções | A |
| R10.2 | **A integração** | `infra$ python3 confere-envio.py` (questionário descartável) | **7 de 7**: a instância dispara, a devolução volta, a rotina classifica, o estado do participante muda e o contador de recusa fica em zero | A |
| R10.3 | **Erro permanente na primeira ocorrência** | primeira execução real; C-09 depois da leitura de devoluções seguinte | os **23** com principal em `invalido.test`: devolução `permanente` com `marcou = 1`, `emailstatus = invalido` e plano `contato inválido`; nenhum lembrete a eles depois (C-06) | C |
| R10.4 | **Erro temporário: o limiar de três** | os **12** de `indisponivel.test`, ao longo da cadência; C-09 depois de cada leitura de devoluções | marcados como inválidos depois da devolução da **3ª mensagem** do ciclo, que é o lembrete 2 — a intenção do P8: "exigir as três primeiras antes de declarar o contato perdido". Recebem convite, lembrete 1 e lembrete 2, e **não** o lembrete 3. Herdado da E09, que não pôde exercitá-lo. **Ver o risco abaixo** | C |
| R10.5 | **Ciclo de reparo, com teto de uma rodada** | operação de reparo da E26: trocar para o `email_alternativo` no participante, pela API, e na base central, por console | os **12** reparáveis (6 + 6) voltam a `pendente`, são **reconvidados uma vez**, com nova contagem, e a mensagem é entregue; o que tem alternativo em `invalido.test` devolve de novo e **fica** em `contato inválido` — o plano registra "teto de reparo atingido"; os 22 sem alternativo ficam na fila de correção (canal alternativo não automatizado, ADR-0003) | C |
| R10.6 | **Contato inválido não é recusa** | C-02 antes e depois das leituras de devolução da E26; R09.2, conferência 6 | nenhuma pessoa bloqueada pela leitura de devoluções; no ciclo seguinte, quem tinha contato inválido é convidado | C, A |
| R10.7 | **Sem rastreamento de abertura** | `infra$ python3 confere-mensagens.py` (conferência 3) | os modelos não têm imagem nem marcador desconhecido (P8, seção 10.3) | A |

**Risco em R10.4, achado nesta etapa por leitura do código, não observado.** O P8
conta **mensagens** devolvidas. A rotina conta **devoluções**: cada linha de
`egressos_devolucoes` é identificada pelo `Message-ID` da própria devolução
(`scripts/ler_devolucoes.py`, `interpreta`), e não pelo da mensagem original. O
correio de ensaio avisa o atraso em 1 minuto (`delay_warning_time = 1m`) e expira a
fila em 1 hora (`maximal_queue_lifetime = 1h`, `infra/correio/entrypoint.sh`). Ao
expirar, o Postfix costuma devolver `Action: failed` com o código 4.x.x da última
tentativa, que a classificação lê como **temporário**, porque o código manda
(`leitura-devolucoes.md`, seção 3). Se for assim, cada mensagem a
`indisponivel.test` produz **duas** devoluções temporárias, com `Message-ID`
distintos, e o limiar de três chega na devolução do **lembrete 1**. O contato seria
marcado depois de duas mensagens, e não de três. A E09 não viu isso porque não
esperou a expiração. **A E26 observa**: quantas devoluções cada mensagem produz e com
que código. Se for o caso, R10.4 **não atende**, e a correção — contar mensagens
originais distintas, e não devoluções — é da E27. Em implantação real o efeito
persiste, com prazos de horas e dias no lugar de minutos.

## 14. R11 — Extração dos resultados

**Do projeto:** exportar o conjunto de respostas → arquivo íntegro e estruturado.
**Redigido contra:** a exportação **nativa** da plataforma, pela API — decisão desta
etapa. A rotina de extração é da E28, e a E28 vem depois da E27, que preenche a
matriz. Por isso a E27 verifica pela exportação que a plataforma já oferece, e a E28
reexecuta o mesmo item contra a sua rotina (R11.5). "Íntegro" e "estruturado" ficam
definidos aqui, porque o projeto não os define.

**Procedimento comum (F).** Depois da E26, pela API, com o cliente de
`scripts/limesurvey_api.py`, como `consulta-consentimento.py` já faz:
`export_responses(202615, "csv", None, "all", "code", "short")`, o mesmo em `"json"`,
e `get_summary(202615)`. Os arquivos exportados ficam **fora do repositório**: são
sintéticos, mas são respostas.

| Item | Verificação | Resultado esperado | Momento |
|---|---|---|---|
| R11.1 | **Íntegro** | registros no CSV = no JSON = `COUNT(*)` de `lime_responses_202615`; `id` único; o CSV é lido com leitor estrito da RFC 4180, e toda linha tem o número de campos do cabeçalho; UTF-8 válido, com o texto acentuado de AF4 escrito na E26 devolvido igual | F |
| R11.2 | **Estruturado** | uma coluna por campo, com o **código** do campo (AF1, IDA1…) e o de subquestão quando houver, mais `CONV`, `CONDH` e os metadados da plataforma (`id`, `token`, `submitdate`, `lastpage`, `startdate`); nenhum nome `Q<qid>`; todo valor de campo fechado dentro do domínio da seção 12.3 de `blocos-instrumento.md`, ou vazio; datas em formato fixo, em UTC (a plataforma roda em UTC) | F |
| R11.3 | **Cifrados legíveis** | AF4, EQ1 a EQ3 e CT1 a CT3 saem **decifrados** — dentro do domínio, quando fechados —, enquanto o banco guarda o cifrado (VC3) | F |
| R11.4 | **Recusas e parciais distinguíveis** | recusa identificável por CON1 diferente de `CONC`, embora com `submitdate`; parcial por `submitdate` vazio; parcial órfã por `lastpage = 0` e CON1 vazio. Registrar a diferença: as completas de `get_summary` são respondentes **mais recusas** (E15) | F |
| R11.5 | **A rotina da E28** | R11.1 a R11.4 sobre o arquivo da rotina de extração, mais a VC4 | X |

## 15. R12 — Responsividade

**Do projeto:** abrir o instrumento em dispositivo móvel → instrumento utilizável sem
perda de função.
**Redigido contra:** os critérios abaixo, definidos nesta etapa. O projeto não os
define, e a E15 registrou que telas pequenas não tinham sido vistas
(`navegacao-condicional.md`, seção 11.3, item 2). **Decisão desta etapa:** emulação
de dispositivo no navegador, com a diferença para o aparelho real declarada como
ressalva. Um aparelho real exigiria publicar a porta na rede local
(`ENDERECO_BIND=0.0.0.0`), e expor o painel não se justifica para isso.

**Procedimento comum (C).** Numa cópia de ensaio
(`raiz$ python3 infra/instrumento/instrumento.py copia-de-ensaio`, que imprime os
endereços), no navegador do aplicativo, em duas emulações: **375×812** (predefinição
de celular, com agente de usuário móvel e toque) e **360×640**. Sessão nova a cada
percurso (`&newtest=Y`). Percorrer C3, o caminho mais longo, com V e os recortes de
equidade; C4, com o VI; e C1 e C2, para os encerramentos. Remover a cópia ao fim.

**O que é "sem perda de função", página a página:**

1. **sem rolagem horizontal:** `document.documentElement.scrollWidth` não passa de
   `window.innerWidth`;
2. **todo campo exibido é alcançável e operável por toque:** opção única, lista,
   múltipla escolha, texto e número;
3. **as regras dinâmicas da mesma página funcionam** (R04.3);
4. **a validação aparece junto ao campo**, e a página não avança com erro (R04.8);
5. **"Anterior", "Próximo", "Enviar" e "Retomar mais tarde" visíveis e acionáveis**,
   inclusive com o menu do tema recolhido;
6. **zoom permitido:** a página declara `width=device-width` e não impede a
   ampliação (`user-scalable=no` ausente), conforme o critério 1.4.4 da WCAG 2.2;
7. **alvo de toque de ao menos 24×24 px CSS** (WCAG 2.2, critério 2.5.8, nível AA).
   A área do rótulo conta quando aciona o controle.

| Item | Verificação | Resultado esperado | Momento |
|---|---|---|---|
| R12.1 | **As páginas do questionário** | as dez páginas e o encerramento atendem aos sete critérios nas duas emulações; falha registrada por página e por emulação | C |
| R12.2 | **Salvar e retomar no celular** | R05.1 feito na emulação: formulário de salvamento e de carregamento utilizáveis, retomada na página certa | C |
| R12.3 | **Páginas fora do questionário** | a página de confirmação da recusa — aberta pelo endereço de uma mensagem guardada por `confere-mensagens.py --enviar --guardar <dir fora do repositório>`, **sem confirmar** — e as mensagens de acesso negado de R02.3, utilizáveis e em português | C |
| R12.4 | **Retrato e paisagem** | as páginas 1, 2 e 7 também em 812×375, sem perda de função (WCAG 2.2, critério 1.3.4) | C |

## 16. Verificações complementares

Fora dos doze requisitos do projeto, e por isso fora do critério de aceite formal.
Entram porque etapas anteriores as encaminharam para cá: a contenção, pela E06; a
trilha e a cifragem, pela E23; a anonimização, pela política da E23, que a E28
aplica. A E27 as registra na mesma tabela da seção 17.

### VC1 — Contenção do disparo (critério K6 da ADR-0002)

**Característica do ambiente, e não procedimento de operação** (E06). Confere-se pelo
efeito, como `verifica-ambiente.sh` já faz para o banco. Mas a contenção que importa
está no **caminho do correio** (`infra/README.md`, "Contenção"), e esse script não
confere o correio. A VC1 confere. Momento: **A**.

| Item | Procedimento | Resultado esperado |
|---|---|---|
| VC1.1 | `docker inspect egressos-correio` e `egressos-rotinas`, redes; `docker network ls --filter name=egressos` | correio e rotinas **só** em `egressos_interna`, e ela com `internal=true` |
| VC1.2 | em `correio` e em `rotinas`: `getent hosts example.com`; `timeout 5 bash -c "</dev/tcp/1.1.1.1/53"`; no correio, também a porta 25. **Controle positivo:** a mesma sonda TCP no `limesurvey`, que está na rede externa | correio e rotinas **não** resolvem nome externo e **não** alcançam a internet, inclusive a porta 25; o LimeSurvey **alcança**. Sem o controle positivo, "não alcança" poderia ser só a sonda quebrada |
| VC1.3 | `config.php` do LimeSurvey (`emailmethod`, `emailsmtphost`) e C-10 | entrega por `smtp` a `correio:25`; nenhuma linha `email%` em `lime_settings_global` que sobreponha a configuração |
| VC1.4 | `docker compose exec correio postconf relayhost relay_domains` | `relayhost` vazio; `relay_domains` só com `indisponivel.test` |
| VC1.5 | `.env` e `infra$ python3 confere-mensagens.py` (conferência 1) | os três domínios de ensaio sob `.test`; remetente e retorno sob `.test`, com caixa própria |
| VC1.6 | R01.6 e R04.8 | endereço fora de `.test` rejeita o arquivo na entrada e barra a página no instrumento: a segunda barreira (leiaute, seção 7) |
| VC1.7 | `infra$ ./verifica-ambiente.sh` | sem falha: o banco não resolve nome externo, não alcança a internet e não publica porta |

**Sondas conferidas nesta etapa, quanto à exequibilidade:** as de VC1.1 a VC1.4 rodaram
em 09/10/2026 e deram o esperado, com o controle positivo alcançando. O registro
delas na seção 17 é da execução em A, e não deste ensaio da sonda.

### VC2 — Trilha de auditoria

Momento: **A** (configuração) e **F** (conteúdo).

| Item | Procedimento | Resultado esperado |
|---|---|---|
| VC2.1 | R09.1 | trilha ativa, com a correção na imagem |
| VC2.2 | ao fim da E26, para cada tipo de evento que ela produziu, a fonte da tabela da seção 3.4 de `conformidade.md` | cada evento com registro e data: importação (`egressos_importacoes`), execução e envio (`egressos_execucoes`, `egressos_disparos`), devolução (`egressos_devolucoes`), recusa e revogação (`egressos_recusas` e `lime_auditlog_log`, com `emailstatus` e `blacklisted` da recusa pela mensagem), higienização (`egressos_higienizacoes`), manifestação na tela (`CON1`, `CONV`, `CONDH`) |

A trilha **não é inviolável**: quem administra o banco pode alterá-la
(`conformidade.md`, seção 11). Não se verifica integridade contra o administrador.

### VC3 — Cifragem em repouso

| Item | Procedimento | Resultado esperado | Momento |
|---|---|---|---|
| VC3.1 | `confere-instrumento.py`, conferência 9 | cifrados na instância exatamente AF4, EQ1 a EQ3 e CT1 a CT3 | A |
| VC3.2 | `confere-conformidade.py --exercitar`, conferência 3 | no banco, o cifrado; na exportação, o valor | A |
| VC3.3 | numa resposta da E26 com EQ2 e AF4 preenchidos: o valor no banco e o exportado (R11.3) | no banco ≠ exportado, e o exportado é o que foi respondido | F |

### VC4 — Anonimização na extração

Momento: **X**. A anonimização nativa da plataforma não serve ao mecanismo
(ADR-0010), e a política da seção 7 de `conformidade.md` é aplicada pela rotina da
E28.

| Item | Resultado esperado no conjunto extraído |
|---|---|
| VC4.1 | **não saem:** token, `participant_id`, nome, e-mail, telefone, CT1 a CT3, `CONV`, `CONDH` |
| VC4.2 | `identificador` ausente, ou só pseudonimizado por resumo com chave guardada fora do conjunto |
| VC4.3 | AF4 ausente, ou só categorizado depois de revisão humana |
| VC4.4 | EQ1 a EQ3 e PM3 só agregados, com o tamanho mínimo de célula fixado pela E28, e EQ só de quem deu CON2 |
| VC4.5 | recusas fora dos denominadores; parciais órfãs descartadas; uma resposta concluída por participante e ciclo |

## 17. Registro dos resultados

Preenchido por quem executa — E26, E27 e E28 —, uma linha por item. O commit é o do
repositório no momento da execução, e a evidência que não couber aqui vai para a
especificação da etapa que executou, com remissão.

| Item | Momento | Executado em | Commit | Resultado obtido | Situação |
|---|---|---|---|---|---|
| R01.1 | A | | | | |
| R01.2 | A | | | | |
| R01.3 | C | | | | |
| R01.4 | C | | | | |
| R01.5 | A | | | | |
| R01.6 | A | | | | |
| R02.1 | A | | | | |
| R02.2 | A | | | | |
| R02.3 | A | | | | |
| R02.4 | A | | | | |
| R03.1 | A | | | | |
| R03.2 | C | | | | |
| R03.3 | A | | | | |
| R03.4 | C | | | | |
| R03.5 | C | | | | |
| R04.1 | A | | | | |
| R04.2 | C | | | | |
| R04.3 | C | | | | |
| R04.4 | C | | | | |
| R04.5 | C | | | | |
| R04.6 | C | | | | |
| R04.7 | C | | | | |
| R04.8 | C | | | | |
| R05.1 | C | | | | |
| R05.2 | C | | | | |
| R05.3 | C | | | | |
| R05.4 | C | | | | |
| R05.5 | C | | | | |
| R06.1 | A | | | | |
| R06.2 | A | | | | |
| R06.3 | C, F | | | | |
| R06.4 | F | | | | |
| R07.1 | A | | | | |
| R07.2 | A | | | | |
| R07.3 | A | | | | |
| R07.4 | A | | | | |
| R07.5 | C, F | | | | |
| R08.1 | A | | | | |
| R08.2 | A | | | | |
| R08.3 | C, F | | | | |
| R08.4 | C | | | | |
| R08.5 | C | | | | |
| R09.1 | A | | | | |
| R09.2 | A | | | | |
| R09.3 | C | | | | |
| R09.4 | C | | | | |
| R09.5 | C | | | | |
| R09.6 | C | | | | |
| R09.7 | F | | | | |
| R10.1 | A | | | | |
| R10.2 | A | | | | |
| R10.3 | C | | | | |
| R10.4 | C | | | | |
| R10.5 | C | | | | |
| R10.6 | C, A | | | | |
| R10.7 | A | | | | |
| R11.1 | F | | | | |
| R11.2 | F | | | | |
| R11.3 | F | | | | |
| R11.4 | F | | | | |
| R11.5 | X | | | | |
| R12.1 | C | | | | |
| R12.2 | C | | | | |
| R12.3 | C | | | | |
| R12.4 | C | | | | |
| VC1.1–VC1.7 | A | | | | |
| VC2.1 | A | | | | |
| VC2.2 | F | | | | |
| VC3.1–VC3.2 | A | | | | |
| VC3.3 | F | | | | |
| VC4.1–VC4.5 | X | | | | |

**Situação por requisito** — pela regra da seção 2.4, ao fim da E27 (e da E28, para
R11):

| Req. | Situação | Itens que a decidem |
|---|---|---|
| R01 | | |
| R02 | | |
| R03 | | |
| R04 | | |
| R05 | | |
| R06 | | |
| R07 | | |
| R08 | | |
| R09 | | |
| R10 | | |
| R11 | | |
| R12 | | |

## 18. Verificação do critério de conclusão

*Critério da E25: os doze requisitos do projeto contemplados.* **Atendido.**

**Nas duas direções.**

- **Todo requisito do projeto tem item.** As doze linhas da matriz do projeto,
  conferidas contra o documento (Fase 6), estão nas seções 4 a 15, com a redação dele
  na primeira linha. Cada uma tem ao menos um item com procedimento e resultado
  esperado: **12 de 12**, com 65 itens no total, mais 4 verificações complementares.
- **Todo encaminhamento das etapas anteriores tem item.** Cada nota "Vindo da E*nn*"
  da E25 em `ETAPAS.md`, e cada ponto "E25" das especificações:

| Origem | O que pediu | Onde está |
|---|---|---|
| E06, ADR-0002 | contenção do disparo como característica do ambiente | VC1 |
| E05, P5 seção 15 | seletividade, recusa e contato inválido contra a máquina de estados | R07, R09, R10 |
| E05, P3 seção 5.2 | seletividade como item da matriz, e não taxa de resposta | R07; seção 1 |
| E09 | contato inválido contra os dois verificadores | R10.1, R10.2 |
| E11 | arquivos inválidos de propósito, um por regra | R01.5 (N01–N31) |
| E11 | rejeição de endereço fora de `.test` como contenção | R01.6, VC1.6 |
| E12 | consentimento específico do dado sensível | R08.5 |
| E12 | navegação contra os públicos dos blocos | R04.2 |
| E13 | correção com preservação do original | R03.4, R03.5 |
| E13 | regras de campo da seção 12.10 | R04.3, R04.4, R04.5 |
| E14 | os dez caminhos | R04.1, R04.2 |
| E14 | retomada como salvar, fechar e carregar com nome e senha | R05.1 |
| E15 | `confere-instrumento.py` como procedimento da estrutura | R04.1, R03.1, VC3.1 |
| E16 | sete defeitos como ponto de partida; faltavam os de arquivo; CPF construído | N08, N10, N17, N18, N21, N26, N28; N01–N07 |
| E17 | 27 casos do validador | R01.5 |
| E17 | reimportação idempotente; recusa preservada | R01.2; R01.4 |
| E19 | conferência de unicidade e os 15 defeitos | R02.1; R02.4 (U01–U15) |
| E21 | `--agendada`, `--perdida`, mutações da cadência | R06.1, R07.2; R06.2; R07.3 (M01–M18) |
| E22 | `confere-consentimento.py` e `consulta-consentimento.py`; estrutural com oito | R08.1–R08.3; R04.1 |
| E23 | recusa, trilha, cifragem e ciclo seguinte; estrutural com nove | R09.1–R09.2; VC2; VC3; R04.1 |
| ADR-0003 | **não** incluir envio por mensagem instantânea | seção 19, item 1 |
| linha de base | Indicador 3.7 do INEP como critério externo | seção 1 |
| fichamentos de Davis e Silva | contraste com a avaliação por percepção | seção 1 |

**Exequibilidade conferida, sem preencher resultado.** Para que a matriz seja
executável, e não só escrita, conferiu-se nesta etapa, só leitura:

- **toda linha de comando** contra as opções que cada script de fato aceita;
- **as consultas do Apêndice A** contra o banco vivo — sintaxe e conversão de fuso;
- **o gerador:** a base regenerada tem o mesmo SHA-256 das importações nº 10, 11 e 12
  e dá, no validador, os valores esperados de R01;
- **as sondas de contenção** da VC1, com o controle positivo.

Nenhum item foi executado como verificação. A seção 17 está vazia de propósito: os
resultados são da E26 em diante.

## 19. O que fica fora da matriz, e por quê

1. **Envio por mensagem instantânea.** Não há automação a exercitar
   ([ADR-0003](../decisoes/0003-canal-alternativo-nao-automatizado.md)).
2. **Taxa de resposta.** Sem aplicação real, não há como verificar. O que se verifica
   é a capacidade instalada de cobrança sistemática (R06, R07, R09, R10).
3. **Aceitação por pessoas.** R12 é funcional, e não percepção de uso.
4. **A eliminação por prazo.** A política está escrita (`conformidade.md`, seção 8);
   os anos e a rotina são da instituição e da E30.
5. **Um reinício real do Windows** e **a regra dos doze meses entre ciclos em dois
   ciclos reais.** O primeiro é condição do hospedeiro (`rotina-disparo.md`, seção
   11); o segundo é conferido pelas regras (M16) e pelo ciclo seguinte de R09.2.
6. **Outros motores de navegador**, como o do Safari. A emulação de R12 usa o motor do
   navegador do aplicativo.

## 20. O que esta matriz não permite afirmar

1. **Que o mecanismo eleva a taxa de resposta.** Atender R07 mostra que o lembrete
   vai a quem deve; não, que ele faz alguém responder.
2. **Nada sobre egressos.** Os números produzidos na simulação são de base sintética,
   e não comportam interpretação substantiva.
3. **Que uma conferência que passa está certa.** Os casos negativos e o controle
   positivo reduzem o risco de a conferência reproduzir a premissa do que confere
   (E21, E22), mas não o eliminam. Defeito que passe por um caso negativo é achado, e
   não ruído.
4. **Que a emulação é o aparelho.** Teclado virtual sobre o campo, toque real e motor
   de outro navegador ficam fora de R12, como ressalva.
5. **Conformidade legal.** A matriz verifica requisitos de projeto. O termo é de
   ensaio, pendente de validação do encarregado de dados do IFSP, e a base legal é
   escolha do projeto (consentimento), e não conclusão da lei.
6. **Homologação para uso real.** É critério de aceite de uma prova de conceito.
   Qualquer aplicação junto a egressos reais exige apreciação ética prévia, como o
   documento do projeto registra na Fase 7.

## 21. O que determina para as etapas seguintes

- **E26 (cenários)** — abrir pela ordem da seção 2.1: VC1, R01.5 e R01.6, R01.1 e
  R01.2 (reimplantação do 202615, ainda sem resposta nem envio), e a bateria A;
  **só então** ligar o modo real. Implementar a operação de reparo de contato, de que
  dependem R01.3 e R10.5. Com o modo real, os números da seção 13 são o esperado da
  primeira execução: 255 convites; 23 permanentes; 12 temporários; 12 reparáveis.
  **Hospedeiro ligado às 10:00 em dia útil** — achado da seção 2.2 —, e 12/10 é
  feriado. Cada cenário do entregável da E26 alimenta itens já previstos aqui:
  preenchimento parcial com retomada (R05), ausência de resposta (R07.5), contato
  inválido (R10.3 a R10.5) e recusa (R09.3 a R09.6). Observar quantas devoluções
  cada mensagem a `indisponivel.test` produz, e com que código — o risco de R10.4.
  A reimplantação de R01.1 precisa de autorização, como nas E22 e E23.
- **E27 (registro)** — preencher a seção 17 e a situação por requisito; corrigir e
  reexecutar o que não atender. Para reexecutar a bateria A depois da E26, ajustar as
  limpezas de `confere-rotina.py`, `confere-consentimento.py` e
  `confere-conformidade.py` para comparar com o estado anterior, e não com zero
  (seção 2.1). Se o risco de R10.4 se confirmar, contar mensagens originais distintas
  no limiar do erro temporário.
- **E28 (extração)** — R11.5 e VC4; a fila de revisão de R03.4 como rotina.
- **E30 (guia)** — a carga do zero (`docker compose down -v`), na variante que a E26
  não faz, entra no teste de replicação; incorporar as sondas de contenção do correio
  da VC1 a `verifica-ambiente.sh`, que hoje só confere o banco; o guia remete a esta
  matriz como critério de aceite.
- **E31 (relatório final)** — a matriz como critério de aceite; o contraste com a
  avaliação por percepção (seção 1); e a seção 20.

## Apêndice A — Consultas

Só leitura. Todas pelo cliente do contêiner do banco, a partir de `infra/`, com a
senha lida do ambiente do próprio contêiner:

```bash
docker compose exec -T banco sh -c \
  'mariadb --skip-ssl -B -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"' \
  < consulta.sql
```

`consulta.sql` é um arquivo fora do repositório com a consulta. Datas:
`egressos_execucoes` e `egressos_disparos` estão em hora local (America/Sao_Paulo,
`-03:00`); as respostas, em UTC; `egressos_recusas.manifestada_em` é ISO 8601 com o
fuso. A sintaxe de todas foi conferida contra o banco em 09/10/2026, sem dados da E26.

**C-01 — impressão digital dos participantes e da base central** (R01.2, R01.6)

```sql
SELECT COUNT(*) AS n, MD5(GROUP_CONCAT(CONCAT_WS('|', tid, participant_id, token,
       email, emailstatus, blacklisted, attribute_1, attribute_2, attribute_3,
       attribute_4, attribute_5, attribute_6) ORDER BY tid SEPARATOR '\n')) AS digital
  FROM lime_tokens_202615;
SELECT COUNT(*) AS n, MD5(GROUP_CONCAT(CONCAT_WS('|', participant_id, firstname,
       lastname, email, blacklisted) ORDER BY participant_id SEPARATOR '\n')) AS digital
  FROM lime_participants;
```

**C-02 — pessoas bloqueadas na base central** (R01.4, R10.6)

```sql
SELECT participant_id FROM lime_participants WHERE blacklisted = 'Y' ORDER BY 1;
```

**C-03 — execuções agendadas de disparo no período** (R06.3)

```sql
SELECT DATE(previsto_para) AS dia, situacao, modo,
       TIMESTAMPDIFF(SECOND, previsto_para, iniciado_em) AS atraso_s
  FROM egressos_execucoes
 WHERE tarefa = 'disparo' AND origem = 'agendada'
   AND previsto_para BETWEEN '<início da E26>' AND '<fim da E26>'
 ORDER BY previsto_para;
```

**C-04 — nenhuma execução agendada em fim de semana** (R06.3; os feriados, conferidos
contra `agenda.json`)

```sql
SELECT COUNT(*) AS fora_de_dia_util FROM egressos_execucoes
 WHERE tarefa = 'disparo' AND origem = 'agendada' AND WEEKDAY(previsto_para) >= 5;
```

**C-05 — as tarefas a intervalos** (R06.4)

```sql
SELECT tarefa, DATE(previsto_para) AS dia, COUNT(*) AS execucoes,
       SUM(situacao = 'concluida') AS concluidas
  FROM egressos_execucoes
 WHERE tarefa IN ('devolucoes', 'conformidade')
   AND previsto_para BETWEEN '<início da E26>' AND '<fim da E26>'
 GROUP BY tarefa, DATE(previsto_para) ORDER BY dia, tarefa;
```

**C-06 — lembretes só a quem estava `convidado` ou `em preenchimento`** (R05.4,
R07.5, R09.7, R10.3)

```sql
SELECT estado, COUNT(*) AS n FROM egressos_disparos
 WHERE questionario = 202615 AND tipo = 'lembrete' AND resultado = 'enviado'
 GROUP BY estado;
```

**C-07 — nenhum lembrete depois de resposta enviada**, conferido pela data da
resposta, e não pelo estado que a rotina registrou (R07.5). Esperado: zero linhas.

```sql
SELECT d.tid, d.numero, d.registrado_em, r.submitdate
  FROM egressos_disparos d
  JOIN lime_tokens_202615 t ON t.tid = d.tid
  JOIN lime_responses_202615 r ON r.token = t.token AND r.submitdate IS NOT NULL
 WHERE d.questionario = 202615 AND d.tipo = 'lembrete' AND d.resultado = 'enviado'
   AND d.registrado_em > CONVERT_TZ(r.submitdate, '+00:00', '-03:00');
```

**C-08 — nenhum disparo depois de recusa de contato não revogada** (R09.7). Esperado:
zero linhas.

```sql
SELECT r.tid, r.via, r.manifestada_em, d.tipo, d.numero, d.registrado_em
  FROM egressos_recusas r
  JOIN egressos_disparos d
    ON d.questionario = r.questionario AND d.tid = r.tid AND d.resultado = 'enviado'
 WHERE r.tipo = 'contato' AND r.revogada_em IS NULL
   AND d.registrado_em > CONVERT_TZ(STR_TO_DATE(LEFT(r.manifestada_em, 19),
                                                '%Y-%m-%dT%H:%i:%s'),
                                    '+00:00', '-03:00');
```

**C-09 — devoluções e marcação** (R10.3, R10.4)

```sql
SELECT ciclo, questionario, tipo, marcou, COUNT(*) AS n
  FROM egressos_devolucoes GROUP BY ciclo, questionario, tipo, marcou;
SELECT emailstatus, COUNT(*) AS n FROM lime_tokens_202615 GROUP BY emailstatus;
```

**C-10 — nenhuma configuração de correio no banco que sobreponha o `config.php`**
(VC1.3). Esperado: zero linhas.

```sql
SELECT stg_name, stg_value FROM lime_settings_global WHERE stg_name LIKE 'email%';
```

A conversão de fuso usa deslocamento fixo (`-03:00`): o Brasil não tem horário de
verão desde 2019, e o banco não tem as tabelas de fuso por nome carregadas. Se a
E26 cruzar mudança de regra de fuso, a consulta precisa mudar.
