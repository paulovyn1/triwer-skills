import { motion, useMotionValue, useSpring, useTransform } from "motion/react";

// Livro em 3D feito com CSS a partir da capa em imagem. Inclina com o cursor.
export default function BookMockup({ src, alt = "", size = 300, float = true, interactive = true, baseY = -24 }) {
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
    <div className="book-stage" style={{ "--bw": `${size}px` }} onPointerMove={onMove} onPointerLeave={onLeave}>
      <motion.div
        className="book-float"
        animate={float ? { y: [0, -14, 0] } : undefined}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
      >
        <motion.div className="book" style={{ rotateX: rx, rotateY: ry }}>
          <div className="book-pages" />
          <div className="book-back" />
          <div className="book-spine" />
          <div className="book-front">
            <img src={src} alt={alt} width="900" height="1440" />
            <span className="book-shine" />
          </div>
        </motion.div>
        <div className="book-shadow" />
      </motion.div>
    </div>
  );
}
