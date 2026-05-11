"""
presenca.py
Modo presença contínua — Atlas/Lyra sempre ouvindo.
Loop com wake word: standby → detecta "atlas"/"lyra" → ouve comando → processa → falar → standby
Grace period de 30s: após wake word, aceita comandos diretos sem repetir a chamada.
"""

import asyncio
import time
from voz.entrada import ouvir
from voz.saida import falar
import httpx

_ATIVO = False
_PRESENCE = "atlas"
_API_URL = "http://127.0.0.1:8000"
_GRACE_PERIOD = 30


def definir_presence(presence: str):
    global _PRESENCE
    _PRESENCE = presence


def esta_ativo() -> bool:
    return _ATIVO


async def _processar(comando: str) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{_API_URL}/chat/{_PRESENCE}",
            json={"texto": comando, "presence": _PRESENCE},
        )
        return r.json().get("resposta", "")


async def iniciar_presenca():
    global _ATIVO
    _ATIVO = True
    print("[Presença] Standby — aguardando wake word (atlas / lyra)")

    ultimo_wake = 0.0

    while _ATIVO:
        try:
            texto = ouvir()
            if texto == "__silencio__":
                continue

            texto_lower = texto.lower()
            agora = time.monotonic()

            _wake_atlas = any(w in texto_lower for w in ("atlas", "atlas,", "atleis"))
            _wake_lyra  = any(w in texto_lower for w in ("lyra", "lyra,", "lira", "lira,"))

            if _wake_atlas:
                definir_presence("atlas")
                ultimo_wake = agora
                if len(texto.split()) <= 2:
                    print("[Presença] Wake word 'atlas' — ouvindo comando...")
                    comando = ouvir()
                    if comando == "__silencio__":
                        continue
                else:
                    comando = texto

            elif _wake_lyra:
                definir_presence("lyra")
                ultimo_wake = agora
                if len(texto.split()) <= 2:
                    print("[Presença] Wake word 'lyra' — ouvindo comando...")
                    comando = ouvir()
                    if comando == "__silencio__":
                        continue
                else:
                    comando = texto

            elif agora - ultimo_wake < _GRACE_PERIOD:
                # Dentro do grace period — trata como comando direto sem wake word
                comando = texto
                ultimo_wake = agora  # renova o grace period

            else:
                # Sem wake word e fora do grace period — ignora silenciosamente
                continue

            resposta = await _processar(comando)
            if resposta:
                try:
                    falar(resposta, presence=_PRESENCE)
                except Exception as e:
                    print(f"[Presença] Erro ao falar: {e}")

        except Exception as e:
            print(f"[Presença] Erro: {e}")
            await asyncio.sleep(1)


def parar_presenca():
    global _ATIVO
    _ATIVO = False
    print("[Presença] Modo contínuo encerrado.")
