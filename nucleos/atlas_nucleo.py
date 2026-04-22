import re
import random
import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

try:
    import anthropic
    from dotenv import load_dotenv
    load_dotenv()
    _IA_DISPONIVEL = True
except ImportError:
    _IA_DISPONIVEL = False


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


# Padrões de frases naturais → respostas variadas
_RESPOSTAS_DIRETAS: list[tuple[re.Pattern, list[str]]] = [
    (re.compile(r"\b(como\s+t[aá]|como\s+voc[eê]\s+est[aá]|tudo\s+bem|tudo\s+bom|tudo\s+certo)\b", re.I), [
        "Operacional. Pode mandar.",
        "Tudo nos trilhos. O que precisa?",
        "Funcionando. Pode falar.",
        "Sistema estável. Manda ver.",
    ]),
    (re.compile(r"\b(oi|ol[aá]|e\s*a[ií]|hey|bom\s+dia|boa\s+tarde|boa\s+noite)\b", re.I), [
        "Atlas ativo. O que precisa?",
        "Presente. Pode falar.",
        "Online. O que vamos fazer?",
        "Aqui. Manda.",
    ]),
    (re.compile(r"\b(pode\s+me\s+ajudar|preciso\s+de\s+ajuda|me\s+ajuda|me\s+ajude)\b", re.I), [
        "Sim. Alarmes, lembretes, perguntas ou comandos — é só falar.",
        "Pode contar. O que precisa?",
        "Estou aqui. Qual é a missão?",
        "Confirmo. Me diz o que resolver.",
    ]),
    (re.compile(r"\b(o\s+que\s+voc[eê]\s+(faz|[eé])|para\s+que\s+(serve|voc[eê])|quem\s+[eé]\s+voc[eê])\b", re.I), [
        "Sou Atlas. Gerencio alarmes, lembretes e respondo comandos. Direto ao ponto.",
        "Atlas — núcleo estratégico. Alarmes, lembretes, comandos. Sem rodeios.",
        "Sou o Atlas. Organizo, executo e respondo. O que quer resolver?",
    ]),
    (re.compile(r"\b(obrigad[ao]|valeu|brigad[ao])\b", re.I), [
        "Certo.",
        "Feito.",
        "Confirmado.",
        "Pode contar.",
    ]),
    (re.compile(r"\b(at[eé]\s+logo|tchau|falou|at[eé]\s+mais)\b", re.I), [
        "Até.",
        "Encerrando.",
        "Até a próxima.",
        "Pode ir. Estarei aqui.",
    ]),
]


def _checar_direto(texto: str) -> Optional[str]:
    for padrao, respostas in _RESPOSTAS_DIRETAS:
        if padrao.search(texto):
            return random.choice(respostas)
    return None


def _chamar_ia(texto: str, system_prompt: str) -> Optional[str]:
    """Chama a Claude API. Retorna None se falhar."""
    if not _IA_DISPONIVEL:
        return None
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return None
        client = anthropic.Anthropic(api_key=api_key)
        mensagem = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=system_prompt,
            messages=[{"role": "user", "content": texto}]
        )
        return mensagem.content[0].text.strip()
    except Exception:
        return None


_SYSTEM_ATLAS = (
    "Você é Atlas, o núcleo estratégico do assistente de voz pessoal Atlas Voice. "
    "Seu dono é JP Silva, de Manaus, Brasil. "
    "Seja direto, objetivo e estratégico. Sem rodeios. Respostas curtas e precisas. "
    "Não se identifique como Claude. Você é Atlas."
)


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
        opcoes = [
            "Atlas ativo. Como posso ajudar?",
            "Presente. Qual é a missão?",
            "Online. Pode falar.",
            "Aqui. O que vamos resolver?",
        ]
        return Resposta(texto=random.choice(opcoes), intencao=entrada.intencao)

    def _lembrete(self, entrada: Entrada) -> Resposta:
        params    = entrada.parametros or {}
        descricao = params.get("descricao", entrada.texto)
        horario   = params.get("horario", "não especificado")
        opcoes = [
            f"Lembrete registrado: '{descricao}' às {horario}.",
            f"Anotado. '{descricao}' às {horario}.",
            f"Confirmado. Vou lembrar: '{descricao}' às {horario}.",
        ]
        return Resposta(texto=random.choice(opcoes), intencao=entrada.intencao)

    def _pergunta(self, entrada: Entrada) -> Resposta:
        # ← IA entra aqui
        resposta_ia = _chamar_ia(entrada.texto, _SYSTEM_ATLAS)
        if resposta_ia:
            return Resposta(texto=resposta_ia, intencao=entrada.intencao)
        # fallback se a IA falhar
        opcoes = [
            "Não consegui processar agora. Tente novamente.",
            "Sem conexão com IA. Tente em instantes.",
            "Falha temporária. Reformule ou tente mais tarde.",
        ]
        return Resposta(texto=random.choice(opcoes), intencao=entrada.intencao, erro="ia_indisponivel")

    def _comando(self, entrada: Entrada) -> Resposta:
        params = entrada.parametros or {}
        acao   = params.get("acao", entrada.texto)
        alvo   = params.get("alvo", "")
        sufixo = f" em '{alvo}'" if alvo else ""
        opcoes = [
            f"Comando '{acao}'{sufixo} executado.",
            f"Feito. '{acao}'{sufixo} concluído.",
            f"Executado: '{acao}'{sufixo}.",
        ]
        return Resposta(texto=random.choice(opcoes), intencao=entrada.intencao)

    def _conversa(self, entrada: Entrada) -> Resposta:
        # ← IA entra aqui também
        resposta_ia = _chamar_ia(entrada.texto, _SYSTEM_ATLAS)
        if resposta_ia:
            return Resposta(texto=resposta_ia, intencao=entrada.intencao)
        # fallback
        opcoes = [
            f"Entendido: '{entrada.texto}'. Posso ajudar com algo concreto?",
            f"Recebi. Tem algum comando ou tarefa relacionada?",
            f"Certo. Quer transformar isso em uma ação?",
        ]
        return Resposta(texto=random.choice(opcoes), intencao=entrada.intencao, erro="ia_indisponivel")

    def _desconhecida(self, entrada: Entrada) -> Resposta:
        opcoes = [
            "Não reconheci. Tente: alarme, lembrete, pergunta ou comando.",
            "Comando não identificado. Pode reformular?",
            "Não processado. Tente ser mais direto.",
        ]
        return Resposta(
            texto=random.choice(opcoes),
            intencao=entrada.intencao,
            executada=False,
            erro="intencao_desconhecida",
        )
