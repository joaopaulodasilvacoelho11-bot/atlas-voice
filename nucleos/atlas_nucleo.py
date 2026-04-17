import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Intencao(Enum):
    SAUDACAO     = "saudacao"
    LEMBRETE     = "lembrete"
    PERGUNTA     = "pergunta"
    COMANDO      = "comando"
    CONVERSA     = "conversa"
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


# Padrões de frases naturais → resposta direta
_RESPOSTAS_DIRETAS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(como\s+t[aá]|como\s+voc[eê]\s+est[aá]|tudo\s+bem|tudo\s+bom|tudo\s+certo)\b", re.I),
     "Operacional. Pode mandar."),
    (re.compile(r"\b(oi|ol[aá]|e\s*a[ií]|hey|bom\s+dia|boa\s+tarde|boa\s+noite)\b", re.I),
     "Atlas ativo. O que precisa?"),
    (re.compile(r"\b(pode\s+me\s+ajudar|preciso\s+de\s+ajuda|me\s+ajuda|me\s+ajude)\b", re.I),
     "Sim. Alarmes, lembretes, perguntas ou comandos — é só falar."),
    (re.compile(r"\b(o\s+que\s+voc[eê]\s+(faz|[eé])|para\s+que\s+(serve|voc[eê])|quem\s+[eé]\s+voc[eê])\b", re.I),
     "Sou Atlas. Gerencio alarmes, lembretes e respondo comandos. Direto ao ponto."),
    (re.compile(r"\b(obrigad[ao]|valeu|brigad[ao])\b", re.I),
     "Certo."),
    (re.compile(r"\b(at[eé]\s+logo|tchau|falou|at[eé]\s+mais)\b", re.I),
     "Até."),
]


def _checar_direto(texto: str) -> Optional[str]:
    for padrao, resposta in _RESPOSTAS_DIRETAS:
        if padrao.search(texto):
            return resposta
    return None


class AtlasNucleo:

    def processar(self, entrada: Entrada) -> Resposta:
        direto = _checar_direto(entrada.texto)
        if direto:
            return Resposta(texto=direto, intencao=entrada.intencao)

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

    def _saudacao(self, entrada: Entrada) -> Resposta:
        return Resposta(
            texto="Atlas ativo. Como posso ajudar?",
            intencao=entrada.intencao,
        )

    def _lembrete(self, entrada: Entrada) -> Resposta:
        params    = entrada.parametros or {}
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
        params = entrada.parametros or {}
        acao   = params.get("acao", entrada.texto)
        alvo   = params.get("alvo", "")
        sufixo = f" em '{alvo}'" if alvo else ""
        return Resposta(
            texto=f"Comando '{acao}'{sufixo} executado.",
            intencao=entrada.intencao,
        )

    def _conversa(self, entrada: Entrada) -> Resposta:
        return Resposta(
            texto=f"Entendido: '{entrada.texto}'. Posso ajudar com algo concreto?",
            intencao=entrada.intencao,
        )

    def _desconhecida(self, entrada: Entrada) -> Resposta:
        return Resposta(
            texto="Não reconheci. Tente: alarme, lembrete, pergunta ou comando.",
            intencao=entrada.intencao,
            executada=False,
            erro="intencao_desconhecida",
        )
