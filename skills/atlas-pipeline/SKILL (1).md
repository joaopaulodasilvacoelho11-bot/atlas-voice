---
name: atlas-pipeline
description: Skill do projeto Atlas Voice. Use sempre que o JP mencionar bases, pipeline, módulos, camadas, base_2_x, base_Bx, ou quando for desenvolver, integrar ou depurar qualquer componente do sistema Atlas Voice. Esta skill contém o mapa completo do pipeline de processamento — do que cada base faz, como se conectam, e qual é a ordem de execução.
---

# Atlas Pipeline — Mapa Completo das Bases

## Visão Geral do Fluxo

```
ENTRADA (voz/texto)
    ↓
[B1] Detecção
    ↓
[B2] Interpretação
    ↓
[2.3] Compreensão Humana
    ↓
[2.4] Motor Temporal
    ↓
[2.5] Classificador de Intenção
    ↓
[2.6] Orquestrador Intenção + Tempo
    ↓
[B3] Decisão
    ↓
[2.7] Orquestrador Resposta Pré-Voz
    ↓
[B4] Execução
    ↓
SAÍDA (texto/voz)
```

**Lei do pipeline:** cada base herda 100% da anterior. Nenhuma nasce do zero.

---

## Pipeline Principal — Bases 2.x

### base_2_0 — Fundação
| Arquivo | Função |
|---|---|
| `base_2_0_entrada_oficial.py` | Recebe e normaliza a entrada do usuário |
| `base_2_0_motor_execucao.py` | Motor central de execução de comandos |
| `base_2_0_orquestrador_consciente.py` | Orquestrador com consciência de contexto |

**Herança:** ponto de partida — todas as bases 2.x descendem daqui.

---

### base_2_2 — Identidade Viva
| Arquivo | Função |
|---|---|
| `base_2_2_orquestrador_identidade_viva.py` | Mantém a identidade do Atlas coerente entre sessões |

**O que faz:** garante que o Atlas responde sempre como Atlas — mesmo com contexto variável.  
**JSON gerado:** `identidade_viva_2_2.json`

---

### base_2_3 — Compreensão Humana
| Arquivo | Função |
|---|---|
| `base_2_3_compreensao_humana.py` | Versão de desenvolvimento |
| `base_2_3_compreensao_humana_oficial.py` | Versão oficial em uso |

**O que faz:** interpreta linguagem natural humana — gírias, abreviações, contexto emocional, intenção implícita.

---

### base_2_4 — Motor Temporal
| Arquivo | Função |
|---|---|
| `base_2_4_motor_temporal_oficial.py` | Interpreta referências de tempo natural |

**O que faz:** converte expressões como "daqui a pouco", "amanhã cedo", "depois do almoço" em timestamps precisos.  
**Usado por:** alarmes, lembretes, agendamentos.

---

### base_2_5 — Classificador de Intenção
| Arquivo | Função |
|---|---|
| `base_2_5_classificador_intencao_oficial.py` | Classifica a intenção do usuário e roteia para o módulo correto |

**O que faz:** decide o que o usuário quer fazer e para onde a requisição vai.  
**Saídas possíveis:** alarme, lembrete, pergunta, comando, conversa, configuração.

---

### base_2_6 — Orquestrador Intenção + Tempo
| Arquivo | Função |
|---|---|
| `base_2_6_orquestrador_intencao_tempo_oficial.py` | Une classificação de intenção com motor temporal |

**O que faz:** primeira integração completa — sabe O QUE o usuário quer E QUANDO.

---

### base_2_7 — Orquestrador Resposta Pré-Voz ← ÚLTIMA BASE CONSOLIDADA
| Arquivo | Função |
|---|---|
| `base_2_7_orquestrador_resposta_pre_voz_oficial.py` | Prepara a resposta final antes da saída por voz |

**O que faz:** formata, ajusta tom (Atlas ou Lyra), e entrega a resposta pronta para ser falada ou exibida.  
**Status:** ✅ Base consolidada — ponto de referência atual do projeto.

---

### base_2_8 — Orquestrador (em desenvolvimento)
| Arquivo | Função |
|---|---|
| `base_2_8_orquestrador.py` | Próxima evolução do orquestrador central |

**Status:** 🔧 Em progresso — herda da 2.7.

---

## Pipeline B — Comportamento Autônomo

Pipeline paralelo que controla como o Atlas age, não só como responde.

### base_B1 — Detecção
**Arquivo:** `base_B1_deteccao.py`  
**O que faz:** detecta o tipo de input — voz, texto, comando, pergunta, emoção, urgência.  
**Posição no fluxo:** primeira camada — tudo passa por aqui.

---

### base_B2 — Interpretação
**Arquivo:** `base_B2_interpretacao.py`  
**O que faz:** interpreta o que foi detectado em B1 — dá significado ao input bruto.  
**Depende de:** B1 + bases 2.3 e 2.4.

---

### base_B3 — Decisão
**Arquivo:** `base_B3_decisao.py`  
**O que faz:** decide qual ação tomar com base na interpretação — executa, pergunta, aguarda, delega.  
**Regra:** o usuário sempre comanda. O Atlas sugere, nunca decide sozinho.

---

### base_B4 — Execução
**Arquivo:** `base_B4_execucao.py`  
**O que faz:** executa a ação decidida em B3 — aciona funcionalidade, gera resposta, salva estado.  
**Posição no fluxo:** última camada antes da saída.

---

## Camadas de Suporte

Módulos que alimentam o pipeline principal com dados contextuais.

| Arquivo | Função |
|---|---|
| `camada_1_8_interativa.py` | Interação contextual — mantém fluxo de conversa |
| `camada_1_8_lembretes.py` | Gestão de lembretes com prioridade |
| `camada_1_8_prioridade.py` | Sistema de priorização de tarefas |
| `camada_1_9_motor_decisao.py` | Motor de decisão avançado |
| `camada_1_9_motor_decisao_9_9.py` | Versão refinada do motor de decisão |
| `camada_2_1_contexto_emocional.py` | Detecta e mantém contexto emocional do usuário |
| `camada_2_1_historico_avancado.py` | Histórico de interações com indexação |
| `camada_2_1_identidade_viva.py` | Identidade persistente entre sessões |

---

## JSONs de Estado

Arquivos gerados em uso — persistência entre sessões.

| Arquivo | O que armazena |
|---|---|
| `identidade_viva_2_1_3.json` | Estado da identidade do Atlas |
| `identidade_viva_2_2.json` | Estado atualizado da identidade |
| `contexto_emocional_2_1.json` | Contexto emocional atual do usuário |
| `historico_avancado_2_1.json` | Histórico completo de interações |
| `execucao_2_0_log.json` | Log de execuções |
| `orquestracao_2_0_log.json` | Log de orquestrações |
| `orquestracao_2_2_log.json` | Log atualizado de orquestrações |
| `motor_decisao_1_9_log.json` | Log do motor de decisão |
| `lembretes_1_8.json` | Lembretes ativos |
| `consolidacao_log_1_7_1.json` | Log de consolidação da base 1.7 |

---

## Regras do Pipeline

```
1. Toda base herda 100% da anterior — nunca reescrever do zero
2. A base_2_7 é o ponto de referência atual
3. Qualquer nova base começa a partir da 2_7 ou 2_8
4. JSONs são gerados automaticamente — não editar manualmente
5. Testar cada base antes de integrar à próxima
6. B1→B4 e 2.x rodam em paralelo — não são sequenciais absolutos
```

---

## Próxima Evolução do Pipeline (V2)

Quando iniciar V2, o pipeline ganha:
- Integração com IA externa (Claude API)
- STT real (Whisper) na entrada
- TTS real (ElevenLabs) na saída
- Memória de longo prazo persistente
- Interface web no lugar da CLI

---

*Atlas Voice — Pipeline Map — JP Silva*  
*Atualizar sempre que uma nova base for consolidada*
