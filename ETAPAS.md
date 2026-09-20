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

### [~] E02 — Fichar as fontes da pesquisa
- **Objetivo:** consolidar as referências já levantadas em fichamentos utilizáveis.
- **Entregável:** um arquivo por fonte em `docs/pesquisa/fichamentos/`, com
  problema identificado, método, resultado e implicação para o projeto.
- **Conclusão quando:** todas as referências do projeto estiverem fichadas.
- **Em andamento:** 17 fontes identificadas no documento do projeto e indexadas em
  `docs/pesquisa/fichamentos/README.md`. Modelo definido. 8 fichadas, 9 pendentes.
  Três correções de referência detectadas e registradas no índice.

### [ ] E03 — Analisar o instrumento vigente (linha de base)
- **Objetivo:** caracterizar as limitações do questionário institucional atual.
- **Entregável:** `docs/pesquisa/linha-de-base.md` cobrindo modo de acesso,
  identificação do respondente, padronização dos campos, mecanismos de cobrança
  e registro de consentimento.
- **Conclusão quando:** cada limitação estiver associada à dificuldade correspondente na literatura.
- **Atenção:** análise documental apenas. Não responder, não coletar, não contatar ninguém.

### [ ] E04 — Montar o quadro comparativo de estratégias de engajamento
- **Objetivo:** sistematizar o que outras instituições fizeram e com que efeito.
- **Entregável:** `docs/pesquisa/quadro-engajamento.md` com instituição,
  estratégia, efeito observado, limitação e implicação técnica.
- **Conclusão quando:** cobrir busca ativa, aceite eletrônico, mala direta,
  mobilização por turmas e contrapartidas ao egresso.

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
  qualquer aplicação futura junto a egressos reais.

---

## Registro de sessões

Uma linha por sessão, mais recente ao final.

| Data | Etapas trabalhadas | Situação ao encerrar | Pendências |
|------|--------------------|----------------------|------------|
| 20/09/2026 | E01 | Concluída. Repositório público publicado e sincronizado. | Python não instalado na máquina (necessário em E16 e E28). `.gitattributes` não criado. Titularidade do copyright a confirmar (hoje em nome do autor). |
