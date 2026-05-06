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

**Degrau 1 — Alarmes reais via IA** ✅
1. Extrator de alarme criado — `funcionalidades/extrator_alarme.py`
2. Detecção automática de intenção e horário no texto do usuário
3. Alarme persistente — repete a cada 20s até o usuário confirmar
4. Cancelamento natural — "ok", "acordei", "pode parar", "entendido"
5. Vozes distintas — Atlas e Lyra com Voice IDs diferentes no ElevenLabs
6. Atlas: sB7vwSCyX0tQmU24cW2C — Lyra: ZbmOZ3GRVkMFzTTGCFG7
7. Botão de áudio ON/OFF recuperado no dock
8. Extrator integrado no chat_lyra também — não só no chat_atlas
9. Commit: "Degrau 1 completo: alarmes reais via IA, persistentes, vozes distintas Atlas/Lyra"

**Degrau 2 — Lembretes reais via IA** ✅
1. `funcionalidades/extrator_lembrete.py` criado — detecta intenção + horário + prioridade
2. Regex com lookahead/lookbehind — cobre `15:30`, `15h30`, `15h`, `8 horas`
3. Prioridade automática — "urgente" → Alta, "quando der" → Baixa, padrão → Normal
4. `api.py` — integrado no `chat_atlas` e `chat_lyra` + 3 endpoints novos
5. Endpoints: `POST /lembrete`, `GET /lembretes`, `POST /lembretes/verificar`
6. `atlas_dashboard.html` — loop de 15s agora verifica alarmes E lembretes
7. Fix crítico — removido `return` prematuro que bloqueava o bloco de lembretes
8. Lyra disparando lembretes com voz — testado e confirmado
9. Commit: "[feat] Degrau 2 completo: lembretes reais via IA, disparo no horário, Atlas e Lyra"

### Como rodar

```bash
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
uvicorn api:app --reload --port 8000
# Browser — abrir atlas_dashboard.html
```

---

## Próximo Passo — Degrau 3

**Loop de verificação no backend** — BackgroundTask do FastAPI rodando a cada 30s, verificando alarmes e lembretes automaticamente, independente do dashboard estar aberto. Dispara voz direto do backend quando o horário chega.

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
| `/lembrete` | POST | Criar lembrete no JSON |
| `/lembretes` | GET | Listar lembretes ativos |
| `/lembretes/verificar` | POST | Disparar lembretes no horário |
| `/sessao` | GET | Dados da sessão atual |
| `/sessao/resetar` | POST | Limpar histórico |

---

## Roadmap 1.0 — 9 Degraus

| Degrau | Status |
|---|---|
| 1 — Alarmes reais via IA | ✅ CONCLUÍDO |
| 2 — Lembretes reais via IA | ✅ CONCLUÍDO |
| 3 — Loop de verificação no backend | 🔜 PRÓXIMO |
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
| Lembretes reais via IA — com prioridade | ✅ |
| Disparo de lembretes no horário com voz | ✅ |
| Loop de verificação backend | 🔜 Degrau 3 |
| Script iniciar.bat | 🔜 Degrau 7 |
| Android (V2.0) | Futuro |

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 06/05/2026 — Degrau 2 concluído — Degrau 3 próximo*
