# IFSP — Acompanhamento dos Egressos (portal institucional)

**Referência:** INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO
(IFSP). Acompanhamento dos egressos. São Paulo: IFSP, 2022.
**Tipo:** documento institucional (página do portal e instrumento vinculado)
**Acesso:** https://ifsp.edu.br/index.php/ceua/42-assuntos/ensino/2895-acompanhamento-dos-egressos · consultado em 20/09/2026
**Alimenta:** E03 (fonte primária da linha de base), E12, E13, E18, E22

## Problema identificado

Esta é a materialização pública da PAEg: o canal por onde o IFSP se dirige aos
egressos e o ponto de acesso ao instrumento de coleta vigente. É, portanto, a
fonte primária da linha de base do projeto — o objeto cuja limitação o trabalho
se propõe a superar.

A página está publicada desde 29/03/2020, com última atualização registrada em
05/03/2026 e 61.535 acessos contabilizados.

## Método

Observação documental da página e da tela inicial do instrumento vinculado.
Nenhuma resposta foi preenchida e nada foi submetido, conforme a delimitação do
projeto.

**A página** apresenta o "Espaço dos Egressos", define egresso nos termos do art.
4º da RN 13/2022, oferece três contrapartidas (educação continuada, integração
acadêmica e colaboração voluntária) e conduz ao questionário eletrônico. Reúne os
normativos: RN nº 13/2022, Portaria nº 5148/2023 e Portaria nº 6601/2025
(designação do COPAEG) e Portaria Normativa nº 128/2025 (Regulamento do Programa).
Disponibiliza ainda dois relatórios da pesquisa de acompanhamento.

**O instrumento** está em `https://enquetes.ifsp.edu.br/889783?lang=pt-BR`.

## Resultado

A caracterização técnica do instrumento vigente é o achado desta fonte:

| Aspecto observado | Constatação |
|---|---|
| Plataforma | **LimeSurvey** — declarado na metatag `generator` do documento |
| Modo de acesso | **aberto, por link público**; não há campo de token nem autenticação |
| Tela de consentimento | **ausente** — a primeira tela já apresenta a pergunta 1 |
| Retomada | ativa: há "Carregar questionário não finalizado" e "Retomar mais tarde" |
| Barra de progresso | ativa |
| Primeira pergunta | campus do primeiro curso, obrigatória, lista fechada com 39 campi mais "Outros" |
| Tipo de curso | obrigatória, lista fechada com 9 opções mais "Outros" |
| Nome do primeiro curso | **texto livre**, obrigatório |
| Situação de trabalho | obrigatória, binária |

Observou-se ainda que o texto de ajuda da primeira pergunta permanece com o
conteúdo padrão de exemplo da plataforma, não substituído.

## Implicação para o projeto

Três consequências, e a primeira reposiciona o trabalho inteiro.

**1. A instituição já opera LimeSurvey.** A escolha de plataforma do projeto deixa
de ser preferência técnica e passa a ser aderência ao que já está em produção no
IFSP. Isso eleva substancialmente o valor prático do artefato: o guia de replicação
(E30) não proporá migração de ferramenta, e sim uma configuração diferente da
mesma ferramenta que a instituição já mantém. É argumento forte para a seção de
resultados e para a viabilidade de adoção.

**2. A limitação não é da ferramenta — é da configuração.** Este é o ponto central
para a E03. O LimeSurvey oferece nativamente tabela de participantes, acesso por
token, convites, lembretes automatizados e controle de quem respondeu. Nada disso
está ativado: o instrumento roda em modo aberto. A consequência é a mesma cadeia
identificada no relatório do Ifes (2025) — sem identificação individual não se
sabe quem não respondeu; sem isso não há denominador nem cobrança dirigida; e o
acesso por link público admite resposta múltipla e de não egressos.

A diferença em relação ao Ifes é decisiva e favorece o argumento do projeto: lá a
limitação decorreu da ferramenta escolhida (Google Forms); aqui, a ferramenta já
instalada tem os recursos e eles não foram acionados. O trabalho não precisa
demonstrar que uma nova plataforma resolveria — precisa demonstrar que a
configuração adequada da plataforma vigente resolve. É uma tese mais modesta e
muito mais defensável.

**3. Confirma empiricamente a lacuna de conformidade.** A ausência de tela de
consentimento no instrumento vigente é a contraparte prática do silêncio da RN
13/2022 sobre proteção de dados. O que na resolução era omissão normativa aparece
aqui como ausência funcional. Justifica a E22 como correção de uma lacuna real e
observada, não como requisito acrescentado por zelo.

Para a **E13**, o campo de nome do curso em texto livre é o exemplo concreto do
problema de padronização: impede agregação por curso sem tratamento posterior,
numa instituição com 39 campi. Para a **E12** e a **E18**, o conjunto observado
(campus, tipo de curso, curso, situação de trabalho) é justamente o tipo de dado
que a instituição já possui e que poderia ser pré-preenchido em vez de perguntado.

## Limitações da fonte

- **A observação cobre apenas a tela inicial.** Não foram percorridos os demais
  grupos de perguntas, porque isso exigiria avançar no instrumento. A
  caracterização completa do instrumento vigente — número de blocos, condicionais,
  domínios, obrigatoriedade — é objeto da E03 e permanece pendente. Convém
  definir ali como percorrê-lo sem submeter resposta.
- **Não se observa a configuração administrativa, apenas o comportamento público.**
  A inferência de que a tabela de participantes não está ativada decorre da
  ausência de token na URL e de campo de acesso, o que é indício forte mas não
  prova: seria possível, em tese, haver uma versão por convite coexistindo com a
  versão aberta. A afirmação deve ser formulada como "o instrumento divulgado no
  portal opera em modo aberto", que é o que se pode sustentar.
- **Não há informação sobre volume, período ou taxa de resposta.** Os dois
  relatórios disponíveis na página podem conter esses dados, e não foram
  examinados — estão fora das 17 referências e ficam registrados como material a
  incorporar na E03.
- **A página não é datada de 2022.** A referência do projeto indica 2022, mas a
  publicação original é de 29/03/2020 e a última atualização, de 05/03/2026. Como
  conteúdo vivo, a citação deve registrar a data de consulta, e não um ano fixo.
