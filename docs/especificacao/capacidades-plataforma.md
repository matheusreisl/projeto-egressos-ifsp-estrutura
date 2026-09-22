# Capacidades da plataforma — conferência contra a instância

**Etapa:** E08 — instalar o LimeSurvey e validar o acesso
**Data da conferência:** 22/09/2026
**Ambiente:** o da [ADR-0002](../decisoes/0002-ambiente-execucao.md), com a imagem
própria da [ADR-0004](../decisoes/0004-imagem-propria-e-leitura-de-devolucoes.md)

## 1. Por que este documento existe

A seção 13 de [`parametros-contato.md`](parametros-contato.md) listou **dez
capacidades** que a plataforma precisa suportar para que os parâmetros de contato
sejam exequíveis, e registrou expressamente que afirmar o que o LimeSurvey faz
nativamente, antes de haver instância, seria asserção sem conferência.

A instância existe. Este documento é a conferência, uma a uma, **contra a
instância viva** — e não contra documentação de produto.

O que se afirma aqui foi verificado por execução: questionário de teste criado,
tabela de participantes ativada, participantes sintéticos inseridos sob domínio
`.test`, esquema inspecionado e comportamento observado. O questionário de teste
foi removido ao fim, sem deixar tabela remanescente.

## 2. Versão e configuração aplicada

| Item | Valor |
|---|---|
| LimeSurvey | **7.2.0**, build **260921** |
| Versão de banco | 716 |
| Versão de recursos | 30507 |
| PHP | 8.3.33 |
| Banco | MariaDB 11.4.13 |
| Prefixo de tabelas | `lime_` |
| Conjunto de caracteres | `utf8mb4` / `utf8mb4_unicode_ci` |
| Fuso horário | `America/Sao_Paulo` |
| `urlFormat` | `path`, com `showScriptName` verdadeiro |
| `RPCInterface` | `json` |
| `debug` | 0 |

A instalação é **desatendida e idempotente**: a inicialização do contêiner gera o
`config.php` a partir do `.env` e executa o instalador de console quando o banco
está vazio. Verificado por execução — `docker compose down -v` seguido de
`up -d` devolve instância instalada, sem passo manual.

### 2.1 Sobre o caminho `latest-master`

A ADR-0004 registrou a dúvida: o pacote da linha 7.x vem de um caminho cujo nome
sugere compilação de desenvolvimento.

**O que se pode afirmar.** O `version.php` do pacote declara `versionnumber`
7.2.0 e `buildnumber` 260921, e a instância instalada reporta os mesmos valores;
a página oficial de descarga apresenta esse pacote como a versão corrente da
linha 7.x. **O que não se pode afirmar** é que a política de publicação do
projeto LimeSurvey distinga, nesse caminho, compilação de linha estável de
compilação de desenvolvimento — isso não foi verificado e não há como verificar
a partir do artefato.

A consequência prática é nenhuma para este trabalho, porque a versão está fixada
por soma de verificação: o que se instala é sempre o mesmo pacote, seja qual for
o nome do caminho.

## 3. Quadro das capacidades

| # | Capacidade | Veredito |
|---|---|---|
| C1 | endereço individual, único e não adivinhável | **atende** |
| C2 | estado de conclusão por participante | **atende** |
| C3 | distinção entre acesso iniciado e não iniciado | **atende** |
| C4 | contagem e data do último disparo | **atende** |
| C5 | disparo seletivo por estado, sem interação humana | **atende** |
| C6 | marcação persistente de recusa entre ciclos | **parcial** |
| C7 | validade temporal do acesso | **atende** |
| C8 | registro do estado de entrega | **parcial** |
| C9 | atributos por participante | **atende** |
| C10 | trilha de auditoria | **parcial** |

Sete atendem sem ressalva. As três parciais não são lacunas da plataforma no
mesmo sentido: **C6** e **C8** exigem escolha de implementação, e **C10** exige
uma operação que a plataforma não expõe por comando. Detalhamento abaixo.

## 4. Detalhamento

### C1 — endereço individual, único e não adivinhável · atende

Coluna `token`, `varchar(36)`, indexada. Os endereços gerados têm **15
caracteres** alfanuméricos — comprimento padrão, configurável por questionário.
Unicidade confirmada na base gerada.

Verificado também por comportamento: uma requisição ao endereço individual
devolve o questionário (HTTP 200, título correto). O endereço tem a forma
`…/index.php/<sid>?token=<token>`.

### C2 — estado de conclusão por participante · atende

Coluna `completed` na tabela de participantes, e o contador `token_completed` no
resumo que a API devolve por `get_summary`.

### C3 — distinção entre acesso iniciado e não iniciado · atende

A tabela de respostas traz `startdate`, `submitdate` e `lastpage`. Uma linha com
`startdate` preenchido e `submitdate` nulo é lida pela própria plataforma como
resposta incompleta: o `get_summary` passou a `incomplete_responses = 1` com
`completed_responses = 0`.

**Achado que muda a leitura da máquina de estados da E05.** Abrir o endereço
individual **não cria linha de resposta** — verificado: depois de uma requisição
bem-sucedida ao endereço, a tabela de respostas continuava vazia. Na plataforma,
"iniciado" significa **ter submetido ao menos uma página**, não ter aberto o
link.

A consequência é direta para a seção 12 de `parametros-contato.md`: o estado
`em preenchimento` corresponde a *submeteu página e não concluiu*, e quem abriu
o convite sem avançar permanece indistinguível de quem não o abriu. Como a E05
já decidiu **não rastrear abertura** (seção 10.3), isso é coerente com o
desenho — mas precisa estar escrito, porque "iniciou o preenchimento" sugere
outra coisa em linguagem comum.

### C4 — contagem e data do último disparo · atende

Colunas `sent`, `remindersent` e `remindercount`.

### C5 — disparo seletivo por estado, sem interação humana · atende

A API expõe `invite_participants` e `remind_participants`. O disparo é, portanto,
acionável por rotina, sem tela — que é o que a E21 exige.

**Não se verificou aqui** o modelo de cadência que essas rotinas expressam. É o
ponto de verificação da seção 13.1 de `parametros-contato.md` e continua sendo da
**E21**: nada nesta etapa o antecipa.

### C6 — marcação persistente de recusa entre ciclos · parcial

A plataforma tem **duas marcações distintas**, e a distinção é exatamente o que
decide se a capacidade é atendida:

| Onde | Escopo | Sobrevive ao ciclo? |
|---|---|---|
| `lime_tokens_<sid>.blacklisted` | do questionário | **não** — morre com a tabela de participantes daquele ciclo |
| `lime_participants.blacklisted` | base central de participantes | **sim** |

O vínculo entre as duas é a tabela `lime_survey_links`, que liga
`participant_id` a `token_id` por questionário e guarda `date_invited` e
`date_completed`.

**Precisão obtida por experimento, e que contraria a leitura intuitiva.** Marcar
`blacklisted = 'Y'` no token **não** moveu o contador `token_opted_out`. O que o
moveu foi `emailstatus = 'OptOut'`. São dois mecanismos diferentes, e usar um
esperando o efeito do outro produz um bloqueio que não bloqueia.

**Por que fica parcial.** A capacidade existe, mas **só pela base central**, e
isso é uma decisão de arquitetura, não uma configuração: a recusa de contato do
parâmetro P6 — permanente até revogação — exige que a base central seja adotada
e mantida entre ciclos. Isso reforça, por outro caminho, a decisão de base
persistente de participantes que a **E17** precisa registrar em ADR.

### C7 — validade temporal do acesso · atende

Colunas `validfrom` e `validuntil`, do tipo `datetime`. Atende à janela de 60
dias do parâmetro P5.

### C8 — registro do estado de entrega · parcial

A plataforma tem `emailstatus` na tabela de participantes e a tabela
`lime_failed_emails`, cujo esquema é adequado ao que a P8 precisa registrar:
`recipient`, `error_message`, `status`, `email_type`, `surveyid`, `responseid`,
`created`, `updated`.

**Fica parcial pelo motivo já decidido, e não por surpresa:** a plataforma
registra o estado, mas **não lê a devolução**, porque o caminho nativo para isso
depende da extensão `imap`, ausente por decisão da ADR-0004. A leitura e a
classificação são rotina própria, e são escopo da **E09**.

**Ponto em aberto, honestamente registrado.** Definir `emailstatus = 'invalid'`
não moveu o contador `token_invalid`. Não se determinou o que o move — provável
que seja validade temporal ou usos restantes, e não estado de entrega. Quem
depende disso é a E09, e é lá que precisa ser resolvido: **não usar
`token_invalid` como indicador de contato inválido sem antes verificar o que ele
conta.**

### C9 — atributos por participante · atende

Colunas `attribute_1`, `attribute_2`, … criadas sob demanda na ativação da tabela
de participantes. Verificado com dois atributos, preenchidos com semestre de
conclusão e curso — que são, não por acaso, dois dos campos que a **E11** tornou
obrigatórios.

### C10 — trilha de auditoria · parcial

O plugin **AuditLog acompanha a plataforma**, e o seu código traz a criação da
tabela de registro. Mas:

1. vem **inativo** na instalação;
2. **nenhuma tabela de auditoria existe** enquanto ele não for ativado;
3. a ativação **não é alcançável por comando de console** — o comando `plugin`
   oferece apenas as ações `cron` e `index`;
4. marcar `active = 1` diretamente no banco **não basta**: o gancho que cria a
   tabela não é executado por essa via, e a tabela continua ausente.

**Consequência para a E23 e para o guia.** A ativação da trilha de auditoria
passa hoje pelo gerenciador de plugins, na interface. Isso colide com o critério
K7 da ADR-0002 — o guia é feito de comandos, não de capturas de tela. A E23
precisa decidir entre encontrar um caminho programático que execute o gancho de
ativação ou **declarar este passo como exceção documentada**, com a operação de
tela descrita. Não se resolve por omissão: a trilha de auditoria é requisito de
conformidade, não conveniência.

## 5. O que esta conferência não permite afirmar

1. **Não se verificou o contador de resposta incompleta a partir do fluxo real do
   respondente.** A linha parcial foi inserida diretamente no banco, porque o
   método `add_response` da API **preenche `submitdate` mesmo quando não se pede**
   — isto é, cria sempre resposta concluída. O que se demonstrou é que o modelo de
   dados representa o estado e que a plataforma o lê corretamente. Exercitar o
   percurso do respondente, com preenchimento parcial e retomada, é cenário da
   **E26**.
2. **Não se verificou o modelo de cadência** das rotinas de convite e lembrete —
   permanece com a E21, conforme a seção 13.1 de `parametros-contato.md`.
3. **Não se verificou envio de mensagem**, em nenhuma direção. Não havia serviço
   de correio no ambiente, e não haverá antes da E09.
4. **Nada aqui foi verificado sobre dados de pessoas reais.** A base foi
   sintética, o domínio foi `.test` e o questionário de teste foi removido.

## 6. O que esta etapa determina para as seguintes

- **E09** — não usar `token_invalid` como indicador de contato inválido sem
  descobrir o que ele conta; a fila de correção da P8 se apoia em `emailstatus` e
  em `lime_failed_emails`.
- **E15** — a tabela de respostas chama-se `lime_responses_<sid>`, e **não**
  `lime_survey_<sid>`, que é o nome que a documentação e os tutoriais antigos
  usam. Toda consulta direta precisa do nome novo.
- **E17** — a persistência da recusa entre ciclos depende da **base central de
  participantes**, não da tabela do questionário. É argumento adicional para a
  ADR de base persistente que aquela etapa já previa.
- **E21** — o disparo seletivo é acionável por API; o modelo de cadência continua
  por verificar.
- **E22 e E23** — recusa de contato exige `emailstatus = 'OptOut'` **e** marcação
  na base central; `blacklisted` no token sozinho não produz o efeito esperado. A
  trilha de auditoria exige ativação de plugin por interface, ponto a resolver.
- **E26** — exercitar o preenchimento parcial pelo percurso real, que esta etapa
  não pôde exercitar.
- **E28** — a extração conversa com a instância pela API RemoteControl, já
  habilitada e verificada.
