# Atlas Voice — V1.0

> *"Uma presença. Não uma ferramenta."*

Atlas Voice é um assistente de voz pessoal com duas personalidades — **ATLAS** (estratégico, direto) e **LYRA** (emocional, acolhedora). Ele ouve, responde, lembra e age — mesmo quando você não está olhando para a tela.

**Fundador:** JP Silva — Manaus, Brasil  
**Repositório:** github.com/joaopaulodasilvacoelho11-bot/atlas-voice

---

## Como Rodar

**Opção 1 — Duplo clique:**
```
iniciar.bat
```

**Opção 2 — Manual:**
```bash
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
uvicorn api:app --reload --port 8000
```

Dashboard abre em `http://127.0.0.1:8000/dashboard`

---

## Funcionalidades

| Status | Funcionalidade |
|--------|----------------|
| ✅ | Chat com ATLAS (estratégico, direto) |
| ✅ | Chat com LYRA (emocional, acolhedora) |
| ✅ | Troca de núcleo por comando |
| ✅ | Vozes distintas via ElevenLabs |
| ✅ | Entrada por voz (Whisper + Silero VAD) |
| ✅ | Wake word — "Atlas" / "Lyra" |
| ✅ | Modo presença contínua |
| ✅ | Alarmes reais via IA — persistentes |
| ✅ | Cancelamento natural de alarme por voz |
| ✅ | Lembretes com prioridade automática |
| ✅ | Disparo de alarmes e lembretes no horário |
| ✅ | Loop de verificação no backend (30s) |
| ✅ | Memória de longo prazo entre sessões |
| ✅ | Memória unificada — Atlas e Lyra compartilham histórico |
| ✅ | Dashboard React servido pelo FastAPI |
| ✅ | Login seguro (bcrypt) |
| ✅ | Script iniciar.bat |

---

## Comandos Disponíveis

| Comando | Ação |
|---------|------|
| `me acorda às 8h` | Cria alarme |
| `cancelar alarme` | Lista e cancela alarme |
| `me lembra de X às 15h` | Cria lembrete prioridade Normal |
| `me lembra de X às 15h urgente` | Cria lembrete prioridade Alta |
| `me lembra de X às 15h quando der` | Cria lembrete prioridade Baixa |
| `cancelar lembrete` | Lista e cancela lembrete |
| `falar com Lyra` | Ativa núcleo emocional |
| `mudar para Atlas` | Ativa núcleo estratégico |
| `sair` / `encerrar` | Encerra sessão |

> **Wake word:** diga "Atlas" ou "Lyra" para ativar a presença sem usar o teclado.

---

## Estrutura de Arquivos

```
atlas-voice-v1/
├── api.py                              — FastAPI principal
├── atlas_dashboard.html                — Dashboard (React, arquivo único)
├── iniciar.bat                         — Inicia o sistema com duplo clique
├── config.py                           — Caminhos dinâmicos
├── .env                                — Chaves de API (não commitado)
├── nucleos/
│   ├── atlas_nucleo.py                 — Núcleo ATLAS
│   └── lyra_nucleo.py                  — Núcleo LYRA
├── funcionalidades/
│   ├── extrator_alarme.py              — Detecção de alarme no texto
│   ├── extrator_lembrete.py            — Detecção de lembrete no texto
│   ├── alarmes.py                      — CRUD alarmes (JSON)
│   ├── lembretes.py                    — CRUD lembretes (JSON)
│   └── memoria_persistente.py          — Memória de longo prazo
├── voz/
│   ├── entrada.py                      — Whisper STT
│   ├── saida.py                        — ElevenLabs TTS
│   └── presenca.py                     — Modo presença contínua + wake word
├── pipeline/
│   ├── base_2_4_motor_temporal.py      — Interpreta tempo natural
│   └── base_2_5_classificador.py       — Classifica intenção + roteia
└── data/                               — JSONs gerados em uso
```

---

## Stack

| Camada | Tecnologia |
|--------|------------|
| Backend | Python + FastAPI |
| IA | Claude Haiku (Anthropic) |
| Voz — entrada | Whisper + Silero VAD |
| Voz — saída | ElevenLabs |
| Dashboard | React (single file) |
| Ambiente | Anaconda (env: atlasvoice) |
| Persistência | JSON local |
| Segurança | bcrypt |

---

## Variáveis de Ambiente (.env)

```
ANTHROPIC_API_KEY
ELEVENLABS_API_KEY
ELEVENLABS_VOICE_ID         — voz do ATLAS
ELEVENLABS_VOICE_ID_LYRA    — voz da LYRA
```

---

## Endpoints da API

| Endpoint | Método | Função |
|----------|--------|--------|
| `/` | GET | Status |
| `/chat/atlas` | POST | Chat com ATLAS |
| `/chat/lyra` | POST | Chat com LYRA |
| `/voz/ouvir` | POST | Microfone → texto |
| `/voz/falar` | POST | Texto → áudio |
| `/alarme` | POST | Criar alarme |
| `/alarmes` | GET | Listar alarmes |
| `/alarmes/verificar` | POST | Disparar alarmes |
| `/lembrete` | POST | Criar lembrete |
| `/lembretes` | GET | Listar lembretes |
| `/lembretes/verificar` | POST | Disparar lembretes |
| `/presenca/iniciar` | POST | Iniciar modo presença |
| `/presenca/parar` | POST | Parar modo presença |
| `/presenca/status` | GET | Status da presença |
| `/sessao` | GET | Dados da sessão |
| `/sessao/resetar` | POST | Limpar histórico |
| `/dashboard` | GET | Dashboard web |

---

## Roadmap

| Fase | Foco | Status |
|------|------|--------|
| V1 | Fundação — voz, memória, presença contínua | ✅ Concluído |
| V2 | Interface web refinada + expansão de habilidades | 🔜 Próximo |
| V3 | Android + voz nativa no celular | Futuro |
| V4 | App publicado | Futuro |
| V5 | Plataforma pública | Visão |

---

## Requisitos

- Python 3.10+
- Anaconda
- Conta Anthropic (Claude Haiku)
- Conta ElevenLabs

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*V1.0 — Maio 2026*
