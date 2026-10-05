# ADR-0009 — Registro do consentimento na própria resposta, com o termo arquivado por versão

**Status:** aceita
**Data:** 05/10/2026
**Etapa de origem:** E22 — implementar o consentimento eletrônico

## Contexto

O critério da E22 é o aceite **persistido e recuperável**, com data e versão do
termo. A exigência vem da LGPD: o ônus de provar que o consentimento foi obtido é do
controlador (art. 8º, §2º), e prova, aqui, significa poder dizer, para cada pessoa,
**o que ela escolheu, quando e diante de que texto**. A E13 havia fixado que data,
hora e versão são metadados registrados pela plataforma, e não campos que o
respondente preenche.

O que a plataforma oferece, conferido na instância e no código:

- o **aviso de política nativo** é uma caixa de aceite só: não tem versão, não tem as
  duas recusas da P6 nem o consentimento específico do art. 11;
- a **data de início da resposta** é a da abertura do endereço, e não a do aceite
  (E20); a da última ação muda a cada página;
- a **equação** é recalculada no servidor a cada envio da página, oculta ou não, e
  gravada na resposta; no modo de uma página por vez, o envio de outra página não
  recalcula as da página 1;
- a **estrutura de questionário ativo não muda**: acrescentar questão a ele é
  recusado.

## Alternativas avaliadas

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Equações ocultas na página 1 (versão e momento), com o texto de cada versão arquivado e resumido** | o registro nasce na própria resposta, no mesmo envio da manifestação; sobrevive à recusa, que descarta o resto; o resumo prova o texto sem guardá-lo em cada resposta | exige recriar o instrumento ativo; a versão precisa de disciplina — texto novo, versão nova |
| Aviso de política nativo | nenhum código | sem versão, sem as recusas, sem o consentimento específico |
| Datas da resposta como data do aceite, e versão presumida pela data | sem mudar a estrutura | a data é a da abertura, e não a do aceite; versão presumida não é prova |
| Tabela própria, preenchida pela rotina ao ver a resposta | esquema sob controle do projeto | o momento seria o da leitura, e não o da manifestação; segunda fonte de verdade ao lado da resposta |
| Plugin que grave no evento de envio da página | momento exato | código PHP próprio dentro da plataforma, com instalação pela interface (o problema da E08 com o AuditLog) |

## Decisão

1. **Duas equações ocultas na página 1, sempre relevantes:** `CONV` grava a versão e
   o resumo SHA-256 do documento da página 1; `CONDH` grava o momento da manifestação
   em ISO 8601, com o deslocamento.
2. **O documento da página 1 de cada versão fica arquivado**, imutável, em
   `infra/instrumento/termos/<versão>.html`. O gerador recusa a mesma versão com
   texto diferente.
3. **A recuperação lê a exportação da própria plataforma**, e confere o texto
   arquivado pelo resumo gravado.
4. **Recriar instrumento ativo** passa a ser admissível — e só então — quando não há
   resposta alguma nem envio, porque é a única via que a plataforma deixa para mudar
   a estrutura.
5. **O termo é modelo de ensaio**, redigido pelo projeto com os elementos do art. 9º,
   sujeito à validação do encarregado de dados do IFSP. Decisão do orientando.

## Justificativa

O registro tem de nascer com a manifestação, e não ser reconstruído depois. As
equações são calculadas no servidor no mesmo envio que grava CON1, e por isso têm o
momento exato. Só elas, entre as alternativas, cumprem as duas coisas sem código
dentro da plataforma.

O resumo, e não o texto, vai na resposta porque o texto é o mesmo para milhares de
respostas. O arquivo da versão é a prova, e o resumo é o elo verificável entre a
resposta e o arquivo. Um arquivo que pudesse ser reescrito sob a mesma versão não
provaria nada — daí a recusa do gerador e a linha do `.gitattributes`.

## Consequências

**Passa a ser verdade:**

- cada manifestação — aceite ou recusa — guarda CON1, CON2 quando houver, a versão e
  o momento; a recusa os guarda mesmo descartando o resto;
- **mudar o termo exige versão nova.** O caminho verificado para levá-la à instância
  é a reimplantação, que só se admite sem respostas. Texto e equação são propriedades
  da questão, e não estrutura: aplicá-los a instrumento ativo pela API talvez seja
  possível, mas **não foi exercitado**. Se for, um ciclo pode ter duas versões, e
  cada resposta diz qual viu — é para isso que a versão vai na resposta;
- o momento está em **UTC**, com `+00:00` explícito, porque a plataforma roda em UTC;
- os nomes das colunas de resposta (`Q<qid>`) mudam a cada reimplantação: script
  nenhum pode fixá-los.

**Esta decisão impede:**

- reescrever o texto de uma versão já usada. Uma resposta antiga apontaria para um
  texto que ela não viu — e o gerador recusa exatamente isso.

## Revisão

Revisável se a plataforma passar a registrar versão e momento do aceite por conta
própria, ou se a instituição preferir manter o termo fora do questionário, com
aceite registrado em outro sistema.
