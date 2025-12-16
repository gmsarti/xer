# US-04: Design System

**História**: Como desenvolvedor, quero um design system consistente, para que todas as páginas tenham aparência e comportamento uniforme.

## Tarefas

### CSS Base
- [ ] Criar `static/css/main.css` com:
  - [ ] CSS Reset/Normalize
  - [ ] Variáveis CSS (custom properties):
    - [ ] Paleta de cores (primária, secundária, neutros)
    - [ ] Tipografia (family, sizes, weights)
    - [ ] Espaçamento (scale: 4px, 8px, 16px, 24px, etc.)
    - [ ] Bordas e sombras
  - [ ] Tipografia global:
    - [ ] Import de Google Fonts (Inter ou Outfit)
    - [ ] Definir hierarchy (h1-h6, p, etc.)
  - [ ] Utilitários de layout:
    - [ ] Container responsivo
    - [ ] Grid system
    - [ ] Flexbox helpers

### Componentes Reutilizáveis
- [ ] Definir estilos para:
  - [ ] `.card` - Cards de contos
  - [ ] `.btn` - Botões (primary, secondary)
  - [ ] `.badge` - Tags/badges para classificações
  - [ ] `.input` - Campos de busca
  - [ ] `.filter-group` - Grupos de checkboxes

### Template Base
- [ ] Criar `xer/templates/base.html`:
  - [ ] Estrutura HTML5 semântica
  - [ ] `<head>` com:
    - [ ] Meta tags (charset, viewport, description)
    - [ ] Open Graph tags
    - [ ] Link para CSS
  - [ ] `<body>` com:
    - [ ] Header/navbar (fixo ou não)
    - [ ] `{% block content %}` para páginas
    - [ ] Footer (opcional)
  - [ ] Link para JS (se necessário)

### Responsividade
- [ ] Definir breakpoints:
  - [ ] Mobile: < 768px
  - [ ] Tablet: 768px - 1024px
  - [ ] Desktop: > 1024px
- [ ] Testar em diferentes viewports

### Acessibilidade
- [ ] Garantir contraste WCAG AA
- [ ] Estados de foco visíveis
- [ ] Semântica HTML correta

### Documentação
- [ ] Criar `docs/design_system.md` (opcional) com:
  - [ ] Paleta de cores documentada
  - [ ] Exemplos de componentes
