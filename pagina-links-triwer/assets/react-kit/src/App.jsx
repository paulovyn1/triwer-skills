import { useEffect, useRef, useState } from "react";
import { AnimatePresence, MotionConfig, motion, useInView, useMotionValue, useScroll, useSpring, useTransform } from "motion/react";
import BookMockup from "./components/BookMockup.jsx";
import * as I from "./components/icons.jsx";
import { CARDS, DESTAQUE, FRASE_MENU, GRATUITO, PERFIL, REDES, RODAPE } from "./config.js";

const ease = [0.22, 1, 0.36, 1];
const Icone = ({ nome, ...p }) => {
  const C = I.porNome[nome] || I.Link;
  return <C {...p} />;
};

// Link ainda sem destino ("#") não faz nada ao clicar.
const linkProps = (href) => ({
  href,
  ...(href.startsWith("http") ? { target: "_blank", rel: "noopener noreferrer" } : {}),
  onClick: href === "#" ? (e) => e.preventDefault() : undefined,
});

// "texto com **negrito**" -> partes com <b>.
const Rich = ({ text }) => text.split(/\*\*(.+?)\*\*/g).map((t, i) => (i % 2 ? <b key={i}>{t}</b> : t));

const MENU = [
  { nome: DESTAQUE.titulo, tag: DESTAQUE.selo, href: DESTAQUE.href, icone: DESTAQUE.midia?.tipo === "livro" ? "livro" : "link" },
  ...CARDS.map((c) => ({ nome: c.titulo, tag: c.tag || "", href: c.href, icone: c.icone })),
  ...(GRATUITO ? [{ nome: GRATUITO.titulo, tag: GRATUITO.selo, href: GRATUITO.href, icone: "quiz" }] : []),
];

function Reveal({ children, delay = 0, y = 34, className }) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y, scale: 0.97 }}
      whileInView={{ opacity: 1, y: 0, scale: 1 }}
      viewport={{ once: true, margin: "-8% 0px" }}
      transition={{ duration: 0.9, ease, delay }}
    >
      {children}
    </motion.div>
  );
}

// Cartão que inclina levemente seguindo o dedo/cursor.
function Tilt({ children, className, href }) {
  const mx = useMotionValue(0);
  const my = useMotionValue(0);
  const rx = useSpring(useTransform(my, [-0.5, 0.5], [4, -4]), { stiffness: 160, damping: 18 });
  const ry = useSpring(useTransform(mx, [-0.5, 0.5], [-5, 5]), { stiffness: 160, damping: 18 });
  const move = (e) => {
    const r = e.currentTarget.getBoundingClientRect();
    mx.set((e.clientX - r.left) / r.width - 0.5);
    my.set((e.clientY - r.top) / r.height - 0.5);
  };
  const leave = () => {
    mx.set(0);
    my.set(0);
  };
  return (
    <motion.a
      {...linkProps(href)}
      className={className}
      style={{ rotateX: rx, rotateY: ry, transformPerspective: 900 }}
      onPointerMove={move}
      onPointerLeave={leave}
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 300, damping: 22 }}
    >
      {children}
    </motion.a>
  );
}

function Words({ text, tape = [], delay = 0 }) {
  return (
    <motion.h1 className="hero-title" initial="hidden" animate="show" transition={{ staggerChildren: 0.06, delayChildren: delay }}>
      {text.split(" ").map((w, i) => (
        <span className="word-mask" key={i}>
          <motion.span className={tape.includes(i) ? "word word-tape" : "word"} variants={{ hidden: { y: "115%" }, show: { y: "0%", transition: { duration: 0.8, ease } } }}>
            {w}
          </motion.span>
        </span>
      ))}
    </motion.h1>
  );
}

function Socials({ delay = 0, className = "" }) {
  return (
    <motion.div className={`socials ${className}`} initial="hidden" animate="show" transition={{ staggerChildren: 0.08, delayChildren: delay }}>
      {REDES.map(({ nome, href, icone }) => (
        <motion.a
          key={nome}
          {...linkProps(href)}
          aria-label={nome}
          className="social"
          variants={{ hidden: { opacity: 0, scale: 0.4 }, show: { opacity: 1, scale: 1, transition: { type: "spring", stiffness: 380, damping: 18 } } }}
          whileHover={{ y: -3, scale: 1.08 }}
          whileTap={{ scale: 0.92 }}
        >
          <Icone nome={icone} />
        </motion.a>
      ))}
    </motion.div>
  );
}

function Header({ onMenu, onShare }) {
  return (
    <motion.header className="top" initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, ease }}>
      <motion.button className="icon-btn" onClick={onMenu} aria-label="Abrir menu" whileTap={{ scale: 0.9 }} whileHover={{ rotate: 90 }}>
        <I.Grid />
      </motion.button>
      <img className="logo" src={PERFIL.logo} alt={PERFIL.logoAlt} />
      <motion.button className="icon-btn" onClick={onShare} aria-label="Compartilhar" whileTap={{ scale: 0.9 }}>
        <I.Share />
      </motion.button>
    </motion.header>
  );
}

function Menu({ open, onClose }) {
  useEffect(() => {
    if (!open) return;
    const esc = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", esc);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", esc);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div className="veil" onClick={onClose} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }} />
          <motion.nav
            className="sheet"
            initial={{ opacity: 0, y: -24, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -16, scale: 0.97 }}
            transition={{ type: "spring", stiffness: 320, damping: 30 }}
            aria-label="Menu"
          >
            <div className="sheet-head">
              <span className="eyebrow">Menu</span>
              <motion.button className="icon-btn ghost" onClick={onClose} aria-label="Fechar menu" whileTap={{ scale: 0.9 }} whileHover={{ rotate: 90 }}>
                <I.Close />
              </motion.button>
            </div>
            <motion.ul initial="hidden" animate="show" transition={{ staggerChildren: 0.06, delayChildren: 0.1 }}>
              {MENU.map(({ nome, tag, href, icone }) => (
                <motion.li key={nome} variants={{ hidden: { opacity: 0, x: -14 }, show: { opacity: 1, x: 0, transition: { duration: 0.5, ease } } }}>
                  <a {...linkProps(href)} className="sheet-item" onClick={href === "#" ? (e) => e.preventDefault() : onClose}>
                    <span className="sheet-ico"><Icone nome={icone} /></span>
                    <span className="sheet-name">{nome}</span>
                    <span className="sheet-tag">{tag}</span>
                    <I.ArrowUpRight className="sheet-arrow" />
                  </a>
                </motion.li>
              ))}
            </motion.ul>
            <p className="sheet-quote"><Rich text={FRASE_MENU} /></p>
            <Socials delay={0.35} className="center" />
          </motion.nav>
        </>
      )}
    </AnimatePresence>
  );
}

function Hero() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const imgY = useTransform(scrollYProgress, [0, 1], [0, 90]);
  const imgS = useTransform(scrollYProgress, [0, 1], [1.04, 1.16]);

  return (
    <section className="hero" ref={ref}>
      <motion.div className="hero-card" initial={{ opacity: 0, scale: 0.94, y: 20 }} animate={{ opacity: 1, scale: 1, y: 0 }} transition={{ duration: 1.1, ease }}>
        <motion.img className="hero-img" src={PERFIL.foto} alt={PERFIL.fotoAlt} style={{ y: imgY, scale: imgS }} />
        <div className="hero-shade" />
        <div className="hero-copy">
          <motion.span className="eyebrow light" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5, duration: 0.8 }}>
            {PERFIL.rotulo}
          </motion.span>
          <Words text={PERFIL.frase} tape={PERFIL.faixa} delay={0.45} />
          <Socials delay={1.1} />
        </div>
      </motion.div>
      <a href="#links" className="notch-cue" aria-label="Ver links">
        <motion.span animate={{ y: [0, 4, 0] }} transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}>
          <I.Chevron />
        </motion.span>
      </a>
    </section>
  );
}

// Traços de fundo do card de destaque. Troque por um elemento gráfico da identidade do expert.
const tracos = ["M-20 70 L260 -20", "M-20 170 L380 10", "M40 300 L470 90", "M80 -10 L240 330", "M210 -10 L360 300", "M330 210 C400 170 450 170 520 140"];

function DestaqueCard() {
  const { titulo, faixa, midia } = DESTAQUE;
  const semFaixa = faixa && titulo.endsWith(faixa) ? titulo.slice(0, -faixa.length) : titulo;
  return (
    <Reveal className="feature-wrap">
      <span className="notch notch-yellow">{DESTAQUE.selo}</span>
      <div className="feature">
        <svg className="feature-planta" viewBox="0 0 460 320" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
          <g fill="none" stroke="currentColor" strokeWidth="1.2">
            {tracos.map((d, i) => (
              <motion.path key={d} d={d} initial={{ pathLength: 0 }} whileInView={{ pathLength: 1 }} viewport={{ once: true }} transition={{ duration: 2, delay: 0.2 + i * 0.12, ease }} />
            ))}
            <motion.circle cx="400" cy="70" r="34" initial={{ pathLength: 0 }} whileInView={{ pathLength: 1 }} viewport={{ once: true }} transition={{ duration: 1.8, delay: 0.6 }} />
          </g>
        </svg>
        {midia?.tipo === "livro" && (
          <div className="feature-book">
            <BookMockup src={midia.src} alt={midia.alt} size={190} baseY={-20} />
          </div>
        )}
        {midia?.tipo === "foto" && (
          <motion.img
            className="feature-foto"
            src={midia.src}
            alt={midia.alt}
            initial={{ opacity: 0, scale: 0.92, rotate: -2 }}
            whileInView={{ opacity: 1, scale: 1, rotate: -2 }}
            viewport={{ once: true }}
            transition={{ duration: 0.9, ease }}
          />
        )}
        <div className="feature-body">
          <h2 className="feature-title">
            {semFaixa}
            {faixa && titulo.endsWith(faixa) && (
              <motion.span
                className="tape"
                initial={{ clipPath: "inset(0 100% 0 0)", rotate: -3 }}
                whileInView={{ clipPath: "inset(0 0% 0 0)", rotate: -3 }}
                viewport={{ once: true }}
                transition={{ duration: 0.7, ease, delay: 0.5 }}
              >
                {faixa}
              </motion.span>
            )}
          </h2>
          <p className="feature-sub">{DESTAQUE.texto}</p>
          <Magnetic href={DESTAQUE.href}>{DESTAQUE.cta}</Magnetic>
        </div>
      </div>
    </Reveal>
  );
}

// Botão com brilho que segue o cursor.
function Magnetic({ href, children, variant = "yellow" }) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const sx = useSpring(x, { stiffness: 220, damping: 16 });
  const sy = useSpring(y, { stiffness: 220, damping: 16 });
  return (
    <motion.a
      {...linkProps(href)}
      className={`cta cta-${variant}`}
      style={{ x: sx, y: sy }}
      onPointerMove={(e) => {
        const r = e.currentTarget.getBoundingClientRect();
        x.set((e.clientX - r.left - r.width / 2) * 0.12);
        y.set((e.clientY - r.top - r.height / 2) * 0.25);
      }}
      onPointerLeave={() => {
        x.set(0);
        y.set(0);
      }}
      whileTap={{ scale: 0.97 }}
    >
      <span>{children}</span>
      <span className="cta-arrow" aria-hidden="true"><I.ArrowRight /></span>
    </motion.a>
  );
}

function LinkCard({ href, titulo, texto, cta, img, imgAlt, icone, tom }) {
  return (
    <Reveal>
      <Tilt href={href} className={`link-card ${tom === "claro" ? "light" : ""}`}>
        {img && <img className="link-img" src={img} alt={imgAlt} loading="lazy" />}
        <div className="link-shade" />
        <div className="link-copy">
          <h3 className="link-title">{titulo}</h3>
          <p className="link-text"><Rich text={texto} /></p>
          <span className="link-cta">
            <Icone nome={icone} /> {cta}
            <span className="link-arrow"><I.ArrowUpRight /></span>
          </span>
        </div>
      </Tilt>
    </Reveal>
  );
}

// Tela do material gratuito que vai marcando os itens em sequência.
function TelaGratuito() {
  const ref = useRef(null);
  const inView = useInView(ref, { margin: "-15% 0px" });
  const [step, setStep] = useState(0);
  const itens = GRATUITO.itens;
  useEffect(() => {
    if (!inView) return;
    const t = setInterval(() => setStep((s) => (s + 1) % (itens.length + 3)), 900);
    return () => clearInterval(t);
  }, [inView, itens.length]);
  const done = Math.min(step, itens.length);

  return (
    <div className="quiz" ref={ref}>
      <div className="quiz-head">
        <span className="quiz-brand">{GRATUITO.telaTitulo}</span>
        <span className="quiz-count">{done}/{itens.length}</span>
      </div>
      <div className="quiz-bar">
        <motion.span animate={{ width: `${(done / itens.length) * 100}%` }} transition={{ duration: 0.6, ease }} />
      </div>
      <ul className="quiz-list">
        {itens.map((p, i) => {
          const on = i < done;
          return (
            <li key={p} className={on ? "on" : ""}>
              <motion.span className="quiz-box" animate={{ scale: on ? [1, 1.25, 1] : 1 }} transition={{ duration: 0.4 }}>
                <AnimatePresence>
                  {on && (
                    <motion.span initial={{ scale: 0, rotate: -40 }} animate={{ scale: 1, rotate: 0 }} exit={{ scale: 0 }} transition={{ type: "spring", stiffness: 500, damping: 20 }}>
                      <I.Check />
                    </motion.span>
                  )}
                </AnimatePresence>
              </motion.span>
              {p}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

function GratuitoCard() {
  return (
    <Reveal className="feature-wrap">
      <span className="notch">{GRATUITO.selo}</span>
      <div className="free">
        <div className="free-glow" />
        <TelaGratuito />
        <h2 className="free-title">{GRATUITO.titulo}</h2>
        <p className="free-sub">{GRATUITO.texto}</p>
        <Magnetic href={GRATUITO.href} variant="light">{GRATUITO.cta}</Magnetic>
        {GRATUITO.nota && <p className="free-note">{GRATUITO.nota}</p>}
      </div>
    </Reveal>
  );
}

export default function App() {
  const [menu, setMenu] = useState(false);
  const [toast, setToast] = useState(false);

  const share = async () => {
    const data = { title: PERFIL.tituloAba, url: window.location.href };
    try {
      if (navigator.share) return await navigator.share(data);
      await navigator.clipboard.writeText(data.url);
      setToast(true);
      setTimeout(() => setToast(false), 1800);
    } catch {
      /* compartilhamento cancelado */
    }
  };

  return (
    <MotionConfig reducedMotion="user">
      <div className="grain" />
      <main className="page">
        <Header onMenu={() => setMenu(true)} onShare={share} />
        <Menu open={menu} onClose={() => setMenu(false)} />
        <Hero />
        <div className="stack" id="links">
          <DestaqueCard />
          {CARDS.map((c) => (
            <LinkCard key={c.titulo} {...c} />
          ))}
          {GRATUITO && <GratuitoCard />}
        </div>
        <footer className="foot">{RODAPE}</footer>
      </main>
      <AnimatePresence>
        {toast && (
          <motion.div className="toast" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 20 }}>
            Link copiado
          </motion.div>
        )}
      </AnimatePresence>
    </MotionConfig>
  );
}
