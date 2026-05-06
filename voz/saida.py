import os
import io
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import pygame

load_dotenv()

cliente = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
VOICE_ID_LYRA = os.getenv("ELEVENLABS_VOICE_ID_LYRA")

def falar(texto: str, presence: str = "atlas"):
    """Converte texto em áudio e reproduz."""
    try:
        voice_id = VOICE_ID_LYRA if presence == "lyra" else VOICE_ID
        audio = cliente.text_to_speech.convert(
            voice_id=voice_id,
            text=texto,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        # Coleta o áudio em bytes
        audio_bytes = b"".join(audio)
        
        # Reproduz com pygame
        pygame.mixer.init()
        pygame.mixer.music.load(io.BytesIO(audio_bytes))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"[Atlas] Erro na voz: {e}")
        print(f"[Atlas] {texto}")