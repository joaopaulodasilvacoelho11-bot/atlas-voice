import json
from datetime import datetime, timedelta
from typing import Optional

from config import DIRS

_ARQUIVO = DIRS["data"] / "alarmes.json"


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def _carregar() -> list[dict]:
    if not _ARQUIVO.exists():
        return []
    with _ARQUIVO.open("r", encoding="utf-8") as f:
        return json.load(f)


def _salvar(alarmes: list[dict]) -> None:
    _ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    with _ARQUIVO.open("w", encoding="utf-8") as f:
        json.dump(alarmes, f, ensure_ascii=False, indent=2)


def _agora() -> datetime:
    return datetime.now().replace(second=0, microsecond=0)


def _parsear(horario: str) -> datetime:
    """Aceita HH:MM ou HH:MM DD/MM/YYYY.
    Se apenas HH:MM for fornecido e o horário já passou hoje, agenda para amanhã."""
    horario = horario.strip()
    try:
        dt = datetime.strptime(horario, "%H:%M %d/%m/%Y")
        return dt.replace(second=0, microsecond=0)
    except ValueError:
        pass
    try:
        agora = _agora()
        dt = datetime.strptime(horario, "%H:%M").replace(
            year=agora.year, month=agora.month, day=agora.day,
            second=0, microsecond=0,
        )
        if dt <= agora:
            dt += timedelta(days=1)
        return dt
    except ValueError:
        pass
    raise ValueError(f"Formato de horário inválido: '{horario}'. Use HH:MM ou HH:MM DD/MM/YYYY.")


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def criar_alarme(horario: str, mensagem: str) -> dict:
    dt      = _parsear(horario)
    alarmes = _carregar()

    for a in alarmes:
        if a["horario"] == dt.isoformat() and not a["cancelado"]:
            return {"status": "duplicado", "alarme": a}

    alarme = {
        "horario":   dt.isoformat(),
        "mensagem":  mensagem,
        "criado_em": datetime.now().isoformat(timespec="seconds"),
        "disparado": False,
        "cancelado": False,
    }
    alarmes.append(alarme)
    _salvar(alarmes)
    return {"status": "criado", "alarme": alarme}


def cancelar_alarme(horario: str) -> dict:
    dt      = _parsear(horario)
    alarmes = _carregar()
    alvo    = dt.isoformat()
    cancelados = 0

    for a in alarmes:
        if a["horario"] == alvo and not a["cancelado"]:
            a["cancelado"] = True
            cancelados += 1

    _salvar(alarmes)
    if cancelados:
        return {"status": "cancelado", "horario": alvo, "total": cancelados}
    return {"status": "nao_encontrado", "horario": alvo}


def listar_alarmes(incluir_cancelados: bool = False) -> list[dict]:
    agora   = _agora()
    hoje    = agora.date()
    alarmes = _carregar()

    resultado = []
    for a in alarmes:
        if not incluir_cancelados and a["cancelado"]:
            continue
        if a["disparado"]:
            continue
        dt = datetime.fromisoformat(a["horario"])
        if dt.date() >= hoje:
            resultado.append(a)

    return sorted(resultado, key=lambda a: a["horario"])


def verificar_alarmes() -> list[dict]:
    agora   = _agora()
    alarmes = _carregar()
    disparar = []

    for a in alarmes:
        if a["cancelado"] or a["disparado"]:
            continue
        if datetime.fromisoformat(a["horario"]) <= agora:
            a["disparado"] = True
            disparar.append(a)

    if disparar:
        _salvar(alarmes)

    return disparar
