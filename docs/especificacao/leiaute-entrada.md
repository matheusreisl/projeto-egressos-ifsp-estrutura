# Leiaute do arquivo de entrada

**Etapa:** E11 — especificar o leiaute do arquivo de entrada
**Data:** 28/09/2026
**Ponto de partida:** leiaute da Especificação Técnica Preliminar do [documento do projeto](../projeto/Projeto_de_Pesquisa_Egressos_IFSP.docx)
**Decorre de:** [`parametros-contato.md`](parametros-contato.md) (E05), [`capacidades-plataforma.md`](capacidades-plataforma.md) (E08) e [linha de base](../pesquisa/linha-de-base.md) (E03)

Especificação do arquivo que popula a base de participantes: o que cada linha
representa, em que formato o arquivo chega, que campos traz, de que tipo, com que
obrigatoriedade e sob que regra de validação — e o que acontece quando uma regra
é violada.

É insumo direto da E12 e da E13 (bloco de identificação acadêmica e domínios), da
E16 (base sintética), da E17 (importação), da E18 (pré-preenchimento), da E19
(unicidade), da E21 (âncora do ciclo e fila de correção) e da E25 (matriz de
verificação).

> **Nota de notação.** Como em `parametros-contato.md`, as estratégias do
> [quadro de engajamento](../pesquisa/quadro-engajamento.md) aparecem como
> "linha E*n* do quadro", com um dígito. As etapas do projeto são E01 a E31.

## 1. Objeto e método

**Objeto.** O arquivo estruturado de participantes que a instituição extrai da sua
base acadêmica e que o mecanismo importa a cada ciclo.

**Método.** Derivação documental, como na E05. Cada campo recebe tipo,
obrigatoriedade, regra de validação e — o que decide o critério de conclusão — o
**consumidor** que o justifica: o parâmetro de contato, a capacidade da
plataforma, o indicador do Regulamento ou a etapa que precisa dele. Campo sem
consumidor não entra; consumidor sem campo é lacuna.

**O que esta etapa não faz.** Não escreve o validador nem importa nada: a
importação é da E17 e a base sintética, da E16. Não fecha as listas de cursos e de
unidades, que são domínio compartilhado com o bloco de identificação acadêmica e
ficam com a E13. Não redige questão alguma do instrumento.

### 1.1 O ponto de partida: o documento do projeto já propõe o leiaute

A Especificação Técnica Preliminar do documento do projeto traz um leiaute de
nove campos, apresentado como o "conjunto mínimo necessário à identificação, à
segmentação e ao contato, em observância ao princípio da necessidade":

| Campo | Descrição no documento | Obrig. |
|---|---|---|
| `identificador` | código único do registro na base de origem, usado para deduplicação | sim |
| `nome` | nome completo do egresso | sim |
| `curso` | nome padronizado do curso concluído | sim |
| `campus` | unidade de conclusão | sim |
| `ano_conclusao` | ano de conclusão do curso | sim |
| `semestre_conclusao` | semestre de conclusão (1 ou 2) | sim |
| `email_principal` | endereço de correio eletrônico para contato | sim |
| `email_alternativo` | endereço secundário, quando houver | não |
| `telefone` | contato telefônico com código de área | não |

As duas exigências que a E05 deixou para esta etapa **já estão atendidas** pela
proposta: há mais de uma via de contato e há o semestre de conclusão. A etapa,
portanto, não inventa o leiaute. **Testa** a proposta contra o princípio da
necessidade e contra os consumidores que surgiram depois dela, e acrescenta o que
o documento não tem: tipo e regra de validação.

O teste encontrou uma lacuna, uma indefinição e duas imprecisões:

| # | Achado | Tratamento |
|---|---|---|
| 1 | **Falta o nível do curso.** O Anexo I do Regulamento conta egressos "por ano, campus, nível e curso" (Ind2) e separa técnicos de graduação em oito indicadores (Ind5 a Ind12). A linha de base, na seção 11, já pedia o dado. O documento do projeto não cita o Regulamento, que só foi recuperado na E03 | campo `nivel` acrescentado (seção 4.4) |
| 2 | **A unidade do registro não está definida** — a pessoa ou o curso concluído | decidida: a pessoa (seção 2) |
| 3 | **O `identificador` precisa de propriedades que o documento não enuncia**: estabilidade entre extrações, sem a qual a recusa de contato da P6 não sobrevive ao ciclo seguinte; e não ser documento civil nem token de acesso | seção 4.1 |
| 4 | **"Nome completo" não diz qual nome.** Convite automatizado que trate pelo nome civil quem tem nome social registrado contraria o Decreto nº 8.727/2016 | `nome` passa a ser o nome de tratamento (seção 4.2) |

**Nenhum dos nove campos originais sai, e a obrigatoriedade de cada um é mantida.**
O que muda está consolidado na seção 10 e vira pendência de atualização do
documento do projeto na E31, como os parâmetros da E05.

## 2. Unidade do registro

**Decisão: uma linha por egresso — a pessoa, e não o curso concluído.** Quem
concluiu mais de um curso aparece uma vez, com a **conclusão mais recente** pelo
par (ano, semestre); em empate, a de nível mais alto.

**Origem.** Decisão de projeto, confirmada com o orientando antes da execução e
registrada na [ADR-0005](../decisoes/0005-uma-linha-por-egresso.md).

**Por que a pessoa.** Os parâmetros de contato foram desenhados em torno dela:

- a P4 limita as mensagens **por participante** e por ciclo, e o limite existe para
  conter incômodo ao destinatário — o incômodo é de quem recebe, não do curso;
- a P5 proíbe mais de um convite a cada doze meses e ciclo aberto sobreposto
  **para o mesmo participante**.

Com uma linha por curso, quem fez técnico e graduação no IFSP receberia dois
convites por ano. Reconciliar as duas linhas exigiria uma segunda chave, de
pessoa, além da de conclusão — ou heurística sobre nome e endereço, que erra nos
dois sentidos.

**O que a decisão custa, dito sem arredondar.** O art. 19 do Regulamento
acompanha **por turma**, e quem tem duas conclusões pertence a duas turmas. Com a
conclusão mais recente, o acompanhamento segue a turma mais nova e deixa a
anterior. Para os indicadores, o efeito é coerente: enquanto cursa a graduação, o
egresso técnico continua técnico na base e responde como técnico que prosseguiu
os estudos — entra no numerador do Ind9, e também do Ind5 se prosseguir no IFSP.
Ao concluir a graduação, passa a egresso de graduação na extração seguinte. O que
se perde é o acompanhamento **simultâneo** das duas formações, que tampouco
caberia em um convite por ano.

**Consequência para a âncora do ciclo.** Quando uma conclusão nova chega em
extração posterior, a âncora da P5 passa ao novo semestre. A regra de não
sobreposição continua valendo: o ciclo aberto termina na sua janela, e o seguinte
já parte da âncora nova. É requisito da E21.

## 3. Formato do arquivo

| Aspecto | Especificação |
|---|---|
| Formato | valores separados por vírgula, conforme a RFC 4180: campo com vírgula, aspas ou quebra de linha vai entre aspas duplas, e aspas internas são duplicadas |
| Codificação | UTF-8; marcador de ordem de bytes no início é tolerado e descartado |
| Primeira linha | cabeçalho com **exatamente** os dez nomes de campo da seção 4, cada um uma vez, em qualquer ordem |
| Demais linhas | um egresso por linha; linhas inteiramente vazias são ignoradas; fim de linha CRLF ou LF |
| Valores | espaços nas pontas são removidos antes da validação; campo opcional sem valor fica vazio |
| Guarda | o arquivo nunca é versionado: o sintético fica em `dados/sinteticos/`, fora do controle de versão, e arquivo com dado real não entra no projeto em hipótese alguma |

**O leiaute é fechado.** Coluna fora dele **rejeita o arquivo**, em vez de ser
ignorada. É a forma operacional do princípio da necessidade: o que o mecanismo
não precisa não entra, nem por descuido de extração. Um arquivo que chegue com CPF
ou data de nascimento "a mais" é devolvido, e não aproveitado em parte.

**Coluna opcional ausente também rejeita.** Valor opcional vazio é admitido; a
coluna inteira faltar, não. A diferença importa: a coluna ausente esconde que a
extração esqueceu uma via de contato inteira, e o reparo da P8 degradaria em
silêncio para a base toda.

**Armadilha nomeada.** Planilha configurada em português do Brasil costuma
exportar "CSV" com **ponto e vírgula** e em codificação regional, e não em UTF-8.
O primeiro caso produz cabeçalho que não se divide nos dez campos; o segundo,
bytes que não decodificam como UTF-8. Os dois rejeitam o arquivo, e a mensagem de
rejeição deve nomear a causa provável, porque o sintoma sozinho não a revela.
Aceitar a codificação regional sem aviso seria pior: os nomes acentuados
chegariam corrompidos às mensagens de convite.

## 4. Os campos

| # | Campo | Descrição | Tipo | Obrig. | Regra de validação |
|---|---|---|---|---|---|
| 1 | `identificador` | código estável que a instituição atribui ao egresso na base de origem; chave de deduplicação e de reencontro entre ciclos | texto de 1 a 64 caracteres entre `A–Z`, `a–z`, `0–9`, `.`, `_` e `-` | sim | único no arquivo, sem distinção entre maiúsculas e minúsculas; não pode ter forma de CPF (seção 4.1) |
| 2 | `nome` | nome pelo qual o egresso é tratado: o nome social, quando registrado; o civil, caso contrário | texto de 2 a 150 caracteres | sim | começa por letra; só letras de qualquer alfabeto, espaço, apóstrofo, hífen e ponto; ao menos duas letras; espaços internos repetidos reduzidos a um |
| 3 | `curso` | nome padronizado do curso concluído | texto de domínio fechado | sim | pertence à lista de cursos da instituição (E13); não admite texto livre nem "Outros" |
| 4 | `nivel` | nível do curso concluído | código de domínio fechado | sim | `tecnico`, `graduacao` ou `pos_graduacao` |
| 5 | `campus` | unidade em que o curso foi concluído | texto de domínio fechado | sim | pertence à lista de unidades da instituição (E13); não admite "Outros" |
| 6 | `ano_conclusao` | ano letivo de conclusão | inteiro de quatro dígitos | sim | não posterior ao ano corrente, nem anterior ao limite configurado pela instituição |
| 7 | `semestre_conclusao` | semestre letivo de conclusão | inteiro | sim | `1` ou `2`; curso em regime anual informa `2` |
| 8 | `email_principal` | endereço para convite e lembretes | endereço de correio eletrônico | sim | sintaxe da seção 4.6; domínio convertido a minúsculas |
| 9 | `email_alternativo` | segundo endereço, quando houver | endereço de correio eletrônico | não | mesma sintaxe; diferente do principal |
| 10 | `telefone` | telefone com código do país e de área | texto no formato E.164 | não | seção 4.7 |

Os nomes de campo são os do documento do projeto, acrescidos de `nivel`:
minúsculas, sem acento, com sublinhado. A ordem do quadro é a recomendada, não a
exigida (seção 3).

### 4.1 `identificador`

**Três propriedades, e só a primeira se verifica num arquivo isolado.**

1. **Único no arquivo.** A comparação não distingue maiúsculas de minúsculas,
   para que `EGR-1` e `egr-1` não passem como pessoas diferentes.
2. **Estável entre extrações.** O mesmo egresso recebe o mesmo identificador em
   todo ciclo. É a propriedade de que mais depende o restante do mecanismo: a
   recusa de contato da P6 é permanente e vive na base central de participantes
   (C6, conferida na E08). Um identificador que mude entre extrações faz o
   egresso que recusou voltar como pessoa nova — e ser convidado de novo. É
   requisito da **origem**; o mecanismo só pode flagrar violação por indício entre
   arquivos, não prová-la num arquivo só (seção 9).
3. **Não é documento civil nem o token de acesso.** Nem CPF, nem RG, nem número
   de outro documento: a deduplicação não precisa deles, e o cruzamento com bases
   externas que os justificaria está fora do escopo do projeto, assim como a
   integração com o SUAP e a raspagem de perfis. Nem o token: a C1 exige endereço
   individual **não adivinhável**, e um código acadêmico é sequencial ou previsível.
   O token é gerado pela plataforma; o identificador é da instituição.

**Guarda automática contra o erro mais provável.** Valor que, desconsiderados
pontos e hífens, forme onze dígitos cujos dois últimos conferem como dígitos
verificadores de CPF **rejeita o registro**. A regra pode rejeitar por
coincidência um código interno legítimo de onze dígitos — cerca de um em cem —, e
o custo é baixo: a instituição acrescenta um prefixo. O custo do contrário é o CPF
da base inteira dentro do mecanismo.

**Quando a origem não tem código estável por pessoa.** A instituição pode
derivá-lo por **pseudonimização**: um resumo criptográfico **com chave** — HMAC
com SHA-256, por exemplo — de um código interno, com a chave guardada pela
instituição e fora do mecanismo. É o conceito que a LGPD define no art. 13, §4º,
no contexto de estudos em saúde pública: dado que só se reassocia ao indivíduo
"pelo uso de informação adicional mantida separadamente pelo controlador em
ambiente controlado e seguro". **Resumo sem chave não serve**, sobretudo sobre
CPF: são cerca de um bilhão de números possíveis, um espaço que se percorre por
força bruta em pouco tempo. O resultado em hexadecimal tem 64 caracteres, dentro
do limite do campo.

### 4.2 `nome`

**O nome de tratamento.** O Decreto nº 8.727/2016 obriga os órgãos e entidades da
administração pública federal direta, autárquica e fundacional a adotar, em seus
atos e procedimentos, o nome social da pessoa travesti ou transexual (art. 2º).
Nos registros, o nome civil acompanha o social e é "utilizado apenas para fins
administrativos internos" (art. 3º), e só pode ser empregado, junto do social,
"quando estritamente necessário ao atendimento do interesse público e à
salvaguarda de direitos de terceiros" (art. 5º). Os Institutos Federais têm
natureza jurídica de autarquia (Lei nº 11.892/2008, art. 1º, parágrafo único), e
convite a egresso é comunicação externa. Logo: **nome social, quando registrado;
civil, caso contrário.**

**Um campo, e não dois.** O mecanismo precisa de um nome só — o de tratamento.
Carregar os dois contrariaria a necessidade e reintroduziria o risco que o
decreto quer evitar: o nome civil à mão da próxima rotina que precise "de um
nome". A escolha é feita na extração, onde o sistema de origem conhece os dois; o
registro já chega com o nome certo.

**Por que o campo é necessário.** É o único campo cuja necessidade não vem do
fluxo automatizado. Seus consumidores são o **convite personalizado**, previsto no
documento do projeto (Fase 5), e a **operação humana** da busca ativa e do canal
alternativo — P8 e P9 —, em que o operador precisa saber por quem procura.

**Sem divisão em prenome e sobrenome.** A plataforma separa `firstname` e
`lastname`, mas dividir nome brasileiro por regra erra em partículas ("da",
"dos") e em nomes compostos. O campo chega inteiro, e a correspondência é da E17
(seção 11).

**Sem campo de gênero.** A saudação da E20 será neutra. Acrescentar gênero só para
flexionar "Prezado" e "Prezada" é exatamente o tipo de campo que a necessidade não
sustenta.

### 4.3 `curso` e `campus`

**Domínio fechado, sem "Outros".** O instrumento vigente pergunta o curso em texto
livre e oferece "Outros" em campus e em tipo de curso
([linha de base](../pesquisa/linha-de-base.md), seção 5). No arquivo de entrada,
nenhum dos dois cabe: quem informa é o sistema da própria instituição, que conhece
os seus cursos e as suas unidades. "Outros" só faz sentido quando quem responde é
o egresso.

**As listas não são deste documento.** Os valores admitidos são configuração da
instituição e formam o **mesmo domínio** dos campos correspondentes do bloco de
identificação acadêmica, que o arquivo pré-preenche. Se diferissem, o
pré-preenchimento exibiria valor fora das opções do instrumento. Por isso a E13
fecha os dois de uma vez — e a linha de base, na seção 11, já apontou o curso como
caso-teste do fechamento de domínio.

### 4.4 `nivel` — o campo acrescentado

**Valores.** `tecnico`, `graduacao` e `pos_graduacao`, exibidos como Técnico,
Graduação e Pós-graduação.

**Por que entra.** Os indicadores do Anexo I do Regulamento dependem dele
([linha de base](../pesquisa/linha-de-base.md), Anexo A):

- o **Ind2** conta os egressos por "ano, campus, nível e curso", no sistema e
  entre os respondentes;
- os pares **Ind5/Ind6** a **Ind11/Ind12** — verticalização, verticalização
  qualificada, continuidade e continuidade em área correlata — são definidos
  separadamente para egressos técnicos e de graduação.

Sem o nível na base, esses oito indicadores não têm como separar os seus
denominadores.

**Por que só três valores.** O instrumento vigente oferece nove tipos de curso
([fichamento do portal](../pesquisa/fichamentos/ifsp-portal-egressos-2022.md)), mas
nenhum dos dezenove indicadores usa distinção mais fina que técnico, graduação e
pós-graduação. A forma de oferta — integrado, concomitante, subsequente — e o
grau — tecnologia, licenciatura, bacharelado — derivam do curso, se algum dia
forem necessários. A população-alvo do art. 18 do Regulamento cabe nos três:
técnicos nas três formas, graduação e pós-graduação *lato* e *stricto sensu*.

**Por que não pesa contra a necessidade.** O nível não acrescenta informação sobre
o titular: é função do curso. Está no leiaute para que a segmentação exigida pelo
Regulamento não dependa de um catálogo mantido à parte. Se a lista de cursos da
E13 registrar o nível de cada curso, a coerência entre os dois campos vira regra
de validação — e a redundância passa a proteger, em vez de arriscar.
*Atualizado na E13:* a lista registra o nível de cada curso
([`blocos-instrumento.md`](blocos-instrumento.md), seção 12.3). A regra está
ativa: `nivel` diferente do nível do curso na lista **rejeita o registro**, e a
E17 a implementa com as demais.

### 4.5 `ano_conclusao` e `semestre_conclusao`

**Âncora do ciclo e coorte.** O par é a âncora da P5: o D0 do primeiro ciclo é o
término do semestre de conclusão (art. 19 do Regulamento), e os seguintes vêm a
cada doze meses. É também a coorte do perfil de não resposta. O viés que o Ifes
observou — respondentes concentrados nas turmas dos últimos dez anos (linha E4 do
quadro) — aparece no ano de conclusão sem que seja preciso pedir data de
nascimento.

**O registro traz o semestre, não a data.** A data concreta do D0 depende do
calendário acadêmico de cada unidade e de cada ano, e é **configuração da rotina**
da E21, não dado de entrada. Pedir a data de conclusão de cada egresso
acrescentaria um dado sem acrescentar consumidor.

**Curso em regime anual informa semestre 2**, correspondente ao término do ano
letivo. **O ano corrente é admitido**: a conclusão do semestre em curso entra na
base e só gera ciclo quando o semestre terminar — é o caso dos pré-egressos do
art. 22. O limite inferior é configuração da instituição, e serve para barrar erro
de digitação.

### 4.6 `email_principal` e `email_alternativo`

**Sintaxe.** Endereço na forma `parte-local@domínio`, com:

- parte local de até 64 caracteres, domínio de até 255 e endereço inteiro de até
  254 — os limites da RFC 5321, seção 4.5.3.1, descontados os dois delimitadores
  do caminho;
- parte local no subconjunto usual *dot-atom* da RFC 5322: sem a forma entre
  aspas, sem espaço, sem ponto no início, no fim ou repetido;
- domínio com ao menos um ponto, formado por rótulos de letras, dígitos e hífen.

**Normalização.** O domínio é convertido a minúsculas. A parte local é preservada
como veio, porque a RFC 5321 manda tratá-la como sensível a maiúsculas (seção
2.4), ainda que desaconselhe explorar isso.

**O que a sintaxe não garante: entrega.** Endereço bem formado pode não existir, e
quem descobre isso é o P8, pela devolução. Consultar o domínio na rede durante a
importação seria inútil no ensaio — `.test` não resolve, por definição — e
redundante na implantação, porque o P8 já faz a verificação que importa.

**O alternativo.** Se for igual ao principal, comparados sem distinção entre
maiúsculas e minúsculas, é descartado com alerta: não é segunda via. É ele que dá
à fila de correção da P8 um caminho **automatizável** — o reconvite ao segundo
endereço dentro da rodada única de reparo (`parametros-contato.md`, seção 6.1) —,
ao passo que o telefone depende de ação humana.

### 4.7 `telefone`

**Formato E.164**, sem espaços nem separadores: `+`, código do país e número
nacional, com até 15 dígitos no total — o limite da Recomendação E.164 da UIT.

- **Brasil (`+55`):** código de área de dois dígitos seguido de 8 dígitos (fixo)
  ou de 9 dígitos iniciados por 9 (móvel).
- **Outros países:** apenas a estrutura E.164. O documento do projeto lembra que
  há egressos atuando no exterior, e "código de área", sozinho, não os comporta.

**Consumidores.** A busca ativa reparadora da P8 (linha E1 do quadro) e o canal
alternativo da P9 (art. 16, §1º do Regulamento). Os dois são operação **humana**:
o envio por mensagem instantânea está fora do disparo automatizado
([ADR-0003](../decisoes/0003-canal-alternativo-nao-automatizado.md)). O telefone é
o único campo de contato que nenhuma rotina do mecanismo usa.

**O código de área não é conferido contra o plano de numeração.** Número malformado
é descartado; número bem formado com código inexistente passa. A regra fica mais
simples, o custo é nulo — o erro aparece no primeiro contato humano — e isso
permite ao ensaio usar números **fora** do plano por construção (seção 7).

## 5. Regras entre registros

| Situação | Consequência | Por quê |
|---|---|---|
| o mesmo `identificador` em mais de um registro | **todos** os registros com esse identificador são rejeitados | não há como saber qual está certo; aceitar um deles seria escolher por acaso |
| o mesmo `email_principal` em registros de identificadores distintos | aceita, com alerta | endereço compartilhado existe, e cada registro recebe o seu próprio token; mas é também o sintoma de pessoa duplicada sob dois identificadores, que a E19 verifica |
| registro sem `email_alternativo` e sem `telefone` | aceita, com alerta | rejeitar tiraria o egresso da base, o que é pior do que ter uma via só; mas o relatório precisa contar quantos registros não têm reparo possível |

**A exigência da E05 vale para o leiaute, não para cada registro.** A E05
determinou mais de uma via de contato para que a fila de correção tenha para onde
recorrer, e o leiaute a cumpre. Exigi-la de cada registro converteria dado ausente
na origem em exclusão do egresso — o oposto do que a busca ativa existe para
fazer.

## 6. Consequência de cada violação

Três níveis, escolhidos por uma regra só: **rejeita-se o arquivo quando o problema
é da extração; o registro, quando é do dado; e aceita-se com alerta quando o dado
faltante ou inválido é opcional.**

| Nível | Quando |
|---|---|
| **Rejeita o arquivo** | não decodifica como UTF-8; aspas não fechadas até o fim do arquivo; cabeçalho sem os dez campos, com campo repetido ou com coluna não prevista; no ensaio, qualquer violação da seção 7 |
| **Rejeita o registro** | número de campos diferente do cabeçalho; campo com quebra de linha; campo obrigatório vazio ou fora da regra da seção 4; identificador repetido ou com forma de CPF |
| **Aceita com alerta** | `email_alternativo` ou `telefone` fora da regra, ou alternativo igual ao principal — o valor é descartado e o registro entra; registro sem via alternativa; endereço principal compartilhado |

**Relatório de validação.** Toda importação produz relatório com a contagem por
nível e por regra, e identifica cada registro afetado **pela linha e pelo
identificador, sem reproduzir nome, endereço ou telefone**. Dado pessoal copiado
para registro de execução é dado pessoal fora do lugar onde é protegido.

## 7. Restrições do ensaio

As regras abaixo valem **somente no modo de ensaio**, que é o único em que este
projeto opera. São a restrição inviolável do projeto — nenhum dado real, nenhum
envio a endereço real — convertida em propriedade do arquivo, na mesma lógica com
que a E06 converteu a contenção do disparo em propriedade do ambiente (critério K6
da [ADR-0002](../decisoes/0002-ambiente-execucao.md)).

| Regra | Consequência |
|---|---|
| todo endereço, principal ou alternativo, pertence a domínio sob o TLD reservado `.test` (RFC 2606 e 6761) | violação **rejeita o arquivo inteiro** |
| todo telefone é brasileiro (`+55`), com código de área **terminado em 0** | violação **rejeita o arquivo inteiro** |

**Por que o arquivo inteiro, e não o registro.** Um endereço real numa base
sintética não é erro de dado: é sinal de que dado real vazou para dentro dela.
Aproveitar o restante seria tratar o vazamento como defeito pontual.

**Por que código de área terminado em 0.** Para correio existe domínio reservado;
para telefone, não há equivalente. Nenhum dos 67 códigos nacionais em uso termina
em zero — conferido em 28/09/2026 contra a relação pública dos códigos em uso,
que são os destinados pelo Plano Geral de Códigos Nacionais da Anatel. A consulta
não pôde ser feita na página da própria Anatel, que não respondeu, e por isso a
E16 reconfere na fonte oficial antes de gerar a base. Um número com código
terminado em zero é bem formado e **não pertence a ninguém**, que é exatamente o
que a base sintética precisa. A regra do ensaio é mais estrita que a da seção 4.7,
e é a seção 4.7 que a torna possível.

*Atualizado na E16:* **reconferido na fonte oficial**, em 03/10/2026 — o painel
"CN – Áreas de Numeração" da Anatel, que segue o Plano Geral de Códigos Nacionais
anexo ao Despacho Decisório nº 20/2026/PRRE/SPR, filtrado pelos códigos vigentes.
Os 67 códigos em uso são 11 a 19, 21, 22, 24, 27, 28, 31 a 35, 37, 38, 41 a 49,
51, 53 a 55, 61 a 69, 71, 73 a 75, 77, 79, 81 a 89 e 91 a 99: **nenhum termina em
zero**, e a busca por `*0` no próprio filtro do painel não encontra
correspondência. O painel exibe "68" na contagem do filtro, mas o contador soma
sempre um ao número de valores — conferido em três buscas —, e os valores são 67.
O plano muda por despacho: a regra precisa ser reconferida se o ensaio for
retomado depois de nova alteração do PGCN.

**A contenção do ambiente continua sendo a garantia principal.** O caminho do
correio não tem rota para fora da máquina ([ADR-0002](../decisoes/0002-ambiente-execucao.md),
[ADR-0004](../decisoes/0004-imagem-propria-e-leitura-de-devolucoes.md)). As regras
desta seção são uma segunda barreira, na entrada, e não a substituem. Numa
implantação real, o modo de ensaio é desligado **conscientemente** — é ponto do
guia da E30.

## 8. Verificação do critério de conclusão

O critério é que o conjunto seja **mínimo e suficiente**. A LGPD define a
necessidade como "limitação do tratamento ao mínimo necessário para a realização
de suas finalidades, com abrangência dos dados pertinentes, proporcionais e não
excessivos" (art. 6º, III). A verificação tem as duas direções.

### 8.1 Suficiente — todo consumidor tem os campos de que precisa

| Consumidor | O que precisa | Campos |
|---|---|---|
| P1 — convite individual | endereço para o convite | `email_principal` |
| P5 — âncora do ciclo (art. 19) | semestre de conclusão | `ano_conclusao`, `semestre_conclusao` |
| P6 — recusa de contato permanente entre ciclos | chave que reencontre o egresso no ciclo seguinte | `identificador` |
| P8 — fila de correção | via alternativa automatizável, via humana e saber por quem procurar | `email_alternativo`, `telefone`, `nome` |
| P9 — canal alternativo (art. 16, §1º) | número para mensagem instantânea | `telefone` |
| Convite personalizado (documento do projeto, Fase 5; E20) | nome de tratamento | `nome` |
| E17 e E19 — importação sem duplicidade e unicidade | chave de deduplicação | `identificador` |
| E18 (C9) — pré-preenchimento do bloco de identificação | atributos acadêmicos que a instituição já possui | `curso`, `nivel`, `campus`, `ano_conclusao`, `semestre_conclusao` |
| Ind2 — número de egressos | ano, campus, nível e curso | `ano_conclusao`, `campus`, `nivel`, `curso` |
| Ind5 a Ind12 — verticalização e continuidade | separação entre técnicos e graduação | `nivel` |
| Perfil de não resposta ([linha de base](../pesquisa/linha-de-base.md), seção 4) | comparar respondentes e base pelos mesmos recortes | `curso`, `nivel`, `campus`, `ano_conclusao` |

**Nenhum consumidor descoberto.** Os demais indicadores do Anexo I — o Ind1, de
gestão operacional, e os Ind3, Ind4 e Ind13 a Ind19, calculados sobre respostas —
não pedem atributo de entrada além dos recortes já cobertos.

### 8.2 Mínimo — todo campo tem consumidor

| Campo | Consumidores |
|---|---|
| `identificador` | P6, E17, E19 |
| `nome` | convite personalizado, P8, P9 |
| `curso` | E18, Ind2, perfil de não resposta, turma do art. 19 |
| `nivel` | E18, Ind2, Ind5 a Ind12, perfil de não resposta |
| `campus` | E18, Ind2, perfil de não resposta, turma do art. 19 |
| `ano_conclusao` | P5, E18, Ind2, perfil de não resposta |
| `semestre_conclusao` | P5, E18 |
| `email_principal` | P1 |
| `email_alternativo` | P8 |
| `telefone` | P8, P9 |

**Nenhum campo sem consumidor.**

### 8.3 Mínimo — o que ficou de fora, e por quê

O inventário do que **não** entra é a outra metade da demonstração. A política de
proteção de dados do IFTO lista catorze categorias de dados pessoais, para uma
instituição inteira ([fichamento](../pesquisa/fichamentos/ifto-ppdp-2023.md)); o
leiaute fica em três tipos de dado — identificação, vínculo acadêmico e contato.

| Candidato | Por que fica fora |
|---|---|
| CPF, RG ou outro documento civil | a deduplicação é feita pelo `identificador`; o cruzamento com bases externas que o justificaria está fora do escopo |
| nome civil, quando há nome social | o mecanismo só usa o nome de tratamento, e o decreto restringe o civil ao estritamente necessário |
| data de nascimento ou idade | nenhum indicador a usa; a coorte sai do ano de conclusão |
| sexo, gênero, raça/cor | nenhum recorte do Anexo I os usa, e raça/cor é dado sensível (LGPD, art. 5º, II). Se o instrumento os perguntar, é questão, com consentimento — não atributo de entrada |
| endereço postal | não há contato postal previsto |
| perfis em redes sociais | a busca ativa por redes é operação humana, que não depende de dado armazenado; a raspagem de perfis está fora do escopo |
| forma de oferta e grau do curso | nenhum indicador os usa; derivam do curso |
| código de turma | a turma do art. 19 é o conjunto (curso, campus, ano, semestre) |
| data exata de conclusão ou de colação | o D0 vem do semestre e do calendário configurado na rotina (seção 4.5) |
| e-mail institucional como campo próprio | coberto pelas duas vias de e-mail, sem precisar tipificar |
| recusa ou consentimento anteriores | são estado do mecanismo, guardado na base central, e não dado da origem |
| notas, coeficiente, situação de matrícula | nenhum consumidor |
| idioma | fixo em português |

**Resultado.** Dez campos, nenhum sem consumidor; onze consumidores, nenhum sem
campo; nenhum dado sensível; nenhum documento civil. **Critério atendido.**

## 9. O que esta especificação não permite afirmar

1. **Não se conferiu a compatibilidade com as colunas da plataforma.** Os limites
   de tamanho vêm das normas (RFC 5321, E.164) e de decisão do leiaute — o nome
   até 150 caracteres. A conferência contra o esquema da instância não foi feita
   nesta etapa e passa à E17, em que a importação real a exercita. *Atualizado na
   E17:* conferida — a base central limita nome a 150 e e-mail a 254, os mesmos
   limites do leiaute, e a tabela do questionário usa `text`; nenhum campo trunca
   ([`importacao-base.md`](importacao-base.md), seção 3).
2. **Não se verificou que o sistema de origem de alguma instituição tenha cada
   campo no formato exigido.** O leiaute especifica o que a extração precisa
   **entregar**, não o que o sistema acadêmico contém — não há acesso a sistema
   institucional, por decisão do projeto. Que a instituição já possui curso,
   campus, ano e modalidade é constatação da linha de base (o instrumento vigente
   pergunta ao egresso o que o sistema sabe), e não inspeção do sistema.
3. **A estabilidade do identificador não é verificável num arquivo isolado.** É
   requisito da origem. Entre extrações, o mecanismo só pode flagrar indícios —
   o mesmo endereço sob identificador diferente de um ciclo para outro, por
   exemplo —, e isso fica com a E17 e a E19.
4. **Sintaxe válida não é entrega.** Nenhuma regra desta especificação atesta que
   um endereço existe; é o P8 que o descobre.
5. **Nada aqui envolveu dado de pessoa real.** O exemplo da seção 12 é fictício,
   sob domínio `.test` e com telefone fora do plano de numeração.

## 10. O que mudou em relação ao documento do projeto

| Onde | Documento do projeto | Esta especificação |
|---|---|---|
| unidade do registro | não definida | uma linha por pessoa, com a conclusão mais recente |
| `identificador` | "código único do registro na base de origem, usado para deduplicação" | código **estável** por pessoa, que não é documento civil nem token |
| `nome` | "nome completo do egresso" | nome de tratamento: o social, quando registrado |
| `nivel` | ausente | acrescentado, obrigatório, três valores |
| `telefone` | "com código de área" | E.164, com código do país |
| tipos e regras de validação | ausentes | seções 3 a 7 |

A obrigatoriedade dos nove campos originais não mudou. **Não há alteração de
escopo, de meta nem de cronograma**: o próprio documento prevê que as definições
da Especificação Técnica Preliminar "poderão ser refinadas ao longo do trabalho,
mediante registro da justificativa no relatório final". Fica como pendência da
**E31**, junto com o ajuste de fundamentação dos parâmetros de contato que veio da
E05.

## 11. O que esta especificação determina para as etapas seguintes

- **E12 (blocos)** — o bloco de identificação acadêmica pré-preenche curso, nível,
  campus, ano e semestre; a segmentação que ele alimenta passa a incluir o nível.
- **E13 (domínios)** — fechar as listas de cursos e de unidades como domínio
  **compartilhado** entre o leiaute e o bloco de identificação, sem "Outros"; e
  decidir se a lista de cursos registra o nível de cada curso, caso em que a
  coerência entre `curso` e `nivel` vira regra de validação.
- **E16 (base sintética)** — uma linha por pessoa; identificadores sintéticos
  estáveis e sem forma de CPF; endereços só sob `.test`; telefones `+55` com
  código de área terminado em 0, depois de reconferir na fonte oficial da Anatel
  que nenhum código em uso termina em zero (seção 7); parte da base **sem** via
  alternativa e parte **com** `email_alternativo`, para exercitar o alerta e o
  reparo.
- **E17 (importação)** — implementar as seções 3 a 7 como validação **prévia** à
  importação, em modo de ensaio; reencontrar o egresso na base central pelo
  `identificador`; conferir os tamanhos contra as colunas da plataforma; registrar
  cada importação na trilha — data, resumo SHA-256 do arquivo e contagens por
  regra; e eliminar o arquivo depois de importado, porque o dado pessoal é
  eliminado ao término do seu tratamento (LGPD, art. 16). **Decidir**, ainda, o que
  prevalece quando uma extração nova traz um contato que o mecanismo já corrigiu
  por busca ativa. A correspondência prevista com a plataforma, **não verificada**:

  | Campo | Destino previsto |
  |---|---|
  | `identificador` | atributo do participante e da base central; **nunca** o `token` |
  | `nome` | `firstname`, inteiro, com `lastname` vazio |
  | `email_principal` | `email` |
  | `curso`, `nivel`, `campus`, `ano_conclusao`, `semestre_conclusao` | atributos do participante, para o pré-preenchimento (C9) |
  | `email_alternativo`, `telefone` | de preferência **só na base central**: o questionário não precisa deles, e o que não está na tabela do questionário não acompanha a exportação das respostas |

  *Atualizado na E17:* verificada, com dois acréscimos — curso e campus vão ao
  participante do questionário pelo **código** do instrumento, e todo contato da
  base central fica **cifrado**, como a plataforma já cifra nome e e-mail. A
  precedência decidida é a da correção até a origem mudar
  ([`importacao-base.md`](importacao-base.md), seções 3 e 5).

- **E18 (pré-preenchimento)** — os atributos exibidos são os cinco acadêmicos; o
  nome, quando exibido, é o de tratamento.
- **E19 (unicidade)** — além de token repetido: identificador repetido,
  identificador igual a algum token e o alerta de endereço principal compartilhado.
- **E20 (mensagens)** — saudação com o `nome` inteiro e em forma neutra, sem
  flexão de gênero.
- **E21 (rotina)** — a data do D0 vem de calendário configurável por semestre, e
  não do arquivo; a âncora muda quando chega conclusão nova (seção 2); e a fila de
  correção tem **duas vias de naturezas diferentes**: o `email_alternativo`, que
  admite reconvite automatizado dentro da rodada única de reparo, e o `telefone`,
  que é operação humana.
- **E23 (conformidade)** — o relatório de validação não reproduz dado pessoal, e a
  eliminação do arquivo de entrada entra na política de retenção.
- **E25 (matriz)** — o requisito "importação da base" precisa de arquivos
  **inválidos de propósito**, um por regra de rejeição, e não só do arquivo
  sintético válido. A rejeição de endereço fora de `.test` é característica
  verificável da contenção, como o K6.
- **E26 (cenários)** — o ciclo de reparo herdado da E09 ganha, com este leiaute,
  uma via automatizável — o `email_alternativo` —, e é por ela que o cenário de
  contato inválido pode ser exercitado sem ação humana.
- **E30 (guia)** — como produzir o arquivo: UTF-8 e vírgula, com a armadilha da
  planilha em português; o nome de tratamento; a pseudonimização do identificador
  quando a origem não tiver código estável; e o desligamento consciente do modo de
  ensaio.
- **E31 (relatório final)** — atualizar o leiaute no documento do projeto,
  conforme a seção 10.

## 12. Exemplo

Fictício, só para mostrar o formato. Endereços sob `.test`, telefone com código de
área inexistente e cursos e unidades meramente ilustrativos — as listas reais são
da E13.

```csv
identificador,nome,curso,nivel,campus,ano_conclusao,semestre_conclusao,email_principal,email_alternativo,telefone
EGR-000123,Pessoa Exemplo Um,Tecnologia em Análise e Desenvolvimento de Sistemas,graduacao,Campus Exemplo A,2021,2,pessoa.exemplo1@egressos.test,exemplo1.alt@egressos.test,+5520912345678
EGR-000124,Pessoa Exemplo Dois,Técnico em Informática,tecnico,Campus Exemplo B,2019,2,pessoa.exemplo2@egressos.test,,
```

O primeiro registro tem as três vias de contato. O segundo é aceito com alerta,
porque não tem via alternativa: se o endereço principal devolver erro, a fila de
correção não terá para onde recorrer.
