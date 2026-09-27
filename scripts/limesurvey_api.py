#!/usr/bin/env python3
"""
Cliente minimo da API RemoteControl do LimeSurvey.

Existe para que as rotinas do projeto conversem com a instancia por uma via so,
e para que os enganos que essa API impoe fiquem tratados num lugar unico em vez
de repetidos em cada rotina. Sao dois, e ambos custaram tempo na E08:

  1. Sucesso e sinalizado por {"status": "OK"}; falha, por {"status": "<motivo>"},
     as vezes com "error_code" ao lado. Condicionar o teste ao numero de chaves
     do dicionario faz passar erro por sucesso.
  2. A tabela de respostas chama-se `lime_responses_<sid>`, e nao
     `lime_survey_<sid>`, que e o nome que a documentacao antiga usa.

Usado por ler_devolucoes.py (E09) e pela extracao de resultados (E28).
"""

import json
import os
import urllib.error
import urllib.request


class ErroAPI(Exception):
    pass


# Marcadores de ausencia de dados. A API sinaliza "nao ha nada" com erro, e isso
# nao e falha: num questionario recem-criado, "sem participantes" e o estado
# esperado.
SEM_DADOS = ("ERR_NO_DATA", "No surveys found", "No survey participants",
             "No Tokens found")


def normaliza_participante(registro):
    """Achata um registro de `list_participants` num dicionario unico.

    Necessario porque a API devolve estrutura MISTA, e essa e a terceira
    armadilha dela: `firstname`, `lastname` e `email` vem ANINHADOS sob
    `participant_info`, enquanto `tid`, `token`, `emailstatus` e `sent` vem no
    nivel de cima. Ler tudo de um dos dois lugares devolve campo vazio sem erro
    algum — foi o que fez a E09 concluir que uma gravacao bem-sucedida nao tinha
    pegado.
    """
    if not isinstance(registro, dict):
        return {}
    achatado = {k: v for k, v in registro.items() if k != "participant_info"}
    aninhado = registro.get("participant_info")
    if isinstance(aninhado, dict):
        for k, v in aninhado.items():
            achatado.setdefault(k, v)
    return achatado


def eh_erro(resultado):
    """Diz se um resultado com campo `status` representa falha.

    O campo `status` da API NAO significa erro por si so: ele carrega tambem
    mensagens informativas de sucesso, como "0 left to send" devolvido por
    `invite_participants` quando todos os convites sairam. Tratar todo `status`
    diferente de "OK" como falha faz um envio bem-sucedido parecer erro — e foi
    exatamente o engano que custou uma rodada de diagnostico na E09.

    O sinal confiavel e a presenca de `error_code`. O prefixo textual entra como
    reforco, para os poucos casos em que a API o omite.
    """
    if not isinstance(resultado, dict):
        return False
    if resultado.get("error_code"):
        return True
    texto = str(resultado.get("status", "")).strip().upper()
    return texto.startswith(("ERROR", "INVALID", "NO PERMISSION",
                             "NO DATA", "FAILED"))


class API:
    """Sessao com a API RemoteControl.

    Usar como gerenciador de contexto, para que a chave de sessao seja sempre
    liberada:

        with API() as api:
            api.chamar("list_surveys", [])
    """

    def __init__(self, url=None, usuario=None, senha=None, tempo_limite=60):
        base = url or os.environ.get("LIMESURVEY_URL", "http://limesurvey")
        self.endereco = base.rstrip("/") + "/index.php/admin/remotecontrol"
        self.usuario = usuario or os.environ.get("LIMESURVEY_USUARIO")
        self.senha = senha or os.environ.get("LIMESURVEY_SENHA")
        self.tempo_limite = tempo_limite
        self.chave = None

    # -- ciclo de vida ----------------------------------------------------

    def abrir(self):
        if not self.usuario or not self.senha:
            raise ErroAPI("LIMESURVEY_USUARIO ou LIMESURVEY_SENHA nao definidos")
        chave = self._enviar("get_session_key", [self.usuario, self.senha])
        if not isinstance(chave, str):
            raise ErroAPI(f"sessao nao obtida: {chave}")
        self.chave = chave
        return self

    def fechar(self):
        if self.chave:
            try:
                self._enviar("release_session_key", [self.chave])
            except ErroAPI:
                pass
            self.chave = None

    def __enter__(self):
        return self.abrir()

    def __exit__(self, *_):
        self.fechar()
        return False

    # -- chamadas ---------------------------------------------------------

    def _enviar(self, metodo, params):
        corpo = json.dumps({"method": metodo, "params": params, "id": 1}).encode()
        pedido = urllib.request.Request(
            self.endereco, data=corpo,
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(pedido, timeout=self.tempo_limite) as resp:
                dados = json.loads(resp.read().decode())
        except urllib.error.URLError as e:
            raise ErroAPI(f"{metodo}: instancia inacessivel em {self.endereco} ({e})")
        if dados.get("error"):
            raise ErroAPI(f"{metodo}: {dados['error']}")
        resultado = dados.get("result")
        if isinstance(resultado, dict) and "status" in resultado:
            if eh_erro(resultado):
                raise ErroAPI(f"{metodo}: {resultado.get('status')} "
                              f"{resultado.get('error_code', '')}".strip())
        return resultado

    def chamar(self, metodo, params=None):
        if self.chave is None:
            raise ErroAPI("sessao nao aberta")
        return self._enviar(metodo, [self.chave] + list(params or []))

    # -- atalhos usados pelas rotinas -------------------------------------

    def participantes(self, questionario, limite=1000, atributos=None):
        """Lista os participantes de um questionario.

        Devolve lista vazia quando nao ha nenhum, em vez de propagar o erro que
        a API emite nesse caso — "No survey participants found" nao e falha.
        """
        try:
            r = self.chamar("list_participants",
                            [questionario, 0, limite, False,
                             atributos or ["email", "emailstatus", "sent",
                                           "remindersent", "remindercount",
                                           "completed", "blacklisted"]])
        except ErroAPI as e:
            if any(m in str(e) for m in SEM_DADOS):
                return []
            raise
        if not isinstance(r, list):
            return []
        # Ja achatados: quem chama nao precisa conhecer a estrutura mista.
        return [normaliza_participante(p) for p in r]

    def participante_por_email(self, questionario, endereco):
        """Acha um participante pelo endereco. Devolve None se nao houver."""
        alvo = endereco.strip().lower()
        for p in self.participantes(questionario):
            if str(p.get("email", "")).strip().lower() == alvo:
                return p
        return None

    def marcar_estado_de_entrega(self, questionario, token_id, estado):
        """Grava o estado de entrega de um participante.

        Vai pela API, e nao por UPDATE direto na tabela, para que a rotina nao
        dependa do esquema interno do LimeSurvey.
        """
        return self.chamar("set_participant_properties",
                           [questionario, {"tid": token_id},
                            {"emailstatus": estado}])
