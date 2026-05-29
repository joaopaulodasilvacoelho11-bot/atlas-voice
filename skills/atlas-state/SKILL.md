# Atlas State — 29/05/2026

## Estado Atual
- V1: completo (tag v1.0, 12/05/2026)
- V2: em andamento
- Commit atual: dc1bc99

## O que mudou hoje (29/05)
- STT: Whisper local → Groq API (whisper-large-v3-turbo)
- Latência STT: ~300ms (era ~2-3s)
- prompt="Atlas, Lyra" para reduzir alucinações
- Detecção por energia (sem Silero VAD)
- GROQ_API_KEY adicionada no .env

## Problema conhecido
- Groq alucina com ruído ambiente — próxima sessão resolver
- Solução planejada: filtro pós-transcrição + Push-to-Talk como fallback

## Próximas melhorias
1. Filtro de alucinação no entrada.py
2. ElevenLabs streaming (TTS mais rápido)
3. Respostas mais curtas do Haiku
