# Atlas Voice — API FastAPI
# Ponte entre o dashboard HTML e os núcleos Atlas/Lyra
# Rodar: uvicorn api:app --reload --port 8000

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from nucleos.atlas_nucleo import AtlasNucleo, Entrada, Intencao
from nucleos.lyra_nucleo import LyraNucleo
from pipeline.base_2_5_classificador_intencao_oficial import classificar

app = FastAPI(title="Atlas Voice API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

atlas = AtlasNucleo()
lyra  = LyraNucleo()

# ── Memória de sessão ──────────────────────────────────────────
_MAX_HISTORICO = 10
_historico: dict = {"atlas": [], "lyra": []}
_sessao_inicio = datetime.now()


def _adicionar_historico(nucleo: str, role: str, texto: str):
    hist = _historico[nucleo]
    hist.append({"role": role, "content": texto})
    if len(hist) > _MAX_HISTORICO * 2:
        _historico[nucleo] = hist[-(_MAX_HISTORICO * 2):]


class Mensagem(BaseModel):
    texto: str


def _montar_entrada(texto: str, nucleo: str) -> Entrada:
    try:
        resultado = classificar(texto)
        mapa = {
            "saudacao":       Intencao.SAUDACAO,
            "lembrete":       Intencao.LEMBRETE,
            "pergunta":       Intencao.PERGUNTA,
            "comando":        Intencao.COMANDO,
            "conversa":       Intencao.CONVERSA,
            "fora_de_escopo": Intencao.DESCONHECIDA,
        }
        intencao = mapa.get(resultado.intencao.value, Intencao.DESCONHECIDA)
    except Exception:
        intencao = Intencao.DESCONHECIDA
    # Injeta histórico nos parâmetros
    historico = list(_historico[nucleo])
    return Entrada(texto=texto, intencao=intencao, parametros={"historico": historico})


@app.get("/")
def status():
    uptime = int((datetime.now() - _sessao_inicio).total_seconds())
    return {"status": "online", "sistema": "Atlas Voice", "versao": "1.0", "uptime_segundos": uptime}


@app.get("/sessao")
def info_sessao():
    uptime = int((datetime.now() - _sessao_inicio).total_seconds())
    h = uptime // 3600
    m = (uptime % 3600) // 60
    s = uptime % 60
    return {
        "inicio": _sessao_inicio.strftime("%H:%M:%S"),
        "uptime": f"{h:02d}:{m:02d}:{s:02d}",
        "uptime_segundos": uptime,
        "mensagens_atlas": len(_historico["atlas"]) // 2,
        "mensagens_lyra":  len(_historico["lyra"])  // 2,
    }


@app.post("/chat/atlas")
def chat_atlas(msg: Mensagem):
    _adicionar_historico("atlas", "user", msg.texto)
    entrada  = _montar_entrada(msg.texto, "atlas")
    resposta = atlas.processar(entrada)
    _adicionar_historico("atlas", "assistant", resposta.texto)
    return {
        "resposta":  resposta.texto,
        "nucleo":    "atlas",
        "intencao":  resposta.intencao.value,
        "executada": resposta.executada,
    }


@app.post("/chat/lyra")
def chat_lyra(msg: Mensagem):
    _adicionar_historico("lyra", "user", msg.texto)
    entrada  = _montar_entrada(msg.texto, "lyra")
    resposta = lyra.processar(entrada)
    _adicionar_historico("lyra", "assistant", resposta.texto)
    return {
        "resposta":  resposta.texto,
        "nucleo":    "lyra",
        "intencao":  resposta.intencao.value,
        "executada": resposta.executada,
    }


@app.post("/sessao/resetar")
def resetar_sessao():
    global _sessao_inicio
    _historico["atlas"].clear()
    _historico["lyra"].clear()
    _sessao_inicio = datetime.now()
    return {"status": "sessao_resetada"}
