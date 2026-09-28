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

### [ ] E14 — Definir a lógica de navegação condicional
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

### [ ] E15 — Implementar a estrutura no LimeSurvey
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

---

## Fase 4 — Base sintética e acesso rastreável
Metas 4 e 5 · set–nov/26

### [ ] E16 — Gerar a base sintética
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

### [ ] E18 — Configurar acesso por token e pré-preenchimento
- **Objetivo:** endereço individual por participante, com atributos pré-carregados.
- **Entregável:** configuração aplicada e documentada.
- **Conclusão quando:** um acesso de amostra abrir com os atributos corretos.
- **Vindo da E12:** os cinco atributos vão para o bloco de identificação
  acadêmica, editáveis, com a correção registrada e o valor original preservado.
- **Vindo da E13:** o nível não se edita por conta própria — acompanha o curso
  escolhido; e a correção não move o ciclo em andamento (seção 12.5).

### [ ] E19 — Validar unicidade e deduplicação
- **Objetivo:** garantir integridade da base de participantes.
- **Entregável:** registro da verificação.
- **Conclusão quando:** nenhum token repetido ou inválido for encontrado.
- **Vindo da E11:** além de token repetido, verificar identificador repetido,
  identificador igual a algum token e o alerta de endereço principal compartilhado
  por identificadores distintos — sintoma de pessoa duplicada.

---

## Fase 5 — Automação do contato e conformidade
Metas 6 e 7 · out–nov/26

### [ ] E20 — Configurar convites e modelos de mensagem
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

### [ ] E21 — Configurar a rotina agendada de lembretes
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
