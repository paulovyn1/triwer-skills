# Changelog — edicao-motion-triwer

Mais recente no topo. Formato de cada entrada: `## <versão> [CRITICAL] - <data>` (a tag só quando a correção muda o resultado
entregue). O BOOT da skill compara a primeira entrada com o `VERSION` instalado.

## 0.4.0 - 2026-10-26
- Primeira versão pública. Edita vídeo vertical (Reels, anúncio, VSL curta, vídeo narrado) no Claude Code, com Remotion,
  Python e ffmpeg: cortes de silêncio e gagueira, voz tratada, legenda animada no tempo da fala, painéis de motion, trilha
  escolhida pela emoção de cada trecho, efeitos sonoros com revisão numerada e master em −14 LUFS.
- Catálogo de 7 estilos de edição (Fala Dinâmica, Recorte de Jornal, Documentário Colagem, P&B Neon, Mural de Memórias,
  Mesa e Telas, Prancheta Técnica) e como catalogar um estilo novo a partir de um vídeo de referência.
- Aprende as preferências de cada usuário com os pedidos de ajuste, numa pasta fora da skill (`~/.claude/edicao-motion-triwer/`):
  atualizar a skill não apaga nada disso.
- Material real: trecho do YouTube, bancos gratuitos (Internet Archive, Wikimedia Commons, Pexels, Pixabay), prints de página e
  comentários com autor anonimizado, sempre com crédito e licença registrados.
- Vídeo narrado por cenas (`cenas.json`), sem pessoa filmada.
- Efeitos sonoros e músicas do Mixkit baixados na hora do uso (a licença do Mixkit não permite redistribuir os arquivos).
