# ALVARES, LOUTFI e CAMPOS (2020) — Mapeamento automatizado dos egressos da UNIRIO

**Referência:** ALVARES, R. V.; LOUTFI, M. S.; CAMPOS, N. de S. Onde estão meus
egressos? Relato sobre um mapeamento automatizado da vida profissional dos formados
em Sistemas de Informação da UNIRIO. In: WORKSHOP SOBRE EDUCAÇÃO EM COMPUTAÇÃO
(WEI), 28., 2020, Cuiabá. Anais [...]. Porto Alegre: SBC, 2020. p. 56-60.
**Tipo:** artigo científico (relato de experiência)
**Acesso:** https://sol.sbc.org.br/index.php/wei/article/view/11129 · consultado em 20/09/2026
**Alimenta:** E03, E04, E31 — e sustenta a decisão de não integrar RAIS/CAGED

## Problema identificado

Após a graduação o egresso não tem obrigação formal de manter contato com a
instituição, e o distanciamento resultante impede a IES de conhecer sua trajetória
profissional. O problema tem consequência avaliativa: os autores registram que o
perfil do egresso figura em sete indicadores do instrumento de avaliação in loco
de cursos do MEC.

## Método

Os autores propõem o modelo **MVP — Mapeamento da Vida Profissional**, cuja
premissa declarada é obter os dados **sem entrar em contato com o egresso**. O
desenho integra três fontes:

| Fonte | Papel | Condição de acesso |
|---|---|---|
| Sistema acadêmico da IES (SIE UNIRIO) | fornece nome e CPF, em relatório CSV | interno |
| RAIS, base nomeada, ano-base 2018 | vínculos formais de emprego, por busca com nome e CPF | **convênio entre o Departamento de Informática da UNIRIO e o Ministério da Economia** |
| Base aberta de CNPJ (Receita Federal) | identifica sócios de empresa e MEI | pública, tratada por projeto de terceiros (`qsacnpj`), em SQLite |

Consolidação em MySQL, com rotinas de importação e exportação e consultas SQL para
gerar os indicadores. População: 281 egressos formados até 2018/1.

## Resultado

| Indicador | Valor |
|---|---|
| Índice de empregabilidade | 76% (214 egressos com vínculo formal) |
| Remuneração média | R$ 7.560 |
| Concentração em quatro cargos | 62% do total |
| Analista de Desenvolvimento de Sistemas | 42% · R$ 7.342 |
| Desenvolvedor de sistemas de TI | 11% · R$ 5.721 |
| Egressos sócios de empresa ou MEI | 10% |

Os autores interpretam o índice de 76% como piso e não como medida: atribuem a
diferença a egressos em pós-graduação em dedicação exclusiva, à informalidade
frequente na área de TI e aos sócios e MEI — nenhum dos três captável pela RAIS.

## Implicação para o projeto

Este artigo documenta a **alternativa por registro administrativo**: obter o dado
sobre o egresso sem depender da adesão dele. É precisamente o caminho que este
projeto descartou, e o artigo fornece a evidência que sustenta a decisão.

1. **Confirma a barreira de acesso.** O acesso à RAIS nominal se deu mediante
   convênio formal entre a instituição e o Ministério da Economia. Convênio é
   exatamente o tipo de tramitação cuja duração não é controlável pela equipe e que
   o projeto excluiu do caminho crítico do cronograma. O que na UNIRIO foi possível
   por via institucional não é reproduzível em um projeto de ensino com prazo de
   cinco meses.
2. **Opera sobre pessoas identificadas, sem consentimento.** O cruzamento se faz
   por nome e CPF. O desenho deste projeto é o oposto: consentimento eletrônico,
   anonimização e trilha de auditoria. As duas abordagens respondem à mesma
   pergunta por fundamentos distintos, e isso merece registro no relatório final.
3. **Reforça o valor do contato dirigido.** Ao discutir o distanciamento, os autores
   observam que ele diminui quando a IES estrutura um programa de acompanhamento
   com encontros regulares, contato por rede social ou e-mails personalizados —
   insumo para o quadro de engajamento da E04.

## Limitações da fonte

- **Recorte temporal mínimo.** Limitação declarada pelos autores: apenas o ano-base
  2018 da RAIS, sem série histórica. Não permite falar em trajetória, apenas em
  fotografia.
- **O indicador principal é um piso, não uma medida.** Os próprios autores
  reconhecem que a RAIS não capta informalidade nem vínculo societário. O "índice
  de empregabilidade" mede presença em registro formal de emprego, que é coisa
  diferente de estar empregado.
- **Não é transferível sem convênio.** Isso não é uma falha do estudo, mas é o que
  mais importa aqui: o método não se replica em instituição que não consiga o
  mesmo acesso.
- **Caso único, sem comparação.** Um curso, uma IES, cinco páginas de relato. Não há
  contraste com outras unidades nem com outros métodos de coleta.
- **Silencia sobre o que o egresso pensa.** Por construção, o método produz vínculo
  formal e situação societária. Percepção sobre a formação, adequação do currículo,
  continuidade de estudos e satisfação ficam integralmente fora do alcance — e são
  justamente os indicadores que uma política de acompanhamento precisa coletar.
  Registro administrativo e instrumento de coleta não são substitutos entre si.
