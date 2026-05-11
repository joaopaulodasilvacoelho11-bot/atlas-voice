# Atlas Voice — API FastAPI
# Ponte entre o dashboard HTML e os núcleos Atlas/Lyra
# Rodar: uvicorn api:app --reload --port 8000

import sys
import os
from datetime import datetime
from contextlib import asynccontextmanager
import asyncio
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from nucleos.atlas_nucleo import AtlasNucleo, Entrada, Intencao
from nucleos.lyra_nucleo import LyraNucleo
from pipeline.base_2_5_classificador_intencao_oficial import classificar


# ── Degrau 3 — Loop de verificação backend ────────────────────
async def _loop_verificacao():
    """Verifica alarmes e lembretes a cada 30s, independente do dashboard."""
    while True:
        await asyncio.sleep(30)
        # Alarmes
        try:
            from funcionalidades.alarmes import verificar_alarmes as _ver_alarmes
            disparados_a = _ver_alarmes()
            for item in disparados_a:
                try:
                    from voz.saida import falar
                    falar(item.get("mensagem", "Alarme!"), presence="atlas")
                except Exception:
                    pass
        except Exception:
            pass
        # Lembretes
        try:
            from funcionalidades.lembretes import verificar_lembretes as _ver_lembretes
            disparados_l = _ver_lembretes()
            for item in disparados_l:
                try:
                    from voz.saida import falar
                    falar(item.get("mensagem", "Lembrete!"), presence="lyra")
                except Exception:
                    pass
        except Exception:
            pass


@asynccontextmanager
async def lifespan(app):
    task = asyncio.create_task(_loop_verificacao())
    yield
    task.cancel()


# ── App ───────────────────────────────────────────────────────
app = FastAPI(title="Atlas Voice API", version="1.0", lifespan=lifespan)

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
    presence: str = "atlas"


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

    # Degrau 1: Alarme real via IA
    texto_final = resposta.texto
    alarme_criado = None
    try:
        from funcionalidades.extrator_alarme import tentar_extrair_alarme
        from funcionalidades.alarmes import criar_alarme as _criar_alarme
        dados = tentar_extrair_alarme(msg.texto)
        if dados:
            resultado = _criar_alarme(dados["horario"], dados["mensagem"])
            alarme_criado = resultado
            horario = dados["horario"]
            if "alarme" not in resposta.texto.lower() and horario not in resposta.texto:
                texto_final = resposta.texto + f"\nAlarme registrado para {horario}."
    except Exception:
        pass

    # Degrau 2: Lembrete real via IA
    lembrete_criado = None
    try:
        from funcionalidades.extrator_lembrete import tentar_extrair_lembrete
        from funcionalidades.lembretes import criar_lembrete as _criar_lembrete
        dados_l = tentar_extrair_lembrete(msg.texto)
        if dados_l:
            resultado_l = _criar_lembrete(dados_l["horario"], dados_l["mensagem"], dados_l["prioridade"])
            lembrete_criado = resultado_l
            texto_final = f"Lembrete registrado para {dados_l['horario']}: {dados_l['mensagem']}."
    except Exception:
        pass

    return {
        "resposta":        texto_final,
        "nucleo":         "atlas",
        "intencao":       resposta.intencao.value,
        "executada":      resposta.executada,
        "latencia_ms":    latencia,
        "alarme_criado":  alarme_criado,
        "lembrete_criado": lembrete_criado,
    }


@app.post("/chat/lyra")
def chat_lyra(msg: Mensagem):
    t0 = time.time()
    _adicionar_historico("lyra", "user", msg.texto)
    entrada  = _montar_entrada(msg.texto, "lyra")
    resposta = lyra.processar(entrada)
    _adicionar_historico("lyra", "assistant", resposta.texto)
    latencia = int((time.time() - t0) * 1000)

    # Degrau 1: Alarme real via IA
    alarme_criado = None
    try:
        from funcionalidades.extrator_alarme import tentar_extrair_alarme
        from funcionalidades.alarmes import criar_alarme as _criar_alarme
        dados = tentar_extrair_alarme(msg.texto)
        if dados:
            resultado = _criar_alarme(dados["horario"], dados["mensagem"])
            alarme_criado = resultado
    except Exception:
        pass

    # Degrau 2: Lembrete real via IA
    texto_final = resposta.texto
    lembrete_criado = None
    try:
        from funcionalidades.extrator_lembrete import tentar_extrair_lembrete
        from funcionalidades.lembretes import criar_lembrete as _criar_lembrete
        dados_l = tentar_extrair_lembrete(msg.texto)
        if dados_l:
            resultado_l = _criar_lembrete(dados_l["horario"], dados_l["mensagem"], dados_l["prioridade"])
            lembrete_criado = resultado_l
            texto_final = f"Lembrete registrado para {dados_l['horario']}: {dados_l['mensagem']}."
    except Exception:
        pass

    return {
        "resposta":        texto_final,
        "nucleo":          "lyra",
        "intencao":        resposta.intencao.value,
        "executada":       resposta.executada,
        "latencia_ms":     latencia,
        "alarme_criado":   alarme_criado,
        "lembrete_criado": lembrete_criado,
    }


class MensagemAlarme(BaseModel):
    horario: str
    mensagem: str = "Alarme Atlas Voice"


@app.post("/alarme")
def criar_alarme(dados: MensagemAlarme):
    """Cria um alarme real via módulo de alarmes."""
    try:
        from funcionalidades.alarmes import criar_alarme as _criar_alarme
        resultado = _criar_alarme(dados.horario, dados.mensagem)
        return resultado
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}


@app.get("/alarmes")
def listar_alarmes():
    """Lista alarmes ativos."""
    try:
        from funcionalidades.alarmes import listar_alarmes as _listar
        return {"alarmes": _listar()}
    except Exception as e:
        return {"alarmes": [], "erro": str(e)}


@app.post("/alarmes/verificar")
def verificar_alarmes():
    """Verifica e dispara alarmes que chegaram no horário."""
    try:
        from funcionalidades.alarmes import verificar_alarmes as _verificar
        disparados = _verificar()
        return {"disparados": disparados, "total": len(disparados)}
    except Exception as e:
        return {"disparados": [], "erro": str(e)}


class MensagemLembrete(BaseModel):
    horario: str
    mensagem: str = "Lembrete Atlas Voice"
    prioridade: str = "Normal"


@app.post("/lembrete")
def criar_lembrete_endpoint(dados: MensagemLembrete):
    try:
        from funcionalidades.lembretes import criar_lembrete as _criar_lembrete
        return _criar_lembrete(dados.horario, dados.mensagem, dados.prioridade)
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}


@app.get("/lembretes")
def listar_lembretes_endpoint():
    try:
        from funcionalidades.lembretes import listar_lembretes as _listar
        return {"lembretes": _listar()}
    except Exception as e:
        return {"lembretes": [], "erro": str(e)}


@app.post("/lembretes/verificar")
def verificar_lembretes_endpoint():
    try:
        from funcionalidades.lembretes import verificar_lembretes as _verificar
        disparados = _verificar()
        return {"disparados": disparados, "total": len(disparados)}
    except Exception as e:
        return {"disparados": [], "erro": str(e)}


@app.post("/voz/falar")
def voz_falar(msg: Mensagem):
    """Converte texto em voz via ElevenLabs e reproduz."""
    try:
        from voz.saida import falar
        falar(msg.texto, presence=msg.presence)
        return {"status": "ok"}
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
