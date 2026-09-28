# ADR-0005 — Uma linha por egresso no arquivo de participantes

**Status:** aceita
**Data:** 28/09/2026
**Etapa de origem:** E11 — especificar o leiaute do arquivo de entrada

## Contexto

O leiaute proposto no documento do projeto não define o que cada linha do arquivo
de participantes representa. A questão aparece com quem concluiu mais de um curso
na instituição — técnico e, depois, graduação, por exemplo: são duas conclusões,
e a pessoa pertence a duas turmas.

A escolha decide o identificador, a deduplicação e o limite de contato. E há duas
referências que puxam para lados opostos:

- os parâmetros de contato da E05 foram escritos **por participante**: a P4 limita
  a quatro mensagens por participante e por ciclo, para conter incômodo ao
  destinatário; a P5 proíbe mais de um convite a cada doze meses e ciclo aberto
  sobreposto para o mesmo participante;
- o Regulamento do Programa acompanha **por turma**, a partir do término do
  semestre de conclusão (art. 19).

## Alternativas avaliadas

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Uma linha por egresso, com a conclusão mais recente** | um convite por ano por pessoa, e a P4 e a P5 cumpridas por construção; uma chave só para deduplicar; nenhum dado a mais | o acompanhamento segue a turma mais nova e deixa a anterior; exige identificador estável por pessoa |
| Uma linha por curso concluído | segue a turma do art. 19 ao pé da letra; corresponde à granularidade natural do registro acadêmico | quem tem dois cursos recebe dois convites por ano, contra a P4 e a P5; juntar as linhas da mesma pessoa exige uma segunda chave, de pessoa, ou heurística sobre nome e endereço, que erra nos dois sentidos |
| Uma linha por egresso, com todas as conclusões em colunas repetidas | preserva o histórico de formações | leiaute de largura variável; mais dado por registro sem consumidor que o exija; o pré-preenchimento não saberia qual conclusão exibir |

## Decisão

O arquivo de entrada tem **uma linha por egresso**. Quem concluiu mais de um curso
aparece uma vez, com a **conclusão mais recente** pelo par (ano, semestre); em
empate, a de nível mais alto.

## Justificativa

O mecanismo existe para cobrar resposta de pessoas, e os limites que protegem o
destinatário só se cumprem por construção se a unidade da base for a pessoa. Com
uma linha por curso, o limite da P4 e o intervalo da P5 passariam a depender de
uma reconciliação entre linhas, feita por uma chave que o leiaute não tem e que
não deve ter, porque na prática seria um documento civil.

Para os indicadores do Anexo I do Regulamento, o efeito é coerente. Enquanto cursa
a graduação, o egresso técnico continua técnico na base e responde como técnico
que prosseguiu os estudos: entra no numerador do Ind9, e também no do Ind5 se
prosseguir no IFSP. Ao concluir a graduação, passa a egresso de graduação na
extração seguinte.

Decisão confirmada com o orientando antes da execução da E11. A especificação
completa está em
[`leiaute-entrada.md`](../especificacao/leiaute-entrada.md), seção 2.

## Consequências

**Passa a ser verdade:**

- O `identificador` identifica a pessoa e precisa ser **estável entre extrações**
  (seção 4.1 do leiaute): é a chave com que a base central reencontra quem recusou
  contato no ciclo anterior.
- A âncora do ciclo da P5 **muda** quando uma conclusão nova chega em extração
  posterior. A regra de não sobreposição continua valendo: o ciclo aberto termina
  na sua janela, e o seguinte já parte da âncora nova. É requisito da E21.
- A base sintética da E16 é gerada com uma linha por pessoa.
- A deduplicação da E17 e da E19 opera sobre a pessoa: identificador repetido no
  arquivo rejeita todos os registros que o compartilham.

**Esta decisão impede:**

- O acompanhamento **simultâneo** de duas formações da mesma pessoa. A turma
  anterior perde o egresso quando ele conclui o curso seguinte, e a aderência à
  letra do art. 19 é, por isso, parcial. Deve ser enunciado assim no relatório
  final (E31), junto com as demais limitações.

## Revisão

Revisável se a instituição precisar acompanhar cada formação separadamente — por
exemplo, para avaliar um curso técnico cujos egressos em boa parte se graduaram
depois. Nesse caso, a unidade passa a ser a conclusão, e os limites de contato
precisam ser redefinidos por pessoa, o que exige uma chave de pessoa além da chave
de conclusão.
