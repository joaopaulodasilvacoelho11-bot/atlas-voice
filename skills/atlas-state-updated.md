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

## Como Retomar — Sem Perguntas

> "Estou dentro. Última sessão: [resumo]. Próximo passo: [ação concreta]. Começamos?"

---

## Última Sessão — 01/05/2026 (noite)

### O que foi feito

1. FastAPI completa com todos os endpoints operantes
2. Atlas e Lyra com IA real (Claude Haiku) e personalidades distintas
3. Atlas conhece a Lyra como parceira — system prompt atualizado
4. Memória de sessão + persistência em `data/memoria_sessao.json`
5. Sessão viva — contador real de tempo e mensagens
6. Latência real no painel
7. Núcleo reativo — PROCESSANDO → FALANDO → OUVINDO
8. Título ATLAS/LYRA reativo com cor e nome corretos
9. Pontos animados no dock durante espera
10. Microfone conectado — Whisper + VAD transcreve e envia automaticamente
11. ElevenLabs conectado — botão de voz no dock, Atlas e Lyra falam após responder
12. Alarmes — endpoint `/alarme` existe e salva no JSON, mas IA ainda não chama automaticamente
13. Verificação de alarmes a cada 30s no dashboard
14. Roadmap 1.0 criado — 9 degraus até o fechamento (`skills/atlas-roadmap/SKILL.md`)

### Como rodar

```bash
# Terminal — API
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
uvicorn api:app --reload --port 8000

# Browser — abrir da pasta do projeto
C:\Users\Gleida\Desktop\atlas-voice-v1\atlas_dashboard.html
```

---

## Próximo Passo — Degrau 1 do Roadmap

**Alarmes reais via IA** — quando o usuário pede um alarme, a IA confirma em texto mas não chama o endpoint `/alarme`. O JSON fica vazio.

**O que precisa ser feito:**
- Detectar intenção de alarme na resposta da IA
- Extrair horário e descrição
- Chamar `/alarme` automaticamente com os dados
- Atlas confirma que foi salvo de verdade

**Critério de conclusão:** "me acorda às 21h" → aparece no `alarmes.json` → dispara em voz no horário.

---

## Endpoints da API

| Endpoint | Método | Função |
|---|---|---|
| `/` | GET | Status da API |
| `/chat/atlas` | POST | Chat com Atlas (IA real) |
| `/chat/lyra` | POST | Chat com Lyra (IA real) |
| `/voz/ouvir` | POST | Microfone → Whisper → texto |
| `/voz/falar` | POST | Texto → ElevenLabs → áudio |
| `/alarme` | POST | Criar alarme no JSON |
| `/alarmes` | GET | Listar alarmes ativos |
| `/alarmes/verificar` | POST | Disparar alarmes no horário |
| `/sessao` | GET | Dados da sessão atual |
| `/sessao/resetar` | POST | Limpar histórico |

---

## Roadmap 1.0 — 9 Degraus

| Degrau | Status |
|---|---|
| 1 — Alarmes reais via IA | 🔜 PRÓXIMO |
| 2 — Lembretes reais via IA | 🔜 |
| 3 — Loop de verificação no backend | 🔜 |
| 4 — Memória de longo prazo real | 🔜 |
| 5 — Lyra integrada com Atlas | 🔜 |
| 6 — Dashboard na pasta do projeto | 🔜 |
| 7 — Script iniciar.bat | 🔜 |
| 8 — Testes de uso real + correções | 🔜 |
| 9 — Documentação + tag v1.0 | 🔜 |

---

## Status das Funcionalidades

| Funcionalidade | Status |
|---|---|
| Atlas + Lyra com IA real | ✅ |
| Atlas conhece Lyra como parceira | ✅ |
| Dashboard completo + backend integrado | ✅ |
| Memória persistente entre sessões | ✅ |
| Microfone (Whisper + VAD) no dashboard | ✅ |
| ElevenLabs no dashboard (voz ON/OFF) | ✅ |
| Latência real, sessão viva, núcleo reativo | ✅ |
| Alarmes endpoint funcionando | ✅ |
| Alarmes via IA (extração automática) | 🔜 Degrau 1 |
| Lembretes via IA | 🔜 Degrau 2 |
| Loop de verificação backend | 🔜 Degrau 3 |
| Script iniciar.bat | 🔜 Degrau 7 |
| Android (V2.0) | Futuro |

---

*Atlas Voice — JP Silva — Manaus, Brasil*
*Atualizado: 01/05/2026 — 20:50*
