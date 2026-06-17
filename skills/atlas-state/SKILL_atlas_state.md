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
| Endpoint POST /voz/ouvir-ptt em api.py (UploadFile → Groq, reusa _groq de voz/entrada.py) | 17/06/2026 |
| Fix: python-multipart adicionado ao requirements.txt (dep. obrigatória FastAPI UploadFile) | 17/06/2026 |
| Botão PTT no dashboard — estilo WhatsApp, desabilitado quando Modo Presença ativo | 17/06/2026 |
| Refactor: enviarAoNucleo(texto) extraída de send — usada por digitado e PTT sem duplicar | 17/06/2026 |
| PTT conectado ao núcleo ativo — após transcrição chama /chat/atlas ou /chat/lyra automático | 17/06/2026 |
| iniciar.bat atualizado para --host 0.0.0.0 (acesso via rede local, não só localhost) | 17/06/2026 |
| Regra firewall Windows porta 8000, profile=any (resolve bloqueio em redes "Público") | 17/06/2026 |
| Testado: PTT com Atlas ok, Lyra ok, celular via rede local (192.168.1.8:8000/dashboard) | 17/06/2026 |
| Commits: 3fda7a5 (backend PTT), cd0f008 (botão PTT), 14b0ed1 (PTT→núcleo) → push origin | 17/06/2026 |

---

## O QUE ESTÁ SENDO FEITO AGORA

**PTT (Push-to-Talk) completo e funcional ponta a ponta**

Captura no navegador → transcrição via Groq → resposta do núcleo ativo (Atlas/Lyra) → exibição no chat. Validado em PC e em celular via rede local.

Pendência conhecida, não bloqueante: o atlas_dashboard.html não é responsivo para tela de celular — ao abrir no navegador mobile, parte do layout (lado direito) fica cortado/com espaço preto, embora toda a funcionalidade (PTT, chat, núcleos) funcione corretamente por trás.

Último commit: `14b0ed1` — feat: conecta PTT ao núcleo ativo (Atlas/Lyra)

---

## PRÓXIMO PASSO — O QUE FAZER NA PRÓXIMA SESSÃO

**Responsividade mobile do atlas_dashboard.html**

Ao abrir no navegador do celular, parte do layout (lado direito) fica cortado/com espaço preto. Toda a funcionalidade funciona, mas o layout não se adapta à largura da tela.

**Como implementar:**
1. Adicionar media queries CSS para telas menores (≤768px)
2. Recolher ou empilhar os painéis laterais (side--left / side--right) em mobile
3. Garantir que dock, transcript e botão PTT sejam acessíveis em tela pequena
4. Não alterar nenhuma lógica funcional (PTT, enviarAoNucleo, Modo Presença) — apenas layout/CSS

**Cuidado:** o JSX usa classes CSS e `style={{}}` inline — mudanças de layout exigem ajuste tanto no `<style>` quanto nos componentes React

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
*Atualizado: 17/06/2026 — commit 14b0ed1*
