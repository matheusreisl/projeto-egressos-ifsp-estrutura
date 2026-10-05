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

### [x] E05 — Derivar os parâmetros de contato
- **Objetivo:** transformar o quadro anterior em parâmetros justificados.
- **Entregável:** `docs/especificacao/parametros-contato.md` com número de
  lembretes, intervalos, limite de tentativas, tratamento da recusa, remetente
  e verificação de entrega — cada um com sua justificativa.
- **Conclusão quando:** todo parâmetro tiver fundamento rastreável ao quadro.
- **Concluída em:** 20/09/2026 · `docs/especificacao/parametros-contato.md`.
- **Registro:** nove parâmetros especificados — os seis do critério, mais convite
  inicial, janela do ciclo e canal alternativo, que a E04 apontara como
  necessários e que o documento do projeto não enuncia. Cada um recebeu rótulo de
  origem (`norma` / `quadro` / `projeto`), na mesma lógica da escala de evidência
  da E04.
- **Ressalva ao critério de conclusão.** "Fundamento rastreável ao quadro" foi
  atendido, mas três parâmetros — cadência, limite de tentativas e remetente —
  rastreiam ao quadro **pela ausência**: a seção 8 da E04 declara que nenhuma
  fonte os informa e os remete à E05 como decisão de projeto. Oito dos nove têm
  algum componente de decisão de projeto; só o convite individual é integralmente
  determinado por fora.
- **Descoberta que mudou o desenho da etapa:** o documento do projeto **já
  propunha** os sete parâmetros, com valores fechados. A etapa não os inventou —
  manteve os valores e corrigiu a atribuição de origem, porque o documento afirma
  que derivam da literatura e a E04 demonstrou que três não derivam.
- **Decisões tomadas** (confirmadas com o orientando antes da execução):
  - **Cadência** D+4/D+7/D+14 mantida, agora com faixa admissível declarada
    (primeiro lembrete entre D+3 e D+7, intervalo mínimo de 3 dias entre disparos
    consecutivos, último não depois de D+21). Fora da faixa exige ADR.
  - **Recusa** desdobrada em duas, resolvendo a pergunta que a E04 deixou aberta:
    *recusa de consentimento* encerra o ciclo corrente e o egresso volta no ciclo
    seguinte; *recusa de contato* é permanente até revogação expressa, com via de
    reversão tão simples quanto a manifestação.
  - **Janela do ciclo** de 60 dias corridos. O que fixou o número foi o ciclo de
    reparo de contato — detecção do erro, correção, reconvite e cadência própria
    precisam caber inteiros na janela —, e não a folga após o último lembrete.
- **Achado normativo:** os gatilhos dos arts. 14, 19 e 22 do Regulamento são **um
  só ciclo**. Ancorando-o no semestre de conclusão da turma, a "campanha de dois
  anos após a formatura" é o terceiro ciclo anual dessa mesma sequência — não
  acrescenta disparo. Uma regra em vez de três rotinas sobrepostas.
- **Gerou ADR-0003** — canal alternativo de convite (art. 16, §1º) sem automação.
- **Pendência encaminhada para a E31:** corrigir, na próxima versão do documento
  do projeto, a afirmação de que os parâmetros de contato "derivam das
  experiências sistematizadas na revisão da literatura". Os valores ficam; a
  atribuição de origem muda. Sem alteração de escopo, valor ou cronograma.

---

## Fase 2 — Implantação da instância própria
Meta 2 · ago–set/26

### [x] E06 — Decidir o ambiente de execução (ADR-0002)
- **Objetivo:** escolher entre Docker no WSL2, VM local ou nuvem em camada gratuita.
- **Entregável:** `docs/decisoes/0002-ambiente-execucao.md` preenchido, com
  critérios, alternativas avaliadas, decisão e consequências.
- **Conclusão quando:** a decisão estiver registrada e justificada.
- **Critérios sugeridos:** custo zero, facilidade de reprodução por terceiros,
  suporte a tarefa agendada, viabilidade de envio de e-mail, portabilidade.
- **Concluída em:** 21/09/2026 · `docs/decisoes/0002-ambiente-execucao.md`.
- **Decisão:** **conteinerização declarativa em máquina local** — Docker Engine e
  Docker Compose, composição inteira (LimeSurvey, banco, serviço de correio e
  rotina agendada) declarada em arquivo versionado em `infra/`, em rede fechada.
  O WSL2 é o hospedeiro **desta** máquina e foi explicitamente registrado como
  substrato trocável, não como parte da decisão: a mesma composição sobe em Linux
  nativo, macOS ou servidor institucional.
- **Registro:** cinco alternativas avaliadas contra sete critérios. Estado da
  máquina verificado antes de decidir (WSL 2.7.10 presente **sem distribuição**,
  Docker ausente, virtualização ativa) — nada foi afirmado sem conferência.
- **Dois critérios acrescentados aos cinco sugeridos.** **K6 — contenção do
  disparo:** a restrição "nunca disparar para endereços reais" vinha sendo tratada
  como regra de conduta, e a escolha de ambiente é o único momento em que pode
  virar propriedade do ambiente. Em rede fechada com correio próprio, a mensagem
  não tem rota de saída; um endereço equivocado produz devolução interna, não
  mensagem real a um desconhecido. **Foi este critério que decidiu a etapa.**
  **K7 — operação integral por linha de comando:** pré-condição da reprodução por
  terceiros, porque o guia da E30 é feito de comandos, não de capturas de tela.
- **Domínio dos ensaios fixado:** TLD reservado `.test` (RFC 2606/6761), que não
  resolve na internet pública. Dá conteúdo concreto à expressão "domínio
  controlado pelo projeto", usada desde a E05 sem ambiente que a materializasse.
- **Docker Desktop descartado por licença, não por técnica.** O Engine é Apache 2.0
  sem limiar; o Desktop exige assinatura acima de 250 funcionários ou US$ 10 mi de
  receita. Um Instituto Federal não cabe no limiar, e a instituição replicante não
  pode ser presumida cabendo. Resultado técnico idêntico, sem nota de rodapé no guia.
- **Custo assumido e declarado:** a rotina agendada só executa com a máquina ligada.
  Aceitável porque a Fase 6 é simulação com compressão temporal declarada (E26).
  Vira limitação a enunciar na E31 — não se poderá afirmar que a rotina se sustenta
  por um ciclo anual em relógio real.
- **Risco novo registrado:** não há imagem de contêiner publicada pelo projeto
  LimeSurvey; as de uso corrente são comunitárias. Decisão explícita na E07 —
  imagem comunitária de referência ou imagem própria a partir do código oficial —,
  com fixação por digest em qualquer dos casos.

### [x] E07 — Provisionar o ambiente escolhido
- **Objetivo:** ter o ambiente base funcionando.
- **Entregável:** artefatos de provisionamento em `infra/`.
- **Conclusão quando:** o ambiente subir do zero seguindo apenas o que está versionado.
- **Concluída em:** 21/09/2026 · `infra/` · **ADR-0004**.
- **Ambiente de pé e conferido.** Ubuntu 24.04.5 LTS sobre WSL2 com `systemd`,
  Docker Engine 29.8.1, Compose v5.5.1. Composição com LimeSurvey 7.2.0+260921 e
  MariaDB 11.4.13. `verifica-ambiente.sh` — também artefato versionado —
  executa **21 conferências, todas passando**.
- **Critério de conclusão verificado por execução, não por afirmação.** Volumes e
  imagem construída foram **destruídos** (`docker compose down -v` mais remoção da
  imagem) e o ambiente **reconstruído do nada em 24 s**, com as 21 conferências
  passando outra vez. *Ressalva honesta:* essa segunda subida reaproveitou o cache
  de camadas do Docker. O caminho completo — descarga do pacote, conferência da
  soma e compilação das extensões — foi exercitado na **primeira** construção, que
  era fria por não existir cache algum. As duas execuções somadas cobrem o
  percurso; nenhuma delas sozinha o cobriria.
- **Artefatos criados:** `compose.yml`, `.env.exemplo`, `limesurvey/Dockerfile`,
  `hospedeiro/provisiona-docker.sh`, `hospedeiro/provisiona-ferramentas.sh`,
  `verifica-ambiente.sh` e o `README.md` com o procedimento — que é a semente do
  guia da E10. O `.gitignore` ganhou exceção para `.env.exemplo`, que a regra
  `.env.*` estava engolindo.
- **Imagem própria, decidida com o orientando e registrada na ADR-0004.** Não há
  imagem publicada pelo projeto LimeSurvey. O Dockerfile fixa a imagem base por
  digest e o pacote por versão **e soma SHA-256**, conferida antes de descompactar
  — verificado em construção real (`/tmp/limesurvey.zip: OK`).
- **Achado que redirecionou a etapa e gerou a segunda metade da ADR-0004.** A
  extensão `imap` do PHP, que o manual do LimeSurvey declara necessária ao
  rastreamento de devoluções — o P8 —, **não compila mais na base atual**: a
  biblioteca UW-IMAP foi removida do Debian 13 e a extensão saiu do núcleo do PHP
  na 8.4. Decidido, com o orientando: base atual sem `imap`, e a leitura de
  devoluções passa a ser **rotina própria**. O argumento é que as regras do P8 são
  do projeto e o recurso nativo não as implementa — a lógica teria de ser escrita
  de qualquer modo.
- **Contenção do K6 verificada por experimento, não por leitura de documentação.**
  Rede `internal` do Docker **não permite publicar porta** — conferido duas vezes,
  com e sem vínculo a 127.0.0.1. Daí a topologia de duas redes: banco e correio
  ficam só na interna, sem rota de saída nem resolução de nome externo; o
  LimeSurvey fica em ambas, porque publicar porta exige. **A contenção do caminho
  do correio é integral; o contêiner do LimeSurvey mantém saída HTTP** — dito assim
  no `infra/README.md`, sem arredondar.
- **Erro meu, corrigido antes de virar documentação falsa.** Diagnostiquei que o
  painel não respondia do Windows por causa do endereço de vínculo, e cheguei a
  escrever isso no README. Testado: com `127.0.0.1` e reinício limpo do WSL, o
  Windows alcança normalmente. A causa real é **encaminhamento obsoleto do WSL após
  a distro ser reaberta no meio da sessão**, e o sintoma engana porque o acesso pelo
  IP da distro continua funcionando. Registrado no README com a pista falsa nomeada.
- **Linha 6.x do LimeSurvey encerrou suporte em 31/08/2026.** A 7.x é a única
  linha suportada. Registrado na ADR-0004.
- **Releituras de fonte — encerradas.** Ferramenta instalada (poppler 24.02,
  tesseract 5.3.4 com português, ocrmypdf 15.2, Python 3.12.3), e as duas fontes
  foram relidas **na íntegra**, sem precisar de OCR: ambas tinham camada de texto,
  e o que faltava antes era a ferramenta.
  - **Ferreira (2026)** — duas correções materiais. O método **não** é coleta de
    perfis públicos: o algoritmo **autentica-se no LinkedIn** antes de percorrer os
    perfis. Isso **reforça** o descarte da raspagem por este projeto, pelo mesmo
    critério da ADR-0003, em vez de enfraquecê-lo. E a cobertura é de **103 perfis
    em 127 formados (≈81%)** — alta, mas sobre coorte pequena, recente e de área de
    tecnologia, sem base para transposição. Corrigidos grau e número de folhas.
    `quadro-engajamento.md` atualizado nos dois pontos.
  - **Davis (1989)** — uma correção material: os "n" de 184 e 80 somam *avaliações*,
    não pessoas; são **112** e **40** participantes. Acrescentada a natureza
    **prospectiva** do Estudo 2, que delimita o alcance de avaliações de protótipo
    por TAM — a do SAVE, entre elas.
- **Python deixou de ser pendência.** Instalado no ambiente (3.12.3), o que resolve
  o que estava marcado para **E16** e **E28**.
- **Também recolhe o `.gitattributes`**, ainda não criado. Passa a importar aqui,
  quando os primeiros artefatos de shell entram no repositório e a normalização de
  fim de linha deixa de ser cosmética.
- **Lista fechada pela E06** (ADR-0002): instalar a distribuição Linux no WSL2 com
  `systemd` habilitado; instalar o **Docker Engine** na distribuição, não o Docker
  Desktop; escrever a composição em `infra/` com `.env.exemplo` sem valores reais;
  **fixar todas as imagens por digest**. A rede da composição é fechada, sem rota
  de saída para a internet.
- **Decisão que esta etapa precisa tomar explicitamente:** imagem comunitária de
  referência do LimeSurvey ou imagem própria construída a partir do código oficial.
  Não há imagem publicada pelo projeto LimeSurvey. Registrar a escolha e o digest.

### [x] E08 — Instalar o LimeSurvey e validar o acesso
- **Objetivo:** instância operacional com painel administrativo acessível.
- **Entregável:** instância instalada; registro da versão e das configurações aplicadas.
- **Conclusão quando:** for possível criar um questionário de teste e acessá-lo.
- **Conferência que a E06 encaminhou para cá.** É a primeira etapa com instância
  viva, e portanto a primeira em que as **capacidades C1 a C10** da seção 13 de
  `parametros-contato.md` deixam de ser especulação. Conferir uma a uma contra a
  instância e registrar o resultado — a E05 declarou expressamente que afirmar o
  que o LimeSurvey faz nativamente, antes disso, seria asserção sem conferência.
- **Ponto de partida pronto.** O ambiente já está de pé (E07): o instalador do
  LimeSurvey responde em `http://localhost:8080`. Esta etapa faz a instalação
  propriamente dita e registra a versão.
- **Conferir junto (ADR-0004):** o pacote da linha 7.x vem do caminho oficial
  `latest-master`, nome que sugere compilação de desenvolvimento embora seja a via
  que a página oficial apresenta como versão corrente. Confirmar contra a instância
  instalada ao registrar a versão.
- **Concluída em:** 22/09/2026 · `docs/especificacao/capacidades-plataforma.md` ·
  `infra/confere-capacidades.py`.
- **Instalada e registrada:** LimeSurvey **7.2.0 build 260921**, DBVersion 716,
  sobre PHP 8.3.33 e MariaDB 11.4.13. Configuração aplicada e registrada:
  `urlFormat=path`, `RPCInterface=json`, `debug=0`, prefixo `lime_`, `utf8mb4`,
  fuso `America/Sao_Paulo`.
- **A instalação virou desatendida e idempotente.** A inicialização do contêiner
  gera o `config.php` a partir do `.env` e roda o instalador de console quando o
  banco está vazio — verificado por `down -v` seguido de `up -d`, que devolve
  instância pronta sem passo manual. Atende o critério K7 da ADR-0002 e dá à E10
  um procedimento executável em vez de capturas de tela. A senha do administrador
  **não** é gravada no `config.php`.
- **Capacidades C1 a C10 conferidas contra a instância viva: 7 atendem, 3 parciais,
  nenhuma ausente.** Verificação por execução — questionário de teste criado,
  participantes sintéticos sob domínio `.test`, esquema e comportamento
  inspecionados, cenário removido sem resíduo. O verificador ficou versionado.
- **Quanto ao `latest-master`:** o pacote declara `versionnumber` 7.2.0 e
  `buildnumber` 260921, e a instância reporta os mesmos valores. **Não se pôde
  verificar** se o caminho distingue linha estável de desenvolvimento — isso não
  é inferível do artefato. Consequência prática nula, porque a versão está fixada
  por soma de verificação.
- **Achado que corrige toda consulta direta ao banco:** no LimeSurvey 7 a tabela
  de respostas é **`lime_responses_<sid>`**, e não `lime_survey_<sid>`, que é o
  nome usado pela documentação e pelos tutoriais antigos. Custou-me um diagnóstico
  errado antes de encontrar.
- **Achado que precisa a máquina de estados da E05:** abrir o endereço individual
  **não cria linha de resposta**. "Iniciado", na plataforma, é ter submetido ao
  menos uma página. O estado `em preenchimento` da seção 12 de
  `parametros-contato.md` precisa ser lido assim. Coerente com a decisão de não
  rastrear abertura (E05, seção 10.3), mas não óbvio.
- **Achado que evita um bloqueio que não bloqueia:** marcar `blacklisted='Y'` no
  token **não** move o contador de recusa. O que move é `emailstatus='OptOut'`.
  São mecanismos distintos.
- **Duas correções a diagnósticos meus, registradas para não se perderem:**
  cheguei a concluir que o `.lss` de exemplo importava já ativo, deixando o
  questionário em estado inconsistente. **Era falso** nas duas pontas — o pacote
  importa inativo, e o que parecia tabela ausente era eu procurando pelo nome
  antigo.

### [x] E09 — Configurar e verificar o envio de mensagens
- **Objetivo:** garantir que a instância envia e-mail, pré-requisito da automação.
- **Entregável:** configuração de SMTP documentada, sem credenciais versionadas.
- **Conclusão quando:** um envio de teste chegar a endereço sob domínio controlado
  **e** uma devolução de erro for lida e registrada pela instância.
- **Critério ampliado pela E05.** O critério anterior — só a chegada do envio de
  teste — é satisfeito por uma configuração que envia corretamente e não permite
  ler devoluções, e essa configuração inviabiliza o parâmetro P8 (verificação de
  entrega) e o requisito "contato inválido" da matriz do projeto. **Verificar as
  duas direções.**
- **Armadilha nomeada pela E06.** O serviço de correio é do próprio compose, com
  domínio sob `.test`. Atenção: capturadores de SMTP de uso corrente em
  desenvolvimento **aceitam tudo e nunca devolvem erro** — servem para inspecionar
  o envio e não atendem P8. Ver a mensagem chegar ao capturador **não** satisfaz o
  critério desta etapa. É preciso um serviço que devolva erro permanente para caixa
  inexistente do domínio controlado, e verificar isso explicitamente.
- **Escopo ampliado pela E07 (ADR-0004).** A leitura de devoluções **não** usará o
  recurso nativo do LimeSurvey: a extensão `imap` não está na imagem, por decisão
  registrada. Esta etapa passa a incluir a **rotina própria** que lê a caixa,
  classifica conforme P8 (permanente marca na 1ª ocorrência; temporário na 3ª do
  mesmo ciclo) e atualiza o estado. Em Python, mesma via da E28. O serviço de
  correio precisa, em consequência, **expor caixa legível por essa rotina**.
- **Lugar exato na topologia, já preparado:** o serviço de correio entra **somente**
  na rede `interna` do `compose.yml`. É o que garante que mensagem nenhuma saia da
  máquina, qualquer que seja o endereço de destino. Não colocá-lo na rede `externa`.
- **Armadilha achada na E08.** **Não usar `token_invalid` como indicador de contato
  inválido sem antes descobrir o que ele conta.** Definir `emailstatus='invalid'`
  no token **não** moveu esse contador — provavelmente ele se refere a validade
  temporal ou usos restantes, e não a estado de entrega. O que a fila de correção
  da P8 tem de sólido é `emailstatus` e a tabela `lime_failed_emails`, cujo
  esquema já foi conferido e serve.
- **Concluída em:** 27/09/2026 · `docs/especificacao/leitura-devolucoes.md` ·
  `infra/correio/` · `infra/rotinas/` · `scripts/`.
- **Correio de ensaio, em imagem própria.** Postfix mais Dovecot, **somente na
  rede interna**. Não é capturador de SMTP, e a distinção é o ponto: capturador
  aceita tudo e nunca devolve, satisfazendo "vi a mensagem chegar" e
  inviabilizando o P8. Três domínios sob o TLD reservado `.test`, cada um
  produzindo **uma linha** da tabela de classificação da seção 10.1 — entrega,
  erro permanente e erro temporário.
- **Serviço `rotinas` criado, por topologia e não por conveniência.** O correio
  fica só na rede interna, que o hospedeiro não alcança; logo a rotina que lê a
  caixa tem de rodar de dentro dela. Desse contêiner se alcança `correio:143`,
  `limesurvey:80` e `banco:3306`, e **não** a internet — verificado. A **E21** e a
  **E28** reaproveitam esse ponto de execução.
- **Rotina implementada.** `scripts/ler_devolucoes.py` lê a caixa, classifica pelo
  código de estado da RFC 3463, grava em tabela própria `egressos_devolucoes` e
  aplica a regra do P8: permanente marca na primeira ocorrência, temporário só na
  terceira do mesmo ciclo. Chave única sobre mensagem e destinatário dá
  **idempotência** — a mesma devolução lida duas vezes não conta duas.
- **Cliente de API compartilhado** em `scripts/limesurvey_api.py`, que concentra
  os enganos daquela interface num lugar só, em vez de repetidos por rotina.
- **Categoria acrescentada ao P8:** `indeterminado`, para devolução ilegível.
  O P8 pressupõe retorno legível e nem todo servidor real devolve normalizado.
  Tratar o ilegível como permanente marcaria por falha de interpretação; como
  temporário, alimentaria um limiar indevidamente. Registra-se sem agir.
- **Verificação nas duas direções, conforme a seção 10.4 exige.** Dois artefatos,
  com divisão deliberada, **ambos 7 de 7**: `scripts/verifica_correio.py` exercita
  o **correio** por SMTP direto, e `infra/confere-envio.py` exercita a
  **integração**, chamando a rotina de verdade e não uma cópia dela. Devolução
  permanente classificada como `5.1.1 / failed`; temporária como `4.4.1 / delayed`,
  após 124 s.
- **Caminho completo verificado ponta a ponta:** a instância dispara, a mensagem
  chega à caixa coletora, a devolução volta, a rotina classifica, marca o contato
  como inválido, a fila de correção passa a mostrá-lo — e a **recusa permanece
  intacta** (`token_opted_out=0`), o que confere a distinção da seção 10.2.
- **Três detalhes de configuração que decidem se existe devolução a ler**, cada um
  capaz de produzir um ambiente que parece funcionar e no qual o P8 é inexequível:
  `local_recipient_maps` vazio (sem isso a recusa é síncrona e não há devolução);
  `relay_domains` nomeando o domínio indisponível (sem isso vem
  `454 Relay access denied`); e o aviso de atraso, que **não é imediato** — no
  ensaio está reduzido a um minuto, contra horas em implantação real.
- **Quatro armadilhas da API, todas encontradas nesta etapa e concentradas no
  cliente compartilhado.** A **E28 vai encontrar as mesmas**, e todas falham em
  silêncio:
  1. o campo `status` **não** significa erro — carrega mensagem informativa de
     sucesso, como `0 left to send`. O sinal confiável é `error_code`;
  2. **ausência de dados vem como erro** — `ERR_NO_DATA` num ambiente
     recém-criado é o estado esperado, não falha;
  3. a **estrutura de retorno é mista** — em `list_participants`, `email` vem
     aninhado sob `participant_info` e `emailstatus` vem no nível de cima. Ler os
     dois do mesmo lugar devolve campo vazio **sem erro**, e foi isso que me fez
     concluir que uma gravação bem-sucedida não havia pegado: a gravação estava
     correta, a leitura não;
  4. **lista vazia não é "todos"** — `invite_participants` com lista vazia de
     tokens responde "No candidate tokens", que parece falha de configuração.
- **Achado de ambiente, não do desenho.** O relógio da máquina virtual do WSL
  **salta** quando a distribuição suspende e retoma; o Dovecot detecta o salto e
  se recusa a lançar serviços naquele intervalo. O sintoma foi o pior para
  diagnóstico: contêiner saudável, porta aberta, autenticação interna funcionando
  e toda sessão de rede recusada — com um registro mostrando
  `1/1 successful auths in 4294967285 secs`, valor negativo estourado. **Terceiro
  sintoma da mesma raiz.** A verificação de saúde e a supervisão passaram a fazer
  **LOGIN de verdade**, e duas falhas seguidas derrubam o contêiner para que ele
  seja recriado. O serviço passou a se recuperar sozinho — mas a raiz é do
  hospedeiro e é da **E21**.

### [x] E10 — Documentar o procedimento de instalação
- **Objetivo:** iniciar o guia de replicação.
- **Entregável:** `entregas/guia-replicacao.md` com requisitos, passo a passo e
  configurações de segurança aplicadas.
- **Conclusão quando:** um terceiro conseguir reproduzir o ambiente pelo documento.
- **Concluída em:** 27/09/2026 · `entregas/guia-replicacao.md`. **Fase 2 encerrada.**
- **Partes I a III completas**, e IV a VI marcadas como pendentes com a etapa
  responsável de cada uma — de propósito, para que a **E30 preencha em vez de
  reestruturar**. O documento já tem a forma final.
- **Critério verificado por execução, e não por leitura.** Destruí o ambiente,
  inclusive as imagens construídas, **clonei o repositório num diretório novo** e
  segui a Parte II ao pé da letra. Os três verificadores deram exatamente os
  resultados que o guia promete: **21/21**, **7 atendem e 3 parciais**, **7/7**.
  - *Ressalva honesta:* o clone reaproveitou o cache de camadas do Docker, então a
    construção **fria** — com a descarga de 123 MB — não foi reexercitada aqui. Ela
    foi exercitada na E07, quando não havia cache.
- **Defeito de ordem que o teste expôs.** A seção do hospedeiro mandava rodar um
  script **do repositório**, e o clone só aparecia depois. Um terceiro travaria ali.
  O clone passou a vir antes, e as seções foram renumeradas.
- **Números do guia medidos, não estimados.** Imagens: 2,8 GB no total (LimeSurvey
  1,98 GB, banco 455 MB, correio 211 MB, rotinas 190 MB). Memória em repouso: cerca
  de 200 MB nos quatro contêineres somados — uma ordem de grandeza abaixo do que eu
  havia escrito por estimativa.
- **Seção 8 é a espinha do documento:** lista, item por item, o que precisa mudar
  antes de o ambiente tocar dado real — sem TLS, correio sem autenticação,
  interface RPC habilitada, domínios reservados e rede sem saída são ajustes
  deliberados que tornam o ensaio possível e que precisam ser desfeitos.
- **Achado novo, e o quarto sintoma do relógio do WSL — o pior até agora.** Um
  salto **para trás** durante a inicialização do MariaDB faz o certificado que ele
  mesmo acabou de gerar parecer "ainda não válido"; o passo de segurança falha e o
  banco fica **inicializado pela metade**, com `root` e a verificação de saúde sem
  autenticar. Não se recupera por reinício, só recriando o volume.
  - **Tratado desligando o TLS do banco**, o que é coerente com a postura já
    documentada do ambiente — nada mais ali usa TLS, e o banco não publica porta.
  - **Consequência que exigiu ajuste:** o cliente do MariaDB 11.4 **exige** TLS por
    padrão, então as chamadas de cliente precisaram de `--skip-ssl`. Registrado nos
    dois lugares onde isso aparece.
- **Achado operacional para o guia:** a composição tem nome de projeto fixo, então
  **dois clones na mesma máquina compartilham contêineres e volumes** — um
  `down -v` em qualquer um apaga os dados de ambos. Documentado com a saída
  (`COMPOSE_PROJECT_NAME`).
- **Apêndice A reúne as falhas que de fato ocorreram** no desenvolvimento, porque
  em todas o sintoma engana — e em três delas o diagnóstico natural é o errado.

---

## Fase 3 — Estrutura de dados e campos do instrumento
Meta 3 · set–out/26

### [x] E11 — Especificar o leiaute do arquivo de entrada
- **Objetivo:** definir o arquivo que popula a base de participantes.
- **Entregável:** `docs/especificacao/leiaute-entrada.md` com campo, descrição,
  tipo, obrigatoriedade e regra de validação.
- **Conclusão quando:** o conjunto for mínimo e suficiente (princípio da necessidade).
- **Campos que a E05 tornou obrigatórios.** **Mais de uma via de contato**, sem o
  que a fila de correção do parâmetro P8 não tem para onde recorrer e o reparo de
  contato inválido fica decorativo. E o **semestre de conclusão**, que é a âncora
  do ciclo anual em P5 — sem ele não há como aplicar a regra dos arts. 14/19/22.
- **Concluída em:** 28/09/2026 · `docs/especificacao/leiaute-entrada.md` ·
  **ADR-0005**. **Fase 3 iniciada.**
- **Descoberta que mudou o desenho da etapa — a mesma da E05:** o documento do
  projeto **já propunha** o leiaute, com nove campos e a obrigatoriedade de cada
  um, e já atendia às duas exigências da E05. A etapa não o inventou: testou-o
  contra o princípio da necessidade e contra os consumidores que surgiram depois
  dele, e acrescentou o que o entregável pede e o documento não tinha — tipo e
  regra de validação.
- **Leiaute final: dez campos.** Os nove do documento, com a mesma
  obrigatoriedade, mais `nivel`. **Critério verificado nas duas direções:** todo
  campo tem consumidor — parâmetro, capacidade, indicador ou etapa — e todo
  consumidor tem campo; dez campos, onze consumidores, nenhum órfão. Treze
  candidatos ficaram de fora, cada um com o motivo, de CPF e data de nascimento a
  raça/cor e perfis em redes sociais.
- **Decisões tomadas** (confirmadas com o orientando antes da execução):
  - **uma linha por egresso**, com a conclusão mais recente. A P4 e a P5 foram
    escritas por participante, e uma linha por curso daria dois convites por ano
    a quem tem duas formações. Custo declarado: a turma anterior perde o egresso
    quando ele conclui o curso seguinte. Registrada na **ADR-0005**;
  - **`nivel` acrescentado** — técnico, graduação ou pós-graduação. O Ind2 do
    Regulamento conta egressos por nível, e os Ind5 a Ind12 separam técnicos de
    graduação. O documento do projeto não cita o Regulamento, que só foi
    recuperado na E03.
- **Duas precisões que o documento não fazia.** O `identificador` precisa ser
  **estável entre extrações** — sem isso a recusa permanente da P6 não sobrevive
  ao ciclo seguinte — e não pode ser CPF nem o token de acesso; valor com forma de
  CPF, mesmo pontuado, rejeita o registro. E o `nome` é o **nome de tratamento**:
  o social, quando registrado, pelo Decreto nº 8.727/2016, que alcança os
  Institutos Federais por serem autarquias.
- **O leiaute é fechado**, que é a forma operacional da necessidade: coluna a mais
  ou a menos rejeita o arquivo. Há três níveis de consequência — rejeita o arquivo,
  rejeita o registro ou aceita com alerta —, e o relatório de validação não
  reproduz dado pessoal.
- **Restrições do ensaio convertidas em propriedade do arquivo**, como a E06 fez
  com o ambiente: endereço fora de `.test`, ou telefone fora de DDD terminado em 0,
  rejeita o arquivo inteiro. Nenhum dos 67 DDDs em uso termina em zero — conferido
  em fonte secundária, porque a página da Anatel não respondeu; a E16 reconfere.
- **Verificado por execução, e não por leitura.** O exemplo do próprio documento
  passa pelas regras que ele especifica — um registro aceito e outro aceito com
  alerta, como o texto afirma —, os links internos estão íntegros, e a guarda
  contra CPF colide em 1,01% de 200 mil códigos aleatórios, o que confirma o
  "cerca de um em cem" do texto. As normas citadas foram conferidas no texto
  oficial: o Decreto nº 8.727/2016, a LGPD e a Lei nº 11.892/2008, esta já com a
  redação dada pela Lei nº 15.521/2026, que mantém os IFs como autarquias.
- **Não conferido:** a compatibilidade dos tamanhos do leiaute com as colunas da
  plataforma. A leitura do esquema da instância não foi feita nesta sessão, e a
  conferência passa à E17, em que a importação real a exercita.
- **Pendência encaminhada para a E31:** atualizar o leiaute no documento do
  projeto. Sem alteração de escopo, meta ou cronograma.

### [x] E12 — Especificar os blocos estruturais do instrumento
- **Objetivo:** definir os contêineres que acolherão as questões.
- **Entregável:** `docs/especificacao/blocos-instrumento.md` com bloco,
  finalidade estrutural e indicador alimentado.
- **Conclusão quando:** nenhum bloco existir sem indicador correspondente.
- **Atenção:** estrutura apenas. Conteúdo temático das questões não entra aqui.
- **Vindo da E11:** o bloco de identificação acadêmica pré-preenche **cinco**
  atributos — curso, nível, campus, ano e semestre de conclusão —, e a segmentação
  que ele alimenta passa a incluir o nível, que o Ind2 do Regulamento exige. O
  documento do projeto nomeia só curso, campus e ano.
- **Concluída em:** 28/09/2026 · `docs/especificacao/blocos-instrumento.md` ·
  **ADR-0006**.
- **Descoberta que mudou o desenho da etapa: três referências que não
  coincidem.** O documento do projeto propunha sete blocos próprios, anteriores ao
  Regulamento, e deixava seis indicadores do Anexo I sem bloco (Ind13 a Ind17 e
  Ind19). O art. 17 do Regulamento estrutura o questionário do IFSP em outros sete
  blocos. E três destes — II, VI e VII — não alimentam nenhum indicador do Anexo I,
  embora sirvam a objetivos expressos da mesma norma.
- **Decisões tomadas** (confirmadas com o orientando antes da execução e
  registradas na **ADR-0006**):
  - a estrutura parte dos sete blocos do art. 17, com nomes e ordem da norma, mais
    três de controle — consentimento, identificação acadêmica, contato e
    manifestações — e um de recortes de equidade: **onze blocos**;
  - "indicador correspondente" é um indicador do Anexo I **ou** um objetivo
    expresso do Regulamento (arts. 3º e 34), operacionalizado por indicador mínimo
    proposto pelo projeto, com origem declarada — escala Anexo I / objetivo +
    projeto / controle, na lógica da E05.
- **Critério verificado nas duas direções, e por execução:** onze blocos, nenhum
  sem indicador; dezoito dos dezenove indicadores do Anexo I alimentados — o Ind1
  é listagem de atividades institucionais, e não dado de questionário —; e os dez
  objetivos de coleta do art. 3º com bloco.
- **Achado no Anexo I.** As fórmulas são texto no PDF, e não imagem, como a linha
  de base registrava. Conferidas contra as páginas, três medem outra coisa que a
  própria descrição — a do Ind7 repete a do Ind5, a do Ind12 repete a do Ind10, e
  a do Ind11 tem outro denominador; as dos Ind9 a Ind12 contam só quem está
  cursando, quando as descrições incluem quem já concluiu; e o Ind13 pede média,
  maior e menor remuneração com faixas cuja última é aberta. **Regra adotada: a
  descrição prevalece** — decisão de projeto, a comunicar ao Comitê Permanente.
- **Recortes de equidade, com dado sensível.** Raça/cor e deficiência. O bloco
  depende de consentimento específico e destacado (LGPD, art. 11, I), é opcional e
  oferece não declarar em cada questão. Quem o pede é o próprio Regulamento
  (art. 3º, item 16).
- **Linha de base corrigida em três pontos**, cada um marcado no texto: as
  fórmulas não estavam perdidas; são seis os indicadores em escala de 1 a 10, e
  não sete; e os pares Ind5/Ind9 e Ind6/Ind10 diferem no numerador, e não no
  denominador.
- **Não relido:** o conteúdo vigente dos blocos. A finalidade de cada um parte do
  nome dado pelo art. 17 e do objetivo que ele operacionaliza — limitação
  sobretudo para o Bloco II, cuja leitura como "anterior ao ingresso no curso" a
  E13 confirma.
- **Pendência encaminhada para a E31:** atualizar a tabela de blocos no documento
  do projeto e comunicar ao Comitê Permanente as divergências do Anexo I.

### [x] E13 — Definir domínios, obrigatoriedade e validações
- **Objetivo:** fechar os domínios de valores e as regras de preenchimento.
- **Entregável:** seção complementar em `blocos-instrumento.md`, incluindo o
  comportamento do pré-preenchimento quando o dado de origem estiver desatualizado.
- **Conclusão quando:** todo campo padronizável tiver domínio fechado.
- **Vindo da E11:** as listas de cursos e de unidades são **domínio compartilhado**
  entre o arquivo de entrada e o bloco de identificação que ele pré-preenche — se
  diferissem, o pré-preenchimento exibiria valor fora das opções do instrumento.
  Sem "Outros": quem informa é o sistema da instituição, não o egresso. Decidir
  se a lista de cursos registra o nível de cada curso; se registrar, a coerência
  entre `curso` e `nivel` vira regra de validação do leiaute.
- **Vindo da E12** (`blocos-instrumento.md`, seções 4 e 11). Aplicar aos campos o
  critério que a E12 aplicou aos blocos, com a mesma escala de origem. Fechar no
  Bloco IV as três distinções que as descrições do Anexo I exigem — concluiu ou
  cursa, IFSP ou outra instituição, mesma área ou não. Decidir se o Ind4 é
  autodeclarado ou derivado e se o Ind13 é valor declarado ou faixa; justificar ou
  retirar setor e localidade; decidir entre gênero e sexo; prever não declarar nos
  recortes de equidade e "não conheço" no Bloco VII; confirmar a leitura do Bloco
  II; e fixar a obrigatoriedade, a começar pelo Bloco III. O entregável completa a
  seção 12 do mesmo arquivo, deixada em aberto para isso.
- **Concluída em:** 28/09/2026 · `docs/especificacao/blocos-instrumento.md`,
  seção 12.
- **Descoberta que mudou o desenho da etapa: o instrumento documentado.** O
  Relatório 2 da PAE publica as trinta questões com todas as opções de resposta,
  e foi lido nesta etapa. Três achados. Nome e conteúdo divergem em dois blocos —
  o I reúne perfil e identificação, sem avaliar a formação, e o VII mede o impacto
  do curso, sem avaliar o programa; o Bloco II confirmou a leitura da E12 ("Você
  trabalhava quando entrou no curso do IFSP?"). O instrumento documentado **calcula
  pouco do Anexo I**: nenhuma escala de 1 a 10, renda aberta que o próprio relatório
  não conseguiu apurar, continuidade só para quem está matriculado e sem
  pós-graduação, e "trabalhando" incluindo trabalho sem remuneração. E a versão no
  ar hoje já difere da documentada, que é de 2019 a 2023.
- **Trinta e cinco campos** nos onze blocos, cada um com código proposto, tipo,
  domínio, obrigatoriedade, consumidor e origem do domínio — Anexo I, instrumento
  documentado, oficial, E11 ou projeto. Dez questões documentadas reaproveitadas
  para preservar a série, com a relação de cada uma declarada; sexo e gênero,
  declarados não equivalentes.
- **Decisões tomadas** (confirmadas com o orientando antes da execução):
  - **renda pelas faixas do Anexo I**, como configuração versionada por ciclo — a
    média do Ind13 deixa de ser calculável com rigor, e isso é declarado;
  - **campos documentados sem consumidor ficam fora** — doze, cada um com o
    motivo, e reintroduzíveis mediante indicador declarado;
  - **as questões 29 e 30 vão para o Bloco I**, e o Bloco VII fica com a avaliação
    do programa, em campo novo com "não conheço", como a ADR-0006 estabeleceu.
- **Padrões adotados e declarados:** o Ind4 conta só "sim, totalmente", e
  "parcialmente" é sensibilidade; o vínculo sobe para o Bloco III, porque decide
  quem tem atividade remunerada; o estágio remunerado conta como atividade
  remunerada; a lista de cursos registra o nível, e a coerência entre `curso` e
  `nivel` vira regra do leiaute; a lista de unidades inclui as instituições
  antecessoras; um único texto livre, o de sugestões (Regulamento, art. 12, item
  4). Nenhuma ADR nova: as decisões aplicam aos campos o critério da ADR-0006.
- **Pré-preenchimento desatualizado:** a correção vale para a resposta e para a
  navegação, preserva o valor original, não move o ciclo em andamento e entra numa
  fila de revisão, que é consulta e não estrutura nova.
- **Critério verificado por execução:** 31 campos padronizáveis, todos com
  domínio fechado; 4 não padronizáveis, justificados; todo campo com consumidor; e
  a composição dos Ind2 a Ind19 só com campos existentes.
- **Correções em documentos anteriores**, marcadas no texto: oito pontos da E12 —
  Blocos I, II e VII, setor e localidade, tabelas e limitações — e a ativação da
  regra `curso`–`nivel` no leiaute da E11.
- **Pendência encaminhada para a E31:** comunicar ao Comitê Permanente que o
  instrumento documentado não calcula a maior parte do Anexo I, e as adaptações
  do Ind13 e do Ind4.

### [x] E14 — Definir a lógica de navegação condicional
- **Objetivo:** mapear os caminhos alternativos do instrumento.
- **Entregável:** `docs/especificacao/navegacao-condicional.md` com as regras e um diagrama de fluxo.
- **Conclusão quando:** todos os caminhos previstos estiverem descritos.
- **Vindo da E12:** os públicos da seção 2 de `blocos-instrumento.md` viram regras
  — Bloco V só com atividade remunerada e Bloco VI só sem; a parte de continuidade
  do Bloco IV só para técnico e graduação, pelo `nivel` pré-preenchido; recortes
  de equidade só com o consentimento específico; e as duas recusas do
  consentimento encerram o preenchimento. O fluxo parte dos onze blocos.
- **Vindo da E13** (`blocos-instrumento.md`, seção 12.10): as condições descem ao
  campo — CON2 só com CON1 "concordo"; AP2 só com AP1 "sim"; SA2 só se SA1 incluir
  "trabalhando"; Bloco V só com atividade remunerada, que depende de SA1 **e** SA2;
  EF2 e EF3 só se EF1 não for "não". E toda regra que dependa de atributo usa o
  valor **confirmado** na identificação, e não o pré-preenchido.
- **Concluída em:** 29/09/2026 · `docs/especificacao/navegacao-condicional.md`.
- **Consolidação, e não invenção.** As regras de exibição vinham decididas pela E12
  e pela E13; a etapa as reuniu numa tabela só e acrescentou o que nenhuma das duas
  decidira: como o preenchimento termina, em que estado deixa o participante, e como
  o respondente se movimenta.
- **Achado que precisa chegar à plataforma: recusa não é resposta.** Com o
  consentimento na primeira página, quem recusa também envia uma página — e a E08
  mostrou que é o envio de página que cria a resposta. Conforme a plataforma
  encerre, a recusa pode sair marcada como concluída. **O estado do participante sai
  de CON1, e não da marca de "concluído"**; sem isso, quem recusou entraria no
  denominador de todos os indicadores.
- **Dez caminhos:** duas recusas e oito de preenchimento, decididos por CON2, pelo
  nível confirmado e pela atividade remunerada; com diagrama de fluxo em Mermaid.
- **Decisões tomadas** (confirmadas com o orientando antes da execução):
  - um bloco por página, com o consentimento sempre na primeira;
  - voltar permitido, com as regras recalculadas e o **descarte** do que sai do
    caminho — mudar CON1 para recusa descarta todo o preenchimento, e retirar CON2
    descarta os recortes de equidade;
  - **retomada por "salvar e retomar", com nome e senha**, e não pela reabertura do
    endereço individual. Contra a recomendação inicial, e com argumento que ficou
    registrado: o endereço é transportável (ADR-0003) e as respostas salvas podem
    conter dado sensível, de modo que a senha separa quem tem o link de quem
    respondeu. Custos declarados: o lembrete precisa explicar a retomada, quem
    interromper sem salvar recomeça, e reabrir o link pode criar preenchimento
    órfão.
- **Verificado por execução.** Uma implementação independente das regras percorreu
  **2.802 combinações** das respostas que decidem o caminho: cada uma caiu em
  exatamente um dos dez caminhos, e os dez foram alcançados. A primeira execução
  acusou as duas recusas como ambíguas — defeito da verificação, que comparava só
  os blocos, e não a linha inteira; corrigido e registrado. O diagrama foi
  renderizado pela biblioteca Mermaid 11, sem erro, com os dezenove nós.
- **Não conferido:** nada na plataforma. As cinco conferências ficam com a E15.

### [x] E15 — Implementar a estrutura no LimeSurvey
- **Objetivo:** materializar a especificação na instância.
- **Entregável:** questionário estruturado; exportação da estrutura versionada em `infra/`.
- **Conclusão quando:** todos os caminhos forem percorríveis manualmente.
- **Nome de tabela, conferido na E08:** a tabela de respostas é
  **`lime_responses_<sid>`**, e não `lime_survey_<sid>`. O nome antigo é o que
  aparece na documentação e nos tutoriais, e leva a consulta a falhar sem motivo
  aparente. Vale para esta etapa e para E26, E27 e E28.
- **Vindo da E12:** bloco é grupo de questões, e a estrutura exportada reproduz os
  onze blocos de `blocos-instrumento.md`.
- **Vindo da E13:** os 35 campos da seção 12.3, conferindo se a plataforma aceita
  os códigos e os tipos propostos; a lista de cursos com nível, a de unidades com
  as antecessoras e as faixas de rendimento como configuração versionada; e as
  restrições do modo de ensaio também nos campos de contato.
- **Vindo da E14** (`navegacao-condicional.md`, seção 10): um grupo por bloco, na
  ordem da seção 2; condições por grupo e por campo, com as dependências na mesma
  página **dinâmicas**. E cinco conferências na instância, porque nenhuma foi feita:
  se a plataforma descarta as respostas que saem do caminho; como "salvar e
  retomar" se comporta com participantes identificados; se o formulário de
  salvamento pede e-mail, e se isso se desativa; o que acontece quando o endereço é
  reaberto sem carregar o salvo; e como a recusa encerra o preenchimento, e com que
  marca.
- **Concluída em:** 03/10/2026 · `infra/instrumento/` · `infra/confere-instrumento.py`
  · `navegacao-condicional.md`, seção 11. **Fase 3 encerrada.**
- **Instrumento implantado:** questionário **202615**, onze grupos, 35 campos e 229
  opções, inativo e sem participantes, para a E17. A exportação da própria instância
  está versionada em `infra/instrumento/instrumento.lss`.
- **Estrutura, e não conteúdo.** Cada enunciado é um marcador que nomeia o campo e o
  dado. O texto das perguntas, o do termo e o de encerramento ficam com o projeto
  correlato e a E22. Os domínios entram completos.
- **Por linha de comando, de ponta a ponta (K7).** Um gerador em Python monta o
  `.lss` a partir de `estrutura.py` e da configuração versionada, e o importa pela
  API. A exportação é feita por comando de console próprio, porque a API do
  LimeSurvey 7 importa `.lss` e **não exporta** — conferido contra a lista de
  métodos. O console carrega comandos de `YII_CONSOLE_COMMANDS`, e o comando usa a
  mesma função do botão de exportação do painel; a imagem não muda.
- **Decisões tomadas** (confirmadas com o orientando antes da execução):
  - **unidades reais, cursos ilustrativos** — os 57 campi da página oficial do IFSP,
    com a sigla oficial como código, mais as três antecessoras registradas na E13; e
    treze cursos ilustrativos nos três níveis, a substituir pela instituição;
  - **conferências numa cópia descartável** — mesmo `.lss`, outro sid, ativada com
    participantes sintéticos e removida ao fim sem resíduo —, para que o instrumento
    chegue à E17 inativo.
- **Configurações declaradas, cada uma com o motivo** no README da pasta: um grupo
  por página, voltar, salvar e retomar **sem** retomada pelo link (E14); respostas
  **não anônimas**, porque o estado sai de CON1 ligado ao token — a anonimização é
  da E23; data registrada; IP, URL de origem e tempos não registrados; sem opção
  "sem resposta", sem índice, sem captcha. **Nenhuma ADR nova:** as escolhas
  aplicam a E14, o K7 e a minimização, sem decisão de arquitetura própria.
- **Os 35 códigos da E13 foram aceitos como propostos.** Códigos de opção têm no
  máximo **cinco caracteres**, limite da coluna `lime_answers.code`, conferido. O
  nível vem do prefixo do código do curso, e o gerador recusa curso incoerente.
- **Dois defeitos meus, achados por conferência antes de virarem resultado:**
  1. o Bloco VI **sumia** para quem só estuda. O Expression Manager torna falsa
     toda expressão de exibição que cite questão oculta sem o sufixo `.NAOK`, e SA2
     está oculto justamente nesse caso. Achado na fonte (`em_core_helper.php`),
     antes do percurso; corrigido com `SA2.NAOK`;
  2. o nível derivado gravava **o texto da fórmula**: o atributo de equação é texto
     com trechos `{…}`, e não expressão. Achado no percurso, e **não** pela
     conferência estrutural, que avaliava a equação como expressão. Corrigidos o
     instrumento e a conferência.
- **Conferência estrutural independente do gerador.** `confere-instrumento.py` lê a
  especificação direto dos documentos das E13 e E14, e a instância pela API: **6 de
  6**, inclusive os dez caminhos avaliados com as expressões da instância sobre as
  **2.802 combinações** da E14, nas mesmas contagens por caminho. **A conferência
  foi testada por mutação:** a primeira versão **não acusava** o defeito do
  `.NAOK`, porque o avaliador fazia curto-circuito e o Expression Manager não faz.
  Corrigida, ela reprova as cinco mutações apresentadas.
- **Critério verificado no navegador.** Os **dez caminhos foram percorridos** pela
  interface do respondente, cada um com os blocos da seção 5 da E14, e nenhum
  registro tem V e VI juntos. A exibição dinâmica na mesma página funciona,
  inclusive o nível acompanhando o curso. As validações barram o envio: ano, `.test`,
  código de área real, alternativo igual ao principal.
- **As cinco conferências da E14** (seção 11.2 de `navegacao-condicional.md`):
  - (a) a plataforma **descarta, mas só no envio final**: recusa depois de preencher
    deixa só CON1, e a resposta **interrompida** guarda campos fora do caminho;
  - (b) salvar e retomar funciona com participante identificado, com a senha em
    bcrypt e o IP vazio;
  - (c) o formulário pede **e-mail opcional**, fixo no tema, **sem configuração**
    que o desligue;
  - (d) reabrir o link sem carregar o salvo **cria uma segunda resposta** — a órfã
    que a E14 previa;
  - (e) a recusa encerra pelo fim natural e sai **marcada como concluída**, na
    resposta e no participante. A plataforma contou 13 completas onde havia 10
    respondentes e 3 recusas.
- **Achados para a extração:** as colunas de resposta chamam-se `Q<qid>`, e não pelo
  código; IDA4 sai em decimal; EF4 e CT4 viram subcolunas (`EF4_NEN`, `CT4_RECT`).
- **Fonte não baixada.** O PDF do Relatório 2 da PAE é servido como download, e não
  foi baixado sem autorização; as antecessoras vêm do registro da E13.
- **Não conferido:** preenchimento por uma pessoa — foi conduzido por script, na
  interface real; outros navegadores e telas pequenas; a janela de 60 dias; e o
  encerramento da recusa por cota.

---

## Fase 4 — Base sintética e acesso rastreável
Metas 4 e 5 · set–nov/26

### [x] E16 — Gerar a base sintética
- **Objetivo:** produzir a base de validação.
- **Entregável:** `scripts/gerar_base_sintetica.py` e base de ~500 registros
  distribuídos em 10 anos de conclusão.
- **Conclusão quando:** a base refletir o leiaute de E11 e usar apenas domínio controlado.
- **Atenção:** nenhum dado de pessoa real, nem parcial, nem "de exemplo".
- **Leiaute fixado pela E11** (`leiaute-entrada.md`): uma linha por pessoa
  (ADR-0005); identificadores sintéticos estáveis e sem forma de CPF; endereços só
  sob `.test`; telefones `+55` com DDD terminado em 0 — **reconferir antes, na
  fonte oficial da Anatel**, que nenhum DDD em uso termina em zero, porque a E11
  só pôde conferir em fonte secundária; e parte da base sem via alternativa e
  parte com `email_alternativo`, para exercitar o alerta e o reparo.
- **Vindo da E15:** cursos e unidades vêm de `infra/instrumento/configuracao/` — o
  arquivo de entrada leva o **nome**, e o nível tem de ser o do curso na lista. A
  lista de cursos é **ilustrativa**, treze cursos nos três níveis; a de unidades é
  a oficial, com as antecessoras. Ano de conclusão de 1909 ao ano corrente.
- **Concluída em:** 03/10/2026 · `scripts/gerar_base_sintetica.py` · base em
  `dados/sinteticos/base-sintetica.csv`, não versionada. **Fase 4 iniciada.**
- **DDDs reconferidos na fonte oficial, primeiro.** No painel "CN – Áreas de
  Numeração" da Anatel (PGCN anexo ao Despacho Decisório nº 20/2026/PRRE/SPR),
  filtrado pelos vigentes, foram coletados os 67 códigos, um a um: **nenhum
  termina em zero**, e a busca `*0` no próprio filtro não encontra nada. O painel
  conta "68", mas o contador soma sempre um — conferido em três buscas. A regra da
  E11 está confirmada, e a seção 7 do leiaute registra a reconferência.
- **Decisões tomadas** (confirmadas com o orientando antes da execução):
  - **nomes inventados**, por sílabas, com acentos, partícula, apóstrofo, hífen e
    abreviatura com ponto, para exercitar a seção 4.2 do leiaute. **Correção de
    uma afirmação minha:** ao propor a opção, escrevi que nomes inventados "não
    coincidem com pessoa real nem por acaso", o que é forte demais. Para chegar
    perto disso, o gerador recusa todo prenome ou sobrenome que coincida com os
    mais frequentes no Brasil; a coincidência do nome inteiro fica improvável, e
    não impossível, e é assim que está declarada;
  - **janela de 2016 a 2025**, dez anos completos.
- **A base: 500 registros, determinística** — a mesma semente produz o mesmo
  arquivo, byte a byte, o que dá ao identificador a estabilidade que o leiaute
  exige. Composição de ensaio, e não estimativa de população:
  - de 41 a 58 concluintes por ano; 255 técnicos, 202 de graduação e 43 de
    pós-graduação; os treze cursos e os 57 campi; as antecessoras ficam fora,
    porque são anteriores a 2008;
  - e-mail principal em `egressos.test` (436), `invalido.test` (45) e
    `indisponivel.test` (19) — as três linhas da tabela do P8; dez com domínio em
    maiúsculas, para exercitar a normalização;
  - 198 com `email_alternativo`, 21 deles reparando um principal que devolve;
    271 com telefone; **139 sem via alternativa** (alerta); e **três pares** com o
    mesmo e-mail principal sob identificadores distintos (alerta, sintoma que a
    E19 verifica);
  - identificadores `SIN-000001` a `SIN-000500`.
- **Critério verificado por conferência independente do gerador**, que
  reimplementa as regras das seções 3 a 5 e 7 do leiaute: **10 de 10** — leiaute,
  regras por campo, unicidade e guarda de CPF, endereços só nos três domínios
  `.test`, telefones só com DDD terminado em 0 e fora dos 67 da Anatel, dez anos,
  vias alternativas, nomes fora de uma lista de frequentes distinta da do gerador,
  e determinismo. **A conferência foi testada por mutação** e reprova os sete
  defeitos plantados: e-mail fora de `.test`, DDD em uso, identificador com forma
  de CPF, curso incoerente com o nível, identificador repetido com outra caixa,
  nome com dígito e alternativo igual ao principal. A primeira rodada de mutação
  "passou" em tudo — a conferência tinha quebrado por uma edição minha e não
  imprimia nada; o teste passou a exigir saída válida antes de julgar.
- **A conferência não foi versionada**, de propósito: o validador que barra a
  importação é entregável da E17, e duas implementações das mesmas regras no
  repositório divergiriam. O resultado fica registrado aqui.
- **Não conferido:** como a plataforma recebe os nomes e os tamanhos — é a
  importação real, na E17.

### [x] E17 — Importar a base e ativar a tabela de participantes
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
- **Vindo da E11** (`leiaute-entrada.md`, seções 3 a 7 e 11). A validação do
  arquivo é **prévia** à importação e roda em modo de ensaio; o egresso é
  reencontrado na base central pelo `identificador`, que **nunca** é o token. Três
  coisas a fazer aqui: conferir os tamanhos do leiaute contra as colunas da
  plataforma, que a E11 não conferiu; registrar cada importação na trilha — data,
  SHA-256 do arquivo e contagens por regra — e eliminar o arquivo depois (LGPD,
  art. 16); e **decidir** o que prevalece quando a extração nova traz um contato
  que o mecanismo já corrigiu por busca ativa. A correspondência campo a campo com
  a plataforma está proposta, não verificada.
- **Vindo da E13:** ativar a regra de coerência entre `curso` e `nivel` do arquivo
  de entrada — a lista de cursos registra o nível —; e a decisão de precedência na
  reimportação passa a cobrir também os cinco atributos corrigidos pelo egresso.
- **Vindo da E15:** o instrumento é o questionário **202615**, inativo. A sequência
  que funcionou na cópia de ensaio está em `instrumento.py copia-de-ensaio`: acesso
  fechado (`access_mode = C`), ativação e tabela de participantes, nessa ordem.
  **Ativar trava a estrutura** — mudança depois disso é nova versão do instrumento.
  O questionário não é anônimo, por decisão: a E23 trata a anonimização.
- **Vindo da E16:** a base é `dados/sinteticos/base-sintetica.csv`, gerada por
  `python3 scripts/gerar_base_sintetica.py` (semente padrão 2016). Ela deve passar
  **inteira** no validador desta etapa — nenhum registro rejeitado —, com três
  tipos de alerta esperados: 139 sem via alternativa, três pares com o mesmo
  e-mail principal e dez domínios em maiúsculas a normalizar. Se o validador
  rejeitar algum registro, ou o validador ou o gerador está errado, e a
  divergência é achado. Nomes têm de 10 a 54 caracteres, com acentos, apóstrofo e
  hífen — o caso para conferir contra `firstname`.
- **Concluída em:** 04/10/2026 · **ADR-0007** · `docs/especificacao/importacao-base.md`
  · `scripts/valida_entrada.py`, `scripts/importar_base.py`,
  `scripts/limesurvey_console.py` · três comandos de console em
  `infra/instrumento/comandos/` · subcomando `preparar-participantes`.
- **Base persistente decidida e registrada (ADR-0007).** Base central de
  participantes do LimeSurvey, uma pessoa por identificador, contra a opção do RAEG
  de não manter base fixa. A necessidade lida como "guardar o mínimo, protegido, e
  eliminar o que cumpriu o papel", e não como "não guardar".
- **Decisões tomadas** (confirmadas com o orientando antes da execução):
  - **precedência de contato: prevalece a correção até a origem mudar** — guarda-se
    o último valor visto na origem; arquivo igual mantém a correção, arquivo
    diferente prevalece e a substituição vai para a trilha. Nome e acadêmicos:
    origem (E13). Recusa: nunca tocada;
  - **ativação adiada para depois da E18**: esta etapa fecha o acesso e cria a
    tabela de participantes — o acesso controlado —, e a E18 ativa depois de
    configurar o pré-preenchimento, porque ativar trava a estrutura;
  - **código do instrumento no participante do questionário** (curso `T01`, campus
    `SPO`) e o nome na base central — a tradução que a E15 deixara para a E18.
- **O desenho mudou no meio da etapa, porque a instância o desmentiu.** A primeira
  versão rodava no `rotinas`, gravava pela API e lia o estado por SQL. A primeira
  carga funcionou — e a conferência mostrou que **a base central cifra nome,
  sobrenome e e-mail por padrão**. A precedência leria o e-mail cifrado e, na
  reimportação, regravaria o cifrado para ser cifrado de novo: corrupção do
  contato. E os atributos de contato tinham sido criados em claro, ao lado de um
  e-mail cifrado. **Corrigido:** todo contato da base central cifrado, e a
  comparação feita num comando de console, com os modelos da plataforma, sem a
  chave sair do contêiner; a importação passou a rodar no hospedeiro. A carga da
  primeira versão foi apagada por SQL, como limpeza pontual de ensaio; a preparação
  recusou trocar a cifragem com os dados presentes, como deve.
- **Armadilhas encontradas**, todas silenciosas: a atualização da API
  (`cpd_importParticipants`) **grava `blacklisted = 'N'`** quando o campo não vem —
  apagaria a recusa permanente; a base central é cifrada por padrão; no console, a
  decifração exige importar o Expression Manager (abortou a importação #2, que
  ficou na trilha com o arquivo mantido); `activate_tokens` responde "OK" também
  quando a tabela já existe, sem recriá-la; e a cifragem da plataforma é
  **determinística**, o que revela igualdade.
- **Tamanhos conferidos** contra a plataforma, que a E11 deixara em aberto: a base
  central limita nome a 150 e e-mail a 254 — os mesmos limites do leiaute — e o
  questionário usa `text`. Nenhum campo trunca.
- **Elo com a base central:** `participant_id` derivado do identificador (UUID v5),
  gravado no participante do questionário — o elo que a recusa global nativa usa.
  `lime_survey_links` não é populada, e nenhuma etapa depende dela.
- **Critério verificado por execução, com a trilha registrando cada passo (#1 a
  #9):** 500 pessoas e 500 participantes, sem duplicidade de `participant_id`,
  token ou identificador; **reimportação idempotente**, com os participantes
  idênticos byte a byte — o que prova também a decifração; **precedência** nos dois
  sentidos, com correção simulada por comando de teste não versionado; **recusa
  preservada** e pessoa recusada não recolocada; **validador: 27 de 27** casos
  plantados com o desfecho esperado, sem vazar dado no relatório; arquivo
  rejeitado sem efeito na instância, registrado e eliminado.
- **Não conferido:** a recusa global nativa em ação (exige questionário ativo); a
  cifragem da tabela do questionário, que fica em claro por padrão; a busca ativa
  real; a saída de quem deixa de constar no arquivo (retenção).

### [x] E18 — Configurar acesso por token e pré-preenchimento
- **Objetivo:** endereço individual por participante, com atributos pré-carregados.
- **Entregável:** configuração aplicada e documentada.
- **Conclusão quando:** um acesso de amostra abrir com os atributos corretos.
- **Vindo da E12:** os cinco atributos vão para o bloco de identificação
  acadêmica, editáveis, com a correção registrada e o valor original preservado.
- **Vindo da E13:** o nível não se edita por conta própria — acompanha o curso
  escolhido; e a correção não move o ciclo em andamento (seção 12.5).
- **Vindo da E14:** o nível acompanha o curso **na própria página 2**, porque é o
  valor enviado nela que decide o que o Bloco IV exibe.
- **Vindo da E15:** isso já funciona — IDA2 é equação sobre o prefixo do código do
  curso, conferida no navegador. O que falta é a tradução: o arquivo de entrada traz
  **nomes** de curso e de campus, e o instrumento usa **códigos** (`T01`…, a sigla
  do campus); o pré-preenchimento converte pela `configuracao/`.
- **Vindo da E17:** a tradução já está feita — o participante do 202615 tem
  `attribute_2` com o código de IDA1 e `attribute_4` com o de IDA3; `attribute_3`,
  `attribute_5` e `attribute_6` são nível, ano e semestre; `attribute_1` é o
  identificador. **A ativação do questionário é desta etapa**, depois de
  configurar o pré-preenchimento — a E17 só fechou o acesso e criou a tabela de
  participantes, com 500 pessoas.
- **Concluída em:** 04/10/2026 · `docs/especificacao/pre-preenchimento.md` ·
  subcomando `ativar` · conferência 7 em `infra/confere-instrumento.py`.
  **Questionário 202615 ativo.**
- **Pré-preenchimento como estrutura, e não à mão.** IDA1, IDA3, IDA4 e IDA5 têm
  valor padrão `{TOKEN:ATTRIBUTE_n}`, declarado em `estrutura.py` (`pre_preenchido`)
  e com o número do atributo calculado da mesma lista que a preparação da E17 usa
  para criar as colunas — a ligação vive num lugar só. IDA2 segue derivado do curso,
  sem padrão.
- **Conferido no código da plataforma:** o padrão é processado como expressão e só
  aceito se for resposta válida — funciona nas listas porque o atributo já é o
  código; e **um atributo inválido abre o campo vazio, sem erro para o
  respondente**. Por isso a verificação cobriu os 500 participantes, e não só a
  amostra.
- **Decisão tomada** (confirmada com o orientando antes da execução): **acesso de
  amostra no próprio instrumento**, com limpeza depois, e não em cópia.
- **Caminho completo refeito do zero**, porque padrões são estrutura: implantar
  (com `--substituir`, que descarta os participantes), preparar, reimportar — 500
  pessoas reencontradas na base central, 500 participantes novos — e ativar. O
  `.lss` versionado foi reexportado com os padrões. Nada havia sido enviado.
- **Critério verificado:**
  - **conferência estrutural 7 de 7** — a nova sétima deriva do texto da
    especificação o atributo de cada campo e confere a ligação pela descrição;
    **falhou antes da reimplantação**, apontando os quatro padrões que faltavam, e
    passou depois;
  - **três acessos de amostra**, um por nível, pelo endereço individual: a página 2
    abriu com curso, nível, campus, ano e semestre **iguais ao arquivo de origem**,
    traduzidos para código;
  - **correção:** trocado o curso, o nível acompanhou na hora; a resposta guardou o
    corrigido, o participante ficou com o original e sem marca de concluído; a fila
    de revisão — consulta pela API, por código, e não pelas colunas `Q<qid>` —
    apontou exatamente as duas divergências;
  - **os 500** com curso e campus entre as opções, ano e semestre válidos e nível
    coerente;
  - **controle de acesso:** sem token, pede o código; token inexistente, recusa;
  - **limpeza:** as três respostas de teste apagadas pela API; estado final com
    500 participantes, nenhuma resposta, nada enviado.
- **Não conferido:** a janela de validade do acesso (`validfrom` e `validuntil`,
  60 dias da P5), que é da E21; a fila de revisão como rotina, que é da E28.

### [x] E19 — Validar unicidade e deduplicação
- **Objetivo:** garantir integridade da base de participantes.
- **Entregável:** registro da verificação.
- **Conclusão quando:** nenhum token repetido ou inválido for encontrado.
- **Vindo da E11:** além de token repetido, verificar identificador repetido,
  identificador igual a algum token e o alerta de endereço principal compartilhado
  por identificadores distintos — sintoma de pessoa duplicada.
- **Vindo da E16:** a base traz **três pares plantados** com o mesmo e-mail
  principal sob identificadores distintos. A verificação tem de achar exatamente
  esses três.
- **Vindo da E17:** na base central o e-mail é **cifrado de forma determinística**
  — os três pares aparecem como o mesmo cifrado, e a comparação pode ser feita
  sobre ele; no participante do questionário, em claro. O `participant_id` é
  derivado do identificador, o que torna o identificador repetido impossível na
  base central; conferir também no participante (`attribute_1`).
- **Vindo da E18:** o 202615 foi reimplantado e está **ativo**, com 500
  participantes e tokens novos, gerados na reimportação; a base central é a mesma
  da E17. Verificar sobre esse estado.
- **Concluída em:** 04/10/2026 · `docs/especificacao/unicidade-participantes.md` ·
  `infra/confere-participantes.py`. **Fase 4 encerrada.**
- **Decisão tomada** (confirmada com o orientando antes da execução): e-mail
  principal compartilhado por identificadores distintos é **alerta para revisão
  humana**, listado pelos identificadores, e o mecanismo **não funde pessoas** —
  endereço compartilhado existe de verdade, e a fusão automática juntaria duas
  pessoas reais quando errasse.
- **"Token inválido" ganhou definição verificada, em três sentidos:** o da
  plataforma — o contador `token_invalid` conta token **nulo ou vazio**, conferido
  no código, o que fecha o ponto que a E08 deixou aberto e mostra que a suposição
  registrada lá (validade ou usos) estava errada —; a forma (15 caracteres
  alfanuméricos); e a confusão (tokens que só diferem na caixa, token igual a
  identificador).
- **Conferência só de leitura, reexecutável**, com oito verificações: tokens
  presentes, bem formados e únicos, inclusive sem caixa; identificador presente,
  único e diferente de todo token; `participant_id` único, presente na base central
  e igual ao UUID v5 do identificador, recalculado de forma independente; base
  central íntegra e coberta pelo questionário; e os grupos de e-mail compartilhado
  **iguais no questionário, em claro, e na base central, pelo cifrado
  determinístico**.
- **Critério atendido: 8 de 8.** Nenhum token repetido ou inválido. Os três grupos
  de e-mail compartilhado são **exatamente os três pares plantados pela E16**,
  recalculados do gerador.
- **A conferência foi testada por mutação:** quinze defeitos plantados numa cópia
  em memória dos dados reais, sem tocar o banco, e os quinze reprovados pela
  verificação certa.
- **Não detectável, e declarado:** a mesma pessoa sob identificadores **e**
  endereços distintos — exigiria heurística sobre nome, que o leiaute não sustenta.

---

## Fase 5 — Automação do contato e conformidade
Metas 6 e 7 · out–nov/26

### [x] E20 — Configurar convites e modelos de mensagem
- **Objetivo:** preparar o disparo inicial.
- **Entregável:** modelos de convite e lembrete, com remetente e assunto padronizados.
- **Conclusão quando:** o convite de teste chegar corretamente formatado.
- **Pronto da E09:** o remetente de ensaio é `naoresponda@egressos.test` e o
  endereço de retorno é `devolucoes@egressos.test`, ambos já configurados e
  verificados. O remetente **institucional** é especificação de implantação real,
  conforme a seção 9.1 do P8, e não valor de ensaio — não trocar um pelo outro.
- **Vindo da E11:** o convite usa o `nome` inteiro — o nome de tratamento, que já
  chega como nome social quando houver registro — e saudação neutra. Não há campo
  de gênero, de propósito: a necessidade não sustenta um campo só para flexionar
  a saudação.
- **Vindo da E14:** o lembrete a quem está `em preenchimento` explica como retomar —
  carregar o questionário não finalizado com o nome e a senha escolhidos — e que,
  esquecida a senha, o preenchimento recomeça.
- **Vindo da E15:** reabrir o link sem carregar o salvo **começa outro
  preenchimento**, conferido; o lembrete precisa dizer isso. E a recusa consome o
  convite do ciclo: quem recusou e reabre o link vê "Esse convite já foi utilizado".
- **Vindo da E18:** o endereço individual é `…/index.php/202615?token=<token>&lang=pt-BR`,
  e o 202615 já está ativo. O convite pode dizer que a identificação vem preenchida,
  para confirmar ou corrigir.
- **Concluída em:** 04/10/2026 · `docs/especificacao/modelos-mensagem.md` ·
  `infra/instrumento/mensagens.py` · subcomando `aplicar-mensagens` · comando de
  console `completaratributos` · `infra/confere-mensagens.py`.
- **Modelos como fonte única versionada.** Convite e lembrete, assuntos, remetente
  e retorno em `mensagens.py`; o gerador os põe no `.lss`, o `aplicar-mensagens` os
  grava no instrumento ativo e a conferência compara a instância com o arquivo. O
  `instrumento.lss` foi reexportado. Assuntos estáveis, com a instituição e sem ano;
  saudação neutra com o nome inteiro; identificação pré-preenchida; “Retomar mais
  tarde” e “Carregar questionário não finalizado” com os rótulos conferidos na
  tradução da instância; a contrapartida que o IFSP já anuncia; nenhuma imagem.
- **Decisão 1** (confirmada com o orientando antes da execução): **o remetente de
  ensaio deixou de ser `naoresponda@`**, que contrariava o P7 — no-reply vedado,
  retorno monitorado. Passou a `acompanhamento@egressos.test`, com **caixa própria**
  no correio (`CORREIO_CAIXA_REMETENTE`), para que a resposta humana não caia entre
  as entregues. O remetente é **do questionário** (`adminemail`, `bounce_email`),
  que tem precedência sobre o do sítio — conferido no código —, e por isso vai no
  `.lss`. Imagem do correio passou a 1.1. Continua tudo sob `.test` (seção 9.1).
- **Decisão 2** (confirmada com o orientando): **lembrete com dois ramos num modelo
  só**, por `{if()}` do Expression Manager sobre o 7º atributo,
  `variante_lembrete`, que a rotina grava antes de cada lembrete — assim o
  `remind_participants` nativo e seus contadores continuam servindo. É parâmetro do
  disparo, não estado.
- **Recusa de contato pela lista de bloqueio da base central**
  (`{GLOBALOPTOUTURL}`), e não pela recusa só deste questionário (`{OPTOUTURL}`).
  Abrir o link só mostra a confirmação; a recusa exige POST — conferido no código.
- **Critério verificado: 9 de 9**, com convite de teste real a um participante
  sintético do 202615 e limpeza (decisão 3, confirmada: no próprio instrumento, como
  na E18): remetente, retorno e assunto certos; HTML com alternativa em texto; nome
  com acentos; nenhum marcador por resolver; endereço de acesso do participante,
  que abre o termo; endereço de recusa, que abre a confirmação, não confirmada;
  lembrete com o ramo certo para cada valor; resposta humana na caixa do
  remetente. Mensagens lidas também renderizadas. Estado final: 500 participantes,
  nada enviado, nenhuma resposta, nenhum bloqueio.
- **Duas armadilhas achadas pela primeira execução, que falhou:** acrescentar
  coluna de atributo a instrumento ativo exige comando de console (a API não o
  faz) **e esvaziar o cache de esquema da web** — sem isso a API recusa gravar na
  coluna por até uma hora; e o cache do console é `CDummyCache`, cujo `flush()` não
  faz nada. A interrupção deixou `sent` e uma resposta parcial, desfeitos à mão; a
  limpeza da conferência passou a executar cada passo de forma independente.
- **Achado para a E21:** **abrir o endereço já cria resposta parcial** (`lastpage
  = 0`), sem responder nada.
- **Não verificado:** o efeito do bloqueio sobre disparos futuros (E22/E23); prazo
  de 60 dias, que o texto não promete (E21); a URL pública, que no ensaio é a do
  hospedeiro (E30).

### [x] E21 — Configurar a rotina agendada de lembretes
- **Objetivo:** automatizar a cobrança conforme os parâmetros de E05.
- **Entregável:** rotina agendada ativa; procedimento em `infra/`.
- **Conclusão quando:** o disparo executar no horário e atingir só os não respondentes.
- **Ponto de verificação vindo da E05.** Rotinas nativas de lembrete tendem a
  expressar cadência como *intervalo mínimo desde o último disparo* mais *número
  máximo de lembretes*, modelo que só coincide com o D+*n* desde o convite quando
  os intervalos são uniformes — e D+4/D+7/D+14 não são. Verificar qual modelo a
  rotina disponível expressa e, sendo o primeiro, decidir entre traduzir a cadência
  para intervalos uniformes (dentro da faixa admissível) ou agendar fora da rotina
  nativa. Registrado como verificação, não como diagnóstico: não havia instância.
- **Dois requisitos de implementação.** A cadência conta-se **por participante**, a
  partir do envio efetivo do convite a cada um, e não de uma data única de abertura
  do ciclo — quem entra por reparo de contato receberia lembrete antes do convite.
  E o horário de disparo é **fixo e único, em dia útil**, sem o que o critério
  "executar no horário" não é verificável.
- **"Não respondente" não é estado da base.** É o conjunto de `convidado`,
  `em preenchimento` e `expirado`, conforme a máquina de estados da seção 12 de
  `parametros-contato.md`. Não implementar marcação redundante.
- **Problema concreto descoberto na E07, mais agudo do que "a máquina precisa estar
  ligada".** O WSL **encerra a distribuição quando ela fica ociosa**, e com ela
  param os contêineres — observado nesta etapa, no meio do trabalho. Ao reabrir, o
  `systemd` sobe o Docker e os contêineres voltam sozinhos pela política de
  reinício, **mas a distribuição só reabre quando algo a invoca**. Sem mecanismo
  que a mantenha viva ou a acorde no horário, o disparo agendado simplesmente não
  ocorre, com a máquina ligada e tudo aparentemente correto. Resolver aqui, e
  registrar a solução no guia — é o tipo de falha silenciosa que passa por
  "funcionou nos testes".
- **A mesma raiz voltou na E09, num terceiro sintoma.** O relógio da máquina
  virtual **salta** quando a distribuição suspende e retoma, e o Dovecot se recusa
  a lançar serviços naquele intervalo — contêiner saudável, porta aberta, toda
  sessão de rede recusada. Custou três diagnósticos. O correio ganhou supervisão
  que o recria, mas isso trata o sintoma.
- **Parte da raiz foi tratada em 27/09/2026, com autorização do orientando:**
  `instanceIdleTimeout = -1` na seção `[general]` do `%UserProfile%\.wslconfig`,
  que impede o encerramento da distribuição por ociosidade. Documentado em
  `infra/README.md`, na parte de opções de hospedeiro — é ajuste **do hospedeiro**,
  não da composição.
  - **Efeito medido:** tempo de atividade da distribuição de 401 s para 621 s ao
    longo de 220 s de ociosidade **sem sessão anexada** — cresceu exatamente o
    tempo esperado, em vez de zerar. Antes do ajuste, o padrão a encerrava em 15 s.
  - **Dois tropeços do caminho, registrados porque enganam:** o primeiro teste que
    escrevi esperava *dentro* da distribuição, o que mantém sessão ativa e dá falso
    positivo; e o arquivo saiu com marcador de ordem de bytes, que o WSL trata como
    malformado e **ignora em silêncio** — sintoma indistinguível de "não funciona".
  - **Supervisão do correio verificada na mesma sessão:** matando o Dovecot, o
    contêiner foi recriado em cerca de 20 s e voltou saudável.
  - **Correção de rumo registrada:** eu havia indicado `vmIdleTimeout`, da seção
    `[wsl2]`. Era a configuração errada. Aquela governa a máquina virtual e só
    aceita número de milissegundos; a que governa a **distribuição** — que era o
    que se observava morrendo — é `instanceIdleTimeout`, e é a única das duas que
    aceita `-1`.
  - **O que continua em aberto para esta etapa:** o ajuste não cobre suspensão ou
    hibernação do Windows, em que a máquina virtual suspende de todo modo. E ele é
    do ambiente de trabalho, **não** do entregável: a decisão de arquitetura desta
    etapa é onde o agendador vive, e a resposta portátil é **dentro da composição**
    (no contêiner `rotinas`), com o hospedeiro permanecer acordado virando
    requisito documentado. Não amarrar o agendamento ao Agendador de Tarefas do
    Windows, que tornaria o mecanismo dependente de um sistema operacional.
- **Duas coisas a agendar, não uma.** A E09 mostrou que a devolução temporária
  **não chega dentro do mesmo disparo que a originou** — o servidor de origem
  guarda a mensagem na fila e só avisa depois. A leitura de devoluções tem, por
  isso, de ser agendada **independentemente** da cadência de disparo, e não como
  etapa final dela.
- **Vindo da E11.** A data do D0 vem de calendário configurável por semestre, e
  não do arquivo, que traz só ano e semestre; e a âncora muda quando chega
  conclusão nova (ADR-0005). A fila de correção tem **duas vias de naturezas
  diferentes**: o `email_alternativo`, que admite reconvite automatizado dentro da
  rodada única de reparo, e o `telefone`, que é operação humana (ADR-0003).
- **Vindo da E14:** o estado do participante sai de CON1 e da conclusão, e **não**
  só da marca de "concluído" da plataforma — a recusa pode vir marcada como
  concluída; e as recusas interrompem a cadência.
- **Vindo da E19:** `infra/confere-participantes.py` pode ser a guarda antes de cada
  disparo — dispara só se as conferências 1 a 7 passarem.
- **Vindo da E20:** antes de cada lembrete, gravar `variante_lembrete`
  (`attribute_7`) com `convidado` ou `em_preenchimento`; sem isso o lembrete sai
  com o ramo de quem não iniciou. Disparar por `remind_participants` com lista
  explícita de participantes — com `iMinDaysBetween` nulo ele não filtra por
  intervalo, e a cadência D+*n* fica com a rotina. **Abrir o endereço já cria
  resposta parcial com `lastpage = 0`**: decidir se isso é acesso iniciado (C3) ou
  ainda `convidado`. O convite é `invite_participants` com lista explícita; e
  `confere-mensagens.py` (leitura) serve de guarda junto com a da E19.
- **Vindo da E18:** a janela de 60 dias da P5 é `validfrom` e `validuntil` do
  participante, ainda não configurados — são desta etapa, por ciclo. A âncora vem
  dos atributos, que a correção do egresso não altera (conferido).
- **Vindo da E17:** a correção de contato por busca ativa precisa gravar nos dois
  lugares — no participante do questionário, pela API, e na base central, onde o
  contato é cifrado, **só por comando de console**, como a importação. A regra de
  precedência da E17 lê o contato atual da base central.
- **Vindo da E15:** confirmado — a recusa sai com `completed` preenchido no
  participante e `submitdate` na resposta. E um participante pode ter **duas
  respostas** no ciclo, a concluída e uma parcial órfã; a rotina não decide pelo
  número de respostas.
- **Concluída em:** 05/10/2026 · `docs/especificacao/rotina-disparo.md` · ADR-0008 ·
  `scripts/cadencia.py`, `disparar.py`, `agendador.py` e
  `conferencia_participantes.py` · `infra/rotinas/configuracao/agenda.json` ·
  `infra/confere-rotina.py` · `infra/hospedeiro/liga-wsl-ao-entrar.ps1`.
- **Ponto 13.1 respondido, no código da plataforma:** a rotina nativa é *intervalo
  desde o último envio* mais *máximo de lembretes*, e não há agendador. **A cadência
  ficou fora dela, e o P3 não mudou** (ADR-0008). `cadencia.py` calcula estado e
  vencimento por participante, e a plataforma só recebe a lista explícita. Quatro
  armadilhas tratadas: `sent` e `remindersent` estão em **UTC**, e `validuntil` em
  hora local; cada chamada envia no máximo 50; sem `continueOnError` o lote para na
  primeira falha; e o envio pela API não grava `date_invited`. Por isso a regra dos
  doze meses sai do registro próprio. Também `list_participants` pagina por `tid`, e
  não por deslocamento.
- **Agendador:** laço próprio, processo principal do contêiner `rotinas`. O disparo
  é às 10:00, de segunda a sexta, menos os feriados da agenda, com tolerância de
  30 min; as devoluções são lidas a cada 30 min, separadas. Cada horário é reservado
  com chave única. Horário vencido vira `perdida` e **não** roda fora da hora: a
  cadência é por vencimento, e o que venceu sai no dia útil seguinte. Registro em
  `egressos_execucoes` e `egressos_disparos`, sem token, nome nem endereço. A guarda
  roda as conferências 1 a 7 da E19 — a lógica passou para `scripts/`, conferida 8
  de 8 — e as condições da E20.
- **Decisão sobre `lastpage = 0`:** abrir o endereço **não** é iniciar. `em
  preenchimento` é resposta não enviada com CON1 gravado. Medido pelo caminho real:
  abrir deixa `lastpage 0` com CON1 vazio; enviar a página 1 deixa `lastpage 1` com
  `CONC`.
- **Decisões confirmadas com o orientando:** modo **simulado** até a E26; a
  operação de reparo de contato fica para a E26; a tarefa de logon do Windows foi
  **criada por mim, com autorização**, e só liga a distribuição, conferida com a
  distribuição encerrada e a tarefa disparada; disparo às 10:00, de segunda a
  sexta, com feriados.
- **Critério verificado:**
  - **Execução real de hoje:** prevista para as 10:00:00, rodou às 10:00:08, em
    simulado, com 255 convites planejados e nada enviado.
  - **`confere-rotina.py --agendada`, 14 de 14:** disparo previsto para as 10:06:00
    começou às 10:06:11. Os lembretes foram só para os quatro não respondentes
    vencidos, com o ramo certo, e houve um reconvite. Nenhum dos outros 9 plantados
    nem dos 486 de controle recebeu nada; chegaram 5 mensagens; a limpeza foi
    completa.
  - **Regras:** 7 de 7, com 16 de 16 mutações reprovadas.
  - **`--perdida`:** 8 de 8.
  - **Estado final:** 500 participantes, nada enviado, nenhuma resposta.
- **A primeira execução de `--agendada` falhou na limpeza.** O relógio do WSL voltou
  7,3 s, o IMAP recusou login e um `SystemExit` escapou da limpeza. Restaram uma
  mensagem e o registro do ciclo de teste, desfeitos à mão. A conferência passou a
  insistir na caixa, a capturar a falha em cada passo e a guardar o log do agendador
  de teste. A segunda execução passou inteira. Outro furo foi achado pela mutação
  e corrigido: os casos não distinguiam UTC de hora local.
- **Achados:**
  - **Relógio:** o da máquina virtual do WSL está **7,3 s atrás** do Windows e é
    corrigido aos saltos para trás, sem suspensão. É o quinto sintoma da raiz da
    E07.
  - **Distribuição parada:** a distribuição estava parada depois do reinício do
    Windows, e o `instanceIdleTimeout` não a liga.
  - **Datas da resposta:** estão em UTC.
  - **Envio sem JavaScript:** exige os campos `relevance<qid>`; sem eles, a
    plataforma descarta a resposta em silêncio.
- **Não verificado:** um reinício real do Windows; a cadência correndo em dias de
  calendário, porque o tempo foi comprimido pela API; e a regra dos doze meses
  entre ciclos, conferida só nas regras, porque há um questionário só.

### [ ] E22 — Implementar consentimento eletrônico
- **Objetivo:** registrar aceite conforme a LGPD.
- **Entregável:** tela inicial de consentimento com registro de aceite, data e versão do termo.
- **Conclusão quando:** o aceite for persistido e recuperável.
- **Requisito acrescentado pela E05.** A tela precisa oferecer **duas manifestações
  separadas**, não uma: *não concordo com o termo neste ciclo* (encerra o ciclo
  corrente; o egresso é convidado no ciclo seguinte) e *não quero mais ser
  contatado* (permanente até revogação). Uma única opção de recusa erra em qualquer
  das direções — ou exclui para sempre quem apenas hesitou, ou ignora quem pediu
  para sair. Justificativa em `parametros-contato.md`, seção 8.
- **Vindo da E12: três manifestações, e não duas.** Além das duas recusas da P6,
  o consentimento específico e destacado do dado sensível (LGPD, art. 11, I), que
  os recortes de equidade exigem. Negá-lo dispensa só aquele bloco, sem encerrar o
  questionário.
- **Vindo da E13:** os campos são CON1 e CON2, e data, hora e versão do termo são
  metadados registrados pela plataforma, e não campos.
- **Vindo da E14:** mudar CON1 para uma das recusas descarta todas as respostas
  daquele preenchimento, e retirar CON2 descarta os recortes de equidade.
- **Vindo da E15:** o consentimento já é grupo próprio, com CON1 e CON2, e o aviso
  nativo de política está desligado. Os dois descartes acontecem **no envio final**
  — conferido. O formulário de salvamento pede **e-mail opcional**, fixo no modelo
  do tema (`save.twig`), sem configuração: decidir entre derivar o tema e manter o
  campo, tratando-o na E23. A recusa encerra pelo fim natural e marca o
  participante como concluído; o encerramento por cota, não testado, é a
  alternativa se isso atrapalhar.
- **Vindo da E17:** o elo da recusa global nativa — o `participant_id` no
  participante do questionário — está gravado, mas a recusa pelo endereço
  individual não foi exercitada, porque exige questionário ativo. Exercitá-la aqui.
- **Vindo da E20:** a mensagem leva `{GLOBALOPTOUTURL}`, que marca `OptOut` no
  participante **e** põe na lista de bloqueio da base central (conferido no código,
  não exercitado — a conferência só abre a confirmação). Exercitar a confirmação e
  verificar que o bloqueio impede convite e lembrete seguintes, inclusive em outro
  questionário, e qual configuração global da lista de bloqueio isso exige. O
  texto hoje indica a revogação como "responder a esta mensagem", que chega à
  caixa `acompanhamento`; a via definitiva é da E23.
- **Vindo da E21:** a rotina já lê como recusa de contato o bloqueio da base
  central, `emailstatus = 'OptOut'` e CON1 = `RCONT`, e não dispara a quem a tem.
  Exercitar a recusa pelo endereço e conferir que o plano a reflete, com
  `disparar.py --simular` no contêiner.

### [ ] E23 — Configurar anonimização e trilha de auditoria
- **Objetivo:** completar os controles de conformidade.
- **Entregável:** parametrização aplicada e documentada, incluindo tratamento da recusa.
- **Conclusão quando:** a recusa **de contato** interromper novos disparos em todos
  os ciclos, e a recusa **de consentimento** interromper apenas o ciclo corrente.
- **Precisão vinda da E05.** São dois estados com efeitos distintos, e um terceiro
  que não é recusa: `contato inválido` interrompe o disparo do ciclo corrente e
  abre fila de correção, mas **não** bloqueia ciclos futuros — tratá-lo como recusa
  converteria falha de cadastro em manifestação de vontade que ninguém expressou e
  degradaria a base a cada ciclo. Registrar data, hora, ciclo, versão do termo e
  via de manifestação; e prever revogação tão simples quanto a manifestação.
- **Dois achados da E08, ambos de implementação.**
  1. **A recusa exige `emailstatus='OptOut'`, e não `blacklisted`.** Marcar
     `blacklisted='Y'` no token não move o contador de recusa — produz um bloqueio
     que não bloqueia. E a persistência **entre ciclos** só existe pela base
     central `lime_participants`, porque a marcação no token morre com a tabela do
     questionário.
  0. **Insumo pronto da E09:** a tabela `egressos_devolucoes` já registra, por
     devolução, data e hora da leitura, ciclo, questionário, participante,
     endereço, tipo, código, ação, diagnóstico e se houve marcação. É trilha de
     auditoria do P8 e pode ser aproveitada aqui. A rotina de devoluções **não**
     toca a marcação de recusa — se esta etapa precisar registrar recusa, é por
     outra via, e a separação é deliberada.
  2. **A trilha de auditoria exige ativar um plugin pela interface.** O `AuditLog`
     acompanha a plataforma mas vem inativo, e nenhuma tabela de auditoria existe
     antes da ativação. O comando de console não oferece ação para isso, e marcar
     `active=1` no banco não basta: o gancho que cria a tabela não roda por essa
     via. **Decidir aqui** entre achar caminho programático ou declarar exceção
     documentada ao critério K7, com a operação de tela descrita. Não resolver por
     omissão — auditoria é requisito de conformidade.
- **Vindo da E11:** o relatório de validação da importação não reproduz nome,
  endereço nem telefone, e a eliminação do arquivo de entrada depois de importado
  entra na política de retenção.
- **Vindo da E12:** a correção de atributo pré-preenchido e a atualização de
  contato pelo egresso entram na trilha; e o dado sensível dos recortes de
  equidade exige tratamento próprio na anonimização.
- **Vindo da E13:** o campo de sugestões (AF4) é o único texto livre e o de maior
  risco de conter dado pessoal não previsto, inclusive de terceiros — tratá-lo antes
  de qualquer exportação; e a faixa de renda entra na anonimização.
- **Vindo da E14:** o e-mail do formulário de salvamento, se a plataforma não o
  deixar desativar; e os descartes por mudança de caminho como eventos da trilha.
- **Vindo da E15:** a plataforma **não** deixa desativar o e-mail do salvamento por
  configuração; ele vai para `lime_saved_control`, com o nome e a senha em hash, e o
  registro é apagado na conclusão. Mais grave: o descarte só ocorre no envio final,
  e a resposta **interrompida** guarda campos fora do caminho — por inferência,
  também os recortes de equidade de quem retirou CON2 e abandonou. Tratar a parcial
  com CON2 diferente de "concordo" como portadora de dado sensível sem
  consentimento.
- **Vindo da E17:** a base central cifra nome, e-mail e contatos, mas a tabela do
  questionário fica **em claro** por padrão — decidir a cifragem dos participantes
  do questionário. Declarar que a cifragem da plataforma é **determinística**.
  Definir a **retenção** da base central, que agora é persistente (ADR-0007), e o
  que acontece com quem deixa de constar no arquivo. A trilha
  `egressos_importacoes` é insumo de auditoria, e a recusa nunca é tocada pela
  importação — conferido.
- **Vindo da E19:** descrever a **revisão humana** dos grupos de e-mail
  compartilhado — quem revisa, e que a pessoa de fato duplicada se corrige na
  origem, e não no mecanismo.
- **Vindo da E21:** `egressos_execucoes` e `egressos_disparos` são trilha, inclusive
  da execução perdida. **Anonimizar as respostas quebra a rotina:** sem o token na
  resposta, ela não distingue `convidado` de `em preenchimento` nem vê a conclusão.
  Preservar o vínculo ou substituí-lo. As datas da resposta estão em UTC.

### [ ] E24 — Documentar recomendações que dependem de terceiros
- **Objetivo:** registrar o que não será executado mas deve constar.
- **Entregável:** seção no guia de replicação sobre divulgação em colação de grau,
  grupos de turma e ações dirigidas a turmas antigas.
- **Conclusão quando:** cada recomendação estiver ligada à evidência da literatura.
- **Vindo da E12:** a adesão voluntária, que o documento do projeto punha no bloco
  de contato e que exige termo próprio (Regulamento, art. 40), e os objetivos de
  ação institucional do art. 3º do Regulamento (itens 9, 10, 11, 13 e 14).

---

## Fase 6 — Validação por simulação controlada
Meta 8 · nov–dez/26

### [ ] E25 — Montar a matriz de verificação executável
- **Objetivo:** transformar a matriz do projeto em roteiro aplicável.
- **Entregável:** `docs/especificacao/matriz-verificacao.md` com requisito,
  procedimento, resultado esperado e campo para resultado obtido.
- **Conclusão quando:** os 12 requisitos do projeto estiverem contemplados.
- **Acrescentado pela E06:** a **contenção do disparo** passou a ser propriedade do
  ambiente, e não regra de conduta — logo é verificável e deve entrar na matriz
  como característica do ambiente, não como procedimento de operação.
- **Vindo da E11:** o requisito "importação da base" precisa de arquivos
  **inválidos de propósito**, um por regra de rejeição de `leiaute-entrada.md`, e
  não só do sintético válido. A rejeição de endereço fora de `.test` é
  característica verificável da contenção, na mesma linha do K6.
- **Vindo da E12:** "registro do consentimento" passa a incluir o consentimento
  específico do dado sensível; e "navegação condicional" é redigido contra os
  públicos de `blocos-instrumento.md`, e não contra a noção genérica de "blocos
  pertinentes".
- **Vindo da E13:** "pré-preenchimento" inclui corrigir um atributo e verificar
  que o original foi preservado; "navegação condicional", as regras de campo da
  seção 12.10.
- **Vindo da E14:** "navegação condicional" é redigido contra os **dez caminhos** de
  `navegacao-condicional.md`; e "retomada de preenchimento" passa a ser salvar,
  fechar e carregar com nome e senha.
- **Vindo da E15:** a conferência estrutural já existe e é executável —
  `infra/confere-instrumento.py`, seis conferências — e pode ser o procedimento do
  requisito de estrutura do instrumento.
- **Vindo da E16:** sete defeitos já foram plantados em cópias da base para testar
  a conferência da E16 — e-mail fora de `.test`, DDD em uso, identificador com
  forma de CPF, curso incoerente com o nível, identificador repetido com outra
  caixa, nome com dígito e alternativo igual ao principal. São ponto de partida
  para os arquivos inválidos de propósito, um por regra; faltam os de arquivo
  (codificação, separador, cabeçalho, aspas). Identificador com forma de CPF se
  constrói a partir de base fixa e dígitos calculados, nunca de número real.
- **Vindo da E17:** os de arquivo já foram exercitados — **27 casos** contra
  `valida_entrada.py`, um por regra de rejeição e de alerta (importacao-base.md,
  seção 9.2). E dois requisitos verificáveis novos: a reimportação idempotente e a
  recusa preservada na reimportação.
- **Vindo da E19:** o requisito de unicidade tem procedimento pronto —
  `confere-participantes.py`, mais os quinze defeitos do teste de mutação como casos
  negativos (`unicidade-participantes.md`, seção 5.1).
- **Vindo da E21:** "seletividade do lembrete" e "disparo no horário" têm
  procedimento pronto — `confere-rotina.py --agendada`, catorze situações contra a
  máquina de estados —, e a execução perdida, `--perdida`. Os dezesseis defeitos da
  mutação de `cadencia.py` (`rotina-disparo.md`, seção 9.3) servem de casos
  negativos.

### [ ] E26 — Executar os cenários de simulação
- **Objetivo:** exercitar o mecanismo sob condições previstas em operação real.
- **Entregável:** execução dos cenários de preenchimento parcial com retomada,
  ausência de resposta, contato inválido e recusa.
- **Conclusão quando:** todos os cenários tiverem resultado registrado.
- **Herdado da E09.** Duas coisas que aquela etapa implementou e **não** pôde
  exercitar: o **limiar de três ocorrências** de erro temporário, que exige três
  devoluções ao mesmo participante no mesmo ciclo com os intervalos de P3 entre
  elas; e o **ciclo de reparo** com o teto de uma rodada. A classificação em si já
  está verificada.
- **Herdado da E08, que não pôde fazer.** A E08 demonstrou que o modelo de dados
  **representa** o preenchimento parcial — `submitdate` nulo com `startdate`
  preenchido é lido como resposta incompleta —, mas inseriu a linha direto no
  banco, porque o método `add_response` da API grava `submitdate` mesmo quando não
  se pede, isto é, cria sempre resposta concluída. **Exercitar o percurso real do
  respondente é desta etapa**, e é o que fecha a verificação de C3.
- **Vindo da E11:** o ciclo de reparo ganhou uma via automatizável — o
  `email_alternativo` —, e é por ela que o cenário de contato inválido pode ser
  exercitado sem ação humana.
- **Vindo da E13:** incluir quem trabalha sem remuneração, que segue para o Bloco
  VI, e a correção de nível que muda a exibição do Bloco IV.
- **Vindo da E14:** cada um dos dez caminhos ao menos uma vez; interrupção com e
  sem salvamento; voltar mudando a situação atual; e recusa na primeira página,
  conferindo que ela não conta como resposta.
- **Vindo da E16:** a base dá os casos do P8 prontos — 45 principais em
  `invalido.test` (erro permanente), 19 em `indisponivel.test` (erro temporário) e
  21 principais que devolvem com alternativo entregável, que é o reparo
  automatizável.
- **Vindo da E15:** `infra/instrumento/instrumento.py copia-de-ensaio` monta uma
  cópia percorrível, e `remover` a desfaz. Duas sessões no mesmo navegador colidem
  ("código de acesso incompatível"); `&newtest=Y` abre sessão nova. O cenário de
  interrupção precisa conferir os campos fora do caminho, que a parcial guarda.
- **Vindo da E21:**
  - **Ligar o modo real:** `ROTINA_DISPARO=real` no `.env` e `docker compose up -d
    rotinas`. A primeira execução convida todos cuja âncora já passou: 255 de 500 em
    05/10/2026, os do 1º semestre; os do 2º vencem em 15/12. Exige o hospedeiro
    ligado às 10:00.
  - **Implementar a operação de reparo de contato** (decisão do orientando): trocar
    para o `email_alternativo` no participante, pela API, e na base central, só por
    console no hospedeiro. A rotina já reconvida uma vez no ciclo quem volta a
    `pendente` e reinicia a contagem.
  - **Correr a cadência em dias de calendário**, ou declarar a compressão. A E21
    viu cada situação num disparo, com as datas postas no passado pela API.
  - **Caminho real sem JavaScript:** `confere-rotina.py` mostra como responder a
    página 1 por HTTP, com os campos `relevance<qid>`.

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
- **Boa parte do caminho já está aberta pela E09.** Há cliente de API
  compartilhado em `scripts/limesurvey_api.py`, com as quatro armadilhas daquela
  interface já tratadas, e o contêiner `rotinas` como ponto de execução. Esta
  etapa acrescenta a extração, não a infraestrutura.
- **Lembrete de nome de tabela:** `lime_responses_<sid>`, não `lime_survey_<sid>`.
- **Vindo da E12:** calcular os indicadores pelas **descrições** do Anexo I, e não
  pelas fórmulas, registrando a divergência (`blocos-instrumento.md`, seção 6); e
  aplicar os recortes de equidade aos Ind3, Ind4 e Ind5 a Ind12.
- **Vindo da E13:** calcular pelas composições da seção 12.4 de
  `blocos-instrumento.md` — o Ind4 com "sim, totalmente" e a parcela
  "parcialmente" como sensibilidade; o Ind13 por faixas, sem média rigorosa.
- **Vindo da E14:** denominadores sem as recusas; no máximo uma resposta concluída
  por participante e ciclo; parciais órfãs descartadas; e, se a plataforma guardar
  respostas fora do caminho, a extração reaplica as regras de exibição.
- **Vindo da E15:** a plataforma **guarda**, nas parciais — reaplicar as regras deixa
  de ser condicional. As colunas de `lime_responses_<sid>` chamam-se **`Q<qid>`** e
  `Q<qid>_S<sqid>`, e não pelo código do campo: traduzir por `lime_questions`, ou
  exportar pela API com cabeçalho por código. IDA4 sai em decimal
  (`2020.0000000000`). EF4 e CT4 são subcolunas (`EF4_NEN`, `CT4_RECT` = `Y`). E a
  contagem nativa de completas inclui as recusas: 13 contra 10 respondentes na
  cópia de ensaio.
- **Vindo da E18:** a **fila de revisão** — respostas com IDA1 a IDA5 diferentes do
  atributo original do participante — já foi exercitada pela API (exportação por
  código mais lista de participantes); falta torná-la rotina, com a taxa de
  correção por atributo como indicador de qualidade da base
  (`pre-preenchimento.md`, seção 4).
- **Vindo da E19:** os grupos de e-mail compartilhado são candidatos a pessoa
  duplicada, e **não** devem ser fundidos na extração.
- **Vindo da E21:** as datas da resposta (`startdate`, `submitdate`) estão em
  **UTC**. `egressos_disparos` dá, por participante, quantas mensagens recebeu e
  quando, e `cadencia.estado` dá o estado da seção 12 sem reimplementá-lo.

### [ ] E29 — Painel de visualização (CONDICIONAL)
- **Objetivo:** apresentar os indicadores de forma agregada.
- **Entregável:** painel funcional com atenção a níveis de acesso multicampi.
- **Conclusão quando:** os indicadores forem exibidos a partir dos dados extraídos.
- **Atenção:** só iniciar após E01–E28. Se o prazo não comportar, especificar
  como trabalho futuro e marcar esta etapa como dispensada.
- **Vindo da E12:** exibir separados os indicadores do Anexo I e os propostos pelo
  projeto, com o rótulo de origem — os segundos não são indicadores
  institucionais.

### [ ] E30 — Consolidar o guia de replicação
- **Objetivo:** entregar o artefato replicável por outras instituições.
- **Entregável:** `entregas/guia-replicacao.md` completo.
- **Conclusão quando:** cobrir instalação, configuração, estrutura, automação e conformidade.
- **Organização que a E06 determinou.** Separar o que o guia **ensina** — a
  composição, idêntica em qualquer lugar — do que ele apenas **oferece como
  opção** — como obter um hospedeiro Docker em cada sistema operacional. E
  registrar o que muda numa implantação real: hospedeiro que permanece ligado,
  correio institucional e rede não isolada. Sem essa separação, o guia parece
  prescrever um equipamento pessoal, quando o artefato é a composição.
- **Três detalhes de correio que precisam constar, vindos da E09.** Cada um, se
  esquecido, produz um ambiente que **parece** funcionar e no qual o P8 é
  inexequível: `local_recipient_maps` vazio, `relay_domains` nomeando o domínio
  indisponível, e o fato de o aviso de atraso não ser imediato. Estão explicados em
  `docs/especificacao/leitura-devolucoes.md`, seção 2.1.
- **Advertência de método a registrar:** capturador de SMTP não serve. É o atalho
  natural de quem monta ambiente de ensaio, e ele satisfaz a aparência do critério
  sem satisfazer o requisito.
- **O documento já existe e já tem a forma final.** A E10 escreveu as Partes I a
  III e deixou IV a VI marcadas com a etapa responsável de cada uma. **Esta etapa
  preenche, não reestrutura** — e, ao preencher, deve refazer o teste do critério
  da E10: clonar num diretório novo e seguir o guia ao pé da letra, agora incluindo
  estrutura, automação e conformidade.
- **Vindo da E11:** como produzir o arquivo de entrada — UTF-8 e vírgula, com a
  armadilha da planilha em português, que exporta ponto e vírgula em codificação
  regional; o nome de tratamento; a pseudonimização do identificador por resumo
  com chave, quando a origem não tiver código estável; e o desligamento
  **consciente** do modo de ensaio numa implantação real.
- **Vindo da E13:** a atualização das faixas de rendimento a cada ciclo, com versão,
  porque os valores em reais do Anexo I envelhecem.
- **Vindo da E15:** a Parte IV do guia parte de `infra/instrumento/README.md` —
  implantar, conferir, exportar. Numa implantação real, trocar as duas expressões
  do modo de ensaio (e-mail sob `.test`, código de área terminado em 0) e a lista
  ilustrativa de cursos. E as seis armadilhas daquele README, que falham sem erro.
  O `.gitattributes` trata `.lss` como binário: as versões do instrumento não
  mostram diferença no Git.
- **Vindo da E17:** a carga é de dois comandos — `instrumento.py
  preparar-participantes`, uma vez, e `importar_base.py`, a cada arquivo —, e roda
  no **hospedeiro**, porque chama o console da plataforma; explicar por quê. E as
  cinco armadilhas de `importacao-base.md`, seção 8, sobretudo a que apaga a
  recusa pela API.
- **Vindo da E20:** o remetente institucional entra em `mensagens.py` (remetente,
  nome e retorno do questionário), com caixa de retorno lida por pessoa; a URL das
  mensagens é montada pelo host da requisição — configurar a URL pública da
  instância; lembrete disparado pelo painel sai sem a gravação do ramo; e as duas
  armadilhas de `modelos-mensagem.md`, seção 5.1 (coluna nova em instrumento ativo
  e cache de esquema).
- **Vindo da E21:**
  - **Parte V do guia:** parte de `infra/README.md`, seção "Rotina agendada".
  - **Tarefa de logon do Windows:** `hospedeiro/liga-wsl-ao-entrar.ps1` entra como
    **opção de hospedeiro**, e não do mecanismo.
  - **Valores de ensaio:** trocar feriados e calendário de `agenda.json` pelos da
    instituição.
  - **Relógio do WSL:** ele anda para trás.
  - **Virada de ciclo:** o procedimento de abrir o questionário do ano seguinte
    ainda não existe e precisa ser escrito. A rotina opera sobre o questionário
    configurado, e `implantar` usa sid fixo.

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
- **Correção de fundamentação no documento do projeto**, vinda da E05. O documento
  afirma que os parâmetros de contato são "derivados das experiências sistematizadas
  na revisão da literatura" e, na Fase 5, "definidos a partir do quadro comparativo".
  A E04 demonstrou que número de lembretes, intervalo e limite de tentativas não
  derivam de efeito medido — nenhuma fonte os informa. Os valores ficam; a
  atribuição de origem muda para decisão de projeto declarada. Sem alteração de
  escopo, valor ou cronograma. Redação sugerida em `parametros-contato.md`, seção 14.
- **Conformidade parcial a declarar:** o art. 16, §1º do Regulamento (convite por
  mensagens instantâneas) não é atendido por automação, conforme ADR-0003. O
  projeto entrega a condição técnica — endereço individual transportável —, não o
  disparo. Enunciar assim, sem arredondamento.
- **Limitação vinda da E06:** o ambiente é local e a rotina agendada só executa com
  a máquina ligada. Não se poderá afirmar que a rotina se sustenta ao longo de um
  ciclo anual em **relógio real** — atesta-se o comportamento sob compressão
  temporal declarada. Enunciar assim, junto das demais limitações.
- **Titularidade do copyright** a confirmar antes da entrega: a licença MIT nomeia
  um titular, e o repositório é público. Definir se o titular é o estudante, a
  orientação ou o IFSP, e ajustar o `LICENSE` se for o caso.
- **Atualização do leiaute no documento do projeto**, vinda da E11: acréscimo de
  `nivel`, unidade do registro, propriedades do identificador e nome de
  tratamento, conforme a seção 10 de `leiaute-entrada.md`. Sem alteração de
  escopo, meta ou cronograma.
- **Limitação vinda da E11 (ADR-0005):** uma linha por egresso adere só em parte à
  letra do art. 19 do Regulamento — a turma anterior perde o egresso que conclui
  outro curso. Enunciar assim, junto das demais limitações.
- **Vinda da E12:** atualizar a tabela de blocos no documento do projeto;
  comunicar ao Comitê Permanente as divergências entre fórmula e descrição no
  Anexo I — Ind7, Ind11 e Ind12, e o alcance dos Ind9 a Ind12; e declarar como
  propostas os indicadores que o projeto acrescentou (ADR-0006).
- **Vinda da E13:** comunicar ao Comitê Permanente que o instrumento documentado
  (2019 a 2023) não calcula a maior parte do Anexo I; declarar as adaptações do
  Ind13 (faixas, sem média rigorosa) e do Ind4 ("sim, totalmente"); e declarar que a
  série de sexo e a de gênero não são equivalentes.
- **Vinda da E21:** a limitação da E06 ganha forma. O horário fixo depende do
  hospedeiro ligado, e a execução perdida é **registrada, não evitada**. A rotina viu
  cada situação num disparo, com o tempo comprimido pela API. Declarar assim.

---

## Registro de sessões

Uma linha por sessão, mais recente ao final.

| Data | Etapas trabalhadas | Situação ao encerrar | Pendências |
|------|--------------------|----------------------|------------|
| 20/09/2026 | E01, E02, E03 | E01 a E03 concluídas. Repositório publicado; 17 fontes fichadas; linha de base do instrumento vigente. | Reler Ferreira 2026 e Davis 1989 na íntegra. Python não instalado (E16, E28). `.gitattributes` não criado. Titularidade do copyright a confirmar. |
| 20/09/2026 | E04 | E04 concluída. Quadro de engajamento com onze estratégias, estado da evidência declarado por linha e cruzamento com a norma do IFSP. Pendências de fonte passaram a ter etapa responsável. | Nenhuma pendência sem dono. Releituras de fonte (Ferreira 2026, Davis 1989) e `.gitattributes` → E07, junto com a ferramenta de extração e OCR. Conferências de referência (Ranthum, Praga de Souza, OCR da RN 13/2022), Mello et al. (2023) e titularidade do copyright → E31. Python não instalado segue marcado para E16 e E28. |
| 20/09/2026 | E05 | **Fase 1 encerrada.** E05 concluída: nove parâmetros de contato especificados, cada um com origem declarada (`norma`/`quadro`/`projeto`). Descoberto que o documento do projeto já propunha os sete parâmetros — a etapa manteve os valores e corrigiu a atribuição de origem. Recusa desdobrada em duas; ciclo anual ancorado na turma, absorvendo os arts. 14, 19 e 22 numa só regra. ADR-0003 registrada. | Nenhuma pendência nova sem dono. A E05 **ampliou critérios** de quatro etapas seguintes: E09 (verificar devolução de erro, não só envio), E11 (mais de uma via de contato e semestre de conclusão), E22 (duas manifestações de recusa na tela) e E23 (efeitos distintos por estado). E21 recebeu ponto de verificação sobre o modelo de cadência da rotina nativa. Correção de fundamentação do documento do projeto → E31. Demais pendências inalteradas. |
| 21/09/2026 | E06 | **Fase 2 iniciada.** E06 concluída: ambiente decidido como conteinerização declarativa em máquina local (Docker Engine + Compose), com o WSL2 registrado como substrato trocável. ADR-0002 preenchida com sete critérios, cinco alternativas e consequências. Estado da máquina foi verificado antes de decidir. | Nenhuma pendência nova sem dono. A E06 **acrescentou dois critérios** (contenção do disparo e operação por linha de comando) e **ampliou** E07 (lista de provisionamento fechada; escolher e fixar a imagem por digest), E08 (conferir C1–C10 contra a instância viva), E09 (capturador de SMTP não atende P8 — exigir serviço que devolva erro), E25 (contenção do disparo como característica verificável), E30 (separar o que o guia ensina do que oferece) e E31 (limitação da compressão temporal). Docker Desktop descartado por licença, não por técnica. Demais pendências inalteradas. |
| 21/09/2026 | E07 | E07 concluída. Ambiente de pé e conferido: Ubuntu 24.04 sobre WSL2 com systemd, Docker Engine 29.8.1, LimeSurvey 7.2.0 em imagem própria e MariaDB 11.4. `verifica-ambiente.sh` roda 21 conferências, todas passando. ADR-0004 registrada — imagem própria e leitura de devoluções por rotina. As duas releituras de fonte foram encerradas, com correção material em cada uma. | Nenhuma pendência nova sem dono. **Encerradas:** releituras de Ferreira e Davis, `.gitattributes`, Python (que destrava E16 e E28). **Ampliadas:** E09 ganha a rotina própria de devoluções e o correio só na rede interna; E08 ganha a conferência do caminho `latest-master`; E21 ganha o problema do WSL encerrar a distro ociosa e derrubar os contêineres — falha silenciosa que precisa de mecanismo. Conferências de referência e titularidade do copyright seguem na E31. |
| 22/09/2026 | E08 | E08 concluída. LimeSurvey 7.2.0 build 260921 instalado, com a instalação convertida em desatendida e idempotente — `down -v` seguido de `up -d` devolve instância pronta. Capacidades C1 a C10 conferidas contra a instância viva: 7 atendem, 3 parciais, nenhuma ausente. Registro em `docs/especificacao/capacidades-plataforma.md`; verificador versionado em `infra/confere-capacidades.py`. | Nenhuma pendência nova sem dono. **Ampliadas:** E09 (não usar `token_invalid` como indicador de contato inválido sem saber o que ele conta); E15, E26, E27 e E28 (a tabela de respostas é `lime_responses_<sid>`, não `lime_survey_<sid>`); E22 e E23 (recusa exige `emailstatus=OptOut` mais a base central, e a auditoria exige ativar plugin por interface — decidir entre caminho programático ou exceção documentada ao K7); E26 (exercitar o preenchimento parcial pelo percurso real, que esta etapa não pôde). E21 segue com o problema da distro ociosa e com o modelo de cadência por verificar. |
| 27/09/2026 | E09 | E09 concluída. Correio de ensaio em imagem própria (Postfix mais Dovecot), somente na rede interna, com três domínios sob `.test` — cada um produzindo uma linha da tabela de classificação do P8. Serviço `rotinas` criado, por topologia. Rotina `ler_devolucoes.py` implementa o P8 com tabela própria de registro e idempotência. Verificação nas duas direções: **7 de 7** no correio isolado e **7 de 7** na integração ponta a ponta. | Nenhuma pendência nova sem dono. **Ampliadas:** E20 (remetente e retorno já configurados; não confundir com o institucional); E21 (agendar a leitura de devoluções **independentemente** da cadência, porque a devolução temporária não chega no mesmo disparo — e decidir a raiz do hospedeiro que suspende, que já custou três diagnósticos); E23 (a tabela `egressos_devolucoes` é insumo de auditoria; a rotina não toca recusa, por decisão); E26 (exercitar o limiar de três ocorrências e o ciclo de reparo); E28 (cliente de API e ponto de execução prontos, com quatro armadilhas já tratadas); E30 (os três detalhes de correio e a advertência sobre capturador de SMTP). |
| 27/09/2026 | E10 | **Fase 2 encerrada.** E10 concluída: `entregas/guia-replicacao.md` com Partes I a III completas e IV a VI marcadas com a etapa responsável, para que a E30 preencha em vez de reestruturar. Critério verificado por execução — ambiente destruído, repositório clonado em diretório novo, guia seguido ao pé da letra, e os três verificadores nos resultados prometidos (21/21, 7 atendem e 3 parciais, 7/7). | Nenhuma pendência nova sem dono. **Achado novo e quarto sintoma do relógio do WSL, o pior:** um salto para trás durante a inicialização do MariaDB deixa o banco pela metade, sem `root` nem verificação de saúde autenticando — tratado desligando o TLS do banco, coerente com a postura do ambiente, o que obrigou `--skip-ssl` nos clientes porque o cliente 11.4 exige TLS. **Dois defeitos do próprio guia corrigidos pelo teste:** ordem das seções (o script do repositório vinha antes do clone) e números estimados, agora medidos. **Ampliada:** E30 herda a instrução de refazer o teste do critério ao preencher as partes restantes. |
| 28/09/2026 | E11 | **Fase 3 iniciada.** E11 concluída: `docs/especificacao/leiaute-entrada.md` com dez campos — os nove do documento do projeto, que já propunha o leiaute e já atendia à E05, mais `nivel`, exigido pelos indicadores do Regulamento. Uma linha por egresso, com a conclusão mais recente (ADR-0005). Identificador estável, sem forma de CPF e distinto do token; nome de tratamento (nome social, Decreto nº 8.727/2016); leiaute fechado, com três níveis de consequência e as restrições do ensaio como propriedade do arquivo. Critério verificado nas duas direções — dez campos e onze consumidores, nenhum órfão — e por execução do exemplo contra as próprias regras. | Nenhuma pendência nova sem dono. **Não conferido:** tamanhos do leiaute contra as colunas da plataforma → E17. **Ampliadas:** E12 (cinco atributos pré-preenchidos, com nível); E13 (domínio de cursos e unidades compartilhado, sem "Outros"); E16 (leiaute, e DDD terminado em 0 só depois de reconferir na Anatel); E17 (validação prévia, trilha e eliminação do arquivo, precedência entre contato corrigido e extração nova); E19; E20 (saudação neutra); E21 (D0 por calendário, âncora móvel, duas vias na fila de correção); E23; E25 (arquivos inválidos de propósito); E26 (reparo automatizável); E30; E31 (atualizar o leiaute no documento do projeto e declarar a aderência parcial ao art. 19). |
| 28/09/2026 | E12 | E12 concluída: `docs/especificacao/blocos-instrumento.md` com onze blocos — os sete do art. 17 do Regulamento, três de controle (consentimento, identificação acadêmica, contato e manifestações) e um de recortes de equidade. Critério lido como indicador do Anexo I ou objetivo expresso do Regulamento, com origem declarada (ADR-0006). Verificado nas duas direções e por execução: nenhum bloco sem indicador, dezoito dos dezenove indicadores do Anexo I alimentados (o Ind1 é registro institucional) e todos os objetivos de coleta do art. 3º com bloco. Achado: as fórmulas do Anexo I são texto, e três medem outra coisa que a descrição; adotada a descrição. Linha de base corrigida em três pontos. | Nenhuma pendência nova sem dono. **Não relido:** o conteúdo vigente dos blocos → a E13 confirma a leitura do Bloco II. **Ampliadas:** E13 (critério por campo, três distinções do Bloco IV, Ind4, Ind13, setor e localidade, gênero ou sexo; completa a seção 12), E14 (públicos viram regras), E15, E18, E22 (três manifestações, com o consentimento do dado sensível), E23, E24 (adesão voluntária), E25, E28 (calcular pelas descrições), E29 e E31 (tabela de blocos no documento do projeto; divergências do Anexo I ao Comitê Permanente). |
| 28/09/2026 | E13 | E13 concluída: seção 12 de `blocos-instrumento.md` com 35 campos, cada um com tipo, domínio, obrigatoriedade, consumidor e origem do domínio. Achado: o Relatório 2 da PAE, lido nesta etapa, mostra que o instrumento documentado calcula pouco do Anexo I e que os Blocos I e VII têm conteúdo diferente do nome. Renda por faixas do Anexo I; doze campos sem consumidor fora; questões 29 e 30 no Bloco I. Pré-preenchimento desatualizado: correção preserva o original e não move o ciclo. Critério verificado por execução: 31 campos padronizáveis com domínio fechado e 4 não padronizáveis justificados. | Nenhuma pendência nova sem dono. **Não percorrida:** a versão do instrumento hoje no ar. **Corrigidos:** oito pontos da E12 e a regra `curso`–`nivel` no leiaute da E11. **Ampliadas:** E14 (regras de campo; valor confirmado), E15 (35 campos e configuração versionada), E17 (regra `curso`–`nivel`; precedência dos atributos corrigidos), E18, E22, E23 (texto livre), E25, E26 (trabalho sem remuneração), E28 (composições; Ind4 e Ind13), E30 (faixas por ciclo) e E31 (comunicação ao Comitê; sexo e gênero não equivalentes). |
| 29/09/2026 | E14 | E14 concluída: `docs/especificacao/navegacao-condicional.md` com as regras de exibição consolidadas, as saídas e os estados, dez caminhos e o diagrama de fluxo. Achado: a recusa, enviada na primeira página, pode sair marcada como concluída — o estado do participante sai de CON1, e não da marca da plataforma. Um bloco por página; voltar com descarte do que sai do caminho; retomada com nome e senha, por decisão do orientando e com o motivo registrado. Verificado por execução: 2.802 combinações, cada uma em exatamente um caminho, e o diagrama renderizado. | Nenhuma pendência nova sem dono. **Não conferido:** nada na plataforma — cinco conferências para a E15. **Ampliadas:** E15 (conferências e dependências dinâmicas), E18, E20 (lembrete explica a retomada), E21 (estado sai de CON1), E22 (descartes na recusa), E23 (e-mail do salvamento; descartes na trilha), E25 (dez caminhos; retomada com senha), E26 (caminhos e recusa) e E28 (denominadores sem recusas; parciais órfãs). |
| 03/10/2026 | E15 | **Fase 3 encerrada.** E15 concluída: instrumento implantado como questionário 202615 — onze grupos, 35 campos, inativo, para a E17 —, com a exportação da instância versionada em `infra/instrumento/instrumento.lss`. Tudo por linha de comando: gerador, importação pela API e exportação por comando de console próprio, porque a API não exporta. Unidades reais (57 campi e 3 antecessoras), cursos ilustrativos. Dois defeitos meus achados por conferência — Bloco VI sumindo sem `.NAOK` e equação sem chaves — e corrigidos. Conferência estrutural independente do gerador, 6 de 6, testada por mutação. Dez caminhos percorridos no navegador numa cópia descartável; cinco conferências da E14 respondidas. | Nenhuma pendência nova sem dono. **Não conferido:** preenchimento por pessoa, outros navegadores, janela de 60 dias, recusa por cota. **Ampliadas:** E16 (listas e nomes da `configuracao/`), E17 (sid, sequência de ativação, estrutura travada), E18 (nome do arquivo para código do instrumento), E20 (reabrir o link recomeça; recusa consome o convite), E21 (recusa marcada como concluída; duas respostas por participante), E22 (e-mail do salvamento fixo no tema; cota como alternativa), E23 (parcial guarda campos fora do caminho, inclusive dado sensível), E25 (conferência estrutural pronta), E26 (cópia de ensaio; `newtest=Y`), E28 (colunas `Q<qid>`, IDA4 decimal, contagem nativa inclui recusas) e E30 (Parte IV a partir do README; trocar as validações do ensaio e a lista de cursos). |
| 03/10/2026 | E16 | **Fase 4 iniciada.** E16 concluída: `scripts/gerar_base_sintetica.py`, determinístico, gera 500 egressos sintéticos de 2016 a 2025 no leiaute da E11, em `dados/sinteticos/`, fora do versionamento. DDDs reconferidos no painel oficial da Anatel: os 67 em uso, nenhum terminado em zero. Nomes inventados, com recusa dos prenomes e sobrenomes frequentes — e correção registrada de uma afirmação minha forte demais sobre coincidência. Endereços nos três domínios do correio de ensaio; vias alternativas, ausência delas e pares compartilhados plantados. Conferência independente, 10 de 10, testada por mutação com sete defeitos, todos reprovados. | Nenhuma pendência nova sem dono. **Não conferido:** a recepção dos nomes e dos tamanhos pela plataforma → E17. **Ampliadas:** E17 (a base tem de passar inteira no validador, com os três alertas esperados), E19 (três pares plantados), E25 (sete defeitos como ponto de partida dos inválidos de propósito) e E26 (casos do P8 já presentes na base). |
| 04/10/2026 | E17 | E17 concluída: base persistente decidida na **ADR-0007** — base central do LimeSurvey, contra a opção do RAEG. Validador das seções 3 a 7 do leiaute, importador e três comandos de console; 500 pessoas na base central e 500 participantes no 202615, sem duplicidade, com acesso fechado e ativação adiada para a E18. Desenho corrigido no meio da etapa: a base central cifra nome e e-mail por padrão, e a precedência leria o cifrado — passou a ser feita dentro da plataforma, com todo contato cifrado. Armadilha da API que apagaria a recusa permanente encontrada e evitada. Verificado: idempotência, precedência nos dois sentidos, recusa preservada, 27 de 27 casos do validador, arquivo rejeitado sem efeito. | Nenhuma pendência nova sem dono. **Não conferido:** recusa global nativa em ação, cifragem da tabela do questionário, busca ativa real, retenção. **Ampliadas:** E18 (atributos já em código; ativação é dela), E19 (cifragem determinística; conferir identificador no participante), E21 (correção de contato grava nos dois lugares, na base central só por console), E22 (exercitar a recusa global nativa), E23 (cifrar o questionário, retenção, cifragem determinística), E25 (27 casos; idempotência e recusa preservada) e E30 (dois comandos, no hospedeiro; armadilhas). |
| 04/10/2026 | E18 | E18 concluída: pré-preenchimento da identificação como estrutura — IDA1, IDA3, IDA4 e IDA5 com padrão no atributo do participante, ligação calculada num lugar só —, caminho completo refeito do zero (implantar, preparar, importar, ativar) e **questionário 202615 ativo**. Conferência estrutural 7 de 7, com a nova sétima falhando antes e passando depois. Três acessos de amostra, um por nível, abriram com os atributos do arquivo de origem; a correção de curso levou o nível junto, ficou na resposta e preservou o original; fila de revisão exercitada pela API; os 500 com atributos válidos; controle de acesso conferido; respostas de teste apagadas. | Nenhuma pendência nova sem dono. **Não conferido:** janela de validade do acesso → E21; fila de revisão como rotina → E28. **Ampliadas:** E19 (verificar sobre o estado reimplantado e ativo), E20 (forma do endereço individual), E21 (`validfrom`/`validuntil` por ciclo) e E28 (fila de revisão e taxa de correção). |
| 04/10/2026 | E19 | **Fase 4 encerrada.** E19 concluída: conferência só de leitura `infra/confere-participantes.py`, com oito verificações — tokens, identificadores, elo com a base central pelo `participant_id` derivado, e e-mail compartilhado comparado em claro e pelo cifrado determinístico. **8 de 8, critério atendido**; os três grupos de e-mail compartilhado são exatamente os três pares plantados pela E16. "Token inválido" definido e verificado — o contador nativo conta token vazio, o que fecha o ponto aberto da E08. E-mail compartilhado é alerta para revisão humana, sem fusão automática. Conferência testada com quinze defeitos plantados, todos reprovados. | Nenhuma pendência nova sem dono. **Não detectável:** a mesma pessoa sob identificadores e endereços distintos. **Ampliadas:** E21 (conferência como guarda antes do disparo), E23 (procedimento de revisão humana), E25 (procedimento e casos negativos prontos) e E28 (não fundir os grupos na extração). |
| 04/10/2026 | E20 | **Fase 5 iniciada.** E20 concluída: convite e lembrete em `infra/instrumento/mensagens.py`, fonte única que vai no `.lss` e é aplicada ao 202615 ativo pelo `aplicar-mensagens`. Remetente de ensaio trocado de `naoresponda@` para `acompanhamento@egressos.test`, com caixa própria, porque o P7 veda no-reply — remetente e retorno como propriedades do questionário. Lembrete com dois ramos num modelo só, pelo atributo `variante_lembrete` (7º, acrescentado por comando de console com esvaziamento do cache de esquema da web). Recusa de contato pela lista de bloqueio da base central. Convite de teste real a um participante sintético: **9 de 9**, mensagens lidas renderizadas, estado final limpo. Primeira execução falhou e deixou resíduo, desfeito à mão; limpeza tornada independente por passo. | Nenhuma pendência nova sem dono. **Não verificado:** efeito do bloqueio → E22/E23; prazo de 60 dias → E21; URL pública → E30. **Ampliadas:** E21 (gravar o ramo antes do lembrete; abrir o link cria resposta com `lastpage = 0`), E22 (exercitar `GLOBALOPTOUTURL`), E30 (remetente institucional, URL pública, armadilhas). |
| 05/10/2026 | E21 | E21 concluída: **rotina agendada ativa** no contêiner `rotinas`, com disparo às 10:00 em dia útil e devoluções a cada 30 min, separadas, em **modo simulado** até a E26 (decisão do orientando). O ponto 13.1 foi respondido no código: a rotina nativa é intervalo mais máximo, sem agendador, e por isso a cadência D+*n* por participante ficou fora dela, sem alterar o P3 (ADR-0008). Também no código: datas de envio em UTC, lote de 50, lote que para na primeira falha e `date_invited` não gravado. `lastpage = 0` é `convidado`, medido pelo caminho real. Guarda E19 1–7 mais E20; execução perdida registrada. A distribuição do WSL foi achada parada depois de reinício, e a tarefa de logon que só a liga foi criada com autorização e conferida. Critério: execução real das 10:00 às 10:00:08; `--agendada` 14 de 14, com o disparo às 10:06:11 atingindo só os 4 não respondentes vencidos, com o ramo certo; regras 7 de 7, com 16 de 16 mutações reprovadas; `--perdida` 8 de 8. A primeira execução falhou na limpeza porque o relógio do WSL voltou 7,3 s; foi desfeita à mão e a conferência foi endurecida. | Nenhuma pendência nova sem dono. **Não verificado:** reinício real do Windows; cadência em dias de calendário; doze meses entre ciclos (um questionário só). **Ampliadas:** E22 (recusa já lida pela rotina), E23 (registro como trilha; anonimizar respostas quebra o estado; datas em UTC), E25 (procedimentos prontos e 16 mutações), E26 (ligar o modo real, 255 convites na primeira execução; **operação de reparo nos dois lugares**; dias de calendário), E28 (datas UTC; envios por participante), E30 (Parte V; tarefa de logon como opção de hospedeiro; feriados e calendário; relógio; **virada de ciclo**) e E31 (execução perdida registrada, não evitada). |
