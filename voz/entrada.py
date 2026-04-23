import whisper
import sounddevice as sd
import tempfile
import scipy.io.wavfile as wav
import imageio_ffmpeg
import numpy as np
import os
import shutil

# Copia o ffmpeg do imageio para um local com nome correto
_ffmpeg_src = imageio_ffmpeg.get_ffmpeg_exe()
_ffmpeg_dir = os.path.dirname(_ffmpeg_src)
_ffmpeg_dst = os.path.join(_ffmpeg_dir, "ffmpeg.exe")

if not os.path.exists(_ffmpeg_dst):
    shutil.copy(_ffmpeg_src, _ffmpeg_dst)

os.environ["PATH"] = _ffmpeg_dir + os.pathsep + os.environ["PATH"]

# Carrega modelo Whisper
modelo = whisper.load_model("base")

def ouvir() -> str:
    DURACAO = 5
    TAXA = 16000
    LIMIAR_SILENCIO = 200  # energia mínima para considerar que há fala

    print("[Atlas] Ouvindo...")
    audio = sd.rec(int(DURACAO * TAXA), samplerate=TAXA, channels=1, dtype='int16')
    sd.wait()
    print("[Atlas] Processando...")

    # Verifica energia do áudio — ignora silêncio
    energia = np.abs(audio).mean()
    if energia < LIMIAR_SILENCIO:
        return "__silencio__"

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        nome_arquivo = f.name
        wav.write(nome_arquivo, TAXA, audio)

    resultado = modelo.transcribe(nome_arquivo, language="pt", fp16=False)
    texto = resultado["text"].strip()

    if not texto or len(texto) < 2:
        return "__silencio__"

    print(f"[Atlas] Você disse: {texto}")
    return texto