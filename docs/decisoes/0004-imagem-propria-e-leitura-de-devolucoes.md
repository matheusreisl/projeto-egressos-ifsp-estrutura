# ADR-0004 — Imagem própria do LimeSurvey e leitura de devoluções por rotina

**Status:** aceita
**Data:** 21/09/2026
**Etapa de origem:** E07 — provisionar o ambiente escolhido

## Contexto

A [ADR-0002](0002-ambiente-execucao.md) fechou o ambiente em conteinerização
declarativa e deixou expressamente para esta etapa uma decisão: **adotar imagem
comunitária de referência ou construir imagem própria a partir do código
oficial**, com fixação por digest em qualquer dos casos.

Duas constatações desta etapa moldaram a decisão.

**A primeira, já antecipada na ADR-0002 e agora confirmada:** o projeto LimeSurvey
**não publica imagem de contêiner**. As de uso corrente — `martialblog/limesurvey`,
`acspri/limesurvey`, `adamzammit/limesurvey`, entre outras — são mantidas por
terceiros, sem vínculo com o projeto.

**A segunda apareceu durante o provisionamento e não estava prevista.** O manual
do LimeSurvey registra que a extensão `imap` do PHP é *"needed for the email bounce
tracking system"* — isto é, é o caminho nativo para ler devoluções de e-mail, que é
exatamente o que o parâmetro **P8** da E05 exige e o que a **E09** precisa
verificar. Ocorre que essa extensão **não se constrói mais sobre a base atual**:

- a biblioteca UW-IMAP (`libc-client`), da qual ela depende, **foi removida do
  Debian** por falta de manutenção — verificado: ausente no Debian 13 (trixie),
  presente no Debian 12 (bookworm) como `libc-client2007e-dev`;
- a própria extensão **saiu do núcleo do PHP na versão 8.4**.

Registra-se ainda um achado com efeito sobre a versão a adotar: **a linha 6.x LTS
do LimeSurvey encerrou o suporte em 31/08/2026**. A linha 7.x é a única suportada.

## Alternativas avaliadas

### Quanto à imagem

| Alternativa | Prós | Contras |
|---|---|---|
| Imagem comunitária de referência, fixada por digest | mantida, com integração contínua, variantes e exemplos prontos; menos trabalho e menor risco de erro sutil de configuração | dependência de mantenedor terceiro; a instalação vira caixa-preta e a E10 teria de documentar por fora o que a imagem faz por dentro |
| **Imagem própria, do código oficial** | o Dockerfile **é** o procedimento de instalação, que é o entregável da E10; cadeia de confiança sem intermediário; sem dependência de terceiro | mais trabalho; a manutenção das extensões do PHP passa a ser do projeto |

### Quanto à leitura de devoluções

| Alternativa | Prós | Contras |
|---|---|---|
| Base Debian 12 com `imap`, usando o recurso nativo | destrava o recurso imediatamente; poupa código agora | prende o projeto a base *oldstable* para obter extensão depreciada cuja biblioteca o Debian já removeu; quem replicar em 2027 encontra o caminho fechado |
| **Base atual sem `imap`, com rotina própria** | sem dependência em retirada; a classificação fica explícita e testável; mesma via da E28 | mais código do projeto, que precisa existir antes de a E09 fechar |

## Decisão

**1.** A instância roda em **imagem própria**, construída a partir do **pacote
oficial** do LimeSurvey, fixado por versão **e por soma de verificação SHA-256**,
sobre `php:8.3-apache` fixada por digest. Versão adotada: **7.2.0+260921**.

**2.** A imagem **não inclui a extensão `imap`**. A leitura e a classificação de
devoluções previstas em P8 são feitas por **rotina própria**, fora do recurso
nativo do LimeSurvey.

## Justificativa

**Sobre a imagem — o argumento que decide é de economia de artefato.** O entregável
da E10 é o procedimento de instalação documentado. Com imagem própria, o Dockerfile
*é* esse procedimento: executável, versionado, conferível e impossível de divergir
da instalação real, porque é a instalação real. Com imagem comunitária, haveria dois
artefatos — a imagem que faz e o texto que descreve o que ela faz — e o segundo
começaria a envelhecer no dia seguinte.

Some-se a isso a coerência com a própria ADR-0002, que descartou camadas gratuitas
de nuvem porque **um guia de replicação ancorado em oferta de terceiro tem prazo de
validade que não depende de quem o escreveu**. O argumento vale igual para imagem
mantida por terceiro. Recusar a nuvem por esse motivo e aceitar a imagem pelo
mesmo risco seria incongruente.

**Sobre as devoluções — o recurso nativo resolveria menos do que parece.** As regras
do P8 são do projeto, não da plataforma: erro permanente marca o contato como
inválido **na primeira** ocorrência; erro temporário só na **terceira** do mesmo
ciclo; o resultado abre **fila de correção**; e `contato inválido` **não é recusa**,
distinção que a E05, seção 10.2, estabeleceu com efeitos opostos entre ciclos. O
tratamento nativo marca o token como devolvido e não implementa nada disso. **A
lógica de classificação teria de ser escrita de qualquer modo** — o nativo pouparia
apenas o trecho que busca a mensagem na caixa e a analisa, que é a parte simples.

Trocar isso por uma base *oldstable* e uma extensão em retirada seria pagar caro
por pouco. E pagaria justamente na moeda que este projeto não pode gastar: a
replicabilidade futura do guia.

**Há ainda uma sinergia que não é acessória.** A E28 já prevê rotina de extração em
Python contra a API do LimeSurvey. A rotina de devoluções usa a mesma linguagem, a
mesma via de acesso e a mesma forma de teste. São duas rotinas irmãs, não duas
tecnologias.

## Consequências

### Passa a ser verdade

- **O Dockerfile em `infra/limesurvey/` é artefato de entrega**, e parte do que a
  E10 documenta. Alterá-lo é alterar o procedimento de instalação.
- **Atualizar o LimeSurvey é uma operação declarada**: trocar três argumentos de
  construção e recalcular a soma de verificação, conforme `infra/README.md`. Não há
  atualização implícita por rótulo móvel.
- **A conferência da soma acontece antes da descompactação.** Pacote que não confere
  interrompe a construção, de propósito.
- **A versão do PHP fica em 8.3** enquanto a decisão valer, e a escolha passa a ter
  motivo registrado em vez de ser herdada por acaso.

### Esta decisão custa

- **A E09 ganha escopo:** a rotina de leitura e classificação de devoluções passa a
  ser requisito dela, e precisa existir antes que ela feche. O serviço de correio
  precisa, em consequência, expor caixa legível por essa rotina.
- **A manutenção das extensões do PHP é do projeto.** Numa implantação real isso
  implica rotina de atualização — ponto a constar do guia (E30), já que aqui o
  ambiente é fechado e o modelo de ameaça, mínimo.
- **Não se poderá afirmar que o mecanismo usa o rastreamento nativo de devoluções
  do LimeSurvey.** Ele não usa. Enunciar assim na E31, sem arredondamento, na mesma
  linha da conformidade parcial já declarada na ADR-0003.

### O que fica pendente de verificação

- **A URL oficial do pacote da linha 7.x está sob o caminho `latest-master`.** Foi
  a via que a página oficial de descarga apresenta como versão corrente, e não uma
  compilação de desenvolvimento — mas o nome é enganoso e merece confirmação na
  E08, ao registrar a versão da instância.
- **A E08 confere as capacidades C1 a C10** contra a instância viva, como já
  determinado pela ADR-0002. Esta decisão não antecipa nenhuma delas.

## Revisão

Decisão revisável em duas hipóteses:

1. **O projeto LimeSurvey passa a publicar imagem oficial.** Some o argumento
   principal contra a imagem de terceiro, porque deixaria de ser de terceiro.
2. **Surge caminho mantido para leitura de devoluções dentro da plataforma.** Ainda
   assim, a classificação do P8 continuaria sendo do projeto — o que mudaria é
   apenas de onde a mensagem é lida.
