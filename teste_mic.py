import sounddevice as sd
import numpy as np
print('Fale agora por 5 segundos...')
audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype='float32')
sd.wait()
print(f'Volume maximo: {np.max(np.abs(audio)):.4f}')
print(f'Volume medio: {np.mean(np.abs(audio)):.4f}')