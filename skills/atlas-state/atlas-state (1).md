---
name: atlas-state
description: Skill do projeto Atlas Voice. Use SEMPRE que o JP (João Paulo) iniciar uma sessão de trabalho no Atlas Voice, mencionar "onde paramos", "retomar o projeto", "estado atual", ou qualquer variação. Esta skill carrega o contexto completo do projeto e instrui como retomar com precisão cirúrgica — sem reexplicar nada, sem perder progresso.
---

# Atlas State — Retomada de Sessão

## Identidade do Projeto

**Projeto:** Atlas Voice  
**Fundador:** João Paulo da Silva Coelho (JP) — Manaus, Brasil  
**Repositório:** github.com/joaopaulodasilvacoelho11-bot/atlas-voice  
**Backup:** github.com/joaopaulodasilvacoelho11-bot/AtlasVoiceBackup  
**Localização local:** `C:\Users\Gleida\Desktop\atlas-voice-v1`  
**Ambiente:** Anaconda — env: `atlasvoice`  
**Ferramentas:** Claude.ai (planejamento), Claude Code (edição de código), Replit (testes), Claude Design (dashboard visual)

---

## Como Retomar — Sem Perguntas

Ao iniciar uma sessão com o JP, NÃO perguntar onde parou. Leia este documento, identifique o próximo passo e apresente diretamente:

> "Estou dentro. Última sessão: [resumo]. Próximo passo: [ação concreta]. Começamos?"

---

## Última Sessão — 25/04/2026

### O que foi feito

1. **Modos de entrada (V3.1)** — `_MODO_ENTRADA` + `_capturar()` implementados no `main.py`
2. **Alternância voz ↔ texto** — comandos "ativar voz" / "ativar texto" funcionando
3. **`falar()` condicional** — só chama ElevenLabs em modo voz
4. **Fluxos internos** — 4 `input()` hardcoded substituídos por `_capturar()`
5. **Login documentado** — mantido em texto por segurança, comentado no código
6. **VAD Silero (V3.2)** — `voz/entrada.py` refatorado com detecção de voz ativa
7. **Whisper small** — modelo trocado de `base` para `small` — melhor precisão pt-BR
8. **Filtro de transcrição suja** — caracteres fora do português ignorados
9. **Commits no GitHub** — V3.1 (`992fb1c`), V3.2 (`674382c`)
10. **Dashboard visual** — iniciado no Claude Design — layout completo aprovado
11. **Identidade visual definida** — ampulheta de energia (vórtice helicoidal) como presença central
12. **Claude Design — limite atingido** — renova terça-feira 28/04

### Estado atual do código

```
voz/
├── entrada.py   ← VAD Silero + Whisper small + filtro sujeira
└── saida.py     ← ElevenLabs eleven_multilingual_v2 + pygame
main.py          ← _MODO_ENTRADA + _capturar() + alternância voz/texto
.env             ← local only — ANTHROPIC_API_KEY + ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID
```

---

## Próximo Passo

**1. Claude Design (terça 28/04) — ajuste final da ampulheta:**
- Mover funil de cima mais para cima
- Mover funil de baixo mais para baixo
- Sem mudar o resto do layout

**2. Exportar dashboard do Claude Design como HTML**

**3. Integrar dashboard com backend Python via FastAPI**

**4. Chat real — input do dashboard vai para o Atlas de verdade**

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
| Cronômetro + Timer | ✅ |
| Notas rápidas | ✅ |
| Integração IA — Claude API (V2) | ✅ |
| Voz entrada — Whisper small + VAD (V3.2) | ✅ |
| Voz saída — ElevenLabs (V3) | ✅ |
| Modo texto / voz alternável (V3.1) | ✅ |
| Dashboard visual — Claude Design | 🔄 Em refinamento |
| Dashboard integrado ao backend | 🔜 Próximo |
| Android (V4) | Futuro |

---

## Identidade Visual do Dashboard

| Elemento | Definição |
|---|---|
| Presença central | Ampulheta de energia — vórtice helicoidal |
| Cores | Azul ciano elétrico + dourado sobre fundo nebulosa azul escuro |
| Funil superior | Anéis crescendo do centro para cima |
| Funil inferior | Anéis crescendo do centro para baixo |
| Centro | Ponto estreito brilhante conectando os dois funis |
| Fundo | Nebulosa espacial azul profundo com estrelas |
| ATLAS | Azul ciano — presença estratégica |
| LYRA | Roxo/violeta — presença emocional |

---

## Decisões de Produto Definidas

- **Texto = padrão** — gratuito, sem consumir crédito
- **Voz = premium** — ativada por comando, consome ElevenLabs/Whisper
- **No futuro** — sistema de créditos de voz para o usuário comprar
- **Tela de boas-vindas** — usuário escolhe Atlas ou Lyra antes de começar
- **Uma presença ativa** — não dois logos, uma presença ocupa a tela inteira
- **Rosto futuro** — decisão adiada para fase com designer ou solução técnica adequada

---

## Roadmap Resumido

| Fase | Foco | Status |
|---|---|---|
| V1 | Fundação — CLI funcional | ✅ |
| V2 | Inteligência — IA externa (Claude API) | ✅ |
| V3 | Voz real — Whisper + ElevenLabs + VAD | ✅ |
| V3.1 | Modos texto/voz alternáveis | ✅ |
| V3.2 | VAD Silero — captura natural | ✅ |
| Dashboard | Interface visual — Claude Design | 🔄 |
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
*Atualizado: 25/04/2026*
