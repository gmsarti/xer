# Tech Stack

Este documento descreve as tecnologias utilizadas no projeto e aquelas que ainda precisam ser definidas.

## Core & Backend
- **Linguagem**: Python 3.13
- **Gerenciador de Pacotes**: [uv](https://github.com/astral-sh/uv)
- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server**: Uvicorn
- **Configuração**: Pydantic Settings

## Frontend
- **Template Engine**: Jinja2 (Server-side rendering)
- **Estilização**: CSS Vanilla / Tailwind (a definir)

## AI & Data Engineering
- **Orquestração LLM**: LangChain & LangGraph
- **Modelos**: Integração via `langchain-openai`
- **Manipulação de Dados**: Pandas
- **Web Scraping**: BeautifulSoup4

## Qualidade & Tooling
- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff)
- **Testes**: Pytest (com `pytest-cov` para cobertura)
- **Task Runner**: [Taskipy](https://github.com/taskipy/taskipy)

## Infraestrutura
- **Containerização**: Docker (Multi-stage build)
- **Banco de Dados Atual**: SQLite (Arquivo local `xer.db`)

---

## 🚧 A Definir / Melhorias Futuras

As seguintes áreas ainda precisam de definição ou decisão arquitetural:

### Infraestrutura & Deploy
- [ ] **CI/CD**: Definir pipeline (ex: GitHub Actions) para rodar testes e linter em PRs.
- [ ] **Banco de Dados de Produção**: Decidir se SQLite será mantido ou migrar para PostgreSQL/outro.
- [ ] **Estratégia de Deploy**: Definir onde e como a aplicação será hospedada (AWS, GCP, VPS, etc.).

### Desenvolvimento & Qualidade
- [ ] **Type Checking**: Adotar `mypy` ou `pyright` no pipeline de verificação?
- [ ] **Pre-commit hooks**: Configurar hooks para rodar ruff antes de commits?
- [ ] **Documentação de API**: Melhorar descrições e exemplos no Swagger/OpenAPI gerado.

### Observabilidade
- [ ] **Logs Estruturados**: Implementar JSON logs (ex: structlog) para melhor ingestão em ferramentas de monitoramento.
- [ ] **Tracing/Metrics**: Definir ferramenta de observabilidade (Sentry, OpenTelemetry, etc.).

### Arquitetura da Aplicação
- [ ] **Autenticação/Autorização**: Definir estratégia se houver necessidade de usuários (JWT, OAuth2, etc.).
