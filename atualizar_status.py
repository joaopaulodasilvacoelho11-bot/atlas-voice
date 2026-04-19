# ============================================
# Atlas Voice - Atualizador de Status
# Atualiza o README.md automaticamente
# Uso: py atualizar_status.py
# ============================================

import subprocess
from datetime import datetime
from pathlib import Path

FUNCIONALIDADES = [
    ("Login seguro (bcrypt)", True),
    ("Perfil por usuário", True),
    ("Atlas respondendo", True),
    ("Lyra respondendo", True),
    ("Troca Atlas/Lyra por comando", True),
    ("Alarmes — criar por voz", True),
    ("Alarmes — cancelar com lista", True),
    ("Alarmes — horário passado vai para amanhã", True),
    ("Monitor de alarmes em segundo plano", True),
    ("Lembretes com prioridade", True),
    ("Memória entre sessões", True),
    ("Histórico de interações", True),
    ("Menu de configurações", True),
    ("Cronômetro (iniciar, parar, tempo, zerar)", True),
]

PROXIMOS_PASSOS = [
    "Timer com contagem regressiva",
    "Notas rápidas por voz",
    "Lista de tarefas (to-do)",
    "Integração com IA externa (V2)",
    "Interface web (V2)",
    "Voz real com ElevenLabs (V3)",
]

VERSAO = "V1.1"


def obter_ultimos_commits(n=5):
    try:
        resultado = subprocess.run(
            ["git", "log", f"-{n}", "--pretty=format:%h %ad %s", "--date=short"],
            capture_output=True, text=True, encoding="utf-8"
        )
        if resultado.returncode == 0:
            return resultado.stdout.strip().split("\n")
        return []
    except Exception:
        return []


def obter_branch():
    try:
        resultado = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, encoding="utf-8"
        )
        return resultado.stdout.strip() or "master"
    except Exception:
        return "master"


def gerar_readme():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    branch = obter_branch()
    commits = obter_ultimos_commits()

    linhas_func = ""
    for nome, ativo in FUNCIONALIDADES:
        status = "✅" if ativo else "🔲"
        linhas_func += f"| {status} | {nome} |\n"

    linhas_proximos = ""
    for item in PROXIMOS_PASSOS:
        linhas_proximos += f"- 🔲 {item}\n"

    linhas_commits = ""
    if commits:
        for c in commits:
            if c.strip():
                linhas_commits += f"- `{c.strip()}`\n"
    else:
        linhas_commits = "- Nenhum commit encontrado.\n"

    return f"""# Atlas Voice {VERSAO}
> Assistente pessoal de voz — JP Silva, Manaus, Brasil
> *"Presença contínua, não uma ferramenta."*

---

## Status do Projeto
> Última atualização: **{agora}** | Branch: `{branch}`

---

## Funcionalidades

| Status | Funcionalidade |
|--------|----------------|
{linhas_func}
---

## Próximos Passos

{linhas_proximos}
---

## Últimos Commits

{linhas_commits}
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
"""


if __name__ == "__main__":
    readme_path = Path(__file__).parent / "README.md"
    conteudo = gerar_readme()
    readme_path.write_text(conteudo, encoding="utf-8")
    print(f"README.md atualizado — {datetime.now().strftime('%d/%m/%Y %H:%M')}")