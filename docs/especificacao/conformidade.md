# Conformidade: recusa, trilha de auditoria, cifragem, anonimização e retenção

**Etapa:** E23 — configurar anonimização e trilha de auditoria
**Data:** 05/10/2026
**Implementa:** o P6 de [`parametros-contato.md`](parametros-contato.md) (as duas
recusas e a revogação), a distinção da seção 10.2 do P8 (contato inválido não é
recusa) e os arts. 6º, III, 8º, §5º, 11, 18, 37 e 46 da LGPD, conforme o
[fichamento](../pesquisa/fichamentos/brasil-lei-13709-2018.md)
**Decisão:** [ADR-0010](../decisoes/0010-conformidade-no-mecanismo.md)
**Onde está:** [`scripts/conformidade.py`](../../scripts/conformidade.py) (rotina) ·
[`infra/conformidade.py`](../../infra/conformidade.py) (operação: `aplicar`,
`revogar`) · comandos de console `ativarauditoria` e `revogarrecusa` ·
[`infra/limesurvey/Dockerfile`](../../infra/limesurvey/Dockerfile), seções 4.1 e 4.2 ·
[`infra/confere-conformidade.py`](../../infra/confere-conformidade.py)

## 1. O que esta etapa entrega

| Item | Como |
|---|---|
| Recusa de contato em todos os ciclos | as três vias — tela, conclusão (CT4) e mensagem — chegam à **base central**; o ciclo seguinte não convida quem recusou |
| Recusa de consentimento só no ciclo | registrada, sem tocar a base central; o ciclo seguinte convida |
| Contato inválido | não é recusa: não é registrado como tal, não bloqueia nada |
| Registro de cada recusa | `egressos_recusas`: tipo, via, momento, ciclo, versão do termo, chegada à base central, revogação |
| Revogação | pelo operador, a pedido do egresso, por comando; registrada e com trilha |
| Trilha de auditoria | `AuditLog` da plataforma, ativado **por comando**, com uma correção de defeito na imagem |
| Cifragem em repouso | EQ1 a EQ3, AF4 e CT1 a CT3 |
| Dado sensível sem consentimento | apagado das respostas interrompidas, e registrado |
| Página de recusa | em português — sete traduções acrescentadas na imagem |
| Termo | versão `ensaio-2`, com a guarda por princípio e a cifragem |
| Anonimização na extração e retenção | política documentada (seções 7 e 8), para a E28 e a E30 |

## 2. As recusas

### 2.1 O que faltava

Até a E22, só a recusa pelo **endereço da mensagem** chegava à base central — a
plataforma a leva sozinha. A recusa feita na **tela** (CON1 = "não quero mais ser
contatado") e a marcada ao **concluir** (CT4) valiam só no questionário do ciclo: a
rotina da E21 não disparava a elas, mas o ciclo seguinte as convidaria. E nenhuma
recusa ficava registrada com data, via e versão do termo.

### 2.2 A rotina de conformidade

Tarefa do agendador, a cada 30 minutos, em qualquer dia, e **sempre de verdade**,
qualquer que seja o modo do disparo: não contata ninguém, só protege. Três deveres,
nesta ordem.

**1. Registrar.** Cada manifestação vira uma linha de `egressos_recusas`:

| Via | De onde a rotina a lê | Tipo | Momento | Versão do termo |
|---|---|---|---|---|
| tela | resposta enviada com CON1 = `RCONS` ou `RCONT` | consentimento ou contato | `CONDH` da resposta (E22) | `CONV` da resposta |
| conclusão | resposta enviada com CON1 = `CONC` e CT4 marcado | contato | data de envio da resposta | `CONV` da resposta |
| mensagem | participante com `OptOut` | contato | **da trilha de auditoria**; sem ela, o da detecção | a vigente no questionário |
| base central | pessoa bloqueada por outro questionário ou ciclo | contato | da trilha, ou da detecção | a vigente |

A coluna `fonte_do_momento` diz de onde veio cada data — `CONDH`, `submitdate`,
`auditoria` ou `deteccao` —, para que não se confunda a data em que a pessoa recusou
com a data em que a rotina a viu. Todo instante vai em ISO 8601, em UTC, com
`+00:00`. Nada de token, nome nem endereço.

**2. Levar a recusa de contato à base central.** Para cada recusa de contato aberta
que ainda não chegou lá, a rotina aplica a recusa global **pela via da própria
plataforma**: abre a mesma página de confirmação que a mensagem leva e confirma por
POST, com o token de proteção do formulário. Os modelos da plataforma marcam o
participante (`OptOut`) e a base central (`blacklisted`), e a trilha registra. A
escolha, e não uma gravação direta, é o que mantém um caminho só para a recusa de
contato — o que a plataforma faz quando o egresso clica é o que ela faz quando a
rotina age por ele.

**3. Apagar dado sensível sem consentimento.** Resposta não enviada com CON2
diferente de "concordo" e campo do bloco de equidade preenchido tem esses campos
apagados. É o achado da E15: o descarte da plataforma só ocorre no envio final, e
quem deu o consentimento específico, preencheu o bloco, voltou, retirou o
consentimento e abandonou deixava o dado guardado. O apagamento é por gravação direta
— a API recusa alterar resposta quando o questionário não permite edição depois de
concluído, e o instrumento não permite, de propósito — e fica em
`egressos_higienizacoes`.

**Idempotente.** Manifestação já registrada não se registra de novo, e recusa
revogada não volta a contar. Uma recusa nova depois da revogação, pela mensagem, é
registrada — a trilha dá o momento da última mudança, e não o da primeira.

### 2.3 O critério: todos os ciclos, ou só o corrente

| | Recusa de contato | Recusa de consentimento | Contato inválido |
|---|---|---|---|
| Ciclo corrente | a rotina da E21 não dispara | a rotina da E21 não dispara | a rotina da E21 não dispara |
| Base central | **bloqueada** | intacta | intacta |
| Ciclo seguinte | a importação não acrescenta a pessoa (E17), e a plataforma **recusa** o convite em qualquer questionário | convidada | convidada |

**Conferido no ciclo seguinte de verdade:** um questionário novo, com as mesmas
pessoas ligadas à base central. A plataforma recusou convidar as três que recusaram
contato — uma por via — e convidou quem recusou só o consentimento e quem tinha
contato inválido.

### 2.4 A revogação

O egresso pede **respondendo a uma mensagem**, como o termo diz — o canal humano que
a caixa `acompanhamento` já recebe (E20). O operador roda:

```bash
python3 conformidade.py revogar --identificador SIN-000123 \
    --registro "pedido por resposta de 05/10/2026 na caixa acompanhamento"
```

O comando roda a rotina uma vez, para que a recusa esteja registrada antes de ser
revogada; tira o bloqueio da base central e devolve `OK` aos participantes com
`OptOut`, pelos modelos da plataforma (comando de console `revogarrecusa`, com
trilha); e marca a revogação no registro, com o texto dado.

**Por que pelo operador, e não pelo próprio egresso** (decisão do orientando): a
plataforma oferece revogação por link (`allowunblacklist`), mas com ela **qualquer
pessoa com o endereço individual do egresso** poderia desfazer a recusa dele — e o
endereço é transportável por desenho (P9). A recusa é feita pelo egresso com um
clique; a revogação, com uma resposta. O art. 8º, §5º pede procedimento "gratuito e
facilitado", e responder a uma mensagem é ambos.

**A resposta com a recusa antiga continua na plataforma.** No ciclo corrente, a
pessoa segue como recusa de contato para a rotina da E21 — ela já encerrou o
questionário. A revogação vale para os ciclos seguintes, e a rotina de conformidade
não volta a bloquear.

## 3. A trilha de auditoria

### 3.1 Ativada por comando

O `AuditLog` acompanha a plataforma e vinha inativo. A E08 mostrou que marcar
`active = 1` no banco não basta, porque a tabela é criada pelo evento
`beforeActivate`. O comando de console `ativarauditoria` faz o que o painel faz,
conferido no código (`PluginManagerController::activate`): carrega o plugin, despacha
o evento e só então marca o plugin ativo. O critério K7 da ADR-0002 — guia de
comandos, e não de telas — fica preservado. Executado por:

```bash
python3 conformidade.py aplicar
```

**Numa instalação do zero, este passo entra na sequência**, depois do `ativar` do
instrumento: a trilha nasce desativada.

### 3.2 O que ela registra

Mudanças no participante do questionário e na base central, respostas pela
digitação no painel, usuários, permissões e acessos. Cada linha tem a data (em UTC),
quem agiu (vazio quando foi o egresso ou o console), a entidade e **só os campos que
mudaram**, com o valor anterior e o novo. A recusa pela mensagem aparece como duas
linhas — `emailstatus` passando a `OptOut` e `blacklisted` a `Y` —, com data: é dali
que a rotina tira o momento da recusa, que a plataforma sozinha não guarda.

**A trilha também guarda dado pessoal.** Uma atualização registra só os campos que
mudaram, sem dado pessoal na recusa e na revogação. Mas a **criação** de um
participante registra todos os campos, e cada importação deixa nome e e-mail do
questionário na trilha. Ela precisa da mesma proteção e da mesma política de guarda
da base (seção 8). E é tabela MyISAM, como a plataforma a cria: sem transação.

### 3.3 A correção na imagem

Oito registros do plugin leem o usuário atual sem conferir se ele existe. Na web,
quando quem age é o egresso, isso é aviso, e a recusa passa, com usuário vazio. **No
console é erro fatal:** com a trilha ativa, gravar na base central por comando —
a importação da E17, a revogação — quebrava. Observado nesta etapa. A seção 4.2 do
Dockerfile aplica, nos oito, a mesma conferência que três outros registros do plugin
já fazem; a construção para se o padrão sobrar, e o `aplicar` confere que a correção
está na imagem. Depois dela, a importação dos 500 rodou com a trilha ativa.

### 3.4 O que compõe a trilha do mecanismo

| Fonte | Registra | Etapa |
|---|---|---|
| `lime_auditlog_log` | mudanças em participantes, base central, usuários, permissões, acessos | E23 |
| `egressos_recusas` | cada recusa, com via, momento, versão do termo, chegada à base central e revogação | E23 |
| `egressos_higienizacoes` | cada resposta que teve dado sensível apagado, e quais campos | E23 |
| `egressos_execucoes` | cada execução das rotinas, prevista e real, inclusive a perdida | E21 |
| `egressos_disparos` | cada convite e lembrete tentado | E21 |
| `egressos_devolucoes` | cada devolução lida e a marcação de contato inválido | E09 |
| `egressos_importacoes` | cada importação: data, resumo do arquivo, contagens | E17 |
| respostas: `CON1`, `CON2`, `CONV`, `CONDH` | o aceite e a recusa na tela, com versão e momento | E22 |

## 4. Cifragem em repouso

Sete campos passam a ser gravados cifrados, com a chave da plataforma — a mesma que
já cifra nome e e-mail na base central (E17):

| Campos | Por quê |
|---|---|
| EQ1, EQ2, EQ3 | gênero, raça/cor e deficiência: os dois últimos, dado sensível (LGPD, art. 5º, II) |
| AF4 | o texto livre, que pode conter dado pessoal não previsto, inclusive de terceiros (E13) |
| CT1, CT2, CT3 | os contatos atualizados pelo egresso |

**Conferido por comportamento:** no banco, o valor gravado não é o valor; na
exportação da plataforma, é. EQ4, que não está na lista, fica em claro. A
conferência estrutural ganhou a nona verificação — os cifrados na instância são
exatamente os da tabela da especificação —, que **falhou antes da reimplantação e
passou depois**.

**Nome e e-mail do participante do questionário continuam em claro** no ensaio
(decisão do orientando). A base central, que é a persistente, já os cifra. Cifrá-los
também no questionário é recurso da plataforma, mas quatro conferências os leem
direto no banco e precisariam passar a ler pela API. Fica como ajuste da implantação
real (E30). A cifragem da plataforma é **determinística** (E17): o mesmo valor gera o
mesmo texto cifrado, o que permite comparar sem decifrar e revela igualdade.

Mudar a cifragem é mudar estrutura, e a plataforma não muda estrutura de questionário
ativo: o 202615 foi **reimplantado** pela segunda vez, sem nada a perder (0
respostas, nada enviado), como na E22.

## 5. A página de recusa em português

A tradução pt-BR do LimeSurvey 7.2 não tem sete mensagens das páginas de recusa e de
revogação globais, inclusive a frase principal da confirmação e o resultado que
aparece depois dela. O egresso que recusava contato lia a confirmação em inglês
(achado da E22).

A seção 4.1 do Dockerfile acrescenta as sete ao arquivo de idioma, na construção da
imagem, por um script PHP próprio
([`acrescenta-traducoes.php`](../../infra/limesurvey/traducoes/acrescenta-traducoes.php))
que **nunca substitui** tradução existente e confere o que escreveu — conferido: 7
acrescentadas, nenhuma das 5.625 existentes alterada, e uma segunda execução sem
efeito. As traduções estão em
[`traducoes/pt-BR.json`](../../infra/limesurvey/traducoes/pt-BR.json), e dizem ao
egresso o efeito — "não receberá mais convites nem lembretes de nenhum questionário
dele" —, e não só "lista central de participantes". A imagem passou a
`egressos/limesurvey:7.2.0-1`.

## 6. O termo `ensaio-2`

Duas mudanças, e por isso versão nova: a cifragem das respostas sensíveis, dita no
parágrafo "Como e por quanto tempo"; e a **guarda por princípio**, no lugar do
marcador da E22:

> Os seus dados acadêmicos e de contato ficam guardados enquanto você fizer parte do
> acompanhamento de egressos. As suas respostas ficam identificadas só até serem
> usadas no cálculo dos indicadores do ano; depois disso, o que fica não identifica
> você. O registro da sua manifestação sobre este termo — inclusive uma recusa — fica
> guardado enquanto for preciso comprovar que ela foi respeitada. Prazos em anos:
> [a preencher pela instituição].

Os anos são da **instituição**, pela tabela de temporalidade de documentos do IFSP
(decisão do orientando). O arquivo `ensaio-1.html` fica intacto, e o gerador conferiu
isso: é a prova do que as respostas daquela versão aceitaram.

## 7. Anonimização na extração (para a E28)

**A anonimização nativa das respostas não serve** a este mecanismo: sem o token na
resposta, a rotina da E21 não distingue `convidado` de `em preenchimento` nem vê a
conclusão. A anonimização acontece **na extração**, e é a E28 que a aplica. A
política:

| Dado | Na extração |
|---|---|
| token, `participant_id`, nome, e-mail, telefone | **nunca saem** |
| `identificador` | só pseudonimizado, por resumo com chave guardada fora do conjunto, e só se o uso exigir série por pessoa; senão, não sai |
| CT1 a CT3 | não saem: servem ao reparo de contato, e não aos indicadores |
| `CONV`, `CONDH` | não saem no conjunto de indicadores: são prova de consentimento, e ficam onde estão |
| AF4 | **não sai** sem revisão humana que retire dado pessoal — inclusive de terceiros — ou sai só categorizado |
| EQ1 a EQ3 | só **agregados**, com tamanho mínimo de célula a fixar na E28, e só de quem deu CON2 |
| PM3 (renda) | só a faixa, e só agregada |
| IDA1 a IDA5, demais campos | categóricos, como estão |
| respostas com CON1 diferente de "concordo" | fora dos denominadores (E14); parciais órfãs, descartadas |

## 8. Retenção (para a E30)

Por evento — a instituição fixa os anos pela tabela de temporalidade (seção 6):

| Dado | Guardado enquanto | Depois |
|---|---|---|
| base central: contato e dados acadêmicos | a pessoa fizer parte do acompanhamento — constar das extrações da instituição | eliminado; **exceto** a marca de recusa de contato, que fica, mínima, enquanto vigorar |
| respostas identificadas do ciclo | até a extração anonimizada do ciclo (E28) | eliminadas, preservado antes o registro de consentimento de cada uma |
| registro de consentimento (CON1, CON2, `CONV`, `CONDH`) e `egressos_recusas` | for preciso comprovar que a manifestação foi respeitada (LGPD, art. 8º, §2º) | eliminado no prazo da instituição |
| e-mail do formulário "Retomar mais tarde" | a resposta salva existir | a plataforma o apaga na conclusão; para quem não conclui, sai com a resposta, ao fim do ciclo. **Nunca é exportado** — decisão do orientando de mantê-lo |
| trilhas (seção 3.4) | o prazo de auditoria da instituição | eliminadas; contêm dado pessoal na criação de participantes |
| arquivo de entrada | a importação | eliminado na hora (E17) |

**A eliminação não é rotina nesta etapa.** A política está escrita para que a
implantação real a configure com os anos da instituição. Fica com a E30.

## 9. Revisão humana do e-mail compartilhado (vinda da E19)

A conferência de participantes lista, pelos identificadores e sem nome nem endereço,
as pessoas que compartilham o e-mail principal. O mecanismo **não as funde**.

**Quem revisa:** a equipe do programa de acompanhamento, que tem acesso ao cadastro
acadêmico. **O que faz:** confere no sistema de origem se são duas pessoas — irmãos,
um e-mail de família, o que o leiaute aceita com alerta — ou uma pessoa duplicada.
**Onde se corrige:** pessoa duplicada se corrige **na origem**, e chega corrigida na
extração seguinte; o identificador estável faz a importação reencontrar a pessoa
certa (ADR-0005). Corrigir no mecanismo e não na origem desfaria a correção na
importação seguinte.

## 10. Verificação do critério de conclusão

*Critério: a recusa de contato interromper novos disparos em todos os ciclos, e a de
consentimento, apenas no ciclo corrente.* **Atendido.**

`python3 confere-conformidade.py --exercitar`, **12 de 12** na primeira execução,
com oito participantes sintéticos e limpeza:

| # | Conferência | Resultado |
|---|---|---|
| 1 | trilha ativa, lista de bloqueio nos padrões, correção na imagem | ok |
| 2 | página de recusa em português | "Confirme que você deseja ser retirado(a)…" |
| 3 | cifragem: no banco, cifrado; exportado, o valor | EQ2 no banco "RULwxc9L…", exportado "PRE" |
| 4 | registro de cada recusa; contato inválido, não | A consentimento/tela, B contato/tela, C contato/conclusão, D contato/mensagem (momento da trilha) |
| 5 | recusa de contato na base central, pela plataforma e com trilha | B, C, D bloqueados; A e E livres |
| 6 | **ciclo seguinte** | B, C, D: "No candidate tokens"; A e E convidados |
| 7 | **ciclo corrente** | A recusa de consentimento; B, C, D recusa de contato; E contato inválido |
| 8 | dado sensível sem consentimento | F apagado e registrado; G e H mantidos |
| 9 | idempotência | segunda passada sem efeito |
| 10 | revogação | B livre, revogação registrada e na trilha, sem novo bloqueio |
| 11 | recuperável | `consulta-consentimento.py` mostra recusa, via, momento, versão e revogação |
| 12 | limpeza | estado como antes; a trilha fica, por ser trilha |

**Regressão:** E22 11 de 11, E21 14 de 14 e estrutura 9 de 9, com a trilha ativa e a
tarefa nova rodando; unicidade 8 de 8; mensagens 4 de 4.

## 11. O que esta etapa não permite afirmar

1. **A eliminação por prazo não roda.** A política está escrita; os anos e a rotina são
   da implantação real.
2. **A extração anonimizada não existe ainda.** A seção 7 é a política que a E28
   aplica.
3. **A recusa por conclusão (CT4) foi plantada pela API.** A conclusão das onze
   páginas pelo caminho real é da E26.
4. **A trilha não é inviolável.** Quem administra o banco pode alterá-la; integridade
   contra o administrador exigiria trilha fora da instância, o que este projeto não
   faz.
5. **Nome e e-mail do questionário estão em claro** no ensaio (seção 4).

## 12. O que determina para as etapas seguintes

- **E25** — "tratamento da recusa", "trilha de auditoria" e "cifragem" têm
  procedimento pronto: `confere-conformidade.py --exercitar`, doze conferências,
  inclusive o ciclo seguinte.
- **E26** — a recusa por CT4 pela conclusão real; a revogação pedida por resposta de
  verdade, na caixa `acompanhamento`.
- **E28** — aplicar a política da seção 7; ler as respostas cifradas pela exportação
  da plataforma, que decifra; não confundir `CONV` e `CONDH` com campos.
- **E30** — `conformidade.py aplicar` na sequência de instalação; a correção do
  AuditLog e as traduções como parte da imagem; os anos da tabela de temporalidade no
  termo, com versão nova; a eliminação por prazo; a cifragem de nome e e-mail do
  questionário; a revisão humana da seção 9.
- **E31** — declarar que a trilha registra também dado pessoal, e que não é
  inviolável; e que a revogação é pelo operador, por decisão.
