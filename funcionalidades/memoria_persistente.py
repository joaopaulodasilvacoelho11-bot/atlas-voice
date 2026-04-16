import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import DIRS

_ARQUIVO = DIRS["data"] / "memoria.json"

_ESTRUTURA_PADRAO = {
    "identidade_viva": {
        "nome_usuario": "JP",
        "projeto":      "Atlas Voice",
        "versao":       "v1",
        "primeira_sessao": None,
        "total_sessoes":   0,
    },
    "ultima_sessao": {
        "inicio":   None,
        "fim":      None,
        "total_interacoes": 0,
    },
    "padroes_usuario": {
        "intencoes_frequentes": {},
        "horarios_ativos":      [],
        "temas_recorrentes":    [],
    },
    "historico": [],
}


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def _carregar_arquivo() -> dict:
    if not _ARQUIVO.exists():
        return json.loads(json.dumps(_ESTRUTURA_PADRAO))
    with _ARQUIVO.open("r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_arquivo(dados: dict) -> None:
    _ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    with _ARQUIVO.open("w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def _agora() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def salvar_sessao(inicio: Optional[str] = None, fim: Optional[str] = None) -> None:
    dados = _carregar_arquivo()

    if dados["identidade_viva"]["primeira_sessao"] is None:
        dados["identidade_viva"]["primeira_sessao"] = inicio or _agora()

    dados["identidade_viva"]["total_sessoes"] += 1

    dados["ultima_sessao"]["inicio"] = inicio or _agora()
    dados["ultima_sessao"]["fim"]    = fim or _agora()
    dados["ultima_sessao"]["total_interacoes"] = sum(
        1 for item in dados["historico"]
        if item.get("sessao") == dados["identidade_viva"]["total_sessoes"]
    )

    _salvar_arquivo(dados)


def carregar_sessao() -> dict:
    dados = _carregar_arquivo()
    return {
        "identidade_viva": dados["identidade_viva"],
        "ultima_sessao":   dados["ultima_sessao"],
        "padroes_usuario": dados["padroes_usuario"],
    }


def registrar_interacao(
    texto_usuario: str,
    resposta: str,
    intencao: str,
    respondente: str,
) -> None:
    dados = _carregar_arquivo()

    sessao_atual = dados["identidade_viva"]["total_sessoes"]

    entrada = {
        "timestamp":   _agora(),
        "sessao":      sessao_atual,
        "usuario":     texto_usuario,
        "resposta":    resposta,
        "intencao":    intencao,
        "respondente": respondente,
    }
    dados["historico"].append(entrada)

    # Atualiza padrões: contagem de intenções
    freq = dados["padroes_usuario"]["intencoes_frequentes"]
    freq[intencao] = freq.get(intencao, 0) + 1

    # Atualiza horários ativos (hora cheia)
    hora = datetime.now().strftime("%H:00")
    if hora not in dados["padroes_usuario"]["horarios_ativos"]:
        dados["padroes_usuario"]["horarios_ativos"].append(hora)

    _salvar_arquivo(dados)


def obter_historico(
    limite: Optional[int] = None,
    intencao: Optional[str] = None,
    respondente: Optional[str] = None,
) -> list[dict]:
    dados    = _carregar_arquivo()
    historico = dados["historico"]

    if intencao:
        historico = [h for h in historico if h.get("intencao") == intencao]
    if respondente:
        historico = [h for h in historico if h.get("respondente") == respondente]
    if limite:
        historico = historico[-limite:]

    return historico
