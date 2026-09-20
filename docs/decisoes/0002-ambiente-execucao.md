# ADR-0002 — Ambiente de execução da instância LimeSurvey

**Status:** proposta (pendente — etapa E06)
**Data:** —

## Contexto
O projeto exige instância própria do LimeSurvey, com custo praticamente nulo e
reprodutível por terceiros. É necessário suportar tarefa agendada (lembretes
automáticos) e envio de e-mail. A decisão foi deliberadamente postergada para a
fase de implantação.

## Alternativas avaliadas
| Alternativa | Prós | Contras |
|-------------|------|---------|
| Docker no Windows via WSL2 | Reprodução simples, ambiente versionável, custo zero | Depende da máquina local ligada para agendamento |
| VM local (VirtualBox) | Isolamento completo, próximo de servidor real | Mais pesado, reprodução mais trabalhosa |
| Nuvem em camada gratuita | Disponibilidade contínua, agendamento confiável | Limites da camada gratuita, risco de descontinuidade |

## Decisão
A preencher na etapa E06.

## Justificativa
A preencher.

## Consequências
A preencher.
