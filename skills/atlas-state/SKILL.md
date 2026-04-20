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

---

## Como Usar Esta Skill

Ao iniciar uma sessão com o JP:

1. **Leia este documento inteiro** antes de responder qualquer coisa
2. **Pergunte apenas o que mudou** desde a última sessão — não o que já está aqui
3. **Entre direto no ponto** — sem resumos, sem reexplicações da visão
4. **Tom:** cirúrgico, direto, preciso — como um co-fundador técnico

Frase de abertura ideal:
> "Estou dentro. O que foi feito desde a última sessão?"

---

## Estado Atual do Projeto — V1 Funcional

### Fase Atual
**V1 — Fundação** — Sistema funcional. Em validação com uso real do JP.

### Critério para avançar para V2
JP usa o V1 no dia a dia real → anota o que falta ou incomoda → bugs corrigidos → só então inicia V2.

### Funcionalidades entregues no V1

| Funcionalidade | Status |
|---|---|
| Login seguro (bcrypt) | ✅ |
| Perfil por usuário | ✅ |
| Atlas respondendo | ✅ |
| Lyra respondendo | ✅ |
| Troca Atlas/Lyra por comando | ✅ |
| Respostas naturais | ✅ |
| Alarmes — criar, cancelar, monitorar | ✅ |
| Lembretes com prioridade | ✅ |
| Memória entre sessões | ✅ |
| Histórico de interações | ✅ |
| Menu de configurações | ✅ |

### Limitações atuais
- Sem IA externa ainda
- Sem acesso à internet
- Só texto — voz ainda não implementada
- Interface CLI — sem tela visual ainda

---

## Estrutura de Arquivos — V1

```
atlas-voice-v1/
├── config.py                          ← caminhos dinâmicos
├── main.py                            ← entrada única
├── requirements.txt                   ← bcrypt
├── README.md
├── nucleos/
│   ├── atlas_nucleo.py               ← respostas estratégicas
│   └── lyra_nucleo.py                ← respostas emocionais
├── pipeline/
│   ├── base_2_4_motor_temporal.py    ← interpreta tempo natural
│   └── base_2_5_classificador.py    ← classifica intenção + roteia
├── funcionalidades/
│   ├── alarmes.py
│   ├── lembretes.py
│   └── memoria_persistente.py
└── data/                             ← JSONs gerados em uso
```

---

## Stack Técnica

| Camada | Tecnologia |
|---|---|
| Backend | Python |
| Ambiente | Anaconda (env: atlasvoice) |
| Entrada atual | Texto (voz futuramente) |
| Segurança | bcrypt |
| Persistência | JSON |
| Versionamento | GitHub |

---

## Roadmap Resumido

| Fase | Foco | Status |
|---|---|---|
| V1 | Fundação — CLI funcional | ✅ Em validação |
| V2 | Inteligência — IA externa + interface web | 🔜 Próximo |
| V3 | Mobile — Android + voz real (Whisper + ElevenLabs) | Futuro |
| V4 | Ecossistema — IoT, saúde, emergência | Futuro |
| V5 | Escala nacional — produto público | Futuro |
| V6+ | Presença total — multi-dispositivo, robótica | Visão |

---

## Regras do Projeto (Lei)

```
1. Nenhuma versão nasce do zero
2. Toda base herda 100% das anteriores
3. Nunca avançar sem fechar a fase atual
4. Backup antes de qualquer mudança grande
5. Um módulo por vez — foco e destreza
6. A lógica precisa estar sólida antes de construir interface
7. Todo código novo herda o anterior
```

---

## Valores do Trabalho

| Valor | Aplicação prática |
|---|---|
| Propósito | Cada linha tem razão de existir |
| Compromisso | Nenhuma base é abandonada |
| Foco | Um passo de cada vez |
| Destreza | Cirúrgico — preciso e eficiente |

---

## Protocolo de Atualização desta Skill

Ao final de cada sessão produtiva, o JP deve atualizar:
- O que foi feito nesta sessão
- Qual é o próximo passo concreto
- Se alguma funcionalidade mudou de status

Isso garante que a próxima sessão retome sem perda de nenhum passo.

---

## Núcleos do Sistema

- **ATLAS** — estratégico, direto, objetivo
- **LYRA** — emocional, calmo, acolhedor

O sistema decide quem responde. O usuário pode trocar quando quiser.

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Skill viva — atualizada a cada fase concluída*
