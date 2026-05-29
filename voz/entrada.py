import os
import wave
import tempfile
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

TAXA_AMOSTRAGEM = 16000
DURACAO_CHUNK = 0.1
SILENCIO_APOS_FALA = 1.0
DURACAO_MAXIMA = 15
LIMIAR_ENERGIA = 0.01

_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ouvir() -> str:
    print("[ATLAS] Ouvindo...")

    amostras_chunk = int(TAXA_AMOSTRAGEM * DURACAO_CHUNK)
    max_chunks = int(DURACAO_MAXIMA / DURACAO_CHUNK)
    chunks_silencio_max = int(SILENCIO_APOS_FALA / DURACAO_CHUNK)

    gravando = []
    chunks_silencio = 0
    fala_iniciada = False

    with sd.InputStream(samplerate=TAXA_AMOSTRAGEM, channels=1, dtype="float32") as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(amostras_chunk)
            audio_chunk = chunk[:, 0]
            energia = np.mean(np.abs(audio_chunk))

            if energia > LIMIAR_ENERGIA:
                fala_iniciada = True
                chunks_silencio = 0
                gravando.append(audio_chunk)
            elif fala_iniciada:
                gravando.append(audio_chunk)
                chunks_silencio += 1
                if chunks_silencio >= chunks_silencio_max:
                    break

    if not fala_iniciada or len(gravando) == 0:
        print("[ATLAS] Nenhuma voz detectada.")
        return ""

    audio_final = np.concatenate(gravando)
    audio_int16 = (audio_final * 32767).astype(np.int16)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
        with wave.open(tmp_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(TAXA_AMOSTRAGEM)
            wf.writeframes(audio_int16.tobytes())

    try:
        with open(tmp_path, "rb") as audio_file:
            transcricao = _groq.audio.transcriptions.create(
                file=("audio.wav", audio_file.read()),
                model="whisper-large-v3-turbo",
                language="pt",
                response_format="text",
                prompt="Atlas, Lyra"
            )
        texto = transcricao.strip() if isinstance(transcricao, str) else transcricao.text.strip()
        print(f"[ATLAS] Transcrito: {texto}")
        return texto
    except Exception as e:
        print(f"[ERRO] Groq falhou: {e}")
        return ""
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    resultado = ouvir()
    print(f"Resultado: {resultado}")
