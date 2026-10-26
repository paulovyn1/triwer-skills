# Criar o kit de um cliente ou marca nova (inclusive a do próprio usuário)

O kit é uma skill de projeto pequena, `edicao-<cliente>`, em `<workspace>/.claude/skills/edicao-<cliente>/`. Ela **não repete o
processo** (que é desta skill) e guarda só o que é do cliente. Ler o kit no início de todo vídeo dele.

## Perguntar ao usuário (uma rodada, no máximo 6 perguntas; o resto vem do site ou da página do cliente)
1. **Identidade:** página, site ou Instagram de referência, para extrair cores, fontes, estilo visual e fotos. Fonte de licença
   paga não entra: usar a equivalente do Google Fonts.
2. **Contexto:** o que o cliente vende, para quem, qual a promessa, o vocabulário e como a pessoa fala (tu/você, formal/informal).
3. **Compliance:** o que NÃO pode aparecer (empresa atual, concorrentes, promessa de resultado, nomes) e quais logos são autorizados.
4. **Provas reais disponíveis:** fotos, logos, números, depoimentos, páginas do produto.
5. **Estilo e gosto:** qual estilo do catálogo (`estilos/INDICE.md`) combina, 1 ou 2 vídeos de referência, e a ousadia de
   legenda e efeito (calmo, médio, agressivo).
6. **Destino:** Reels orgânico, anúncio ou VSL curta, e o CTA padrão.

## Estrutura do kit
```
edicao-<cliente>/
  SKILL.md        description com gatilhos ("vídeo do <cliente>") e o resumo do kit; aponta para edicao-motion-triwer
  marca.md        cores (hex), fontes (nomes do Google Fonts), regras de foto e ilustração, bloco C/F pronto para theme.tsx
  contexto.md     o que vende, público, vocabulário, compliance, CTA, logos e fotos autorizados
  padroes.md      presets: estilo preferido, legenda, mapa emocional que funcionou, efeitos recorrentes, estilo de painel
  assets/         fotos, logos (SVG/PNG), tema pronto (theme.tsx)
  paineis-<video>/  painéis .tsx de vídeos anteriores (tempos por useAt; POUSOS.md se tiver tempos fixos)
```
- O `SKILL.md` do kit tem no máximo 60 linhas, só ponteiros (quem é, quando ler cada arquivo), sem copiar o processo.
- Preferências de gosto do cliente vão para `preferencias.py registrar ... --cliente "<nome>"`, e não para o kit, para valerem
  também nos estilos novos.
- As músicas já entregues ficam registradas sozinhas (`registro.py`).

## Depois do 1º vídeo
Atualizar `contexto.md` e `padroes.md` com o que foi aprovado ou rejeitado e copiar os painéis novos para o kit. Painel que
servir a dois clientes é promovido para `biblioteca/paineis/` ou vira bloco em `template/remotion/src/blocos`.
