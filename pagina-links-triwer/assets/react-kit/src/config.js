// Todo o conteúdo da página fica aqui. Os componentes só leem.
// Link ainda sem destino: deixe "#". O botão aparece, mas clicar não faz nada.
// Negrito no texto: **assim**. Ícones disponíveis: veja `porNome` em components/icons.jsx.

export const PERFIL = {
  nome: "[Nome do expert]",
  rotulo: "[Nome do expert] · [O que ele é, em até 4 palavras]",
  // Frase de viés curta (até 7 palavras). As palavras dos índices em `faixa` ganham o marca-texto.
  frase: "[Frase curta que resume a visão dele]",
  faixa: [1, 2],
  foto: "/img/hero.webp",
  fotoAlt: "[Descrição da foto]",
  logo: "/img/logo.svg",
  logoAlt: "[Nome da marca]",
  tituloAba: "[Nome do expert] | [Marca ou profissão]",
};

// O card grande. Só um. É o que o expert mais quer que a pessoa clique agora.
export const DESTAQUE = {
  selo: "Lançamento",
  titulo: "[Nome do produto]",
  faixa: "", // palavra do fim do título que ganha a faixa (opcional, precisa ser a última)
  texto: "[Uma frase sobre o que a pessoa ganha]",
  cta: "[Verbo + objeto, ex.: Quero o meu livro]",
  href: "#",
  // tipo: "livro" (mockup 3D a partir da capa), "foto" (imagem em moldura) ou "nenhum"
  midia: { tipo: "livro", src: "/img/capa.webp", alt: "[Capa do produto]" },
};

// Cards médios, na ordem de prioridade. Ideal: 2 ou 3.
// tom: "escuro" ou "claro" (alterne para dar ritmo).
export const CARDS = [
  {
    titulo: "[Serviço ou produto 2]",
    texto: "[Uma frase com **o ganho** em negrito]",
    cta: "[Ex.: Falar no WhatsApp]",
    icone: "whatsapp",
    href: "#",
    img: "/img/card-1.webp",
    imgAlt: "[Descrição]",
    tom: "escuro",
  },
  {
    titulo: "[Conteúdo ou produto 3]",
    texto: "[Uma frase com **o ganho** em negrito]",
    cta: "[Ex.: Ler os artigos]",
    icone: "link",
    href: "#",
    img: "/img/card-2.webp",
    imgAlt: "[Descrição]",
    tom: "claro",
  },
];

// O material gratuito (isca). Se o expert não tiver, use `null` e o bloco some.
export const GRATUITO = {
  selo: "Gratuito",
  titulo: "[Nome do material]",
  texto: "[O que a pessoa descobre ou recebe]",
  cta: "[Ex.: Fazer o quiz agora]",
  href: "#",
  nota: "100% gratuito",
  // A tela animada vai marcando estes itens. Use o que o material REALMENTE cobre
  // (etapas, pilares, capítulos). Até 5 itens curtos.
  telaTitulo: "[Nome do material]",
  itens: ["[Item 1]", "[Item 2]", "[Item 3]", "[Item 4]"],
};

// Ícones redondos no topo e no menu, na ordem de importância.
export const REDES = [
  { nome: "Instagram", icone: "instagram", href: "#" },
  { nome: "LinkedIn", icone: "linkedin", href: "#" },
];

// Frase de fechamento do menu. **negrito** vira o marca-texto.
export const FRASE_MENU = "[Frase do expert com **um trecho** em destaque]";

export const RODAPE = "Todos os direitos reservados © [Nome do expert] · [Ano]";
