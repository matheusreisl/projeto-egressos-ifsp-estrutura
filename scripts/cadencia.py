"""
Cadencia de contato por participante (E21): o estado de cada participante e o
que vence para ele num dado instante.

Logica pura. Nao fala com a plataforma, com o banco nem com o relogio: recebe o
que a plataforma guarda, a agenda e o instante, e devolve o plano. E isso que
permite conferir as regras com casos construidos (infra/confere-rotina.py), sem
esperar dias de calendario — e e o motivo de esta logica nao estar dentro da
rotina que dispara (disparar.py), que so busca os dados e executa o plano.

O que implementa, de docs/especificacao/parametros-contato.md:

  P1  um convite por ciclo, na ancora da turma (secao 7.2)
  P2  ate tres lembretes, so a quem nao concluiu, com o ramo certo (secao 4.1)
  P3  D+4, D+7 e D+14 contados do envio EFETIVO do convite a cada participante,
      e nao de uma data unica do ciclo (secao 5)
  P4  quatro mensagens por ciclo; o reparo de contato abre nova contagem, uma
      vez so (secao 6.1)
  P5  janela de 60 dias; ancoragem na turma; nenhum convite a menos de doze
      meses do anterior (secao 7)
  12  a maquina de estados — calculada, e nao gravada: "nao respondente" nao e
      estado da base, e esta logica nao cria marcacao alguma

O modelo da rotina nativa da plataforma — intervalo minimo desde o ultimo envio
mais numero maximo de lembretes — nao expressa D+n desde o convite quando os
intervalos nao sao uniformes, que e o caso (secao 13.1). Por isso a cadencia e
calculada aqui, e a plataforma so recebe a lista de quem vence
(docs/especificacao/rotina-disparo.md; ADR-0008).

Duas convencoes de data da plataforma, conferidas no codigo do LimeSurvey 7 e
observadas, que esta logica respeita e que enganam, porque nao coincidem:

  sent, remindersent   gravados em UTC (gmdate), na forma AAAA-MM-DD HH:MM
  validuntil           lido no fuso do PHP (America/Sao_Paulo), o da agenda

As datas da resposta (startdate, submitdate) tambem sairam em UTC na E21, mas
esta logica nao as usa: decide pela presenca de submitdate e pelo CON1.
"""

import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

# --- Estados (secao 12 do P5) -----------------------------------------------

PENDENTE = "pendente"
CONVIDADO = "convidado"
EM_PREENCHIMENTO = "em preenchimento"
RESPONDENTE = "respondente"
CONTATO_INVALIDO = "contato inválido"
RECUSA_CONSENTIMENTO = "recusa de consentimento"
RECUSA_CONTATO = "recusa de contato"
EXPIRADO = "expirado"
# Nao e estado da maquina: e inconsistencia a revisar. Participante marcado
# como concluido sem resposta enviada que o explique. Nao recebe nada.
CONCLUIDO_SEM_RESPOSTA = "concluído sem resposta"

ESTADOS = (PENDENTE, CONVIDADO, EM_PREENCHIMENTO, RESPONDENTE,
           CONTATO_INVALIDO, RECUSA_CONSENTIMENTO, RECUSA_CONTATO, EXPIRADO,
           CONCLUIDO_SEM_RESPOSTA)

# "Nao respondente" e o conjunto destes tres (secao 12). So os dois primeiros
# recebem lembrete.
NAO_RESPONDENTES = (CONVIDADO, EM_PREENCHIMENTO, EXPIRADO)
RECEBEM_LEMBRETE = (CONVIDADO, EM_PREENCHIMENTO)

# Codigos de CON1 no instrumento (E13, E15).
CON1_CONCORDO = "CONC"
CON1_RECUSA_CONSENTIMENTO = "RCONS"
CON1_RECUSA_CONTATO = "RCONT"

# Valores do atributo `variante_lembrete` (E20). Sao os de
# infra/instrumento/mensagens.py; a conferencia da rotina confere que coincidem.
VARIANTE_CONVIDADO = "convidado"
VARIANTE_EM_PREENCHIMENTO = "em_preenchimento"

UTC = timezone.utc


class ErroAgenda(Exception):
    pass


# --- Agenda -----------------------------------------------------------------

@dataclass(frozen=True)
class Agenda:
    fuso: ZoneInfo
    lembretes_dias: tuple
    intervalo_minimo_dias: int
    janela_dias: int
    horario: time
    dias_da_semana: frozenset
    feriados: frozenset
    calendario_padrao: dict
    calendario_excecoes: dict
    tolerancia_minutos: int
    devolucoes_intervalo_minutos: int
    reconvites_por_ciclo: int
    meses_entre_convites: int
    lote: int
    avisos: tuple = ()

    def dia_util(self, dia):
        return dia.weekday() in self.dias_da_semana and dia not in self.feriados

    def data_ancora(self, ano, semestre):
        """D0 do ciclo do ano `ano` para quem concluiu no semestre `semestre`:
        o termino desse semestre no calendario (secao 7.2 do P5; leiaute,
        secao 4.5). Uma excecao por ano-semestre prevalece sobre o padrao."""
        chave = f"{ano}-{semestre}"
        if chave in self.calendario_excecoes:
            return self.calendario_excecoes[chave]
        mes, dia = self.calendario_padrao[str(semestre)]
        return date(ano, mes, dia)


def _mes_dia(texto, onde):
    try:
        d = datetime.strptime(texto, "%m-%d")
    except (TypeError, ValueError):
        raise ErroAgenda(f"{onde}: '{texto}' nao e MM-DD")
    return d.month, d.day


def le_agenda(dados):
    """Valida e monta a agenda a partir do dicionario do agenda.json.

    Recusa o que estiver fora da faixa admissivel da secao 5.1 do P3, a menos
    que `registro_fora_da_faixa` aponte o registro proprio que a secao exige
    (ADR, durante o projeto; guia, por instituicao replicante). Nesse caso a
    violacao vira aviso. Erro de estrutura nunca vira aviso.
    """
    erros, faixa = [], []
    try:
        fuso = ZoneInfo(dados["fuso"])
        lembretes = tuple(int(x) for x in dados["lembretes_dias"])
        intervalo = int(dados["intervalo_minimo_dias"])
        janela = int(dados["janela_dias"])
        horario = datetime.strptime(dados["horario"], "%H:%M").time()
        dias = frozenset(int(x) for x in dados["dias_da_semana"])
        feriados = frozenset(date.fromisoformat(x) for x in dados["feriados"])
        cal = dados["calendario"]
        padrao = {s: _mes_dia(cal["padrao"][s], f"calendario.padrao.{s}")
                  for s in ("1", "2")}
        excecoes = {k: date.fromisoformat(v)
                    for k, v in (cal.get("excecoes") or {}).items()}
        tolerancia = int(dados["tolerancia_minutos"])
        devolucoes = int(dados["devolucoes_intervalo_minutos"])
        reconvites = int(dados["reconvites_por_ciclo"])
        meses = int(dados["meses_entre_convites"])
        lote = int(dados["lote"])
    except ErroAgenda:
        raise
    except (KeyError, TypeError, ValueError) as e:
        raise ErroAgenda(f"agenda malformada: {e!r}")

    # Estrutura e limites que nao sao ajuste operacional.
    if not 1 <= len(lembretes) <= 3:
        erros.append("de um a tres lembretes (P2; P4 limita a quatro mensagens)")
    if list(lembretes) != sorted(set(lembretes)):
        erros.append("lembretes_dias precisa ser estritamente crescente")
    if not dias or not dias <= {0, 1, 2, 3, 4}:
        erros.append("dias_da_semana so admite dias uteis, 0 (seg) a 4 (sex)")
    if lembretes and janela <= lembretes[-1]:
        erros.append("a janela precisa exceder o ultimo lembrete (P5)")
    for k in excecoes:
        ano, _, sem = k.partition("-")
        if not (ano.isdigit() and sem in ("1", "2")):
            erros.append(f"calendario.excecoes: chave '{k}' nao e AAAA-S")
    if not 0 <= tolerancia <= 120:
        erros.append("tolerancia_minutos entre 0 e 120")
    if not 5 <= devolucoes <= 1440:
        erros.append("devolucoes_intervalo_minutos entre 5 e 1440")
    if reconvites not in (0, 1):
        erros.append("reconvites_por_ciclo e 0 ou 1: uma rodada de reparo, no "
                     "maximo (secao 6.1)")
    if meses < 12:
        erros.append("meses_entre_convites nao pode ser menor que 12 (secao 7.2)")
    if not 1 <= lote <= 50:
        erros.append("lote entre 1 e 50, o maxemails da plataforma")
    if erros:
        raise ErroAgenda("; ".join(erros))

    # Faixa admissivel da secao 5.1: fora dela e admissivel, com registro.
    if lembretes and not 3 <= lembretes[0] <= 7:
        faixa.append(f"primeiro lembrete em D+{lembretes[0]}, fora de D+3 a D+7")
    if intervalo < 3:
        faixa.append(f"intervalo minimo de {intervalo} dias, abaixo de 3")
    passos = [b - a for a, b in zip((0,) + lembretes, lembretes)]
    if any(p < intervalo for p in passos):
        faixa.append(f"intervalos entre disparos {passos}, algum abaixo do minimo")
    if lembretes and lembretes[-1] > 21:
        faixa.append(f"ultimo lembrete em D+{lembretes[-1]}, depois de D+21")
    registro = dados.get("registro_fora_da_faixa")
    if faixa and not registro:
        raise ErroAgenda("fora da faixa admissivel (secao 5.1 do P3), sem "
                         "registro_fora_da_faixa: " + "; ".join(faixa))
    avisos = tuple(f"{f} — registrado em {registro}" for f in faixa)

    return Agenda(fuso=fuso, lembretes_dias=lembretes,
                  intervalo_minimo_dias=intervalo, janela_dias=janela,
                  horario=horario, dias_da_semana=dias, feriados=feriados,
                  calendario_padrao=padrao, calendario_excecoes=excecoes,
                  tolerancia_minutos=tolerancia,
                  devolucoes_intervalo_minutos=devolucoes,
                  reconvites_por_ciclo=reconvites, meses_entre_convites=meses,
                  lote=lote, avisos=avisos)


def carrega_agenda(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return le_agenda(json.load(fh))


# --- Participante -----------------------------------------------------------

@dataclass
class Resposta:
    submetida: bool
    con1: str = None


@dataclass
class Participante:
    tid: int
    participant_id: str = None
    sent: str = "N"
    remindersent: str = "N"
    remindercount: int = 0
    completed: str = "N"
    emailstatus: str = "OK"
    blacklisted: str = None
    validuntil: str = None
    ano_conclusao: str = None
    semestre_conclusao: str = None
    recusa_base_central: bool = False
    respostas: list = field(default_factory=list)


def instante_utc(texto):
    """`sent` e `remindersent`: 'N' ou vazio quando nao houve; senao UTC."""
    texto = (texto or "").strip()
    if texto in ("", "N"):
        return None
    for formato in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(texto, formato).replace(tzinfo=UTC)
        except ValueError:
            continue
    raise ValueError(f"data de envio ilegivel: {texto!r}")


def _instante_local(texto, fuso):
    texto = (texto or "").strip()
    if not texto:
        return None
    for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(texto, formato).replace(tzinfo=fuso)
        except ValueError:
            continue
    raise ValueError(f"data ilegivel: {texto!r}")


def enviado_em(p):
    return instante_utc(p.sent)


def validade(p, agenda):
    """Fim da janela do participante. O gravado na plataforma, se houver; se
    nao, o que a janela da P5 da a partir do envio — para que um convite feito
    fora da rotina, sem janela gravada, tambem expire."""
    gravado = _instante_local(p.validuntil, agenda.fuso)
    if gravado is not None:
        return gravado
    envio = enviado_em(p)
    if envio is None:
        return None
    return envio.astimezone(agenda.fuso) + timedelta(days=agenda.janela_dias)


def estado(p, agora, agenda):
    """O estado do participante na secao 12 do P5, calculado do que a
    plataforma guarda. A ordem dos testes e a precedencia, e importa:

      1. recusa de contato — na base central, no participante ou em CON1;
         vale sobre tudo, inclusive sobre resposta de outro ciclo
      2. a resposta enviada decide pelo CON1, e NAO pela marca de concluido
         da plataforma: a recusa sai marcada como concluida (E14, E15)
      3. contato invalido — o emailstatus que a rotina de devolucoes grava
      4. pendente — sem convite neste ciclo
      5. expirado — janela encerrada sem conclusao
      6. em preenchimento — ha resposta NAO enviada com CON1 gravado, isto e,
         a pagina 1 foi enviada concordando. Abrir o endereco sem enviar pagina
         cria resposta com lastpage 0 e CON1 vazio (achado da E20), e isso
         continua `convidado`: o mecanismo nao rastreia abertura (P8, 10.3), e
         a plataforma so sabe que alguem comecou quando uma pagina chega (E08).
      7. convidado
    """
    status = (p.emailstatus or "").strip()
    if (p.recusa_base_central or status == "OptOut"
            or (p.blacklisted or "").strip().upper() == "Y"):
        return RECUSA_CONTATO
    enviadas = {(r.con1 or "").strip() for r in p.respostas if r.submetida}
    if CON1_RECUSA_CONTATO in enviadas:
        return RECUSA_CONTATO
    if CON1_CONCORDO in enviadas:
        return RESPONDENTE
    if CON1_RECUSA_CONSENTIMENTO in enviadas:
        return RECUSA_CONSENTIMENTO
    if enviadas or (p.completed or "N").strip() not in ("N", ""):
        return CONCLUIDO_SEM_RESPOSTA
    if status not in ("OK", ""):
        return CONTATO_INVALIDO
    if enviado_em(p) is None:
        return PENDENTE
    fim = validade(p, agenda)
    if fim is not None and fim < agora:
        return EXPIRADO
    if any(not r.submetida and (r.con1 or "").strip() for r in p.respostas):
        return EM_PREENCHIMENTO
    return CONVIDADO


# --- Plano ------------------------------------------------------------------

@dataclass
class Acao:
    tid: int
    participant_id: str
    tipo: str          # convite | lembrete | janela
    numero: int = 0    # 0 no convite; 1, 2, 3 no lembrete
    motivo: str = ""   # ancora | reconvite | cadencia | janela
    variante: str = None
    estado: str = ""
    validuntil: str = None


@dataclass
class Plano:
    convites: list = field(default_factory=list)
    lembretes: list = field(default_factory=list)
    janelas: list = field(default_factory=list)
    por_estado: Counter = field(default_factory=Counter)
    sem_envio: Counter = field(default_factory=Counter)

    def resumo(self):
        return {
            "por_estado": dict(self.por_estado),
            "convites": len(self.convites),
            "lembretes": dict(Counter(f"{a.numero}:{a.variante}"
                                      for a in self.lembretes)),
            "janelas": len(self.janelas),
            "sem_envio": dict(self.sem_envio),
        }


def soma_meses(dia, meses):
    ano, mes = divmod(dia.month - 1 + meses, 12)
    ano, mes = dia.year + ano, mes + 1
    for d in (dia.day, 30, 29, 28):
        try:
            return date(ano, mes, min(dia.day, d))
        except ValueError:
            continue
    raise ValueError(dia)


def _texto_local(instante):
    return instante.strftime("%Y-%m-%d %H:%M:%S")


def plano(participantes, agenda, ciclo_ano, agora,
          convites_no_ciclo=None, ultimo_convite_fora=None):
    """O que vence em `agora`, participante por participante.

    convites_no_ciclo     {tid: quantos convites ja enviados a ele neste
                           questionario e ciclo}, do registro proprio da
                           rotina. Distingue o convite inicial do reconvite
                           depois do reparo de contato (secao 6.1).
    ultimo_convite_fora   {participant_id: data do ultimo convite em OUTRO
                           questionario ou ciclo}, tambem do registro proprio:
                           o envio pela API nao atualiza `date_invited` da base
                           central (conferido no codigo), e a regra dos doze
                           meses precisa dessa data.
    """
    convites_no_ciclo = convites_no_ciclo or {}
    ultimo_convite_fora = ultimo_convite_fora or {}
    hoje = agora.astimezone(agenda.fuso).date()
    r = Plano()

    for p in participantes:
        try:
            e = estado(p, agora, agenda)
        except ValueError as ex:
            r.por_estado["ilegível"] += 1
            r.sem_envio[f"dado ilegível ({ex})"] += 1
            continue
        r.por_estado[e] += 1

        if e == PENDENTE:
            ja = convites_no_ciclo.get(p.tid, 0)
            if ja == 0:
                try:
                    ano = int(p.ano_conclusao)
                    semestre = int(p.semestre_conclusao)
                    if semestre not in (1, 2):
                        raise ValueError
                except (TypeError, ValueError):
                    r.sem_envio["sem âncora legível"] += 1
                    continue
                if ano > ciclo_ano:
                    r.sem_envio["conclusão posterior ao ciclo"] += 1
                    continue
                if hoje < agenda.data_ancora(ciclo_ano, semestre):
                    r.sem_envio["antes da âncora"] += 1
                    continue
                anterior = ultimo_convite_fora.get(p.participant_id)
                if anterior is not None and hoje < soma_meses(
                        anterior, agenda.meses_entre_convites):
                    r.sem_envio["menos de doze meses do convite anterior"] += 1
                    continue
                r.convites.append(Acao(p.tid, p.participant_id, "convite",
                                       motivo="ancora", estado=e))
            elif ja <= agenda.reconvites_por_ciclo:
                # Voltou a pendente depois de convidado: e o reparo de contato
                # (P8). Reconvite imediato, nova contagem, uma vez por ciclo.
                r.convites.append(Acao(p.tid, p.participant_id, "convite",
                                       motivo="reconvite", estado=e))
            else:
                r.sem_envio["teto de reparo atingido"] += 1
            continue

        if e not in RECEBEM_LEMBRETE:
            r.sem_envio[e] += 1
            continue

        envio = enviado_em(p).astimezone(agenda.fuso)
        if not (p.validuntil or "").strip():
            r.janelas.append(Acao(
                p.tid, p.participant_id, "janela", motivo="janela", estado=e,
                validuntil=_texto_local(envio + timedelta(
                    days=agenda.janela_dias))))

        k = int(p.remindercount or 0)
        if k >= len(agenda.lembretes_dias):
            r.sem_envio["lembretes esgotados"] += 1
            continue
        vence = envio.date() + timedelta(days=agenda.lembretes_dias[k])
        ultimo = instante_utc(p.remindersent)
        if k > 0 and ultimo is not None:
            vence = max(vence, ultimo.astimezone(agenda.fuso).date()
                        + timedelta(days=agenda.intervalo_minimo_dias))
        if hoje < vence:
            r.sem_envio["lembrete ainda não venceu"] += 1
            continue
        r.lembretes.append(Acao(
            p.tid, p.participant_id, "lembrete", numero=k + 1,
            motivo="cadencia", estado=e,
            variante=(VARIANTE_EM_PREENCHIMENTO if e == EM_PREENCHIMENTO
                      else VARIANTE_CONVIDADO)))

    return r


# --- Horario ----------------------------------------------------------------

def previsto_para(agenda, dia):
    """Instante do disparo agendado no dia, ou None se o dia nao e util."""
    if not agenda.dia_util(dia):
        return None
    return datetime.combine(dia, agenda.horario, tzinfo=agenda.fuso)
