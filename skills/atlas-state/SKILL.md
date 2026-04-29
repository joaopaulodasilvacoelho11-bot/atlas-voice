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

## Última Sessão — 29/04/2026

### O que foi feito

1. **Dashboard exportado do Claude Design** — HTML completo com todos os arquivos (app.jsx, vortex.jsx, background.jsx, styles.css, tweaks-panel.jsx)
2. **Ampulheta removida** — stage central limpo, sem presença visual ainda
3. **Esfera de presença construída** — canvas animado com 4 estados:
   - `listening` — ondas de sonar se expandindo
   - `speaking` — ondas de som + raios de plasma coloridos
   - `thinking` — anéis concêntricos girando em direções opostas + arco de scan roxo
   - `idle` — respiração mínima, quase apagada
4. **ATLAS/LYRA implementados** — dois botões acima da esfera trocam a presença:
   - ATLAS → azul ciano
   - LYRA → roxo violeta
   - Transição de cor suave na esfera ao trocar
5. **Integrado no Claude Design** — esfera animada substituiu a esfera estática, ATLAS/LYRA posicionados corretamente acima da esfera no painel direito
6. **Layout finalizado** — TROCAR PRESENÇA no topbar, OUVINDO/ATLAS/LYRA/esfera/MEMÓRIA/CONTEXTO/SESSÃO no painel direito, tudo alinhado

### Estado atual do dashboard

```
Topbar:        ATLAS logo | Relógio | TROCAR PRESENÇA
Painel esq:    LATÊNCIA | SINAL | MODELO | CANAL
Centro:        Stage vazio (ampulheta removida)
Painel dir:    OUVINDO | ATLAS/LYRA | Esfera animada | MEMÓRIA | CONTEXTO | SESSÃO
Transcript:    Mensagens acima do dock
Dock:          Input de chat + botão ENVIAR
```

### Arquivos da esfera

- `esfera_final2.html` — versão standalone para testes
- `esfera_design_final.js` — componente para integração

---

## Próximo Passo

**Integrar o núcleo central** — o stage central está vazio. Decidir e construir a presença visual central do Atlas Voice (o núcleo foi iniciado mas não integrado ao dashboard).

Opções em aberto:
- Núcleo infinito animado (nucleo_atlas_v4.html — construído, não integrado)
- Outra presença central a definir com JP

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
| Dashboard — layout base | ✅ |
| Esfera de presença animada (4 estados) | ✅ |
| ATLAS/LYRA com troca de cor | ✅ |
| Centro do dashboard (núcleo visual) | 🔜 Próximo |
| Dashboard integrado ao backend | 🔜 Futuro |
| Android (V4) | Futuro |

---

## Identidade Visual do Dashboard

| Elemento | Definição |
|---|---|
| Esfera de presença | Canvas animado — azul ciano (ATLAS) / roxo violeta (LYRA) |
| Estado ouvindo | Ondas de sonar expandindo |
| Estado falando | Ondas de som + raios de plasma |
| Estado processando | Anéis concêntricos + arco de scan |
| Estado idle | Respiração mínima |
| Cores ATLAS | Azul ciano #4dd9ff |
| Cores LYRA | Roxo violeta #b45aff |
| Fundo | Nebulosa espacial azul profundo com estrelas |
| Centro | Vazio — aguarda definição do núcleo |

---

## Decisões de Produto Definidas

- **Texto = padrão** — gratuito, sem consumir crédito
- **Voz = premium** — ativada por comando, consome ElevenLabs/Whisper
- **ATLAS e LYRA** — mesma esfera, cores diferentes, botões simples acima
- **Esfera nunca é estática** — sempre viva, mesmo em idle

---

## Roadmap Resumido

| Fase | Foco | Status |
|---|---|---|
| V1 | Fundação — CLI funcional | ✅ |
| V2 | Inteligência — IA externa (Claude API) | ✅ |
| V3 | Voz real — Whisper + ElevenLabs + VAD | ✅ |
| V3.1 | Modos texto/voz alternáveis | ✅ |
| V3.2 | VAD Silero — captura natural | ✅ |
| Dashboard | Interface visual — layout base + esfera | ✅ |
| Dashboard | Núcleo central visual | 🔜 |
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
*Atualizado: 29/04/2026*
