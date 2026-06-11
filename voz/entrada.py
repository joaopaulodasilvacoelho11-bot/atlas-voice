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
LIMIAR_ENERGIA = 0.02          # era 0.01 — ruído ambiente passa abaixo disso
DURACAO_MINIMA_FALA = 0.2      # mínimo de segundos de fala real antes de transcrever

_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Palavras que indicam fala real em português
_PALAVRAS_REAIS = {
    "atlas", "lyra", "oi", "olá", "bom", "boa", "dia", "tarde", "noite",
    "pode", "quero", "preciso", "cria", "crie", "define", "fala", "me",
    "como", "quando", "onde", "qual", "que", "sim", "não", "ok", "tudo",
    "alarme", "lembrete", "nota", "timer", "hora", "hoje", "amanhã",
    "ajuda", "obrigado", "valeu", "tchau", "para", "parar", "desativa",
    "desative", "liga", "desliga", "abre", "fecha", "mostra", "lista",
    "você", "seu", "sua", "por", "favor", "preciso", "quero", "tenho",
    "vamos", "fazer", "feito", "novo", "nova", "meu", "minha",
}

# Alucinações conhecidas do Whisper com ruído ambiente
_ALUCINACOES_CONHECIDAS = {
    "obrigado", "obrigada", "obrigado.", "obrigada.",
    "até logo", "até mais", "até logo.", "até mais.",
    "legenda", "legendas", "transcrição", "transcrição.",
    "you", "the", "a", "i", "and", "is", "in", "of", "to",
    "thank you", "thanks", "bye", "goodbye",
    "subtitles", "subtitle", "amara.org",
    ".", "..", "...", "…",
    # Whisper alucina o próprio prompt com ruído
    "atlas, lyra", "atlas, lyra.", "atlas,lyra",
    "atlas lyra", "atlas lyra.", "lyra, atlas",
    "atlas, lyra, ae", "atlas, lyra, aê",
}

def _filtrar_alucinacao(texto: str) -> bool:
    """Retorna True se o texto parece fala real. False se parece ruído/alucinação."""
    if not texto or len(texto.strip()) < 3:
        return False

    texto_lower = texto.lower().strip()

    # Alucinação conhecida exata
    if texto_lower in _ALUCINACOES_CONHECIDAS:
        print(f"[ATLAS] Filtrado (alucinação conhecida): {texto}")
        return False

    palavras = texto_lower.split()

    # Texto muito curto sem palavras reconhecíveis
    if len(palavras) <= 2:
        tem_palavra_real = any(p.rstrip(".,!?") in _PALAVRAS_REAIS for p in palavras)
        if not tem_palavra_real:
            print(f"[ATLAS] Filtrado (sem palavra real): {texto}")
            return False

    # Repetição excessiva de caracteres (ex: "aaaaaaa", "mmmmm")
    for palavra in palavras:
        if len(palavra) > 3 and len(set(palavra)) <= 2:
            print(f"[ATLAS] Filtrado (repetição): {texto}")
            return False

    # Texto em inglês puro (Whisper alucina em inglês com ruído)
    palavras_pt = sum(1 for p in palavras if p.rstrip(".,!?") in _PALAVRAS_REAIS)
    palavras_en = {"the", "a", "is", "in", "of", "to", "and", "you", "i", "it", "that"}
    palavras_ingles = sum(1 for p in palavras if p.rstrip(".,!?") in palavras_en)
    if len(palavras) >= 3 and palavras_ingles > palavras_pt and palavras_pt == 0:
        print(f"[ATLAS] Filtrado (inglês/ruído): {texto}")
        return False

    return True


def ouvir() -> str:
    print("[ATLAS] Ouvindo...")

    amostras_chunk = int(TAXA_AMOSTRAGEM * DURACAO_CHUNK)
    max_chunks = int(DURACAO_MAXIMA / DURACAO_CHUNK)
    chunks_silencio_max = int(SILENCIO_APOS_FALA / DURACAO_CHUNK)
    chunks_fala_minima = int(DURACAO_MINIMA_FALA / DURACAO_CHUNK)  # 4 chunks = 0.4s

    gravando = []
    chunks_silencio = 0
    fala_iniciada = False
    chunks_com_fala = 0

    with sd.InputStream(samplerate=TAXA_AMOSTRAGEM, channels=1, dtype="float32") as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(amostras_chunk)
            audio_chunk = chunk[:, 0]
            energia = np.mean(np.abs(audio_chunk))

            if energia > LIMIAR_ENERGIA:
                fala_iniciada = True
                chunks_silencio = 0
                chunks_com_fala += 1
                gravando.append(audio_chunk)
            elif fala_iniciada:
                gravando.append(audio_chunk)
                chunks_silencio += 1
                if chunks_silencio >= chunks_silencio_max:
                    break

    if not fala_iniciada or len(gravando) == 0:
        print("[ATLAS] Nenhuma voz detectada.")
        return ""

    # Descartar se fala foi muito curta (ruído pontual)
    if chunks_com_fala < chunks_fala_minima:
        print(f"[ATLAS] Filtrado (fala muito curta: {chunks_com_fala * DURACAO_CHUNK:.1f}s)")
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

            )
        texto = transcricao.strip() if isinstance(transcricao, str) else transcricao.text.strip()
        print(f"[ATLAS] Transcrito: {texto}")
        if not _filtrar_alucinacao(texto):
            return ""
        return texto
    except Exception as e:
        print(f"[ERRO] Groq falhou: {e}")
        return ""
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    resultado = ouvir()
    print(f"Resultado: {resultado}")
