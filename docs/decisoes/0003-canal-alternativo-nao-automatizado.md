# ADR-0003 — Canal alternativo de convite sem automação

**Status:** aceita
**Data:** 20/09/2026
**Etapa de origem:** E05 — parâmetros de contato

## Contexto

O art. 16, §1º da Portaria Normativa nº 128/2025 (Regulamento do Programa de
Acompanhamento de Egressos do IFSP) determina convite por e-mail e, "não sendo
possível", por aplicativos de mensagens instantâneas. É requisito normativo
expresso, não recomendação.

A E04 identificou, além disso, que o contato por canal alternativo é prática
documentada — o Ifes recorreu a telefone "quando o telefone estava disponível" —
e a distinguiu da busca ativa *reparadora*, que corrige o cadastro em vez de
entregar o convite por outra via. As duas exigem coisas diferentes do mecanismo, e
esta decisão trata apenas da segunda.

O projeto opera sob restrição de custo zero e não instala dependências pagas.

## Alternativas avaliadas

| Alternativa | Prós | Contras |
|-------------|------|---------|
| Interface oficial de mensagens instantâneas | Conformidade integral ao art. 16, §1º; disparo automatizado ponta a ponta | Contratação paga na prática corrente; colide com a restrição de custo zero e com a replicabilidade por instituição sem orçamento |
| Automação não oficial da plataforma de mensagens | Custo zero aparente | Contrária aos termos de uso; frágil a mudanças do fornecedor; reintroduz no projeto a fragilidade técnica que motivou o descarte da raspagem de dados |
| SMS por provedor de camada gratuita | Automatizável | Camadas gratuitas instáveis e limitadas; SMS não é o canal que a norma nomeia; acrescenta dado pessoal (telefone) ao tratamento automatizado |
| **Não automatizar; garantir que o endereço individual seja transportável** | Custo zero; sem dependência de fornecedor; preserva a rastreabilidade; replicável | Conformidade apenas parcial ao art. 16, §1º; o envio passa a depender de ação humana |

## Decisão

O envio de convite por aplicativos de mensagens instantâneas **fica fora do
disparo automatizado deste projeto**. Em seu lugar, o mecanismo garante que o
endereço individual de acesso seja **extraível da base de participantes e
transportável para fora do e-mail**, mantendo a individualidade do acesso e,
portanto, a rastreabilidade.

## Justificativa

A alternativa escolhida é a única que preserva simultaneamente as três restrições
que o projeto não pode relaxar: custo zero, replicabilidade por instituição sem
orçamento e rastreabilidade do participante.

As duas primeiras alternativas foram descartadas pelos mesmos motivos que já
haviam eliminado a integração com SUAP e a raspagem de perfis — dependência não
controlável e fragilidade técnica com risco de termos de uso. Manter coerência com
esses descartes importa: seria incongruente recusar a raspagem por fragilidade e
adotar automação não oficial de mensageria pela mesma via.

O ponto que sustenta a decisão é que **a parte tecnicamente difícil do art. 16,
§1º não é o envio, é a individualidade do endereço**. Uma instituição que já tenha
a base de participantes e os endereços individuais pode entregá-los por qualquer
via, inclusive manualmente. Uma instituição que não os tenha não resolve nada
integrando um mensageiro, porque continuará sem saber a quem cobrar. O projeto
entrega a condição que falta; o transporte é operação, não arquitetura.

## Consequências

**Passa a ser verdade:**

- A conformidade deste mecanismo ao art. 16, §1º é **parcial e declarada**. Deve
  ser assim enunciada no relatório final (E31), sem arredondamento.
- A base de participantes precisa permitir extração do endereço individual por
  participante — capacidade C1 de
  [`parametros-contato.md`](../especificacao/parametros-contato.md), seção 13.
- A operação do canal alternativo vira recomendação de implantação, com
  responsável institucional definido (E24), e entra no guia de replicação (E30).

**Esta decisão impede:**

- Que o projeto declare conformidade integral ao Capítulo VI do Regulamento.
- Que a matriz de verificação (E25) inclua requisito de envio por mensagem
  instantânea — não há o que verificar, porque não há automação a exercitar.

**Advertência que acompanha a recomendação (E30).** Entregar por mensagem
instantânea o **endereço individual de cada egresso** é compatível com o
mecanismo. Difundir um **endereço comum** em grupo de turma devolve o instrumento
ao modo aberto e anula o denominador. A distinção precisa estar escrita, porque é
o tipo de detalhe que uma instituição desfaz sem perceber.

## Revisão

Decisão revisável se houver interface oficial gratuita, ou se a instituição
replicante já dispuser de contratação própria. Nesse caso, o que muda é o
transporte; nada do que esta especificação fixa sobre individualidade do endereço
precisa ser refeito.
