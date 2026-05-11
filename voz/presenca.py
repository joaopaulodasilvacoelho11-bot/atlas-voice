"""
presenca.py
Modo presença contínua — Atlas/Lyra sempre ouvindo.
Loop: ouvir → processar → falar → ouvir...
"""

import asyncio
from voz.entrada import ouvir
from voz.saida import falar
import httpx

_ATIVO = False
_PRESENCE = "atlas"
_API_URL = "http://127.0.0.1:8000"


def definir_presence(presence: str):
    global _PRESENCE
    _PRESENCE = presence


def esta_ativo() -> bool:
    return _ATIVO


async def iniciar_presenca():
    global _ATIVO
    _ATIVO = True
    print(f"[Presença] Modo contínuo ativo — {_PRESENCE}")
    while _ATIVO:
        try:
            texto = ouvir()
            if texto == "__silencio__":
                continue
            async with httpx.AsyncClient(timeout=30) as client:
                endpoint = f"{_API_URL}/chat/{_PRESENCE}"
                r = await client.post(endpoint, json={"texto": texto, "presence": _PRESENCE})
                dados = r.json()
                resposta = dados.get("resposta", "")
                if resposta:
                    falar(resposta, presence=_PRESENCE)
        except Exception as e:
            print(f"[Presença] Erro: {e}")
            await asyncio.sleep(1)


def parar_presenca():
    global _ATIVO
    _ATIVO = False
    print("[Presença] Modo contínuo encerrado.")
