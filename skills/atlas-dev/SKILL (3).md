---
name: atlas-dev
description: Skill do projeto Atlas Voice. Use sempre que o JP pedir para escrever, corrigir, refatorar ou expandir código do Atlas Voice, ou quando for tomar decisões técnicas sobre arquitetura, integração ou stack. Esta skill contém os padrões de desenvolvimento, convenções de código, e como trabalhar cirurgicamente no projeto sem quebrar o que já funciona.
---

# Atlas Dev — Padrões de Desenvolvimento

## Princípio Central

> "Nenhuma versão nasce do zero. Toda base herda 100% das anteriores."

Antes de escrever qualquer linha de código, perguntar:
- Qual base estou expandindo?
- O que já existe que posso reaproveitar?
- Estou quebrando alguma funcionalidade existente?

---

## Stack Técnica

| Camada | Tecnologia | Observações |
|---|---|---|
| Linguagem | Python | Única linguagem do backend |
| Ambiente | Anaconda — env: `atlasvoice` | Sempre ativar antes de rodar |
| Segurança | bcrypt | Senhas nunca em texto plano |
| Persistência | JSON | Simples, direto, sem banco de dados ainda |
| Versionamento | GitHub | Commit antes de qualquer mudança grande |
| Testes | Replit (com limitações) | Repositório privado tem problema de sync |

### Ativar ambiente
```bash
conda activate atlasvoice
```

### Rodar o sistema
```bash
cd C:\Users\Gleida\Desktop\atlas-voice-v1
python main.py
```

---

## Estrutura de Pastas — Obrigatória

```
atlas-voice-v1/
├── config.py                    ← NUNCA mover ou renomear
├── main.py                      ← entrada única — não duplicar
├── requirements.txt
├── README.md
├── nucleos/
│   ├── atlas_nucleo.py
│   └── lyra_nucleo.py
├── pipeline/
│   ├── base_2_4_motor_temporal.py
│   └── base_2_5_classificador.py
├── funcionalidades/
│   ├── alarmes.py
│   ├── lembretes.py
│   └── memoria_persistente.py
├── data/                        ← gerado automaticamente — não versionar JSONs de uso
└── skills/                      ← skills do Claude para este projeto
```

---

## Convenções de Código

### Nomenclatura de arquivos
```
base_2_X_nome_da_base_oficial.py    ← bases do pipeline principal
base_BX_nome.py                     ← bases do pipeline comportamental
camada_X_X_nome.py                  ← camadas de suporte
nome_modulo.py                      ← módulos de funcionalidade
```

### Nomenclatura de funções
```python
# Descritivo e em português ou inglês consistente
def classificar_intencao(texto: str) -> dict:
def criar_alarme(horario: str, descricao: str) -> bool:
def carregar_memoria() -> dict:
```

### Estrutura padrão de um módulo
```python
# imports
import json
import os
from config import DATA_DIR

# constante de arquivo de dados (se necessário)
ARQUIVO_DADOS = os.path.join(DATA_DIR, "nome_modulo.json")

# função principal
def funcao_principal(parametro):
    """Docstring clara do que faz."""
    pass

# funções auxiliares
def _funcao_interna():
    pass

# bloco de teste (só em desenvolvimento)
if __name__ == "__main__":
    pass
```

### Persistência em JSON
```python
# Salvar
def salvar_dados(dados: dict, arquivo: str):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# Carregar
def carregar_dados(arquivo: str) -> dict:
    if not os.path.exists(arquivo):
        return {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)
```

---

## Regras de Desenvolvimento

```
1. Um módulo por vez — terminar antes de começar outro
2. Testar isolado antes de integrar ao pipeline
3. Commit no GitHub antes de qualquer mudança grande
4. Não editar JSONs de dados manualmente
5. config.py é a única fonte de caminhos — nunca hardcodar paths
6. main.py é o único ponto de entrada — nunca chamar módulos diretamente
7. Toda nova funcionalidade herda o estado atual do sistema
8. Documentar o que cada função faz — mesmo que brevemente
```

---

## Como Expandir uma Base Existente

### Passo a passo
1. **Leia a base atual** — entenda 100% do que ela faz
2. **Identifique o ponto de extensão** — onde a nova lógica se encaixa
3. **Escreva a extensão** — sem apagar o que já funciona
4. **Teste isolado** — rode só o novo trecho
5. **Integre** — conecte ao fluxo existente
6. **Teste o fluxo completo** — do `main.py` até a saída
7. **Commit** — salva no GitHub com mensagem clara

### Mensagem de commit padrão
```
[base_2_X] descrição do que foi feito
[feat] nome da funcionalidade adicionada
[fix] descrição do bug corrigido
[refactor] o que foi reorganizado
```

---

## Como Adicionar Nova Funcionalidade

```python
# 1. Criar arquivo em funcionalidades/
# funcionalidades/nova_funcionalidade.py

from config import DATA_DIR
import os, json

ARQUIVO = os.path.join(DATA_DIR, "nova_funcionalidade.json")

def executar(parametros):
    """Executa a nova funcionalidade."""
    pass

# 2. Registrar no classificador de intenção
# pipeline/base_2_5_classificador_intencao_oficial.py
# Adicionar novo caso de intenção

# 3. Conectar no main.py
# Importar e chamar quando a intenção for detectada
```

---

## Tratamento de Erros — Padrão

```python
# Sempre usar try/except em operações de I/O
def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"[ERRO] Arquivo corrompido: {arquivo}")
        return {}
```

---

## Integração com IA Externa — V2 (Planejado)

Quando iniciar V2, a integração com Claude API seguirá este padrão:

```python
# Será adicionado em nucleos/atlas_nucleo.py
import anthropic

def responder_com_ia(pergunta: str, contexto: dict) -> str:
    client = anthropic.Anthropic()
    mensagem = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system="Você é o Atlas — assistente estratégico do JP.",
        messages=[{"role": "user", "content": pergunta}]
    )
    return mensagem.content[0].text
```

---

## Checklist Antes de Commitar

```
[ ] O código roda sem erros?
[ ] As funcionalidades anteriores ainda funcionam?
[ ] Os JSONs de dados estão íntegros?
[ ] O main.py ainda é o único ponto de entrada?
[ ] A mensagem do commit é clara?
[ ] Backup feito antes de mudança grande?
```

---

## Ambiente de Desenvolvimento

| Ferramenta | Uso |
|---|---|
| VS Code | Editor principal |
| Anaconda | Gestão de ambiente Python |
| GitHub Desktop | Versionamento visual |
| Replit | Testes online (limitado) |
| scrcpy | Espelhamento Android (futuro) |

---

*Atlas Voice — Dev Standards — JP Silva*  
*Atualizar quando stack ou padrões mudarem*
