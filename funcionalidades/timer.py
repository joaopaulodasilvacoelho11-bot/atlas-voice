# ============================================
# Atlas Voice - Funcionalidades
# Timer Regressivo
# ============================================

import time
import threading
from typing import Optional

_timer_thread: Optional[threading.Thread] = None
_cancelado = False
_ativo = False
_fim: Optional[float] = None


def iniciar_timer(segundos: int, callback=None) -> str:
    global _timer_thread, _cancelado, _ativo, _fim

    if _ativo:
        restante = tempo_restante_timer()
        return f"Já existe um timer ativo. {restante}"

    if segundos <= 0:
        return "Tempo inválido. Use um valor maior que zero."

    _cancelado = False
    _ativo = True
    _fim = time.time() + segundos

    def _executar():
        global _ativo
        time.sleep(segundos)
        if not _cancelado:
            _ativo = False
            if callback:
                callback()
            else:
                print(f"\n⏰ [ATLAS] Timer encerrado. Tempo esgotado.")

    _timer_thread = threading.Thread(target=_executar, daemon=True)
    _timer_thread.start()

    return f"Timer iniciado: {_formatar(segundos)}."


def cancelar_timer() -> str:
    global _cancelado, _ativo, _fim

    if not _ativo:
        return "Nenhum timer ativo."

    _cancelado = True
    _ativo = False
    _fim = None
    return "Timer cancelado."


def tempo_restante_timer() -> str:
    global _ativo, _fim

    if not _ativo or _fim is None:
        return "Nenhum timer ativo."

    restante = _fim - time.time()
    if restante <= 0:
        return "Timer encerrando."

    return f"Tempo restante: {_formatar(int(restante))}"


def _formatar(segundos: int) -> str:
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60

    if h > 0:
        return f"{h}h {m}min {s}s"
    elif m > 0:
        return f"{m}min {s}s"
    else:
        return f"{s}s"
