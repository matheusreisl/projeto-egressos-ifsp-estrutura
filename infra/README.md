# Infraestrutura

Artefatos de provisionamento da instância LimeSurvey.

O ambiente foi decidido na etapa E06 e está registrado em
[`ADR-0002`](../docs/decisoes/0002-ambiente-execucao.md): **conteinerização
declarativa em máquina local** — Docker Engine e Docker Compose, com a composição
inteira (LimeSurvey, banco de dados, serviço de correio e rotina agendada)
declarada em arquivo, em rede fechada, sem rota de saída para a internet.

Nesta máquina, o hospedeiro do Docker Engine é uma distribuição Linux sobre WSL2.
O WSL2 é substrato local e não faz parte da decisão: a mesma composição sobe em
Linux nativo, em macOS ou em servidor institucional.

Regras que valem para tudo o que entrar aqui:

- O ambiente deve subir do zero usando **apenas o que está versionado** nesta pasta.
- Credenciais nunca entram. Use `.env` local, já ignorado pelo Git; versione apenas
  o `.env.exemplo`, sem valores reais.
- Imagens de contêiner fixadas por digest, e não por rótulo móvel — sem isso o
  ambiente não é reproduzível duas vezes.
- Nenhuma configuração relevante pode existir apenas dentro do contêiner.

Os artefatos são criados na etapa E07.
