// Containers dos painéis: entrada/saída, emenda amarela, troca painel→painel e fade das telas cheias.
import React from "react";
import { AbsoluteFill, Freeze, interpolate, Sequence, useCurrentFrame } from "remotion";
import { PANELS, PanelDef } from "../timeline";
import { C, easeInOut, easeOut, PANEL_H } from "../theme";
import { PanelStartCtx } from "../words";

const IN = 9;
const OUT = 7;
const TAIL = 8; // quem sai debaixo de uma tela cheia segura o último frame enquanto ela aparece/some

const prev = (i: number) => PANELS[i - 1];
const next = (i: number) => PANELS[i + 1];
const touches = (a?: PanelDef, b?: PanelDef) => !!a && !!b && Math.abs(b.from - a.to) <= 2;

/** renderiza o componente congelando no último frame depois do fim */
const Held: React.FC<{ C: React.FC; dur: number; from: number }> = ({ C: Comp, dur, from }) => {
  const f = useCurrentFrame();
  return (
    <PanelStartCtx.Provider value={from}>
      {f >= dur ? (
        <Freeze frame={dur - 1}>
          <Comp />
        </Freeze>
      ) : (
        <Comp />
      )}
    </PanelStartCtx.Provider>
  );
};

const TopPanel: React.FC<{ p: PanelDef; i: number }> = ({ p, i }) => {
  const f = useCurrentFrame(); // local
  const dur = p.to - p.from;
  const slideIn = !(touches(prev(i), p) && prev(i)!.kind === "cover");
  const slideOut = !touches(p, next(i));
  const inY = slideIn ? interpolate(f, [0, IN], [-PANEL_H - 40, 0], { easing: easeOut, extrapolateRight: "clamp" }) : 0;
  const outY = slideOut ? interpolate(f, [dur - OUT, dur], [0, -PANEL_H - 40], { easing: easeInOut, extrapolateLeft: "clamp" }) : 0;
  return (
    <AbsoluteFill style={{ height: PANEL_H, transform: `translateY(${inY + outY}px)`, overflow: "visible" }}>
      <AbsoluteFill style={{ overflow: "hidden", boxShadow: "0 26px 50px rgba(0,0,0,0.55)" }}>
        <Held C={p.C} dur={dur} from={p.from} />
      </AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: -3,
          height: 6,
          background: C.yellow,
          boxShadow: "0 0 18px rgba(245,217,10,0.6)",
        }}
      />
    </AbsoluteFill>
  );
};

const CoverPanel: React.FC<{ p: PanelDef }> = ({ p }) => {
  const f = useCurrentFrame();
  const dur = p.to - p.from;
  const op = interpolate(f, [0, 6, dur, dur + TAIL - 1], [0, 1, 1, 0], { extrapolateRight: "clamp" });
  const sc = interpolate(f, [0, 8], [1.06, 1], { easing: easeOut, extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: op, transform: `scale(${sc})` }}>
      <Held C={p.C} dur={dur} from={p.from} />
    </AbsoluteFill>
  );
};

export const Panels: React.FC = () => {
  const tops = PANELS.map((p, i) => ({ p, i })).filter(({ p }) => p.kind === "top");
  const covers = PANELS.filter((p) => p.kind === "cover");
  const overlays = PANELS.filter((p) => p.kind === "overlay");
  return (
    <>
      {tops.map(({ p, i }) => {
        const tail = touches(p, next(i)) && next(i)!.kind === "cover" ? TAIL : 0;
        return (
          <Sequence key={p.id} from={p.from} durationInFrames={p.to - p.from + tail} name={p.id}>
            <TopPanel p={p} i={i} />
          </Sequence>
        );
      })}
      {covers.map((p) => (
        <Sequence key={p.id} from={p.from} durationInFrames={p.to - p.from + TAIL} name={p.id}>
          <CoverPanel p={p} />
        </Sequence>
      ))}
      {overlays.map((p) => (
        <Sequence key={p.id} from={p.from} durationInFrames={p.to - p.from} name={p.id}>
          <PanelStartCtx.Provider value={p.from}>
            <p.C />
          </PanelStartCtx.Provider>
        </Sequence>
      ))}
    </>
  );
};
