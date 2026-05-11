---
name: atlas-state
description: Skill do projeto Atlas Voice. Use SEMPRE que o JP iniciar uma sessao de trabalho no Atlas Voice, mencionar "onde paramos", "retomar o projeto", "estado atual", ou qualquer variacao.
---

# Atlas State — Retomada de Sessao

## Identidade
- Projeto: Atlas Voice
- Fundador: JP Silva — Manaus, Brasil
- Repo: github.com/joaopaulodasilvacoelho11-bot/atlas-voice
- Local: C:\Users\Gleida\Desktop\atlas-voice-v1
- Ambiente: Anaconda — env: atlasvoice

## Como Rodar

```bash
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
uvicorn api:app --reload --port 8000
# Abrir atlas_dashboard.html no browser
```

## Estado Atual — 11/05/2026

### Degraus Concluidos

**Degrau 1 — Alarmes reais via IA** (concluido 06/05)
- extrator_alarme.py — detecta intencao + horario no texto
- Alarme persistente, repete a cada 20s ate confirmacao
- Cancelamento natural: "ok", "acordei", "pode parar"
- Integrado em chat_atlas e chat_lyra

**Degrau 2 — Lembretes reais via IA** (concluido 06/05, refinado 11/05)
- extrator_lembrete.py — detecta intencao + horario + prioridade
- Padroes: 15:30, 15h30, 15h, 8 horas, "13 e 23"
- Fix: _INTENCAO cobre "me lembre de" (lembr[ae][r]?)
- Fix: _HORARIO usa lookarounds (?<!\d)/(?!\d) em vez de \b
- Prioridade automatica: "urgente" -> Alta, "quando der" -> Baixa
- Resposta limpa: "Lembrete registrado para HH:MM: Mensagem."
- 3 endpoints: POST /lembrete, GET /lembretes, POST /lembretes/verificar
- Dashboard: loop de 15s verifica alarmes E lembretes (try/catch separados)

**Degrau 3 — Loop de verificacao no backend** (concluido 11/05)
- _loop_verificacao() — asyncio, roda a cada 30s via lifespan do FastAPI
- Verifica alarmes e lembretes independente do dashboard estar aberto
- Dispara voz diretamente do backend quando o horario chega

**Degrau 4 — Memoria de longo prazo real** (concluido 11/05)
- funcionalidades/memoria_persistente.py — registrar_interacao, obter_historico
- _montar_entrada injeta ultimas 5 interacoes da memoria longa como prefixo do historico
- chat_atlas e chat_lyra registram cada interacao apos resposta
- Atlas e Lyra agora lembram do historico entre sessoes distintas

**Degrau 5 — Memoria unificada do usuario** (concluido 11/05)
- registrar_interacao com respondente="usuario" em chat_atlas e chat_lyra
- resposta gravada e texto_final (ja com confirmacoes de alarme/lembrete)
- obter_historico sem filtro — Atlas e Lyra leem da mesma memoria
- Trocar de nucleo nao perde historico nem relacionamento

**Degrau 6 — Dashboard servido pelo FastAPI** (concluido 11/05)
- GET /dashboard retorna atlas_dashboard.html via FileResponse
- _BASE_DIR = pathlib.Path(__file__).parent
- Imports: StaticFiles, FileResponse, pathlib
- Dashboard acessivel em http://127.0.0.1:8000/dashboard

**Degrau 7 — Script iniciar.bat** (concluido 11/05)
- iniciar.bat na raiz do projeto — duplo clique sobe tudo
- conda activate atlasvoice -> abre browser em /dashboard -> uvicorn api:app --port 8000

**Degrau 8 — Modo presenca continua** (concluido 11/05)
- voz/presenca.py — loop: ouvir -> processar -> falar -> ouvir
- POST /presenca/iniciar — ativa o loop com o presence informado
- POST /presenca/parar — encerra o loop
- GET /presenca/status — retorna se esta ativo
- Fix: registrar_interacao movido para apos Degrau 2, garantindo texto_final correto

### Proximos Degraus

| Degrau | Status |
|---|---|
| 9 — Documentacao + tag v1.0 | pendente |

## Endpoints da API

| Endpoint | Metodo | Funcao |
|---|---|---|
| / | GET | Status |
| /chat/atlas | POST | Chat com Atlas |
| /chat/lyra | POST | Chat com Lyra |
| /voz/ouvir | POST | Microfone -> texto |
| /voz/falar | POST | Texto -> audio (suporta presence) |
| /alarme | POST | Criar alarme |
| /alarmes | GET | Listar alarmes |
| /alarmes/verificar | POST | Disparar alarmes no horario |
| /lembrete | POST | Criar lembrete |
| /lembretes | GET | Listar lembretes |
| /lembretes/verificar | POST | Disparar lembretes no horario |
| /sessao | GET | Dados da sessao |
| /sessao/resetar | POST | Limpar historico |

## Arquivos Principais

```
api.py                              — FastAPI principal, todos os endpoints
atlas_dashboard.html                — Dashboard React (tudo em um arquivo)
voz/saida.py                        — ElevenLabs TTS (suporta presence=atlas/lyra)
voz/entrada.py                      — Whisper STT
funcionalidades/extrator_alarme.py  — Regex alarme
funcionalidades/extrator_lembrete.py — Regex lembrete
funcionalidades/alarmes.py          — CRUD alarmes (JSON)
funcionalidades/lembretes.py        — CRUD lembretes (JSON)
funcionalidades/memoria_persistente.py — Memoria de longo prazo entre sessoes
nucleos/atlas_nucleo.py             — Nucleo Atlas (Claude Haiku)
nucleos/lyra_nucleo.py              — Nucleo Lyra (Claude Haiku)
```

## Variaveis de Ambiente (.env)

```
ANTHROPIC_API_KEY
ELEVENLABS_API_KEY
ELEVENLABS_VOICE_ID          — voz do Atlas
ELEVENLABS_VOICE_ID_LYRA     — voz da Lyra
```

*Atualizado: 11/05/2026 — Degrau 8 concluido — resta apenas o Degrau 9*
