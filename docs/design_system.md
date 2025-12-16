# Design System - Xer

Este documento apresenta o design system do projeto Xer, seguindo a estética "Biblioteca Moderna" com tema claro/escuro.

## Paleta de Cores

### Cores Principais (Light Mode)

| Nome | Hex | Uso |
|------|-----|-----|
| `--color-bg` | `#F5F1E8` (cream) | Fundo principal |
| `--color-surface` | `#EAE7DC` (off-white) | Superfícies (cards) |
| `--color-text` | `#2C2A2A` (dark-gray) | Texto principal |
| `--color-text-muted` | `#706C68` | Texto secundário |
| `--color-gold` | `#B8860B` (gold-leaf) | Acentos e CTAs |
| `--color-gold-hover` | `#A0740A` | Hover state |

### Dark Mode (Manual Toggle)

| Nome | Hex | Uso |
|------|-----|-----|
| `--color-bg` | `#1A1C20` (charcoal) | Fundo principal |
| `--color-surface` | `#2C2A2A` | Superfícies (cards) |
| `--color-text` | `#EAE7DC` (off-white) | Texto principal |
| `--color-text-muted` | `#A8A4A0` | Texto secundário |

> **Nota:** O dark mode é controlado manualmente via botão de toggle no header (🌙/☀️). A preferência é salva no localStorage e persiste entre sessões. O tema é aplicado via atributo `data-theme="dark"` no elemento `<html>`.

## Tipografia

### Famílias de Fonte

```css
--font-serif: 'Lora', 'Georgia', serif;
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

- **Lora (Serif)**: Usado para títulos, conteúdo de leitura, preview de contos
- **Inter (Sans-serif)**: Usado para UI, botões, navegação, labels

### Hierarquia Tipográfica

| Elemento | Família | Tamanho | Uso |
|----------|---------|---------|-----|
| `.hero-title` | Lora | 2.5rem | Título principal homepage |
| `.card-title` | Lora | 1.5rem | Títulos de cards |
| `.tale-title` | Lora | 2.5rem | Título do conto |
| `.tale-paragraph` | Lora | 1.1875rem (19px) | Texto de leitura |
| Body | Inter | 1rem (16px) | Texto padrão |

## Espaçamento

Scale baseado em múltiplos de 4px:

```css
--space-xs: 0.25rem;  /* 4px */
--space-sm: 0.5rem;   /* 8px */
--space-md: 1rem;     /* 16px */
--space-lg: 1.5rem;   /* 24px */
--space-xl: 2rem;     /* 32px */
--space-2xl: 3rem;    /* 48px */
--space-3xl: 4rem;    /* 64px */
```

## Border Radius

```css
--radius-sm: 0.375rem;  /* 6px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 0.75rem;   /* 12px */
--radius-xl: 1rem;      /* 16px */
```

## Sombras

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.15);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
```

## Transições

```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
```

---

## Componentes

### Card (`.card`)

Container para contos com hover effects.

**Estrutura:**
```html
<article class="card">
    <div class="card-content">
        <h3 class="card-title">Título do Conto</h3>
        <p class="card-preview">Preview do texto...</p>
    </div>
    <div class="card-footer">
        <a href="/tales/123" class="btn btn-primary">Ler Conto</a>
    </div>
</article>
```

**Características:**
- Hover: `translateY(-4px)` + borda dourada
- Padding: `var(--space-xl)`
- Border radius: `var(--radius-lg)`
- Sombra elevada no hover

### Button (`.btn`)

**Variantes:**
- `.btn-primary` - Botão principal com fundo dourado

```html
<button class="btn btn-primary">Buscar</button>
<a href="/" class="btn btn-primary">Voltar</a>
```

**Características:**
- Hover: `scale(1.05)` + sombra aumentada
- Font weight: 600
- Padding: `var(--space-sm) var(--space-lg)`

### Badge (`.badge`)

Tags para classificações narrativas.

**Variantes:**

```html
<!-- Primary (dourado) -->
<span class="badge badge-primary">Protagonista</span>

<!-- Secondary (neutro) -->
<span class="badge badge-secondary">Estrutura</span>

<!-- Outline -->
<span class="badge badge-outline">Booker</span>
```

**Características:**
- Font size: 0.75rem
- Text transform: uppercase
- Letter spacing: 0.05em

### Filter Group (`.filter-group`)

Grupos de checkboxes para filtros.

**Estrutura:**
```html
<div class="filter-group">
    <h4 class="filter-group-title">Personagens de Propp</h4>
    <label class="filter-option">
        <input type="checkbox" class="filter-checkbox" name="char" value="hero">
        <span class="filter-label">Herói</span>
    </label>
    <label class="filter-option">
        <input type="checkbox" class="filter-checkbox" name="char" value="villain">
        <span class="filter-label">Vilão</span>
    </label>
</div>
```

**Características:**
- Checkbox com `accent-color: var(--color-gold)`
- Hover: borda dourada nos checkboxes e labels
- Size: 18x18px

### Dark Mode Toggle (`.theme-toggle`)

Botão para alternar entre tema claro e escuro.

**Estrutura:**
```html
<button id="theme-toggle" class="theme-toggle" aria-label="Mudar para modo escuro">
    🌙
</button>
```

**Comportamento:**
- Ícone muda automaticamente: 🌙 (light) → ☀️ (dark)
- Preferência salva em `localStorage` (`xer-theme`)
- Tema aplicado via `data-theme` attribute no `<html>`
- JavaScript: `/static/js/theme-toggle.js`

**Características:**
- Size: 40x40px
- Border: 2px com hover effect dourado
- Transform: `scale(1.1)` no hover
- Focus: anel dourado com box-shadow

**Implementação:**

O tema é controlado por JavaScript que:
1. Lê preferência do localStorage (`xer-theme`)
2. Aplica `data-theme="dark"` ou `data-theme="light"` no `<html>`
3. CSS reage ao atributo via `[data-theme="dark"]` seletores
4. Salva preferência ao alternar

### Search Form (`.search-form`)

**Estrutura:**
```html
<form action="/search" method="get" class="search-form">
    <input type="text" name="q" class="search-input" placeholder="Buscar contos...">
    <select name="limit" class="search-limit">
        <option value="60">60</option>
    </select>
    <button type="submit" class="btn btn-primary">Buscar</button>
</form>
```

**Características:**
- Layout: flexbox com gap
- Input flex: 1 (ocupa espaço disponível)
- Focus state: borda dourada

### Layout Container (`.container`)

Wrapper responsivo para conteúdo.

```html
<div class="container">
    <!-- Conteúdo -->
</div>
```

**Características:**
- Max-width: 1200px
- Padding horizontal: `var(--space-lg)`
- Centralizado: `margin: 0 auto`

### Tales Grid (`.tales-grid`)

Grid responsivo para cards de contos.

```html
<div class="tales-grid">
    <article class="card">...</article>
    <article class="card">...</article>
    <!-- ... -->
</div>
```

**Características:**
- `display: grid`
- `grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))`
- Gap: `var(--space-xl)`
- Responsivo: 1 coluna em mobile

---

## Responsividade

### Breakpoints

- **Mobile**: `< 768px`
- **Desktop**: `≥ 768px`

### Mobile Adjustments

```css
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .tales-grid { grid-template-columns: 1fr; }
    .tale-paragraph { font-size: 1.0625rem; text-align: left; }
}
```

---

## Acessibilidade

### Contraste

Todas as combinações de cores atendem **WCAG AA**:
- Texto principal sobre fundo: ≥ 4.5:1
- Texto grande sobre fundo: ≥ 3:1

### Estados de Foco

Todos elementos interativos têm:
```css
:focus {
    outline: none;
    border-color: var(--color-gold);
}
```

### Semântica HTML

- `<article>` para cards de contos
- `<section>` para áreas temáticas
- `<nav>` para navegação
- ARIA labels em formulários: `aria-label="Buscar contos"`

---

## Uso

Para aplicar o design system, inclua o CSS principal:

```html
<link rel="stylesheet" href="/static/css/main.css">
```

E as fontes do Google:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
```

Todos os componentes usam CSS Variables para fácil manutenção e tematização automática dark/light mode.
