# Mecanismo Digital de Acompanhamento de Egressos

Projeto de ensino do curso de Tecnologia em Análise e Desenvolvimento de Sistemas
do Instituto Federal de São Paulo (IFSP), executado entre agosto e dezembro de 2026.

## O que é

Prova de conceito de um mecanismo de acompanhamento de egressos construído sobre
instância própria da plataforma livre LimeSurvey, com três características que a
literatura da área aponta como determinantes para a qualidade dos dados coletados:

- **rastreabilidade de participantes**, permitindo identificar quem ainda não respondeu;
- **automação de convites e lembretes**, substituindo a espera passiva por cobrança sistemática;
- **conformidade com a LGPD**, com consentimento eletrônico, anonimização e trilha de auditoria.

O objetivo é produzir um artefato documentado e replicável por instituições de
ensino que enfrentem restrições orçamentárias e operacionais semelhantes.

## Delimitação

Este projeto **não realiza coleta de dados junto a seres humanos**. Toda a
validação ocorre por simulação controlada sobre base de participantes
integralmente sintética. Não há contato com egressos reais em nenhuma etapa.

Qualquer aplicação futura do mecanismo a uma população real deverá ser precedida
de apreciação pelo Comitê de Ética em Pesquisa.

## Organização

- `ETAPAS.md` — sequenciamento das etapas e registro de progresso
- `docs/` — pesquisa, decisões e especificações
- `infra/`, `scripts/`, `dados/`, `entregas/` — artefatos técnicos e produtos

## Licença

MIT — ver [LICENSE](LICENSE). A escolha por licença permissiva é deliberada: o
objetivo declarado do projeto é ser replicado por outras instituições de ensino.
