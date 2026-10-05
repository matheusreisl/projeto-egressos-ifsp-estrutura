# Instrumento

A estrutura do questionário implantada na instância, e o que a produz.

**Etapa:** E15 — implementar a estrutura no LimeSurvey
**Data:** 03/10/2026
**Decorre de:** [`blocos-instrumento.md`](../../docs/especificacao/blocos-instrumento.md)
(E12 e E13) e [`navegacao-condicional.md`](../../docs/especificacao/navegacao-condicional.md)
(E14)

O instrumento é o questionário **202615** da instância: onze grupos, um por bloco,
35 campos, inativo e sem participantes. A ativação e o acesso controlado são da E17.

**Estrutura, e não conteúdo.** Cada enunciado é um marcador que nomeia o campo e o
dado — `[AF1] satisfação com a formação recebida no IFSP` — seguido de "Enunciado a
definir pelo projeto correlato". O texto das perguntas não é deste projeto
(CLAUDE.md, decisão 5). Os domínios de resposta são estrutura e entram completos.

**O termo de consentimento e o encerramento são** (E22): texto informativo da LGPD,
e não conteúdo temático. Estão em `termo.py`, numa **versão de ensaio** sujeita à
validação do encarregado de dados do IFSP — decisão confirmada com o orientando.

## O que há aqui

| Arquivo | Papel |
|---|---|
| `instrumento.lss` | **a estrutura exportada da instância** — o artefato versionado |
| `estrutura.py` | a especificação das E12 a E14 transcrita em dados: grupos, campos, domínios, regras de exibição |
| `mensagens.py` | convite e lembrete, remetente, retorno e assuntos (E20) |
| `termo.py` | termo de consentimento, consentimento específico, encerramento e a versão gravada em cada resposta (E22) |
| `termos/<versão>.html` | o documento da página 1 de cada versão do termo, **imutável** — a prova do texto que cada resposta aceitou (E22) |
| `instrumento.py` | gera o `.lss`, implanta, exporta, cria e remove cópias de ensaio, e prepara o acesso controlado (E17) |
| `comandos/ExportarestruturaCommand.php` | comando de console que exporta o `.lss` |
| `comandos/PrepararbasecentralCommand.php` | cria os atributos da base central, os de contato cifrados (E17) |
| `comandos/ImportarbasecentralCommand.php` | grava a importação na base central, decifrando para aplicar a precedência (E17) |
| `comandos/RegistrarimportacaoCommand.php` | registra cada importação na trilha `egressos_importacoes` (E17) |
| `comandos/CompletaratributosCommand.php` | acrescenta coluna de atributo do participante a instrumento já ativo e esvazia o cache de esquema (E20) |
| `comandos/AtivarauditoriaCommand.php` | ativa o plugin `AuditLog` como o painel faz, sem tela (E23) |
| `comandos/RevogarrecusaCommand.php` | revoga a recusa de contato de uma pessoa pelos modelos da plataforma, com trilha (E23) |
| `configuracao/cursos.csv` | lista de cursos, com o nível de cada um |
| `configuracao/unidades.csv` | lista de unidades, com as antecessoras |
| `configuracao/faixas-rendimento.csv` | as cinco faixas do Anexo I |
| `configuracao/parametros.json` | versão da configuração, limite inferior do ano e fontes |

A conferência fica fora desta pasta, junto das outras:
[`../confere-instrumento.py`](../confere-instrumento.py).

## Procedimento

A partir de `infra/`, com a composição de pé:

```bash
python3 instrumento/instrumento.py implantar
python3 confere-instrumento.py
```

O primeiro gera o `.lss` a partir de `estrutura.py` e de `configuracao/`, importa-o
pela API com o sid fixo 202615 e exporta de volta o que a instância guardou para
`instrumento/instrumento.lss`. Recusa se o questionário já existir; com
`--substituir`, recria o **inativo** — ou o **ativo que não tenha nenhuma resposta
nem envio** (E22).

**Mudar a estrutura de um instrumento ativo é recriá-lo.** A plataforma recusa
acrescentar ou remover questão e grupo em questionário ativo ("Survey is active and
not editable" — conferido no código da API). Recriar apaga a tabela de
participantes junto, e por isso só se admite quando não há nada a perder: o
`implantar` confere, antes, que não há resposta — completa, incompleta ou salva — nem
participante com envio ou conclusão. Depois, a ordem é a de sempre: `preparar-
participantes`, a importação — que reencontra cada pessoa na base central e cria
participantes com tokens novos — e `ativar`. A base sintética é regenerada pelo
gerador, com a mesma semente, porque a importação elimina o arquivo. Feito assim na
E22, para acrescentar os metadados do consentimento.

O segundo confere o instrumento contra a especificação (seção "Verificação").

**Por que o arquivo versionado é a exportação, e não o que o gerador produz.** A
exportação é o que a instância de fato guardou, depois de interpretar o arquivo.
Quem replicar pode importá-la diretamente, pela tela ou pela API, sem o gerador:

```bash
python3 instrumento/instrumento.py exportar --sid 202615 --saida /tmp/x.lss
```

**Por que o comando de console.** A API RemoteControl do LimeSurvey 7 importa
`.lss` e **não exporta** — conferido contra a lista de métodos da instância. A
exportação pela tela contraria o critério K7 da
[ADR-0002](../../docs/decisoes/0002-ambiente-execucao.md). O console carrega comandos
adicionais do diretório indicado em `YII_CONSOLE_COMMANDS`; o comando daqui chama
`surveyGetXMLData`, a mesma função do botão de exportação do painel. O
`instrumento.py` copia o arquivo para o contêiner a cada exportação, de modo que a
imagem não muda.

### Cópia de ensaio

Percorrer o questionário exige que ele esteja ativo e tenha participantes, e as duas
coisas são da E17. As conferências usam uma **cópia descartável**:

```bash
python3 instrumento/instrumento.py copia-de-ensaio
python3 instrumento/instrumento.py remover --sid <sid da cópia>
```

A cópia é o mesmo `.lss` com outro sid, com acesso fechado, ativada, e com doze
participantes sintéticos sob `.test`. O comando imprime os endereços individuais.
`remover` recusa o sid do instrumento.

### Acesso controlado (E17)

```bash
python3 instrumento/instrumento.py preparar-participantes
```

Cria os atributos da base central — os de contato **cifrados**, como a plataforma
já cifra nome e e-mail —, fecha o acesso do instrumento e cria a sua tabela de
participantes, com seis atributos nomeados: identificador, curso, nível, campus,
ano e semestre de conclusão. **Não ativa** o questionário: a ativação trava a
estrutura, e a E18 ainda configura o pré-preenchimento. Idempotente; recusa trocar
a marca de cifragem de um atributo que já tem valores. A importação que vem depois
está em
[`docs/especificacao/importacao-base.md`](../../docs/especificacao/importacao-base.md).

**O `instrumento.lss` versionado é o de antes da preparação**, com acesso aberto. A
preparação muda duas propriedades do questionário — o modo de acesso e a descrição
dos atributos —, e não a estrutura de grupos e questões; reproduz-se pelo comando,
e não pelo arquivo.

### Pré-preenchimento e ativação (E18)

IDA1, IDA3, IDA4 e IDA5 têm valor padrão igual ao atributo do participante
(`{TOKEN:ATTRIBUTE_n}`), declarado em `estrutura.py` pelo campo `pre_preenchido`. O
número do atributo sai da ordem de `ATRIBUTOS_QUESTIONARIO` — a mesma que a
preparação usa para criar as colunas —, e a conferência 7 de
`confere-instrumento.py` verifica a ligação pela descrição de cada atributo.

```bash
python3 instrumento/instrumento.py ativar
```

Ativa o instrumento, **por último**: a ativação trava a estrutura. Recusa sem acesso
fechado ou sem participantes. A ordem completa, do zero, é implantar,
`preparar-participantes`, a importação (`scripts/importar_base.py`) e `ativar` —
detalhada em
[`docs/especificacao/pre-preenchimento.md`](../../docs/especificacao/pre-preenchimento.md).

### Modelos de mensagem (E20)

Convite e lembrete, remetente e retorno estão em `mensagens.py`, e vão no `.lss`
gerado. Para o instrumento já ativo:

```bash
python3 instrumento/instrumento.py aplicar-mensagens
python3 confere-mensagens.py            # só leitura
python3 confere-mensagens.py --enviar   # convite e lembretes de teste, desfeitos
```

O lembrete tem dois ramos, escolhidos pelo atributo `variante_lembrete`
(`attribute_7`), que a rotina grava antes de cada disparo. Num instrumento ativo,
a coluna é acrescentada pelo comando de console `completaratributos`, que também
esvazia o cache de esquema da web. Detalhes em
[`docs/especificacao/modelos-mensagem.md`](../../docs/especificacao/modelos-mensagem.md).

### Consentimento (E22)

A página 1 leva o termo (enunciado de CON1), o consentimento específico do dado
sensível (enunciado de CON2) e duas **equações ocultas**, que ninguém preenche e que
a plataforma calcula ao receber a página:

| Metadado | Grava |
|---|---|
| `CONV` | `ensaio-1 sha256:<resumo>` — a versão e o resumo do documento da página 1 |
| `CONDH` | o momento da manifestação, `date('c')`, em UTC com `+00:00` explícito |

Ao gerar o `.lss`, o documento da página 1 — termo, opções de CON1, texto e opções
de CON2 — é **arquivado** em `termos/<versão>.html`. Se o arquivo da versão já
existir com outro texto, o gerador **recusa**: mudar o termo exige versão nova em
`termo.py`, e o arquivo de uma versão não se reescreve. O `.gitattributes` fixa LF
nesses arquivos, para que o resumo confira em qualquer cópia.

```bash
python3 confere-consentimento.py                  # termo e versão na instância
python3 confere-consentimento.py --exercitar      # aceite, recusas e recusa pela mensagem, desfeitos
python3 consulta-consentimento.py --identificador SIN-000001
```

Especificação em
[`docs/especificacao/consentimento.md`](../../docs/especificacao/consentimento.md).

O termo em vigor é o `ensaio-2` (E23), com a guarda por princípio e a cifragem; o
arquivo do `ensaio-1` continua em `termos/`, intacto.

### Cifragem em repouso (E23)

AF4, EQ1 a EQ3 e CT1 a CT3 têm `cifrado` em `estrutura.py` e vão com `encrypted =
Y`: a plataforma grava a resposta cifrada, com a mesma chave que já cifra a base
central, e a exportação pela API a devolve decifrada. As colunas desses campos passam
a ser `text`. A lista está na tabela "Cifrado" da seção 12.3 de
`blocos-instrumento.md`, e a conferência 9 a compara com a instância. Mudar a
cifragem é mudar estrutura: exige reimplantar, como na E22.

## Da especificação para a plataforma

| Tipo da especificação | Tipo da plataforma | Onde |
|---|---|---|
| escolha única | lista, botões de opção (`L`) | a maioria |
| escolha única de domínio longo | lista suspensa (`!`) | IDA1, IDA3 |
| escala de 1 a 10 | lista com as opções `1` a `10` | AF1, AF3, PM2, PM4, PM5; AV1 e EQ4 com `NC` |
| escolha múltipla | múltipla escolha (`M`) | EF4, com `NEN` exclusivo |
| caixa de marcação | múltipla escolha com uma opção | CT4, gravado como `CT4_RECT = Y` |
| número inteiro | numérico, só inteiros (`N`) | IDA4, de 1909 a `date('Y')` |
| texto livre | texto longo (`T`), até 1.000 caracteres | AF4 |
| texto com validação | texto curto (`S`) com expressão regular | CT1 a CT3 |
| derivado do curso | equação (`*`) | IDA2 |
| metadado do consentimento | equação oculta (`*`, `hidden`), sempre relevante | CONV, CONDH (E22) |

**Códigos.** Os 35 códigos de campo da E13 foram aceitos como estão. Os códigos de
opção têm **no máximo cinco caracteres** — é o tamanho de `lime_answers.code` na
instância (`varchar(5)`) — e são mnemônicos:

| Campo | Códigos |
|---|---|
| CON1 | `CONC` concordo · `RCONS` não concordo neste ciclo · `RCONT` não quero mais ser contatado |
| CON2 | `CONC` · `NCONC` |
| IDA1 | o código do curso, cuja primeira letra é o nível: `T`, `G` ou `P` |
| IDA2 | `tecnico` · `graduacao` · `pos_graduacao` — os valores da E11 |
| IDA3 | a sigla oficial do campus (`SPO`, `CMP`…) ou `EIETS`, `ETFSP`, `CEFET` |
| IDA5 | `1` · `2` |
| AF2 | `MEL` · `IGU` · `PIO` |
| AP1 | `S` · `N` |
| AP2, SA2 | `ACC` com carteira · `ASC` sem carteira · `PUB` · `AUT` · `MICR` · `AGR` · `ESTR` estágio remunerado · `ESTN` estágio não remunerado · `FAMN` negócio familiar sem remuneração |
| SA1 | `EST` · `TRA` · `ETR` · `NEN` |
| EF1 | `CON` · `MAT` · `NAO` |
| EF2 | `IFSP` · `OUT` |
| EF3, PM1 | `TOT` · `PAR` · `NAO` · `NS` |
| EF4 | `TEC` · `GRA` · `ESP` · `MD` · `EXT` · `NEN` |
| PM3 | `F1` a `F5` |
| PM6 | `IND` · `COM` · `TRA` · `CON` · `AGR` · `SOC` · `FIN` · `UTI` · `SER` · `OUT` |
| MI1 | `EST` · `SAL` · `OFE` · `ARE` · `QUA` · `EXP` · `PES` · `OUT` |
| AV1, EQ4 | `1` a `10` · `NC` |
| EQ1 | `MUL` · `HOM` · `NB` · `OUT` · `PND` |
| EQ2 | `PRE` · `PAR` · `IND` · `AMA` · `BRA` · `PND` |
| EQ3 | `S` · `N` · `PND` |

**O nível vem do código do curso.** IDA2 é a equação
`{if(substr(IDA1, 0, 1) == 'T', 'tecnico', …)}`, calculada na própria página 2, à
medida que o curso muda (E18). O gerador recusa curso cujo prefixo não bata com a
coluna `nivel` da configuração.

## Configurações do questionário

| Configuração | Valor | Por quê |
|---|---|---|
| formato | um grupo por página | E14, decisão 1 |
| voltar | permitido | E14, decisão 2 |
| salvar e retomar | ligado | E14, decisão 3 |
| retomada pelo endereço individual (`tokenanswerspersistence`) | **desligada** | E14, seção 7.3: a retomada é por nome e senha |
| captcha | nenhum | não há tela pública; o acesso é por endereço individual |
| respostas anônimas | **não** | o estado do participante sai de CON1, ligado ao token (E14, seção 4); a anonimização é da E23 |
| data das respostas | registrada | data e hora da manifestação (P6) |
| endereço IP, URL de origem, tempos | não registrados | sem consumidor |
| página de boas-vindas | não | o consentimento é a primeira página |
| índice de perguntas | não | não se salta página — as regras de exibição se aplicam em sequência |
| opção "sem resposta" | não | o domínio é exatamente o especificado; campo opcional fica em branco |
| nome do bloco | exibido, sem descrição | o bloco é a unidade da página |
| aviso de política do questionário | não | o consentimento é grupo próprio (E22) |
| confirmação por mensagem | não | mensagens são da E20 |
| leitura de devoluções nativa | não | rotina própria (E09) |
| modo de acesso | aberto | o acesso controlado é da E17 |

## Configuração versionada

- **Unidades** — os 57 campi da página oficial do IFSP, consultada em 03/10/2026, com
  a sigla oficial como código. Dois nomes foram normalizados: "Hortôlandia" para
  Hortolândia e "Jaçana" para Jaçanã, grafias que o próprio endereço da página usa
  ou que a toponímia confirma. Mais as três antecessoras da questão 4 do instrumento
  documentado, conforme registradas na E13. A lista inclui campi em implantação, que
  não têm egressos ainda: são unidades oficiais, e o domínio é o da instituição.
- **Cursos** — **lista ilustrativa** de treze cursos, cinco técnicos, cinco de
  graduação e três de pós-graduação, para exercitar os três níveis. **Não é o
  catálogo do IFSP** e precisa ser substituída pela instituição, mantendo a regra do
  prefixo.
- **Faixas de rendimento** — as do Anexo I da Portaria Normativa nº 128/2025. Os
  valores em reais envelhecem: a cada ciclo, atualizar `faixas-rendimento.csv` e a
  `versao_configuracao` de `parametros.json`, e reimplantar.
- **Ano de conclusão mínimo** — 1909, o ano do Decreto nº 7.566, que criou as
  Escolas de Aprendizes Artífices, origem do IFSP. É barreira contra erro de
  digitação, e não domínio. O máximo é o ano corrente, calculado no preenchimento.

## Modo de ensaio

As restrições da seção 7 do leiaute valem também no questionário:

- CT1 e CT2 aceitam só endereço sob `.test`;
- CT3 aceita só `+55` com código de área terminado em 0.

As duas expressões estão em `estrutura.py`, `VALIDACOES`. **Numa implantação real,
as duas mudam**, e esse é um ponto do guia (E30).

## Armadilhas encontradas

Todas falham sem erro aparente.

1. **Expressão de exibição que cita questão oculta vale falso.** O Expression
   Manager, antes de avaliar, confere todas as variáveis citadas (`GetVarsUsed`, em
   `em_core_helper.php`) e, se alguma estiver oculta e sem o sufixo `.NAOK`,
   devolve falso. A primeira versão do Bloco VI — `não R`, com SA2 dentro de R —
   **sumia** para quem só estuda, justamente quem deve vê-lo, porque nesse caso SA2
   está oculto. Corrigido com `SA2.NAOK`. Onde a cascata é desejada — EF2 e EF3
   ocultos quando EF1 está oculto —, a regra trabalha a favor, e o sufixo não entra.
2. **A equação é texto, e não expressão.** Sem chaves, o atributo `equation` grava
   literalmente `if(substr(IDA1, …`, e o Bloco IV nunca reconhece técnico nem
   graduação. Precisa de `{…}`. Achado no percurso, e não na leitura da API: a
   conferência estrutural avaliava a equação como expressão e não o acusou. Ela foi
   corrigida para reproduzir o comportamento da plataforma.
3. **As colunas de resposta chamam-se `Q<qid>`**, e `Q<qid>_S<sqid>` nas
   subquestões — e não `<sid>X<gid>X<qid>`, nem o código da questão. Consulta direta
   a `lime_responses_<sid>` precisa traduzir pelo `lime_questions`. Vale para a E28.
4. **IDA4 é gravado como decimal** — `2020.0000000000`. A extração converte.
5. **A opção exclusiva desmarca as demais e as trava** enquanto marcada. Para
   escolher outra, o respondente desmarca "nenhuma" primeiro.
6. **Duas sessões no mesmo navegador colidem.** Abrir o endereço de um participante
   com o preenchimento de outro em curso dá "código de acesso incompatível". No
   ensaio, `&newtest=Y` inicia sessão nova. Para o egresso, que usa o próprio
   navegador, não se aplica.
7. **Sem JavaScript, o envio precisa dos campos de relevância** (E21, E22).
   `relevance<qid>` e `relevanceG<n>` vêm no formulário com aspas simples, e o script
   da página os atualiza conforme as respostas. Ausentes, a plataforma descarta a
   resposta em silêncio; com CON2 marcado como irrelevante, a página não avança.
   Quem conduzir o preenchimento por HTTP precisa enviá-los como o navegador faria.
8. **Os qids mudam a cada reimplantação** (E22). Toda referência a `Q<qid>` em
   script tem de ser lida da instância pelo código da questão. A conferência da E21,
   com `Q676` escrito, quebrou na primeira execução depois da reimplantação; e
   `add_response` descarta **em silêncio** a chave que não é coluna.
9. **A plataforma roda em UTC** (E22). O LimeSurvey fixa o fuso do PHP em UTC em
   `application/config/internal.php`, qualquer que seja o `date.timezone` da imagem
   — que o `php -r` mostra, mas a aplicação não usa. Toda data da plataforma está em
   UTC: envio, lembrete, `validuntil`, datas da resposta e o `date()` das equações.

## Verificação

`confere-instrumento.py` lê a especificação **direto dos documentos** — a seção 12.3
de `blocos-instrumento.md` e as seções 2 e 5 de `navegacao-condicional.md` — e não de
`estrutura.py`, para que um erro de transcrição no gerador apareça como divergência
em vez de se confirmar a si mesmo. Nove conferências:

1. os onze grupos, na ordem da E14;
2. os 35 campos: código, grupo, tipo, obrigatoriedade e domínio, opção por opção
   pelo rótulo;
3. as listas de configuração contra `configuracao/`;
4. o nível derivado de cada curso;
5. as validações de contato contra vinte exemplos;
6. os dez caminhos, **avaliando as expressões que estão na instância** sobre as
   2.802 combinações da seção 8 da E14, com a regra do item 1 das armadilhas;
7. o pré-preenchimento (E18): cada campo da identificação aponta para o atributo
   do participante que tem o seu nome, derivado do texto da especificação;
8. os metadados do consentimento (E22), lidos da tabela "Metadado" da seção 12.3:
   equações ocultas do grupo do consentimento, sempre relevantes e não obrigatórias;
9. a cifragem em repouso (E23), lida da tabela "Cifrado" da seção 12.3: cifrados
   na instância exatamente os campos listados.

**Resultado: 6 de 6 na E15; 7 de 7 desde a E18; 8 de 8 desde a E22; 9 de 9 desde a
E23** — a nona também falhou antes da reimplantação e passou depois. A sétima
falhou antes da reimplantação com os padrões, apontando os quatro que faltavam, e
passou depois; a oitava, do mesmo modo, falhou antes da reimplantação da E22
("CONV: ausente; CONDH: ausente") e passou depois. A
conferência foi ela mesma testada por mutação, e reprova
as cinco versões defeituosas que lhe foram apresentadas: sem `.NAOK` (280
combinações sem caminho), AP2 sempre exibido (5.042 combinações em vez de 2.802),
domínio e obrigatoriedade alterados, telefone aceitando código de área real, e
equação sem chaves (1.200 combinações sem caminho).

O percurso manual dos dez caminhos e as cinco conferências que a E14 pediu estão na
seção 11 de [`navegacao-condicional.md`](../../docs/especificacao/navegacao-condicional.md).
