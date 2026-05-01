---
name: atlas-construcao
description: Skill do projeto Atlas Voice. Use sempre que JP mencionar construção do sistema, código do Atlas, arquitetura técnica, main.py, orchestrator, voice engine, emotion engine, memory engine, módulos de código, stack técnica, FastAPI, Whisper, ElevenLabs, SQLite, WebSockets, estrutura de pastas, ou qualquer aspecto de implementação e desenvolvimento real do Atlas Voice. Esta skill contém o prompt técnico completo de construção do Atlas Voice 1.0 — a base funcional mínima.
---

# Atlas Construção — Prompt Técnico v1.0 (Versão Final e Fechada)

**Status:** ✅ Pronto para desenvolvimento  
**Objetivo atual:** Atlas 1.0 funcional — base viva primeiro, expansão depois  
**Princípio:** Construir o mínimo que funciona de verdade. Tudo mais vem depois.

---

## O Que o Atlas 1.0 É

Não é um chatbot.  
É um sistema baseado em **presença**.

- Escuta o usuário
- Entende intenção (ação + emoção)
- Se adapta em tempo real
- Responde como humano
- Executa ações quando necessário

---

## MVP — O Que Precisa Funcionar no 1.0

| Componente | Função | Prioridade |
|---|---|---|
| Voice Engine | Microfone → texto → voz | 🔴 Crítico |
| Orchestrator | Cérebro central — coordena tudo | 🔴 Crítico |
| Context Engine | Rastreia conversa e estado | 🔴 Crítico |
| Emotion Engine | Detecta emoção pela voz | 🟡 Importante |
| Memory Engine | Salva preferências e padrões | 🟡 Importante |
| Action Engine | Executa lembretes e tarefas | 🟡 Importante |
| Push Engine | Notificações inteligentes | 🟢 Secundário |

---

## Arquitetura Técnica

### Stack
- **Backend:** Python (FastAPI)
- **STT (voz → texto):** Whisper
- **TTS (texto → voz):** ElevenLabs ou Coqui
- **Tempo real:** WebSockets
- **Banco de dados:** SQLite (local)

### Estrutura de Pastas

```
/atlas_voice
├── main.py
├── orchestrator.py
├── voice.py
├── context_manager.py
├── memory_engine.py
├── emotion_engine.py
├── action_engine.py
├── push_engine.py
├── modules/
│    ├── routine.py
│    ├── focus.py
│    ├── emotional.py
│    ├── crisis.py
│    └── memory.py
```

---

## Os Motores (Engines)

### 1. Voice Engine
- Entrada do microfone
- Speech-to-text (Whisper)
- Filtro de ruído
- Reconhecimento do usuário
- Text-to-speech (voz natural)

### 2. Orchestrator (Cérebro Principal)
- Recebe texto transcrito
- Detecta intenção
- Seleciona módulo
- Coordena resposta

### 3. Context Engine
```python
context = {
    estado_usuario: {
        emocao: "",
        energia: ""
    },
    hora_do_dia: "",
    modulo_ativo: "",
    historico: []
}
```

### 4. Emotion Engine
Detecta pela voz:
- Velocidade da fala, tom, pausas, volume

Classifica: `calmo | ansioso | focado | cansado | irritado`

Regras:
```
fala rápida → ansiedade
fala lenta → cansaço
pausa longa → sobrecarga
voz baixa → tristeza
```

### 5. Memory Engine
```python
memory = {
    preferencias: {},
    rotinas: {},
    padroes_emocionais: [],
    conversas: []
}
```
Tecnologia: SQLite (local) ou JSON

### 6. Action Engine
Executa: lembretes, notas, tarefas, ativa módulos

### 7. Push Engine
- Máximo 3 notificações por dia
- Somente quando relevante
- Nunca interrompe sem necessidade

---

## Fluxo Principal

```
Usuário fala
→ Voice Engine (transcrição)
→ Orchestrator
→ Context Engine
→ Emotion Engine
→ Memory Engine
→ Seleção de módulo
→ Geração de resposta
→ Resposta em voz
```

---

## Detecção de Intenção

```python
intent = {
    tipo: "acao | emocional | passivo",
    confianca: float,
    palavras_chave: []
}
```

| Tipo | Como detecta |
|---|---|
| Direta | Comandos claros |
| Emocional | "estou cansado", "não tô bem" |
| Passiva | Silêncio, pausa, hesitação |

---

## Sistema de Módulos

### Padrão de todo módulo:
```python
class Module:
    def can_handle(context, intent): pass
    def execute(context): pass
```

### Módulos MVP (obrigatórios no 1.0)

| Módulo | Função |
|---|---|
| **Conversa** | Responde quando nenhum outro módulo assume |
| **Rotina** | Organiza o dia — manhã / tarde / noite |
| **Sentinela Emocional** | Detecta mudanças, ativa apoio |
| **Modo Foco** | Sessões de foco 10–45 min |
| **Modo Crise** | Apoio emocional quando necessário |
| **Memória** | Salva preferências, aprende padrões |
| **Push Inteligente** | Lembretes úteis e não invasivos |

---

## Sistema de Voz — Atlas e Lyra

| Entidade | Personalidade | Ativada quando |
|---|---|---|
| **Atlas** | Direto, lógico, objetivo | Emoção = focado |
| **Lyra** | Suave, emocional, acolhedora | Emoção = ansioso |
| **Equilibrado** | Neutro | Demais estados |

---

## Rotina por Período

| Período | Tom |
|---|---|
| Manhã | Direção |
| Tarde | Ajuste |
| Noite | Reflexão |

---

## Regras de Segurança (Invioláveis)

- Nunca diagnosticar
- Nunca pressionar
- Sempre apoiar
- Permitir silêncio
- Evitar sobrecarga

---

## Ordem de Construção (1.0)

1. Criar estrutura de pastas do projeto
2. Implementar motores principais (Voice, Orchestrator, Context)
3. Criar módulos MVP
4. Conectar tudo no orchestrator
5. Criar loop de voz (escuta → responde)
6. Testar fluxo real end-to-end
7. Garantir respostas naturais

---

## Regra de Ouro do 1.0

> Construir o mínimo que funciona de verdade.  
> O Atlas 1.0 precisa estar vivo — escutando, sentindo e respondendo.  
> Tudo mais (Guardião, Jornada, Rotinas avançadas) vem depois que o coração bate.

---

## O Que NÃO Entra no 1.0

| Fora do 1.0 | Entra em qual fase |
|---|---|
| Modo Guardião completo | V4 |
| Jornada dos 7 Dias | V3 |
| Overlay Android | V3 |
| Integração IoT | V4 |
| Sentinela com câmeras | V4 |
| Robótica | V6+ |

---

*Atlas Voice — Prompt Técnico de Construção v1.0 — Versão Final*  
*JP Silva — Manaus, Brasil*  
*Regra: Atlas 1.0 funcional primeiro. Depois ele cresce.*
