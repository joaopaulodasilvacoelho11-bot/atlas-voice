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

## Última Sessão — 22/04/2026

### O que foi feito
1. **Integração Claude API** — `nucleos/atlas_nucleo.py` e `nucleos/lyra_nucleo.py` — função `_chamar_ia()` criada, chama modelo Haiku, fallback garantido se falhar
2. **IA em `_desconhecida()`** — Atlas e Lyra agora tentam IA mesmo em intenções não reconhecidas
3. **Classificador expandido** — `pipeline/base_2_5_classificador_intencao_oficial.py` — novos padrões de `PERGUNTA` adicionados
4. **`.env` criado localmente** — chave `ANTHROPIC_API_KEY` protegida fora do Git
5. **`.gitignore` atualizado** — `.env` nunca vai pro GitHub
6. **Chave comprometida deletada** — nova chave criada e configurada
7. **Commit limpo no GitHub** — V2 completa no repositório

### Estado atual do código
```
nucleos/
├── atlas_nucleo.py   ← ATUALIZADO — _chamar_ia() + _SYSTEM_ATLAS + IA em _pergunta, _conversa, _desconhecida
└── lyra_nucleo.py    ← ATUALIZADO — _chamar_ia() importada + _SYSTEM_LYRA + IA em _pergunta, _conversa, _desconhecida

pipeline/
└── base_2_5_classificador_intencao_oficial.py  ← ATUALIZADO — novos padrões de PERGUNTA

.env                  ← local only — NUNCA no GitHub
.gitignore            ← .env protegido
```

---

## Próximo Passo — O que fazer agora

**V3 — Voz Real**

- **Entrada:** Whisper (OpenAI) — captura áudio do microfone e converte em texto
- **Saída:** ElevenLabs — converte resposta em áudio e reproduz no speaker
- Ponto de entrada: `main.py` — adicionar loop de voz antes do loop de texto
- Estratégia: cirúrgica — voz como camada sobre o sistema existente, texto como fallback

**Ordem de execução:**
1. Instalar dependências: `openai-whisper`, `sounddevice`, `elevenlabs`
2. Criar `voz/entrada.py` — captura e transcreve áudio
3. Criar `voz/saida.py` — sintetiza e reproduz resposta
4. Integrar no `main.py` — loop de voz ativo por padrão

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
| Integração IA (V2) | ✅ Completa |
| Voz real — Whisper + ElevenLabs (V3) | 🔜 Próximo |

---

## Roadmap Resumido

| Fase | Foco | Status |
|---|---|---|
| V1 | Fundação — CLI funcional | ✅ Completa |
| V2 | Inteligência — IA externa (Claude API) | ✅ Completa |
| V3 | Voz real — Whisper + ElevenLabs | 🔜 Próximo |
| V4 | Mobile — Android + voz nativa | Futuro |
| V5 | Ecossistema — IoT, saúde, emergência | Futuro |
| V6 | Escala nacional | Futuro |

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
8. NUNCA commitar .env — chave sempre local
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

- **ATLAS** — estratégico, direto, objetivo. System prompt: "Seja direto, objetivo e estratégico. Sem rodeios. Respostas curtas e precisas."
- **LYRA** — emocional, calmo, acolhedor. System prompt: "Seja acolhedora, empática e presente. Respostas humanas e calorosas, mas sem exagero."

---

## Segurança

- API Key da Anthropic: salva em `.env` local — nunca no GitHub
- `.gitignore` protege o `.env`
- Chave nomeada `atlas-voice` no console da Anthropic

---

## Protocolo de Atualização desta Skill

Ao final de cada sessão produtiva, JP cola o resumo do que foi feito e o Claude atualiza esta skill antes de encerrar. Isso garante continuidade perfeita na próxima sessão.

---

*Atlas Voice — JP Silva — Manaus, Brasil*  
*Atualizado: 22/04/2026*
