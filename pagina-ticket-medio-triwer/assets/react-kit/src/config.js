// Tudo que muda sem mexer no layout fica aqui. Valores entre [COLCHETES] são pendências.

// Link do checkout (Hotmart, Kiwify, Eduzz...). Enquanto estiver "#oferta", os botões rolam até o preço.
export const CHECKOUT_URL = "#oferta";

// Link do WhatsApp da equipe. Formato: https://wa.me/55DDDNUMERO
export const WHATSAPP_URL = "#";

// CNPJ do rodapé. Vazio, a linha some.
export const CNPJ = "";

// Link do vídeo de vendas (VSL). Vazio, o hero mostra um player ilustrativo sem link.
export const VIDEO_URL = "";

// Preço. Só aparece no bloco de ancoragem (recapitulando + cartão de preço), nunca no topo, hero ou botões.
// O aluno define: parcelas, valor da parcela e valor à vista. A soma das parcelas só pode diferir do
// à vista se o checkout cobrar juros. Confirme com o checkout antes de publicar.
export const PRECO = "[297]";
export const PARCELAS = "12"; // número de parcelas
export const PARCELA = "[29,70]"; // valor de cada parcela, em destaque
export const PRECO_AVISTA = "[297,00]"; // valor à vista, pequeno embaixo
export const PRECO_DE = "[1.135]"; // soma dos valores de referência da lista "Recapitulando"

// Garantia, em dias. Vem do aluno, nunca de ficha ou briefing. Aparece em vários lugares da página.
export const GARANTIA_DIAS = "[7]";

// Depoimentos em vídeo ou print. Enquanto a lista estiver vazia, a seção não aparece.
// Formato: { nome, cargo, empresa, prazo, img: "/img/depoimentos/nome.webp" }
export const DEPOIMENTOS = [];

// Nomes de empresas ou clientes da trajetória do expert. Respeite a regra de confidencialidade dele.
export const EMPRESAS = ["[Empresa 1]", "[Empresa 2]", "[Empresa 3]"];

// Conta de custo (bloco "a conta que ninguém faz"): dois valores de mercado com fonte.
export const CUSTO_DE = 0; // [valor de hoje]
export const CUSTO_PARA = 0; // [valor do próximo degrau]
