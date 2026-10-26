// Legenda dinâmica: palavra por palavra (build), slam no gancho e blocos editoriais (stack).
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CUES, CWord, Cue } from "../captions";
import { captionY } from "../layout";
import { C, F, pop } from "../theme";

const SHADOW = "0 4px 0 rgba(0,0,0,0.30), 0 6px 26px rgba(0,0,0,0.55)";

const Word: React.FC<{ w: CWord; f: number; size: number; mode: Cue["mode"]; big?: boolean }> = ({ w, f, size, mode, big }) => {
  const shown = f >= w.start - 1;
  const p = pop(f, w.start - 1, 30, 11, 220);
  const active = f >= w.start && f < Math.max(w.end, w.start + 6);
  const scale = interpolate(p, [0, 1], [big ? 1.9 : 0.55, 1]) * (active && w.style === "plain" && !big ? 1.06 : 1);
  const base: React.CSSProperties = {
    display: "inline-block",
    opacity: shown ? Math.min(1, p * 1.6) : 0,
    transform: `translateY(${interpolate(p, [0, 1], [big ? 0 : 26, 0])}px) scale(${scale})`,
    margin: "0 0.13em",
    whiteSpace: "nowrap",
  };
  const clean = w.text;
  if (w.style === "serif") {
    return (
      <span
        style={{
          ...base,
          fontFamily: F.serif,
          fontStyle: "italic",
          fontWeight: 400,
          fontSize: size * (mode === "stack" ? 2.3 : 1.42),
          lineHeight: 0.85,
          color: C.yellow,
          letterSpacing: "-0.01em",
          textShadow: SHADOW,
        }}
      >
        {clean}
      </span>
    );
  }
  if (w.style === "tape") {
    const wipe = interpolate(f, [w.start - 2, w.start + 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    return (
      <span style={{ ...base, position: "relative", padding: "0.04em 0.18em", margin: "0 0.04em" }}>
        <span
          style={{
            position: "absolute",
            inset: 0,
            background: C.yellow,
            transform: `scaleX(${wipe})`,
            transformOrigin: "left",
            boxShadow: "0 10px 30px -10px rgba(245,217,10,0.6)",
          }}
        />
        <span
          style={{
            position: "relative",
            fontFamily: F.display,
            fontWeight: 900,
            fontSize: size,
            textTransform: "uppercase",
            color: C.black,
            letterSpacing: "-0.02em",
          }}
        >
          {clean}
        </span>
      </span>
    );
  }
  return (
    <span
      style={{
        ...base,
        fontFamily: F.display,
        fontWeight: 900,
        fontSize: big ? size * 3.1 : size,
        lineHeight: big ? 0.9 : 1,
        textTransform: "uppercase",
        letterSpacing: "-0.025em",
        color: w.style === "blue" ? C.blue2 : active && !big ? C.yellow : "#fff",
        textShadow: SHADOW,
      }}
    >
      {clean}
    </span>
  );
};

const CueView: React.FC<{ cue: Cue; f: number }> = ({ cue, f }) => {
  const lines = Array.from(new Set(cue.words.map((w) => w.line)));
  const size = cue.mode === "stack" ? 108 : 84;
  const y = cue.mode === "stack" || cue.mode === "slam" ? Math.min(captionY(f), 1300) : captionY(f);
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: 50,
          right: 50,
          top: y,
          transform: "translateY(-50%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          gap: cue.mode === "stack" ? 0 : 6,
        }}
      >
        {lines.map((ln) => (
          <div key={ln} style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", alignItems: "baseline" }}>
            {cue.words
              .filter((w) => w.line === ln)
              .map((w, i) => (
                <Word key={i} w={w} f={f} size={size} mode={cue.mode} big={cue.mode === "slam" && ln === 0} />
              ))}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const Captions: React.FC = () => {
  const f = useCurrentFrame();
  const cue = CUES.find((c) => f >= c.start - 1 && f < c.end - 1);
  if (!cue || !["build", "slam", "stack"].includes(cue.mode)) return null;
  return <CueView cue={cue} f={f} />;
};
