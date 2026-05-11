"""
extrator_lembrete.py
Detecta intenção de lembrete no texto do usuário e extrai horário + descrição + prioridade.
Usado pelo api.py após receber mensagem — antes de responder.
"""

import re
from typing import Optional


_INTENCAO = re.compile(
    r"\b("
    r"me\s+lembr[ae][r]?\s+de|me\s+lembr[ae][r]?\s+que|"
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

_HORARIO = re.compile(
    r"(?<!\d)(\d{1,2})[h:](\d{2})(?!\d)"
    r"|(?<!\d)(\d{1,2})h(?!\d)"
    r"|(?<!\d)(\d{1,2})\s+horas?"
    r"|(?<!\d)(\d{1,2})\s+e\s+(\d{2})(?!\d)",
    re.IGNORECASE,
)

_PRIORIDADE_ALTA = re.compile(
    r"\b(urgente|importante|prioridade\s+alta|n[aã]o\s+pode\s+esquecer|cr[ií]tico)\b",
    re.IGNORECASE,
)
_PRIORIDADE_BAIXA = re.compile(
    r"\b(quando\s+der|se\s+possível|sem\s+pressa|baixa\s+prioridade|depois)\b",
    re.IGNORECASE,
)

_CONTEXTO = re.compile(
    r"\b(reuni[aã]o|m[eé]dico|m[eé]dica|consulta|dentista|trabalho|academia|treino|"
    r"aula|prova|compromisso|evento|apresenta[cç][aã]o|entrevista|voo|vi[aá]gem|"
    r"almo[cç]o|janta|jantar|caf[eé]|call|meeting|palestra|conf[eé]r[eê]ncia|"
    r"rem[eé]dio|medica[cç][aã]o|ligação|ligar|pagar|conta|boleto|compra[r]?|"
    r"buscar|pegar|enviar|mandar|responder|confirmar|cancelar|agendar|"
    r"[aá]gua|beber|tomar)\b",
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
    elif m.group(4) is not None:
        hora, minuto = int(m.group(4)), 0
    elif m.group(5) is not None:
        hora, minuto = int(m.group(5)), int(m.group(6))
    else:
        return None
    if 0 <= hora <= 23 and 0 <= minuto <= 59:
        return f"{hora:02d}:{minuto:02d}"
    return None


def _extrair_descricao(texto: str) -> str:
    m = _CONTEXTO.search(texto)
    if m:
        return m.group(0).capitalize()
    desc = _INTENCAO.sub("", texto).strip()
    desc = _HORARIO.sub("", desc).strip()
    desc = re.sub(
        r"\b(para|às|as|pra|por|de|no|na|num|numa|um|uma|o|a|que|me)\b",
        "", desc, flags=re.IGNORECASE,
    ).strip()
    desc = re.sub(r"\s{2,}", " ", desc).strip(" .,;:-")
    if len(desc) < 3:
        return "Lembrete"
    return desc.capitalize()


def _extrair_prioridade(texto: str) -> str:
    if _PRIORIDADE_ALTA.search(texto):
        return "Alta"
    if _PRIORIDADE_BAIXA.search(texto):
        return "Baixa"
    return "Normal"


def tentar_extrair_lembrete(texto: str) -> Optional[dict]:
    if not _INTENCAO.search(texto):
        return None
    horario = _extrair_horario(texto)
    if not horario:
        return None
    return {
        "horario":    horario,
        "mensagem":   _extrair_descricao(texto),
        "prioridade": _extrair_prioridade(texto),
    }


if __name__ == "__main__":
    testes = [
        "me lembra de ligar pra mamae as 15:22",
        "me lembra de academia as 18h",
        "me lembre de tomar água às 13 e 23",
        "me lembra de beber água às 14 e 05",
    ]
    for t in testes:
        print(f"TEXTO: {t}")
        print(f"RESULTADO: {tentar_extrair_lembrete(t)}")
        print()
