---
name: atlas-state
description: Skill do projeto Atlas Voice. Use SEMPRE que o JP (João Paulo) iniciar uma sessão de trabalho no Atlas Voice, mencionar "onde paramos", "retomar o projeto", "estado atual", ou qualquer variação. Esta skill carrega o contexto completo do projeto e instrui como retomar com precisão cirúrgica — sem reexplicar nada, sem perder progresso.
---

# Atlas State — Retomada de Sessão

## Identidade do Projeto

**Projeto:** Atlas Voice  
**Fundador:** João Paulo da Silva Coelho (JP) — Manaus, Brasil  
**Repositório:** github.com/joaopaulodasilvacoelho11-bot/atlas-voice  
**Localização local:** `C:\Users\Gleida\Desktop\atlas-voice-v1`  
**Ambiente:** Anaconda — env: `atlasvoice`

---

## Como Retomar

1. Leia este documento inteiro antes de responder
2. Pergunte apenas o que mudou — não o que já está aqui
3. Entre direto no ponto — sem resumos, sem reexplicações da visão
4. Tom: cirúrgico, direto, preciso — como co-fundador técnico

---

## Como Rodar

```bash
# Duplo clique no iniciar.bat — sobe tudo e abre o browser automaticamente
C:\Users\Gleida\Desktop\atlas-voice-v1\iniciar.bat

# Dashboard: http://127.0.0.1:8000/dashboard
```

---

## Estado Atual — 29/05/2026

### V1 — COMPLETO ✅ (tag v1.0 em 12/05/2026)

### V2 — EM ANDAMENTO 🔄

| Feature | Status |
|---|---|
| Screensaver mode | ✅ |
| Painel de histórico (slide-in, lado esquerdo) | ✅ |
| Logo da marca (dois anéis ovais — cyan ATLAS + violet LYRA) | ✅ |
| Status panel — próximo alarme/lembrete | ✅ |
| Sidebar com contadores | ✅ |
| Modo Presença com loop contínuo no dashboard | ✅ |
| Wake word "Atlas" e "Lyra" detectados no loop | ✅ |
| Desativar Modo Presença por voz | ✅ |
| iniciar.bat com reinício automático do backend | ✅ |
| STT: Groq API (whisper-large-v3-turbo) | ✅ |
| Latência STT ~300ms | ✅ |
| ElevenLabs streaming (TTS) | ⏳ Próximo |
| Respostas curtas do Haiku | ⏳ Próximo |
| Filtro de alucinação do Groq | ⏳ Próximo |

---

## Arquitetura do Modo Presença (V2)

O Modo Presença roda **no dashboard** (não no backend):

- Botão **PRESENÇA** ativa o loop
- Loop: standby silencioso → wake word → ativo 30s → standby
- Wake words: **"Atlas"** → troca pro Atlas | **"Lyra"** → troca pra Lyra
- Desativar por voz: "desativa a voz", "para a voz", "desativar", "desative"
- Clique no botão PRESENÇA desativa o loop

---

## Stack Técnica

| Camada | Tecnologia |
|---|---|
| Backend | Python / FastAPI |
| Ambiente | Anaconda (env: atlasvoice) |
| STT | Groq API — whisper-large-v3-turbo |
| TTS | ElevenLabs |
| IA | Claude Haiku (Anthropic) |
| Dashboard | React/Babel in-browser JSX |
| Persistência | JSON |
| Versionamento | GitHub |

### Voice IDs ElevenLabs
- Atlas: `sB7vwSCyX0tQmU24cW2C`
- Lyra: `ZbmOZ3GRVkMFzTTGCFG7`

### STT — Groq API (voz/entrada.py)
- Modelo: `whisper-large-v3-turbo`
- Detecção: energia do áudio (LIMIAR_ENERGIA=0.01) — sem Silero VAD
- prompt="Atlas, Lyra" para reduzir alucinações
- SILENCIO_APOS_FALA=1.0s
- DURACAO_MAXIMA=15s
- Problema conhecido: Groq alucina com ruído ambiente intenso

---

## Variáveis de Ambiente (.env)

```
ANTHROPIC_API_KEY
ELEVENLABS_API_KEY
ELEVENLABS_VOICE_ID          — voz do Atlas
ELEVENLABS_VOICE_ID_LYRA     — voz da Lyra
GROQ_API_KEY                 — STT via Groq Whisper
```

---

## Arquivos Principais

```
api.py                                — FastAPI principal, todos os endpoints
atlas_dashboard.html                  — Dashboard React (tudo em um arquivo)
iniciar.bat                           — Sobe tudo, reinicia automaticamente se cair
voz/saida.py                          — ElevenLabs TTS
voz/entrada.py                        — Groq STT (substituiu Whisper local)
funcionalidades/extrator_alarme.py    — Regex alarme
funcionalidades/extrator_lembrete.py  — Regex lembrete
funcionalidades/alarmes.py            — CRUD alarmes (JSON)
funcionalidades/lembretes.py          — CRUD lembretes (JSON)
funcionalidades/memoria_persistente.py — Memória de longo prazo
nucleos/atlas_nucleo.py               — Núcleo Atlas (Claude Haiku)
nucleos/lyra_nucleo.py                — Núcleo Lyra (Claude Haiku)
```

---

## Commits Recentes

| Commit | Descrição |
|---|---|
| 979d440 | docs: atlas state 29/05/2026 |
| dc1bc99 | feat: Groq STT integrado |
| 051dfcb | feat: modo presença com wake word |

---

## Armadilhas Conhecidas

- JSX aninhado em ternários de `className` causa blank page sem erro visível
- Desalinhamento de colchetes em `useEffect` após `str_replace` sequenciais
- `const` em React não tem hoisting — declarar antes de usar
- Dashboard em cache — usar Ctrl+Shift+R após mudanças
- Groq alucina com ruído ambiente — não usar em ambiente barulhento
- Eco: microfone capta voz do Atlas — flag `atlasfalando` bloqueia mic durante TTS
- Mudanças em cascata no dashboard quebram o loop — uma mudança por vez

---

## Regras do Projeto (Lei)

```
1. Nenhuma versão nasce do zero
2. Toda base herda 100% das anteriores
3. Nunca avançar sem fechar a fase atual
4. Backup antes de qualquer mudança grande
5. Um módulo por vez — foco e destreza
6. A lógica precisa estar sólida antes de construir interface
7. Todo código novo herda o anterior
```

---

## Roadmap

| Fase | Foco | Status |
|---|---|---|
| V1 | Fundação — sistema funcional local | ✅ Completo |
| V2 | Dashboard evoluído + voz melhorada | 🔄 Em andamento |
| V3 | Mobile — acesso via Wi-Fi local, Android | Futuro |
| V4 | Ecossistema — Bluetooth, IoT, câmeras | Futuro |
| V5 | App próprio — produto público | Futuro |
| V6+ | Presença total — multi-dispositivo, robótica | Visão |

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 29/05/2026 — Groq STT integrado, latência ~300ms*
