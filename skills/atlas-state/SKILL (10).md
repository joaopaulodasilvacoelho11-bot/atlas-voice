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
# Se o backend cair, reinicia sozinho em 3 segundos
C:\Users\Gleida\Desktop\atlas-voice-v1\iniciar.bat

# Dashboard: http://127.0.0.1:8000/dashboard
# Ou abrir atlas_dashboard.html direto pelo browser
```

---

## Estado Atual — 24/05/2026

### V1 — COMPLETO ✅ (tag v1.0 em 12/05/2026)

Todos os 9 Degraus concluídos.

### V2 — EM ANDAMENTO 🔄

| Feature | Status |
|---|---|
| Screensaver mode | ✅ |
| Painel de histórico (slide-in, lado esquerdo) | ✅ |
| Logo da marca melhorado (dois anéis ovais — cyan ATLAS + violet LYRA) | ✅ |
| Status panel — próximo alarme/lembrete | ✅ |
| Sidebar com contadores | ✅ |
| Modo Presença com loop contínuo no dashboard | ✅ |
| Wake word "Atlas" e "Lyra" detectados no loop | ✅ |
| Desativar Modo Presença por voz | ✅ |
| iniciar.bat com reinício automático do backend | ✅ |
| Whisper otimizado (tiny + beam_size=1 + condition_on_previous_text=False) | ✅ |
| VAD calibrado (LIMIAR_VAD=0.3) para microfone de notebook | ✅ |
| Microfone do Lenovo destravado (estava mutado no Lenovo Vantage) | ✅ |

---

## Arquitetura do Modo Presença (V2)

O Modo Presença roda **no dashboard** (não no backend) para evitar conflito de microfone:

- Botão **PRESENÇA** no dock ativa o loop contínuo
- Loop: ouve → detecta wake word ou comando → processa → responde → ouve de novo
- Wake words: **"Atlas"** → troca pro Atlas | **"Lyra"** → troca pra Lyra
- Desativar por voz: "desativa a voz", "desativa a voz", "para a voz"
- Clique no botão PRESENÇA desativa o loop

---

## Stack Técnica

| Camada | Tecnologia |
|---|---|
| Backend | Python / FastAPI |
| Ambiente | Anaconda (env: atlasvoice) |
| STT | Whisper tiny + Silero VAD (LIMIAR=0.3) |
| TTS | ElevenLabs |
| IA | Claude Haiku (Anthropic) |
| Dashboard | React/Babel in-browser JSX |
| Persistência | JSON |
| Versionamento | GitHub |

### Voice IDs ElevenLabs
- Atlas: `sB7vwSCyX0tQmU24cW2C`
- Lyra: `ZbmOZ3GRVkMFzTTGCFG7`

### Otimizações de voz (CPU sem GPU)
- Modelo: `whisper tiny` (4x mais rápido que small)
- `beam_size=1` — busca greedy, sem candidatos
- `condition_on_previous_text=False` — menos overhead
- `SILENCIO_APOS_FALA=0.8s` — encerra captura mais cedo
- `LIMIAR_VAD=0.3` — sensível para microfone de notebook a 40-60cm

---

## Arquivos Principais

```
api.py                                — FastAPI principal, todos os endpoints
atlas_dashboard.html                  — Dashboard React (tudo em um arquivo)
iniciar.bat                           — Sobe tudo, reinicia automaticamente se cair
voz/saida.py                          — ElevenLabs TTS
voz/entrada.py                        — Whisper STT (otimizado)
voz/presenca.py                       — Modo presença backend (não usado ativamente)
funcionalidades/extrator_alarme.py    — Regex alarme
funcionalidades/extrator_lembrete.py  — Regex lembrete
funcionalidades/alarmes.py            — CRUD alarmes (JSON)
funcionalidades/lembretes.py          — CRUD lembretes (JSON)
funcionalidades/memoria_persistente.py — Memória de longo prazo
nucleos/atlas_nucleo.py               — Núcleo Atlas (Claude Haiku)
nucleos/lyra_nucleo.py                — Núcleo Lyra (Claude Haiku)
```

---

## Endpoints da API

| Endpoint | Método | Função |
|---|---|---|
| `/` | GET | Status |
| `/dashboard` | GET | Serve o dashboard HTML |
| `/chat/atlas` | POST | Chat com Atlas |
| `/chat/lyra` | POST | Chat com Lyra |
| `/voz/ouvir` | POST | Microfone → Whisper → texto |
| `/voz/falar` | POST | Texto → ElevenLabs → áudio |
| `/alarme` | POST | Criar alarme |
| `/alarmes` | GET | Listar alarmes |
| `/alarmes/verificar` | POST | Disparar alarmes no horário |
| `/lembrete` | POST | Criar lembrete |
| `/lembretes` | GET | Listar lembretes |
| `/lembretes/verificar` | POST | Disparar lembretes no horário |
| `/sessao` | GET | Dados da sessão |
| `/sessao/resetar` | POST | Limpar histórico |
| `/presenca/iniciar` | POST | Inicia modo presença backend |
| `/presenca/parar` | POST | Para modo presença backend |
| `/presenca/status` | GET | Status do modo presença |

---

## Variáveis de Ambiente (.env)

```
ANTHROPIC_API_KEY
ELEVENLABS_API_KEY
ELEVENLABS_VOICE_ID          — voz do Atlas
ELEVENLABS_VOICE_ID_LYRA     — voz da Lyra
```

---

## Núcleos do Sistema

- **ATLAS** — estratégico, direto, objetivo (cyan)
- **LYRA** — emocional, calma, acolhedora (violet)

Memória e relacionamento pertencem ao usuário, não ao núcleo. Trocar de núcleo preserva todo o histórico.

---

## Armadilhas Conhecidas

- JSX aninhado em ternários de `className` causa blank page sem erro visível — usar sempre strings
- Desalinhamento de colchetes em `useEffect` após `str_replace` sequenciais — verificar com `grep -n "useEffect"` após mudanças
- `const` em React não tem hoisting — declarar refs e funções antes de usá-los
- Microfone do Lenovo pode ficar mutado no Lenovo Vantage → Utilitários → Som → Entrada
- Backend na porta 8000 pode cair — o `iniciar.bat` reinicia automaticamente
- Dashboard servido pelo backend (`127.0.0.1:8000/dashboard`) pode estar em cache — usar Ctrl+Shift+R

---

## Próximos Passos (V2 — pendentes)

- Latência ainda alta (~3s) — limite do CPU sem GPU; próxima melhoria real seria GPU ou API STT externa
- Respostas mais curtas do Haiku para reduzir tempo de TTS

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
| V1 | Fundação — sistema funcional local | ✅ Completo (12/05/2026) |
| V2 | Dashboard evoluído + voz melhorada | 🔄 Em andamento |
| V3 | Mobile — acesso via Wi-Fi local, Android | Futuro |
| V4 | Ecossistema — Bluetooth, IoT, câmeras | Futuro |
| V5 | App próprio — produto público | Futuro |
| V6+ | Presença total — multi-dispositivo, robótica | Visão |

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 24/05/2026 — Sessão de 2h34 — Modo Presença com wake word entregue*
