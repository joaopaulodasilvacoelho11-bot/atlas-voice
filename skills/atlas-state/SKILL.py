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

## Última Sessão — 06/05/2026

### O que foi feito

1. Degrau 1 concluído — alarmes reais via IA, funcionando em produção
2. Extrator de alarme criado — `funcionalidades/extrator_alarme.py`
3. Detecção automática de intenção e horário no texto do usuário
4. Alarme persistente — repete a cada 20s até o usuário confirmar
5. Cancelamento natural — "ok", "acordei", "pode parar", "entendido"
6. Vozes distintas — Atlas e Lyra com Voice IDs diferentes no ElevenLabs
7. Atlas: sB7vwSCyX0tQmU24cW2C — Lyra: ZbmOZ3GRVkMFzTTGCFG7 (Lyra presença)
8. Botão de áudio ON/OFF recuperado no dock
9. Voz integrada nas respostas normais do chat
10. Tag correta no disparo — ATLAS ou LYRA conforme presença ativa
11. Extrator integrado no chat_lyra também — não só no chat_atlas
12. 3 documentos mestres criados — visão, defesa e segurança por versão
13. Commit: "Degrau 1 completo: alarmes reais via IA, persistentes, vozes distintas Atlas/Lyra"

### Como rodar

```bash
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
uvicorn api:app --reload --port 8000
# Browser — abrir atlas_dashboard.html
```

---

## Próximo Passo — Degrau 2

**Lembretes reais via IA** — mesma lógica dos alarmes. O usuário fala "me lembra de ligar pro médico às 14h" → sistema extrai intenção, horário e descrição → salva no JSON → dispara no horário com voz e nome do usuário.

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
| 1 — Alarmes reais via IA | ✅ CONCLUÍDO |
| 2 — Lembretes reais via IA | 🔜 PRÓXIMO |
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
| Atlas + Lyra com IA real (Claude Haiku) | ✅ |
| Vozes distintas Atlas e Lyra | ✅ |
| Dashboard completo + backend integrado | ✅ |
| Memória persistente entre sessões | ✅ |
| Microfone (Whisper + VAD) no dashboard | ✅ |
| ElevenLabs — botão ON/OFF no dock | ✅ |
| Latência real, sessão viva, núcleo reativo | ✅ |
| Alarmes reais via IA — persistentes | ✅ |
| Cancelamento natural de alarme por voz | ✅ |
| Lembretes via IA | 🔜 Degrau 2 |
| Loop de verificação backend | 🔜 Degrau 3 |
| Script iniciar.bat | 🔜 Degrau 7 |
| Android (V2.0) | Futuro |

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 06/05/2026 — Degrau 1 concluído — Degrau 2 próximo*