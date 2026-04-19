# Atlas Voice V1.1
> Assistente pessoal de voz — JP Silva, Manaus, Brasil
> *"Presença contínua, não uma ferramenta."*

---

## Status do Projeto
> Última atualização: **19/04/2026 12:54** | Branch: `master`

---

## Funcionalidades

| Status | Funcionalidade |
|--------|----------------|
| ✅ | Login seguro (bcrypt) |
| ✅ | Perfil por usuário |
| ✅ | Atlas respondendo |
| ✅ | Lyra respondendo |
| ✅ | Troca Atlas/Lyra por comando |
| ✅ | Alarmes — criar por voz |
| ✅ | Alarmes — cancelar com lista |
| ✅ | Alarmes — horário passado vai para amanhã |
| ✅ | Monitor de alarmes em segundo plano |
| ✅ | Lembretes com prioridade |
| ✅ | Memória entre sessões |
| ✅ | Histórico de interações |
| ✅ | Menu de configurações |
| ✅ | Cronômetro (iniciar, parar, tempo, zerar) |

---

## Próximos Passos

- 🔲 Timer com contagem regressiva
- 🔲 Notas rápidas por voz
- 🔲 Lista de tarefas (to-do)
- 🔲 Integração com IA externa (V2)
- 🔲 Interface web (V2)
- 🔲 Voz real com ElevenLabs (V3)

---

## Últimos Commits

- `1ded380 2026-04-19 feat: adiciona cronômetro (iniciar, parar, tempo, zerar)`
- `b0ccf0d 2026-04-18 feat: monitor de alarmes em segundo plano`
- `0714cf3 2026-04-18 fix: alarme passado avanca para amanha em ambos os formatos`
- `8cf77e3 2026-04-17 fix: respostas naturais Atlas e Lyra, bug alarme passado`
- `83b9165 2026-04-17 feat: lembretes por voz, cancelamento e README`

---

## Comandos Disponíveis

| Comando | Ação |
|---------|------|
| `me acorda às 8h` | Cria alarme |
| `cancelar alarme` | Lista e cancela alarme |
| `me lembra de X às 15h` | Cria lembrete Normal |
| `me lembra de X às 15h urgente` | Cria lembrete Alta prioridade |
| `cancelar lembrete` | Lista e cancela lembrete |
| `iniciar cronômetro` | Inicia cronômetro |
| `parar cronômetro` | Para cronômetro |
| `quanto tempo passou` | Consulta tempo decorrido |
| `zerar cronômetro` | Zera cronômetro |
| `falar com Lyra` | Ativa núcleo emocional |
| `mudar para Atlas` | Ativa núcleo estratégico |
| `configurar` | Menu de configurações |
| `sair` / `encerrar` | Encerra sessão |

---

## Requisitos

- Python 3.10+
- bcrypt

---

*Atlas Voice — JP Silva — Manaus, Brasil*
*Documento gerado automaticamente por atualizar_status.py*
