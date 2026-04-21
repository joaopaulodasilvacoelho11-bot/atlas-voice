"""
Atlas Voice — Módulo de Tratamento de Erros Global
Captura, loga e recupera erros sem derrubar o sistema.
"""

import logging
import traceback
from datetime import datetime
from pathlib import Path
from config import DIRS

# ---------------------------------------------------------------------------
# Configuração do logger
# ---------------------------------------------------------------------------

LOG_DIR = DIRS["data"] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "atlas_erros.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger("atlas")


# ---------------------------------------------------------------------------
# Funções de log
# ---------------------------------------------------------------------------

def log_erro(contexto: str, erro: Exception) -> None:
    """Registra um erro no arquivo de log com contexto."""
    logger.error(f"[{contexto}] {type(erro).__name__}: {erro}")
    logger.error(traceback.format_exc())


def log_aviso(contexto: str, mensagem: str) -> None:
    """Registra um aviso no log."""
    logger.warning(f"[{contexto}] {mensagem}")


def log_info(contexto: str, mensagem: str) -> None:
    """Registra uma informação no log."""
    logger.info(f"[{contexto}] {mensagem}")


# ---------------------------------------------------------------------------
# Decorador de segurança — envolve qualquer função com proteção
# ---------------------------------------------------------------------------

def seguro(contexto: str, fallback: str = "Ocorreu um erro interno. Tente novamente."):
    """
    Decorador que protege uma função de erros não tratados.
    Em caso de erro: loga, retorna mensagem de fallback, não derruba o sistema.

    Uso:
        @seguro("alarmes")
        def criar_alarme(...):
            ...
    """
    def decorador(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_erro(contexto, e)
                return fallback
        return wrapper
    return decorador


# ---------------------------------------------------------------------------
# Proteção do loop principal
# ---------------------------------------------------------------------------

def executar_com_protecao(func, contexto: str, *args, **kwargs):
    """
    Executa uma função com proteção total.
    Retorna None em caso de erro — nunca lança exceção para o chamador.

    Uso no main.py:
        resposta = executar_com_protecao(_processar, "processar", texto, respondente)
        if resposta is None:
            resposta = ("Não consegui processar isso. Tente de outra forma.", "erro", respondente)
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_erro(contexto, e)
        return None


# ---------------------------------------------------------------------------
# Verificação de integridade dos JSONs
# ---------------------------------------------------------------------------

def verificar_json(caminho: Path, contexto: str) -> bool:
    """
    Verifica se um arquivo JSON existe e está íntegro.
    Loga aviso se houver problema.
    Retorna True se ok, False se corrompido ou inexistente.
    """
    import json
    if not caminho.exists():
        log_aviso(contexto, f"Arquivo não encontrado: {caminho}")
        return False
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        log_erro(contexto, e)
        log_aviso(contexto, f"JSON corrompido: {caminho} — será tratado como vazio.")
        return False


# ---------------------------------------------------------------------------
# Relatório de saúde do sistema
# ---------------------------------------------------------------------------

def relatorio_saude() -> str:
    """
    Verifica os arquivos críticos do sistema e retorna um relatório.
    Útil para diagnóstico rápido.
    """
    from config import DIRS
    import json

    arquivos_criticos = [
        DIRS["data"] / "usuarios.json",
        DIRS["data"] / "alarmes.json",
        DIRS["data"] / "lembretes.json",
        DIRS["data"] / "historico.json",
        DIRS["data"] / "sessao.json",
    ]

    linhas = ["--- Saúde do Sistema ---"]
    tudo_ok = True

    for arquivo in arquivos_criticos:
        if not arquivo.exists():
            linhas.append(f"  [AUSENTE]  {arquivo.name}")
        else:
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    json.load(f)
                linhas.append(f"  [OK]       {arquivo.name}")
            except Exception:
                linhas.append(f"  [CORROMPIDO] {arquivo.name}")
                tudo_ok = False

    if LOG_FILE.exists():
        tamanho = LOG_FILE.stat().st_size
        linhas.append(f"  [LOG]      atlas_erros.log ({tamanho // 1024} KB)")

    linhas.append("  Sistema: OK" if tudo_ok else "  Sistema: ATENÇÃO — verifique os arquivos acima")
    return "\n".join(linhas)
