---
name: atlas-state
description: Skill do projeto Atlas Voice. Use SEMPRE que o JP (João Paulo) iniciar uma sessão de trabalho no Atlas Voice, mencionar "onde paramos", "retomar o projeto", "estado atual", ou qualquer variação. Esta skill carrega o contexto completo do projeto e instrui como retomar com precisão cirúrgica — sem reexplicar nada, sem perder progresso.
---

# Atlas State — Retomada de Sessão

## Identidade do Projeto

**Projeto:** Atlas Voice  
**Fundador:** João Paulo da Silva Coelho (JP) — Manaus, Brasil  
**Repositório principal:** github.com/joaopaulodasilvacoelho11-bot/atlas-voice  
**Backup:** github.com/joaopaulodasilvacoelho11-bot/AtlasVoiceBackup  
**Localização local:** `C:\Users\Gleida\Desktop\atlas-voice-v1`  
**Ambiente:** Anaconda — env: `atlasvoice`  
**Ferramentas:** Claude.ai (planejamento), Claude Code (edição de código), Replit (testes)

---

## Como Retomar — Sem Perguntas

Ao iniciar uma sessão com o JP, NÃO perguntar onde parou. Leia este documento, identifique o próximo passo e apresente diretamente:

> "Estou dentro. Última sessão: [resumo]. Próximo passo: [ação concreta]. Começamos?"

---

## Última Sessão — 23/04/2026

### O que foi feito
1. **Voz de entrada — Whisper** — `voz/entrada.py` criado — grava 5s do microfone, detecta energia, transcreve com modelo `base`
2. **Voz de saída — ElevenLabs** — `voz/saida.py` criado — sintetiza resposta com `eleven_multilingual_v2`, reproduz com pygame
3. **Filtro de energia** — silêncio ignorado antes de chamar o Whisper — evita transcrições fantasmas
4. **Normalização de comandos** — variações de "sair" por voz reconhecidas corretamente
5. **Integração no main.py** — `ouvir()` substituiu `input()`, `falar()` adicionado após cada resposta
6. **ElevenLabs configurado** — plano Iniciante ($6/mês) contratado, chave e voice ID no `.env`
7. **Commit V3 no GitHub** — `64ee7fc`

### Estado atual do código
```
voz/
├── entrada.py   ← NOVO — Whisper base + filtro de energia + ffmpeg via imageio
└── saida.py     ← NOVO — ElevenLabs eleven_multilingual_v2 + pygame
main.py          ← ATUALIZADO — ouvir() + falar() integrados no loop principal
.env             ← local only — ANTHROPIC_API_KEY + ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID
```

---

## Próximo Passo

**Melhorias de V3 — qualidade de voz**

1. **Detecção de voz ativa (VAD)** — gravar só quando houver fala, não tempo fixo de 5s
2. **Login por voz** — eliminar input de teclado no início
3. **Feedback sonoro** — Atlas emite som curto quando começa a ouvir

**Depois:** V4 — Android

---

## Status das Funcionalidades

| Funcionalidade | Status |
|---|---|
| Login seguro (bcrypt) | ✅ |
| Perfil por usuário | ✅ |
| Atlas respondendo | ✅ |
| Lyra respondendo | ✅ |
| Troca Atlas/Lyra | ✅ |
| Alarmes completos | ✅ |
| Lembretes com prioridade | ✅ |
| Memória entre sessões | ✅ |
| Histórico de interações | ✅ |
| Cronômetro | ✅ |
| Erros global + log | ✅ |
| Contexto de sessão | ✅ |
| Respostas variadas | ✅ |
| Timer regressivo | ✅ |
| Notas rápidas | ✅ |
| Integração IA (V2) | ✅ |
| Voz real — Whisper + ElevenLabs (V3) | ✅ Completa |
| VAD — detecção de voz ativa | 🔜 Próximo |
| Login por voz | 🔜 Próximo |
| Android (V4) | Futuro |

---

## Roadmap Resumido

| Fase | Foco | Status |
|---|---|---|
| V1 | Fundação — CLI funcional | ✅ |
| V2 | Inteligência — IA externa (Claude API) | ✅ |
| V3 | Voz real — Whisper + ElevenLabs | ✅ |
| V4 | Mobile — Android + voz nativa | Futuro |
| V5 | Ecossistema — IoT, saúde, emergência | Futuro |
| V6 | Escala nacional | Futuro |

---

## Regras do Projeto

- Nenhuma versão nasce do zero
- Toda base herda 100% das anteriores
- Nunca avançar sem fechar a fase atual
- Backup antes de qualquer mudança grande
- Um módulo por vez — foco e destreza
- Claude Code para edição de código
- Testar no Anaconda Prompt após cada mudança
- NUNCA commitar .env — chave sempre local

---

## Como Rodar o Sistema

```bash
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
python main.py
```

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 23/04/2026*
