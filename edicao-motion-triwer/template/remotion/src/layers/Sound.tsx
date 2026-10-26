import React from "react";
import { Audio, staticFile } from "remotion";

// A mixagem inteira (voz + música + efeitos, com automação e ducking) é feita em edit/scripts/mix.py.
// Aqui só toca o resultado, pra prévia no Studio e pro render.
export const MIX = "mix_A.wav";

export const Sound: React.FC = () => <Audio src={staticFile(MIX)} volume={1} />;
