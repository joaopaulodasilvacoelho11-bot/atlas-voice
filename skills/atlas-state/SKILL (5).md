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

## Última Sessão — 20/04/2026

### O que foi feito
1. **5 skills criadas** e salvas em `skills/` — atlas-state, atlas-pipeline, atlas-modules, atlas-dev, atlas-roadmap
2. **Módulo de erros global** — `funcionalidades/erros.py` — sistema nunca cai, log em `data/logs/atlas_erros.log`, comando `saúde` funcionando
3. **Contexto de sessão** — `funcionalidades/contexto_sessao.py` — Atlas lembra o que foi dito na sessão atual
4. **Monitor protegido** com try/except — não derruba o sistema se falhar
5. Tudo commitado e no GitHub

### Estado atual do código
```
funcionalidades/
├── alarmes.py
├── cronometro.py
├── lembretes.py
├── memoria_persistente.py
├── erros.py          ← NOVO — tratamento de erros global
└── contexto_sessao.py ← NOVO — contexto de conversa em memória
```

---

## Próximo Passo — O que fazer agora

**Continuar fortalecendo a base antes do V2. Próximas frentes na ordem:**

### 1. Respostas variadas — PRÓXIMA
Atlas e Lyra repetem sempre as mesmas frases. Precisa ter variações para parecer mais natural e vivo.
- Arquivo a editar: `nucleos/atlas_nucleo.py` e `nucleos/lyra_nucleo.py`
- Ação: adicionar listas de respostas variadas por intenção

### 2. Timer com contagem regressiva
Já existe cronômetro. Falta timer — "avisa daqui a 10 minutos".
- Arquivo a criar: `funcionalidades/timer.py`
- Integrar no `main.py`

### 3. Notas rápidas por voz
"anota aí: comprar pão" → salva em JSON → "quais minhas notas?"
- Arquivo a criar: `funcionalidades/notas.py`

### 4. Integração IA — V2
Quando base estiver sólida, integrar Claude API nos núcleos.
- Ponto de entrada: `nucleos/atlas_nucleo.py` — função `processar()`
- Rota apenas intenções `pergunta` e `conversa` para IA
- Comandos fixos continuam no fluxo atual

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
| Respostas variadas | 🔜 próximo |
| Timer regressivo | 🔜 |
| Notas rápidas | 🔜 |
| Integração IA (V2) | 🔜 |

---

## Roadmap Resumido

| Fase | Foco | Status |
|---|---|---|
| V1 | Fundação — CLI funcional | ✅ Em finalização |
| V2 | Inteligência — IA externa + interface web | 🔜 Próximo |
| V3 | Mobile — Android + voz real | Futuro |
| V4 | Ecossistema — IoT, saúde, emergência | Futuro |
| V5 | Escala nacional | Futuro |

---

## Regras do Projeto

```
1. Nenhuma versão nasce do zero
2. Toda base herda 100% das anteriores
3. Nunca avançar sem fechar a fase atual
4. Backup antes de qualquer mudança grande
5. Um módulo por vez — foco e destreza
6. Claude Code para edição de código — mais rápido
7. Testar no Anaconda Prompt após cada mudança
```

---

## Como Rodar o Sistema

```bash
# Abrir Anaconda Prompt
conda activate atlasvoice
cd C:\Users\Gleida\Desktop\atlas-voice-v1
python main.py

# Comandos especiais dentro do sistema:
saúde          → diagnóstico do sistema
configurar     → menu de configurações
falar com Lyra → ativa núcleo emocional
mudar para Atlas → ativa núcleo estratégico
sair           → encerra sessão
```

---

## Núcleos

- **ATLAS** — estratégico, direto, objetivo
- **LYRA** — emocional, calmo, acolhedor

---

## Protocolo de Atualização desta Skill

Ao final de cada sessão produtiva, JP cola o resumo do que foi feito e o Claude atualiza esta skill antes de encerrar. Isso garante continuidade perfeita na próxima sessão.

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 20/04/2026*
