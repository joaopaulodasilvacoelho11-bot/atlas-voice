import whisper
import sounddevice as sd
import tempfile
import scipy.io.wavfile as wav
import imageio_ffmpeg
import numpy as np
import os
import shutil
import torch
import re as _re

# Copia o ffmpeg do imageio para um local com nome correto
_ffmpeg_src = imageio_ffmpeg.get_ffmpeg_exe()
_ffmpeg_dir = os.path.dirname(_ffmpeg_src)
_ffmpeg_dst = os.path.join(_ffmpeg_dir, "ffmpeg.exe")

if not os.path.exists(_ffmpeg_dst):
    shutil.copy(_ffmpeg_src, _ffmpeg_dst)

os.environ["PATH"] = _ffmpeg_dir + os.pathsep + os.environ["PATH"]

# Carrega modelo Whisper
modelo = whisper.load_model("small")

# Carrega modelo Silero VAD
_vad_model, _vad_utils = torch.hub.load(
    repo_or_dir="snakers4/silero-vad",
    model="silero_vad",
    force_reload=False,
    trust_repo=True,
)
(get_speech_timestamps, _, read_audio, *_) = _vad_utils

TAXA = 16000
SILENCIO_APOS_FALA = 1.5   # segundos de silêncio para encerrar
DURACAO_MAXIMA    = 15      # segundos máximos de captura
CHUNK             = 512     # frames por chunk (~32ms a 16kHz)


def ouvir() -> str:
    print("[Atlas] Ouvindo...")

    gravando        = False
    audio_capturado = []
    chunks_silencio = 0
    chunks_maximos  = int(DURACAO_MAXIMA * TAXA / CHUNK)
    limiar_silencio = int(SILENCIO_APOS_FALA * TAXA / CHUNK)
    total_chunks    = 0

    with sd.InputStream(samplerate=TAXA, channels=1, dtype="float32", blocksize=CHUNK) as stream:
        while total_chunks < chunks_maximos:
            chunk_audio, _ = stream.read(CHUNK)
            chunk_np = chunk_audio[:, 0]

            # Silero VAD — detecta se há fala neste chunk
            tensor = torch.tensor(chunk_np, dtype=torch.float32)
            prob   = _vad_model(tensor, TAXA).item()
            tem_fala = prob > 0.5

            if tem_fala:
                if not gravando:
                    print("[Atlas] Fala detectada...")
                    gravando = True
                audio_capturado.append(chunk_np)
                chunks_silencio = 0
            elif gravando:
                audio_capturado.append(chunk_np)
                chunks_silencio += 1
                if chunks_silencio >= limiar_silencio:
                    break

            total_chunks += 1

    if not audio_capturado:
        return "__silencio__"

    print("[Atlas] Processando...")
    audio_final = np.concatenate(audio_capturado)
    audio_int16 = (audio_final * 32767).astype(np.int16)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        nome_arquivo = f.name
        wav.write(nome_arquivo, TAXA, audio_int16)

    resultado = modelo.transcribe(nome_arquivo, language="pt", fp16=False)
    texto = resultado["text"].strip()

    # Filtro de transcrição suja
    if _re.search(r'[^\x00-\x7Fàáâãäéêíóôõúüçñ\s]', texto):
        return "__silencio__"

    if not texto or len(texto) < 2:
        return "__silencio__"

    print(f"[Atlas] Você disse: {texto}")
    return texto
