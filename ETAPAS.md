# Etapas do Projeto

Sequenciamento oficial. Uma etapa por sessão, na ordem, salvo combinação em contrário.

Legenda de status: `[ ]` pendente · `[~]` em andamento · `[x]` concluída · `[-]` dispensada

---

## Fase 1 — Revisão da literatura, linha de base e engajamento
Meta 1 · ago–set/26

### [x] E01 — Preparar e publicar o repositório
- **Objetivo:** deixar o repositório operacional e versionado.
- **Entregável:** repositório Git inicializado, `.gitignore` aplicado, primeiro
  commit, repositório público criado no GitHub e sincronizado.
- **Conclusão quando:** o repositório estiver acessível no GitHub com a estrutura completa.
- **Atenção:** manter a pasta fora do OneDrive para evitar corrupção do `.git`.
- **Concluída em:** 20/09/2026 · repositório em https://github.com/matheusreisl/projeto-egressos-ifsp-estrutura
- **Registro:** commit inicial `9583ec9`, branch `main`, 16 arquivos. Licença MIT
  aplicada, resolvendo a pendência do README. Pasta confirmada fora do OneDrive.
  `CLAUDE.md` e `.claude/` mantidos fora do versionamento a pedido.

### [x] E02 — Fichar as fontes da pesquisa
- **Objetivo:** consolidar as referências já levantadas em fichamentos utilizáveis.
- **Entregável:** um arquivo por fonte em `docs/pesquisa/fichamentos/`, com
  problema identificado, método, resultado e implicação para o projeto.
- **Conclusão quando:** todas as referências do projeto estiverem fichadas.
- **Concluída em:** 20/09/2026 · 17 de 17 fontes fichadas por leitura do original,
  indexadas em `docs/pesquisa/fichamentos/README.md`.
- **Registro:** modelo de fichamento definido, com campo de limitações obrigatório
  e rastreabilidade para as etapas que cada fonte alimenta. Duas fontes foram
  fichadas por leitura parcial (Ferreira 2026, pelo resumo; Davis 1989, por
  extração incompleta) e estão marcadas para releitura.

### [x] E03 — Analisar o instrumento vigente (linha de base)
- **Objetivo:** caracterizar as limitações do questionário institucional atual.
- **Entregável:** `docs/pesquisa/linha-de-base.md` cobrindo modo de acesso,
  identificação do respondente, padronização dos campos, mecanismos de cobrança
  e registro de consentimento.
- **Conclusão quando:** cada limitação estiver associada à dificuldade correspondente na literatura.
- **Atenção:** análise documental apenas. Não responder, não coletar, não contatar ninguém.
- **Concluída em:** 20/09/2026 · `docs/pesquisa/linha-de-base.md`.
- **Registro:** instrumento caracterizado por análise documental, sem que fosse
  percorrido — avançar entre páginas do LimeSurvey exige POST e criaria registros
  fictícios na base real. A estrutura foi reconstruída pelos Relatórios 1 e 2 da
  PAE, que publicam enunciados, domínios e contagens.
- **Achados:** o instrumento vigente já roda em LimeSurvey, em modo aberto, com os
  recursos de rastreabilidade não acionados; 30 questões em 7 blocos, com
  bifurcação condicional na questão 15 confirmada pelos dados; 2.519 registros
  desde 2015, sem denominador que permita calcular cobertura; nenhum registro de
  consentimento nas camadas verificadas. A exigência normativa está no Indicador
  3.7 do Instrumento de Avaliação Institucional Externa do INEP, e não na Lei do
  SINAES, que não menciona egresso.
- **Achado normativo:** a Portaria Normativa nº 128/2025 (Regulamento) foi
  recuperada e determina, no art. 16, link individual por egresso, convite por
  e-mail com fallback para mensagens instantâneas, disparo automatizado e repetido
  e periodicidade anual. Nada disso está implementado. A lacuna é de suporte
  técnico, não de norma — o mecanismo do projeto viabiliza o que já é exigido.
- **Regulamento recuperado por inteiro**, inclusive os anexos. O art. 25 declara
  conformidade com a LGPD, em cláusula genérica que não desce a base legal,
  consentimento, retenção nem anonimização. O Anexo I define dezenove indicadores
  institucionais, reproduzidos no Anexo A da linha de base — insumo direto da E12.

### [x] E04 — Montar o quadro comparativo de estratégias de engajamento
- **Objetivo:** sistematizar o que outras instituições fizeram e com que efeito.
- **Entregável:** `docs/pesquisa/quadro-engajamento.md` com instituição,
  estratégia, efeito observado, limitação e implicação técnica.
- **Conclusão quando:** cobrir busca ativa, aceite eletrônico, mala direta,
  mobilização por turmas e contrapartidas ao egresso.
- **Concluída em:** 20/09/2026 · `docs/pesquisa/quadro-engajamento.md`.
- **Registro:** onze estratégias sistematizadas — as cinco do critério (busca ativa,
  aceite eletrônico, mala direta, mobilização por turmas, contrapartidas) e mais seis
  que emergiram dos fichamentos (convite individual sobre lista fechada, redução do
  esforço de resposta, divulgação institucional, janela longa de coleta, periodicidade
  definida, portal centralizado). Nenhuma fonte nova foi levantada: o quadro
  reorganiza, sob o recorte do engajamento, o que a E02 e a E03 já haviam lido.
- **Achado principal — o estado da evidência.** Nenhuma fonte isola o efeito de uma
  estratégia sobre a participação. Das onze linhas, **uma** tem efeito medido (os
  35,4% de Coelho e Silva, e mesmo esse confunde convite inicial com busca ativa),
  cinco são relatadas sem separação e cinco não foram avaliadas. O quadro declara o
  estado da evidência em cada linha e não é comparação de desempenho.
- **Consequência direta para a E05:** o quadro **não fornece** número de lembretes,
  intervalo entre disparos nem limite de tentativas — nenhuma fonte os informa. Os
  três terão de ser fixados como decisão de projeto justificada, com registro de que
  não derivam de efeito medido. O que vem pronto da norma é a periodicidade anual, o
  e-mail como canal primário e o fallback por mensagens instantâneas.
- **Achado normativo:** sete das onze estratégias já têm dispositivo expresso na
  norma do IFSP (Regulamento, arts. 14, 16, 19, 22 e 25; PAEg, art. 8º) e nenhuma
  está implementada. Reforça, por outro ângulo, a conclusão da E03: a lacuna é de
  suporte técnico, não de norma.
- **Risco registrado para E24 e E30:** difundir um endereço único em grupo de turma
  ou em campanha aberta anula a rastreabilidade. Mobilização por turmas e convite
  individual não podem compartilhar a mesma URL.
- **Distinção nova, que as fontes não fazem:** busca ativa *reparadora* (corrige o
  cadastro) e contato por *canal alternativo* (entrega o convite por outra via)
  exigem coisas diferentes do mecanismo. Insumo de E05, E11 e E21.

### [ ] E05 — Derivar os parâmetros de contato
- **Objetivo:** transformar o quadro anterior em parâmetros justificados.
- **Entregável:** `docs/especificacao/parametros-contato.md` com número de
  lembretes, intervalos, limite de tentativas, tratamento da recusa, remetente
  e verificação de entrega — cada um com sua justificativa.
- **Conclusão quando:** todo parâmetro tiver fundamento rastreável ao quadro.

---

## Fase 2 — Implantação da instância própria
Meta 2 · ago–set/26

### [ ] E06 — Decidir o ambiente de execução (ADR-0002)
- **Objetivo:** escolher entre Docker no WSL2, VM local ou nuvem em camada gratuita.
- **Entregável:** `docs/decisoes/0002-ambiente-execucao.md` preenchido, com
  critérios, alternativas avaliadas, decisão e consequências.
- **Conclusão quando:** a decisão estiver registrada e justificada.
- **Critérios sugeridos:** custo zero, facilidade de reprodução por terceiros,
  suporte a tarefa agendada, viabilidade de envio de e-mail, portabilidade.

### [ ] E07 — Provisionar o ambiente escolhido
- **Objetivo:** ter o ambiente base funcionando.
- **Entregável:** artefatos de provisionamento em `infra/`.
- **Conclusão quando:** o ambiente subir do zero seguindo apenas o que está versionado.
- **Recolhe as pendências de releitura de fonte.** Ferreira (2026) e Davis (1989)
  foram fichados por leitura parcial porque esta máquina não extraiu o texto dos
  PDFs — a mesma carência de ferramenta que deixou o Python pendente. Ao provisionar
  o ambiente, instalar o que resolve extração de texto e OCR, e então reler as duas
  fontes e atualizar os fichamentos. Ferreira é a que pesa: já está citada na linha
  de base, no quadro de engajamento e na fundamentação do documento do projeto.
- **Também recolhe o `.gitattributes`**, ainda não criado. Passa a importar aqui,
  quando os primeiros artefatos de shell entram no repositório e a normalização de
  fim de linha deixa de ser cosmética.

### [ ] E08 — Instalar o LimeSurvey e validar o acesso
- **Objetivo:** instância operacional com painel administrativo acessível.
- **Entregável:** instância instalada; registro da versão e das configurações aplicadas.
- **Conclusão quando:** for possível criar um questionário de teste e acessá-lo.

### [ ] E09 — Configurar e verificar o envio de mensagens
- **Objetivo:** garantir que a instância envia e-mail, pré-requisito da automação.
- **Entregável:** configuração de SMTP documentada, sem credenciais versionadas.
- **Conclusão quando:** um envio de teste chegar a endereço sob domínio controlado.

### [ ] E10 — Documentar o procedimento de instalação
- **Objetivo:** iniciar o guia de replicação.
- **Entregável:** `entregas/guia-replicacao.md` com requisitos, passo a passo e
  configurações de segurança aplicadas.
- **Conclusão quando:** um terceiro conseguir reproduzir o ambiente pelo documento.

---

## Fase 3 — Estrutura de dados e campos do instrumento
Meta 3 · set–out/26

### [ ] E11 — Especificar o leiaute do arquivo de entrada
- **Objetivo:** definir o arquivo que popula a base de participantes.
- **Entregável:** `docs/especificacao/leiaute-entrada.md` com campo, descrição,
  tipo, obrigatoriedade e regra de validação.
- **Conclusão quando:** o conjunto for mínimo e suficiente (princípio da necessidade).

### [ ] E12 — Especificar os blocos estruturais do instrumento
- **Objetivo:** definir os contêineres que acolherão as questões.
- **Entregável:** `docs/especificacao/blocos-instrumento.md` com bloco,
  finalidade estrutural e indicador alimentado.
- **Conclusão quando:** nenhum bloco existir sem indicador correspondente.
- **Atenção:** estrutura apenas. Conteúdo temático das questões não entra aqui.

### [ ] E13 — Definir domínios, obrigatoriedade e validações
- **Objetivo:** fechar os domínios de valores e as regras de preenchimento.
- **Entregável:** seção complementar em `blocos-instrumento.md`, incluindo o
  comportamento do pré-preenchimento quando o dado de origem estiver desatualizado.
- **Conclusão quando:** todo campo padronizável tiver domínio fechado.

### [ ] E14 — Definir a lógica de navegação condicional
- **Objetivo:** mapear os caminhos alternativos do instrumento.
- **Entregável:** `docs/especificacao/navegacao-condicional.md` com as regras e um diagrama de fluxo.
- **Conclusão quando:** todos os caminhos previstos estiverem descritos.

### [ ] E15 — Implementar a estrutura no LimeSurvey
- **Objetivo:** materializar a especificação na instância.
- **Entregável:** questionário estruturado; exportação da estrutura versionada em `infra/`.
- **Conclusão quando:** todos os caminhos forem percorríveis manualmente.

---

## Fase 4 — Base sintética e acesso rastreável
Metas 4 e 5 · set–nov/26

### [ ] E16 — Gerar a base sintética
- **Objetivo:** produzir a base de validação.
- **Entregável:** `scripts/gerar_base_sintetica.py` e base de ~500 registros
  distribuídos em 10 anos de conclusão.
- **Conclusão quando:** a base refletir o leiaute de E11 e usar apenas domínio controlado.
- **Atenção:** nenhum dado de pessoa real, nem parcial, nem "de exemplo".

### [ ] E17 — Importar a base e ativar a tabela de participantes
- **Objetivo:** converter o questionário para acesso controlado.
- **Entregável:** base importada; registro do procedimento.
- **Conclusão quando:** todos os registros forem criados sem duplicidade.
- **Gera ADR.** É aqui que a base persistente de participantes passa a existir, e
  essa é uma decisão de arquitetura com fundamento em princípio legal, não uma
  escolha de implementação. O RAEG (Praga de Souza et al., 2025) optou pelo
  contrário — **não** manter base fixa de participantes, em nome da minimização de
  dados. Este projeto opta pela base persistente porque ela é a condição da
  rastreabilidade, e endereça o risco por consentimento (E22), anonimização e
  trilha de auditoria (E23). São escolhas legítimas e opostas diante do mesmo
  princípio da necessidade, e há literatura no caminho oposto: registrar em ADR,
  conforme recomendado no fichamento do RAEG.

### [ ] E18 — Configurar acesso por token e pré-preenchimento
- **Objetivo:** endereço individual por participante, com atributos pré-carregados.
- **Entregável:** configuração aplicada e documentada.
- **Conclusão quando:** um acesso de amostra abrir com os atributos corretos.

### [ ] E19 — Validar unicidade e deduplicação
- **Objetivo:** garantir integridade da base de participantes.
- **Entregável:** registro da verificação.
- **Conclusão quando:** nenhum token repetido ou inválido for encontrado.

---

## Fase 5 — Automação do contato e conformidade
Metas 6 e 7 · out–nov/26

### [ ] E20 — Configurar convites e modelos de mensagem
- **Objetivo:** preparar o disparo inicial.
- **Entregável:** modelos de convite e lembrete, com remetente e assunto padronizados.
- **Conclusão quando:** o convite de teste chegar corretamente formatado.

### [ ] E21 — Configurar a rotina agendada de lembretes
- **Objetivo:** automatizar a cobrança conforme os parâmetros de E05.
- **Entregável:** rotina agendada ativa; procedimento em `infra/`.
- **Conclusão quando:** o disparo executar no horário e atingir só os não respondentes.

### [ ] E22 — Implementar consentimento eletrônico
- **Objetivo:** registrar aceite conforme a LGPD.
- **Entregável:** tela inicial de consentimento com registro de aceite, data e versão do termo.
- **Conclusão quando:** o aceite for persistido e recuperável.

### [ ] E23 — Configurar anonimização e trilha de auditoria
- **Objetivo:** completar os controles de conformidade.
- **Entregável:** parametrização aplicada e documentada, incluindo tratamento da recusa.
- **Conclusão quando:** a recusa interromper novos disparos.

### [ ] E24 — Documentar recomendações que dependem de terceiros
- **Objetivo:** registrar o que não será executado mas deve constar.
- **Entregável:** seção no guia de replicação sobre divulgação em colação de grau,
  grupos de turma e ações dirigidas a turmas antigas.
- **Conclusão quando:** cada recomendação estiver ligada à evidência da literatura.

---

## Fase 6 — Validação por simulação controlada
Meta 8 · nov–dez/26

### [ ] E25 — Montar a matriz de verificação executável
- **Objetivo:** transformar a matriz do projeto em roteiro aplicável.
- **Entregável:** `docs/especificacao/matriz-verificacao.md` com requisito,
  procedimento, resultado esperado e campo para resultado obtido.
- **Conclusão quando:** os 12 requisitos do projeto estiverem contemplados.

### [ ] E26 — Executar os cenários de simulação
- **Objetivo:** exercitar o mecanismo sob condições previstas em operação real.
- **Entregável:** execução dos cenários de preenchimento parcial com retomada,
  ausência de resposta, contato inválido e recusa.
- **Conclusão quando:** todos os cenários tiverem resultado registrado.

### [ ] E27 — Registrar resultados e corrigir desvios
- **Objetivo:** fechar o ciclo de validação.
- **Entregável:** matriz preenchida; correções aplicadas e reexecutadas.
- **Conclusão quando:** todos os requisitos forem atendidos ou o desvio estiver justificado.

---

## Fase 7 — Resultados, documentação e fechamento
Metas 9 e 10 · out–dez/26

### [ ] E28 — Extrair os resultados da simulação
- **Objetivo:** obter os dados de forma programática.
- **Entregável:** rotina de extração via API do LimeSurvey e conjunto exportado.
- **Conclusão quando:** a extração for reproduzível por comando.

### [ ] E29 — Painel de visualização (CONDICIONAL)
- **Objetivo:** apresentar os indicadores de forma agregada.
- **Entregável:** painel funcional com atenção a níveis de acesso multicampi.
- **Conclusão quando:** os indicadores forem exibidos a partir dos dados extraídos.
- **Atenção:** só iniciar após E01–E28. Se o prazo não comportar, especificar
  como trabalho futuro e marcar esta etapa como dispensada.

### [ ] E30 — Consolidar o guia de replicação
- **Objetivo:** entregar o artefato replicável por outras instituições.
- **Entregável:** `entregas/guia-replicacao.md` completo.
- **Conclusão quando:** cobrir instalação, configuração, estrutura, automação e conformidade.

### [ ] E31 — Redigir o relatório final
- **Objetivo:** fechar a produção científica.
- **Entregável:** relatório final e rascunho de artigo/resumo expandido.
- **Conclusão quando:** incluir a recomendação de apreciação ética prévia a
  qualquer aplicação futura junto a egressos reais **e** nenhuma pendência de fonte
  permanecer em aberto.
- **Recolhe as conferências de referência.** Cada uma está anotada no fichamento
  correspondente, contra PDF já localizado:
  - **RANTHUM e SANTOS JUNIOR (2023)** — o fichamento não registra a instituição de
    aplicação da ferramenta; o documento do projeto a atribui à Universidade
    Paranaense. Conferir.
  - **PRAGA DE SOUZA et al. (2025)** — divergência de autoria entre o PDF (dois
    autores) e a página do periódico (três). Adotou-se a citação da página.
  - **IFSP — RN nº 13/2022** — a numeração de artigos veio corrompida do OCR
    ("Art. IP", "Art. Y"). Conferir no PDF original todo dispositivo citado.
- **Mello et al. (2023)** — avaliação do SAVE pela perspectiva do egresso, ausente
  das 17 referências. É a única fonte que traria o lado do respondente a um conjunto
  hoje formado só por gestores e coordenadores. Localizar e incorporar ao quadro de
  engajamento ou, não sendo possível, declarar a ausência como limitação do quadro.
- **Titularidade do copyright** a confirmar antes da entrega: a licença MIT nomeia
  um titular, e o repositório é público. Definir se o titular é o estudante, a
  orientação ou o IFSP, e ajustar o `LICENSE` se for o caso.

---

## Registro de sessões

Uma linha por sessão, mais recente ao final.

| Data | Etapas trabalhadas | Situação ao encerrar | Pendências |
|------|--------------------|----------------------|------------|
| 20/09/2026 | E01, E02, E03 | E01 a E03 concluídas. Repositório publicado; 17 fontes fichadas; linha de base do instrumento vigente. | Reler Ferreira 2026 e Davis 1989 na íntegra. Python não instalado (E16, E28). `.gitattributes` não criado. Titularidade do copyright a confirmar. |
| 20/09/2026 | E04 | E04 concluída. Quadro de engajamento com onze estratégias, estado da evidência declarado por linha e cruzamento com a norma do IFSP. Pendências de fonte passaram a ter etapa responsável. | Nenhuma pendência sem dono. Releituras de fonte (Ferreira 2026, Davis 1989) e `.gitattributes` → E07, junto com a ferramenta de extração e OCR. Conferências de referência (Ranthum, Praga de Souza, OCR da RN 13/2022), Mello et al. (2023) e titularidade do copyright → E31. Python não instalado segue marcado para E16 e E28. |
