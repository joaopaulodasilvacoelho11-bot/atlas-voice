from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Intencao(Enum):
    SAUDACAO    = "saudacao"
    LEMBRETE    = "lembrete"
    PERGUNTA    = "pergunta"
    COMANDO     = "comando"
    CONVERSA    = "conversa"
    DESCONHECIDA = "desconhecida"


@dataclass
class Entrada:
    texto: str
    intencao: Intencao
    parametros: Optional[dict] = None


@dataclass
class Resposta:
    texto: str
    intencao: Intencao
    executada: bool = True
    erro: Optional[str] = None


class AtlasNucleo:

    def processar(self, entrada: Entrada) -> Resposta:
        handlers = {
            Intencao.SAUDACAO:    self._saudacao,
            Intencao.LEMBRETE:    self._lembrete,
            Intencao.PERGUNTA:    self._pergunta,
            Intencao.COMANDO:     self._comando,
            Intencao.CONVERSA:    self._conversa,
            Intencao.DESCONHECIDA: self._desconhecida,
        }
        handler = handlers.get(entrada.intencao, self._desconhecida)
        return handler(entrada)

    def _saudacao(self, entrada: Entrada) -> Resposta:
        return Resposta(
            texto="Atlas ativo. Como posso ajudar?",
            intencao=entrada.intencao,
        )

    def _lembrete(self, entrada: Entrada) -> Resposta:
        params = entrada.parametros or {}
        descricao = params.get("descricao", entrada.texto)
        horario   = params.get("horario", "não especificado")
        return Resposta(
            texto=f"Lembrete registrado: '{descricao}' às {horario}.",
            intencao=entrada.intencao,
        )

    def _pergunta(self, entrada: Entrada) -> Resposta:
        return Resposta(
            texto=f"Pergunta recebida: '{entrada.texto}'. Processando resposta.",
            intencao=entrada.intencao,
        )

    def _comando(self, entrada: Entrada) -> Resposta:
        params  = entrada.parametros or {}
        acao    = params.get("acao", entrada.texto)
        alvo    = params.get("alvo", "")
        sufixo  = f" em '{alvo}'" if alvo else ""
        return Resposta(
            texto=f"Comando '{acao}'{sufixo} executado.",
            intencao=entrada.intencao,
        )

    def _conversa(self, entrada: Entrada) -> Resposta:
        return Resposta(
            texto=f"Entendido: '{entrada.texto}'.",
            intencao=entrada.intencao,
        )

    def _desconhecida(self, entrada: Entrada) -> Resposta:
        return Resposta(
            texto="Intenção não reconhecida. Reformule o pedido.",
            intencao=entrada.intencao,
            executada=False,
            erro="intencao_desconhecida",
        )
