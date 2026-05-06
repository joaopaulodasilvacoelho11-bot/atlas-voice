"""
extrator_lembrete.py
Detecta intenção de lembrete no texto do usuário e extrai horário + descrição + prioridade.
Usado pelo api.py após receber mensagem — antes de responder.
"""

import re
from typing import Optional


# ---------------------------------------------------------------------------
# Padrões de intenção de lembrete
# ---------------------------------------------------------------------------
_INTENCAO = re.compile(
    r"\b("
    r"me\s+lembra[r]?\s+de|me\s+lembra[r]?\s+que|"
    r"lembra\s+me\s+de|lembre\s+me\s+de|"
    r"pode\s+me\s+lembrar\s+de|"
    r"n[aã]o\s+me\s+deixa[r]?\s+esquecer|"
    r"cria[r]?\s+lembrete|coloca[r]?\s+lembrete|bota[r]?\s+lembrete|"
    r"lembrete\s+para|lembrete\s+[àa]s|"
    r"me\s+avisa[r]?\s+de|me\s+avisa[r]?\s+que|"
    r"agenda[r]?\s+lembrete|salva[r]?\s+lembrete|"
    r"preciso\s+lembrar|quero\s+lembrar|"
    r"anota[r]?\s+que|n[aã]o\s+esquece[r]?\s+de"
    r")\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Padrões de horário
# ---------------------------------------------------------------------------
# Exemplos: 21h, 21h30, 21:30, 9h, 09:00, 8 horas, às 7
_HORARIO = re.compile(
    r"(?<!\d)(\d{1,2})[h:](\d{2})(?!\d)"
    r"|(?<!\d)(\d{1,2})h(?!\d)"
    r"|(?<!\d)(\d{1,2})\s+horas?",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Padrões de prioridade explícita
# ---------------------------------------------------------------------------
_PRIORIDADE_ALTA = re.compile(
    r"\b(urgente|importante|prioridade\s+alta|n[aã]o\s+pode\s+esquecer|cr[ií]tico)\b",
    re.IGNORECASE,
)
_PRIORIDADE_BAIXA = re.compile(
    r"\b(quando\s+der|se\s+possível|sem\s+pressa|baixa\s+prioridade|depois)\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Substantivos de contexto para descrição
# ---------------------------------------------------------------------------
_CONTEXTO = re.compile(
    r"\b(reuni[aã]o|m[eé]dico|m[eé]dica|consulta|dentista|trabalho|academia|treino|"
    r"aula|prova|compromisso|evento|apresenta[cç][aã]o|entrevista|voo|vi[aá]gem|"
    r"almo[cç]o|janta|jantar|caf[eé]|call|meeting|palestra|conf[eé]r[eê]ncia|"
    r"rem[eé]dio|medica[cç][aã]o|ligação|ligar|pagar|conta|boleto|compra[r]?|"
    r"buscar|pegar|enviar|mandar|responder|confirmar|cancelar|agendar)\b",
    re.IGNORECASE,
)


def _extrair_horario(texto: str) -> Optional[str]:
    m = _HORARIO.search(texto)
    if not m:
        return None
    if m.group(1) is not None:
        hora, minuto = int(m.group(1)), int(m.group(2))
    elif m.group(3) is not None:
        hora, minuto = int(m.group(3)), 0
    else:
        hora, minuto = int(m.group(4)), 0
    if 0 <= hora <= 23 and 0 <= minuto <= 59:
        return f"{hora:02d}:{minuto:02d}"
    return None


def _extrair_descricao(texto: str) -> str:
    """Extrai descrição do lembrete. Prioriza substantivo de contexto; fallback: 'Lembrete'."""
    m = _CONTEXTO.search(texto)
    if m:
        return m.group(0).capitalize()

    desc = _INTENCAO.sub("", texto).strip()
    desc = _HORARIO.sub("", desc).strip()
    desc = re.sub(
        r"\b(para|às|as|pra|por|de|no|na|num|numa|um|uma|o|a|que|me)\b",
        "",
        desc,
        flags=re.IGNORECASE,
    ).strip()
    desc = re.sub(r"\s{2,}", " ", desc).strip(" .,;:-")

    if len(desc) < 3:
        return "Lembrete"
    return desc.capitalize()


def _extrair_prioridade(texto: str) -> str:
    """Detecta prioridade no texto. Padrão: Normal."""
    if _PRIORIDADE_ALTA.search(texto):
        return "Alta"
    if _PRIORIDADE_BAIXA.search(texto):
        return "Baixa"
    return "Normal"


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------
def tentar_extrair_lembrete(texto: str) -> Optional[dict]:
    """
    Analisa o texto e, se detectar intenção de lembrete com horário,
    retorna dict com 'horario' (HH:MM), 'mensagem' e 'prioridade'.
    Retorna None se não for um pedido de lembrete.
    """
    if not _INTENCAO.search(texto):
        return None

    horario = _extrair_horario(texto)
    if not horario:
        return None

    descricao  = _extrair_descricao(texto)
    prioridade = _extrair_prioridade(texto)

    return {
        "horario":    horario,
        "mensagem":   descricao,
        "prioridade": prioridade,
    }


if __name__ == "__main__":
    testes = [
        "me lembra de ligar pra mamae as 15:22",
        "me lembra de ligar pro medico às 15:30",
        "me lembra de academia as 18h",
        "lembra de mim de pagar o boleto às 9h30",
    ]
    for t in testes:
        print(f"TEXTO: {t}")
        print(f"RESULTADO: {tentar_extrair_lembrete(t)}")
        print()
