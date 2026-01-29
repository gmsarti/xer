## ---------- Builder ---------- ##
FROM python:3.13-bookworm AS builder
# Instala compiladores e dependências de build
RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# Instala uv
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod 755 /install.sh && /install.sh && rm /install.sh
ENV PATH="/root/.local/bin:${PATH}"
WORKDIR /app
# Copia apenas o pyproject (cache de dependências)
COPY pyproject.toml .
# Instala todas as dependências de runtime (inclui uvicorn)
RUN uv sync
## ---------- Production ---------- ##
FROM python:3.13-slim-bookworm AS production
# Cria usuário não‑root
RUN useradd --create-home appuser
USER appuser
WORKDIR /app
# Copia código da aplicação e arquivos estáticos
COPY --chown=appuser:appuser xer/ xer/
COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser static/ static/
# Copia o virtual‑env gerado no builder
COPY --from=builder /app/.venv .venv
# Adiciona o virtual‑env ao PATH
ENV PATH="/app/.venv/bin:${PATH}"
# Porta da API
EXPOSE 8000
# Inicia a aplicação usando a porta definida por variável de ambiente (padrão Render)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]