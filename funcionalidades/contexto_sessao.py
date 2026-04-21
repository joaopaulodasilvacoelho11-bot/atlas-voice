from typing import List, Dict

_contexto: List[Dict[str, str]] = []


def adicionar_mensagem(papel: str, texto: str) -> None:
    _contexto.append({"papel": papel, "texto": texto})


def obter_contexto_formatado() -> str:
    if not _contexto:
        return ""
    linhas = [f"{m['papel'].upper()}: {m['texto']}" for m in _contexto]
    return "\n".join(linhas)


def limpar_contexto() -> None:
    _contexto.clear()


def contexto_tem_mencao(palavra: str) -> bool:
    palavra_lower = palavra.lower()
    return any(palavra_lower in m["texto"].lower() for m in _contexto)
