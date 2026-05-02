---
name: atlas-roadmap
description: Skill do projeto Atlas Voice. Use sempre que o JP mencionar fases, roadmap, próximos passos, expansão, visão do projeto, ou quando for tomar decisões sobre o que construir a seguir. Esta skill contém o mapa completo de evolução do Atlas Voice — o que está feito, a escada exata até o 1.0, e a visão de longo prazo.
---

# Atlas Voice — Roadmap Completo

## A Visão

> "O Atlas Voice não é um app. É uma presença."

Atlas Voice é um ecossistema brasileiro de inteligência por voz — pessoal, contínuo, que aprende e evolui com o usuário. Feito para qualquer pessoa, qualquer classe social.

---

## Estado Atual — 01/05/2026

O sistema está **funcionalmente operante**. Possui dashboard visual, voz bidirecional, IA real, memória persistente e dois núcleos com personalidades distintas. O objetivo agora é **fechar o Atlas Voice 1.0** — versão completa, estável, sem lacunas funcionais.

---

## O que está FEITO ✅

### Backend Python
- Login seguro (bcrypt)
- Perfil por usuário
- Classificador de intenção (pipeline)
- Atlas Núcleo — estratégico, direto, com IA real (Claude Haiku)
- Lyra Núcleo — emocional, relacional, com IA real (Claude Haiku)
- Alarmes (criar, cancelar, listar, verificar disparo)
- Lembretes com prioridade
- Memória entre sessões (JSON persistente)
- Histórico de interações
- Cronômetro + Timer
- Notas rápidas
- Voz entrada — Whisper small + Silero VAD
- Voz saída — ElevenLabs (eleven_multilingual_v2)

### API FastAPI
- `/chat/atlas` — resposta com IA + histórico de sessão
- `/chat/lyra` — resposta com IA + histórico de sessão
- `/voz/ouvir` — microfone → Whisper → texto
- `/voz/falar` — texto → ElevenLabs → áudio
- `/alarme` — criar alarme real no JSON
- `/alarmes` — listar alarmes ativos
- `/alarmes/verificar` — disparar alarmes no horário
- `/sessao` — contador real de tempo e mensagens
- `/sessao/resetar` — limpar histórico

### Dashboard HTML
- Núcleo central animado (anéis orbitais, partículas, brasas de fogo)
- ATLAS e LYRA com cores, títulos e personalidades distintas
- Estado reativo: OUVINDO → PROCESSANDO → FALANDO
- Latência real no painel
- Sessão viva (contador + mensagens)
- Memória persistente entre sessões
- Microfone no dock (Whisper integrado)
- Botão ElevenLabs (voz de saída liga/desliga)
- Pontos animados durante espera
- Verificação de alarmes a cada 30s

---

## A Escada até o Atlas Voice 1.0

### Degrau 1 — Alarmes reais via IA 🔜 PRÓXIMO
**O que falta:** Quando o usuário pede um alarme, a IA confirma mas não chama o endpoint `/alarme`. O JSON fica vazio.

**O que precisa ser feito:**
- Detectar intenção de alarme na resposta da IA
- Extrair horário e descrição do texto
- Chamar `/alarme` automaticamente com os dados extraídos
- Atlas confirma que foi salvo de verdade

**Critério de conclusão:** Usuário diz "me acorda às 21h" → alarme aparece no `alarmes.json` → no horário certo dispara em voz.

---

### Degrau 2 — Lembretes reais via IA
**O que falta:** Mesmo problema dos alarmes — Lyra confirma mas não salva.

**O que precisa ser feito:**
- Detectar intenção de lembrete
- Chamar endpoint de lembretes com horário e descrição
- Lyra confirma com carinho que foi registrado

**Critério de conclusão:** "Lyra, lembra de ligar para minha mãe às 19h" → salvo no JSON → dispara no horário.

---

### Degrau 3 — Loop de verificação contínua
**O que falta:** Os alarmes só são verificados quando o dashboard está aberto. Precisa de um loop no backend.

**O que precisa ser feito:**
- Adicionar `verificar_alarmes()` em loop a cada 60s no `api.py` (background task)
- Quando dispara: fala em voz + aparece no transcript
- Funciona mesmo com dashboard fechado (backend rodando)

**Critério de conclusão:** Alarme dispara em voz mesmo sem interação ativa no dashboard.

---

### Degrau 4 — Memória de longo prazo real
**O que falta:** O Atlas lembra da sessão atual mas não lembra de conversas de dias anteriores de forma inteligente.

**O que precisa ser feito:**
- Salvar resumo de cada sessão em JSON
- Carregar os últimos N resumos como contexto ao iniciar nova sessão
- Atlas e Lyra fazem referência a conversas passadas naturalmente

**Critério de conclusão:** "Atlas, lembra o que conversamos ontem?" → responde com contexto real.

---

### Degrau 5 — Lyra conhece o Atlas (sistema integrado)
**O que falta:** Lyra não sabe que pode acionar o Atlas para tarefas técnicas.

**O que precisa ser feito:**
- Atualizar system prompt da Lyra com referência ao Atlas como parceiro técnico
- Quando Lyra recebe comando técnico, sugere acionar o Atlas
- Dashboard mostra a passagem de presença visualmente

**Critério de conclusão:** "Lyra, cria um alarme para mim" → Lyra reconhece, aciona o módulo ou sugere trocar para Atlas.

---

### Degrau 6 — Dashboard na pasta do projeto (não nos Downloads)
**O que falta:** O dashboard vive nos Downloads, não no projeto. Não está sendo aberto da pasta correta.

**O que precisa ser feito:**
- Dashboard aberto sempre de `C:\Users\Gleida\Desktop\atlas-voice-v1\atlas_dashboard.html`
- Script de inicialização (`iniciar.bat`) que abre o uvicorn + o dashboard automaticamente

**Critério de conclusão:** Um clique duplo no `iniciar.bat` → API sobe → dashboard abre no browser.

---

### Degrau 7 — Script de inicialização (`iniciar.bat`)
**O que precisa ser feito:**
```bat
@echo off
cd /d C:\Users\Gleida\Desktop\atlas-voice-v1
call conda activate atlasvoice
start uvicorn api:app --port 8000
timeout /t 3
start atlas_dashboard.html
```

**Critério de conclusão:** Atlas Voice inicia com um clique. Sem terminal, sem configuração.

---

### Degrau 8 — Testes de uso real + correções
**O que precisa ser feito:**
- JP usa o sistema no dia a dia por pelo menos 3 dias
- Anota o que incomoda, o que quebra, o que falta
- Cada bug corrigido, cada melhoria aplicada
- Sistema estável e confiável

**Critério de conclusão:** JP usa sem precisar abrir código.

---

### Degrau 9 — Documentação e fechamento do 1.0
**O que precisa ser feito:**
- README atualizado com instruções de uso
- `atlas-state` e `atlas-roadmap` atualizados
- Commit de fechamento: `[release] Atlas Voice 1.0`
- Tag no GitHub: `v1.0`

**Critério de conclusão:** Atlas Voice 1.0 está documentado, commitado e etiquetado.

---

## Após o 1.0 — O Que Vem Depois

| Fase | Foco |
|---|---|
| V1.1 | Melhorias da Lyra — lembretes emocionais, check-ins de bem-estar |
| V1.2 | Notas rápidas com voz — fala e salva |
| V2.0 | App Android nativo com voz sempre ativa |
| V3.0 | Ecossistema — IoT, câmeras, casa inteligente |
| V4.0 | Plataforma pública — lançamento Brasil |

---

## Regras do Projeto (Imutáveis)

- Nenhuma versão nasce do zero — herda 100% da anterior
- Nunca avançar sem fechar o degrau atual
- Backup antes de qualquer mudança grande
- Um módulo por vez — foco e destreza
- NUNCA commitar .env
- O usuário sempre comanda

---

## Como Rodar o Sistema Hoje

```bash
# Terminal
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
uvicorn api:app --reload --port 8000

# Browser
Abrir: C:\Users\Gleida\Desktop\atlas-voice-v1\atlas_dashboard.html
```

---

*Atlas Voice — Roadmap 1.0 — JP Silva — Manaus, Brasil*
*Atualizado: 01/05/2026*
