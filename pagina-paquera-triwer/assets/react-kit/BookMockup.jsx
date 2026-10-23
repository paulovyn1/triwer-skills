import { motion, useMotionValue, useSpring, useTransform } from "motion/react";

// Livro em 3D feito com CSS a partir da capa em imagem. Inclina com o cursor.
export default function BookMockup({ size = 300, float = true, interactive = true, baseY = -24, src = "/img/capa.webp", alt = "Capa do produto" }) {
  const mx = useMotionValue(0);
  const my = useMotionValue(0);
  const rx = useSpring(useTransform(my, [-0.5, 0.5], [10, -10]), { stiffness: 120, damping: 14 });
  const ry = useSpring(useTransform(mx, [-0.5, 0.5], [baseY - 14, baseY + 14]), { stiffness: 120, damping: 14 });

  const onMove = (e) => {
    if (!interactive) return;
    const r = e.currentTarget.getBoundingClientRect();
    mx.set((e.clientX - r.left) / r.width - 0.5);
    my.set((e.clientY - r.top) / r.height - 0.5);
  };
  const onLeave = () => {
    mx.set(0);
    my.set(0);
  };

  return (
    <div className="livro-palco" style={{ "--bw": `${size}px` }} onPointerMove={onMove} onPointerLeave={onLeave}>
      <motion.div
        className="livro-flutua"
        animate={float ? { y: [0, -14, 0] } : undefined}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
      >
        <motion.div className="livro" style={{ rotateX: rx, rotateY: ry }}>
          <div className="livro-paginas" />
          <div className="livro-verso" />
          <div className="livro-lombada" />
          <div className="livro-frente">
            <img src={src} alt={alt} width="900" height="1440" />
          </div>
        </motion.div>
        <div className="livro-sombra" />
      </motion.div>
    </div>
  );
}
