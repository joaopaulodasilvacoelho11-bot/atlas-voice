from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

DIRS = {
    "core":             BASE_DIR / "core",
    "pipeline":         BASE_DIR / "pipeline",
    "camadas":          BASE_DIR / "camadas",
    "nucleos":          BASE_DIR / "nucleos",
    "funcionalidades":  BASE_DIR / "funcionalidades",
    "data":             BASE_DIR / "data",
}

# Subpastas de data
DATA_RAW        = DIRS["data"] / "raw"
DATA_PROCESSED  = DIRS["data"] / "processed"
DATA_OUTPUT     = DIRS["data"] / "output"

# Configurações gerais — sobrescrevíveis por variáveis de ambiente
PROJECT_NAME    = os.getenv("ATLAS_PROJECT_NAME", "atlas-voice-v1")
LOG_LEVEL       = os.getenv("ATLAS_LOG_LEVEL", "INFO")
SAMPLE_RATE     = int(os.getenv("ATLAS_SAMPLE_RATE", "16000"))
LANGUAGE        = os.getenv("ATLAS_LANGUAGE", "pt-BR")


def ensure_dirs():
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
