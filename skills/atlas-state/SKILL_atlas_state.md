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
# Duplo clique no iniciar.bat — sobe tudo e abre o browser
C:\Users\Gleida\Desktop\atlas-voice-v1\iniciar.bat

# Se uvicorn não reconhecido, rodar manualmente:
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
python -m uvicorn api:app --host 0.0.0.0 --port 8000

# Dashboard: http://127.0.0.1:8000/dashboard
# Sempre Ctrl+Shift+R após mudanças (cache)
```

---

## Estado Atual — 10/06/2026

### V1 — COMPLETO (tag v1.0 em 12/05/2026)

### V2 — EM ANDAMENTO

| Feature | Status |
|---|---|
| Screensaver mode | OK |
| Painel de histórico (slide-in, lado esquerdo) | OK |
| Logo da marca (dois anéis ovais — cyan ATLAS + violet LYRA) | OK |
| Status panel — próximo alarme/lembrete | OK |
| Sidebar com contadores | OK |
| Modo Presença com loop contínuo no dashboard | OK |
| Wake word "Atlas" e "Lyra" detectados no loop | OK |
| Desativar Modo Presença por voz | OK |
| iniciar.bat com reinício automático do backend | OK |
| STT: Groq API (whisper-large-v3-turbo) | OK |
| Latência STT ~300ms | OK |
| Respostas curtas do Haiku (max_tokens=150, 30 palavras) | OK |
| Atlas e Lyra independentes — não citam um ao outro | OK |
| Filtro de alucinação Groq (entrada.py) | OK |
| Fix: wake word do mesmo núcleo não cai no chat | OK |
| ElevenLabs streaming TTS (convert_as_stream) | OK |
| Wake word dupla ("Atlas, Lyra") responde como núcleo ativo | OK |
| Troca de núcleo por voz | REMOVIDA (decisão de projeto) |

### V2 — PRÓXIMO PASSO

**Qualidade de voz com ruído ambiente** — Groq ainda alucina com ruído de fundo.

Plano de ataque:
1. Reforçar filtro pós-transcrição em `voz/entrada.py` — descartar transcrições sem intenção real
2. Implementar Push-to-Talk (PTT) no dashboard como fallback — botão segurar para falar

---

## DECISÃO DE PROJETO — Troca de Núcleo (04/06/2026)

**A troca de núcleo por voz foi REMOVIDA.** Não reintroduzir sem nova decisão do JP.

**Motivo:** Lyra e Atlas compartilham a mesma memória e são ambos inteligentes. Não há razão para trocar no meio de uma conversa — o núcleo escolhido atende bem. A troca por voz adicionava complexidade e causava oscilação de estado (atlas<->lyra) sem benefício real.

**Como trocar agora:** o usuário clica no botão ATLAS/LYRA no topo do dashboard. A memória é preservada na troca (pertence ao usuário, não ao núcleo).

**Histórico técnico (para não repetir):** tentamos flushSync, setTimeout(0), .click() via ref, setPresenceRef — nada resolveu a oscilação. Causa raiz: guards de wake word interceptavam frases contendo "atlas"/"lyra" e o estado oscilava. Solução final: remover os guards de troca, manter só `_APENAS_WAKE_WORD` (barra wake word solta caindo no chat) e a troca pelo botão.

---

## Arquitetura do Modo Presença (V2)

O Modo Presença roda **no dashboard** (não no backend):

- Botão **PRESENÇA** ativa o loop
- Loop: standby silencioso -> wake word -> ativo 30s -> standby
- Desativar por voz: "desativa a voz", "para a voz", "desativar", "desative"
- Clique no botão PRESENÇA desativa o loop
- `executarCicloVoz(pres)` é o coração do loop — recursivo via setTimeout, usa `presenceRef.current`
- **FRÁGIL:** qualquer mudança no dashboard exige cuidado máximo, uma de cada vez

---

## Stack Técnica

| Camada | Tecnologia |
|---|---|
| Backend | Python / FastAPI |
| Ambiente | Anaconda (env: atlasvoice) |
| STT | Groq API — whisper-large-v3-turbo |
| TTS | ElevenLabs (convert_as_stream) |
| IA | Claude Haiku (Anthropic) |
| Dashboard | React/Babel in-browser JSX (createRoot, React 18) |
| Persistência | JSON |
| Versionamento | GitHub |

### Voice IDs ElevenLabs
- Atlas: `sB7vwSCyX0tQmU24cW2C`
- Lyra: `ZbmOZ3GRVkMFzTTGCFG7`

### STT — Groq API (voz/entrada.py)
- Modelo: `whisper-large-v3-turbo`
- Detecção: energia do áudio (LIMIAR_ENERGIA=0.01)
- prompt="Atlas, Lyra"
- SILENCIO_APOS_FALA=1.0s, DURACAO_MAXIMA=15s
- Filtro de alucinação: textos curtos sem palavras reais -> descartados

### IA — Claude Haiku
- max_tokens=150
- Limite no system prompt: máximo 2 frases, 30 palavras
- Atlas e Lyra não citam um ao outro salvo se perguntarem

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
voz/saida.py                          — ElevenLabs TTS (streaming)
voz/entrada.py                        — Groq STT + filtro de alucinação
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
| 53b9d09 | fix: remover troca de núcleo por voz, manter só botão; wake word dupla responde como núcleo ativo |
| 86a336e | docs: atlas state 03/06/2026 |
| edbdd08 | fix: barrar wake word do mesmo núcleo ativo caindo no chat |
| dc1bc99 | feat: Groq STT integrado |

---

## Armadilhas Conhecidas

- JSX aninhado em ternários de `className` causa blank page sem erro visível
- Desalinhamento de colchetes em `useEffect` após `str_replace` sequenciais
- `const` em React não tem hoisting — declarar antes de usar
- Dashboard em cache — usar Ctrl+Shift+R após mudanças
- Groq alucina com ruído ambiente — filtro ativo em entrada.py
- Eco: microfone capta voz do Atlas — flag `atlasfalando` bloqueia mic durante TTS
- Mudanças em cascata no dashboard quebram o loop — uma mudança por vez
- iniciar.bat pode não ativar conda — usar `python -m uvicorn` se necessário
- F12 abre calculadora do sistema — usar botão direito -> Inspecionar para DevTools
- React 18 + createRoot: setPresence dentro de loop async não comita visual de forma confiável (motivo da remoção da troca por voz)
- Loop executarCicloVoz é recursivo via setTimeout — stale closure é risco, usa presenceRef.current para evitar

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
8. Não ficar preso num módulo — se não resolve, decidir e seguir
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
*Atualizado: 10/06/2026 — commit 53b9d09 — próximo: filtro ruído + Push-to-Talk*
