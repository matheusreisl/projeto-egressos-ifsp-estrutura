# Simulação controlada

**Etapa:** E26 — executar os cenários de simulação
**Início:** 09/10/2026 · **em andamento**
**Decorre de:** [`matriz-verificacao.md`](matriz-verificacao.md) (seções 2.1 e 21), que
fixa a ordem de execução e os resultados esperados
**Onde está:** [`infra/cenarios.py`](../../infra/cenarios.py) (o respondente, por
HTTP) · [`infra/reparo-contato.py`](../../infra/reparo-contato.py) e o comando de
console `repararcontato` (a operação de reparo) · os registros de execução ficam
fora do repositório; o que eles mostram está aqui

> **Os números deste documento não são resultados sobre egressos.** São de base
> sintética, sob domínio reservado, e servem para mostrar que o mecanismo se
> comporta como especificado — não para descrever população alguma.

## 1. O que esta etapa entrega

A execução dos quatro cenários do documento do projeto — preenchimento parcial com
retomada, ausência de resposta ao longo de sucessivos disparos, contato inválido e
recusa —, pelo caminho real do respondente e com a rotina em **modo real**, em
**dias de calendário**. E, antes deles, a abertura que a matriz exige: contenção,
arquivos inválidos, carga e a bateria das conferências que exercitam e desfazem.

Cada resultado vai para a seção 17 da matriz, pela regra da seção 2.4 dela. Aqui
fica o que a tabela não comporta: como cada cenário foi conduzido, o que se viu, e
o que mudou no caminho.

## 2. Como a simulação foi conduzida

**Decisões do orientando, antes de começar:**

| Decisão | Por quê |
|---|---|
| reimplantar o 202615 para a carga completa (R01.1) | é a última vez em que isso não custa nada: depois do modo real, refazer a carga apagaria a simulação |
| cadência em **dias de calendário**, sem compressão | é o que a E21 não pôde ver: a rotina viu cada situação num disparo, com as datas postas no passado pela API |
| corrigir a conferência 8 de `confere-rotina.py --agendada` antes de rodar a bateria | ela reprovava as execuções `perdida`, que são o comportamento certo (R06.2) |
| registrar aqui e na seção 17 da matriz | a matriz tem a linha por item; o relato precisa de lugar próprio |

**O calendário.** O modo real é ligado antes do disparo agendado de **terça,
13/10/2026, às 10:00** — segunda, 12/10, é feriado na agenda. Para quem é convidado
nesse dia, os lembretes vencem assim, pela regra da seção 4.2 de
[`rotina-disparo.md`](rotina-disparo.md):

| Mensagem | Vence | Sai | Por quê |
|---|---|---|---|
| convite | âncora (15/07) já passou | ter 13/10 | 1º disparo em modo real |
| lembrete 1 | D+4 = sáb 17/10 | **seg 19/10** | fim de semana |
| lembrete 2 | D+7 = ter 20/10 | **qui 22/10** | intervalo mínimo de 3 dias do lembrete 1 |
| lembrete 3 | D+14 = ter 27/10 | **ter 27/10** | — |
| fim da janela | 60 dias | 12/12 | — |

O hospedeiro precisa estar ligado às 10:00 em cada um desses dias. Um dia perdido é
registrado como `perdida`, e o que venceu sai no dia útil seguinte (matriz, seção
2.2).

## 3. A abertura (momento A)

Em 09/10/2026, com o 202615 sem resposta, sem envio e em modo simulado.

| Item | O que se fez | Resultado |
|---|---|---|
| VC1.1–VC1.5, VC1.7 | sondas de rede no correio e nas rotinas, com controle positivo no LimeSurvey; configuração de entrega; Postfix; domínios; `verifica-ambiente.sh` | correio e rotinas só em `egressos_interna` (`internal=true`); não resolvem nome externo nem alcançam a internet, nem a porta 25; o LimeSurvey alcança; entrega por `smtp` a `correio:25`, nenhuma configuração de correio no banco; `relayhost` vazio; domínios sob `.test`; 21 de 21 |
| R01.5 | os 31 casos da matriz, um arquivo cada, contra `valida_entrada.py` | **31 de 31** com o desfecho esperado; em nenhum o relatório reproduziu nome, endereço ou telefone. Em N29, descartar o telefone deixou SIN-000100 sem via alternativa (139 → 140 alertas): consequência esperada, e não defeito |
| R01.6 | importação real do caso N08 (endereço fora de `.test`) | arquivo inteiro rejeitado; as duas impressões digitais iguais antes e depois; trilha nº 13, `arquivo_rejeitado`, com o motivo; arquivo eliminado |
| R01.1 | regenerar (SHA-256 `f2e5b698…a455`), validar, reimplantar, preparar, importar, ativar | 500 lidos, 500 aceitos (144 com alerta); trilha nº 14: `participantes_criados = 500`, `base_central_criados = 0`, `base_central_atualizados = 500`; arquivo eliminado; unicidade 8 de 8, com os três pares |
| R01.2 | reimportar o mesmo arquivo | trilha nº 15: 0 criados, 500 atualizados; as duas digitais idênticas. A da base central é também a de **antes** da reimplantação |
| R02.1 | `confere-participantes.py` | 8 de 8; grupos SIN-000230 · SIN-000461, SIN-000267 · SIN-000354, SIN-000345 · SIN-000408 |
| R03.3 | atributos dos 500 contra a configuração | 500 de 500 |
| R04.1, R03.1, VC3.1 | `confere-instrumento.py` | 9 de 9; os dez caminhos sobre 2.802 combinações |
| R08.1 | `confere-consentimento.py` | 2 de 2, termo `ensaio-2` |
| R09.1, VC2.1 | `confere-conformidade.py` | 2 de 2 |
| R07.1 | `confere-rotina.py` | 7 de 7; a regra 1 tem hoje 17 casos de estado, e não os 16 que a E21 registrou |
| R10.7, VC1.5 | `confere-mensagens.py` | 4 de 4 |
| R02.2, R07.4 | `confere-mensagens.py --enviar` | 9 de 9 |
| R06.1, R07.2 | `confere-rotina.py --agendada` | 14 de 14; disparo de teste 10 s depois do horário; lembretes só para A, B, C e D, reconvite só para M, nada para os demais nem para os 486 de controle |
| R06.2 | `confere-rotina.py --perdida` | 8 de 8, depois da correção da seção 3.1 |
| R08.2 | `confere-consentimento.py --exercitar` | 11 de 11 |
| R09.2, VC3.2 | `confere-conformidade.py --exercitar` | 12 de 12 |

### 3.1 Duas correções em `confere-rotina.py`

As duas na conferência, e não na rotina. A rotina fez o que devia nos dois casos.

**A conferência 8 de `--agendada`** exigia que toda execução agendada do ciclo fosse
`simulada`. As três `perdida` de 07 a 09/10 — o hospedeiro parado às 10:00 (matriz,
seção 2.2) — a reprovariam sem defeito real. Passou a aceitar `perdida` que não
começou, e reprova só execução que tenha rodado fora da hora ou com outra situação.
Decisão do orientando, antes da execução.

**A `--perdida`** esperava um único registro, o de hoje. Mas o agendador acusa todo
horário de disparo passado sem execução desde o **primeiro registro da rotina**, e
com o horário de teste (14:17) os dias úteis de 05 a 08/10 também saíram perdidos —
o que é o comportamento especificado. Na E21, o primeiro registro era do próprio
dia, e a expectativa coincidia por acaso. A conferência passou a exigir: todos os
registros `perdida`, nenhum iniciado, todos em dia útil, no horário de teste, e o de
hoje entre eles. Correção do mesmo tipo da anterior, feita na execução e comunicada
ao orientando.

### 3.2 Incidente: `confere-envio.py` apagou o 202615

**O que aconteceu.** Às 18:02 UTC de 09/10, a conferência de integração do correio
(R10.2) apagou **todos os questionários da instância**, inclusive o 202615. Ela
começava assim desde a E09: listava os questionários e removia cada um, como
limpeza de sobras de execuções anteriores. Foi escrita quando a instância não tinha
instrumento, e não rodava desde a E10. A matriz a prescreveu para o momento A, e ela
foi executada sem que esse trecho fosse lido antes. **Erro de execução desta
etapa**, e não do mecanismo.

**O que se perdeu, e o que não.** O questionário e a sua tabela de participantes.
Nenhuma resposta e nenhum envio: a bateria tinha desfeito tudo o que plantara, e o
modo real não estava ligado. A base central ficou intacta — 500 pessoas, nenhuma
recusa —, e é ela a memória persistente do mecanismo (ADR-0007).

**A recuperação.** O caminho de R01.1, sem `--substituir`: implantar, preparar,
importar e ativar. Trilha nº 16: 500 participantes criados, as 500 pessoas
**reencontradas** na base central, nenhuma criada. As conferências de leitura
voltaram a 9/9, 8/8, 4/4, 2/2 e 2/2, e a bateria que exercita foi rodada de novo
sobre o instrumento recriado (seção 3, tabela).

**A correção.** `confere-envio.py` deixou de apagar questionário que não criou: só
remove o seu, no fim. Rodada de novo depois da correção, deu 7 de 7, e o 202615
continuou ativo, com os 500. E ela e `scripts/verifica_correio.py` passaram a
**recusar rodar com a rotina em modo real**: as duas esvaziam as caixas do correio
no começo, e no período da simulação as caixas são evidência — convites entregues,
devoluções ainda não lidas, respostas ao remetente.

**O que o incidente mostrou sobre a trilha (VC2).** A trilha da plataforma
(`AuditLog`) registra mudanças em participante, base central e usuário, mas **não
registra criação nem remoção de questionário**: a remoção do 202615 não deixou
linha alguma. A remoção de um instrumento inteiro passa sem rastro na trilha.

## 4. A operação de reparo de contato

Decisão do orientando na E21, implementada aqui porque o cenário de contato inválido
a exige: **trocar o e-mail principal pelo alternativo**, no participante do
questionário pela API e na base central por console — o contato da base central é
cifrado, e só se decifra com os modelos da plataforma, dentro do contêiner (E17).

```bash
python3 reparo-contato.py --fila                           # infra$: a fila de correção
python3 reparo-contato.py --identificador SIN-000123       # infra$: repara
python3 reparo-contato.py --identificador SIN-000123 --simular
```

| Onde | O que muda | Por quê |
|---|---|---|
| base central (comando `repararcontato`) | o principal passa a ser o alternativo; o alternativo fica vazio; os `*_origem` **não** mudam | o endereço que devolveu não volta a ser via de reparo; e, com a origem intacta, a correção sobrevive à reimportação do mesmo arquivo, pela precedência da E17 |
| participante do questionário (API) | e-mail novo, entrega `OK`, `sent = N`, contagem de lembretes zerada | volta a `pendente`, e a rotina o reconvida no próximo disparo, com nova contagem (P4, seção 6.1) |

**Recusa, sem gravar nada:** participante sem contato inválido; que já respondeu
(continua respondente); com reconvite já feito no ciclo — o teto de uma rodada
(P4, seção 6.1); e, na base central, pessoa com recusa de contato, sem alternativo
ou com alternativo igual ao principal. O teto fica, portanto, em **dois lugares**:
a operação recusa a segunda rodada, e a rotina não reconvida pela segunda vez
(`confere-rotina.py --agendada`, caso N).

**Ordem:** a base central primeiro. Se a gravação no questionário falhar depois, a
reimportação seguinte leva o contato novo ao participante, mas não o devolve a
`pendente` — a operação avisa e manda repetir.

**Não é automática.** O reparo pelo alternativo dispensa julgamento humano (E11),
mas grava na base central por console, que só o hospedeiro alcança — e o contêiner
`rotinas` não tem acesso ao Docker, de propósito. No ensaio, roda-se à mão sobre a
fila; agendá-lo no hospedeiro é decisão de implantação (E30).

## 5. O respondente, por HTTP

[`infra/cenarios.py`](../../infra/cenarios.py) responde o questionário como um
navegador sem JavaScript, página a página, a partir do endereço individual — o
caminho das conferências da E21 e da E22. Faz, de propósito, o que o script da
página faria: os campos de relevância das perguntas que aparecem ou somem na mesma
página, sem os quais a plataforma descarta a resposta em silêncio (E21).

```bash
python3 cenarios.py candidatos --nivel tecnico --n 3     # infra$: convidados livres
python3 cenarios.py caminho C3 --identificador SIN-…     # infra$: um dos dez caminhos
python3 cenarios.py volta-con2 --identificador SIN-…     # infra$: um cenário
python3 cenarios.py lista
```

**O que ele verifica, e o que não.** Os blocos que a **plataforma serve** — a
página seguinte é decidida no servidor, pelas regras de grupo — e o que ela
**grava**. A exibição dinâmica dentro da página é do navegador, e é verificada no
navegador (R04.3, R05.1, R12). Cada execução imprime os blocos servidos, os blocos
gravados, os campos por código e o estado que a rotina lê — sem nome, endereço nem
token; o texto livre aparece como "(texto)".

**Testado no 202615 antes do modo real**, com participantes não convidados e limpeza
ao fim (respostas apagadas, participantes restaurados, recusas e higienizações do
teste removidas). Os blocos servidos foram os da seção 5 de
`navegacao-condicional.md` em C1, C3 e C6, e os cenários de voltar, parcial,
reabertura, correção, CT4 e recusa pela mensagem fizeram o que a matriz espera. Dois
defeitos do próprio script foram achados assim e corrigidos: ele lia o bloco da
página pelas perguntas, e a página 2 traz também o campo de relevância de CON1, que
a regra do grupo cita — o bloco passou a sair do marcador de grupo
(`relevanceG<n>`); e o cenário de voltar mudando a situação parava em EF, e não em
SA.

## 6. No navegador (R04.3, R04.8, R05.1, R12)

Em 09/10/2026, numa **cópia de ensaio** (mesmo `.lss`, outro sid, removida ao fim),
no navegador do aplicativo, em emulação de celular — decisão do orientando: a
diferença para o aparelho real fica como ressalva. Os participantes da cópia não têm
atributos, e por isso a identificação abre vazia e foi escolhida na tela; o
pré-preenchimento é de R03, no 202615. As medidas foram tiradas por script na
própria página; as respostas, dadas tocando os rótulos.

**Os sete critérios da seção 15 da matriz, página a página:**

| Página | 375×812 | 360×640 | 812×375 (paisagem) |
|---|---|---|---|
| 1 Consentimento | atende | atende | atende |
| 2 Identificação | atende | atende | atende |
| 3 Bloco I | atende | atende | — |
| 4 Bloco II | atende | atende | — |
| 5 Bloco III | atende | atende | — |
| 6 Bloco IV | atende | atende | — |
| 7 Bloco V | atende | atende | atende |
| 7 Bloco VI | atende | atende | — |
| 8 Bloco VII | atende | atende | — |
| 9 Equidade | atende | atende | — |
| 10 Contato | atende | atende | — |
| encerramento (concluiu, recusou o termo, recusou contato) | atende | atende | — |
| salvar e carregar | atende | — | — |

Em nenhuma houve rolagem horizontal; todas declaram `width=device-width` sem
impedir a ampliação. **O alvo de toque** das opções tem 20 px de altura — abaixo
dos 24 do critério 2.5.8 da WCAG 2.2 —, mas os centros de opções vizinhas estão a
50 px, e o critério admite o alvo menor quando o círculo de 24 px em volta dele não
encosta em outro alvo (exceção de espaçamento). Os campos de texto têm 44 px; os
botões, de 38 a 54.

**R04.3 — as regras na mesma página, pelo toque:** CON2 some com a recusa e volta
com "Concordo"; IDA2 acompanha o curso (Técnico, Graduação, Pós-graduação) sem
envio; AP2 só com AP1 = Sim; SA2 só com "Trabalhando" ou "Estudando e trabalhando";
EF2 e EF3 somem com EF1 = Não. As cinco da seção 3.2 de `navegacao-condicional.md`.

**R04.8 no celular:** com e-mail fora de `.test` em CT1 e telefone de código de área
em uso em CT3, a página não avançou, e a mensagem apareceu junto aos campos.

**R05.1 e R12.2 — salvar e retomar no celular.** "Retomar mais tarde" fica no menu
recolhido do tema, e aparece (248×36 px) ao tocar no botão do menu. Salvo no Bloco
V, sem e-mail: `lime_saved_control` com o nome, a senha em **hash bcrypt**, o passo 7
e IP vazio. Em sessão nova, "Carregar questionário não finalizado", pelo mesmo
menu: voltou ao Bloco V com as seis respostas marcadas. A conclusão foi para **a
mesma** resposta, e a plataforma apagou o registro de salvamento. As duas aberturas
do endereço sem carregar deixaram parciais vazias (`lastpage 0`) — as órfãs da seção
7.3 de `navegacao-condicional.md`.

**R12.3 — fora do questionário.** A página de confirmação da recusa, aberta e
**não confirmada**, está em português e é utilizável a 360 — inclusive a variante
**global**, a do 202615, que é a que o egresso vê pelo endereço da mensagem; abri-la
não registrou nada. A página de código de acesso também é utilizável.

**Achados, que não são do tamanho da tela:**

1. **Frases em inglês** em três páginas fora do questionário: "Fields marked with *
   are mandatory." na página do código de acesso; "Fields marked with an asterisk (*)
   are mandatory." nos formulários de salvar e carregar; e o rótulo "Your email
   address" no de salvar. É o mesmo tipo de lacuna da tradução pt-BR que a E23
   corrigiu na página de recusa. R12.3 pede páginas "em português": **não atende**
   como está, e a correção — acrescentar as traduções na imagem, como na seção 4.1 do
   `Dockerfile` — é da E27.
2. **O botão do menu recolhido não tem nome acessível** — nem texto, nem
   `aria-label`. Quem usa leitor de tela não sabe que é ali que estão "Retomar mais
   tarde" e "Carregar questionário não finalizado". Não é um dos sete critérios, mas
   é barreira real, e fica registrada.
3. **"Você completou 0% deste questionário"** aparece nos formulários de salvar e de
   carregar, no meio do preenchimento. Cosmético.

### 6.1 Achado de ambiente: um IP para todos os respondentes

Depois dos testes de código inexistente (R02.3, e a página de acesso no navegador),
a plataforma passou a responder, a **qualquer** participante, "Você excedeu o número
máximo de tentativas de acesso". O registro `lime_failed_login_attempts` mostra por
quê: as três tentativas falhas foram atribuídas ao IP **172.20.0.1** — o gateway da
rede da composição. Pela porta publicada do Docker, a instância não vê o endereço de
quem acessa: vê todos os acessos vindos do mesmo IP.

A proteção da plataforma bloqueia o IP por 10 minutos depois de 3 códigos inválidos
(`maxLoginAttemptParticipants` e `timeOutParticipants`, padrões de
`config-defaults.php`). **Com um IP só, três códigos digitados errado, por quem quer
que seja, bloqueiam o acesso de todos os egressos por 10 minutos** — e alguém de má
fé pode repetir isso indefinidamente. No ensaio, o efeito é só atrasar os cenários.
Numa implantação, é indisponibilidade. A correção é de ambiente: um proxy reverso que
passe o IP de origem, e a plataforma configurada para confiar nele — ponto da E30. O
registro de IP da resposta está desligado (E15), e continua: o que importa aqui é o
IP de quem tenta o código, não o de quem responde.

## 7. Os cenários, a partir do primeiro disparo real

O modo real é ligado depois da abertura e antes do primeiro disparo agendado, o de
**13/10/2026, às 10:00** (seção 8). Os cenários usam participantes
convidados nesse dia, com principal em `egressos.test` e endereço não compartilhado
(`cenarios.py candidatos`); quem não for usado num cenário é a coorte da ausência de
resposta. Os identificadores escolhidos ficam registrados aqui, com o resultado.

| Cenário do projeto | O que se faz | Itens |
|---|---|---|
| preenchimento parcial com retomada | `parcial` (interrompe depois do Bloco II), `reabre` (página 1 de novo, sem carregar), `parcial-sensivel`; o lembrete de retomada no dia 19/10 | R05.2, R05.3, R05.4, R05.5 |
| ausência de resposta ao longo de sucessivos disparos | a coorte que não responde: convite em 13/10, lembretes em 19, 22 e 27/10, nada depois; C-06 e C-07 | R06.3, R07.5 |
| contato inválido | automático: 23 permanentes e 12 temporários na primeira leitura de devoluções; reparo dos reparáveis com `reparo-contato.py`; reconvite no dia útil seguinte; teto | R10.3, R10.4, R10.5, R10.6, R01.3 |
| recusa | `caminho C2` (tela), `ct4` (conclusão), `recusa-mensagem` (endereço da mensagem recebida), `caminho C1` (termo); revogação pedida por resposta à caixa `acompanhamento` e feita por `conformidade.py revogar`; C-08 | R09.3–R09.7, R01.4 |
| os dez caminhos e o voltar | `caminho C1`…`C10`, `volta-situacao`, `volta-recusa`, `volta-con2`, `correcao-graduacao`, `correcao-pos` | R04.2, R04.4–R04.7, R03.2, R03.4, R03.5, R08.3–R08.5 |

**O que já se sabe que vai acontecer**, e o que se vai observar:

- a primeira leitura de devoluções depois das 10:00 marca os 23 de `invalido.test`;
- os 12 de `indisponivel.test` devolvem o aviso de atraso em cerca de 1 minuto, e a
  falha final quando a fila expira, em 1 hora. Quantas devoluções temporárias cada
  mensagem produz decide o risco de R10.4 (matriz, seção 13). Uma primeira
  observação é possível antes disso, com as mensagens de teste da abertura que
  ficaram na fila (seção 8).

## 8. Estado ao fim de 09/10/2026

**Feito:** a abertura inteira (seção 3), a recuperação do incidente, o navegador
(seção 6) e R04.8. O 202615 está ativo, com os 500 participantes, nenhuma resposta,
nenhum envio, nenhuma recusa; a rotina, ainda em **modo simulado**.

**Pendente, antes de terça, 13/10, às 10:00:**

1. **Ler a devolução de expiração da fila.** Três mensagens de teste a
   `indisponivel.test` ficaram na fila do correio (dos dois `confere-envio.py` e do
   `verifica_correio.py`), com expiração em 1 hora. A leitura em modo de simulação
   (`ler_devolucoes.py --simular`, que não consome a caixa) mostra com que código e
   ação vem a falha final — e, com isso, se cada mensagem gera uma ou duas devoluções
   temporárias. Até aqui só se viu o aviso de atraso: **um por mensagem**, `4.4.1`,
   `delayed`.
2. **Limpar das caixas os resíduos de teste.** A rotina de devoluções, em modo real,
   registraria essas devoluções no ciclo 2026, com `token` nulo; C-09 já as exclui,
   mas a E28 não precisa delas.
3. **Ligar o modo real:** `ROTINA_DISPARO=real` no `.env`, `docker compose up -d
   rotinas`, e conferir pelo `disparar.py --simular` o plano de 255 convites.

**O hospedeiro precisa estar ligado às 10:00** de 13, 19, 22 e 27/10.
