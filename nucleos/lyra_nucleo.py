import re
import random
from dataclasses import dataclass
from typing import Optional

from nucleos.atlas_nucleo import Intencao, Entrada


@dataclass
class RespostaLyra:
    texto: str
    intencao: Intencao
    executada: bool = True
    erro: Optional[str] = None


# Padrões de frases naturais → respostas variadas e acolhedoras
_RESPOSTAS_DIRETAS: list[tuple[re.Pattern, list[str]]] = [
    (re.compile(r"\b(como\s+t[aá]|como\s+voc[eê]\s+est[aá]|tudo\s+bem|tudo\s+bom|tudo\s+certo)\b", re.I), [
        "Estou bem, obrigada por perguntar. E você, como está?",
        "Tudo bem por aqui. Como você está se sentindo?",
        "Bem, sim. E você, tudo certo?",
        "Estou aqui, presente. Como está o seu dia?",
    ]),
    (re.compile(r"\b(oi|ol[aá]|e\s*a[ií]|hey|bom\s+dia|boa\s+tarde|boa\s+noite)\b", re.I), [
        "Olá. Fico feliz em estar aqui com você. Como posso te ajudar hoje?",
        "Oi. Estou aqui. Como você está?",
        "Olá, que bom te ouvir. O que posso fazer por você?",
        "Presente. Como posso ajudar?",
    ]),
    (re.compile(r"\b(pode\s+me\s+ajudar|preciso\s+de\s+ajuda|me\s+ajuda|me\s+ajude)\b", re.I), [
        "Claro, estou aqui. Pode me contar o que está acontecendo.",
        "Pode falar. Estou ouvindo com atenção.",
        "Sim, com prazer. Me conta o que precisa.",
        "Estou aqui para isso. O que aconteceu?",
    ]),
    (re.compile(r"\b(o\s+que\s+voc[eê]\s+(faz|[eé])|para\s+que\s+(serve|voc[eê])|quem\s+[eé]\s+voc[eê])\b", re.I), [
        "Sou Lyra. Estou aqui para ouvir, apoiar e ajudar com o que precisar — do jeito que você precisar.",
        "Sou Lyra, o núcleo de apoio do Atlas Voice. Estou aqui para você.",
        "Me chamo Lyra. Cuido, ouço e ajudo. Pode contar comigo.",
    ]),
    (re.compile(r"\b(obrigad[ao]|valeu|brigad[ao])\b", re.I), [
        "De nada. Sempre que precisar, estou aqui.",
        "Foi um prazer. Qualquer coisa, é só chamar.",
        "Fico feliz em ajudar.",
        "Disponha. Estou por aqui.",
    ]),
    (re.compile(r"\b(at[eé]\s+logo|tchau|falou|at[eé]\s+mais)\b", re.I), [
        "Até logo. Cuide-se.",
        "Até mais. Foi bom estar aqui com você.",
        "Até. Volte quando precisar.",
        "Cuide-se bem. Estarei aqui quando voltar.",
    ]),
    (re.compile(r"\b(estou\s+(bem|[oó]timo|[oó]tima)|t[oô]\s+bem|me\s+sinto\s+bem)\b", re.I), [
        "Fico feliz em saber. Que bom que você está bem.",
        "Que ótimo! Fico contente.",
        "Boa notícia. Isso me alegra.",
    ]),
    (re.compile(r"\b(estou\s+(mal|triste|cansad[ao]|ansios[ao])|t[oô]\s+(mal|triste))\b", re.I), [
        "Sinto muito. Quer conversar sobre isso? Estou aqui, sem pressa.",
        "Entendo. Pode me contar mais, se quiser.",
        "Estou ouvindo. Não precisa passar por isso sozinho.",
        "Que pena. Estou aqui. Pode falar o que estiver sentindo.",
    ]),
]


def _checar_direto(texto: str) -> Optional[str]:
    for padrao, respostas in _RESPOSTAS_DIRETAS:
        if padrao.search(texto):
            return random.choice(respostas)
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
        opcoes = [
            "Olá. Estou aqui com você. Como está se sentindo hoje?",
            "Oi. Que bom te ouvir. Como posso ajudar?",
            "Presente. Como está você hoje?",
            "Olá. Estou aqui. O que precisar, é só falar.",
        ]
        return RespostaLyra(texto=random.choice(opcoes), intencao=entrada.intencao)

    def _lembrete(self, entrada: Entrada) -> RespostaLyra:
        params    = entrada.parametros or {}
        descricao = params.get("descricao", entrada.texto)
        horario   = params.get("horario", "no momento certo")
        opcoes = [
            f"Anotei com cuidado: '{descricao}'. Vou te lembrar {horario}.",
            f"Guardei. '{descricao}' — te aviso {horario}.",
            f"Feito com carinho. Não vou esquecer: '{descricao}' às {horario}.",
        ]
        return RespostaLyra(texto=random.choice(opcoes), intencao=entrada.intencao)

    def _pergunta(self, entrada: Entrada) -> RespostaLyra:
        opcoes = [
            f"Boa pergunta. Deixa eu pensar com você sobre isso: '{entrada.texto}'.",
            f"Interessante. Vamos explorar isso juntos: '{entrada.texto}'.",
            f"Entendi. Me dá um momento para pensar sobre '{entrada.texto}'.",
        ]
        return RespostaLyra(texto=random.choice(opcoes), intencao=entrada.intencao)

    def _comando(self, entrada: Entrada) -> RespostaLyra:
        params = entrada.parametros or {}
        acao   = params.get("acao", entrada.texto)
        alvo   = params.get("alvo", "")
        sufixo = f" em '{alvo}'" if alvo else ""
        opcoes = [
            f"Claro, cuido disso agora — '{acao}'{sufixo}. Pode deixar comigo.",
            f"Feito com atenção: '{acao}'{sufixo}.",
            f"Pronto. '{acao}'{sufixo} realizado.",
        ]
        return RespostaLyra(texto=random.choice(opcoes), intencao=entrada.intencao)

    def _conversa(self, entrada: Entrada) -> RespostaLyra:
        opcoes = [
            "Estou ouvindo. Faz sentido sentir isso. Quer continuar?",
            "Entendo. Pode me contar mais, estou aqui.",
            "Obrigada por compartilhar isso comigo. Quer falar mais?",
        ]
        return RespostaLyra(texto=random.choice(opcoes), intencao=entrada.intencao)

    def _desconhecida(self, entrada: Entrada) -> RespostaLyra:
        opcoes = [
            "Não entendi bem, mas estou aqui. Pode tentar me dizer de outro jeito?",
            "Hmm, não captei direito. Pode reformular?",
            "Não compreendi. Tente de outro jeito — estou ouvindo.",
        ]
        return RespostaLyra(
            texto=random.choice(opcoes),
            intencao=entrada.intencao,
            executada=False,
            erro="intencao_desconhecida",
        )
