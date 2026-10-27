import { Fragment } from "react";
import { motion } from "motion/react";
import { CTA, ease, hl } from "./ui.jsx";
import { VIDEO_URL } from "../config.js";

// Texto de exemplo. Troque pela headline e subheadline que o aluno aprovou, palavra por palavra.
const HEADLINE = "[Paradoxo ou dor do lead na fala dele] e é exatamente por isso que [consequência que ele já viveu]";
const DESTAQUE = "exatamente por isso";
const SUBHEADLINE = "[Mecanismo simples + prazo]. [Remoção de objeção 1], [remoção de objeção 2] e [remoção de objeção 3].";

// Player ilustrativo da VSL. Quando houver o vídeo, preencher VIDEO_URL em config.js.
function Player() {
  const Tag = VIDEO_URL ? "a" : "div";
  const props = VIDEO_URL ? { href: VIDEO_URL, target: "_blank", rel: "noreferrer", "aria-label": "Assistir ao vídeo" } : {};
  return (
    <Tag className="player" {...props}>
      <div className="player-screen">
        <span className="player-badge">Assista antes de continuar</span>
        <span className="player-play" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="38" height="38"><path d="M8 5v14l11-7z" fill="currentColor" /></svg>
        </span>
        <span className="player-cap">[Título da VSL: a promessa ou a pergunta que prende o lead]</span>
      </div>
      <div className="player-bar" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18"><path d="M8 5v14l11-7z" fill="currentColor" /></svg>
        <span className="player-time">0:00</span>
        <span className="player-track"><i /></span>
        <svg viewBox="0 0 24 24" width="18" height="18"><path d="M4 9v6h4l5 4V5L8 9H4zm12.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4z" fill="currentColor" /></svg>
        <svg viewBox="0 0 24 24" width="18" height="18"><path d="M5 5h5v2H7v3H5V5zm9 0h5v5h-2V7h-3V5zM5 14h2v3h3v2H5v-5zm12 0h2v5h-5v-2h3v-3z" fill="currentColor" /></svg>
      </div>
    </Tag>
  );
}

export default function Hero() {
  const words = HEADLINE.split(" ");
  const marcadas = hl(HEADLINE, DESTAQUE);
  return (
    <header className="hero">
      <div className="wrap hero-in">
        <h1 className="hero-title">
          {words.map((w, i) => (
            <Fragment key={i}>
              <span className="word-mask">
                <motion.span
                  className={marcadas.includes(i) ? "word hl" : "word"}
                  initial={{ y: "110%" }}
                  animate={{ y: "0%" }}
                  transition={{ duration: 0.85, ease, delay: 0.1 + i * 0.045 }}
                >
                  {w}
                </motion.span>
              </span>{" "}
            </Fragment>
          ))}
        </h1>

        <motion.p className="hero-sub" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, ease, delay: 0.8 }}>
          {SUBHEADLINE}
        </motion.p>

        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.9, ease, delay: 0.95 }}>
          <Player />
          <p className="micro">Clique no play e veja como funciona</p>
          <div className="cta-row" style={{ marginTop: 18 }}>
            <CTA>[Quero + resultado desejado]</CTA>
          </div>
        </motion.div>
      </div>
    </header>
  );
}
