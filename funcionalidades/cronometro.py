# ============================================
# Atlas Voice - Funcionalidades
# Cronômetro
# ============================================

import time

_inicio = None
_pausado = False
_tempo_acumulado = 0.0


def iniciar_cronometro() -> str:
    global _inicio, _pausado, _tempo_acumulado

    if _inicio is not None and not _pausado:
        return "Cronômetro já está rodando."

    _inicio = time.time()
    _pausado = False
    return "Cronômetro iniciado."


def parar_cronometro() -> str:
    global _inicio, _pausado, _tempo_acumulado

    if _inicio is None:
        return "Nenhum cronômetro ativo."

    if _pausado:
        return "Cronômetro já está parado."

    _tempo_acumulado += time.time() - _inicio
    _pausado = True
    return f"Cronômetro parado. Tempo registrado: {_formatar(_tempo_acumulado)}"


def tempo_passado() -> str:
    global _inicio, _pausado, _tempo_acumulado

    if _inicio is None:
        return "Nenhum cronômetro ativo."

    if _pausado:
        total = _tempo_acumulado
    else:
        total = _tempo_acumulado + (time.time() - _inicio)

    return f"Tempo decorrido: {_formatar(total)}"


def zerar_cronometro() -> str:
    global _inicio, _pausado, _tempo_acumulado

    _inicio = None
    _pausado = False
    _tempo_acumulado = 0.0
    return "Cronômetro zerado."


def _formatar(segundos: float) -> str:
    segundos = int(segundos)
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60

    if h > 0:
        return f"{h}h {m}min {s}s"
    elif m > 0:
        return f"{m}min {s}s"
    else:
        return f"{s}s"
