"""Pasta de DADOS do usuário: preferências aprendidas, estilos próprios, músicas já usadas, ambiente da máquina.

Fica FORA da skill (atualizar ou reinstalar a skill nunca apaga) e nunca vai para o repositório nem para quem recebe a skill.
Padrão: ~/.claude/edicao-motion-triwer/  (trocar com a variável EDICAO_DADOS)

    preferencias.md      regras aprendidas com os pedidos de ajuste (preferencias.py registrar/mostrar)
    ambiente.json        caminhos desta máquina: cache, venv, temp, porta, TTS local... (preferencias.py iniciar cria)
    estilos/<id>.md      estilos próprios (mesmo formato de estilos/_modelo.md); mesmo id substitui o cartão da skill
    referencias.md       onde estão os vídeos de referência de cada estilo (vídeos de terceiros não vão para a skill)
    termos_pessoais.txt  nomes/marcas que não podem aparecer na skill compartilhada (checar_pessoal.py)
    musicas_usadas.json  músicas já entregues por cliente (registro.py)
Só biblioteca padrão aqui: é importado antes do venv.
"""
import json
import os
from pathlib import Path

DADOS = Path(os.environ.get("EDICAO_DADOS") or Path.home() / ".claude" / "edicao-motion-triwer")


def ambiente() -> dict:
    p = DADOS / "ambiente.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"aviso: {p} inválido, usando padrões")
    return {}
