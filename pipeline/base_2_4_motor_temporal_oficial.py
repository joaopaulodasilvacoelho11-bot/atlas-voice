import re
from datetime import date, datetime, timedelta
from typing import Optional


# ---------------------------------------------------------------------------
# Tipos de saída
# ---------------------------------------------------------------------------

def _resultado(
    dia: Optional[str] = None,
    hora: Optional[str] = None,
    periodo: Optional[str] = None,
    expressao: Optional[str] = None,
    ambiguidade: bool = False,
) -> dict:
    return {
        "dia":        dia,
        "hora":       hora,
        "periodo":    periodo,
        "expressao":  expressao,
        "ambiguidade": ambiguidade,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hoje() -> str:
    return date.today().isoformat()

def _amanha() -> str:
    return (date.today() + timedelta(days=1)).isoformat()

def _depois_amanha() -> str:
    return (date.today() + timedelta(days=2)).isoformat()

def _hora_atual() -> str:
    return datetime.now().strftime("%H:%M")

def _normalizar(texto: str) -> str:
    return texto.lower().strip()


# ---------------------------------------------------------------------------
# Padrões de extração
# ---------------------------------------------------------------------------

# Horário explícito: "8h", "às 8", "8:30", "8 da manhã", "20h30"
_RE_HORARIO = re.compile(
    r"(?:às?\s*)?(\d{1,2})(?:[h:](\d{2}))?\s*(?:da\s*(manhã|tarde|noite)|hrs?|horas?)?",
    re.IGNORECASE,
)

# Período do dia sem horário fixo
_RE_PERIODO = re.compile(
    r"\b(manhã|tarde|noite|madrugada)\b",
    re.IGNORECASE,
)

# Dia relativo
_RE_DIA = [
    (re.compile(r"\bdepois\s+de\s+amanhã\b",  re.IGNORECASE), "depois_amanha"),
    (re.compile(r"\bamanhã\b",                 re.IGNORECASE), "amanha"),
    (re.compile(r"\bhoje\b",                   re.IGNORECASE), "hoje"),
]

# Expressões vagas de tempo
_RE_EXPRESSOES_VAGAS = [
    (re.compile(r"\bdaqui\s+a\s+pouco\b",      re.IGNORECASE), "daqui_a_pouco"),
    (re.compile(r"\bmais\s+tarde\b",            re.IGNORECASE), "mais_tarde"),
    (re.compile(r"\bem\s+breve\b",              re.IGNORECASE), "em_breve"),
    (re.compile(r"\bagora\s+mesmo\b",           re.IGNORECASE), "agora_mesmo"),
    (re.compile(r"\bagora\b",                   re.IGNORECASE), "agora"),
    (re.compile(r"\bdepois\b",                  re.IGNORECASE), "depois"),
    (re.compile(r"\bmais\s+cedo\b",             re.IGNORECASE), "mais_cedo"),
]

# Mapeamento período → hora estimada (usado quando não há horário explícito)
_HORA_POR_PERIODO = {
    "manhã":     "08:00",
    "tarde":     "14:00",
    "noite":     "20:00",
    "madrugada": "02:00",
}

# Expressões vagas que não fornecem hora concreta
_EXPRESSOES_AMBIGUAS = {"daqui_a_pouco", "mais_tarde", "em_breve", "depois"}


# ---------------------------------------------------------------------------
# Motor principal
# ---------------------------------------------------------------------------

def interpretar(texto: str) -> dict:
    norm       = _normalizar(texto)
    dia        = None
    hora       = None
    periodo    = None
    expressao  = None
    ambiguidade = False

    # 1. Dia relativo
    for padrao, chave in _RE_DIA:
        if padrao.search(norm):
            if chave == "hoje":
                dia = _hoje()
            elif chave == "amanha":
                dia = _amanha()
            elif chave == "depois_amanha":
                dia = _depois_amanha()
            break

    # 2. Expressões vagas (só se não encontrou dia explícito ou complementam)
    for padrao, chave in _RE_EXPRESSOES_VAGAS:
        if padrao.search(norm):
            expressao = chave
            if chave == "agora_mesmo" or chave == "agora":
                dia  = _hoje()
                hora = _hora_atual()
            if chave in _EXPRESSOES_AMBIGUAS:
                ambiguidade = True
            break

    # 3. Horário explícito
    match = _RE_HORARIO.search(norm)
    if match:
        h   = int(match.group(1))
        min_ = match.group(2) or "00"
        turno = match.group(3)

        # Ajuste de período para AM/PM implícito
        if turno == "manhã" and h <= 12:
            periodo = "manhã"
        elif turno == "tarde":
            periodo = "tarde"
            if h < 12:
                h += 12
        elif turno == "noite":
            periodo = "noite"
            if h < 12:
                h += 12
        else:
            # Sem turno explícito: inferir por convenção
            if 1 <= h <= 5:
                periodo     = "madrugada"
                ambiguidade = True
            elif 6 <= h <= 11:
                periodo = "manhã"
            elif h == 12:
                periodo = "tarde"
            elif 13 <= h <= 17:
                periodo = "tarde"
            elif 18 <= h <= 23:
                periodo = "noite"

        hora = f"{h:02d}:{min_}"

        # Se não detectou dia ainda, assume hoje
        if dia is None:
            dia = _hoje()

    # 4. Período sem horário explícito
    if hora is None:
        match_per = _RE_PERIODO.search(norm)
        if match_per:
            periodo    = match_per.group(1).lower()
            hora       = _HORA_POR_PERIODO.get(periodo)
            ambiguidade = True          # hora estimada, não exata
            if dia is None:
                dia = _hoje()

    # 5. Sem nenhuma informação temporal
    if dia is None and hora is None and expressao is None:
        ambiguidade = True

    return _resultado(
        dia=dia,
        hora=hora,
        periodo=periodo,
        expressao=expressao,
        ambiguidade=ambiguidade,
    )
