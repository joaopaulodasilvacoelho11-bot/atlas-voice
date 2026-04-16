import json
import re
import sys
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
from funcionalidades.lembretes import verificar_lembretes

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
    """Retorna mensagem de confirmação se detectou e criou alarme, None caso contrário."""
    if not _RE_ALARME.search(texto):
        return None

    tempo = interpretar_tempo(texto)
    hora  = tempo.get("hora")

    if not hora:
        return "Entendi que você quer um alarme, mas não identifiquei o horário. Tente: 'me acorda às 7h'."

    # Monta string de horário para criar_alarme: HH:MM ou HH:MM DD/MM/YYYY
    dia = tempo.get("dia")
    if dia:
        try:
            dt  = datetime.fromisoformat(dia)
            horario_str = f"{hora} {dt.strftime('%d/%m/%Y')}"
        except ValueError:
            horario_str = hora
    else:
        horario_str = hora

    mensagem = texto.strip()
    resultado = criar_alarme(horario_str, mensagem)

    if resultado["status"] == "criado":
        periodo = tempo.get("periodo") or ""
        aviso   = " (horário estimado)" if tempo.get("ambiguidade") else ""
        sufixo  = f" da {periodo}" if periodo else ""
        return f"Alarme criado para {hora}{sufixo}{aviso}."

    if resultado["status"] == "duplicado":
        return f"Já existe um alarme para {hora}."

    return "Não consegui criar o alarme. Tente novamente."


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

    while True:
        try:
            texto = input(f"[{respondente.upper()}] Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            texto = "sair"

        if not texto:
            continue

        # Encerramento
        if texto.lower() in ("sair", "encerrar"):
            salvar_sessao(inicio=inicio_sessao, fim=datetime.now().isoformat(timespec="seconds"))
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

        # Cancelamento de alarme
        if _RE_CANCELAR_ALARME.search(texto):
            resposta_cancel = _fluxo_cancelar_alarme()
            print(f"  ATLAS: {resposta_cancel}\n")
            registrar_interacao(
                texto_usuario=texto,
                resposta=resposta_cancel,
                intencao="comando",
                respondente="atlas",
            )
            continue

        # Alarme via fala natural
        confirmacao_alarme = _tentar_criar_alarme(texto)
        if confirmacao_alarme:
            print(f"  ATLAS: {confirmacao_alarme}\n")
            registrar_interacao(
                texto_usuario=texto,
                resposta=confirmacao_alarme,
                intencao="comando",
                respondente="atlas",
            )
            continue

        # Processamento
        resposta_texto, intencao, resp_usado = _processar(texto, respondente)
        print(f"  {resp_usado.upper()}: {resposta_texto}\n")

        registrar_interacao(
            texto_usuario=texto,
            resposta=resposta_texto,
            intencao=intencao,
            respondente=resp_usado,
        )


if __name__ == "__main__":
    main()
