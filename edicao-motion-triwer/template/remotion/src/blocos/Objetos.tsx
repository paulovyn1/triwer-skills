// Coisas físicas: foto/papel com sombra (polaroid, moldura, fita, alfinete), barbante, rajada de fotos, faixa de cinema.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const fonte = (src: string) => (/^(https?:|data:)/.test(src) ? src : staticFile(src));

/** Foto ou papel físico. moldura: polaroid | borda | nenhuma (recorte PNG: sombra segue o contorno).
 *  entrada (quadro local): cai na mesa (escala 1,12 → 1, sombra alta → baixa, gira 4° até `rot`). */
export const Cartao: React.FC<{
  src?: string;
  w: number;
  h: number;
  moldura?: "polaroid" | "borda" | "nenhuma";
  corMoldura?: string;
  rot?: number;
  preso?: "fita" | "alfinete" | false;
  legenda?: React.ReactNode;
  entrada?: number;
  ajuste?: "cover" | "contain";
  filtro?: string;
  children?: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ src, w, h, moldura = "polaroid", corMoldura, rot = 0, preso = false, legenda, entrada, ajuste = "cover", filtro, children, style }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = entrada === undefined ? 1 : spring({ frame: f - entrada, fps, config: { damping: 14, stiffness: 160, mass: 0.7 } });
  if (entrada !== undefined && f < entrada) return null;
  const alto = 1 - s; // 1 = ainda no ar
  const pad = moldura === "polaroid" ? { p: w * 0.05, b: w * 0.2 } : moldura === "borda" ? { p: w * 0.035, b: w * 0.035 } : { p: 0, b: 0 };
  const sombra = `0 ${6 + alto * 40}px ${14 + alto * 50}px rgba(0,0,0,${0.32 - alto * 0.12}), 0 2px 3px rgba(0,0,0,0.22)`;
  const conteudo = src ? (
    <Img src={fonte(src)} style={{ width: "100%", height: "100%", objectFit: ajuste, display: "block", filter: filtro }} />
  ) : (
    children
  );
  return (
    <div
      style={{
        position: "relative",
        width: w,
        height: h,
        transform: `rotate(${rot + alto * 4}deg) scale(${1 + alto * 0.12})`,
        opacity: entrada === undefined ? 1 : Math.min(1, (f - entrada) / 3),
        ...style,
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          padding: `${pad.p}px ${pad.p}px ${pad.b}px`,
          background: moldura === "polaroid" ? "#f3f1ea" : moldura === "borda" ? corMoldura ?? "linear-gradient(135deg,#c9a24a,#f1d98a 45%,#9c7a2c)" : undefined,
          boxShadow: moldura === "nenhuma" ? undefined : sombra,
          filter: moldura === "nenhuma" ? `drop-shadow(0 ${8 + alto * 34}px ${10 + alto * 30}px rgba(0,0,0,0.35))` : undefined,
          boxSizing: "border-box",
        }}
      >
        <div style={{ width: "100%", height: "100%", overflow: "hidden", boxShadow: moldura === "borda" ? "inset 0 0 0 2px rgba(0,0,0,0.25)" : undefined }}>{conteudo}</div>
        {legenda && (
          <div style={{ position: "absolute", left: pad.p, right: pad.p, bottom: 0, height: pad.b, display: "flex", alignItems: "center", justifyContent: "center" }}>
            {legenda}
          </div>
        )}
      </div>
      {preso === "fita" && (
        <div
          style={{
            position: "absolute",
            top: -h * 0.035,
            left: "50%",
            width: w * 0.36,
            height: Math.max(26, h * 0.07),
            transform: "translateX(-50%) rotate(-3deg)",
            background: "rgba(236,228,206,0.82)",
            boxShadow: "0 1px 3px rgba(0,0,0,0.18)",
          }}
        />
      )}
      {preso === "alfinete" && (
        <div
          style={{
            position: "absolute",
            top: -Math.max(10, w * 0.03),
            left: "50%",
            width: Math.max(26, w * 0.09),
            height: Math.max(26, w * 0.09),
            transform: "translateX(-50%)",
            borderRadius: "50%",
            background: "radial-gradient(circle at 35% 30%, #ff8a8a, #d0131c 55%, #7a0509)",
            boxShadow: "3px 6px 8px rgba(0,0,0,0.4)",
          }}
        />
      )}
    </div>
  );
};

/** Barbante entre pontos (mural de investigação), desenhado de `inicio` em `dur`. Pontos em px do container (mundo). */
export const Barbante: React.FC<{
  pontos: [number, number][];
  inicio?: number;
  dur?: number;
  cor?: string;
  espessura?: number;
  curva?: number;
}> = ({ pontos, inicio = 0, dur = 18, cor = "#c3161c", espessura = 4, curva = 26 }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [inicio, inicio + dur], [0, 1], { ...clamp, easing: Easing.bezier(0.45, 0, 0.25, 1) });
  let d = `M ${pontos[0][0]} ${pontos[0][1]}`;
  for (let i = 1; i < pontos.length; i++) {
    const [a, b] = [pontos[i - 1], pontos[i]];
    d += ` Q ${(a[0] + b[0]) / 2} ${(a[1] + b[1]) / 2 + curva} ${b[0]} ${b[1]}`;
  }
  return (
    <svg style={{ position: "absolute", left: 0, top: 0, width: "100%", height: "100%", overflow: "visible", pointerEvents: "none" }}>
      <path d={d} fill="none" stroke="rgba(0,0,0,0.25)" strokeWidth={espessura} transform="translate(3 6)" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
      <path d={d} fill="none" stroke={cor} strokeWidth={espessura} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
    </svg>
  );
};

/** Rajada: troca de imagem a cada `cada` quadros, com leve zoom em cada uma (memória, volume, passagem de tempo). */
export const Rajada: React.FC<{ imagens: string[]; inicio?: number; cada?: number; ajuste?: "cover" | "contain"; zoom?: number }> = ({
  imagens,
  inicio = 0,
  cada = 4,
  ajuste = "cover",
  zoom = 0.05,
}) => {
  const f = useCurrentFrame() - inicio;
  if (f < 0 || !imagens.length) return null;
  const i = Math.min(imagens.length - 1, Math.floor(f / cada));
  const local = f - i * cada;
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <Img src={fonte(imagens[i])} style={{ width: "100%", height: "100%", objectFit: ajuste, transform: `scale(${1 + zoom * (local / cada)})` }} />
    </AbsoluteFill>
  );
};

/** Faixa de cinema: conteúdo na razão `razao` (16/9) no meio do vertical; as barras pretas entram em `dur` quadros. */
export const Faixa: React.FC<{ razao?: number; inicio?: number; dur?: number; cor?: string; children: React.ReactNode }> = ({
  razao = 16 / 9,
  inicio = 0,
  dur = 10,
  cor = "#000",
  children,
}) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const alvo = width / razao;
  const hh = interpolate(f, [inicio, inicio + dur], [height, alvo], { ...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1) });
  return (
    <AbsoluteFill style={{ backgroundColor: cor, alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "relative", width, height: hh, overflow: "hidden" }}>
        <AbsoluteFill style={{ top: (hh - alvo) / 2, height: alvo }}>{children}</AbsoluteFill>
      </div>
    </AbsoluteFill>
  );
};
