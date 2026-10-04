# Unicidade e deduplicação dos participantes

**Etapa:** E19 — validar unicidade e deduplicação
**Data:** 04/10/2026
**Decorre de:** [`leiaute-entrada.md`](leiaute-entrada.md), seções 4.1 e 5 (E11);
base sintética da E16; [`importacao-base.md`](importacao-base.md) (E17);
[`pre-preenchimento.md`](pre-preenchimento.md) (E18)

Registro da verificação de integridade da base de participantes: tokens,
identificadores, o elo entre o questionário e a base central, e o sintoma de pessoa
duplicada.

## 1. Objeto e decisão

**Objeto.** O questionário 202615, ativo, com 500 participantes, e a base central de
participantes, com as mesmas 500 pessoas — o estado deixado pela E18.

**Decisão tomada** (confirmada com o orientando antes da execução): **e-mail
principal compartilhado por identificadores distintos é alerta para revisão humana,
e o mecanismo não funde pessoas.** O compartilhamento é sintoma de pessoa duplicada,
mas também existe de verdade — a mesma caixa de família, um endereço institucional
—, e a fusão automática juntaria duas pessoas reais quando errasse. É coerente com o
leiaute, que aceita o registro com alerta (seção 5). A lista sai pelos
identificadores, sem nome nem endereço.

## 2. Onde a duplicidade é barrada antes de chegar aqui

A verificação confirma propriedades que o desenho já impõe por construção:

| Duplicidade | Barrada por | Desde |
|---|---|---|
| identificador repetido no arquivo | validador: **todos** os registros com o identificador repetido são rejeitados, sem distinguir maiúsculas | E17 (`valida_entrada.py`) |
| a mesma pessoa duas vezes na base central | `participant_id` derivado do identificador (UUID v5): o mesmo identificador cai sempre na mesma pessoa | E17 |
| a mesma pessoa duas vezes no questionário | a importação acha o participante pelo `participant_id` e o atualiza, em vez de criar outro | E17 |
| token repetido | a plataforma valida a unicidade ao gerar, e tenta de novo | plataforma (`Token::generateToken`) |

A E19 não confia em nenhuma dessas barreiras: confere o resultado.

## 3. O que é "token inválido"

O critério pede que nenhum token repetido ou **inválido** seja encontrado. Três
sentidos, todos verificados:

1. **o da plataforma** — conferido no código (`Token::summary`): o contador
   `token_invalid` do resumo da API conta participantes com token **nulo ou vazio**.
   É, portanto, participante sem endereço individual, e **não** estado de entrega.
   Isso fecha o ponto que a E08 deixou aberto, quando se observou que marcar
   `emailstatus = 'invalid'` não movia o contador;
2. **forma** — o comprimento configurado no questionário (15) e só caracteres
   alfanuméricos, que é o que o gerador da plataforma produz;
3. **confusão** — dois tokens que só diferem nas maiúsculas seriam confundidos por
   quem os digita; e um token igual a um identificador anularia a separação que o
   leiaute exige entre o código da instituição e o endereço não adivinhável (C1).

## 4. A conferência

`infra/confere-participantes.py`, só de leitura, versionada como as conferências
anteriores e reexecutável depois de cada importação:

| # | Confere |
|---|---|
| 1 | todo participante tem token — `token_invalid` da plataforma igual a zero |
| 2 | todo token com o comprimento configurado e só caracteres alfanuméricos |
| 3 | nenhum token repetido, nem sem distinguir maiúsculas |
| 4 | todo participante tem identificador, e nenhum se repete, sem distinguir maiúsculas |
| 5 | nenhum identificador igual a um token |
| 6 | o elo: `participant_id` único no questionário, presente na base central e igual ao UUID v5 do identificador — a regra da E17, recalculada aqui, e não importada do importador |
| 7 | a base central: identificador único, `participant_id` derivado dele, e toda pessoa sem recusa com participante no questionário |
| 8 | o e-mail principal compartilhado forma os **mesmos grupos de pessoas** no questionário, onde está em claro, e na base central, onde a cifragem determinística permite comparar sem decifrar |

E lista, como alerta, os grupos de e-mail compartilhado pelos identificadores.

```bash
cd infra
python3 confere-participantes.py
```

## 5. Resultado

```
Questionario 202615: 500 participantes; base central: 500 pessoas.
[OK] 1 a 8 — 8 de 8
ALERTA para revisao humana — e-mail principal compartilhado: 3 grupo(s)
  SIN-000230 · SIN-000461
  SIN-000267 · SIN-000354
  SIN-000345 · SIN-000408
Criterio da E19 (nenhum token repetido ou invalido): atendido
```

- **Critério atendido**: nenhum token vazio, fora da forma, repetido — nem na caixa
  — ou igual a identificador.
- **Os três grupos são exatamente os três pares plantados pela E16** — recalculados
  do arquivo que o gerador produz, que é determinístico: nenhum a mais, nenhum a
  menos.
- **Os grupos são os mesmos no questionário e na base central**: a base central,
  onde o e-mail está cifrado, e o questionário, onde está em claro, contam a mesma
  história.

### 5.1 A conferência foi testada

Quinze defeitos, plantados um por vez numa cópia em memória dos dados reais — sem
tocar o banco —, e **os quinze reprovados** pela conferência certa: token vazio,
nulo, curto, com caractere estranho, repetido e repetido só na caixa; identificador
repetido com outra caixa, ausente e igual a um token; `participant_id` órfão e
repetido; pessoa da base central fora do questionário; identificador repetido na
base central; um quarto par compartilhado só no questionário; e um par compartilhado
só na base central. As reprovações em cascata são as esperadas — alterar o
identificador também quebra a derivação do `participant_id`.

## 6. O que esta verificação não permite afirmar

1. **Duplicidade de pessoa sob identificadores e endereços distintos não é
   detectável aqui.** O e-mail compartilhado é o único sintoma que o leiaute oferece;
   a mesma pessoa com dois identificadores e dois endereços passa. Detectá-la exigiria
   comparar nomes, e o leiaute não carrega dado para isso de forma confiável — nem
   deve: seria heurística sobre dado pessoal.
2. **A comparação na base central é por igualdade exata do cifrado.** Dois endereços
   que só diferem na caixa da parte local cifram diferente; no questionário, a
   comparação ignora a caixa. Na base atual não há caso assim, e o validador já
   normaliza o domínio.
3. **A estabilidade do identificador entre extrações** segue sendo requisito da
   origem (leiaute, seção 9).
4. **Nada aqui envolveu dado de pessoa real.**

## 7. O que esta etapa determina para as etapas seguintes

- **E21 (rotina)** — a rotina de convites pode rodar a conferência antes de cada
  disparo: dispara só se as conferências 1 a 7 passarem.
- **E23 (conformidade)** — a revisão humana dos grupos de e-mail compartilhado é
  procedimento a descrever: quem revisa, e o que fazer quando são, de fato, a mesma
  pessoa — o que se resolve na origem, e não no mecanismo.
- **E25 (matriz)** — o requisito de unicidade tem procedimento pronto: a
  conferência, mais os quinze defeitos do teste de mutação como casos negativos.
- **E28 (extração)** — os grupos de e-mail compartilhado são candidatos a pessoa
  duplicada; não devem ser fundidos na extração.
