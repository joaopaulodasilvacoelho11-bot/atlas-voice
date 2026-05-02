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

## Última Sessão — 01/05/2026

### O que foi feito

1. Dashboard HTML completo com núcleo animado (brasas, anéis orbitais, partículas)
2. FastAPI (`api.py`) conectando dashboard ao backend Python
3. Atlas e Lyra com IA real (Claude Haiku) e personalidades distintas
4. Memória de sessão — últimas 10 trocas como contexto para a IA
5. Memória persistente — `data/memoria_sessao.json` carregado ao reiniciar
6. Sessão viva — contador real de tempo e mensagens no painel
7. Latência real — painel mostra ms reais de cada resposta
8. Núcleo reativo — PROCESSANDO → FALANDO → OUVINDO conforme o chat
9. Título reativo — ATLAS/LYRA com cor e nome corretos conforme presença
10. Pontos no dock — animação de espera durante processamento
11. Microfone conectado — Whisper + VAD transcreve e envia automaticamente
12. Endpoint `/alarme` conectado ao módulo de alarmes

### Como rodar

```bash
# Terminal — API
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
uvicorn api:app --reload --port 8000

# Browser — abrir atlas_dashboard.html
```

---

## Próximo Passo

**Integrar módulos reais ao Atlas via API** — módulo por módulo:
- Alarmes reais disparando (endpoint existe, testar execução)
- Lembretes com horário
- ElevenLabs no dashboard — Atlas/Lyra falam em voz

---

## Status das Funcionalidades

| Funcionalidade | Status |
|---|---|
| Atlas + Lyra com IA real | ✅ |
| Dashboard completo + backend integrado | ✅ |
| Memória persistente entre sessões | ✅ |
| Microfone (Whisper + VAD) no dashboard | ✅ |
| Latência real, sessão viva, núcleo reativo | ✅ |
| Módulos reais via API (alarmes, lembretes) | 🔜 |
| ElevenLabs no dashboard (voz de saída) | 🔜 |
| Android (V4) | Futuro |

---

## Roadmap

| Fase | Status |
|---|---|
| V1-V3.2 — Fundação + IA + Voz | ✅ |
| Dashboard completo + FastAPI | ✅ |
| Módulos reais via API | 🔜 |
| V4 — Android | Futuro |
| V5 — Ecossistema IoT | Futuro |

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 01/05/2026 — 19:35*
