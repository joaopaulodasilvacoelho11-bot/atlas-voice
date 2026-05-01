# Atlas Voice — API FastAPI
# Ponte entre o dashboard HTML e os núcleos Atlas/Lyra
# Rodar: uvicorn api:app --reload --port 8000

import sys
import os
from datetime import datetime
import time
import json
import json

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

# ── Memória de sessão + persistência ──────────────────────────
_MAX_HISTORICO = 10
_historico: dict = {"atlas": [], "lyra": []}
_sessao_inicio = datetime.now()
_MEMORIA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "memoria_sessao.json")


def _carregar_memoria():
    try:
        if os.path.exists(_MEMORIA_FILE):
            with open(_MEMORIA_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                _historico["atlas"] = dados.get("atlas", [])[-_MAX_HISTORICO*2:]
                _historico["lyra"]  = dados.get("lyra",  [])[-_MAX_HISTORICO*2:]
    except Exception:
        pass


def _salvar_memoria():
    try:
        os.makedirs(os.path.dirname(_MEMORIA_FILE), exist_ok=True)
        with open(_MEMORIA_FILE, "w", encoding="utf-8") as f:
            json.dump(_historico, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _adicionar_historico(nucleo: str, role: str, texto: str):
    hist = _historico[nucleo]
    hist.append({"role": role, "content": texto})
    if len(hist) > _MAX_HISTORICO * 2:
        _historico[nucleo] = hist[-(_MAX_HISTORICO * 2):]
    _salvar_memoria()


_carregar_memoria()


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
    t0 = time.time()
    _adicionar_historico("atlas", "user", msg.texto)
    entrada  = _montar_entrada(msg.texto, "atlas")
    resposta = atlas.processar(entrada)
    _adicionar_historico("atlas", "assistant", resposta.texto)
    latencia = int((time.time() - t0) * 1000)
    return {
        "resposta":  resposta.texto,
        "nucleo":    "atlas",
        "intencao":  resposta.intencao.value,
        "executada": resposta.executada,
        "latencia_ms": latencia,
    }


@app.post("/chat/lyra")
def chat_lyra(msg: Mensagem):
    t0 = time.time()
    _adicionar_historico("lyra", "user", msg.texto)
    entrada  = _montar_entrada(msg.texto, "lyra")
    resposta = lyra.processar(entrada)
    _adicionar_historico("lyra", "assistant", resposta.texto)
    latencia = int((time.time() - t0) * 1000)
    return {
        "resposta":  resposta.texto,
        "nucleo":    "lyra",
        "intencao":  resposta.intencao.value,
        "executada": resposta.executada,
        "latencia_ms": latencia,
    }


@app.post("/alarme")
def criar_alarme(msg: Mensagem):
    """Cria um alarme real via módulo de alarmes."""
    try:
        from funcionalidades.alarmes import criar_alarme as _criar_alarme
        resultado = _criar_alarme(msg.texto)
        return {"status": "criado", "detalhe": str(resultado)}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}


@app.post("/voz/ouvir")
def voz_ouvir():
    """Ativa o microfone, captura voz e retorna o texto transcrito."""
    try:
        from voz.entrada import ouvir
        texto = ouvir()
        if texto == "__silencio__":
            return {"status": "silencio", "texto": ""}
        return {"status": "ok", "texto": texto}
    except Exception as e:
        return {"status": "erro", "texto": "", "detalhe": str(e)}


@app.post("/sessao/resetar")
def resetar_sessao():
    global _sessao_inicio
    _historico["atlas"].clear()
    _historico["lyra"].clear()
    _sessao_inicio = datetime.now()
    return {"status": "sessao_resetada"}
