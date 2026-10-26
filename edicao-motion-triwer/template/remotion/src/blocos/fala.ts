// Palavras da fala (public/words.json, tempos globais em segundos) convertidas para quadros LOCAIS de uma cena.
import wordsJson from "../../public/words.json";
import type { Palavra } from "./Escrita";

type Bruta = { text: string; start: number };
const PALAVRAS = wordsJson as Bruta[];

/** Palavras faladas entre `de` e `ate` (segundos globais). `origem` = segundo global em que a cena começa (quadro 0 dela). */
export const palavrasDe = (de: number, ate: number, origem = de, fps = 30): Palavra[] =>
  PALAVRAS.filter((w) => w.start >= de - 0.01 && w.start < ate).map((w) => ({
    texto: w.text.trim(),
    quadro: Math.round((w.start - origem) * fps),
  }));

/** Palavras escritas à mão com tempos em segundos locais (para testar uma cena antes de existir narração). */
export const palavrasManuais = (lista: [string, number][], fps = 30): Palavra[] =>
  lista.map(([texto, s]) => ({ texto, quadro: Math.round(s * fps) }));
