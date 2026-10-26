// Texto que acompanha a fala: palavras no tempo do áudio, máquina de escrever, caneta, marca-texto, contador, pílula.
import React from "react";
import { Easing, interpolate, random, spring, useCurrentFrame, useVideoConfig } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const normalizar = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9%]/g, "");

/** Palavra com o quadro LOCAL em que é falada (use palavrasDe() em fala.ts para tirar do words.json). */
export type Palavra = { texto: string; quadro: number };
type Entrada = "desfoque" | "subir" | "mola" | "corte";

const anim = (tipo: Entrada, d: number, fps: number): React.CSSProperties => {
  if (d < 0) return { opacity: 0 };
  if (tipo === "corte") return {};
  if (tipo === "desfoque") {
    const p = interpolate(d, [0, 8], [0, 1], { ...clamp, easing: Easing.bezier(0.22, 1, 0.36, 1) });
    return { opacity: p, filter: p < 0.98 ? `blur(${(1 - p) * 12}px)` : undefined };
  }
  if (tipo === "subir") {
    const p = interpolate(d, [0, 7], [0, 1], { ...clamp, easing: Easing.bezier(0.22, 1, 0.36, 1) });
    return { opacity: p, transform: `translateY(${(1 - p) * 0.45}em)` };
  }
  const s = spring({ frame: d, fps, config: { damping: 11, stiffness: 200, mass: 0.5 } });
  return { opacity: Math.min(1, d / 2), transform: `scale(${0.55 + 0.45 * s})`, display: "inline-block" };
};

/** Palavras entrando no tempo da fala.
 *  modo "acumula": a frase se monta (espaço reservado, layout não pula); "uma": só a palavra atual (estilo palavra-no-papel);
 *  "blocos": legenda corrida em blocos de `porBloco` palavras (ou até pontuação forte).
 *  destaque: { palavraNormalizada: estilo } para a palavra-chave (cor, fonte, escala). antecipa: quadros antes da fala (0-4). */
export const PalavrasNaFala: React.FC<{
  palavras: Palavra[];
  modo?: "acumula" | "uma" | "blocos";
  entrada?: Entrada;
  porBloco?: number;
  antecipa?: number;
  destaque?: Record<string, React.CSSProperties>;
  style?: React.CSSProperties;
  estiloPalavra?: React.CSSProperties;
}> = ({ palavras, modo = "acumula", entrada = "desfoque", porBloco = 3, antecipa = 2, destaque = {}, style, estiloPalavra }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ativo = palavras.filter((p) => p.quadro - antecipa <= f).length - 1;
  let visiveis = palavras.map((p, i) => ({ ...p, i }));
  if (modo === "uma") visiveis = ativo >= 0 ? [visiveis[ativo]] : [];
  if (modo === "blocos") {
    const blocos: (typeof visiveis)[] = [];
    let atual: typeof visiveis = [];
    for (const p of visiveis) {
      atual.push(p);
      if (atual.length >= porBloco || /[.!?…:]$/.test(p.texto)) {
        blocos.push(atual);
        atual = [];
      }
    }
    if (atual.length) blocos.push(atual);
    visiveis = ativo >= 0 ? blocos.find((b) => b.some((p) => p.i === ativo)) ?? [] : [];
  }
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", alignItems: "baseline", columnGap: "0.28em", ...style }}>
      {visiveis.map((p) => (
        <span
          key={p.i}
          style={{
            display: "inline-block",
            ...estiloPalavra,
            ...(destaque[normalizar(p.texto)] ?? {}),
            ...anim(entrada, f - (p.quadro - antecipa), fps),
          }}
        >
          {p.texto}
        </span>
      ))}
    </div>
  );
};

/** Máquina de escrever com cursor. Velocidade por `cps` (caracteres/s) ou terminando em `ate` (quadro local).
 *  O resto do texto fica reservado (invisível) para o layout não pular. */
export const Escrever: React.FC<{
  texto: string;
  inicio?: number;
  ate?: number;
  cps?: number;
  cursor?: "barra" | "bloco" | false;
  corCursor?: string;
  style?: React.CSSProperties;
}> = ({ texto, inicio = 0, ate, cps = 18, cursor = "barra", corCursor, style }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n =
    ate !== undefined
      ? Math.round(interpolate(f, [inicio, Math.max(inicio + 1, ate)], [0, texto.length], clamp))
      : Math.max(0, Math.min(texto.length, Math.floor(((f - inicio) / fps) * cps)));
  const pisca = n < texto.length || Math.floor(f / Math.round(fps * 0.5)) % 2 === 0;
  return (
    <span style={style}>
      {texto.slice(0, n)}
      {cursor && f >= inicio && (
        <span
          style={{
            display: "inline-block",
            width: cursor === "bloco" ? "0.6em" : "0.07em",
            height: "1.05em",
            marginLeft: "0.04em",
            verticalAlign: "-0.15em",
            background: corCursor ?? "currentColor",
            opacity: pisca ? 1 : 0,
          }}
        />
      )}
      <span style={{ opacity: 0 }}>{texto.slice(n)}</span>
    </span>
  );
};

/** Traço de caneta desenhado à mão (círculo irregular, sublinhado, seta, risco, x), dentro de uma caixa w×h. */
export const Caneta: React.FC<{
  forma: "circulo" | "sublinhado" | "seta" | "risco" | "x";
  w: number;
  h: number;
  inicio?: number;
  dur?: number;
  cor?: string;
  espessura?: number;
  semente?: string;
  style?: React.CSSProperties;
}> = ({ forma, w, h, inicio = 0, dur = 12, cor = "#e3262f", espessura = 7, semente = "c", style }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [inicio, inicio + dur], [0, 1], { ...clamp, easing: Easing.bezier(0.45, 0, 0.2, 1) });
  const fase = random(semente) * Math.PI * 2;
  const e = espessura;
  let d = "";
  let ponta = "";
  if (forma === "circulo") {
    const N = 72;
    const a0 = -Math.PI * 0.6 + random(semente + "a") * 0.5;
    const pts: string[] = [];
    for (let i = 0; i <= N; i++) {
      const t = i / N;
      const a = a0 + Math.PI * 2 * 1.1 * t;
      const rr = 1 + 0.045 * Math.sin(t * Math.PI * 3 + fase) + 0.05 * t;
      pts.push(`${(w / 2 + Math.cos(a) * (w / 2 - e) * rr).toFixed(1)} ${(h / 2 + Math.sin(a) * (h / 2 - e) * rr).toFixed(1)}`);
    }
    d = "M " + pts.join(" L ");
  } else if (forma === "sublinhado") {
    d = `M ${e} ${h * 0.6} Q ${w * 0.5} ${h * (0.3 + 0.2 * random(semente + "s"))} ${w - e} ${h * 0.48}`;
  } else if (forma === "risco") {
    d = `M ${-e} ${h * 0.58} Q ${w * 0.5} ${h * 0.46} ${w + e} ${h * 0.44}`;
  } else if (forma === "x") {
    d = `M ${e} ${e} L ${w - e} ${h - e} M ${w - e} ${e} L ${e} ${h - e}`;
  } else {
    // seta curva de baixo-esquerda para cima-direita (girar/espelhar pelo style)
    const [x0, y0, cx, cy, x1, y1] = [e, h - e, w * 0.08, h * 0.15, w - e * 2, e * 2];
    d = `M ${x0} ${y0} Q ${cx} ${cy} ${x1} ${y1}`;
    const ang = Math.atan2(y1 - cy, x1 - cx);
    const L = Math.min(w, h) * 0.22;
    const pt = (da: number) => `${x1 - L * Math.cos(ang + da)} ${y1 - L * Math.sin(ang + da)}`;
    ponta = `M ${pt(0.5)} L ${x1} ${y1} L ${pt(-0.5)}`;
  }
  return (
    <svg width={w} height={h} style={{ overflow: "visible", ...style }}>
      <path d={d} fill="none" stroke={cor} strokeWidth={e} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
      {ponta && (
        <path d={ponta} fill="none" stroke={cor} strokeWidth={e} strokeLinecap="round" strokeLinejoin="round" opacity={interpolate(p, [0.85, 1], [0, 1], clamp)} />
      )}
    </svg>
  );
};

/** Marca-texto passando por trás do texto, da esquerda para a direita. */
export const MarcaTexto: React.FC<{
  inicio?: number;
  dur?: number;
  cor?: string;
  altura?: string;
  children: React.ReactNode;
}> = ({ inicio = 0, dur = 9, cor = "rgba(255,226,0,0.85)", altura = "62%", children }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [inicio, inicio + dur], [0, 1], { ...clamp, easing: Easing.bezier(0.33, 0, 0.2, 1) });
  return (
    <span style={{ position: "relative", display: "inline-block" }}>
      <span
        style={{
          position: "absolute",
          left: "-0.1em",
          right: "-0.1em",
          bottom: "0.02em",
          height: altura,
          background: cor,
          transformOrigin: "left center",
          transform: `scaleX(${p}) skewX(-8deg) rotate(-0.8deg)`,
          borderRadius: "0.12em 0.3em 0.18em 0.25em",
          mixBlendMode: "multiply",
        }}
      />
      <span style={{ position: "relative" }}>{children}</span>
    </span>
  );
};

/** Número contando (pt-BR, algarismos de largura fixa). */
export const Contador: React.FC<{
  de?: number;
  ate: number;
  inicio?: number;
  dur?: number;
  casas?: number;
  prefixo?: string;
  sufixo?: string;
  style?: React.CSSProperties;
}> = ({ de = 0, ate, inicio = 0, dur = 24, casas = 0, prefixo = "", sufixo = "", style }) => {
  const f = useCurrentFrame();
  const v = interpolate(f, [inicio, inicio + dur], [de, ate], { ...clamp, easing: Easing.bezier(0.16, 1, 0.3, 1) });
  const txt = v.toLocaleString("pt-BR", { minimumFractionDigits: casas, maximumFractionDigits: casas });
  return <span style={{ fontVariantNumeric: "tabular-nums", ...style }}>{prefixo + txt + sufixo}</span>;
};

/** Pílula/rótulo de interface (Wi-Fi, Indicações...) entrando com mola; brilho opcional. */
export const Pilula: React.FC<{
  children: React.ReactNode;
  cor?: string;
  corTexto?: string;
  inicio?: number;
  brilho?: boolean;
  style?: React.CSSProperties;
}> = ({ children, cor = "#2b8fd6", corTexto = "#fff", inicio = 0, brilho = false, style }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (f < inicio) return null;
  const s = spring({ frame: f - inicio, fps, config: { damping: 12, stiffness: 220, mass: 0.5 } });
  return (
    <span
      style={{
        display: "inline-block",
        background: cor,
        color: corTexto,
        padding: "0.28em 0.8em",
        borderRadius: "0.35em",
        fontWeight: 600,
        transform: `scale(${0.6 + 0.4 * s}) translateY(${(1 - s) * 18}px)`,
        opacity: Math.min(1, (f - inicio) / 3),
        boxShadow: brilho ? `0 0 24px ${cor}aa, 0 0 6px ${cor}` : "0 6px 16px rgba(0,0,0,0.25)",
        ...style,
      }}
    >
      {children}
    </span>
  );
};
