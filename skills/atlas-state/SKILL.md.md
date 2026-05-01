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
**Ferramentas:** Claude.ai (planejamento), Claude Code (edição de código), Replit (testes)

---

## Como Retomar — Sem Perguntas

Ao iniciar uma sessão com o JP, NÃO perguntar onde parou. Leia este documento, identifique o próximo passo e apresente diretamente:

> "Estou dentro. Última sessão: [resumo]. Próximo passo: [ação concreta]. Começamos?"

---

## Última Sessão — 01/05/2026

### O que foi feito

1. **Dashboard HTML completo** — arquivo único `atlas_dashboard.html` funcional, abre direto no navegador
2. **Núcleo central construído** — canvas animado com:
   - Esfera orbital com 4 anéis giratórios inclinados (dashed, mix de velocidades)
   - 60 partículas em órbita reagindo ao estado
   - 32 brasas de fogo delicadas ao redor do núcleo (âmbar + cor da presença)
   - Core pulsante com gradiente branco → cor da presença → escuro
3. **ATLAS/LYRA integrados** — troca de cor em todo o núcleo (ciano #4dd9ff / violeta #b45aff)
4. **Esfera do painel direito removida** — painel direito limpo: estado em texto + botões ATLAS/LYRA + stats
5. **Posicionamento** — núcleo no terço superior, transcript e dock abaixo sem sobrepor
6. **Fogo afinado** — brasas pequenas, lentas, delicadas — aprovado pelo JP

### Estado atual do dashboard

```
Topbar:        ATLAS logo | Relógio em tempo real | TROCAR PRESENÇA (funcional)
Painel esq:    LATÊNCIA | SINAL | MODELO (muda com presença) | CANAL animado
Centro:        Núcleo animado — anéis orbitais + partículas + brasas de fogo
Painel dir:    OUVINDO/estado | ATLAS/LYRA botões | MEMÓRIA | CONTEXTO | SESSÃO
Transcript:    Últimas 3 mensagens acima do dock
Dock:          Input + botão ENVIAR (respostas simuladas por enquanto)
```

### Arquivo entregue

- `atlas_dashboard.html` — dashboard completo, standalone, abre no browser

---

## Próximo Passo

**Integrar backend Python ao dashboard** — substituir as respostas simuladas do chat por chamadas reais à API do Atlas/Lyra via FastAPI.

Fluxo alvo:
1. Usuário digita no dock → POST para FastAPI local
2. FastAPI chama `atlas_nucleo.py` ou `lyra_nucleo.py`
3. Resposta aparece no transcript do dashboard

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
| Núcleo central animado com fogo | ✅ |
| ATLAS/LYRA com troca de cor | ✅ |
| Dashboard integrado ao backend (FastAPI) | 🔜 Próximo |
| Android (V4) | Futuro |

---

## Identidade Visual do Dashboard

| Elemento | Definição |
|---|---|
| Núcleo central | Canvas 420px — anéis orbitais + partículas + brasas |
| Brasas ATLAS | Âmbar/laranja + wisps ciano #4dd9ff |
| Brasas LYRA | Âmbar/laranja + wisps violeta #b45aff |
| Estado ouvindo | Pulse suave, brasas lentas |
| Estado falando | Burst de raios + brasas aceleradas |
| Estado processando | Arco de scan violeta + anéis rápidos |
| Estado idle | Respiração mínima, brasas quase apagadas |
| Fundo | Nebulosa espacial azul profundo com estrelas |
| Fonte display | Orbitron |
| Fonte mono | JetBrains Mono |

---

## Decisões de Produto Definidas

- **Texto = padrão** — gratuito, sem consumir crédito
- **Voz = premium** — ativada por comando, consome ElevenLabs/Whisper
- **ATLAS e LYRA** — mesma interface, cores diferentes, botões simples
- **Núcleo nunca é estático** — sempre vivo, mesmo em idle
- **Presença evolui com o tempo** — design do núcleo será refinado progressivamente

---

## Roadmap Resumido

| Fase | Foco | Status |
|---|---|---|
| V1 | Fundação — CLI funcional | ✅ |
| V2 | Inteligência — IA externa (Claude API) | ✅ |
| V3 | Voz real — Whisper + ElevenLabs + VAD | ✅ |
| V3.1 | Modos texto/voz alternáveis | ✅ |
| V3.2 | VAD Silero — captura natural | ✅ |
| Dashboard | Interface visual completa com núcleo animado | ✅ |
| Dashboard | Integração FastAPI — chat real | 🔜 |
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

Dashboard: abrir `atlas_dashboard.html` direto no navegador (F11 para tela cheia)

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 01/05/2026*
