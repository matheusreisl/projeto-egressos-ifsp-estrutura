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
definir pelo projeto correlato". O texto das perguntas, o do termo de consentimento
e o de encerramento não são deste projeto (CLAUDE.md, decisão 5; E22). Os domínios
de resposta são estrutura e entram completos.

## O que há aqui

| Arquivo | Papel |
|---|---|
| `instrumento.lss` | **a estrutura exportada da instância** — o artefato versionado |
| `estrutura.py` | a especificação das E12 a E14 transcrita em dados: grupos, campos, domínios, regras de exibição |
| `instrumento.py` | gera o `.lss`, implanta, exporta, cria e remove cópias de ensaio, e prepara o acesso controlado (E17) |
| `comandos/ExportarestruturaCommand.php` | comando de console que exporta o `.lss` |
| `comandos/PrepararbasecentralCommand.php` | cria os atributos da base central, os de contato cifrados (E17) |
| `comandos/ImportarbasecentralCommand.php` | grava a importação na base central, decifrando para aplicar a precedência (E17) |
| `comandos/RegistrarimportacaoCommand.php` | registra cada importação na trilha `egressos_importacoes` (E17) |
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
`--substituir`, recria — mas só se estiver **inativo**, porque ativo tem respostas.

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

## Verificação

`confere-instrumento.py` lê a especificação **direto dos documentos** — a seção 12.3
de `blocos-instrumento.md` e as seções 2 e 5 de `navegacao-condicional.md` — e não de
`estrutura.py`, para que um erro de transcrição no gerador apareça como divergência
em vez de se confirmar a si mesmo. Sete conferências:

1. os onze grupos, na ordem da E14;
2. os 35 campos: código, grupo, tipo, obrigatoriedade e domínio, opção por opção
   pelo rótulo;
3. as listas de configuração contra `configuracao/`;
4. o nível derivado de cada curso;
5. as validações de contato contra vinte exemplos;
6. os dez caminhos, **avaliando as expressões que estão na instância** sobre as
   2.802 combinações da seção 8 da E14, com a regra do item 1 das armadilhas;
7. o pré-preenchimento (E18): cada campo da identificação aponta para o atributo
   do participante que tem o seu nome, derivado do texto da especificação.

**Resultado: 6 de 6 na E15; 7 de 7 desde a E18** — a sétima falhou antes da
reimplantação com os padrões, apontando os quatro que faltavam, e passou depois. A
conferência foi ela mesma testada por mutação, e reprova
as cinco versões defeituosas que lhe foram apresentadas: sem `.NAOK` (280
combinações sem caminho), AP2 sempre exibido (5.042 combinações em vez de 2.802),
domínio e obrigatoriedade alterados, telefone aceitando código de área real, e
equação sem chaves (1.200 combinações sem caminho).

O percurso manual dos dez caminhos e as cinco conferências que a E14 pediu estão na
seção 11 de [`navegacao-condicional.md`](../../docs/especificacao/navegacao-condicional.md).
