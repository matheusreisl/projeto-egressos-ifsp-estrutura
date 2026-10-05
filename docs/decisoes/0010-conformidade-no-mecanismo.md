# ADR-0010 — Conformidade aplicada pela plataforma, com rotina própria e trilha nativa

**Status:** aceita
**Data:** 05/10/2026
**Etapa de origem:** E23 — configurar anonimização e trilha de auditoria

## Contexto

O critério da E23 é que a recusa de contato interrompa os disparos em **todos** os
ciclos, e a de consentimento só no corrente. A E22 deixou o quadro assim: a recusa
pela mensagem já chegava à base central, porque a plataforma a leva; a feita na tela
e por CT4 valia só no questionário do ciclo; nenhuma recusa tinha data, via e versão
registradas; e a trilha de auditoria da plataforma estava desligada, com a ativação
só pela tela (E08).

Três perguntas de desenho, cada uma com mais de uma resposta possível:

1. **Por onde a recusa da tela chega à base central?**
2. **Onde fica a trilha de auditoria** — e a data da recusa pela mensagem, que a
   plataforma não guarda?
3. **Quem revoga, e como?**

## Alternativas avaliadas

**Quanto à recusa na base central:**

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Rotina que aplica a recusa global pela via da própria plataforma** (a página de confirmação da mensagem, confirmada por POST) | um caminho só para a recusa de contato; os modelos da plataforma gravam; a trilha registra; nada de gravação direta | depende da página pública de recusa, e a rotina age pelo egresso |
| Gravação direta em `lime_participants` | simples | contorna a plataforma e a trilha; um segundo caminho para a mesma recusa |
| Comando de console | modelos da plataforma | o contêiner `rotinas` não alcança o console, de propósito; ficaria só manual |
| Encerramento por cota na tela (E15) | a plataforma marcaria o estado | não leva à base central; só muda a marca de concluído |

**Quanto à trilha:**

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **`AuditLog` nativo, ativado por comando de console, mais tabelas próprias para o que é do projeto** | registra o que a plataforma muda — inclusive a recusa pela mensagem, com data —, sem código novo de captura; o comando preserva o K7 | o plugin tinha defeito que quebrava gravação por console; guarda dado pessoal na criação de participantes |
| Só tabelas próprias | esquema sob controle | não veria o que a plataforma muda sozinha; a recusa pela mensagem ficaria sem data |
| Ativar pela tela e declarar exceção ao K7 | sem código | o guia deixaria de ser de comandos, e a exceção ficaria num requisito de conformidade |

**Quanto à revogação:**

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Pelo operador, a pedido do egresso por resposta à mensagem** | só quem é o egresso pede; canal humano que já existe | depende de alguém atender a caixa |
| Pelo próprio egresso, por link (`allowunblacklist = Y`) | o mais simples para o egresso | qualquer pessoa com o endereço individual — transportável por desenho — desfaria a recusa |

## Decisão

1. **Uma rotina de conformidade**, tarefa do agendador a cada 30 minutos e sempre de
   verdade, registra cada recusa em `egressos_recusas`, leva a de contato à base
   central **pela via da plataforma** e apaga dado sensível guardado sem
   consentimento.
2. **A trilha é o `AuditLog` nativo**, ativado pelo comando de console
   `ativarauditoria`, com **correção do defeito** que o fazia quebrar sem usuário
   logado, aplicada na construção da imagem. As tabelas próprias guardam o que é do
   projeto.
3. **A revogação é do operador**, por comando que usa os modelos da plataforma e
   registra o pedido. `allowunblacklist` fica desligado. Decisão do orientando.
4. **Cifragem em repouso** dos sete campos de maior risco, e **anonimização na
   extração**, e não na resposta. Decisões do orientando quanto ao alcance.

## Justificativa

A recusa precisa de um caminho só. Se a rotina gravasse direto na base central, haveria
dois — o da plataforma, quando o egresso clica, e o da rotina —, com efeitos que
podem divergir, como divergiam o `blacklisted` do participante e o `OptOut`, que a
E08 mostrou não serem a mesma coisa. Agindo pela página de recusa, a rotina faz
exatamente o que o egresso teria feito, e a trilha registra igual.

A trilha nativa vê o que a plataforma muda sem que o projeto precise capturar. E é a
única fonte da data da recusa pela mensagem: a plataforma marca o bloqueio e não diz
quando. O defeito do plugin era real — e sem a correção, ativar a trilha teria
quebrado a importação da E17 em silêncio, na próxima vez que alguém a rodasse.

## Consequências

**Passa a ser verdade:**

- recusa de contato por qualquer via chega à base central em até 30 minutos, e o
  ciclo seguinte não convida a pessoa — conferido com um questionário novo;
- cada recusa tem registro com via, momento e a fonte do momento, versão do termo,
  chegada à base central e revogação;
- a imagem do LimeSurvey passa a `7.2.0-1`: as traduções da página de recusa e a
  correção do `AuditLog` fazem parte dela, e a construção para se a correção não
  aplicar;
- uma instalação do zero precisa de `conformidade.py aplicar` na sequência;
- a trilha guarda dado pessoal na criação de participantes e precisa de política de
  guarda própria;
- o apagamento de dado sensível em resposta interrompida é por gravação direta, porque
  a API recusa alterar resposta neste instrumento.

**Esta decisão impede:**

- revogação sem intervenção humana. Se a instituição a quiser, liga
  `allowunblacklist` e aceita o risco descrito acima.

## Revisão

Revisável se a plataforma passar a levar à base central a recusa feita no próprio
questionário, ou se a instituição adotar trilha fora da instância — que traria
integridade contra o administrador, que esta não tem.
