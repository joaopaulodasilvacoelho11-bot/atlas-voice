import json
from datetime import datetime
from enum import Enum
from typing import Optional

from config import DIRS

_ARQUIVO = DIRS["data"] / "lembretes.json"


class Prioridade(Enum):
    ALTA   = "Alta"
    NORMAL = "Normal"
    BAIXA  = "Baixa"


_ORDEM_PRIORIDADE = {
    Prioridade.ALTA.value:   0,
    Prioridade.NORMAL.value: 1,
    Prioridade.BAIXA.value:  2,
}


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def _carregar() -> list[dict]:
    if not _ARQUIVO.exists():
        return []
    with _ARQUIVO.open("r", encoding="utf-8") as f:
        return json.load(f)


def _salvar(lembretes: list[dict]) -> None:
    _ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    with _ARQUIVO.open("w", encoding="utf-8") as f:
        json.dump(lembretes, f, ensure_ascii=False, indent=2)


def _agora() -> datetime:
    return datetime.now().replace(second=0, microsecond=0)


def _parsear(hora: str) -> datetime:
    """Aceita HH:MM ou HH:MM DD/MM/YYYY."""
    for fmt in ("%H:%M %d/%m/%Y", "%H:%M"):
        try:
            dt = datetime.strptime(hora.strip(), fmt)
            if fmt == "%H:%M":
                dt = dt.replace(year=_agora().year, month=_agora().month, day=_agora().day)
            return dt.replace(second=0, microsecond=0)
        except ValueError:
            continue
    raise ValueError(f"Formato inválido: '{hora}'. Use HH:MM ou HH:MM DD/MM/YYYY.")


def _validar_prioridade(prioridade: str) -> str:
    valores = [p.value for p in Prioridade]
    if prioridade not in valores:
        raise ValueError(f"Prioridade inválida: '{prioridade}'. Use: {', '.join(valores)}.")
    return prioridade


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def criar_lembrete(hora: str, mensagem: str, prioridade: str = "Normal") -> dict:
    dt         = _parsear(hora)
    prioridade = _validar_prioridade(prioridade)
    lembretes  = _carregar()

    for l in lembretes:
        if l["hora"] == dt.isoformat() and l["mensagem"] == mensagem and not l["cancelado"]:
            return {"status": "duplicado", "lembrete": l}

    lembrete = {
        "hora":       dt.isoformat(),
        "mensagem":   mensagem,
        "prioridade": prioridade,
        "criado_em":  datetime.now().isoformat(timespec="seconds"),
        "notificado": False,
        "cancelado":  False,
    }
    lembretes.append(lembrete)
    _salvar(lembretes)
    return {"status": "criado", "lembrete": lembrete}


def cancelar_lembrete(hora: str) -> dict:
    dt        = _parsear(hora)
    lembretes = _carregar()
    alvo      = dt.isoformat()
    cancelados = 0

    for l in lembretes:
        if l["hora"] == alvo and not l["cancelado"]:
            l["cancelado"] = True
            cancelados += 1

    _salvar(lembretes)
    if cancelados:
        return {"status": "cancelado", "hora": alvo, "total": cancelados}
    return {"status": "nao_encontrado", "hora": alvo}


def listar_lembretes(
    incluir_cancelados: bool = False,
    prioridade: Optional[str] = None,
) -> list[dict]:
    agora     = _agora()
    hoje      = agora.date()
    lembretes = _carregar()

    resultado = []
    for l in lembretes:
        if not incluir_cancelados and l["cancelado"]:
            continue
        if l["notificado"]:
            continue
        if datetime.fromisoformat(l["hora"]).date() >= hoje:
            resultado.append(l)

    if prioridade:
        _validar_prioridade(prioridade)
        resultado = [l for l in resultado if l["prioridade"] == prioridade]

    return sorted(
        resultado,
        key=lambda l: (_ORDEM_PRIORIDADE.get(l["prioridade"], 99), l["hora"]),
    )


def verificar_lembretes() -> list[dict]:
    agora     = _agora()
    lembretes = _carregar()
    ativos    = []

    for l in lembretes:
        if l["cancelado"] or l["notificado"]:
            continue
        if datetime.fromisoformat(l["hora"]) <= agora:
            l["notificado"] = True
            ativos.append(l)

    if ativos:
        _salvar(lembretes)

    return sorted(
        ativos,
        key=lambda l: _ORDEM_PRIORIDADE.get(l["prioridade"], 99),
    )
