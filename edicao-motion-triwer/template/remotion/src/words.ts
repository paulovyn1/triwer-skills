// Tempo das palavras faladas dentro dos painéis: em vez de números mágicos, `at("dobrar")` devolve o frame LOCAL do painel.
// Uso no painel:  const at = useAt();  const tDobrar = at("dobrar");  const tSegundaVez = at("como", 1);  (offset opcional: at("dobrar", 0, -3))
import React from "react";
import wordsJson from "../public/words.json";
import { FPS } from "./theme";

type RawWord = { text: string; start: number };
const WORDS = wordsJson as RawWord[];
const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]/g, "");

/** início do painel (frame global), preenchido pelo container Panels.tsx */
export const PanelStartCtx = React.createContext(0);

/** frame global em que a n-ésima ocorrência (nth, base 0) da palavra é falada */
export const wordFrame = (word: string, nth = 0): number => {
  const hits = WORDS.filter((w) => norm(w.text) === norm(word));
  if (!hits[nth]) throw new Error(`wordFrame: "${word}" (ocorrência ${nth}) não está em words.json`);
  return Math.round(hits[nth].start * FPS);
};

/** hook: at(palavra, nth?, offset?) = frame LOCAL do painel em que a palavra é falada */
export const useAt = () => {
  const from = React.useContext(PanelStartCtx);
  return (word: string, nth = 0, offset = 0) => wordFrame(word, nth) - from + offset;
};
