# Preferências de edição

Aprendidas com os pedidos de ajuste e correção. A skill lê só o que vale para o vídeo atual
(`python scripts/preferencias.py mostrar --estilo <id> --cliente <nome>`) e grava regra nova com
`python scripts/preferencias.py registrar "<regra>" --tipo <seção>`.

- Uma regra por linha, curta e acionável ("legenda nunca estática", e não "não gostei da legenda").
- As marcas `[estilo:id]` e `[cliente:nome]` limitam onde a regra vale. Sem marca, ela vale sempre.
- Quando duas regras se contradizem, vale a mais nova. A antiga é apagada na próxima consolidação, feita quando passar de 60
  linhas.

## Gosto (fazer)

## Evitar

## Processo (como trabalhar comigo)

## Áudio e voz

## Estilos

## Ambiente
