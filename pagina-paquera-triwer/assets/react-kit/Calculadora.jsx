import { useEffect, useRef, useState } from "react";
import { AnimatePresence, animate, motion, useInView } from "motion/react";
import { CTA, brl, ease } from "./ui.jsx";

// Calculadora do "custo de continuar igual".
// cenarios: { chave: { rotulo, hoje, cima, legendaHoje, legendaCima } }
// textos: { capHoje, capCima, capResultado, subResultado, frase, contraste, pergunta, fonte, botao }
// multiplicador: 12 para mês -> ano. Use 1 se os valores já forem anuais.
function Numero({ value, delay = 0, big = false, run, format }) {
  const [v, setV] = useState(0);
  useEffect(() => {
    if (!run) return;
    const c = animate(0, value, { duration: big ? 1.8 : 0.9, delay, ease: [0.16, 1, 0.3, 1], onUpdate: setV });
    return () => c.stop();
  }, [value, delay, big, run]);
  return <span className={big ? "calc-grande" : "calc-num"}>{format(v)}</span>;
}

const soNumero = (s) => Number(String(s).replace(/\D/g, "")) || 0;
const mascara = (s) => (soNumero(s) ? soNumero(s).toLocaleString("pt-BR") : "");

export default function Calculadora({ cenarios, textos, multiplicador = 12, format = brl, permitirDigitar = true }) {
  const chaves = Object.keys(cenarios);
  const [modo, setModo] = useState(chaves[0]);
  const [hojeTxt, setHojeTxt] = useState("");
  const [cimaTxt, setCimaTxt] = useState("");
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-15% 0px" });

  const manual = modo === "manual";
  const c = cenarios[modo];
  const hoje = manual ? soNumero(hojeTxt) : c.hoje;
  const cima = manual ? soNumero(cimaTxt) : c.cima;
  const preenchido = !manual || (hoje > 0 && cima > 0);
  const diff = (cima - hoje) * multiplicador;
  const valido = preenchido && diff > 0;
  const chave = `${modo}-${hoje}-${cima}`;
  const abas = [...chaves.map((k) => [k, cenarios[k].rotulo]), ...(permitirDigitar ? [["manual", "Digitar meus valores"]] : [])];

  return (
    <div ref={ref} className={`calc vivo${manual ? " manual" : ""}${!valido ? " invalido" : ""}`}>
      <div className="calc-tabs" role="tablist">
        {abas.map(([k, rot]) => (
          <button key={k} role="tab" aria-selected={modo === k} className={modo === k ? "calc-tab on" : "calc-tab"} onClick={() => setModo(k)}>
            {modo === k && <motion.span layoutId="calc-tab-bg" className="calc-tab-bg" transition={{ type: "spring", stiffness: 400, damping: 32 }} />}
            <span>{rot}</span>
          </button>
        ))}
      </div>

      <AnimatePresence>
        {manual && (
          <motion.div className="calc-inputs" initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} transition={{ duration: 0.4, ease }}>
            <label>
              <span>{textos.capHoje}</span>
              <div className="calc-campo"><em>R$</em><input inputMode="numeric" value={hojeTxt} onChange={(e) => setHojeTxt(mascara(e.target.value))} /></div>
            </label>
            <label>
              <span>{textos.capCima}</span>
              <div className="calc-campo"><em>R$</em><input inputMode="numeric" value={cimaTxt} onChange={(e) => setCimaTxt(mascara(e.target.value))} /></div>
            </label>
          </motion.div>
        )}
      </AnimatePresence>

      {/* O CSS do template mostra o aviso só quando o container tem .invalido. */}
      <p className="calc-aviso">{preenchido ? "Confere os valores. O segundo precisa ser maior que o primeiro." : "Digita os dois valores para ver a conta."}</p>
      <div className="calc-linha" key={chave}>
        {valido && (
          <>
            <motion.div className="calc-celula" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ duration: 0.6, ease }}>
              <span className="calc-cap">{textos.capHoje}</span>
              <Numero value={hoje} run={inView} format={format} />
              {!manual && <span className="calc-sub">{c.legendaHoje}</span>}
            </motion.div>
            <span className="calc-op">→</span>
            <motion.div className="calc-celula" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ duration: 0.6, ease, delay: 0.4 }}>
              <span className="calc-cap">{textos.capCima}</span>
              <Numero value={cima} delay={0.4} run={inView} format={format} />
              {!manual && <span className="calc-sub">{c.legendaCima}</span>}
            </motion.div>
            <span className="calc-op">=</span>
            <motion.div className="calc-celula calc-resultado" initial={{ opacity: 0, y: 20 }} animate={inView ? { opacity: 1, y: 0 } : {}} transition={{ duration: 0.6, ease, delay: 0.8 }}>
              <span className="calc-cap">{textos.capResultado}</span>
              <Numero value={diff} delay={0.9} big run={inView} format={format} />
              <span className="calc-sub">{textos.subResultado}</span>
            </motion.div>
          </>
        )}
      </div>

      {valido && inView && (
        <motion.div className="calc-depois" key={"d-" + chave} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 2.2, duration: 0.7, ease }}>
          <p className="calc-frase">{textos.frase}</p>
          <p className="calc-contraste">{textos.contraste}</p>
          <p className="calc-pergunta">{textos.pergunta}</p>
          <CTA>{textos.botao}</CTA>
        </motion.div>
      )}
      <p className="calc-fonte">{textos.fonte} Os valores que tu digita não são guardados nem enviados.</p>
    </div>
  );
}
