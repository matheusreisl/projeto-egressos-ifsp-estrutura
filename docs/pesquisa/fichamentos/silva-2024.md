# SILVA et al. (2024) — Avaliação do sistema SAVE

**Referência:** SILVA, M. E. L.; FERREIRA, M. S.; RIBEIRO, B. M.; QUINCOZES, C. B.;
FINGER, A. F.; DE MELLO, A. V. Inovação no acompanhamento de egressos: avaliação do
SAVE a partir da perspectiva dos gestores. In: ESCOLA REGIONAL DE ENGENHARIA DE
SOFTWARE (ERES), 8., 2024, Santiago/RS. Anais [...]. Porto Alegre: SBC, 2024.
p. 118-127.
**Tipo:** artigo científico
**Acesso:** https://sol.sbc.org.br/index.php/eres/article/view/31845 · consultado em 20/09/2026
**Alimenta:** E04, E12, E18, E25, E31

> **Correção de referência.** O documento do projeto atribui esta fonte a "BASSO, F.
> et al." e a subtitula "a partir da percepção de coordenadores de curso". Nenhuma
> das duas informações confere: não há autor de sobrenome Basso no artigo, cujos
> autores são vinculados à **Universidade Federal do Pampa (Unipampa)**, e o
> subtítulo correto é "a partir da **perspectiva dos gestores**". A referência
> precisa ser corrigida antes de qualquer entrega.

## Problema identificado

Pesquisas com egressos exigem esforço recorrente de ex-alunos e gestores. Os
autores identificam duas limitações nas ferramentas de formulário de uso geral:
construir o instrumento é oneroso para o gestor, que precisa decidir sozinho quais
questões incluir; e a análise gera um gráfico por questão, exigindo ferramentas
complementares para cruzar respostas. Acrescentam uma terceira: essas ferramentas
não armazenam o histórico de respostas, obrigando o egresso a repreencher os mesmos
campos a cada edição.

## Método

Apresentação do **SAVE** (Sistema de Acompanhamento de Egressos), do projeto
Egress@s da Unipampa, por meio de **protótipo de alta fidelidade construído no
Figma** — não de sistema implementado.

Quatro objetivos de projeto: facilitar a elaboração do instrumento por banco de
questões predefinidas, derivadas de mapeamento sistemático da literatura (O1);
agilizar a resposta exibindo ao egresso o que ele já respondeu antes, para que
atualize apenas o que mudou (O2); gerar gráficos automaticamente, inclusive
cruzando questões (O3); e publicar resultados selecionados (O4). Há funcionalidade
de **gerenciar participantes**, com criação e edição de grupos de egressos para o
envio.

**Avaliação.** Protocolo de cinco etapas, com questionário baseado no **Modelo de
Aceitação de Tecnologia (TAM)**, de Davis (1989). Amostra de **sete coordenadores
de curso** da Unipampa. Instrumento com 19 questões — 18 fechadas em escala Likert
de 5 pontos, distribuídas em utilidade, facilidade e pretensão de uso, mais uma
aberta — construído no Google Forms, com termo de consentimento livre e esclarecido
e instruções de uso do sistema. A interação com o protótipo foi supervisionada por
um pesquisador.

## Resultado

| Dimensão | Resultado |
|---|---|
| Utilidade | todos concordaram que o sistema simplificaria e agilizaria a criação de questionários, aceleraria a análise por gráficos e facilitaria o trabalho da coordenação |
| Qualidade | em duas questões, quatro concordaram parcialmente, dois foram neutros e um discordou parcialmente quanto à melhoria da qualidade dos questionários e dos resultados |
| Facilidade | maioria concordante; um coordenador discordou parcialmente que seja fácil editar questões e enviar questionários |
| Pretensão de uso | todos preveem usar a ferramenta e recomendá-la; seis a prefeririam a outros mecanismos de coleta, um foi neutro |

Na questão aberta, respondida por cinco participantes, um observou confusão na
transição entre telas do protótipo e outro duvidou de que a ferramenta auxilie na
análise, por entender que análise envolve uma fase mais profunda de interpretação.

## Implicação para o projeto

**1. É a alternativa metodológica oposta, e isso organiza a justificativa.** Diante
da mesma constatação — ferramentas de uso geral são insuficientes — há duas
respostas possíveis: desenvolver um sistema próprio, como o SAVE, ou configurar
adequadamente uma plataforma livre existente, como faz este projeto. O contraste é
material para o relatório final: o caminho do SAVE exige equipe de desenvolvimento
e manutenção continuada; o deste projeto exige configuração documentada e produz
um artefato que outra instituição instala sem depender de código próprio.

**2. Confirma a pertinência da plataforma escolhida.** Ao revisar a literatura, os
autores registram que os estudos da área utilizam predominantemente **LimeSurvey ou
Google Forms** para coletar os dados. Isso posiciona o LimeSurvey como opção
corrente na área, e não como escolha idiossincrática.

**3. Duas das três limitações apontadas pelos autores são resolvidas por
configuração, não por desenvolvimento.** Esta é a observação mais útil. O objetivo
O2 — poupar o egresso de repreencher o que já informou — é exatamente o que a
tabela de participantes com atributos pré-carregados oferece no LimeSurvey, e é o
que a E18 implementa. A funcionalidade de gerenciar participantes do SAVE tem
equivalente direto na mesma tabela. O que os autores trataram como lacuna a ser
suprida por um sistema novo é, em boa parte, recurso não acionado da ferramenta que
eles próprios identificam como predominante na área. Isso reforça o argumento
central do projeto, já observado no instrumento vigente do IFSP: a limitação
frequente não está na ferramenta, está na configuração.

Permanece fora desse alcance o objetivo O1 — o banco de questões validadas —, que é
conteúdo e não estrutura, e que neste projeto entra como requisito de entrada
vindo de projeto correlato.

**4. Contraste metodológico útil para a E25.** O SAVE foi validado por percepção de
usuários, com TAM. Este projeto valida por simulação controlada contra requisitos
verificáveis. São desenhos com alcances distintos: o TAM mede intenção declarada;
a simulação mede comportamento observado do sistema. Nenhum dos dois mede resultado
de coleta real. Registrar essa distinção protege o relatório final de sugerir mais
do que se verificou.

## Limitações da fonte

- **Não há sistema, há protótipo.** A avaliação incidiu sobre telas no Figma, com
  fluxos parcialmente não clicáveis. Nada no artigo demonstra funcionamento, e
  menos ainda desempenho em coleta real.
- **Amostra de sete, em uma única instituição.** Os próprios autores declaram que
  os resultados não são generalizáveis.
- **Avaliação conduzida pelos desenvolvedores, com interação supervisionada.** O
  artigo não descreve controle desse viés. Em avaliação de aceitação, a presença do
  pesquisador durante o uso e o vínculo dele com o produto tendem a favorecer
  respostas positivas.
- **TAM mede intenção, não efeito.** Todos os indicadores reportados são de
  percepção declarada. Nada no artigo permite afirmar que o SAVE eleve taxa de
  resposta, melhore a qualidade dos dados ou reduza a não resposta — e o artigo,
  corretamente, não o afirma. Ao citá-lo, o relatório final precisa preservar essa
  distinção, que é a mesma restrição que este projeto se impõe.
- **A perspectiva do egresso está ausente deste artigo.** Foi objeto de trabalho
  anterior dos mesmos autores (Mello et al., 2023), não incluído entre as
  referências do projeto. Aqui, avalia-se apenas a visão do gestor.
