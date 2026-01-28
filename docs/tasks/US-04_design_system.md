# US-04: Design System

**História**: Como desenvolvedor, quero um design system consistente, para que todas as páginas tenham aparência e comportamento uniforme.

## Tarefas

### CSS Base
- [x] Criar `static/css/main.css` com:
  - [x] CSS Reset/Normalize
  - [x] Variáveis CSS (custom properties):
    - [x] Paleta de cores (cream, charcoal, gold-leaf)
    - [x] Tipografia (Lora serif, Inter sans-serif)
    - [x] Espaçamento (scale: xs, sm, md, lg, xl, 2xl, 3xl)
    - [x] Bordas e sombras (sm, md, lg, xl)
  - [x] Tipografia global:
    - [x] Import de Google Fonts (Lora + Inter)
    - [x] Definir hierarchy (h1-h6, p, etc.)
  - [x] Utilitários de layout:
    - [x] Container responsivo
    - [x] Grid system (tales-grid)
    - [x] Flexbox helpers (search-form)

### Componentes Reutilizáveis
- [x] Definir estilos para:
  - [x] `.card` - Cards de contos
  - [x] `.btn` - Botões (primary com hover effects)
  - [x] `.badge` - Tags/badges para classificações (3 variantes: primary, secondary, outline)
  - [x] `.search-input` - Campos de busca
  - [x] `.search-limit` - Dropdown de limite
  - [x] `.filter-group` - Grupos de checkboxes

### Template Base
- [x] Criar `xer/templates/base.html`:
  - [x] Estrutura HTML5 semântica
  - [x] `<head>` com:
    - [x] Meta tags (charset, viewport, description)
    - [x] Open Graph tags
    - [x] Link para CSS
  - [x] `<body>` com:
    - [x] Header/navbar
    - [x] `{% block content %}` para páginas
    - [x] Footer
  - [x] Link para JS (mínimo necessário)

### Responsividade
- [x] Definir breakpoints:
  - [x] Mobile: < 768px
  - [x] Tablet/Desktop: > 768px
- [x] Testar em diferentes viewports

### Acessibilidade
- [x] Garantir contraste WCAG AA
- [x] Estados de foco visíveis (gold border)
- [x] Semântica HTML correta

### Documentação
- [x] Criar `docs/design_system.md` com:
  - [x] Paleta de cores documentada
  - [x] Exemplos de componentes
  - [x] Guia de uso
