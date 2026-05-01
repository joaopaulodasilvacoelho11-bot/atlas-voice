# Atlas Voice — API FastAPI
# Ponte entre o dashboard HTML e os núcleos Atlas/Lyra
# Rodar: uvicorn api:app --reload --port 8000

import sys
import os

# Garante que o projeto está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from nucleos.atlas_nucleo import AtlasNucleo, Entrada, Intencao
from nucleos.lyra_nucleo import LyraNucleo
from pipeline.base_2_5_classificador_intencao_oficial import classificar, Intencao as IntencaoPipeline

app = FastAPI(title="Atlas Voice API", version="1.0")

# CORS — permite o dashboard HTML (file://) chamar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

atlas = AtlasNucleo()
lyra  = LyraNucleo()


class Mensagem(BaseModel):
    texto: str


def _montar_entrada(texto: str) -> Entrada:
    """Classifica a intenção e monta o objeto Entrada."""
    try:
        resultado  = classificar(texto)
        # Mapeia Intencao do pipeline para Intencao dos núcleos
        mapa = {
            "saudacao":      Intencao.SAUDACAO,
            "lembrete":      Intencao.LEMBRETE,
            "pergunta":      Intencao.PERGUNTA,
            "comando":       Intencao.COMANDO,
            "conversa":      Intencao.CONVERSA,
            "fora_de_escopo": Intencao.DESCONHECIDA,
        }
        intencao = mapa.get(resultado.intencao.value, Intencao.DESCONHECIDA)
    except Exception:
        intencao = Intencao.DESCONHECIDA
    return Entrada(texto=texto, intencao=intencao)


@app.get("/")
def status():
    return {"status": "online", "sistema": "Atlas Voice", "versao": "1.0"}


@app.post("/chat/atlas")
def chat_atlas(msg: Mensagem):
    entrada  = _montar_entrada(msg.texto)
    resposta = atlas.processar(entrada)
    return {
        "resposta": resposta.texto,
        "nucleo":   "atlas",
        "intencao": resposta.intencao.value,
        "executada": resposta.executada,
    }


@app.post("/chat/lyra")
def chat_lyra(msg: Mensagem):
    entrada  = _montar_entrada(msg.texto)
    resposta = lyra.processar(entrada)
    return {
        "resposta": resposta.texto,
        "nucleo":   "lyra",
        "intencao": resposta.intencao.value,
        "executada": resposta.executada,
    }
