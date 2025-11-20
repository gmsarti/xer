# Xer

**Xer** – a lightweight Python starter project that showcases the integration of FastAPI, LangChain, LangGraph, and Pydantic‑Settings. It includes a basic logger, linting/formatting with Ruff, task automation with Taskipy, and a test suite powered by Pytest.

---

## 📦 Installation

```bash
# Install the UV package manager (if you don't have it yet)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or via Homebrew
brew install uv

# Clone the repository and install dependencies
git clone <repo‑url>
cd xer
uv sync   # creates a .venv and installs all dependencies (including dev tools)
```

---

## ⚙️ Configuration

1. Copy the example environment file and edit the values you need:

```bash
cp .env.example .env
# edit .env with your preferred settings
```

| Variable | Description |
|----------|-------------|
| `APP_NAME` | Name of the application |
| `APP_VERSION` | Application version |
| `ENVIRONMENT` | `development` | `staging` | `production` |
| `DEBUG` | `true` | `false` |
| `API_HOST` | Host address for the FastAPI server |
| `API_PORT` | Port number for the FastAPI server |
| `DATABASE_URL` | Database connection URL (default SQLite) |
| `LOG_LEVEL` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |
| `LOG_FILE` | Optional path to a log file |
| `LANGCHAIN_API_KEY` | Optional LangChain/LangSmith API key |
| `OPENAI_API_KEY` | Optional OpenAI API key |

The values are loaded automatically by `xer.config.Settings` via **pydantic‑settings**.

---

## ▶️ Running the demo

```bash
uv run python main.py
```

You should see something like:

```
🚀 Xer v0.1.0
📦 Ambiente: development
🐛 Debug: True
🌐 API: http://0.0.0.0:8000
💾 Database: sqlite:///./data/xer.db
📝 Log Level: INFO

==================================================
Configurações (dados sensíveis ocultos):
==================================================
app_name: Xer
app_version: 0.1.0
environment: development
debug: True
api_host: 0.0.0.0
api_port: 8000
log_level: INFO
...
```

---

## 🪵 Logging

```python
from xer.logger import logger

logger.info("Application started")
logger.debug("Debug details")
```

The logger respects the `log_level` and, if `log_file` is set, writes rotating logs to the specified file (the directory is created automatically).

---

## 🧹 Lint & Formatting

```bash
# Lint the codebase
uv run taskipy lint

# Auto‑format the code
uv run taskipy format
```

Ruff is configured in `ruff.toml` (selecting a modest set of rules and ignoring line‑length warnings).

---

## 🧪 Testing

```bash
uv run taskipy test   # runs `pytest -q`
```

A minimal test suite lives in `tests/` and currently checks that the default logging level is `INFO` and that the logger instance reflects that level.

---

## 📚 API Documentation (Future)

When you add FastAPI routes, the automatic OpenAPI docs will be available at:

- Swagger UI: `http://localhost:<API_PORT>/docs`
- ReDoc: `http://localhost:<API_PORT>/redoc`

---

## 📈 Suggested Improvements (not yet implemented)

- CI/CD pipeline (GitHub Actions) running Ruff, formatting checks, and Pytest on every PR.
- Pre‑commit hooks (`pre‑commit` configuration) for lint/format before commits.
- Type checking with `mypy`/`pyright`.
- Dockerfile and Docker Compose for containerised development/deployment.
- Version bump automation (semantic‑release) and a `CHANGELOG.md`.
- Integration tests for FastAPI endpoints using `httpx`.
- Structured logging (JSON) with `loguru` or `structlog`.
- Observability via OpenTelemetry or Sentry.
- CLI entry‑point using `typer` for common tasks (run server, seed DB, migrations).
- Rotating file handler for logs (`RotatingFileHandler` or `TimedRotatingFileHandler`).
- Separate package layers (router → service → repository) for a clean architecture.
- Full documentation generation with `mkdocs` or `sphinx`.

---

## 📄 License

This project is provided under the MIT License. Feel free to adapt and extend it for your own needs.

---

*Generated on 2025‑11‑19.*
