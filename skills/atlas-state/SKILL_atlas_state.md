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
2. Não pergunte o que já está aqui — entre direto no ponto
3. Confirme com JP o que foi feito desde a última sessão (se houver)
4. Execute o próximo passo definido abaixo
5. Tom: cirúrgico, direto, preciso — como co-fundador técnico

---

## Como Rodar

```bash
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
iniciar.bat

# Dashboard: http://127.0.0.1:8000/dashboard
# Sempre Ctrl+Shift+R após mudanças (cache)
```

---

## O QUE JÁ FOI FEITO (histórico completo V2)

| Feature | Sessão |
|---|---|
| Screensaver mode | Mai/2026 |
| Painel de histórico slide-in | Mai/2026 |
| Logo marca (anéis cyan/violet) | Mai/2026 |
| Status panel alarme/lembrete | Mai/2026 |
| Modo Presença — loop contínuo no dashboard | Mai/2026 |
| Wake word Atlas/Lyra no loop | Mai/2026 |
| Desativar Modo Presença por voz | Mai/2026 |
| iniciar.bat com reinício automático | Mai/2026 |
| STT: Groq API whisper-large-v3-turbo (~300ms) | 29/05/2026 |
| Respostas Haiku curtas (max_tokens=150, 30 palavras) | 29/05/2026 |
| Atlas e Lyra independentes — não se citam | 29/05/2026 |
| Filtro de alucinação básico em entrada.py | 29/05/2026 |
| Fix: wake word do mesmo núcleo não cai no chat | 04/06/2026 |
| ElevenLabs streaming TTS | 04/06/2026 |
| Wake word dupla responde como núcleo ativo | 04/06/2026 |
| Troca de núcleo por voz — REMOVIDA (decisão permanente) | 04/06/2026 |
| Filtro de ruído reforçado (LIMIAR=0.02, duração mínima 0.2s, lista negra) | 10/06/2026 |
| ElevenLabs atualizado 2.52.0 — método .stream() corrigido | 10/06/2026 |
| Chave Groq exposta revogada, nova chave no .env | 10/06/2026 |
| .gitignore protegendo pastas chave/ e chaves de api/ | 10/06/2026 |

---

## O QUE ESTÁ SENDO FEITO AGORA

**V2 — fase de estabilização**

Sistema estável em 10/06/2026. Voz funcionando, filtro de ruído validado com TV ligada. Sem issues críticos abertos.

Último commit: `a3d3b97` — chore: ignorar pastas de chaves de API no .gitignore

---

## PRÓXIMO PASSO — O QUE FAZER NA PRÓXIMA SESSÃO

**Implementar Push-to-Talk (PTT) no dashboard**

O Modo Presença atual captura tudo que passa pelo limiar de energia — incluindo TV e sons ambiente em português. O PTT é o próximo nível: só captura quando o usuário pressionar e segurar o botão.

**Como implementar:**
1. Adicionar botão PTT no dashboard (segurar = gravando, soltar = processa)
2. Criar endpoint `POST /voz/ouvir-ptt` no backend que recebe áudio já capturado
3. O PTT convive com o Modo Presença — são dois modos, usuário escolhe

**Arquivo a mexer:** `atlas_dashboard.html` — adicionar botão PTT na dock inferior  
**Cuidado:** `executarCicloVoz` é frágil — mexer com cuidado, uma mudança por vez

---

## DECISÃO PERMANENTE — Troca de Núcleo

**Troca de núcleo por voz REMOVIDA.** Não reintroduzir.  
**Como trocar:** botão ATLAS/LYRA no topo do dashboard.  
**Por que foi removida:** guards de wake word causavam oscilação atlas↔lyra. flushSync, setTimeout(0), .click() via ref — nada funcionou. Causa raiz: React 18 setPresence dentro de loop async não comita visual de forma confiável.

---

## Stack Técnica

| Camada | Tecnologia |
|---|---|
| Backend | Python / FastAPI |
| Ambiente | Anaconda (env: atlasvoice) |
| STT | Groq API — whisper-large-v3-turbo |
| TTS | ElevenLabs 2.52.0 — método .stream() |
| IA | Claude Haiku (Anthropic) |
| Dashboard | React/Babel in-browser JSX (React 18, createRoot) |
| Persistência | JSON |
| Versionamento | GitHub |

### Voice IDs ElevenLabs
- Atlas: `sB7vwSCyX0tQmU24cW2C`
- Lyra: `ZbmOZ3GRVkMFzTTGCFG7`

### STT — Groq (voz/entrada.py)
- LIMIAR_ENERGIA=0.02, DURACAO_MINIMA_FALA=0.2s
- prompt removido — causava alucinação do próprio texto
- Lista negra: "atlas, lyra", inglês puro, repetições de caracteres

### IA — Claude Haiku
- max_tokens=150, máximo 2 frases / 30 palavras no system prompt

---

## Variáveis de Ambiente (.env)

```
ANTHROPIC_API_KEY
ELEVENLABS_API_KEY
ELEVENLABS_VOICE_ID       — Atlas
ELEVENLABS_VOICE_ID_LYRA  — Lyra
GROQ_API_KEY              — nova chave gerada em 10/06/2026
```

---

## Arquivos Principais

```
api.py                                — FastAPI, todos os endpoints
atlas_dashboard.html                  — Dashboard React (arquivo único)
iniciar.bat                           — Startup com reinício automático
voz/saida.py                          — ElevenLabs TTS (.stream())
voz/entrada.py                        — Groq STT + filtro de ruído
nucleos/atlas_nucleo.py               — Núcleo Atlas (Claude Haiku)
nucleos/lyra_nucleo.py                — Núcleo Lyra (Claude Haiku)
funcionalidades/extrator_alarme.py    — Regex alarme
funcionalidades/extrator_lembrete.py  — Regex lembrete
funcionalidades/alarmes.py            — CRUD alarmes
funcionalidades/lembretes.py          — CRUD lembretes
funcionalidades/memoria_persistente.py — Memória de longo prazo
```

---

## Armadilhas Conhecidas

- JSX em ternários de `className` → blank page sem erro
- Desalinhamento de colchetes em `useEffect` após str_replace sequenciais
- Dashboard em cache → Ctrl+Shift+R após mudanças
- Groq: não usar `prompt=` → alucina o próprio prompt com ruído
- Eco: `atlasfalando` bloqueia mic durante TTS
- Loop `executarCicloVoz` é recursivo/frágil → uma mudança por vez
- ElevenLabs: método correto é `.stream()`, não `.convert_as_stream()`
- NUNCA commitar chaves de API — .gitignore protege `chave/` e `chaves de api/`
- F12 abre calculadora — usar botão direito → Inspecionar

---

## Regras do Projeto (Lei)

```
1. Nenhuma versão nasce do zero
2. Toda base herda 100% das anteriores
3. Nunca avançar sem fechar a fase atual
4. Backup antes de qualquer mudança grande
5. Um módulo por vez — foco e destreza
6. Lógica sólida antes de construir interface
7. Todo código novo herda o anterior
8. Não ficar preso — se não resolve, decidir e seguir
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
*Atualizado: 10/06/2026 — commit a3d3b97*
