# CARVALHO (2025) — Arquitetura frontend do sistema de egressos da UFU

**Referência:** CARVALHO, L. A. da S. Arquitetura frontend e interface de um
sistema de acompanhamento de egressos para a UFU. 2025. Trabalho de Conclusão de
Curso (Bacharelado em Sistemas de Informação) — Faculdade de Computação,
Universidade Federal de Uberlândia, Uberlândia, 2025.
**Tipo:** trabalho de conclusão de curso
**Acesso:** https://repositorio.ufu.br/bitstream/123456789/45437/1/ArquiteturaFrontendInterface.pdf · consultado em 20/09/2026
**Alimenta:** E04, E29, E31

> **Fonte adicional.** Este trabalho não consta das referências do projeto. Foi
> localizado durante o fichamento e fica registrado por já ter sido lido e por
> servir de termo de comparação do custo da via de desenvolvimento próprio.

## Problema identificado

A UFU desenvolve um sistema próprio de acompanhamento de egressos. Este trabalho dá
continuidade ao projeto, tratando especificamente da camada de interface: construir
um frontend responsivo, acessível e modular para o sistema.

## Método

Desenvolvimento de software com Scrum. Stack: **Angular** no frontend, em
conformidade com o **Design System do Governo Brasileiro (DsGov)**; Java previsto
para o backend; PostgreSQL como banco; Figma para prototipação, em média e alta
fidelidade.

Escopo entregue: frontend concluído; backend em andamento; modelagem do banco
ajustada. Funcionalidades do frontend: gerenciamento de informações acadêmicas e
profissionais, coleta de depoimentos e **exibição de dashboards públicos**.

Postergadas para etapas futuras: integração com o SSO da UFU e extração
automatizada de dados da plataforma Lattes.

## Resultado

O autor conclui que a aplicação facilita o acompanhamento de ex-alunos, atende
exigências regulatórias e fortalece o vínculo com egressos, com potencial de
expansão para outras instituições.

## Implicação para o projeto

**1. Dimensiona o custo da via do desenvolvimento próprio.** É o terceiro caso do
conjunto — com o SAVE e o RAEG — em que a resposta ao problema é construir um
sistema. Aqui o dado mais informativo é o recorte: **um TCC inteiro para entregar
apenas a camada de interface**, com backend ainda em andamento e as integrações
mais sensíveis adiadas. Isso quantifica, em esforço acadêmico, o que significa a
alternativa que este projeto não seguiu. Em um trabalho com prazo de cinco meses,
o argumento de viabilidade fica concreto: configurar plataforma existente e
desenvolver sistema próprio não são caminhos comparáveis em custo.

**2. O DsGov é referência a considerar na E29.** Se o painel de visualização for
executado, seguir o Design System do Governo Brasileiro dá padronização visual e
de acessibilidade compatível com instituição federal, sem custo de design. Vale
registrar como opção, observado que a etapa é condicional.

**3. Dashboards públicos e SSO como pontos de comparação.** A ideia de painel
público aparece aqui, no RAEG e no Alumni USP, o que confirma ser expectativa
corrente. Já o SSO institucional é relevante para o contraste com o acesso por
token: o sistema da UFU pretende autenticar o egresso pela identidade
institucional, enquanto o desenho deste projeto usa token individual por convite —
que não exige que o egresso mantenha credencial ativa na instituição anos após a
formatura.

## Limitações da fonte

- **Sistema incompleto.** Backend em andamento e integrações adiadas. Não há
  sistema em produção nem coleta realizada.
- **Nenhuma avaliação empírica.** Não há teste com usuários, avaliação de
  usabilidade, nem qualquer medição. A conclusão de que a aplicação "facilita o
  acompanhamento" é afirmação do autor sobre um artefato que ainda não foi usado
  para acompanhar ninguém.
- **Sem informação sobre proteção de dados.** O trabalho trata de interface para
  gestão de informações acadêmicas e profissionais de pessoas identificadas, e o
  resumo não menciona consentimento, base legal ou anonimização.
- **Escopo restrito à camada de apresentação.** Para as questões centrais deste
  projeto — rastreabilidade, automação de cobrança, conformidade — a fonte
  contribui pouco em substância. Seu uso aqui é como termo de comparação de custo
  e como referência de padrão visual.
