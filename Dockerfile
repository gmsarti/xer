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
# Instala bash para o entrypoint
RUN apt-get update && apt-get install --no-install-recommends -y \
        bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Cria usuário não‑root
RUN useradd --create-home appuser
WORKDIR /app

# Copia código da aplicação e arquivos estáticos
COPY --chown=appuser:appuser xer/ xer/
COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser static/ static/

# Copia o virtual‑env gerado no builder
COPY --from=builder /app/.venv .venv
# Adiciona o virtual‑env ao PATH
ENV PATH="/app/.venv/bin:${PATH}"

# Prepara dados iniciais (backup para volumes vazios)
COPY --chown=appuser:appuser data/ /app/data_initial/

# Prepara o entrypoint
COPY --chown=appuser:appuser scripts/entrypoint.sh /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh

# Garante permissões na pasta de dados (o volume será montado aqui)
RUN mkdir -p /app/data && chown appuser:appuser /app/data

USER appuser

# Porta da API
EXPOSE 8000

# Usa o script de entrypoint para inicializar o banco e subir a API
ENTRYPOINT ["/app/scripts/entrypoint.sh"]