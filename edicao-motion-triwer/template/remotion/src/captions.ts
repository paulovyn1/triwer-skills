// Roteiro da legenda: cada cue consome palavras do words.json na ordem (o resolver confere o texto).
// Marcação por palavra: *serif itálico amarelo  #faixa amarela  ^azul.  " | " quebra de linha.
// Modos:
//  build  — palavra por palavra montando a frase (palavra falada acende em amarelo)
//  slam   — palavra gigante batendo na tela com tremida
//  stack  — editorial: linhas de tamanhos/fontes diferentes
//  behind — texto gigante ATRÁS da pessoa (entre o fundo e o recorte dela)
//  knock  — knockout: tela preta, vídeo aparece por dentro das letras
//  hide   — fala coberta por um painel que já tem o texto dele
import wordsJson from "../public/words.json";
import { FPS } from "./theme";

export type Mode = "build" | "slam" | "stack" | "behind" | "knock" | "hide";
export type Style = "plain" | "serif" | "tape" | "blue";
export type CWord = { text: string; style: Style; line: number; start: number; end: number };
export type Cue = { mode: Mode; words: CWord[]; start: number; end: number; hold?: number; fx?: string };

type RawWord = { text: string; start: number; end: number };
const WORDS = wordsJson as RawWord[];

const SCRIPT: [Mode, string, { hold?: number; fx?: string }?][] = [
  // Cada linha consome as próximas palavras de words.json NA ORDEM (o resolver confere o texto e falha se sair de sincronia).
  // ["slam", "Para | de tentar"],            // gancho: 1ª linha gigante batendo
  // ["build", "assumindo tarefa"],           // palavra por palavra (o padrão, ~65% do vídeo)
  // ["behind", "logística,"],                // texto gigante ATRÁS da pessoa (precisa de matte_rvm.py)
  // ["behind", "invisível.", { fx: "ghost" }], // idem + efeito fantasma (fundo borrado, pessoa translúcida)
  // ["build", "#duas #horas"],               // # = faixa amarela   * = serif itálico amarelo   ^ = azul
  // ["stack", "me escuta | *aqui."],         // blocos editoriais em linhas de tamanhos diferentes
  // ["knock", "teu esforço | morre ali."],   // knockout: tela preta, vídeo P&B dentro das letras (1x no clímax)
  // ["hide", "texto que o painel já mostra"], // a fala é coberta por painel: consome as palavras sem desenhar legenda
];

const norm = (s: string) =>
  s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]/g, "");

const STYLE_OF: Record<string, Style> = { "*": "serif", "#": "tape", "^": "blue" };

const resolve = (): Cue[] => {
  let k = 0;
  const cues: Cue[] = SCRIPT.map(([mode, text, opt]) => {
    let line = 0;
    const words: CWord[] = [];
    for (const tok of text.split(" ")) {
      if (tok === "|") {
        line++;
        continue;
      }
      const style = STYLE_OF[tok[0]] ?? "plain";
      const clean = style === "plain" ? tok : tok.slice(1);
      const w = WORDS[k];
      if (!w || norm(w.text) !== norm(clean)) {
        throw new Error(`Legenda fora de sincronia em "${clean}" (palavra ${k}: "${w?.text}")`);
      }
      words.push({ text: clean, style, line, start: Math.round(w.start * FPS), end: Math.round(w.end * FPS) });
      k++;
    }
    return { mode, words, start: words[0].start, end: words[words.length - 1].end, ...opt };
  });
  if (k !== WORDS.length) throw new Error(`Legenda consumiu ${k} de ${WORDS.length} palavras`);
  // cada cue fica na tela até a próxima começar
  cues.forEach((c, i) => {
    const next = cues[i + 1];
    c.end = next ? next.start : Math.max(c.end + 15, c.end);
  });
  return cues;
};

export const CUES = resolve();
