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

## Existentes

| Script | Papel | Etapa |
|---|---|---|
| `limesurvey_api.py` | cliente da API RemoteControl, compartilhado pelas rotinas | E09 |
| `ler_devolucoes.py` | lê a caixa de devoluções, classifica e aplica a regra do P8 | E09 |
| `verifica_correio.py` | verifica o correio nas duas direções, por SMTP direto | E09 |

A especificação do que `ler_devolucoes.py` implementa está em
[`docs/especificacao/leitura-devolucoes.md`](../docs/especificacao/leitura-devolucoes.md).

## Previstos

- `gerar_base_sintetica.py` — geração da base de validação (E16)
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
