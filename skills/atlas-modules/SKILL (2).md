---
name: atlas-modules
description: Skill do projeto Atlas Voice. Use sempre que o JP mencionar núcleos, ATLAS, LYRA, funcionalidades, módulos de alarme, lembrete, memória, perfil, ou quando for desenvolver, corrigir ou expandir qualquer funcionalidade do sistema. Esta skill contém o mapa completo dos núcleos e módulos funcionais do Atlas Voice.
---

# Atlas Modules — Núcleos e Funcionalidades

## Os Dois Núcleos

O Atlas Voice tem duas personalidades que operam sobre o mesmo sistema.

### ATLAS — Núcleo Estratégico
**Arquivo:** `nucleos/atlas_nucleo.py`

| Atributo | Valor |
|---|---|
| Tom | Direto, objetivo, preciso |
| Função | Responde tarefas, comandos, informações |
| Estilo | Co-piloto técnico — vai ao ponto |
| Ativação | Padrão do sistema |

**Quando responde:** comandos, perguntas técnicas, execução de tarefas, configurações.

---

### LYRA — Núcleo Emocional
**Arquivo:** `nucleos/lyra_nucleo.py`

| Atributo | Valor |
|---|---|
| Tom | Calmo, acolhedor, empático |
| Função | Suporte emocional, companhia, conversas |
| Estilo | Presença — ouve antes de responder |
| Ativação | Comando do usuário ou detecção emocional |

**Quando responde:** conversas pessoais, momentos de estresse, pedido explícito do usuário.

---

### Troca de Núcleo
- Usuário pode trocar a qualquer momento por comando de voz/texto
- Sistema também troca automaticamente por detecção emocional (via `camada_2_1_contexto_emocional.py`)
- **Regra:** quem manda é sempre o usuário

---

## Módulos Funcionais

### Alarmes
**Arquivo:** `funcionalidades/alarmes.py`

| Funcionalidade | Status |
|---|---|
| Criar alarme por voz/texto | ✅ |
| Cancelar alarme com lista | ✅ |
| Horário passado → vai para amanhã | ✅ |
| Monitor em segundo plano | ✅ |

**Integração:** usa `base_2_4_motor_temporal_oficial.py` para interpretar horários naturais.  
**Exemplos de comando:** "me acorda às 7", "cancela o alarme das 8", "alarme para daqui a 2 horas".

---

### Lembretes
**Arquivo:** `funcionalidades/lembretes.py`  
**JSON:** `lembretes_1_8.json`

| Funcionalidade | Status |
|---|---|
| Criar lembrete com prioridade | ✅ |
| Listar lembretes ativos | ✅ |
| Cancelar lembrete | ✅ |

**Prioridades:** alta, média, baixa  
**Integração:** `camada_1_8_lembretes.py` + `camada_1_8_prioridade.py`

---

### Memória Persistente
**Arquivo:** `funcionalidades/memoria_persistente.py`

| Funcionalidade | Status |
|---|---|
| Guardar informações entre sessões | ✅ |
| Recuperar contexto anterior | ✅ |
| Histórico de interações | ✅ |

**O que persiste:** preferências do usuário, histórico de conversas, contexto emocional, identidade do Atlas.  
**JSONs:** `historico_avancado_2_1.json`, `contexto_emocional_2_1.json`, `identidade_viva_2_2.json`

---

### Login e Perfil
**Arquivo:** `config.py` + sistema de autenticação

| Funcionalidade | Status |
|---|---|
| Login seguro com bcrypt | ✅ |
| Perfil por usuário | ✅ |
| Caminhos dinâmicos por perfil | ✅ |

**Segurança:** senhas nunca armazenadas em texto plano — sempre hash bcrypt.

---

### Menu de Configurações
| Funcionalidade | Status |
|---|---|
| Trocar núcleo ativo (Atlas/Lyra) | ✅ |
| Ver perfil | ✅ |
| Configurações de alarmes | ✅ |
| Configurações de lembretes | ✅ |

---

## Entrada — main.py

**Arquivo:** `main.py` — ponto único de entrada do sistema.

```
main.py
  ↓ login/autenticação
  ↓ carrega perfil do usuário
  ↓ inicializa núcleo ativo (Atlas ou Lyra)
  ↓ loop principal de interação
  ↓ roteia para pipeline ou funcionalidade
  ↓ retorna resposta formatada
```

**Regra:** toda interação passa pelo `main.py`. Nunca chamar módulos diretamente.

---

## config.py — Configuração Central

Gerencia caminhos dinâmicos — o sistema funciona independente de onde está instalado.

```python
# O que config.py define:
- BASE_DIR          ← raiz do projeto
- DATA_DIR          ← onde ficam os JSONs
- NUCLEOS_DIR       ← onde ficam atlas e lyra
- PIPELINE_DIR      ← onde ficam as bases
- FUNCIONALIDADES_DIR
```

---

## Regras dos Módulos

```
1. Nenhum módulo se comunica diretamente com outro — tudo passa pelo pipeline
2. Funcionalidades não conhecem os núcleos — os núcleos é que formatam as respostas
3. JSONs são a memória do sistema — nunca deletar sem backup
4. Cada módulo tem responsabilidade única — não misturar funções
5. Testar o módulo isolado antes de integrar
```

---

## Módulos Planejados para V2+

| Módulo | Fase | Descrição |
|---|---|---|
| Integração IA externa | V2 | Claude API para respostas inteligentes |
| Interface web | V2 | Painel visual — login, menus, chat |
| STT — Whisper | V3 | Voz real como entrada |
| TTS — ElevenLabs | V3 | Voz real como saída |
| Módulo saúde | V4 | Google Fit / HealthKit |
| Módulo emergência | V4 | Acionar contatos, serviços |
| Módulo IoT | V4 | Controle da casa |
| Módulo navegação | V4 | GPS e rotas |

---

*Atlas Voice — Modules Map — JP Silva*  
*Atualizar sempre que um novo módulo for entregue*
