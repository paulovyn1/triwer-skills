import { useEffect, useRef, useState } from "react";
import { motion, animate, useInView, useMotionValue, useSpring } from "motion/react";
import { CHECKOUT_URL } from "../config.js";

export const ease = [0.22, 1, 0.36, 1];

export function Reveal({ children, delay = 0, y = 28, className, as = "div" }) {
  const Tag = motion[as];
  return (
    <Tag
      className={className}
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-12% 0px" }}
      transition={{ duration: 0.8, ease, delay }}
    >
      {children}
    </Tag>
  );
}

// Título que entra palavra por palavra, com máscara.
export function Words({ text, className, as = "h2", delay = 0, highlight = [] }) {
  const Tag = motion[as];
  const words = text.split(" ");
  return (
    <Tag
      className={className}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: "-10% 0px" }}
      transition={{ staggerChildren: 0.045, delayChildren: delay }}
    >
      {words.map((w, i) => (
        <span className="word-mask" key={i}>
          <motion.span
            className={highlight.includes(i) ? "word hl" : "word"}
            variants={{ hidden: { y: "110%" }, show: { y: "0%", transition: { duration: 0.75, ease } } }}
          >
            {w}
          </motion.span>{" "}
        </span>
      ))}
    </Tag>
  );
}

export const brl = (n) => "R$ " + Math.round(n).toLocaleString("pt-BR");

export function CountUp({ to, format = (n) => Math.round(n).toLocaleString("pt-BR"), duration = 1.6, className, start }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-10% 0px" });
  const [val, setVal] = useState(0);
  const go = start === undefined ? inView : start && inView;
  useEffect(() => {
    if (!go) return;
    const c = animate(0, to, { duration, ease: [0.16, 1, 0.3, 1], onUpdate: setVal });
    return () => c.stop();
  }, [go, to, duration]);
  return (
    <span ref={ref} className={className}>
      {format(val)}
    </span>
  );
}

// Botão que segue levemente o cursor.
export function CTA({ children = "Quero garantir meu guia agora", href = CHECKOUT_URL, variant = "primary", className = "" }) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const sx = useSpring(x, { stiffness: 220, damping: 16 });
  const sy = useSpring(y, { stiffness: 220, damping: 16 });
  const onMove = (e) => {
    const r = e.currentTarget.getBoundingClientRect();
    x.set((e.clientX - r.left - r.width / 2) * 0.18);
    y.set((e.clientY - r.top - r.height / 2) * 0.28);
  };
  const reset = () => {
    x.set(0);
    y.set(0);
  };
  return (
    <motion.a
      href={href}
      className={`cta cta-${variant} ${className}`}
      style={{ x: sx, y: sy }}
      onPointerMove={onMove}
      onPointerLeave={reset}
      whileTap={{ scale: 0.97 }}
    >
      <span className="cta-label">{children}</span>
      <span className="cta-arrow" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </span>
    </motion.a>
  );
}

export function Label({ children }) {
  return <span className="label">// {children}</span>;
}

// Faixa amarela de isolamento, a mesma da capa.
export function Tape({ children, rotate = -4, className = "" }) {
  return (
    <motion.span
      className={`tape ${className}`}
      initial={{ clipPath: "inset(0 100% 0 0)", rotate }}
      whileInView={{ clipPath: "inset(0 0% 0 0)", rotate }}
      viewport={{ once: true, margin: "-10% 0px" }}
      transition={{ duration: 0.7, ease, delay: 0.25 }}
    >
      {children}
    </motion.span>
  );
}

export function Pin({ className = "", style }) {
  return (
    <svg className={`pin ${className}`} style={style} viewBox="0 0 24 32" aria-hidden="true">
      <path d="M12 0C5.4 0 0 5.2 0 11.7 0 20.4 12 32 12 32s12-11.6 12-20.3C24 5.2 18.6 0 12 0z" fill="currentColor" />
      <circle cx="12" cy="11.5" r="4.2" fill="#0d1526" />
    </svg>
  );
}
