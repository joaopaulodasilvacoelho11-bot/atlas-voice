import re
from dataclasses import dataclass
from typing import Optional

from nucleos.atlas_nucleo import Intencao, Entrada


@dataclass
class RespostaLyra:
    texto: str
    intencao: Intencao
    executada: bool = True
    erro: Optional[str] = None


# Padrões de frases naturais → resposta acolhedora
_RESPOSTAS_DIRETAS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(como\s+t[aá]|como\s+voc[eê]\s+est[aá]|tudo\s+bem|tudo\s+bom|tudo\s+certo)\b", re.I),
     "Estou bem, obrigada por perguntar. E você, como está?"),
    (re.compile(r"\b(oi|ol[aá]|e\s*a[ií]|hey|bom\s+dia|boa\s+tarde|boa\s+noite)\b", re.I),
     "Olá. Fico feliz em estar aqui com você. Como posso te ajudar hoje?"),
    (re.compile(r"\b(pode\s+me\s+ajudar|preciso\s+de\s+ajuda|me\s+ajuda|me\s+ajude)\b", re.I),
     "Claro, estou aqui. Pode me contar o que está acontecendo."),
    (re.compile(r"\b(o\s+que\s+voc[eê]\s+(faz|[eé])|para\s+que\s+(serve|voc[eê])|quem\s+[eé]\s+voc[eê])\b", re.I),
     "Sou Lyra. Estou aqui para ouvir, apoiar e ajudar com o que precisar — do jeito que você precisar."),
    (re.compile(r"\b(obrigad[ao]|valeu|brigad[ao])\b", re.I),
     "De nada. Sempre que precisar, estou aqui."),
    (re.compile(r"\b(at[eé]\s+logo|tchau|falou|at[eé]\s+mais)\b", re.I),
     "Até logo. Cuide-se."),
    (re.compile(r"\b(estou\s+(bem|[oó]timo|[oó]tima)|t[oô]\s+bem|me\s+sinto\s+bem)\b", re.I),
     "Fico feliz em saber. Que bom que você está bem."),
    (re.compile(r"\b(estou\s+(mal|triste|cansad[ao]|ansios[ao])|t[oô]\s+(mal|triste))\b", re.I),
     "Sinto muito. Quer conversar sobre isso? Estou aqui, sem pressa."),
]


def _checar_direto(texto: str) -> Optional[str]:
    for padrao, resposta in _RESPOSTAS_DIRETAS:
        if padrao.search(texto):
            return resposta
    return None


class LyraNucleo:

    def processar(self, entrada: Entrada) -> RespostaLyra:
        direto = _checar_direto(entrada.texto)
        if direto:
            return RespostaLyra(texto=direto, intencao=entrada.intencao)

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
            texto=f"Estou ouvindo. Faz sentido sentir isso. Quer continuar?",
            intencao=entrada.intencao,
        )

    def _desconhecida(self, entrada: Entrada) -> RespostaLyra:
        return RespostaLyra(
            texto="Não entendi bem, mas estou aqui. Pode tentar me dizer de outro jeito?",
            intencao=entrada.intencao,
            executada=False,
            erro="intencao_desconhecida",
        )
