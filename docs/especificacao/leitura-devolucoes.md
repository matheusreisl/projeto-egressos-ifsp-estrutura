# Leitura e classificação de devoluções

**Etapa:** E09 — configurar e verificar o envio de mensagens
**Data:** 27/09/2026
**Implementa:** parâmetro **P8** da seção 10 de [`parametros-contato.md`](parametros-contato.md)
**Decorre de:** [ADR-0004](../decisoes/0004-imagem-propria-e-leitura-de-devolucoes.md)

## 1. O que esta etapa tinha de resolver

A seção 10.4 do P8 é explícita sobre a armadilha: *"uma configuração de SMTP que
envie corretamente e não permita ler devoluções satisfaz o critério de conclusão
da E09 tal como hoje redigido e ainda assim inviabiliza P8. A E09 precisa
verificar as duas direções."*

Capturadores de SMTP de uso corrente em desenvolvimento aceitam toda mensagem e
**nunca devolvem erro**. Servem para inspecionar o que foi enviado. Não servem
aqui, porque o P8 não pede para ver a mensagem — pede para **ler e classificar a
devolução**.

Logo, o ambiente precisava de um agente de transporte de verdade, e a leitura
precisava de rotina própria, pelo motivo já decidido na ADR-0004: a extensão
`imap` do PHP, de que o rastreamento nativo do LimeSurvey depende, não se
constrói mais sobre a base atual.

## 2. Desenho do correio de ensaio

Três domínios, cada um produzindo **uma linha** da tabela de classificação da
seção 10.1. Todos sob o TLD reservado `.test` (RFC 2606 / 6761), que não resolve
na internet pública.

| Domínio | Mecanismo | Linha da tabela do P8 |
|---|---|---|
| `egressos.test` | destino final, com reescrita para a caixa coletora | *sem retorno* — segue a cadência |
| `invalido.test` | destino final, usuário inexistente | **erro permanente** (5.x.x) |
| `indisponivel.test` | retransmissão para endereço não roteável | **erro temporário** (4.x.x) |

Duas caixas locais, e a separação é funcional: `devolucoes` recebe os retornos e
`entregues` recebe as mensagens entregues. Sem separá-las, a rotina veria
mensagens comuns no meio das devoluções.

### 2.1 Três detalhes que decidem se há devolução a ler

Registrados porque cada um, sozinho, faz a etapa fracassar de um modo que parece
sucesso.

**`local_recipient_maps` vazio.** Com o valor padrão, o Postfix recusa o
destinatário inexistente **no próprio diálogo SMTP**, com um 550 síncrono. O
remetente recebe um erro de protocolo e **nenhuma devolução é gerada**. Com o
parâmetro vazio, o servidor aceita a mensagem e falha na entrega, produzindo a
devolução assíncrona que o P8 pressupõe — que é também o que acontece no mundo
real, onde quem recusa é o servidor de destino, não o de origem.

**`relay_domains` precisa nomear o domínio indisponível.** Ele não é destino
final: precisa ser *retransmitido* para o endereço inalcançável, e é a tentativa
frustrada que gera o erro temporário. Sem declará-lo, o Postfix responde
`454 4.7.1 Relay access denied` no diálogo e, de novo, não há o que ler.

**O aviso de atraso não é imediato.** O erro temporário não produz devolução na
hora: o servidor guarda a mensagem na fila e só avisa depois de
`delay_warning_time`. No ambiente de ensaio esse tempo está reduzido a um minuto,
para caber em tempo de verificação. **Em implantação real seriam horas**, e isso
tem consequência para a E21: a rotina de leitura não pode pressupor que a
devolução temporária chegue dentro do mesmo disparo que a originou.

## 3. Como a classificação é feita

O dado que manda é o **código de estado** da RFC 3463, presente no campo
`Status:` da parte `message/delivery-status`:

| Evidência | Classificação | Tratamento do P8 |
|---|---|---|
| `Status: 5.x.x` | **permanente** | marca o contato como inválido na **primeira** ocorrência |
| `Status: 4.x.x` | **temporário** | conta; marca na **terceira** ocorrência do mesmo ciclo |
| sem código, `Action: failed` | permanente | idem permanente |
| sem código, `Action: delayed` | temporário | idem temporário |
| nada reconhecível | **indeterminado** | registra e **não marca** |

A categoria `indeterminado` não está no P8 e foi acrescentada aqui. A razão é
que o P8 pressupõe uma devolução legível, e nem toda devolução do mundo real é:
há servidores que respondem em prosa, sem a estrutura normalizada. Tratar o
ilegível como permanente marcaria contatos por falha de interpretação; tratá-lo
como temporário o faria contar para um limiar que ele não deveria alimentar.
Registrar sem agir é a única opção que não inventa informação — e deixa o caso
visível para inspeção.

A rotina tenta primeiro o caminho normalizado (RFC 3464) e, não o encontrando,
recorre à leitura do texto, extraindo endereço e código por expressão regular.
O que sai daí cai em `indeterminado` quando não há código.

## 4. Onde cada coisa é gravada

| O quê | Onde | Por quê |
|---|---|---|
| estado de entrega do participante | `emailstatus`, pela **API** do LimeSurvey | é o campo da plataforma para isso, e ir pela API evita depender do esquema interno |
| registro de cada devolução | tabela própria `egressos_devolucoes` | o P8 exige registro, e o limiar de três ocorrências precisa de contagem que o LimeSurvey não tem onde guardar |

A tabela própria é também **insumo da trilha de auditoria da E23**: guarda data e
hora da leitura, ciclo, questionário, participante, endereço, tipo, código,
ação, diagnóstico e se houve marcação.

A chave única sobre `(mensagem_id, destinatario)` garante **idempotência**: a
mesma devolução lida duas vezes não conta duas para o limiar. Sem isso, uma
segunda execução da rotina marcaria contatos indevidamente.

### 4.1 A distinção que a rotina precisa respeitar

A seção 10.2 do P8 é taxativa: **contato inválido não é recusa.** São coisas
diferentes com efeitos opostos entre ciclos.

A E08 descobriu onde cada uma vive na plataforma, e a diferença é o que torna
esta implementação possível sem confundi-las:

- **contato inválido** → `emailstatus` no participante do ciclo corrente, que
  morre com a tabela daquele ciclo. É o que a rotina escreve.
- **recusa de contato** → marcação persistente na base central de participantes.
  **A rotina não toca nisso**, em nenhuma circunstância.

Confundir as duas converteria falha de cadastro em manifestação de vontade que
ninguém expressou, e degradaria a base a cada ciclo. A verificação da etapa
confere explicitamente que o contador de recusa permanece em zero depois de a
rotina agir.

### 4.2 A fila de correção não é estrutura nova

O P8 fala de "fila de correção". Ela não exige tabela nem marcação própria: é o
**conjunto de participantes cujo contato está marcado como inválido**, isto é,
uma consulta. Registrar isso evita que a E21 ou a E23 implementem uma marcação
redundante, como a E05 já advertira a respeito de "não respondente".

## 5. Como se verifica

Dois verificadores, com divisão deliberada de responsabilidade:

| Artefato | O que exercita |
|---|---|
| [`scripts/verifica_correio.py`](../../scripts/verifica_correio.py) | o **correio**, por SMTP direto, sem o LimeSurvey no caminho — isola o comportamento do agente de transporte |
| [`infra/confere-envio.py`](../../infra/confere-envio.py) | a **integração**: a instância dispara, a devolução volta, a rotina classifica, o estado do participante muda e a recusa permanece intacta |

O segundo chama a rotina de verdade, e não uma reimplementação dela. É a
diferença entre verificar o mecanismo e verificar uma cópia do mecanismo.

## 6. Três armadilhas da API, tratadas num lugar só

Estão concentradas em [`scripts/limesurvey_api.py`](../../scripts/limesurvey_api.py)
em vez de repetidas por rotina. Registram-se aqui porque **a E28 vai encontrar as
mesmas**, e cada uma falha de modo silencioso.

**O campo `status` não significa erro.** Ele carrega também mensagem informativa
de sucesso: `invite_participants` responde `0 left to send` quando todos os
convites saíram. Tratar todo `status` diferente de `OK` como falha faz um envio
bem-sucedido parecer erro. O sinal confiável é a presença de `error_code`.

**Ausência de dados vem como erro.** `list_surveys` num ambiente recém-criado
responde `ERR_NO_DATA`, e `list_participants` faz o mesmo antes de haver
participantes. Não é falha: é o estado esperado. Confundir os dois faz a rotina
abortar exatamente onde deveria seguir.

**A estrutura de retorno é mista.** Em `list_participants`, os campos
`firstname`, `lastname` e `email` vêm **aninhados** sob `participant_info`,
enquanto `tid`, `token`, `emailstatus` e `sent` vêm no **nível de cima**. Ler
tudo de um dos dois lugares devolve campo vazio **sem erro algum** — e foi o que
levou esta etapa a concluir que uma gravação bem-sucedida não havia pegado. A
gravação estava correta; a leitura, não. O cliente compartilhado devolve os
registros já achatados.

**Lista vazia não significa "todos".** `invite_participants` com lista vazia de
tokens responde `No candidate tokens`, que parece falha de configuração e é
engano de chamada: a API traduz a lista vazia num conjunto vazio. Omitir o
parâmetro é o que aciona o comportamento pretendido.

## 7. Achado de ambiente, que não é do desenho

Durante esta etapa o serviço de correio apresentou falha intermitente cuja causa
levou três diagnósticos para ficar clara, e que **não é do mecanismo**: num
hospedeiro WSL, o relógio da máquina virtual **salta** quando a distribuição
suspende e retoma. O Dovecot detecta o salto — "Time moved backwards" — e se
recusa a lançar serviços durante aquele intervalo.

O sintoma observado foi o pior possível para diagnóstico: o contêiner
aparentemente saudável, a porta aberta, a autenticação interna funcionando, e
toda sessão de rede recusada. Um dos registros mostrou
`1/1 successful auths in 4294967285 secs` — um valor negativo que estourou o
inteiro, marca inconfundível do relógio andando para trás.

**O que se fez.** A verificação de saúde e a supervisão interna passaram a fazer
**LOGIN de verdade** no IMAP, e não apenas abrir a porta; duas falhas seguidas
encerram o processo para que a política de reinício recrie o contêiner.

**Verificado, e não apenas afirmado.** Matando o Dovecot dentro do contêiner, a
supervisão reagiu e o contêiner foi **recriado em cerca de 20 segundos**, com o
serviço de volta e saudável. A recuperação automática é comportamento medido.

**O que se fez depois, na raiz.** A causa mais frequente — a distribuição ser
encerrada por ociosidade — foi desligada no hospedeiro, com
`instanceIdleTimeout = -1` no `.wslconfig`. Está documentado em
[`infra/README.md`](../../infra/README.md), na parte de opções de hospedeiro,
porque é ajuste **do hospedeiro** e não da composição.

**O que continua em aberto.** O ajuste não cobre suspensão ou hibernação do
Windows, em que a máquina virtual suspende de todo modo e o relógio volta a
saltar na retomada. Por isso a supervisão do serviço permanece — e por isso a
**E21** ainda tem de decidir onde o agendador vive. Em Linux nativo nenhuma
dessas duas coisas ocorre.

## 8. O que esta etapa não permite afirmar

1. **Não se verificou o limiar de três ocorrências em condições reais de
   cadência.** A regra está implementada e a contagem é feita sobre a tabela
   própria, mas exercitá-la exige três devoluções temporárias ao mesmo
   participante no mesmo ciclo, com os intervalos de P3 entre elas. Isso é
   cenário da **E26**.
2. **Não se verificou o comportamento diante de devolução não normalizada.** O
   agente de transporte do ensaio devolve sempre no formato da RFC 3464. O
   caminho de leitura em prosa existe e é exercitado apenas pela lógica, não por
   devolução real — declarado como limite, e não como recurso testado.
3. **O tempo do aviso de atraso está reduzido para caber no ensaio.** Um minuto,
   contra horas numa implantação real. Nada se pode afirmar sobre o
   comportamento da rotina em escala de tempo real a partir desta verificação.
4. **Nada aqui foi verificado sobre endereço real.** O correio não tem rota de
   saída; os domínios são reservados; a base é sintética.

## 9. O que determina para as etapas seguintes

- **E20 (modelos de mensagem)** — o remetente de ensaio é
  `naoresponda@egressos.test` e o endereço de retorno é
  `devolucoes@egressos.test`. O remetente institucional é especificação de
  implantação real, conforme a seção 9.1 do P8, e não valor de ensaio.
- **E21 (rotina agendada)** — três coisas. A rotina de leitura de devoluções
  precisa entrar no agendamento, e não só o disparo. A devolução temporária
  **não chega dentro do mesmo disparo que a originou**, de modo que a leitura tem
  de ser independente da cadência. E a raiz do problema do hospedeiro que
  suspende precisa ser resolvida ali.
- **E23 (conformidade)** — a tabela `egressos_devolucoes` é insumo da trilha de
  auditoria, e já registra data, hora, ciclo e via. A rotina **não** toca a
  marcação de recusa; se a E23 precisar registrar recusa, é outra via.
- **E25 (matriz de verificação)** — o requisito "contato inválido" pode ser
  redigido contra o que os dois verificadores desta etapa já executam.
- **E26 (cenários)** — exercitar o limiar de três ocorrências e o ciclo de reparo
  com o teto de uma rodada.
- **E30 (guia)** — os três detalhes da seção 2.1 precisam constar. Cada um deles,
  se esquecido, produz um ambiente que parece funcionar e no qual o P8 é
  inexequível.
