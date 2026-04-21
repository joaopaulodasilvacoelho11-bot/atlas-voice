import json
import re
import sys
import threading
from datetime import datetime
from pathlib import Path

import bcrypt

from config import DIRS, ensure_dirs
from pipeline.base_2_5_classificador_intencao_oficial import classificar, Respondente
from pipeline.base_2_4_motor_temporal_oficial import interpretar as interpretar_tempo
from nucleos.atlas_nucleo import AtlasNucleo, Entrada, Intencao
from nucleos.lyra_nucleo import LyraNucleo
from funcionalidades.memoria_persistente import (
    salvar_sessao,
    carregar_sessao,
    registrar_interacao,
    obter_historico,
)
from funcionalidades.alarmes import verificar_alarmes, criar_alarme, cancelar_alarme, listar_alarmes
from funcionalidades.lembretes import (
    verificar_lembretes,
    criar_lembrete,
    cancelar_lembrete,
    listar_lembretes,
)
from funcionalidades.cronometro import (
    iniciar_cronometro,
    parar_cronometro,
    tempo_passado,
    zerar_cronometro,
)
from funcionalidades.timer import (
    iniciar_timer,
    cancelar_timer,
    tempo_restante_timer,
)
from funcionalidades.erros import (
    log_erro,
    log_info,
    log_aviso,
    executar_com_protecao,
    relatorio_saude,
)
from funcionalidades.contexto_sessao import (
    adicionar_mensagem,
    obter_contexto_formatado,
    limpar_contexto,
    contexto_tem_mencao,
)
_ARQUIVO_USUARIOS = DIRS["data"] / "usuarios.json"

_atlas = AtlasNucleo()
_lyra  = LyraNucleo()

_INTENCAO_MAP = {
    "saudacao":       Intencao.SAUDACAO,
    "lembrete":       Intencao.LEMBRETE,
    "pergunta":       Intencao.PERGUNTA,
    "comando":        Intencao.COMANDO,
    "conversa":       Intencao.CONVERSA,
    "fora_de_escopo": Intencao.DESCONHECIDA,
}


# ---------------------------------------------------------------------------
# Usuários
# ---------------------------------------------------------------------------

def _carregar_usuarios() -> dict:
    if not _ARQUIVO_USUARIOS.exists():
        return {}
    with _ARQUIVO_USUARIOS.open("r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_usuarios(usuarios: dict) -> None:
    _ARQUIVO_USUARIOS.parent.mkdir(parents=True, exist_ok=True)
    with _ARQUIVO_USUARIOS.open("w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)


def _hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def _verificar_senha(senha: str, hash_: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_.encode())


def _cadastrar(nome: str, senha: str) -> dict:
    usuarios = _carregar_usuarios()
    if nome in usuarios:
        return {"status": "existe"}
    perfil = {
        "hash_senha":   _hash_senha(senha),
        "criado_em":    datetime.now().isoformat(timespec="seconds"),
        "total_logins": 0,
        "respondente_preferido": "atlas",
    }
    usuarios[nome] = perfil
    _salvar_usuarios(usuarios)
    return {"status": "criado", "perfil": perfil}


def _login(nome: str, senha: str) -> dict:
    usuarios = _carregar_usuarios()
    if nome not in usuarios:
        return {"status": "nao_encontrado"}
    if not _verificar_senha(senha, usuarios[nome]["hash_senha"]):
        return {"status": "senha_errada"}
    usuarios[nome]["total_logins"] += 1
    _salvar_usuarios(usuarios)
    return {"status": "ok", "perfil": usuarios[nome]}


def _salvar_preferencia(nome: str, chave: str, valor) -> None:
    usuarios = _carregar_usuarios()
    if nome in usuarios:
        usuarios[nome][chave] = valor
        _salvar_usuarios(usuarios)


# ---------------------------------------------------------------------------
# Saudação personalizada
# ---------------------------------------------------------------------------

def _saudacao_inicial(nome: str, perfil: dict) -> str:
    hora = datetime.now().hour
    if 5 <= hora < 12:
        periodo = "Bom dia"
    elif 12 <= hora < 18:
        periodo = "Boa tarde"
    else:
        periodo = "Boa noite"

    logins = perfil.get("total_logins", 1)
    historico = obter_historico(limite=1)

    if logins == 1:
        return f"{periodo}, {nome}. Primeira sessão iniciada. Estou pronto."

    ultima = ""
    if historico:
        ts = historico[-1].get("timestamp", "")
        if ts:
            ultima = f" Última interação: {ts[:10]}."

    return f"{periodo}, {nome}. Sessão {logins} iniciada.{ultima}"


# ---------------------------------------------------------------------------
# Verificação passiva de alarmes e lembretes
# ---------------------------------------------------------------------------

def _checar_passivo() -> None:
    alarmes  = verificar_alarmes()
    lembretes = verificar_lembretes()

    for a in alarmes:
        print(f"\n  [ALARME] {a['mensagem']} ({a['horario'][:16]})")
    for l in lembretes:
        print(f"\n  [LEMBRETE/{l['prioridade'].upper()}] {l['mensagem']} ({l['hora'][:16]})")


# ---------------------------------------------------------------------------
# Menu de configuração
# ---------------------------------------------------------------------------

def _menu_configuracao(nome: str, respondente_atual: str) -> str:
    print("\n--- Configurações ---")
    print(f"  1. Respondente atual: {respondente_atual.upper()}")
    print("  2. Alterar respondente padrão")
    print("  3. Ver histórico recente (5 últimas)")
    print("  4. Voltar")
    opcao = input("  Opção: ").strip().lower()

    _opcao2 = {"2", "alterar", "alterar respondente", "respondente"}
    _opcao3 = {"3", "historico", "histórico", "ver histórico", "ver historico"}
    _opcao4 = {"4", "voltar", "sair", "fechar"}

    if opcao in _opcao2:
        novo = input("  Novo respondente (atlas / lyra): ").strip().lower()
        if novo in ("atlas", "lyra"):
            _salvar_preferencia(nome, "respondente_preferido", novo)
            print(f"  Respondente padrão alterado para {novo.upper()}.")
            return novo
        print("  Opção inválida.")

    elif opcao in _opcao3:
        hist = obter_historico(limite=5)
        if not hist:
            print("  Nenhuma interação registrada ainda.")
        for h in hist:
            print(f"  [{h['timestamp'][:16]}] {h['respondente'].upper()} | {h['usuario'][:60]}")

    elif opcao in _opcao4:
        pass

    else:
        print("  Opção não reconhecida.")

    return respondente_atual


# ---------------------------------------------------------------------------
# Detecção e criação de alarme via fala natural
# ---------------------------------------------------------------------------

_RE_ALARME = re.compile(
    r"\b(me\s+acord[ae]|acord[ae]|cria\s+alarme|criar\s+alarme|coloca\s+alarme|põe\s+alarme|bota\s+alarme)"
    r"(?:\s+(?:para|pra|às?|as))?\b",
    re.IGNORECASE,
)


def _tentar_criar_alarme(texto: str) -> str | None:
    if not _RE_ALARME.search(texto):
        return None

    tempo = interpretar_tempo(texto)
    hora  = tempo.get("hora")

    if not hora:
        return "Entendi que você quer um alarme, mas não identifiquei o horário. Tente: 'me acorda às 7h'."

    dia = tempo.get("dia")
    try:
        h, m   = map(int, hora.split(":"))
        base   = datetime.fromisoformat(dia) if dia else datetime.now()
        alvo   = base.replace(hour=h, minute=m, second=0, microsecond=0)
        if alvo <= datetime.now():
            from datetime import timedelta
            alvo += timedelta(days=1)
        horario_str = f"{hora} {alvo.strftime('%d/%m/%Y')}"
    except Exception:
        horario_str = hora

    mensagem = texto.strip()
    resultado = criar_alarme(horario_str, mensagem)

    if resultado["status"] == "criado":
        periodo = tempo.get("periodo") or ""
        aviso   = " (horário estimado)" if tempo.get("ambiguidade") else ""
        sufixo  = f" da {periodo}" if periodo else ""
        dia_aviso = f" ({alvo.strftime('%d/%m')})" if alvo.date() != datetime.now().date() else ""
        return f"Alarme criado para {hora}{sufixo}{dia_aviso}{aviso}."

    if resultado["status"] == "duplicado":
        return f"Já existe um alarme para {hora}."

    return "Não consegui criar o alarme. Tente novamente."


# ---------------------------------------------------------------------------
# Criação e cancelamento de lembrete via fala natural
# ---------------------------------------------------------------------------

_RE_LEMBRETE = re.compile(
    r"\b(me\s+lembra\s+de?|lembra\s+de?|me\s+avisa\s+de?|avisa\s+de?|cria\s+lembrete|criar\s+lembrete|coloca\s+lembrete)\b",
    re.IGNORECASE,
)

_RE_PRIORIDADE_LEMBRETE = re.compile(
    r"\b(urgente|importante|alta\s+prioridade|prioridade\s+alta)\b",
    re.IGNORECASE,
)

_RE_CANCELAR_LEMBRETE = re.compile(
    r"\b(cancela(r)?|remove(r)?|apaga(r)?|deleta(r)?|exclui(r)?)\s+(o\s+)?lembrete\b",
    re.IGNORECASE,
)


def _tentar_criar_lembrete(texto: str) -> str | None:
    if not _RE_LEMBRETE.search(texto):
        return None

    tempo = interpretar_tempo(texto)
    hora  = tempo.get("hora")

    if not hora:
        return "Entendi que você quer um lembrete, mas não identifiquei o horário. Tente: 'me lembra de ligar às 15h'."

    dia = tempo.get("dia")
    try:
        h, m   = map(int, hora.split(":"))
        base   = datetime.fromisoformat(dia) if dia else datetime.now()
        alvo   = base.replace(hour=h, minute=m, second=0, microsecond=0)
        if alvo <= datetime.now():
            from datetime import timedelta
            alvo += timedelta(days=1)
        hora_str = f"{hora} {alvo.strftime('%d/%m/%Y')}"
    except Exception:
        hora_str = hora
        alvo     = datetime.now()

    prioridade = "Alta" if _RE_PRIORIDADE_LEMBRETE.search(texto) else "Normal"
    resultado  = criar_lembrete(hora_str, texto.strip(), prioridade)

    if resultado["status"] == "criado":
        periodo   = tempo.get("periodo") or ""
        aviso     = " (horário estimado)" if tempo.get("ambiguidade") else ""
        sufixo    = f" da {periodo}" if periodo else ""
        dia_aviso = f" ({alvo.strftime('%d/%m')})" if alvo.date() != datetime.now().date() else ""
        return f"Lembrete [{prioridade}] criado para {hora}{sufixo}{dia_aviso}{aviso}."

    if resultado["status"] == "duplicado":
        return f"Já existe um lembrete para {hora}."

    return "Não consegui criar o lembrete. Tente novamente."


def _fluxo_cancelar_lembrete() -> str:
    ativos = listar_lembretes()

    if not ativos:
        return "Nenhum lembrete ativo no momento."

    print("\n  Lembretes ativos:")
    for i, l in enumerate(ativos, start=1):
        hora = l["hora"][11:16]
        dia  = l["hora"][:10]
        print(f"  {i}. [{l['prioridade']}] {hora} ({dia}) — {l['mensagem'][:50]}")
    print("  0. Cancelar operação\n")

    try:
        escolha = input("  Qual deseja cancelar? (número): ").strip()
    except (EOFError, KeyboardInterrupt):
        return "Operação cancelada."

    if escolha == "0" or not escolha:
        return "Operação cancelada."

    if not escolha.isdigit() or not (1 <= int(escolha) <= len(ativos)):
        return "Número inválido. Operação cancelada."

    alvo    = ativos[int(escolha) - 1]
    horario = alvo["hora"][11:16]
    dia_str = datetime.fromisoformat(alvo["hora"]).strftime("%d/%m/%Y")
    resultado = cancelar_lembrete(f"{horario} {dia_str}")

    if resultado["status"] == "cancelado":
        return f"Lembrete das {horario} cancelado."
    return "Não foi possível cancelar. Tente novamente."


# ---------------------------------------------------------------------------
# Cancelamento interativo de alarme
# ---------------------------------------------------------------------------

_RE_CANCELAR_ALARME = re.compile(
    r"\b(cancela(r)?|remove(r)?|apaga(r)?|deleta(r)?|exclui(r)?)\s+(o\s+)?alarme\b",
    re.IGNORECASE,
)


def _fluxo_cancelar_alarme() -> str:
    ativos = listar_alarmes()

    if not ativos:
        return "Nenhum alarme ativo no momento."

    print("\n  Alarmes ativos:")
    for i, a in enumerate(ativos, start=1):
        hora = a["horario"][11:16]
        dia  = a["horario"][:10]
        print(f"  {i}. {hora} ({dia}) — {a['mensagem'][:50]}")
    print("  0. Cancelar operação\n")

    try:
        escolha = input("  Qual deseja cancelar? (número): ").strip()
    except (EOFError, KeyboardInterrupt):
        return "Operação cancelada."

    if escolha == "0" or not escolha:
        return "Operação cancelada."

    if not escolha.isdigit() or not (1 <= int(escolha) <= len(ativos)):
        return "Número inválido. Operação cancelada."

    alvo    = ativos[int(escolha) - 1]
    horario = alvo["horario"][11:16]
    dia_str = datetime.fromisoformat(alvo["horario"]).strftime("%d/%m/%Y")
    resultado = cancelar_alarme(f"{horario} {dia_str}")

    if resultado["status"] == "cancelado":
        return f"Alarme das {horario} cancelado."
    return "Não foi possível cancelar. Tente novamente."


# ---------------------------------------------------------------------------
# Detecção de cronômetro
# ---------------------------------------------------------------------------

_RE_CRONOMETRO_INICIAR = re.compile(
    r"\b(iniciar|inicia|começa|comeca|start|liga)\s+cron[oô]metro\b",
    re.IGNORECASE,
)
_RE_CRONOMETRO_PARAR = re.compile(
    r"\b(parar|para|stop|pausa)\s+cron[oô]metro\b",
    re.IGNORECASE,
)
_RE_CRONOMETRO_TEMPO = re.compile(
    r"\b(quanto tempo passou|tempo decorrido|ver cron[oô]metro)\b",
    re.IGNORECASE,
)
_RE_CRONOMETRO_ZERAR = re.compile(
    r"\b(zerar|zera|resetar|reset)\s+cron[oô]metro\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Detecção de timer
# ---------------------------------------------------------------------------

_RE_TIMER_INICIAR = re.compile(
    r"\b(coloca|cria|inicia|iniciar|set|bota|põe)\s+(?:um\s+)?timer\b"
    r"|\btimer\s+de\b"
    r"|\bavisa\s+(daqui\s+a|em)\b"
    r"|\bme\s+avisa\s+(daqui\s+a|em)\b",
    re.IGNORECASE,
)
_RE_TIMER_CANCELAR = re.compile(
    r"\b(cancela(r)?|para(r)?|stop)\s+(o\s+)?timer\b",
    re.IGNORECASE,
)
_RE_TIMER_RESTANTE = re.compile(
    r"\b(quanto\s+tempo\s+(falta|resta)|ver\s+timer|tempo\s+do\s+timer)\b",
    re.IGNORECASE,
)

_RE_TEMPO_TIMER = re.compile(
    r"(\d+)\s*(hora[s]?|h|minuto[s]?|min|segundo[s]?|seg|s)\b",
    re.IGNORECASE,
)


def _extrair_segundos(texto: str) -> int | None:
    total = 0
    encontrou = False
    for m in _RE_TEMPO_TIMER.finditer(texto):
        valor = int(m.group(1))
        unidade = m.group(2).lower()
        if unidade in ("hora", "horas", "h"):
            total += valor * 3600
        elif unidade in ("minuto", "minutos", "min"):
            total += valor * 60
        elif unidade in ("segundo", "segundos", "seg", "s"):
            total += valor
        encontrou = True
    return total if encontrou else None


def _tentar_iniciar_timer(texto: str) -> str | None:
    if not _RE_TIMER_INICIAR.search(texto):
        return None

    segundos = _extrair_segundos(texto)
    if not segundos:
        return "Entendi que você quer um timer, mas não identifiquei o tempo. Tente: 'timer de 10 minutos'."

    return iniciar_timer(segundos)


# ---------------------------------------------------------------------------
# Processamento de input
# ---------------------------------------------------------------------------

def _processar(texto: str, respondente: str) -> str:
    resultado   = classificar(texto)
    intencao_e  = _INTENCAO_MAP.get(resultado.intencao.value, Intencao.DESCONHECIDA)
    entrada     = Entrada(texto=texto, intencao=intencao_e)

    nucleo = _lyra if respondente == "lyra" else _atlas
    resposta = nucleo.processar(entrada)
    return resposta.texto, resultado.intencao.value, respondente


# ---------------------------------------------------------------------------
# Fluxo de autenticação
# ---------------------------------------------------------------------------

def _fluxo_autenticacao() -> tuple[str, dict]:
    print("\n=== Atlas Voice V1 ===")
    print("  1. Login")
    print("  2. Criar conta")
    opcao = input("  Opção: ").strip()

    nome  = input("  Usuário: ").strip()
    senha = input("  Senha: ").strip()

    if opcao == "2":
        r = _cadastrar(nome, senha)
        if r["status"] == "existe":
            print("  Usuário já existe. Faça login.")
            return _fluxo_autenticacao()
        print("  Conta criada. Bem-vindo ao Atlas Voice.")
        return nome, r["perfil"]

    r = _login(nome, senha)
    if r["status"] == "nao_encontrado":
        print("  Usuário não encontrado.")
        return _fluxo_autenticacao()
    if r["status"] == "senha_errada":
        print("  Senha incorreta.")
        return _fluxo_autenticacao()

    return nome, r["perfil"]


# ---------------------------------------------------------------------------
# Monitor em segundo plano
# ---------------------------------------------------------------------------

_encerrar_monitor = threading.Event()


def _monitor_loop() -> None:
    while not _encerrar_monitor.wait(timeout=30):
        try:
            alarmes   = verificar_alarmes()
            lembretes = verificar_lembretes()
            linhas = []
            for a in alarmes:
                linhas.append(f"\n  [ALARME] {a['mensagem']} ({a['horario'][11:16]})")
            for l in lembretes:
                linhas.append(f"\n  [LEMBRETE/{l['prioridade'].upper()}] {l['mensagem']} ({l['hora'][11:16]})")
            if linhas:
                print("".join(linhas), flush=True)
        except Exception as e:
            log_erro("monitor_background", e)


def _iniciar_monitor() -> threading.Thread:
    t = threading.Thread(target=_monitor_loop, daemon=True)
    t.start()
    return t


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

def main() -> None:
    ensure_dirs()

    nome, perfil = _fluxo_autenticacao()

    inicio_sessao = datetime.now().isoformat(timespec="seconds")
    salvar_sessao(inicio=inicio_sessao)

    respondente = perfil.get("respondente_preferido", "atlas")

    print(f"\n  {_saudacao_inicial(nome, perfil)}")
    print(f"  Respondente ativo: {respondente.upper()}")
    print("  (Digite 'sair' para encerrar, 'configurar' para o menu)\n")

    _checar_passivo()
    _iniciar_monitor()

    while True:
        try:
            texto = input(f"[{respondente.upper()}] Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            texto = "sair"

        if not texto:
            continue
        # Diagnóstico do sistema
        if texto.lower() in ("saude", "saúde", "status do sistema"):
            print(f"\n{relatorio_saude()}\n")
            continue
        # Encerramento
        if texto.lower() in ("sair", "encerrar"):
            _encerrar_monitor.set()
            salvar_sessao(inicio=inicio_sessao, fim=datetime.now().isoformat(timespec="seconds"))
            limpar_contexto()
            print(f"\n  Sessão encerrada. Até logo, {nome}.")
            sys.exit(0)

        # Troca de respondente
        if texto.lower() in ("falar com lyra", "mudar para lyra"):
            respondente = "lyra"
            _salvar_preferencia(nome, "respondente_preferido", respondente)
            print("  Lyra ativa.\n")
            continue

        if texto.lower() in ("falar com atlas", "mudar para atlas"):
            respondente = "atlas"
            _salvar_preferencia(nome, "respondente_preferido", respondente)
            print("  Atlas ativo.\n")
            continue

        # Menu de configuração
        if texto.lower() == "configurar":
            respondente = _menu_configuracao(nome, respondente)
            print()
            continue

        # Verificação passiva a cada ciclo
        _checar_passivo()

        # Cancelamento de lembrete
        if _RE_CANCELAR_LEMBRETE.search(texto):
            resposta_cancel = _fluxo_cancelar_lembrete()
            print(f"  ATLAS: {resposta_cancel}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_cancel, intencao="comando", respondente="atlas")
            continue

        # Lembrete via fala natural
        confirmacao_lembrete = _tentar_criar_lembrete(texto)
        if confirmacao_lembrete:
            print(f"  ATLAS: {confirmacao_lembrete}\n")
            registrar_interacao(texto_usuario=texto, resposta=confirmacao_lembrete, intencao="lembrete", respondente="atlas")
            continue

        # Cancelamento de alarme
        if _RE_CANCELAR_ALARME.search(texto):
            resposta_cancel = _fluxo_cancelar_alarme()
            print(f"  ATLAS: {resposta_cancel}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_cancel, intencao="comando", respondente="atlas")
            continue

        # Alarme via fala natural
        confirmacao_alarme = _tentar_criar_alarme(texto)
        if confirmacao_alarme:
            print(f"  ATLAS: {confirmacao_alarme}\n")
            registrar_interacao(texto_usuario=texto, resposta=confirmacao_alarme, intencao="comando", respondente="atlas")
            continue

        # Cronômetro
        if _RE_CRONOMETRO_INICIAR.search(texto):
            resposta_cron = iniciar_cronometro()
            print(f"  ATLAS: {resposta_cron}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_cron, intencao="comando", respondente="atlas")
            continue

        if _RE_CRONOMETRO_PARAR.search(texto):
            resposta_cron = parar_cronometro()
            print(f"  ATLAS: {resposta_cron}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_cron, intencao="comando", respondente="atlas")
            continue

        if _RE_CRONOMETRO_TEMPO.search(texto):
            resposta_cron = tempo_passado()
            print(f"  ATLAS: {resposta_cron}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_cron, intencao="comando", respondente="atlas")
            continue

        if _RE_CRONOMETRO_ZERAR.search(texto):
            resposta_cron = zerar_cronometro()
            print(f"  ATLAS: {resposta_cron}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_cron, intencao="comando", respondente="atlas")
            continue

        # Timer
        if _RE_TIMER_CANCELAR.search(texto):
            resposta_timer = cancelar_timer()
            print(f"  ATLAS: {resposta_timer}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_timer, intencao="comando", respondente="atlas")
            continue

        if _RE_TIMER_RESTANTE.search(texto):
            resposta_timer = tempo_restante_timer()
            print(f"  ATLAS: {resposta_timer}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_timer, intencao="comando", respondente="atlas")
            continue

        resposta_timer = _tentar_iniciar_timer(texto)
        if resposta_timer:
            print(f"  ATLAS: {resposta_timer}\n")
            registrar_interacao(texto_usuario=texto, resposta=resposta_timer, intencao="comando", respondente="atlas")
            continue

        # Processamento geral
        adicionar_mensagem("usuario", texto)
        resposta_texto, intencao, resp_usado = _processar(texto, respondente)
        adicionar_mensagem(resp_usado, resposta_texto)
        print(f"  {resp_usado.upper()}: {resposta_texto}\n")

        registrar_interacao(
            texto_usuario=texto,
            resposta=resposta_texto,
            intencao=intencao,
            respondente=resp_usado,
        )


if __name__ == "__main__":
    main()
