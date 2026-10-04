# ADR-0007 — Base persistente de participantes

**Status:** aceita
**Data:** 04/10/2026
**Etapa de origem:** E17 — importar a base e ativar a tabela de participantes

## Contexto

É na E17 que os egressos passam a existir no mecanismo, e é aqui que se decide se
eles continuam existindo depois do ciclo. Há dois desenhos possíveis, e ambos têm
amparo no mesmo princípio:

- **sem base fixa** — cada ciclo importa o arquivo da instituição, convida,
  cobra e descarta a lista. É a opção do RAEG (Praga de Souza et al., 2025), que
  declara não manter, por padrão, banco de participantes fixo, "pensando na
  segurança dos dados dos participantes" ([fichamento](../pesquisa/fichamentos/praga-de-souza-2025.md));
- **base persistente** — a pessoa permanece no mecanismo entre ciclos, com a sua
  recusa, as suas correções de contato e o seu histórico de convites.

O princípio é o da necessidade (LGPD, art. 6º, III): tratar só o mínimo
necessário à finalidade. O RAEG o lê como "não guardar o que se pode pedir de
novo". Este projeto precisa saber, a cada ciclo, quem não respondeu, quem recusou
e quem tem contato inválido — e três parâmetros da E05 só se cumprem com memória
entre ciclos:

- a **recusa de contato** da P6 é permanente até revogação: sem base persistente,
  quem pediu para não ser mais contatado volta no arquivo do ciclo seguinte e é
  convidado de novo;
- a **correção de contato** da P8, feita por busca ativa, se perde a cada
  extração se o sistema acadêmico continuar com o endereço antigo;
- o **ciclo anual** da P5 se ancora na turma, e a âncora muda quando chega
  conclusão nova (ADR-0005) — o mecanismo precisa saber qual era a anterior.

A E08 acrescentou o dado de plataforma: a recusa só sobrevive ao ciclo na **base
central de participantes** do LimeSurvey; a marcação na tabela do questionário
morre com ela (capacidade C6).

## Alternativas avaliadas

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Base persistente na base central do LimeSurvey** | é onde a plataforma guarda a recusa global e a aplica sozinha (recusa pelo endereço individual, bloqueio de inclusão); cifra nome, sobrenome e e-mail por padrão; a pessoa tem identidade estável (`participant_id`) entre questionários | a API só cobre parte das operações — o resto exige comando de console; mais dado guardado por mais tempo |
| Sem base fixa, como o RAEG | menos dado em repouso; nada a proteger entre ciclos; mais simples | a recusa permanente da P6 não existe; o reparo da P8 se perde a cada extração; não há série por pessoa; o mecanismo vira ferramenta de disparo, e não de acompanhamento |
| Base persistente em tabela própria, fora da base central | esquema sob controle do projeto; toda a lógica num lugar só | duplica a identidade da pessoa: a recusa global da plataforma grava na base central, e a tabela própria teria de ser sincronizada com ela, com duas fontes de verdade para a mesma manifestação; a cifragem teria de ser refeita pelo projeto |

## Decisão

Os egressos são mantidos numa **base persistente**, a **base central de
participantes** do LimeSurvey, uma pessoa por `identificador`, e cada ciclo copia
para o seu questionário só quem não tem recusa permanente.

## Justificativa

A rastreabilidade é o objetivo do projeto, e ela é memória entre ciclos: sem a
pessoa, não há quem não respondeu, quem recusou nem quem teve o contato corrigido.
A opção do RAEG compra segurança ao preço do que os próprios gestores
entrevistados por eles pediram — saber quem não respondeu e cobrar de forma
dirigida — e, neste projeto, ao preço de uma obrigação legal: respeitar a recusa
de quem pediu para não ser mais contatado exige lembrar que ela pediu.

Lida assim, a necessidade não manda descartar a base; manda guardar só o que a
finalidade exige, protegê-lo e eliminar o que já cumpriu o seu papel. É o que a
E17 faz:

- **o mínimo.** A base central guarda os dez campos do leiaute, que a E11
  justificou um a um, e o último valor de contato visto na origem, sem o qual a
  regra de precedência não se aplica. O participante do questionário recebe menos:
  só o identificador e os cinco atributos acadêmicos; via alternativa e telefone
  ficam fora dele;
- **protegido.** Nome, e-mail e todos os atributos de contato ficam **cifrados**
  em repouso, com a chave da plataforma, que não sai do contêiner;
- **eliminado o que cumpriu o papel.** O arquivo de entrada é eliminado depois de
  importado (LGPD, art. 16), e a importação fica na trilha sem reproduzir dado
  pessoal.

O restante do risco é endereçado onde a E05 e a E12 o puseram: o **consentimento**
registrado (E22) e a **anonimização** e a **trilha de auditoria** (E23).

A base central da plataforma, e não uma tabela própria, porque a recusa global
nativa grava nela e a aplica sozinha — e uma segunda base teria de acompanhar a
primeira, com duas fontes de verdade para a mesma manifestação de vontade.

Decisão confirmada com o orientando antes da execução da E17. O procedimento está
em [`importacao-base.md`](../especificacao/importacao-base.md).

## Consequências

**Passa a ser verdade:**

- A pessoa tem `participant_id` **derivado do identificador** (UUID v5, sem
  distinguir maiúsculas): a reimportação reencontra a pessoa em vez de criar
  outra. O identificador precisa ser estável entre extrações (leiaute, seção 4.1).
- A **recusa permanente nunca é tocada pela importação**. Isso exige cuidado
  ativo: a operação de atualização da API grava `blacklisted = 'N'` quando o
  campo não vem no registro, e apagaria a recusa (conferido no código da
  plataforma). A importação grava a base central por comando de console, que lê e
  preserva a recusa.
- A **regra de precedência** de contato se aplica entre extrações: prevalece a
  correção feita pelo mecanismo até a origem mudar.
- Os dados ficam guardados por mais tempo do que num desenho sem base, e a
  política de retenção — por quanto tempo uma pessoa permanece depois de deixar de
  ser convidada — passa a ser necessária. É da E23.
- A cifragem da plataforma é **determinística**: o mesmo valor produz o mesmo
  texto cifrado, o que permite busca exata e revela igualdade entre registros (dois
  egressos com o mesmo e-mail aparecem com o mesmo cifrado). É propriedade da
  plataforma, a declarar na E23.

**Esta decisão impede:**

- Afirmar que o mecanismo trata "só o necessário ao ciclo". Trata o necessário ao
  **acompanhamento**, que é contínuo por definição — e isso precisa estar dito no
  relatório final (E31), em contraste explícito com a opção do RAEG.

## Revisão

Revisável se a instituição decidir não acompanhar por pessoa — por exemplo,
fazendo só levantamentos pontuais, sem cobrança dirigida. Nesse caso, o desenho do
RAEG passa a ser o adequado, e a recusa permanente teria de ser mantida pela
própria instituição, fora do mecanismo.
