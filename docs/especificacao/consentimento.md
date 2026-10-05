# Consentimento eletrônico

**Etapa:** E22 — implementar o consentimento eletrônico
**Data:** 05/10/2026
**Implementa:** a seção 3.1 de [`blocos-instrumento.md`](blocos-instrumento.md) (três
manifestações), as duas recusas do P6 de [`parametros-contato.md`](parametros-contato.md)
e os arts. 8º, 9º, 11, I e 18 da LGPD, conforme o
[fichamento](../pesquisa/fichamentos/brasil-lei-13709-2018.md)
**Decisão:** [ADR-0009](../decisoes/0009-registro-do-consentimento.md)
**Onde está:** [`infra/instrumento/termo.py`](../../infra/instrumento/termo.py) ·
[`infra/instrumento/termos/`](../../infra/instrumento/termos/) ·
[`infra/consulta-consentimento.py`](../../infra/consulta-consentimento.py) ·
[`infra/confere-consentimento.py`](../../infra/confere-consentimento.py)

## 1. O que esta etapa entrega

| Item | Valor |
|---|---|
| Tela | página 1 do 202615: o termo, CON1 com as três opções, CON2 com o consentimento específico do dado sensível |
| Termo | modelo de ensaio com os elementos do art. 9º, versão `ensaio-1`, **sujeito à validação do encarregado de dados do IFSP** antes de qualquer uso real |
| Registro | em cada resposta: CON1, CON2, a versão do termo com o resumo SHA-256 do texto (`CONV`) e o momento da manifestação (`CONDH`) |
| Texto de cada versão | arquivado, imutável, em `infra/instrumento/termos/<versão>.html` |
| Recuperação | `consulta-consentimento.py --identificador`, pela exportação da própria plataforma, conferindo o texto pelo resumo |
| Encerramento | três ramos, pelo CON1: concluiu, recusou o termo, recusou contato |
| Recusa pela mensagem | exercitada: confirmar bloqueia convite e lembrete, neste e em outro questionário |

## 2. A tela

### 2.1 O termo

Redigido nesta etapa como **modelo de ensaio** — decisão do orientando —, com o que o
mecanismo de fato faz, tirado das especificações. Não é conteúdo temático de
pergunta, que continua sendo do projeto correlato (CLAUDE.md, decisão 5).

| Elemento do art. 9º | No termo | De onde vem |
|---|---|---|
| I — finalidade específica | "Para que serve": indicadores do programa e avaliação e planejamento dos cursos, conforme o Regulamento; nenhuma outra | Portaria Normativa nº 128/2025; [`blocos-instrumento.md`](blocos-instrumento.md) |
| II — forma e duração | "Como e por quanto tempo": instalação própria, acesso restrito, divulgação só agregada | ADR-0002; ADR-0007 |
| II — duração | **marcador**: prazo da política de retenção | é da E23 |
| III e IV — controlador e contato | IFSP; encarregado como **marcador** | a preencher pela instituição |
| V — uso compartilhado | não compartilhado com terceiros | ADR-0002 (instância própria, sem integração externa) |
| VI — responsabilidades dos agentes | **parcial**: "acesso restrito à equipe do programa" | a detalhar pela instituição |
| VII — direitos do art. 18 | "Seus direitos", com a correção já possível no próprio questionário | LGPD, art. 18 |
| art. 18, VIII — consequências da negativa | "Se você não concordar": as duas recusas, com efeitos, e "recusar não traz nenhuma outra consequência" | P6 |

O termo também diz o que **não** se coleta — abertura de mensagem e endereço de rede
(P8, 10.3; `ipaddr` desligado) — e que, nas recusas, fica registrada apenas a
manifestação, com data, hora e versão do termo.

**Base legal.** As respostas se apoiam no consentimento (art. 7º, I). É decisão do
projeto, a via mais protetiva, e não conclusão da lei: o art. 7º, IV seria outro
caminho possível (fichamento da LGPD, limitações). O uso dos dados de contato para
enviar o convite antecede o consentimento e precisa de base própria, que o termo
não afirma — fica com o encarregado.

### 2.2 As três manifestações

| Campo | Opções | Efeito |
|---|---|---|
| CON1 | concordo · não concordo com o termo neste ciclo · não quero mais ser contatado | as duas recusas encerram o preenchimento na página 1 (E14) |
| CON2 | concordo · não concordo | só aparece com CON1 = concordo; negar dispensa só o bloco de recortes de equidade |

O consentimento do dado sensível tem **texto próprio**, no enunciado de CON2, e não
cláusula do termo geral: o art. 11, I exige consentimento "de forma específica e
destacada".

### 2.3 O encerramento

Uma expressão do Expression Manager escolhe o texto pelo CON1: agradecimento e novo
convite no ano seguinte, para quem concluiu; "nenhuma resposta foi coletada" e novo
convite no ano seguinte, para quem recusou o termo; "não receberá mais mensagens,
neste nem nos próximos anos", para quem recusou contato. Conferido pelo caminho
real, ramo a ramo.

## 3. O registro: data, hora e versão

A E13 havia fixado que data, hora e versão do termo são **metadados registrados pela
plataforma, e não campos**. Implementados como duas **equações ocultas** da página
1:

| Metadado | Expressão | Grava |
|---|---|---|
| `CONV` | texto literal, sem chaves | `ensaio-1 sha256:fb39012d…` — versão e resumo do documento da página 1 |
| `CONDH` | `{if(is_empty(CON1), '', date('c'))}` | `2026-10-05T14:06:21+00:00` — o momento da manifestação |

Por que funciona, conferido no código do LimeSurvey 7.2:

- **a equação é recalculada no servidor** ao receber a página — "process relevant
  equations, even if hidden, and write the result to the database"
  (`em_manager_helper.php`) —, com ou sem JavaScript no navegador, e com os valores
  que acabaram de chegar;
- **no modo de uma página por vez, avançar e concluir validam só a página corrente**
  (`NavigateForwards`, `_ValidateGroup`): o momento gravado no envio da página 1 não é
  reescrito pelas seguintes. Conferido também pelo caminho real, até a página 2. Se o
  respondente voltar à página 1 e reenviá-la, o momento passa a ser o da última
  manifestação;
- **sempre relevantes**, as duas não são descartadas quando a recusa descarta o resto
  do preenchimento (E14, E15) — e é na recusa que mais importam.

**UTC.** A plataforma roda em UTC: o LimeSurvey fixa o fuso do PHP em UTC na própria
configuração (`application/config/internal.php`), qualquer que seja o
`date.timezone` da imagem. Por isso `CONDH` sai com `+00:00` — explícito, ao
contrário das datas da resposta, que também estão em UTC mas não o dizem. Foi este
achado que revelou o erro de fuso da E21 (seção 8).

**O que não serviu.** O aviso de política nativo é uma caixa de aceite só, sem
versão e sem as recusas. A data de início da resposta é a da **abertura** do
endereço (E20), e não a do aceite; a da última ação muda a cada página.

## 4. A versão e o texto arquivado

`CONV` grava o resumo SHA-256 do **documento da página 1** — o termo, as opções de
CON1, o texto e as opções de CON2, tudo o que o respondente vê antes de se manifestar.
Ao gerar o instrumento, esse documento é arquivado em
`infra/instrumento/termos/<versão>.html`:

- se o arquivo da versão não existe, é escrito;
- se existe com o mesmo texto, nada muda;
- se existe com **outro** texto, o gerador **recusa**: mudar o termo exige versão
  nova, e o arquivo de uma versão não se reescreve. Conferido: o texto revisado nesta
  etapa, com a versão inalterada, foi recusado.

O `.gitattributes` fixa LF nesses arquivos. Sem isso, um checkout no Windows os
traria com CRLF, e o resumo deixaria de conferir.

## 5. A recuperação

```bash
python3 consulta-consentimento.py --identificador SIN-000001
```

```
Identificador SIN-000001 · questionario 202615 · participante tid 1
  manifestacao 1 (resposta 11, nao enviada (em preenchimento)): CON1 Concordo · CON2 Concordo
    em 2026-10-05T14:06:21+00:00 · termo ensaio-1 · texto conferido em instrumento/termos/ensaio-1.html (sha256 fb39012d78bc...)
  recusa de contato pelo endereco da mensagem: nao (participante: nao; base central: sem bloqueio)
```

Lê a resposta pela **exportação da própria plataforma** (`export_responses_by_token`),
e não pelo esquema interno, cujos nomes de coluna mudam a cada reimplantação (seção
7). Para cada manifestação: o que foi escolhido, quando, sob que versão e se o texto
arquivado daquela versão produz o resumo gravado. Mostra também a recusa pelo
endereço da mensagem, no participante e na base central. Não imprime nome, endereço
nem token.

## 6. As recusas

### 6.1 Na tela

As duas recusas enviam a página 1 e encerram o questionário. Fica uma resposta
encerrada com CON1, `CONV` e `CONDH`, e o participante marcado como concluído (E15).
O encerramento mostra o ramo de cada uma. A rotina da E21 lê `RCONS` como recusa de
consentimento e `RCONT` como recusa de contato, e não dispara a nenhuma das duas.

**O que a recusa de contato na tela ainda não faz:** marcar a base central. Ela vale
dentro deste questionário, e o termo e o encerramento prometem "neste nem nos
próximos anos". Cumprir a promessa nos ciclos seguintes é o critério da **E23**, e
precisa estar feito antes de qualquer uso real.

### 6.2 Pela mensagem

O convite e o lembrete levam `{GLOBALOPTOUTURL}` (E20). Exercitado nesta etapa:

| Passo | Resultado |
|---|---|
| abrir o endereço (GET) | página de confirmação; nada é gravado |
| confirmar (POST, com o token de proteção do formulário) | `emailstatus = OptOut` no participante e `blacklisted = Y` na base central |
| convite pela API | recusado pela plataforma: "No candidate tokens" |
| lembrete pela API, com convite simulado | recusado |
| convite em **outro** questionário, com a mesma pessoa ligada pela base central | recusado — o filtro nativo exclui quem está na lista de bloqueio |
| plano da rotina (E21) | recusa de contato |

**A configuração global que isso exige:** nenhuma além dos padrões. O convite e o
lembrete nativos excluem quem está bloqueado na base central em qualquer
questionário, sem depender de configuração. Os padrões da lista de bloqueio, e o que
cada um significa para o mecanismo:

| Configuração | Padrão | Para o mecanismo |
|---|---|---|
| `deleteblacklisted` | N | **manter N.** Com Y, a pessoa bloqueada seria apagada da base central — e com ela a memória de que pediu para sair (ADR-0007) |
| `blockaddingtosurveys` | Y | manter: impede incluir bloqueado em questionário novo pela base central. A importação da E17 já não o inclui |
| `blacklistallsurveys` | N | dispensável: o filtro do envio já lê a base central |
| `blacklistnewsurveys` | N | dispensável, pelo mesmo motivo |
| `allowunblacklist` | N | é a **revogação pelo próprio egresso**: decisão da E23 |

**Achado:** a frase da página de confirmação aparece **em inglês** ("Please confirm
that you want to be removed from the central participant list for this site.") — a
tradução pt-BR da plataforma não a tem, embora o botão esteja traduzido. É a página
que o egresso vê ao recusar. Fica para a E23 e a E30.

## 7. A reimplantação do 202615

A plataforma **recusa mudar a estrutura de questionário ativo** — acrescentar
questão ou grupo devolve "Survey is active and not editable". Os metadados eram
questões novas, e o 202615 estava ativo, com 500 participantes, nenhuma resposta e
nada enviado. Com autorização do orientando, foi recriado:

1. a base sintética regenerada com a mesma semente, porque a importação elimina o
   arquivo;
2. `implantar --substituir`, que passou a aceitar instrumento **ativo** só quando não
   há resposta — completa, incompleta ou salva — nem participante com envio ou
   conclusão;
3. `preparar-participantes`, importação e `ativar`.

Resultado: 500 pessoas reencontradas na base central, nenhuma criada; 500
participantes com tokens novos; e as conferências anteriores intactas: estrutura 8 de
8 — a oitava, dos metadados, falhou antes e passou depois —, unicidade 8 de 8,
mensagens 4 de 4, rotina 7 de 7 e 14 de 14.

**Os qids mudaram**, e com eles os nomes das colunas de resposta. A conferência da
E21, que tinha `Q676` escrito, quebrou na primeira execução depois disso; passou a ler
o nome pela instância. E `add_response` descarta em silêncio a chave que não é coluna.

## 8. Correção na E21: `validuntil` em UTC

A E21 gravava a janela de 60 dias em hora local, supondo que a plataforma a lesse no
fuso do PHP da imagem — o que `php -r` mostra, mas o LimeSurvey não usa (seção 3).
**Conferido por comportamento:** com `validuntil` 30 minutos no passado em UTC — 2h30
no futuro se lido como hora local —, a plataforma recusou o convite por acesso
vencido. A janela acabaria 3 horas antes do previsto, e a rotina julgaria `expirado`
com 3 horas de diferença da plataforma.

Corrigidos: `cadencia.py` e `disparar.py`, que leem e gravam a janela em UTC; a
conferência, com um caso que distingue as duas leituras e a janela esperada
calculada à parte; o teste de mutação, com as duas mutações de fuso — 18 de 18
reprovadas, e uma delas reproduz exatamente o código antigo. A verificação real da
E21 foi refeita: 14 de 14, com a janela do reconvidado em UTC. Registro em
[`rotina-disparo.md`](rotina-disparo.md), seção 4.3.

A verificação da E21 não pegou o erro porque a janela esperada era calculada pela
mesma premissa. É o mesmo padrão de furo que a mutação já tinha mostrado lá: a
conferência que reproduz a premissa do código concorda com o próprio erro.

## 9. Verificação do critério de conclusão

*Critério: o aceite persistido e recuperável.* **Atendido.**

`python3 confere-consentimento.py --exercitar`, **11 de 11**, com seis participantes
sintéticos do 202615 pelo caminho real, em HTTP, e limpeza:

| # | Conferência | Resultado |
|---|---|---|
| 1 | termo, consentimento específico, opções e encerramento da instância iguais aos versionados | ok |
| 2 | o documento reconstruído **da instância** tem o resumo de `CONV` e do arquivo da versão | `ensaio-1 sha256:fb39012d…` |
| 3 | aceite com e sem o consentimento específico, com versão e momento | `CONC/CONC` e `CONC/NCONC`, momento dentro da janela do envio |
| 4 | o momento não muda quando a página seguinte é enviada | mantido com a página 2 aceita |
| 5 | recusa do termo neste ciclo: encerrada, com manifestação, versão e momento | e o ramo "No próximo ano, receberá um novo convite" |
| 6 | recusa de contato na tela: idem | e o ramo "não receberá mais mensagens" |
| 7 | **recuperável** por identificador, com o texto conferido pelo resumo | 5 de 5, pela exportação da plataforma |
| 8 | recusa pela mensagem: abrir não registra; confirmar marca participante e base central | ok |
| 9 | o bloqueio impede convite e lembrete, neste e em outro questionário | "No candidate tokens" nos três |
| 10 | a rotina da E21 lê as três recusas no estado certo | ok |
| 11 | limpeza | 500 participantes como antes, nenhuma resposta, nenhum bloqueio, cópia removida |

**As execuções anteriores, que falharam, ficam registradas:**

- a primeira reprovou o momento das quatro manifestações por esperar `-03:00`. O
  valor era `+00:00`, e a conferência estava errada. É o achado da seção 3 e a
  correção da seção 8;
- a segunda reprovou a limpeza da caixa: o relógio do WSL voltou 7,3 s **duas vezes
  em 25 segundos**, e o Dovecot recusou o login. O auxiliar de caixa da E20, que as
  três conferências usam, passou a insistir;
- a primeira reexecução da conferência da E21 quebrou no `Q676` escrito (seção 7) e
  acusou falso alarme ao devolver o agendador, que nem tinha saído do lugar. A
  conferência passou a ler o nome da coluna da instância e a conferir o estado do
  contêiner, e não a esperar log novo. **Essa quebra exibiu a senha do banco local
  no terminal**, porque o erro do subprocesso repete a linha de comando. Os dois
  auxiliares de consulta passaram a acusar só a resposta do banco. A senha é do
  ensaio e nunca saiu da máquina; trocá-la é opcional.

## 10. O que esta etapa não permite afirmar

1. **O termo não é texto validado.** É modelo de ensaio, com marcadores declarados —
   encarregado e prazo de guarda — e um elemento do art. 9º parcial (VI). Não pode ir
   a egresso real sem a validação do encarregado de dados do IFSP.
2. **A recusa de contato na tela não bloqueia os ciclos seguintes** ainda (seção
   6.1). É da E23, e o texto já o promete.
3. **A conclusão das onze páginas não foi percorrida.** O momento estável foi
   conferido até a página 2 pelo caminho real, e para o envio final pela leitura do
   código. A conclusão completa é da E26.
4. **A recusa pela mensagem não tem data nem versão registradas pelo mecanismo.** A
   plataforma marca o participante e a base central, sem data. O registro da recusa,
   com data, hora, ciclo, versão e via, é da E23.
5. **Nada sobre a qualidade do consentimento.** Se o termo é lido e entendido, não se
   sabe sem aplicação real.

## 11. O que determina para as etapas seguintes

- **E23** — fazer CON1 = `RCONT` (e CT4) marcar a base central, como a recusa pela
  mensagem já faz, e cumprir o que o termo promete; registrar a recusa com data,
  hora, ciclo, versão e via, inclusive a da mensagem, que hoje não tem data; decidir
  a revogação — `allowunblacklist` e a via; tratar o e-mail do formulário de
  salvamento, mantido por decisão do orientando; preencher o prazo de guarda no
  termo, o que exige **versão nova**; traduzir a página de confirmação da recusa;
  manter `deleteblacklisted = N`.
- **E25** — "registro do consentimento" tem procedimento pronto:
  `confere-consentimento.py --exercitar` e `consulta-consentimento.py`.
- **E26** — percorrer a conclusão das onze páginas e conferir o momento intacto;
  usar `Formulario` e `Respondente` de `confere-consentimento.py` como ponto de
  partida do preenchimento por HTTP.
- **E28** — `CONV` e `CONDH` são colunas da resposta, a não confundir com campos; e
  toda data da plataforma está em UTC.
- **E30** — o termo precisa ser validado pelo encarregado, com os marcadores
  preenchidos e versão nova; o procedimento de reimplantar instrumento ativo sem
  nada a perder; a configuração da lista de bloqueio; e a página de confirmação em
  inglês.
- **E31** — declarar o consentimento como base legal escolhida pelo projeto, e o
  termo como modelo de ensaio.
