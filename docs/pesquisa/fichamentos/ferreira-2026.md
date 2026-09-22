# FERREIRA (2026) — Egressos de Estatística da UFOP pelo LinkedIn

**Referência:** FERREIRA, V. M. S. R. Inserção e trajetória profissional dos
egressos de Estatística da Universidade Federal de Ouro Preto: uma análise a partir
da plataforma LinkedIn. 2026. 41 f. Monografia (Bacharelado em Estatística e
Ciência de Dados) — Instituto de Ciências Exatas e Biológicas, Universidade Federal
de Ouro Preto, Ouro Preto, 2026.
**Tipo:** monografia
**Acesso:** https://monografias.ufop.br/handle/35400000/9120 · consultado em 20/09/2026
**Leitura:** **texto integral**, em 21/09/2026 (E07). A ficha anterior, feita pelo
resumo, foi substituída — ver "Histórico de leitura" ao final.
**Alimenta:** E03, E04, E31 — e confronta a decisão de não fazer raspagem

## Problema identificado

A autora parte de uma crítica direta ao método que este projeto adota: os métodos
tradicionais de coleta, "como questionários on-line", apresentariam com frequência
**baixa taxa de resposta e dificuldade de atualização contínua**. A pergunta do
trabalho é se o LinkedIn é alternativa viável para acompanhar egressos.

## Método

Estudo descritivo sobre os egressos do curso de Estatística da UFOP, em três etapas:

1. **Listagem oficial** dos egressos, fornecida pelo colegiado do curso, contendo
   os nomes completos de todos os formados desde o início do curso, em 2008.
2. **Buscas manuais** no LinkedIn para fazer corresponder nome da lista a perfil
   localizado, produzindo um registro preliminar dos egressos com cadastro ativo.
3. **Raspagem automatizada** por algoritmo em R, com os pacotes `RSelenium`
   (navegação automatizada) e `rvest` (extração de HTML), sobre os perfis assim
   identificados. Foram coletadas apenas as seções "Dados pessoais" e
   "Experiência", por serem as que todo perfil possui — escolha que a autora
   justifica também por evitar lógica de navegação condicional.

O algoritmo não é publicado; a autora informa que pode ser obtido diretamente com
os autores da pesquisa.

### O detalhe do método que a leitura integral revelou

O pseudocódigo reproduzido na monografia mostra que o algoritmo **acessa a página
de autenticação do LinkedIn e submete usuário e senha** antes de percorrer os
perfis. **Não se trata, portanto, de coleta sobre páginas abertas ao público não
autenticado, e sim de raspagem sob sessão autenticada.**

A distinção é decisiva para este projeto e está desenvolvida na seção de
implicações. A ficha anterior, escrita a partir do resumo, dizia "perfis públicos
identificados no LinkedIn" e **estava errada** nesse ponto: a expressão é a que a
própria monografia usa no corpo do texto, mas o método descrito a contradiz.

## Resultado

**Cobertura — os números que o resumo não informava:**

| Medida | Valor |
|---|---|
| Formados desde 2008 (universo) | **127** |
| Perfis identificáveis no LinkedIn | **103** |
| Cobertura | **≈ 81%** |

**Completude entre os 103 perfis localizados:**

| Informação | Preenchida |
|---|---|
| Empresa empregadora | 77% |
| Cargo ou função | 81% |
| Habilidades declaradas | 82,5% |

A autora reporta ainda inserção profissional elevada, dispersão geográfica com
mobilidade interestadual e presença internacional, e correspondência entre as
competências formadas e as exigidas nas ocupações. Conclui pelo potencial do
LinkedIn como ferramenta **complementar** de monitoramento institucional.

## Implicação para o projeto

Esta é a fonte que mais frontalmente confronta o desenho deste trabalho, e por isso
a mais útil para a discussão do relatório final.

**1. O descarte da raspagem sai reforçado, não enfraquecido.** A ficha anterior
registrava que a via da raspagem "é executável e produz resultados", o que obrigaria
o projeto a justificar seu descarte por argumento. A leitura integral muda o peso
do argumento a favor do projeto: **a única via demonstrada na literatura consultada
opera sob sessão autenticada**, e o acesso automatizado autenticado é
contratualmente vedado pelos termos de uso da plataforma. É precisamente o mesmo
motivo pelo qual a [ADR-0003](../../decisoes/0003-canal-alternativo-nao-automatizado.md)
recusou a automação não oficial de mensageria. Recusar uma e aceitar a outra seria
incongruente; recusar as duas pelo mesmo critério é coerente.

**2. Os 81% de cobertura precisam ser lidos com o denominador à vista.** É um
número alto, e um leitor apressado pode opô-lo a este projeto. O universo, porém,
é maximamente favorável à presença no LinkedIn: **127 pessoas**, curso único, de
Estatística e Ciência de Dados, formadas a partir de 2008 — coorte pequena, recente
e de área em que a presença digital é instrumento de trabalho. A própria autora
reconhece que "indivíduos mais inseridos no mercado formal ou em áreas ligadas à
tecnologia tendem a utilizar a rede com maior frequência". Não há base para
transpor esse percentual a um instituto federal multicampi, com cursos técnicos e
de tecnologia e coortes muito maiores.

**3. Fornece a crítica que o projeto precisa responder.** A premissa da autora é
que questionários on-line têm baixa taxa de resposta. O projeto não pode refutar
isso com dados próprios, porque não fará aplicação real. Pode responder no plano do
desenho: baixa taxa de resposta é consequência previsível de coleta sem
rastreabilidade e sem cobrança dirigida — que é exatamente o que o mecanismo
corrige. A comparação da autora se faz contra o questionário mal instrumentado, que
é o estado corrente, e não contra o questionário com capacidade instalada de
cobrança.

**4. Confirma os limites do dado observacional, com números.** A autora qualifica o
LinkedIn como ferramenta *complementar*, e as taxas de completude mostram por quê:
mesmo entre os perfis localizados, de 17,5% a 23% não traziam a informação
pretendida. Some-se o que a fonte reconhece não alcançar — veracidade do declarado,
renda, motivação — e o que ela não tem como alcançar: percepção sobre a formação,
adequação curricular, motivos de saída da área. São justamente os indicadores que a
PAEg do IFSP lista no art. 8º. Vale o argumento já registrado em Alvares et al.:
fonte observacional e instrumento de coleta não são substitutos.

**5. Um achado lateral que interessa à E11.** O ponto de partida da autora foi uma
**listagem oficial fornecida pelo colegiado, apenas com nomes completos** — e foi
essa pobreza de cadastro que a obrigou à busca manual de correspondência antes de
qualquer automação. É a mesma carência que este projeto endereça pelo leiaute de
entrada da E11: cadastro com via de contato utilizável dispensa a etapa de
reidentificação.

## Limitações da fonte

- **Tensão interna entre o que o texto afirma e o que o método faz.** A monografia
  declara, em mais de um ponto, basear-se "exclusivamente em dados públicos
  disponíveis na plataforma", mas o algoritmo exige autenticação. Dado acessível
  apenas mediante sessão autenticada não é público no sentido que a afirmação
  sugere.
- **A dimensão legal não é enfrentada.** A autora apresenta como cuidado ético a
  decisão de não coletar informações de menor relevância — número de conexões,
  pronomes de tratamento — e de limitar-se a dados de caráter profissional. Não há,
  em nenhum ponto do texto, menção aos **termos de uso da plataforma**, à **base
  legal** do tratamento sob a LGPD, nem a **apreciação ética prévia**. Tratando-se
  de dados pessoais de terceiros coletados sem consentimento e sob autenticação, a
  omissão é relevante — e é exatamente o risco que motivou o descarte da raspagem
  neste projeto.
- **Viés de seleção reconhecido pela própria autora**, mas não medido: analisar
  perfis significa observar quem está na plataforma, mantém o perfil atualizado e o
  deixa acessível. A conclusão de inserção elevada é, no limite, sobre esse
  subconjunto — problema estrutural análogo ao da autosseleção em questionários,
  que a autora atribui ao método concorrente.
- **Não padronização dos campos**, apontada pela autora como dificuldade de
  categorização: cargos e profissões são texto livre, com variação terminológica
  para funções semelhantes. É o mesmo diagnóstico que a E03 fez do instrumento
  vigente do IFSP e que sustenta a diretriz de domínio fechado da E13 — só que aqui
  a fonte não tem como corrigir, porque não controla o preenchimento.
- **Algoritmo não publicado**, o que impede verificação independente do
  procedimento de coleta e da taxa de erro de correspondência entre nome e perfil.
- **Ausência de acompanhamento longitudinal**, reconhecida nas considerações finais.

## Divergências de referência, a conferir na E31

- **Número de folhas:** a ficha catalográfica do SISBIN registra **41 f.**; o arquivo
  em PDF tem 43 páginas. Adotou-se 41 f., que é o dado catalográfico. A ficha
  anterior registrava 43 f.
- **Titulação:** o grau é **bacharel em Estatística e Ciência de Dados**, e não
  "Graduação em Estatística" como constava. Corrigido.
- **Nome do orientador divergente dentro da própria fonte:** a folha de rosto traz
  "Helgem de Souza Martins Ribeiro" e a ficha catalográfica, "Helgem de Souza
  Ribeiro Martins". Não afeta a citação, que é pela autora, mas fica registrado.

## Histórico de leitura

| Data | Etapa | Base da leitura |
|---|---|---|
| 20/09/2026 | E02 | resumo e metadados do repositório — a extração de texto do PDF falhou por ausência de ferramenta nesta máquina |
| 21/09/2026 | E07 | **texto integral**, extraído com `pdftotext` após o provisionamento do ambiente |

A pendência de releitura registrada na E02 e recolhida pela E07 está **encerrada**.
