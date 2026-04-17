# Atlas Voice V1

Assistente pessoal de voz com dois núcleos: **Atlas** (estratégico, direto) e **Lyra** (emocional, acolhedor). O usuário conversa em linguagem natural e o sistema classifica a intenção, interpreta tempo, gerencia alarmes e lembretes, e persiste memória entre sessões.

---

## Estrutura do projeto

```
atlas-voice-v1/
├── main.py                          # Entrada única do sistema
├── config.py                        # Caminhos e configurações
├── requirements.txt
├── core/                            # Reservado para extensões futuras
├── nucleos/
│   ├── atlas_nucleo.py              # Núcleo estratégico
│   └── lyra_nucleo.py               # Núcleo emocional
├── pipeline/
│   ├── base_2_4_motor_temporal_oficial.py       # Interpretação de tempo natural
│   └── base_2_5_classificador_intencao_oficial.py  # Classificação de intenção
├── funcionalidades/
│   ├── alarmes.py                   # Gerenciamento de alarmes
│   ├── lembretes.py                 # Gerenciamento de lembretes
│   └── memoria_persistente.py       # Histórico e sessões
└── data/                            # Gerado automaticamente (ignorado pelo git)
    ├── alarmes.json
    ├── lembretes.json
    ├── memoria.json
    └── usuarios.json
```

---

## Requisitos

- Python 3.10+
- bcrypt

---

## Instalação

```bash
cd atlas-voice-v1
pip install -r requirements.txt
```

---

## Como rodar

```bash
py main.py
```

No primeiro acesso, escolha a opção **2 (Criar conta)** e defina usuário e senha.

---

## Comandos disponíveis em sessão

| Comando | Ação |
|---|---|
| `me acorda às 8h` | Cria alarme |
| `cancelar alarme` | Lista alarmes ativos e cancela o escolhido |
| `me lembra de X às 15h` | Cria lembrete com prioridade Normal |
| `me lembra de X às 15h urgente` | Cria lembrete com prioridade Alta |
| `cancelar lembrete` | Lista lembretes ativos e cancela o escolhido |
| `falar com Lyra` | Muda para o núcleo emocional |
| `mudar para Atlas` | Muda para o núcleo estratégico |
| `configurar` | Abre menu de configurações |
| `sair` / `encerrar` | Encerra e salva a sessão |

---

## Configurações por variável de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `ATLAS_PROJECT_NAME` | `atlas-voice-v1` | Nome do projeto |
| `ATLAS_LOG_LEVEL` | `INFO` | Nível de log |
| `ATLAS_SAMPLE_RATE` | `16000` | Taxa de amostragem de áudio |
| `ATLAS_LANGUAGE` | `pt-BR` | Idioma |
