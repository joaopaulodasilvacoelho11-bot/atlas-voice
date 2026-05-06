"""
extrator_alarme.py
Detecta intenção de alarme no texto do usuário e extrai horário + descrição.
Usado pelo api.py após receber mensagem — antes de responder.
"""

import re
from typing import Optional


# ---------------------------------------------------------------------------
# Padrões de intenção de alarme
# ---------------------------------------------------------------------------
_INTENCAO = re.compile(
    r"\b("
    r"me\s+acord[ae]r?|acorda\s+me|acorde\s+me|"
    r"pode\s+me\s+acord[ae]r?|"
    r"cria[r]?\s+alarme|coloca[r]?\s+alarme|bota[r]?\s+alarme|"
    r"alarme\s+para|alarme\s+[àa]s|"
    r"me\s+avisa[r]?\s+[àa]s|me\s+avisa[r]?\s+as|"
    r"me\s+lembra[r]?\s+[àa]s|"
    r"set[a]?\s+alarme|ativa[r]?\s+alarme|"
    r"quero\s+acordar|preciso\s+acordar|"
    r"acord[ae]r?\s+[àa]s|acord[ae]r?\s+as"
    r")\b",
    re.IGNORECASE
)

# ---------------------------------------------------------------------------
# Padrões de horário
# ---------------------------------------------------------------------------
# Exemplos: 21h, 21h30, 21:30, 9h, 09:00, 8 horas, às 7
_HORARIO = re.compile(
    r"\b(\d{1,2})\s*[h:]\s*(\d{0,2})\b"
    r"|\b(\d{1,2})\s+horas?\b",
    re.IGNORECASE
)


def _extrair_horario(texto: str) -> Optional[str]:
    """Retorna horário no formato HH:MM ou None se não encontrar."""
    m = _HORARIO.search(texto)
    if not m:
        return None

    if m.group(1) is not None:
        hora = int(m.group(1))
        minuto_str = m.group(2)
        minuto = int(minuto_str) if minuto_str else 0
    else:
        hora = int(m.group(3))
        minuto = 0

    if 0 <= hora <= 23 and 0 <= minuto <= 59:
        return f"{hora:02d}:{minuto:02d}"
    return None


# Substantivos de contexto conhecidos — match direto tem prioridade
_CONTEXTO = re.compile(
    r"\b(reuni[aã]o|m[eé]dico|m[eé]dica|consulta|dentista|trabalho|academia|treino|"
    r"aula|prova|compromisso|evento|apresenta[cç][aã]o|entrevista|voo|vi[aá]gem|"
    r"almo[cç]o|janta|jantar|caf[eé]|call|meeting|palestra|conf[eé]r[eê]ncia)\b",
    re.IGNORECASE,
)


def _extrair_descricao(texto: str) -> str:
    """Extrai descrição do alarme. Prioriza substantivo de contexto; fallback: 'Alarme'."""
    m = _CONTEXTO.search(texto)
    if m:
        return m.group(0).capitalize()

    desc = _INTENCAO.sub("", texto).strip()
    desc = _HORARIO.sub("", desc).strip()
    desc = re.sub(r"\b(para|às|as|pra|por|de|no|na|num|numa|um|uma|o|a)\b", "", desc, flags=re.IGNORECASE).strip()
    desc = re.sub(r"\s{2,}", " ", desc).strip(" .,;:-")

    if len(desc) < 3:
        return "Alarme"
    return desc.capitalize()


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------
def tentar_extrair_alarme(texto: str) -> Optional[dict]:
    """
    Analisa o texto e, se detectar intenção de alarme com horário,
    retorna dict com 'horario' (HH:MM) e 'mensagem'.
    Retorna None se não for um pedido de alarme.
    """
    if not _INTENCAO.search(texto):
        return None

    horario = _extrair_horario(texto)
    if not horario:
        return None

    descricao = _extrair_descricao(texto)
    return {
        "horario": horario,
        "mensagem": descricao,
    }
