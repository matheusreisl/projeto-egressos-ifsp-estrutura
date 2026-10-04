# Acesso por token e pré-preenchimento

**Etapa:** E18 — configurar acesso por token e pré-preenchimento
**Data:** 04/10/2026
**Decorre de:** [`blocos-instrumento.md`](blocos-instrumento.md), seção 12.5 (E13),
[`navegacao-condicional.md`](navegacao-condicional.md), seção 3.3 (E14),
[`infra/instrumento/`](../../infra/instrumento/README.md) (E15) e
[`importacao-base.md`](importacao-base.md) (E17)

Como o egresso chega ao instrumento — pelo endereço individual —, e como a
identificação acadêmica abre já preenchida com o que a instituição sabe dele, para
que ele confirme ou corrija.

## 1. Objeto e decisão

**Objeto.** O questionário 202615, com os 500 participantes sintéticos importados
na E17, agora **ativo**.

**Decisão tomada** (confirmada com o orientando antes da execução): **o acesso de
amostra foi feito no próprio instrumento**, com três participantes da base, e as
respostas de teste foram apagadas em seguida (seção 6). A alternativa — uma cópia
descartável — exigiria importar participantes com atributos só para o teste, e não
verificaria a configuração que vai a campo.

## 2. A configuração aplicada

| O quê | Como | Onde está |
|---|---|---|
| endereço individual | `…/index.php/202615?token=<token>&lang=pt-BR`; o token, de 15 caracteres, é gerado pela plataforma na importação | E17 |
| acesso só por endereço individual | modo de acesso fechado (`access_mode = C`): sem token, a plataforma pede o código de acesso; com token inválido, recusa | E17 |
| pré-preenchimento | valor padrão das questões IDA1, IDA3, IDA4 e IDA5 = atributo do participante (`{TOKEN:ATTRIBUTE_n}`) | `estrutura.py`, campo `pre_preenchido` |
| nível | IDA2 é equação sobre o curso — não tem padrão: acompanha o curso, pré-preenchido ou corrigido, na própria página 2 | E15 |
| ativação | `instrumento.py ativar`, por último, depois da importação | este documento, seção 5 |

| Campo | Atributo do participante | Conteúdo |
|---|---|---|
| IDA1 — curso | `attribute_2` | código do curso (`T01`…) |
| IDA2 — nível | — | derivado do curso |
| IDA3 — campus | `attribute_4` | sigla da unidade (`SPO`…) |
| IDA4 — ano de conclusão | `attribute_5` | quatro dígitos |
| IDA5 — semestre de conclusão | `attribute_6` | `1` ou `2` |

O número de cada atributo vem de **um lugar só**: a ordem de
`ATRIBUTOS_QUESTIONARIO`, em `instrumento.py`. A preparação da E17 cria as colunas
nessa ordem, e o gerador calcula o `{TOKEN:ATTRIBUTE_n}` pela mesma lista. Mudar a
ordem exige reimplantar e reimportar.

**Configurações do questionário que pesam aqui**, todas da E15 e mantidas: respostas
não anônimas — o estado do participante e a fila de revisão dependem do token na
resposta —; retomada **não** pelo endereço, e sim por nome e senha (E14); e o
descarte das respostas fora do caminho, que é o padrão da plataforma
(`deletenonvalues = 1`).

## 3. Como a plataforma aplica o padrão

Conferido no código (`em_manager_helper.php`): ao exibir a página, para cada questão
relevante e ainda sem valor, a plataforma **processa o padrão como expressão** e
**só o aceita se for resposta válida** para a questão. Três consequências:

1. funciona nas listas — curso e campus —, e não só em texto e número, porque o
   valor do atributo é o **código** de uma opção, que a E17 já grava;
2. **um atributo inválido não produz erro para o respondente**: o campo
   simplesmente abre vazio, e só o administrador vê o aviso. Por isso a conferência
   da seção 6 cobre os 500 participantes, e não só a amostra;
3. o padrão só preenche o que ainda não tem valor: quem volta à página 2 vê o que
   confirmou, e não o original de novo.

## 4. Correção, valor original e fila de revisão

Como a seção 12.5 da E13 determinou:

- **o respondente corrige dentro do domínio fechado** — as listas de curso e de
  unidade, o ano e o semestre. Não há correção em texto livre;
- **a resposta guarda o valor confirmado; o atributo do participante continua com
  o original** — conferido depois de uma correção real (seção 6), e não presumido;
- **a correção não move o ciclo**: a âncora da P5 vem do atributo, e o atributo não
  muda.

**A fila de revisão é uma consulta, e não estrutura nova.** São as respostas em que
o valor confirmado de IDA1 a IDA5 difere do atributo original do participante. Ela
se faz pela API, por código do campo — exportação das respostas com cabeçalho por
código e lista de participantes com os atributos —, e não por consulta direta à
tabela de respostas, cujas colunas se chamam `Q<qid>` e **mudam a cada
implantação** (achado da E15). A consulta foi exercitada na verificação (seção 6).
Transformá-la em rotina, e a taxa de correção por atributo em indicador de
qualidade da base, é da extração (E28).

## 5. Procedimento

A ordem completa, do zero, da raiz do repositório:

```bash
python3 infra/instrumento/instrumento.py implantar
python3 infra/instrumento/instrumento.py preparar-participantes
python3 scripts/importar_base.py --arquivo dados/sinteticos/base-sintetica.csv --questionario 202615
python3 infra/instrumento/instrumento.py ativar
```

`ativar` vem **por último** porque a ativação trava a estrutura, e recusa se o
acesso não estiver fechado ou se não houver participantes. Antes da ativação,
`implantar --substituir` recria o questionário — e descarta os seus participantes,
que a importação seguinte recria, reencontrando as mesmas pessoas na base central.
Depois da ativação, `implantar` recusa: ativo tem respostas.

**Nesta etapa o caminho foi refeito inteiro**, porque os padrões são estrutura: o
questionário foi reimplantado com eles, preparado, reimportado — 500 pessoas
reencontradas na base central, 500 participantes novos — e ativado. O `.lss`
versionado foi reexportado com os padrões. Nenhuma mensagem havia sido enviada, e a
troca de tokens não custou nada.

## 6. Verificação do critério

O critério é que **um acesso de amostra abra com os atributos corretos**.

- **Conferência estrutural: 7 de 7.** A nova conferência 7 de
  `infra/confere-instrumento.py` deriva, do texto da especificação, o atributo de
  cada campo — "ano de conclusão" vira `ano_conclusao` — e confere que o padrão
  aponta para a coluna do participante com essa descrição. **Rodada antes da
  reimplantação, falhou**, apontando os quatro padrões que faltavam; depois, passou.
- **Três acessos de amostra, um por nível**, pelo endereço individual, cada um em
  sessão nova, com o consentimento dado e a página 2 lida:

  | Participante | IDA1 | IDA2 | IDA3 | IDA4 | IDA5 |
  |---|---|---|---|---|---|
  | SIN-000001 | T01 — Técnico em Informática | Técnico | DID — Campus Diadema | 2016 | 2 |
  | SIN-000003 | G04 — Bacharelado em Ciência da Computação | Graduação | HTO — Campus Hortolândia | 2016 | 1 |
  | SIN-000023 | P02 — Especialização em Ensino de Ciências e Matemática | Pós-graduação | BRT — Campus Barretos | 2016 | 1 |

  Os três **conferem com o arquivo de origem**, regenerado — o gerador é
  determinístico — e traduzido pela configuração. **Critério atendido.**
- **Correção.** No primeiro participante, o curso foi trocado na página 2 por um de
  graduação: o nível passou a "Graduação" na hora, sem envio. Enviada a página, a
  resposta guarda `G01` e `graduacao`; o participante continua com `T01` e
  `tecnico`, sem marca de concluído. A fila de revisão, pela API, apontou
  exatamente as duas divergências.
- **Os 500, e não só a amostra.** Todo participante tem curso e campus entre as
  opções do instrumento, ano e semestre válidos e nível coerente com o curso — o
  que garante que nenhum abrirá com campo vazio por padrão inválido.
- **Controle de acesso.** Sem token, a plataforma pede o código de acesso; com token
  inexistente, responde que ele "não é válido ou já foi usado".
- **Limpeza.** As três respostas de teste foram apagadas pela API. Estado final: 500
  participantes, nenhuma resposta, nenhum salvamento, nada enviado, nada concluído.

## 7. O que esta etapa não permite afirmar

1. **A janela de validade do acesso não foi configurada.** Os 60 dias da P5 são
   `validfrom` e `validuntil` do participante, ajustados por ciclo — é da rotina da
   E21.
2. **A amostra foi conduzida por script** na interface real, como na E15; a leitura
   da tela foi também visual no primeiro acesso.
3. **A fila de revisão foi exercitada, e não implementada como rotina** — é da E28.
4. **Nada aqui envolveu dado de pessoa real.**

## 8. O que esta etapa determina para as etapas seguintes

- **E19 (unicidade)** — 500 participantes ativos no 202615, com tokens novos, depois
  da reimplantação; a base central é a mesma da E17.
- **E20 (mensagens)** — o endereço individual tem a forma da seção 2, e o convite o
  leva com `lang=pt-BR`; a mensagem explica que a identificação vem preenchida, para
  confirmar ou corrigir.
- **E21 (rotina)** — ajustar `validfrom` e `validuntil` por ciclo; a âncora vem dos
  atributos, que a correção do egresso não altera.
- **E23 (conformidade)** — a correção de atributo pelo egresso é evento da trilha; a
  fila de revisão é a sua fonte.
- **E26 (cenários)** — a correção de nível que muda o Bloco IV já foi vista no
  navegador; repetir no cenário completo.
- **E28 (extração)** — a fila de revisão e a taxa de correção por atributo, pela
  exportação por código; nunca pelas colunas `Q<qid>`.
- **E30 (guia)** — a ordem dos quatro comandos, e por que a ativação vem por último.
