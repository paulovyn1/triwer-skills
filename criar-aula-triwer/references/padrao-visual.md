# Padrão visual do material em HTML

Vale para aula gravada ou material do participante em HTML (etapa 7).

## Identidade do produto

Antes de gerar HTML, descubra a identidade visual do produto do expert: cores, fontes, logotipo, materiais já existentes (PDF, página de vendas, apresentação). Se existir referência, extraia paleta, tipografia e elementos recorrentes dela. Se não existir, pergunte a direção (cores, tom) em vez de inventar. Documente o que for decidido num arquivo da pasta do projeto do expert, para reaproveitar nas próximas aulas.

Estrutura que funciona bem para material de aula:
- Fundo claro quente, nunca branco puro
- Título de bloco em fonte serifada editorial
- Scroll vertical com navegação lateral fixa (um ponto por bloco), nunca navegação por slide
- Toggles (`<details>`) para tudo opcional ou pesado: exercícios, tabelas, checklist

## Bug conhecido: nunca esconder conteúdo via CSS esperando o JavaScript

Animação de "revelar ao rolar" que define `opacity: 0` no CSS como estado inicial faz elementos sumirem para sempre no iPhone e iPad, quando o `IntersectionObserver` não dispara a tempo.

**Regra:** todo elemento é visível por padrão no CSS. Animação de entrada só entra por classe adicionada via JavaScript. Se o JS falhar, o conteúdo aparece normal. Evite `position: fixed` em pseudo-elementos de textura cobrindo a tela; use `position: absolute` no body (com `body { position: relative }`).

Sempre teste em largura de celular antes de entregar.

## Bug conhecido: `<strong>` no meio de item de lista com `display: flex`

`li { display: flex; gap: 14px }` transforma cada filho do `<li>` em coluna. Um `<strong>` no meio da frase vira uma coluna isolada e quebra o alinhamento. Para posicionar uma seta antes do item, use:

```css
ul.points li {
  position: relative;
  padding-left: 28px;
  line-height: 1.65;
}

ul.points li::before {
  content: '→';
  position: absolute;
  left: 0;
  top: 0;
  font-weight: 700;
}
```
