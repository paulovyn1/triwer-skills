// Câmera contínua num "mundo" maior que a tela: a base das transições sem corte (mural, mesa, prancheta, papel).
// O mundo é uma <div> de largura×altura em px; a câmera tem poses por quadro e interpola entre elas com ease-in-out por trecho.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

/** f = quadro local; x,y = ponto do mundo que fica no centro da tela; s = zoom; rx/ry/rz em graus; z = profundidade (px). */
export type Pose = { f: number; x?: number; y?: number; s?: number; rx?: number; ry?: number; rz?: number; z?: number };

const CHAVES = ["x", "y", "s", "rx", "ry", "rz", "z"] as const;

/** valor interpolado da câmera no quadro f (útil para sincronizar efeito sonoro/legenda com o movimento) */
export const poseEm = (poses: Pose[], f: number, padrao: Required<Omit<Pose, "f">>, easing = Easing.bezier(0.65, 0, 0.35, 1)) => {
  const ps = poses.length === 1 ? [poses[0], { ...poses[0], f: poses[0].f + 1 }] : poses;
  const fs = ps.map((p) => p.f);
  const out = {} as Required<Omit<Pose, "f">>;
  for (const k of CHAVES) {
    out[k] = interpolate(f, fs, ps.map((p) => (p[k] ?? padrao[k]) as number), {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing,
    });
  }
  return out;
};

/** Câmera. `respira` = deriva lenta mesmo parada (px), `tremor` = câmera na mão (px). Nunca deixar 0/0 numa pose longa. */
export const Camera: React.FC<{
  poses: Pose[];
  largura: number;
  altura: number;
  perspectiva?: number;
  respira?: number;
  tremor?: number;
  fundo?: string;
  /** true (padrão): a câmera nunca mostra fora do mundo (considera zoom e uma folga para a rotação) */
  limitar?: boolean;
  children: React.ReactNode;
}> = ({ poses, largura, altura, perspectiva = 2200, respira = 6, tremor = 0, fundo, limitar = true, children }) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const c = poseEm(poses, f, { x: largura / 2, y: altura / 2, s: 1, rx: 0, ry: 0, rz: 0, z: 0 });
  if (limitar) {
    // meia-largura/altura visível no mundo; a rotação em z pede folga extra (canto da tela gira para fora)
    const giro = Math.abs(Math.sin((c.rz * Math.PI) / 180));
    const hx = (width / 2 + (height / 2) * giro) / c.s + respira + tremor * 2;
    const hy = (height / 2 + (width / 2) * giro) / c.s + respira + tremor * 2;
    c.x = largura <= 2 * hx ? largura / 2 : Math.min(Math.max(c.x, hx), largura - hx);
    c.y = altura <= 2 * hy ? altura / 2 : Math.min(Math.max(c.y, hy), altura - hy);
  }
  const dx = respira * Math.sin(f / 53) + tremor * (Math.sin(f / 3.7) + 0.6 * Math.sin(f / 1.9 + 1.3));
  const dy = respira * 0.7 * Math.sin(f / 67 + 2) + tremor * (Math.sin(f / 4.3 + 0.7) + 0.5 * Math.sin(f / 2.3));
  return (
    <AbsoluteFill style={{ perspective: perspectiva, overflow: "hidden", backgroundColor: fundo }}>
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: largura,
          height: altura,
          transformOrigin: "0 0",
          transformStyle: "preserve-3d",
          transform:
            `translate(${width / 2 + dx}px, ${height / 2 + dy}px) translateZ(${c.z}px) ` +
            `rotateX(${c.rx}deg) rotateY(${c.ry}deg) rotateZ(${c.rz}deg) scale(${c.s}) translate(${-c.x}px, ${-c.y}px)`,
        }}
      >
        {children}
      </div>
    </AbsoluteFill>
  );
};

/** Coloca um elemento numa coordenada do mundo (canto superior esquerdo em x,y), com rotação e profundidade. */
export const NoMundo: React.FC<{
  x: number;
  y: number;
  w?: number;
  h?: number;
  rot?: number;
  z?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ x, y, w, h, rot = 0, z = 0, children, style }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      height: h,
      transform: `translateZ(${z}px) rotate(${rot}deg)`,
      transformStyle: "preserve-3d",
      ...style,
    }}
  >
    {children}
  </div>
);
