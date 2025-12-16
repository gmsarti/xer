# Xer - Explorador de Contos de Fadas

**Xer** é uma aplicação web para explorar e ler contos de fadas organizados por padrões narrativos. Desenvolvida com FastAPI + Jinja2 (SSR), segue a estética "Biblioteca Moderna" com suporte a dark mode manual.

---

## ✨ Features Implementadas

### 📖 Leitura de Contos
- Visualização de contos individuais com tipografia otimizada para leitura
- Drop cap decorativo no primeiro parágrafo
- Medida de texto ideal (~65 caracteres por linha)
- Navegação intuitiva

### 🔍 Busca Textual
- Busca por título e conteúdo completo
- Priorização de matches no título
- Dropdown de limite de resultados (3, 6, 15, 60, 120)
- Página de resultados com contador

### 🎨 Design System "Biblioteca Moderna"
- Paleta: Cream (#F5F1E8), Charcoal (#1A1C20), Gold-leaf (#B8860B)
- Tipografia: Lora (serif) + Inter (sans-serif)
- Componentes reutilizáveis: cards, buttons, badges, filter-groups
- Dark mode manual com toggle (🌙/☀️)
- Persistência de tema em localStorage
- Totalmente responsivo (mobile/desktop)

### ♿ Acessibilidade
- Contraste WCAG AA
- Estados de foco visíveis
- Semântica HTML (article, section, nav)
- ARIA labels em formulários

---

## 📦 Instalação

```bash
# Instalar uv (se ainda não tiver)
curl -LsSf https://astral.sh/uv/install.sh | sh
# ou via Homebrew
brew install uv

# Clonar e instalar dependências
git clone <repo-url>
cd xer
uv sync
```

---

## ⚙️ Configuração

Copie o arquivo de exemplo e edite conforme necessário:

```bash
cp .env.example .env
```

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `APP_NAME` | Nome da aplicação | `Xer` |
| `ENVIRONMENT` | Ambiente (`development`/`staging`/`production`) | `development` |
| `DATABASE_URL` | URL do banco SQLite | `sqlite:///./data/contos.sqlite` |
| `LOG_LEVEL` | Nível de log (`DEBUG`/`INFO`/`WARNING`/`ERROR`) | `INFO` |

As configurações são carregadas automaticamente via **pydantic-settings**.

---

## ▶️ Como Rodar

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

A aplicação estará disponível em: **http://localhost:8000**

### Endpoints Disponíveis

- **Homepage**: `/` - Explorar contos recentes
- **Busca**: `/search?q=termo&limit=60` - Buscar contos
- **Detalhes**: `/tales/{id}` - Ler conto específico
- **API Docs**: `/docs` - Documentação interativa (Swagger UI)

---

## 🗂️ Estrutura do Projeto

```
xer/
├── docs/                      # Documentação
│   ├── design_system.md       # Design system completo
│   ├── implementation_plan.md # Plano de implementação
│   ├── principles.md          # Princípios do projeto
│   ├── user_stories.md        # User stories
│   └── tasks/                 # Breakdowns de tarefas
├── static/
│   ├── css/
│   │   └── main.css          # CSS do design system
│   └── js/
│       └── theme-toggle.js   # Toggle dark/light mode
├── xer/
│   ├── api/
│   │   └── router.py         # Rotas FastAPI
│   ├── templates/
│   │   ├── base.html         # Template base
│   │   ├── index.html        # Homepage
│   │   ├── search.html       # Página de busca
│   │   └── tale.html         # Detalhe do conto
│   ├── config.py             # Configurações (Pydantic)
│   ├── database.py           # Operações SQL (context managers)
│   └── logger.py             # Logger configurado
├── main.py                   # Entry point FastAPI
└── pyproject.toml           # Dependências e configs
```

---

## 🧹 Linting & Formatting

```bash
# Lint
uv run taskipy lint

# Auto-format
uv run taskipy format
```

Configurado com **Ruff** (settings em `ruff.toml`).

---

## 🧪 Testing

```bash
uv run taskipy test   # executa pytest
```

---

## 📚 User Stories Implementadas

- ✅ **US-01**: Listar Contos - Homepage com grid de cards
- ✅ **US-02**: Buscar Contos - Busca textual com filtro de limite
- ✅ **US-03**: Ler Contos - Experiência de leitura otimizada
- ✅ **US-04**: Design System - Componentes e tema consistentes

Veja `docs/user_stories.md` para detalhes completos.

---

## 🎯 Princípios do Projeto

1. **UX Premium**: Design polido e atraente desde o início
2. **Arquitetura Pragmática**: SSR com Jinja2 (SEO + simplicidade)
3. **Pythonic Core**: Type hints, context managers, convenções modernas
4. **Resource Management**: Sempre usar `with` para recursos (DB, arquivos)
5. **Qualidade & Manutenibilidade**: Testes + documentação viva

Veja `docs/principles.md` para detalhes.

---

## 🚀 Próximos Passos

- [ ] US-05: Filtros por Classificação (Propp, Booker)
- [ ] Paginação para listagem de contos
- [ ] Cache de queries
- [ ] Testes de integração com `httpx`
- [ ] CI/CD com GitHub Actions
- [ ] Containerização (Docker + Docker Compose)

---

## 📄 Licença

MIT License - sinta-se livre para adaptar e estender.

---

**Desenvolvido com 🤎 usando FastAPI, Jinja2, e design premium.**
