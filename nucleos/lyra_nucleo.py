from dataclasses import dataclass
from typing import Optional

from nucleos.atlas_nucleo import Intencao, Entrada


@dataclass
class RespostaLyra:
    texto: str
    intencao: Intencao
    executada: bool = True
    erro: Optional[str] = None


class LyraNucleo:

    def processar(self, entrada: Entrada) -> RespostaLyra:
        handlers = {
            Intencao.SAUDACAO:     self._saudacao,
            Intencao.LEMBRETE:     self._lembrete,
            Intencao.PERGUNTA:     self._pergunta,
            Intencao.COMANDO:      self._comando,
            Intencao.CONVERSA:     self._conversa,
            Intencao.DESCONHECIDA: self._desconhecida,
        }
        handler = handlers.get(entrada.intencao, self._desconhecida)
        return handler(entrada)

    def _saudacao(self, entrada: Entrada) -> RespostaLyra:
        return RespostaLyra(
            texto="Olá. Estou aqui com você. Como está se sentindo hoje?",
            intencao=entrada.intencao,
        )

    def _lembrete(self, entrada: Entrada) -> RespostaLyra:
        params    = entrada.parametros or {}
        descricao = params.get("descricao", entrada.texto)
        horario   = params.get("horario", "no momento certo")
        return RespostaLyra(
            texto=f"Anotei com cuidado: '{descricao}'. Vou te lembrar {horario}.",
            intencao=entrada.intencao,
        )

    def _pergunta(self, entrada: Entrada) -> RespostaLyra:
        return RespostaLyra(
            texto=f"Boa pergunta. Deixa eu pensar com você sobre isso: '{entrada.texto}'.",
            intencao=entrada.intencao,
        )

    def _comando(self, entrada: Entrada) -> RespostaLyra:
        params = entrada.parametros or {}
        acao   = params.get("acao", entrada.texto)
        alvo   = params.get("alvo", "")
        sufixo = f" em '{alvo}'" if alvo else ""
        return RespostaLyra(
            texto=f"Claro, cuido disso agora — '{acao}'{sufixo}. Pode deixar comigo.",
            intencao=entrada.intencao,
        )

    def _conversa(self, entrada: Entrada) -> RespostaLyra:
        return RespostaLyra(
            texto=f"Estou ouvindo. '{entrada.texto}' — faz sentido sentir isso. Quer continuar?",
            intencao=entrada.intencao,
        )

    def _desconhecida(self, entrada: Entrada) -> RespostaLyra:
        return RespostaLyra(
            texto="Não entendi bem, mas estou aqui. Pode tentar me dizer de outro jeito?",
            intencao=entrada.intencao,
            executada=False,
            erro="intencao_desconhecida",
        )
