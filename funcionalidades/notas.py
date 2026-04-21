# ============================================
# Atlas Voice - Funcionalidades
# Notas Rápidas
# ============================================

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import DIRS

_ARQUIVO = DIRS["data"] / "notas.json"


def _carregar() -> list:
    if not _ARQUIVO.exists():
        return []
    with _ARQUIVO.open("r", encoding="utf-8") as f:
        return json.load(f)


def _salvar(notas: list) -> None:
    _ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    with _ARQUIVO.open("w", encoding="utf-8") as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)


def _agora() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def criar_nota(texto: str) -> str:
    if not texto.strip():
        return "Nota vazia. Nada foi salvo."

    notas = _carregar()
    nota = {
        "id":        len(notas) + 1,
        "texto":     texto.strip(),
        "criada_em": _agora(),
    }
    notas.append(nota)
    _salvar(notas)
    return f"Nota salva: '{texto.strip()}'."


def listar_notas() -> str:
    notas = _carregar()
    if not notas:
        return "Nenhuma nota salva."

    linhas = ["Suas notas:"]
    for n in notas:
        data = n["criada_em"][:10]
        linhas.append(f"  {n['id']}. [{data}] {n['texto']}")
    return "\n".join(linhas)


def apagar_nota(id_nota: int) -> str:
    notas = _carregar()
    encontrada = [n for n in notas if n["id"] == id_nota]

    if not encontrada:
        return f"Nota {id_nota} não encontrada."

    notas = [n for n in notas if n["id"] != id_nota]
    _salvar(notas)
    return f"Nota {id_nota} apagada."


def apagar_todas_notas() -> str:
    _salvar([])
    return "Todas as notas foram apagadas."
