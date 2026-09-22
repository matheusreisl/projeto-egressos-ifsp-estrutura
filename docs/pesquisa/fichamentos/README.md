# Fichamentos

Um arquivo por fonte, com problema, método, resultado, implicação para o projeto e
limitações. O modelo está em [`0000-modelo.md`](0000-modelo.md).

As 17 fontes abaixo são as referências do documento do projeto
(`docs/projeto/`), que é a fonte de verdade. Fonte acrescentada depois entra aqui
com a mesma estrutura.

Nomenclatura: `sobrenome-ano.md`, ou `orgao-tipo-ano.md` para normativas, de modo
que a ordenação alfabética da pasta acompanhe a lista de referências. Os arquivos
levam o nome da autoria conferida na fonte.

## Estado — 17 de 17 fichadas

| Fonte (autoria conferida) | Grupo | Arquivo |
|---|---|---|
| ALVARES, LOUTFI e CAMPOS (2020) — UNIRIO, WEI/SBC | experiência | [`alvares-2020.md`](alvares-2020.md) |
| BRASIL — Lei nº 10.861/2004 (SINAES) | normativa | [`brasil-lei-10861-2004.md`](brasil-lei-10861-2004.md) |
| BRASIL — Lei nº 13.709/2018 (LGPD) | normativa | [`brasil-lei-13709-2018.md`](brasil-lei-13709-2018.md) |
| CABRAL, SILVA e PACHECO (2016) — portais online de egressos, GUAL | experiência | [`cabral-2016.md`](cabral-2016.md) |
| COELHO e SILVA (2017) — EMESCAM, Textos & Contextos | estudo de egressos | [`coelho-2017.md`](coelho-2017.md) |
| DAVIS (1989) — TAM, MIS Quarterly | modelo teórico | [`davis-1989.md`](davis-1989.md) |
| FERREIRA (2026) — egressos da UFOP pelo LinkedIn | estudo de egressos | [`ferreira-2026.md`](ferreira-2026.md) |
| IFES (2025) — pesquisa de egressos, versão 2025 | linha de base | [`ifes-2025.md`](ifes-2025.md) |
| IFSP — Resolução Normativa nº 13/2022 (PAEg) | normativa | [`ifsp-rn-13-2022.md`](ifsp-rn-13-2022.md) |
| IFSP — acompanhamento dos egressos (portal) | linha de base | [`ifsp-portal-egressos-2022.md`](ifsp-portal-egressos-2022.md) |
| IFTO (2023) — política de proteção de dados pessoais | normativa | [`ifto-ppdp-2023.md`](ifto-ppdp-2023.md) |
| PRAGA DE SOUZA, COUTO ASSIS e DE SOUZA COSTA (2025) — RAEG | experiência | [`praga-de-souza-2025.md`](praga-de-souza-2025.md) |
| RANTHUM e SANTOS JUNIOR (2023) — ferramenta para pós stricto sensu | experiência | [`ranthum-2023.md`](ranthum-2023.md) |
| SILVA, MINEIRO e FAVARETTO (2022) — revisão integrativa, RSD | experiência | [`silva-2022.md`](silva-2022.md) |
| SILVA et al. (2024) — avaliação do SAVE, ERES/SBC | experiência | [`silva-2024.md`](silva-2024.md) |
| UnB (2019) — egressos RAIS, Educação Física | estudo de egressos | [`unb-2019.md`](unb-2019.md) |
| USP — Programa Alumni USP | programa de referência | [`usp-alumni.md`](usp-alumni.md) |

### Fonte adicional, fora das 17

| CARVALHO (2025) — frontend do sistema de egressos da UFU | [`carvalho-2025.md`](carvalho-2025.md) |
|---|---|

Localizada porque o endereço da referência de Cabral apontava para ela. Não consta
das referências do projeto; fica fichada por já ter sido lida e por servir de termo
de comparação do custo da via de desenvolvimento próprio.

## Pendências levantadas

Toda pendência desta seção tem etapa responsável declarada. Pendência sem etapa
não é recolhida por ninguém — foi o que se aprendeu na E04, e o `ETAPAS.md` traz
o registro correspondente em cada etapa citada aqui.

**Fontes que precisavam de nova leitura** — ~~recolhidas pela **E07**~~ ·
**ENCERRADO em 21/09/2026**

As duas foram relidas na íntegra depois que a E07 provisionou a ferramenta de
extração de texto. Ambas as fichas trazem seção "Histórico de leitura" com o que
mudou.

- **FERREIRA (2026)** — relida. **Duas correções materiais.** O método não é coleta
  de perfis públicos: o algoritmo **autentica-se no LinkedIn** antes de percorrer
  os perfis, o que é raspagem sob sessão autenticada e reforça o descarte da
  raspagem por este projeto, em vez de enfraquecê-lo. E a cobertura, antes não
  verificada, é de **103 perfis em 127 formados (≈81%)** — número alto, mas sobre
  coorte pequena, recente e de área de tecnologia, sem base para transposição a um
  instituto multicampi. Corrigidos também o grau e o número de folhas da referência.
- **DAVIS (1989)** — relido. **Uma correção material:** os "n" de 184 e 80 são
  somas de *avaliações*, não de pessoas — são **112** e **40** participantes. O
  achado central e os coeficientes já estavam corretos. Acrescentou-se a natureza
  **prospectiva** do Estudo 2, que é o que delimita o alcance de avaliações de
  protótipo por TAM, como a do SAVE.

**Conferências de referência antes da entrega** — recolhidas pela **E31**

- **RANTHUM e SANTOS JUNIOR (2023)** — o fichamento não registra a instituição de
  aplicação da ferramenta; o documento do projeto a atribui à Universidade
  Paranaense.
- **PRAGA DE SOUZA et al. (2025)** — divergência de autoria entre o PDF (dois
  autores) e a página do periódico (três). Adotou-se a citação da página.
- **IFSP — RN nº 13/2022** — numeração de artigos corrompida pelo OCR. Conferir no
  PDF original todo dispositivo citado.

**Material relevante ausente das 17 referências**

- ~~Instrumentos de avaliação do INEP~~ — **localizados e usados na E03**. A
  exigência está no Indicador 3.7 do Instrumento de Avaliação Institucional
  Externa (2017), não na Lei do SINAES.
- ~~IFSP, Relatórios 1 e 2 da Pesquisa de Acompanhamento de Egressos~~ — **lidos e
  usados na E03**. Trazem a estrutura completa do instrumento vigente, os domínios
  de resposta e as contagens por período.
- ~~IFSP, Portaria Normativa nº 128/2025~~ — **recuperada por inteiro e usada na
  E03**. O PDF não era digitalizado: tinha camada de texto em fluxos comprimidos.
  Os dezenove indicadores do Anexo I estão reproduzidos na linha de base.
- **Mello et al. (2023)** — avaliação do SAVE com egressos, complementar ao artigo
  de 2024, que cobre apenas gestores. **Recolhida pela E31.** É a única fonte que
  traria o lado do respondente a um conjunto hoje formado só por gestores e
  coordenadores. Localizar e incorporar ao quadro de engajamento ou, não sendo
  possível, declarar a ausência como limitação do quadro.

## Grupos

- **normativa** — o que a lei e os atos institucionais exigem do mecanismo.
- **linha de base** — instrumentos institucionais em operação, insumo da E03.
- **experiência** — sistemas e iniciativas de outras instituições, insumo da E04.
- **estudo de egressos** — levantamentos sobre a população, insumo da E04 e da E05.
- **modelo teórico** — referencial de análise.
- **programa de referência** — iniciativa de relacionamento com egressos em operação.

## Critério

O fichamento é feito sobre a leitura da fonte, não sobre a menção a ela no
documento do projeto. Quando a leitura integral não foi possível, o fichamento
declara o que foi efetivamente lido, no campo de limitações.
