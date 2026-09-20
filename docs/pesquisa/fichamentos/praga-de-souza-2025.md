# PRAGA DE SOUZA, COUTO ASSIS e DE SOUZA COSTA (2025) — Plataforma RAEG

**Referência:** PRAGA DE SOUZA, O.; COUTO ASSIS, G.; DE SOUZA COSTA, E. Plataforma
RAEG – ferramenta de registro e acompanhamento de egressos da educação profissional
e tecnológica. Educação Profissional e Tecnológica em Revista, v. 8, n. Especial,
p. 80-95, 2025.
**Tipo:** artigo científico (relato de produto educacional)
**Acesso:** https://revistas.ifes.edu.br/index.php/ept/article/view/3134 · consultado em 20/09/2026
**Alimenta:** E04, E11, E17, E18, E23, E30, E31

## Problema identificado

O acompanhamento de egressos da EPT é reconhecido como necessário, mas os gestores
o tratam como ação de médio a longo prazo, que exige planejamento, recursos e
pessoal de que as instituições em geral não dispõem. A pesquisa de campo que
originou o produto identificou, junto a coordenadores de curso e diretores, quatro
obstáculos concretos: excesso de encargos acadêmicos e administrativos, número
insuficiente de servidores de apoio, dificuldade de acesso aos dados dos egressos
e desatualização cadastral de telefones e e-mails.

## Método

Produto educacional de mestrado do ProfEPT, no CEFET-MG campus Divinópolis,
desenvolvido em parceria com projeto de iniciação científica e fomento da FAPEMIG.
A plataforma foi projetada a partir de pesquisa de campo com gestores da Rede EPT.
O artigo descreve construção, características e funcionalidades.

**Arquitetura funcional.** Acesso por navegador, com e-mail e senha; dois perfis,
administrador (responsável pela instalação e hospedagem) e usuário final. As abas
centrais são "QUESTÕES", onde o gestor monta o rol de perguntas escolhendo entre
abertas e de múltipla escolha, e "DESTINATÁRIOS", onde insere os participantes
**individualmente ou em lote, por importação de planilha eletrônica** em esquema
definido.

Código-fonte, manual de instalação e manual de uso estão publicados no eduCAPES.

## Resultado

A plataforma reúne, em uma ferramenta, funções que antes exigiam editor de
formulários, servidor de e-mail e planilha — objetivo declarado como "permitir um
trabalho em bloco, evitando a necessidade de abordagens individuais".

Duas decisões de projeto merecem destaque, ambas motivadas por proteção de dados:

1. **A plataforma não mantém, por padrão, banco de dados de participantes fixo** —
   escolha declarada como sendo "pensando na segurança dos dados dos participantes".
2. O envio dos formulários é feito **sem cópias**, para resguardar os dados dos
   destinatários.

## Implicação para o projeto

**1. Formula com clareza a tensão que este projeto precisa resolver.** O RAEG
optou por *não* manter base persistente de participantes, em nome da minimização de
dados. Este projeto opta pelo contrário: a tabela de participantes persistente é
justamente o que viabiliza saber quem não respondeu e cobrar de forma dirigida.
São escolhas legítimas e opostas diante do mesmo princípio da necessidade.

O projeto precisa sustentar a sua, e tem como: a base persistente é a condição da
rastreabilidade, e o risco que ela cria é endereçado por consentimento registrado
(E22), anonimização e trilha de auditoria (E23). A alternativa do RAEG compra
segurança ao preço de perder a série histórica e a cobrança dirigida — exatamente o
que os gestores entrevistados por eles pediram. Vale registrar esta tensão de forma
explícita no relatório final e, preferencialmente, em ADR: é uma decisão de
arquitetura com fundamento em princípio legal, e há literatura tomando o caminho
oposto.

**2. Sustenta o pré-preenchimento com evidência de campo.** Os coordenadores
entrevistados registraram que o contato com o egresso não deve ser custoso nem
desestimulante, e que "o uso de questões redundantes e perguntas com dados que já
estão no banco de dados precisam ser evitadas". Essa é a justificativa direta da
E18, vinda de gestores reais e não de suposição de projeto.

**3. Confirma a desatualização cadastral como obstáculo de primeira ordem.** Vale
para a E05, que precisa definir o tratamento de contato inválido, e para a E11, que
precisa prever no leiaute de entrada mais de uma via de contato.

**4. Importação em lote por planilha** é o mesmo desenho previsto para E11 e E17,
o que reforça que o formato é prática corrente e não invenção deste trabalho.

**5. Precedente de replicabilidade.** Publicar código, manual de instalação e
manual de uso em repositório aberto é o padrão que a E30 persegue. Serve de
referência de escopo para o guia de replicação.

## Limitações da fonte

- **Não há avaliação de uso.** O artigo descreve construção e funcionalidades. Não
  reporta aplicação em coleta real, número de instituições que adotaram, volume de
  respostas nem taxa de resposta. Nada nele permite afirmar efeito sobre a
  participação de egressos.
- **A pesquisa de campo é de requisitos, não de resultado.** As entrevistas com
  coordenadores informaram o que a ferramenta deveria ter; não avaliam o que ela
  entregou.
- **O artigo não detalha o tratamento de dados.** Registra as duas decisões de
  segurança citadas, mas não trata de base legal, consentimento, retenção ou
  anonimização das respostas — a mesma lacuna observada na maioria das fontes
  institucionais deste conjunto.
- **Divergência de autoria entre o PDF e a página do periódico.** O PDF traz dois
  autores (Praga de Souza e Costa); a página do periódico lista três, incluindo
  Couto Assis. Adotou-se aqui a citação oficial da página. Conferir antes da
  entrega.
