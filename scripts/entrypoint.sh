#!/bin/bash
set -e

# Caminhos definidos no Dockerfile e render.yaml
DATA_DIR="/app/data"
INITIAL_DATA_DIR="/app/data_initial"
DB_FILE="tales_db.sqlite"

echo "Verificando banco de dados em $DATA_DIR..."

# Se o arquivo do banco não existir no volume persistente, copia do backup inicial
if [ ! -f "$DATA_DIR/$DB_FILE" ]; then
    echo "Banco de dados não encontrado em $DATA_DIR. Inicializando a partir de $INITIAL_DATA_DIR..."
    mkdir -p "$DATA_DIR"
    cp "$INITIAL_DATA_DIR/$DB_FILE" "$DATA_DIR/$DB_FILE"
    echo "Banco de dados inicializado com sucesso."
else
    echo "Banco de dados já existe em $DATA_DIR. Pulando inicialização."
fi

# Executa o comando da aplicação (passando a porta dinâmica)
echo "Iniciando a API na porta ${PORT:-8000}..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
