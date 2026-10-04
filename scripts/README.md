# Scripts

Rotinas do projeto, em Python.

**Onde rodam.** Dentro do contêiner `rotinas` da composição, que fica **somente
na rede interna** — é de lá que se alcança a caixa de devoluções do correio, que
o hospedeiro não alcança. Esta pasta é montada nele em modo somente leitura, de
modo que os scripts se editam e versionam aqui, sem reconstruir imagem, e não
existe uma segunda cópia que possa divergir.

```bash
cd infra
docker compose exec rotinas python3 <script> [argumentos]
```

**Exceções, que rodam no hospedeiro**, da raiz do repositório: os que gravam ou
leem `dados/`, que o contêiner não monta, e os que chamam o console da plataforma
(`docker compose exec`), que o contêiner não alcança — de propósito, ele não tem
acesso ao Docker. Estão marcados na tabela.

## Existentes

| Script | Papel | Onde roda | Etapa |
|---|---|---|---|
| `limesurvey_api.py` | cliente da API RemoteControl, compartilhado pelas rotinas | — | E09 |
| `ler_devolucoes.py` | lê a caixa de devoluções, classifica e aplica a regra do P8 | contêiner | E09 |
| `verifica_correio.py` | verifica o correio nas duas direções, por SMTP direto | contêiner | E09 |
| `gerar_base_sintetica.py` | gera a base sintética de egressos no leiaute da E11 | hospedeiro | E16 |
| `valida_entrada.py` | valida o arquivo de entrada contra o leiaute, sem importar | hospedeiro | E17 |
| `importar_base.py` | valida, grava na base central e no questionário, registra e elimina o arquivo | hospedeiro | E17 |
| `limesurvey_console.py` | roda os comandos de console próprios no contêiner do LimeSurvey | — | E17 |

A importação está especificada em
[`docs/especificacao/importacao-base.md`](../docs/especificacao/importacao-base.md),
e a decisão de manter base persistente, na
[ADR-0007](../docs/decisoes/0007-base-persistente-de-participantes.md).

A especificação do que `ler_devolucoes.py` implementa está em
[`docs/especificacao/leitura-devolucoes.md`](../docs/especificacao/leitura-devolucoes.md).

### A base sintética

**Exceção à regra de onde rodar:** `gerar_base_sintetica.py` roda no
**hospedeiro**, e não no contêiner, porque grava em `dados/sinteticos/`, que o
contêiner não monta. Da raiz do repositório:

```bash
python3 scripts/gerar_base_sintetica.py
```

Gera 500 egressos, concluintes de 2016 a 2025, no leiaute de
[`leiaute-entrada.md`](../docs/especificacao/leiaute-entrada.md), e imprime um
resumo por ano, nível, domínio e alerta, com o SHA-256 do arquivo, sem nome,
endereço nem telefone. O arquivo não é versionado; o que se versiona é o script.

- **Determinístico.** A mesma semente (`--semente`, padrão 2016) produz o mesmo
  arquivo, byte a byte. É o que mantém o identificador estável entre gerações.
- **Nada de pessoa real.** Nomes inventados, por sílabas, com recusa de
  prenomes e sobrenomes frequentes — o que torna improvável, e não impossível, a
  coincidência de um nome inteiro com o de alguém. Endereços só sob `.test`.
  Telefones `+55` com código de área terminado em 0, que não existe — reconferido
  na fonte oficial da Anatel na E16. Identificadores `SIN-000001` em diante, sem
  forma de CPF.
- **Composição de ensaio, e não estimativa de população.** Cerca de 50% técnico,
  40% graduação e 10% pós; e-mail principal nos três domínios do correio de
  ensaio — `egressos.test` (entrega), `invalido.test` (erro permanente) e
  `indisponivel.test` (erro temporário) —, para exercitar o P8; parte com
  `email_alternativo`, inclusive principais inválidos com alternativo entregável,
  que é o reparo automatizável; parte com telefone; parte sem via alternativa; e
  três pares com o mesmo e-mail principal, o sintoma de pessoa duplicada que a
  E19 verifica. Cursos e unidades vêm de
  [`infra/instrumento/configuracao/`](../infra/instrumento/configuracao/), e a
  lista de cursos é ilustrativa.

## Previstos

- rotina agendada de convites e lembretes (E21)
- extração de resultados via API do LimeSurvey (E28)

## Regras

- **Nenhum script pode processar dados pessoais reais.** A validação é feita
  exclusivamente sobre base sintética.
- **Nenhum endereço fora de domínio controlado pelo projeto.** Os domínios de
  ensaio estão sob o TLD reservado `.test`.
- **Nenhuma credencial no código.** Tudo por variável de ambiente, definida no
  `.env` da composição, que não é versionado.
- **Dependência só quando a biblioteca padrão não resolve.** Hoje há uma:
  `PyMySQL`, para a tabela própria de registro de devoluções.
