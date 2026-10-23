const base = { fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round", strokeLinejoin: "round" };

export const Instagram = (p) => (
  <svg viewBox="0 0 24 24" width="18" height="18" {...p}>
    <rect x="3" y="3" width="18" height="18" rx="5" {...base} />
    <circle cx="12" cy="12" r="4" {...base} />
    <circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" />
  </svg>
);

export const Linkedin = (p) => (
  <svg viewBox="0 0 24 24" width="18" height="18" {...p}>
    <path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4v11H3zM9.5 9.75h3.8v1.5h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1v5.46h-4v-4.84c0-1.16-.02-2.64-1.61-2.64-1.61 0-1.86 1.26-1.86 2.56v4.92h-4z" />
  </svg>
);

export const Substack = (p) => (
  <svg viewBox="0 0 24 24" width="17" height="17" {...p}>
    <path fill="currentColor" d="M4 3h16v2.4H4zM4 7.6h16V10H4zM4 12.2h16V21l-8-4.5L4 21z" />
  </svg>
);

export const Whatsapp = (p) => (
  <svg viewBox="0 0 24 24" width="18" height="18" {...p}>
    <path {...base} d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4z" />
    <path {...base} strokeWidth="1.6" d="M9 8.6c.2-.5.5-.6.8-.6h.5c.2 0 .4.1.5.4l.7 1.6c.1.2 0 .5-.1.6l-.5.6c.6 1.2 1.6 2.1 2.8 2.7l.6-.6c.2-.2.4-.2.6-.1l1.6.7c.3.1.4.3.4.5v.5c0 .3-.2.7-.6.9-.7.4-1.6.4-2.7 0a9 9 0 0 1-4.7-4.6c-.4-1.1-.3-2 .1-2.6z" />
  </svg>
);

export const ArrowUpRight = (p) => (
  <svg viewBox="0 0 24 24" width="16" height="16" {...p}>
    <path {...base} strokeWidth="2" d="M7 17L17 7M9 7h8v8" />
  </svg>
);

export const ArrowRight = (p) => (
  <svg viewBox="0 0 24 24" width="18" height="18" {...p}>
    <path {...base} strokeWidth="2.2" d="M5 12h13M13 6l6 6-6 6" />
  </svg>
);

export const Grid = (p) => (
  <svg viewBox="0 0 24 24" width="20" height="20" {...p}>
    {[5, 12, 19].flatMap((x) => [5, 12, 19].map((y) => <circle key={`${x}${y}`} cx={x} cy={y} r="1.7" fill="currentColor" />))}
  </svg>
);

export const Share = (p) => (
  <svg viewBox="0 0 24 24" width="19" height="19" {...p}>
    <path {...base} d="M12 3v12M7.5 7.5L12 3l4.5 4.5M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6" />
  </svg>
);

export const Close = (p) => (
  <svg viewBox="0 0 24 24" width="20" height="20" {...p}>
    <path {...base} strokeWidth="2" d="M6 6l12 12M18 6L6 18" />
  </svg>
);

export const Chevron = (p) => (
  <svg viewBox="0 0 24 24" width="16" height="16" {...p}>
    <path {...base} strokeWidth="2" d="M6 9l6 6 6-6" />
  </svg>
);

export const Book = (p) => (
  <svg viewBox="0 0 24 24" width="19" height="19" {...p}>
    <path {...base} d="M4 4.5A1.5 1.5 0 0 1 5.5 3H20v15H5.5A1.5 1.5 0 0 0 4 19.5zM4 19.5A1.5 1.5 0 0 0 5.5 21H20M8 7h8" />
  </svg>
);

export const Compass = (p) => (
  <svg viewBox="0 0 24 24" width="19" height="19" {...p}>
    <circle cx="12" cy="12" r="9" {...base} />
    <path {...base} d="M15.5 8.5l-2 5-5 2 2-5z" />
  </svg>
);

export const Quiz = (p) => (
  <svg viewBox="0 0 24 24" width="19" height="19" {...p}>
    <rect x="4" y="3" width="16" height="18" rx="3" {...base} />
    <path {...base} d="M8 8.5l1.3 1.3L12 7.2M8 15l1.3 1.3 2.7-2.6M14.5 9h2M14.5 15.5h2" />
  </svg>
);

export const Check = (p) => (
  <svg viewBox="0 0 24 24" width="14" height="14" {...p}>
    <path {...base} strokeWidth="3" d="M5 12.5l4.5 4.5L19 7.5" />
  </svg>
);

export const Youtube = (p) => (
  <svg viewBox="0 0 24 24" width="19" height="19" {...p}>
    <rect x="2.5" y="5.5" width="19" height="13" rx="4" {...base} />
    <path fill="currentColor" d="M10 9.2v5.6l4.8-2.8z" />
  </svg>
);

export const Tiktok = (p) => (
  <svg viewBox="0 0 24 24" width="18" height="18" {...p}>
    <path {...base} d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5M14 3c.4 2.6 2.2 4.4 5 4.6" />
  </svg>
);

export const Globe = (p) => (
  <svg viewBox="0 0 24 24" width="18" height="18" {...p}>
    <circle cx="12" cy="12" r="9" {...base} />
    <path {...base} d="M3 12h18M12 3c2.5 2.6 3.7 5.6 3.7 9s-1.2 6.4-3.7 9c-2.5-2.6-3.7-5.6-3.7-9S9.5 5.6 12 3z" />
  </svg>
);

export const Mail = (p) => (
  <svg viewBox="0 0 24 24" width="18" height="18" {...p}>
    <rect x="3" y="5" width="18" height="14" rx="3" {...base} />
    <path {...base} d="M4 7l8 6 8-6" />
  </svg>
);

export const Link = (p) => (
  <svg viewBox="0 0 24 24" width="18" height="18" {...p}>
    <path {...base} d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" />
  </svg>
);

// Nome usado no config.js -> componente.
export const porNome = {
  instagram: Instagram, linkedin: Linkedin, substack: Substack, whatsapp: Whatsapp, youtube: Youtube,
  tiktok: Tiktok, site: Globe, email: Mail, link: Link, livro: Book, mentoria: Compass, quiz: Quiz,
};
