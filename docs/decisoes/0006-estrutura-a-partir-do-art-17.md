# ADR-0006 — Estrutura do instrumento a partir do art. 17 do Regulamento

**Status:** aceita
**Data:** 28/09/2026
**Etapa de origem:** E12 — especificar os blocos estruturais do instrumento

## Contexto

O documento do projeto propõe sete blocos próprios para o instrumento. É anterior
ao Regulamento do Programa de Acompanhamento de Egressos (Portaria Normativa nº
128/2025), recuperado só na E03, e deixa sem bloco seis dos dezenove indicadores
do Anexo I: remuneração, as quatro satisfações e a satisfação com a formação.

O Regulamento estrutura o questionário do IFSP em outros sete blocos (art. 17,
§2º). Três deles — II, Atividade Profissional Anterior; VI, Motivos da Não
Inserção no Mercado de Trabalho; VII, Avaliação da PAEG — não alimentam nenhum
indicador do Anexo I, embora sirvam a objetivos que o mesmo Regulamento enuncia
(art. 3º, itens 3 e 5; art. 34, item 1).

O critério de conclusão da E12 é que nenhum bloco exista sem indicador
correspondente. Duas coisas precisavam ser decididas: qual estrutura serve de
referência, e o que conta como "indicador correspondente".

## Alternativas avaliadas

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Blocos do art. 17 mais os de controle; indicador do Anexo I ou objetivo expresso do Regulamento** | hospeda o instrumento do IFSP e o conteúdo do projeto correlato sem alteração estrutural; alimenta 18 dos 19 indicadores do Anexo I; todo bloco tem medida declarada e origem rotulada | três indicadores passam a ser propostos pelo projeto, e a instituição pode redefini-los; a estrutura cresce para onze blocos; entra dado sensível, com o consentimento específico que ele exige |
| Blocos do art. 17 mais os de controle; só o Anexo I | critério estrito, conferível contra a norma sem interpretação | exclui três blocos que a própria norma prescreve e os recortes de gênero e raça que ela pede (art. 3º, item 16); a estrutura não hospedaria o instrumento do IFSP sem alteração |
| Blocos do documento do projeto, completados com o que falta ao Anexo I | continuidade com o documento registrado | diverge do art. 17: o conteúdo que chega nos blocos da norma teria de ser remapeado, e os Blocos II, VI e VII não teriam lugar |

## Decisão

O instrumento tem **onze blocos**: os sete do art. 17, com os nomes e a ordem do
Regulamento; três de controle do mecanismo — consentimento, identificação
acadêmica, contato e manifestações —; e um de recortes de equidade. **"Indicador
correspondente"** é um indicador do Anexo I ou um objetivo expresso do
Regulamento, operacionalizado por indicador mínimo proposto pelo projeto, com a
origem declarada.

## Justificativa

O documento do projeto exige que instrumentos revisados possam ser incorporados
"sem alteração estrutural da solução", e o instrumento do IFSP tem estrutura
fixada por norma. Partir do art. 17 é o que torna essa exigência cumprível — e é
coerente com a posição que a linha de base firmou para o projeto: viabilizar
norma vigente, e não propor outra.

A leitura do critério preserva a sua função, que é a do princípio da necessidade:
nenhum bloco sem medida declarada. A leitura estrita excluiria blocos que servem a
objetivos expressos da mesma norma que define os indicadores. O rótulo de origem —
Anexo I, objetivo + projeto, controle — impede que um indicador proposto pelo
projeto seja lido como institucional, na mesma lógica com que a E05 declarou a
origem de cada parâmetro de contato.

Decisões confirmadas com o orientando antes da execução da E12. A especificação
completa está em [`blocos-instrumento.md`](../especificacao/blocos-instrumento.md).

## Consequências

**Passa a ser verdade:**

- A E13 aplica aos campos o mesmo critério aplicado aos blocos, com a mesma escala
  de origem.
- O bloco de recortes de equidade traz dado sensível — raça/cor e deficiência — e
  depende de consentimento específico e destacado (LGPD, art. 11, I), que a E22
  implementa. O bloco é opcional, e cada questão oferece não declarar.
- Os indicadores propostos pelo projeto — Blocos II, VI e VII, demandas de
  formação e recortes de equidade — são apresentados como propostas, com o rótulo
  de origem, no painel (E29) e no relatório final (E31).
- Todo bloco tem um público declarado, que a E14 converte em regra de navegação.

**Esta decisão impede:**

- Apresentar os indicadores propostos pelo projeto como parte do Anexo I.
- Acrescentar bloco sem indicador do Anexo I nem objetivo expresso do Regulamento
  — inclusive quando o conteúdo vier do projeto correlato.

## Revisão

Revisável se o Comitê Permanente definir indicadores institucionais para os
Blocos II, VI e VII, ou se o art. 17 for revisto. No primeiro caso, o indicador
proposto é trocado pelo institucional, sem mexer na estrutura; no segundo, a
correspondência da seção 5 de `blocos-instrumento.md` mostra o que muda.
