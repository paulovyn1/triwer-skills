// Reaproveitar painel de outro vídeo com outra fala: remapeia o frame local por trechos lineares.
// map = [[frame_novo, frame_original], ...] em ordem crescente; fora do mapa segue com velocidade 1.
// Uso no painel copiado do kit (1 linha): const frame = warp(useCurrentFrame(), MAP);
// Os pousos originais de cada painel do kit estão em <kit>/paineis-*/POUSOS.md (palavra@frame local); os novos vêm de useAt().
export const warp = (f: number, map: [number, number][]): number => {
  if (f <= map[0][0]) return map[0][1] + (f - map[0][0]);
  for (let i = 1; i < map.length; i++) {
    const [a0, b0] = map[i - 1];
    const [a1, b1] = map[i];
    if (f <= a1) return b0 + ((f - a0) / (a1 - a0)) * (b1 - b0);
  }
  const [aN, bN] = map[map.length - 1];
  return bN + (f - aN);
};
