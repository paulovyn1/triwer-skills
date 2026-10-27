import { useRef, useState } from "react";
import { AnimatePresence, motion, useScroll, useTransform } from "motion/react";
import { CTA, CountUp, Label, Reveal, Words, ease, hl } from "./ui.jsx";
import { CNPJ, CUSTO_DE, CUSTO_PARA, DEPOIMENTOS, EMPRESAS, GARANTIA_DIAS, PARCELA, PARCELAS, PRECO, PRECO_AVISTA, PRECO_DE, WHATSAPP_URL } from "../config.js";

// TODO o texto abaixo é exemplo anonimizado. Cada [colchete] é uma pendência a trocar pela copy aprovada.
// Títulos: passe o texto e a frase a destacar com hl(texto, "frase"), sem contar índices.
const T = (texto, frase) => ({ texto, hl: hl(texto, frase) });

const fmt = (n) => Math.round(n).toLocaleString("pt-BR");

function Titulo({ t, className = "h2", delay }) {
  return <Words as="h2" className={className} text={t.texto} highlight={t.hl} delay={delay} />;
}

/* ---------- Topo ---------- */
export function Nav() {
  return (
    <nav className="nav">
      <div className="wrap nav-in">
        <img className="nav-logo" src="/img/logo.svg" alt="[Nome da marca]" width="140" height="46" />
        <CTA variant="ghost">[Quero + resultado]</CTA>
      </div>
    </nav>
  );
}

/* ---------- Faixa de autoridade (logo depois do hero) ---------- */
export function Logos() {
  const lista = [...EMPRESAS, ...EMPRESAS];
  return (
    <section className="authority">
      <div className="wrap center">
        <p className="authority-tit">
          Um curso <strong>só de [área]</strong>, para quem trabalha em [área].
        </p>
        <p className="authority-sub">Seja direcionado pelo mesmo profissional que liderou [a área] dessas grandes empresas:</p>
      </div>
      <div className="logos-mask" aria-label="Empresas da trajetória">
        <div className="logos-track">
          {lista.map((e, i) => (
            <span className="logo-word" key={i}>
              {e}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------- Identificação ---------- */
const TIT_IDENT = T("[Esforço do lead] e na hora do [resultado] passam outro na tua frente", "passam outro na tua frente");
const frasesDor = ["[Frase 1: o que o lead entrega ou faz.]", "[Frase 2: o que ele já viu acontecer.]", "[Frase 3: o que ele já pensou em fazer, e a virada.]"];

export function Ident() {
  return (
    <section className="panel ident" id="dor">
      <Titulo t={TIT_IDENT} />
      <div className="frases">
        {frasesDor.map((f, i) => (
          <Reveal key={f} delay={0.08 * i} className="frase">
            <span className="frase-n">0{i + 1}</span>
            <p>{f}</p>
          </Reveal>
        ))}
      </div>
      <Reveal>
        <p className="ident-fecho grad">Agora é a tua vez de [resultado]!</p>
      </Reveal>
    </section>
  );
}

/* ---------- Provas ---------- */
const TIT_PROVAS = T("[Verbo no imperativo] o método e tenha resultados como esses", "resultados como esses");

export function Provas() {
  return (
    <section className="panel provas">
      <div className="center">
        <Titulo t={TIT_PROVAS} />
        <Reveal>
          <p className="lead">[Uma frase de contexto sobre quem são os casos abaixo.]</p>
        </Reveal>
      </div>
      <div className="provas-grid">
        <Reveal className="prova">
          <span className="chip">[Resultado 1 em destaque, com número e prazo]</span>
          <p>[Contexto em uma frase.]</p>
          <small>[Nome | Cargo ou perfil]</small>
        </Reveal>
        <Reveal className="prova" delay={0.1}>
          <span className="chip y">[Resultado 2 em destaque, com número e prazo]</span>
          <p>[Contexto em uma frase.]</p>
          <small>[Nome | Cargo ou perfil]</small>
        </Reveal>
        <Reveal className="prova" delay={0.2}>
          <span className="chip">[Resultado 3 em destaque, com número e prazo]</span>
          <p>[Contexto em uma frase.]</p>
          <small>[Nome | Cargo ou perfil]</small>
        </Reveal>
      </div>
      <div className="cta-row">
        <CTA>[Quero + resultado]</CTA>
      </div>
    </section>
  );
}

/* ---------- Texto gigante que acende no scroll ---------- */
const FRASE_GIGANTE = "[A virada do problema em uma frase curta. O problema não é X. É Y.]";

function GW({ w, i, n, p }) {
  const a = i / n;
  const o = useTransform(p, [a * 0.7, a * 0.7 + 0.18], [0.12, 1]);
  return (
    <motion.span className="gw" style={{ opacity: o }}>
      {w}
    </motion.span>
  );
}

export function Giant() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start 85%", "end 55%"] });
  const words = FRASE_GIGANTE.split(" ");
  return (
    <section className="giant" ref={ref}>
      <div className="wrap">
        <p>
          {words.map((w, i) => (
            <GW key={i} w={w} i={i} n={words.length} p={scrollYProgress} />
          ))}
        </p>
      </div>
    </section>
  );
}

/* ---------- As 3 travas (caixas numeradas) ---------- */
const TIT_TRAVAS = T("Por que ainda [não aconteceu o resultado]? São 3 travas.", "São 3 travas.");
const travas = [
  ["[Trava 1 em até 6 palavras]", "[A cena que o lead reconhece, em 2 frases.]"],
  ["[Trava 2 em até 6 palavras]", "[A cena que o lead reconhece, em 2 frases.]"],
  ["[Trava 3 em até 6 palavras]", "[A cena que o lead reconhece, em 2 frases.]"],
];

export function Travas() {
  return (
    <section className="panel center">
      <Titulo t={TIT_TRAVAS} />
      <Reveal>
        <p className="lead">[Uma frase que explica por que a competência que trouxe o lead até aqui é a mesma que o prende.]</p>
      </Reveal>
      <div className="steps">
        {travas.map(([t, d], i) => (
          <Reveal key={t} delay={i * 0.1} className="step">
            <span className="step-n">0{i + 1}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </Reveal>
        ))}
      </div>
    </section>
  );
}

/* ---------- O que é o método (3 passos). O nome do método aparece aqui pela primeira vez ---------- */
const TIT_SIMPLES = T("[Resultado] é mais simples do que parece", "mais simples");
const TIT_OQUEE = T("O que é o [Nome do Método]?", "[Nome do Método]?");
const passos = [
  ["Assista", "[Formato das aulas e duração total, para caber na semana do aluno.]"],
  ["Aplique no trabalho", "[O exercício de campo semanal, na rotina real do aluno.]"],
  ["Poste o entregável", "[Onde o aluno mostra o que fez e quem dá feedback.]"],
];

export function OQueE() {
  return (
    <>
      <section className="giant" style={{ paddingBottom: 0 }}>
        <div className="wrap center">
          <Label>[nome do método]</Label>
          <Titulo t={TIT_SIMPLES} />
        </div>
      </section>
      <section className="panel center">
        <Titulo t={TIT_OQUEE} />
        <Reveal>
          <p className="lead">[Um curso gravado, feito só para a área do aluno, que leva do ponto A ao ponto B. Dá para terminar em X, ou em Y no ritmo natural.]</p>
        </Reveal>
        <div className="steps">
          {passos.map(([t, d], i) => (
            <Reveal key={t} delay={i * 0.1} className="step">
              <span className="step-n">0{i + 1}</span>
              <h3>{t}</h3>
              <p>{d}</p>
            </Reveal>
          ))}
        </div>
      </section>
    </>
  );
}

/* ---------- Para quem é ---------- */
const TIT_PARAQUEM = T("Para quem é o [Nome do Método]?", "[Nome do Método]?");
const subareas = ["[Subárea 1]", "[Subárea 2]", "[Subárea 3]", "[Subárea 4]", "[Subárea 5]", "[Subárea 6]"];

export function ParaQuem() {
  const lista = [...subareas, ...subareas, ...subareas];
  return (
    <section className="panel center">
      <Titulo t={TIT_PARAQUEM} />
      <Reveal>
        <p className="lead">[Feito para quem quer X, em qualquer uma destas subáreas.]</p>
      </Reveal>
      <h3 style={{ font: "600 24px var(--display)", margin: "30px 0 0" }}>Para quem trabalha em:</h3>
      <div className="pills" aria-hidden="true">
        <div className="pills-track">
          {lista.map((e, i) => (
            <span className="pill-i" key={i}>{e}</span>
          ))}
        </div>
        <div className="pills-track rev">
          {[...lista].reverse().map((e, i) => (
            <span className="pill-i" key={i}>{e}</span>
          ))}
        </div>
      </div>
      <div className="inner-card">
        <div>
          <h3 className="grad" style={{ display: "inline-block" }}>[ou qualquer outra subárea da tua área.]</h3>
          <p>[Funciona mesmo para quem é X;]</p>
          <p>[já tentou Y e não funcionou;]</p>
          <p>[ou nunca fez Z.]</p>
        </div>
      </div>
      <p className="nao-e">
        Se o que tu procura é <strong>[o que o produto não é]</strong>, esse não é o curso. [Aqui é o que se faz no dia a dia.]
      </p>
    </section>
  );
}

/* ---------- Contraste ---------- */
const TIT_CONTRASTE = T("Isto aqui não é mais um curso", "mais um curso");
const naoE = ["[O que o produto não é 1]", "[O que o produto não é 2]", "[O que o produto não é 3]", "[O que o produto não é 4]"];
const eh = ["[O que o produto é 1]", "[O que o produto é 2]", "[O que o produto é 3]", "[O que o produto é 4]"];

export function Contraste() {
  return (
    <section className="section">
      <div className="wrap">
        <Titulo t={TIT_CONTRASTE} />
        <Reveal>
          <p className="lead">[Quebra a comparação mental do lead com outros caminhos que ele já tentou.]</p>
        </Reveal>
        <div className="cmp">
          <div className="cmp-col cmp-no">
            <h3>O que o curso NÃO é</h3>
            {naoE.map((a, i) => (
              <motion.p key={i} initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1, duration: 0.6, ease }}>
                <span className="cmp-ic">✕</span>
                <span className="cmp-strike">{a}</span>
              </motion.p>
            ))}
          </div>
          <div className="cmp-col cmp-yes">
            <h3>O que o curso É</h3>
            {eh.map((b, i) => (
              <motion.p key={i} initial={{ opacity: 0, x: 20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 + i * 0.1, duration: 0.6, ease }}>
                <span className="cmp-ic">✓</span>
                {b}
              </motion.p>
            ))}
          </div>
        </div>
        <div className="cta-row">
          <CTA>[Quero + resultado]</CTA>
        </div>
      </div>
    </section>
  );
}

/* ---------- Depoimentos (só aparece com itens em config.js) ---------- */
export function Depoimentos() {
  if (!DEPOIMENTOS.length) return null;
  return (
    <section className="panel center">
      <Titulo t={T("Quem já passou por aqui", "já passou")} />
      <div className="provas-grid">
        {DEPOIMENTOS.map((d) => (
          <Reveal key={d.nome} className="prova">
            {d.img && <img src={d.img} alt={`Depoimento de ${d.nome}`} loading="lazy" style={{ borderRadius: 12, marginBottom: 12 }} />}
            <span className="chip y">{d.prazo}</span>
            <small>
              {d.nome} | {d.cargo}, {d.empresa}
            </small>
          </Reveal>
        ))}
      </div>
    </section>
  );
}

/* ---------- Etapas (cartões brancos). Uma por módulo ou semana ---------- */
const TIT_ETAPAS = T("Tu vai percorrer [N] etapas", "[N] etapas");
const etapas = [1, 2, 3, 4, 5].map((n) => ({
  letra: String(n),
  sem: `Semana ${n}`,
  nome: `[Nome da etapa ${n}]`,
  titulo: `[Título da etapa ${n}, começando com verbo]`,
  desc: "[Descrição em até 2 frases: o que muda para o aluno nesta etapa.]",
  res: ["[Resultado verificável 1]", "[Resultado verificável 2]", "[Resultado verificável 3]"],
  entrega: "[O que o aluno entrega ao fim da etapa.]",
}));

export function Etapas() {
  return (
    <section className="panel">
      <div className="center">
        <Titulo t={TIT_ETAPAS} />
        <Reveal>
          <p className="lead">[Cada módulo vira uma aula curta, um exercício na rotina do aluno e um entregável. Os resultados começam a aparecer desde a primeira etapa.]</p>
        </Reveal>
      </div>
      <div className="etapas">
        {etapas.map((e) => (
          <motion.article key={e.letra} className="etapa" initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: "-8% 0px" }} transition={{ duration: 0.8, ease }}>
            <div>
              <span className="etapa-pill">{e.sem}</span>
              <h3>{e.titulo}</h3>
              <p>{e.desc}</p>
              <span className="res-tag">Resultado Esperado</span>
              <ul>
                {e.res.map((r) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
              <p className="etapa-entrega">
                <b>Entregável:</b> {e.entrega}
              </p>
            </div>
            <div className="tile">
              <span className="tile-letra">{e.letra}</span>
              <span className="tile-t">{e.nome}</span>
              <span className="tile-s">{e.sem}</span>
            </div>
          </motion.article>
        ))}
      </div>
      <div className="cta-row">
        <CTA>[Quero + resultado]</CTA>
      </div>
    </section>
  );
}

/* ---------- Material incluído ---------- */
const TIT_MATERIAL = T("Ferramenta de trabalho, não anexo bonito", "não anexo bonito");
const materiais = [1, 2, 3, 4, 5, 6].map((n) => [`[Material ${n}]`, "[Formato e para que serve, em uma linha.]"]);

export function Material() {
  return (
    <section className="section">
      <div className="wrap">
        <Titulo t={TIT_MATERIAL} />
        <div className="mat-grid">
          {materiais.map(([t, d], i) => (
            <Reveal key={t} delay={(i % 3) * 0.08} className="mat">
              <span className="mat-ic">
                <svg viewBox="0 0 40 40"><rect x="8" y="6" width="24" height="29" rx="3" fill="none" stroke="currentColor" strokeWidth="2.4" /><path d="M14 17l3 3 6-6M14 27h12" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" /></svg>
              </span>
              <h3>{t}</h3>
              <p>{d}</p>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------- Bônus. Título neutro, sem terceira pessoa e sem preço no cartão ---------- */
const bonus = [
  ["[Bônus 1, título neutro]", "[O que é, quando, quantas vezes, limite de vagas se houver.]", "[Palavra]", "[detalhe]"],
  ["[Bônus 2, título neutro]", "[O que é, por quanto tempo, quem modera.]", "[Palavra]", "[detalhe]"],
  ["[Bônus 3, título neutro]", "[O que é, formato, duração, para que serve.]", "[Palavra]", "[detalhe]"],
];

export function Bonus() {
  return (
    <section className="section">
      <div className="wrap">
        <div className="bonus-head">
          <p className="bonus-giant" aria-hidden="true">bônus</p>
          <Label>e ainda leva 3 bônus sem pagar nada a mais</Label>
        </div>
        <div className="bonus-list">
          {bonus.map(([t, d, a, b]) => (
            <Reveal key={t} className="bonus-card">
              <div>
                <img className="b-logo" src="/img/logo.svg" alt="" width="110" height="36" />
                <h3>{t}</h3>
                <span className="badge">Bônus incluso</span>
                <p>{d}</p>
              </div>
              <div className="tile">
                <span className="tile-t" style={{ fontSize: "clamp(34px, 5vw, 54px)" }}>{a}</span>
                <span className="tile-s">{b}</span>
              </div>
            </Reveal>
          ))}
        </div>
        <div className="cta-row">
          <CTA>[Quero + resultado]</CTA>
        </div>
      </div>
    </section>
  );
}

/* ---------- Recapitulando + preço (a ÚNICA ancoragem de preço da página) ---------- */
const recap = [
  ["[Produto principal, com a estrutura entre parênteses]", "R$ [valor]"],
  ["[Materiais e templates]", "R$ [valor]"],
  ["Bônus: [bônus 1]", "R$ [valor]"],
  ["Bônus: [bônus 2]", "R$ [valor]"],
  ["Bônus: [bônus 3]", "R$ [valor]"],
];

export function Oferta() {
  return (
    <section className="section" id="oferta">
      <div className="wrap recap">
        <h2 className="recap-tit">Recapitulando</h2>
        {recap.map(([t, v]) => (
          <div className="recap-linha" key={t}>
            <span>{t}</span>
            <s>{v}</s>
          </div>
        ))}
        <div className="recap-total">
          <span>Valor total:</span>
          <s>R$ {PRECO_DE}</s>
        </div>
        <div className="preco-card">
          <p className="mas">Mas hoje, para ter acesso a tudo isso, o teu investimento não é esse.</p>
          <h3>Garanta a tua vaga AGORA, por apenas</h3>
          <p className="preco-de">{PARCELAS}x de</p>
          <p className="preco-n">
            <small>R$</small>
            <span className="g">{PARCELA}</span>
          </p>
          <p className="preco-sub">ou à vista por R$ {PRECO_AVISTA}</p>
          <CTA className="cta-xl">[Quero + resultado]</CTA>
          <div className="selos">
            <span>
              <svg viewBox="0 0 24 24" width="16" height="16"><path d="M12 2l8 4v6c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10V6z" fill="none" stroke="currentColor" strokeWidth="2" /></svg>
              Compra segura
            </span>
            <span>
              <svg viewBox="0 0 24 24" width="16" height="16"><path d="M13 2L4 14h7l-1 8 9-12h-7z" fill="none" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" /></svg>
              Acesso imediato
            </span>
            <span>
              <svg viewBox="0 0 24 24" width="16" height="16"><path d="M20 6L9 17l-5-5" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" /></svg>
              {GARANTIA_DIAS} dias de garantia
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---------- A conta do custo (comparativo do gasto). Fica depois do preço ---------- */
const TIT_CUSTO = T("Cada mês parado no cargo errado custa [N] vezes o valor do curso", "custa [N] vezes o valor do curso");

export function Custo() {
  const mes = CUSTO_PARA - CUSTO_DE;
  const ano = mes * 12;
  return (
    <section className="panel center">
      <Label>a conta que ninguém faz</Label>
      <Titulo t={TIT_CUSTO} />
      <div className="custo-row">
        <div className="custo-cell">
          <span className="calc-cap">[Situação de hoje, média de mercado]</span>
          <span className="calc-num">R$ {fmt(CUSTO_DE)}</span>
        </div>
        <span className="calc-op">→</span>
        <div className="custo-cell">
          <span className="calc-cap">[Próximo degrau, média de mercado]</span>
          <span className="calc-num">R$ {fmt(CUSTO_PARA)}</span>
        </div>
        <span className="calc-op">=</span>
        <div className="custo-cell res">
          <span className="calc-cap">Diferença por ano</span>
          <span className="calc-big">
            R$ <CountUp to={ano} />
          </span>
          <span className="calc-sub">R$ {fmt(mes)} por mês</span>
        </div>
      </div>
      <Reveal>
        <p className="calc-pergunta">[A pergunta final da conta, ligando o custo de esperar ao valor do curso.]</p>
      </Reveal>
    </section>
  );
}

/* ---------- Garantia ---------- */
function Selo() {
  const N = 28;
  const pts = Array.from({ length: N * 2 }, (_, i) => {
    const r = i % 2 === 0 ? 100 : 91;
    const a = (Math.PI * i) / N - Math.PI / 2;
    return `${(100 + r * Math.cos(a)).toFixed(1)},${(100 + r * Math.sin(a)).toFixed(1)}`;
  }).join(" ");
  return (
    <div className="seal">
      <svg viewBox="0 0 200 200" aria-hidden="true">
        <polygon points={pts} fill="#0b7ff0" />
        <defs>
          <path id="circ" d="M100 100 m-74 0 a74 74 0 1 1 148 0 a74 74 0 1 1 -148 0" />
        </defs>
        <text fill="#fff" fontFamily="Outfit Variable, sans-serif" fontWeight="700" fontSize="11" letterSpacing="2.4">
          <textPath href="#circ">GARANTIA INCONDICIONAL · 100% DE VOLTA · GARANTIA INCONDICIONAL · 100% DE VOLTA ·</textPath>
        </text>
      </svg>
      <div className="seal-n">
        <b>{GARANTIA_DIAS}</b>
        <span>DIAS</span>
      </div>
    </div>
  );
}

export function Garantia() {
  return (
    <section className="section">
      <div className="wrap">
        <Reveal className="garantia-card">
          <Selo />
          <div>
            <h2>Tu não corre risco nenhum</h2>
            <p>[Descreva a garantia do aluno: prazo, como pedir e, se houver, a condição. O selo diz "incondicional": troque o texto do selo se houver condição.]</p>
            <p className="forte">100% do teu dinheiro de volta, sem burocracia.</p>
            <p>[Uma frase de fecho sobre por que a garantia existe.]</p>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

/* ---------- Criador ---------- */
const TIT_CRIADOR = T("Quem está por trás do [Nome do Método]", "[Nome do Método]");
const onde = [
  ["/img/expert-1.svg", "[Marco 1 da trajetória, específico e verificável]"],
  ["/img/expert-2.svg", "[Marco 2 da trajetória]"],
  ["/img/expert-3.svg", "[Marco 3 da trajetória]"],
  ["/img/expert-4.svg", "[Marco 4 da trajetória]"],
];

export function Criador() {
  return (
    <section className="panel center">
      <Label>criador</Label>
      <Titulo t={TIT_CRIADOR} />
      <div className="criador-top">
        <figure className="criador-foto">
          <img src="/img/expert-bio.svg" alt="[Nome do expert]" loading="lazy" width="1000" height="1000" />
        </figure>
        <div>
          <h3 className="criador-nome">[Nome do expert]</h3>
          <p className="quote-line">
            <span>“[Objeção do público 1.]”</span> <span>“[Objeção do público 2.]”</span>
          </p>
          <p>[Eu também. Por isso mesmo, tu não precisa virar outra pessoa.]</p>
          <p>[A história do expert em 3 frases: de onde saiu, aonde chegou, em quanto tempo.]</p>
          <p>[Fecho: quem ele é hoje e o que descobriu que serve para o lead.]</p>
        </div>
      </div>
      <h3 className="onde-tit">Onde ele já esteve</h3>
      <div className="onde-grid">
        {onde.map(([img, t]) => (
          <Reveal key={t} className="onde">
            <img src={img} alt="" loading="lazy" />
            <p>{t}</p>
          </Reveal>
        ))}
      </div>
      <div className="curric">
        <small>Estão no meu currículo</small>
        <div>
          {EMPRESAS.map((e) => (
            <span key={e}>{e}</span>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------- FAQ: uma pergunta por objeção real do público ---------- */
const faq = [
  ["[Objeção de tempo]?", "[Resposta honesta e específica.]"],
  ["[Objeção de preço]?", "[Resposta que liga o investimento ao custo de esperar. Sem repetir o preço.]"],
  ["[Objeção 'eu já tenho X']?", "[Resposta.]"],
  ["[Objeção 'minha situação é diferente']?", "[Resposta que diz onde o produto não resolve, se for o caso.]"],
  ["[Objeção de perfil, como timidez ou inexperiência]?", "[Resposta.]"],
  ["[Objeção de momento, como estar desempregado]?", "[Resposta.]"],
  ["[Objeção de porte ou nicho]?", "[Resposta.]"],
  ["Como e quando tenho acesso?", "Logo após a confirmação do pagamento, o acesso chega no teu e-mail."],
  ["E se eu não gostar?", `Tu tem ${GARANTIA_DIAS} dias de garantia. [Descreva a condição, se houver.] O dinheiro volta 100%.`],
];

export function FAQ() {
  const [aberto, setAberto] = useState(0);
  return (
    <section className="section">
      <div className="wrap narrow">
        <Label>faq</Label>
        <Titulo t={T("Dúvidas? Temos as respostas", "Temos as respostas")} />
        <div className="faq-list">
          {faq.map(([q, a], i) => {
            const on = aberto === i;
            return (
              <div className={on ? "faq-item on" : "faq-item"} key={q}>
                <button className="faq-q" onClick={() => setAberto(on ? -1 : i)} aria-expanded={on}>
                  <span>{q}</span>
                  <motion.span className="faq-plus" animate={{ rotate: on ? 45 : 0 }}>
                    +
                  </motion.span>
                </button>
                <AnimatePresence initial={false}>
                  {on && (
                    <motion.div className="faq-a" initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.4, ease }}>
                      <p>{a}</p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ---------- Fechamento ---------- */
const TIT_FECHA = T("Daqui a [N] semanas tu vai estar em um de dois lugares", "um de dois lugares");

export function Fechamento() {
  return (
    <section className="panel center fecha">
      <Titulo t={TIT_FECHA} />
      <Reveal>
        <p className="big">[Os dois destinos: ficar no mesmo ponto de hoje, ou chegar ao resultado com a prova na mão.]</p>
      </Reveal>
      <Reveal delay={0.1}>
        <p>[O que o expert não promete, e o que promete de verdade.]</p>
      </Reveal>
      <div className="cta-row">
        <CTA className="cta-xl">[Quero + resultado]</CTA>
        <p className="micro">Acesso imediato · {GARANTIA_DIAS} dias de garantia</p>
      </div>
    </section>
  );
}

export function Whats() {
  return (
    <section className="section">
      <div className="wrap whats-in">
        <h2>Dúvidas? Chame minha equipe no WhatsApp</h2>
        <CTA href={WHATSAPP_URL} variant="ghost">
          Ir para o WhatsApp
        </CTA>
      </div>
    </section>
  );
}

export function Footer() {
  return (
    <footer className="footer">
      <div className="wrap footer-in">
        <img src="/img/logo.svg" alt="[Nome da marca]" width="130" height="43" />
        <p>
          [@perfil] · <a href="#">Termos de uso</a> · <a href="#">Política de privacidade</a>
        </p>
        <p>{CNPJ ? `CNPJ ${CNPJ} · ` : ""}Todos os direitos reservados</p>
      </div>
    </footer>
  );
}
