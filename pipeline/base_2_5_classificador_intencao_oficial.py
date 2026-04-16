import re
from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Intencao(Enum):
    SAUDACAO        = "saudacao"
    LEMBRETE        = "lembrete"
    PERGUNTA        = "pergunta"
    COMANDO         = "comando"
    CONVERSA        = "conversa"
    FORA_DE_ESCOPO  = "fora_de_escopo"


class Respondente(Enum):
    ATLAS = "atlas"
    LYRA  = "lyra"


# Intenções que pedem precisão e ação → Atlas
# Intenções que pedem presença e escuta → Lyra
_RESPONDENTE_POR_INTENCAO: dict[Intencao, Respondente] = {
    Intencao.SAUDACAO:       Respondente.LYRA,
    Intencao.LEMBRETE:       Respondente.ATLAS,
    Intencao.PERGUNTA:       Respondente.ATLAS,
    Intencao.COMANDO:        Respondente.ATLAS,
    Intencao.CONVERSA:       Respondente.LYRA,
    Intencao.FORA_DE_ESCOPO: Respondente.LYRA,
}

_PADROES: list[Tuple[Intencao, list[str]]] = [
    (Intencao.SAUDACAO, [
        r"\b(oi|olá|ola|hey|bom dia|boa tarde|boa noite|e aí|eai|tudo bem)\b",
    ]),
    (Intencao.LEMBRETE, [
        r"\b(lembra|lembre|avisa|avise|não (me )?deixa esquecer|me avisa|me lembra|agendar?|agenda)\b",
        r"\b(às|as|daqui|em)\b.{0,20}\b(hora|horas|minutos?|amanhã|hoje|semana)\b",
    ]),
    (Intencao.PERGUNTA, [
        r"^(o que|quem|quando|onde|como|por que|porque|qual|quanto|quais)\b",
        r"\?$",
        r"\b(me (diz|fala|explica|conta)|sabe(s)?)\b",
    ]),
    (Intencao.COMANDO, [
        r"^(abre|fecha|liga|desliga|inicia|para|executa|rode|roda|mostra|exibe|toca|pause|play|vai|vá|acessa|busca|pesquisa)\b",
        r"\b(por favor )?(pode |consegue )?(abrir|fechar|ligar|desligar|iniciar|parar|executar|mostrar|tocar)\b",
    ]),
    (Intencao.CONVERSA, [
        r"\b(tô|estou|me sinto|sinto|tava|estava|foi|fui|pensei|acho|achar|preciso conversar|quero falar)\b",
        r"\b(cansado|triste|feliz|ansioso|nervoso|bem|mal|ótimo|péssimo|preocupado)\b",
    ]),
]


@dataclass
class ResultadoClassificacao:
    texto_original: str
    intencao: Intencao
    respondente: Respondente
    confianca: float


def _normalizar(texto: str) -> str:
    return texto.lower().strip()


def _pontuar(texto: str) -> list[Tuple[Intencao, int]]:
    pontuacao: dict[Intencao, int] = {}
    for intencao, padroes in _PADROES:
        for padrao in padroes:
            if re.search(padrao, texto, re.IGNORECASE):
                pontuacao[intencao] = pontuacao.get(intencao, 0) + 1
    return sorted(pontuacao.items(), key=lambda x: x[1], reverse=True)


def classificar(texto: str) -> ResultadoClassificacao:
    normalizado = _normalizar(texto)
    pontuacao   = _pontuar(normalizado)

    if not pontuacao:
        intencao   = Intencao.FORA_DE_ESCOPO
        confianca  = 0.0
    else:
        intencao  = pontuacao[0][0]
        total     = sum(p for _, p in pontuacao)
        confianca = round(pontuacao[0][1] / total, 2)

    return ResultadoClassificacao(
        texto_original=texto,
        intencao=intencao,
        respondente=_RESPONDENTE_POR_INTENCAO[intencao],
        confianca=confianca,
    )
