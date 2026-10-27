import Hero from "./components/Hero.jsx";
import {
  Bonus,
  Contraste,
  Criador,
  Custo,
  Depoimentos,
  Etapas,
  FAQ,
  Fechamento,
  Footer,
  Garantia,
  Giant,
  Ident,
  Logos,
  Material,
  Nav,
  Oferta,
  OQueE,
  ParaQuem,
  Provas,
  Travas,
  Whats,
} from "./components/Sections.jsx";

const Gap = () => <div className="gap" />;

// Ordem de referência: hero, painéis escuros alternando com seções claras, etapas, bônus, preço, garantia, criador, FAQ.
export default function App() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <Logos />
        <Ident />
        <Gap />
        <Provas />
        <Giant />
        <Travas />
        <Gap />
        <OQueE />
        <Gap />
        <ParaQuem />
        <Contraste />
        <Depoimentos />
        <Etapas />
        <Material />
        <Bonus />
        <Oferta />
        <Custo />
        <Garantia />
        <Criador />
        <FAQ />
        <Fechamento />
        <Whats />
      </main>
      <Footer />
    </>
  );
}
