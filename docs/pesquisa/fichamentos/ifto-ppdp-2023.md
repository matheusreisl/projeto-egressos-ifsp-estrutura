# IFTO — Política de Proteção de Dados Pessoais

**Referência:** INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO TOCANTINS
(IFTO). Política de proteção de dados pessoais. Palmas: IFTO, 2023.
**Tipo:** normativa (ato institucional)
**Acesso:** https://portal.ifto.edu.br/acesso-a-informacao/privacidade-e-protecao-de-dados/documentos-lgpd-ifto/PPDP.pdf · consultado em 20/09/2026
**Alimenta:** E10, E11, E22, E23, E25, E31

> **Correção de referência.** O documento do projeto data esta fonte de 2021. O PDF
> disponível no endereço citado está assinado eletronicamente em **27/12/2023**,
> pela Gestora de Segurança da Informação, pelo Diretor e pela Encarregada pelo
> Tratamento de Dados Pessoais. Como o art. 66 prevê revisão a cada dois anos, é
> plausível que exista versão anterior de 2021 e que esta seja sua revisão — mas a
> versão acessível hoje é a de 2023. A referência precisa ser corrigida.

## Problema identificado

A LGPD é norma geral e não diz a uma instituição de ensino como operacionalizar
suas obrigações. A PPDP preenche essa distância no âmbito do IFTO, estabelecendo
conceitos, princípios, diretrizes, competências e responsabilidades para o
tratamento de dados pessoais, aplicáveis a todos os campi, servidores, discentes,
prestadores e terceiros.

## Método

Ato normativo institucional, em 24 capítulos. Os relevantes para este projeto:

| Capítulo | Conteúdo |
|---|---|
| II | conceitos, reproduzindo as definições do art. 5º da LGPD |
| III | base legal, listando LAI, Marco Civil, LGPD e correlatos |
| IV | princípios, reproduzindo os dez do art. 6º da LGPD |
| V | diretrizes gerais — o capítulo operacionalmente mais denso |
| VII | coleta: categorias de dados e finalidades declaradas |
| XIV | direitos dos titulares |
| XVIII | segurança durante o tratamento e boas práticas |

## Resultado

**O achado principal.** O art. 10, §3º, III, declara o **acompanhamento de egressos
como finalidade expressa de tratamento de dados pessoais** no IFTO, descrita como
"notícias da instituição, iniciativas de sucesso profissional de alunos, pesquisas
sobre empregabilidade, oferta de formação contínua e formalizada".

**Diretrizes convertíveis em requisitos** (art. 8º):

| Dispositivo | Diretriz | Requisito correspondente |
|---|---|---|
| §4º | manter registro das operações de tratamento | trilha de auditoria (E23) |
| §5º | elaborar e atualizar o RIPD | fora do escopo, mas citável no relatório |
| §6º | manter avisos de privacidade por ambiente | conteúdo da tela de consentimento (E22) |
| §11 | **Privacy by Design** — assegurar os princípios desde a concepção | método do projeto |
| §12 | procedimentos documentados de descarte | política de retenção (E23) |
| §15 | acesso restrito ao necessário (*need to know*) | níveis de acesso (E29) |
| §16 | **adotar como padrão interações que não envolvam identificação do titular** | anonimização por padrão (E23) |

**Segurança** (art. 56): acesso limitado a quem trata (§4º, I); termos de sigilo com
operadores (§4º, III); armazenamento em ambiente seguro (§4º, IV); compartilhamento
por canal criptográfico (§5º); controles de integridade que permitam identificar
alteração não autorizada (§6º).

## Implicação para o projeto

**1. É o modelo institucional que falta ao IFSP.** O contraste é o argumento mais
útil desta fonte. Dois institutos federais, duas políticas: a do IFSP trata do
acompanhamento de egressos e não menciona proteção de dados; a do IFTO trata de
proteção de dados e declara o acompanhamento de egressos como finalidade de
tratamento. Nenhuma das duas cobre a junção. O mecanismo proposto por este projeto
se situa exatamente aí, e o par de fontes demonstra que a lacuna é real e
documentável — não uma hipótese do autor.

**2. Sustenta metodologicamente a abordagem do projeto.** O art. 8º, §11, adota
Privacy by Design: os princípios devem ser assegurados desde a concepção do
serviço, não acrescentados depois. É precisamente o que o projeto faz ao tratar
consentimento, anonimização e trilha de auditoria como requisitos de construção
verificados por simulação (E22, E23, E25), e não como ajuste posterior. Vale
citar no relatório final como fundamento da escolha metodológica.

**3. Fornece o texto de apoio para requisitos que a LGPD deixa em aberto.** Onde a
LGPD diz "manter registro das operações" sem detalhar, a PPDP adiciona a exigência
de controles de integridade que permitam identificar alteração não autorizada
(art. 56, §6º) — o que é um critério verificável para a trilha de auditoria. O
art. 8º, §16, converte a anonimização de possibilidade em padrão, o que é mais
exigente que o art. 12 da LGPD e mais fácil de testar.

**4. O rol de categorias de dados serve de contraexemplo útil para a E11.** O art.
10, §1º, lista catorze categorias, de identificação a dados de saúde e bancários.
É o inventário de uma instituição inteira, não o conjunto de um instrumento de
egressos. Citá-lo é útil justamente para demonstrar a aplicação do princípio da
necessidade: o leiaute de entrada deve ficar em uma fração disso.

## Limitações da fonte

- **Não vincula o IFSP.** É política de outra instituição da rede federal. Seu uso
  aqui é como referência de boa prática e evidência de que o arranjo é viável em
  um IF, não como norma aplicável ao caso.
- **É documento de governança, não especificação técnica.** Diz "manter registro
  das operações" sem definir formato, campos mínimos, granularidade ou prazo de
  retenção. A lacuna que a LGPD deixa é estreitada, mas não fechada. As decisões
  concretas continuam sendo do projeto e precisam ser registradas em ADR.
- **Boa parte das diretrizes é condicionada.** "Quando possível" e "sempre que
  possível" qualificam dispositivos centrais, inclusive os §§ 3º, 15 e 16 do art.
  8º e os §§ 3º e 8º do art. 56. A anonimização por padrão, que é a diretriz mais
  forte para este projeto, está entre as condicionadas — o que enfraquece sua
  exigibilidade e convém registrar ao citá-la.
- **Não trata do caso específico.** Declara o acompanhamento de egressos como
  finalidade, mas não desce ao instrumento: nada diz sobre base legal aplicável à
  pesquisa com egressos, forma de coleta do consentimento, prazo de retenção das
  respostas ou tratamento da recusa. Essas são exatamente as decisões que este
  projeto precisa tomar, e a fonte as deixa em aberto.
- **Não há evidência de implementação.** O documento estabelece o que deve ser
  feito. Nada nele demonstra que foi feito, nem há aqui avaliação de conformidade
  da prática do IFTO. A fonte é normativa, não empírica.
