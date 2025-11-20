# Pydantic Settings Configuration Example

Este exemplo demonstra como usar as configurações do projeto.

## Uso Básico

```python
from xer.config import get_settings

# Obter as configurações (singleton)
settings = get_settings()

# Acessar valores
print(settings.app_name)
print(settings.environment)
print(settings.api_port)
```

## Variáveis de Ambiente

Você pode configurar o projeto através de variáveis de ambiente ou arquivo `.env`:

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```

2. Edite o arquivo `.env` com suas configurações

3. As configurações serão carregadas automaticamente

## Configurações Disponíveis

### Aplicação
- `APP_NAME`: Nome da aplicação
- `APP_VERSION`: Versão da aplicação
- `ENVIRONMENT`: Ambiente (development/staging/production)
- `DEBUG`: Modo debug (true/false)

### API
- `API_HOST`: Host da API (padrão: 0.0.0.0)
- `API_PORT`: Porta da API (padrão: 8000)

### Banco de Dados
- `DATABASE_URL`: URL de conexão com o banco

### LangChain/LangSmith
- `LANGCHAIN_API_KEY`: API key do LangSmith
- `LANGCHAIN_PROJECT`: Nome do projeto
- `LANGCHAIN_TRACING_V2`: Ativar tracing

### OpenAI
- `OPENAI_API_KEY`: API key da OpenAI
- `OPENAI_MODEL`: Modelo a ser usado

### Logging
- `LOG_LEVEL`: Nível de log (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- `LOG_FILE`: Arquivo de log (opcional)

## Exemplo com FastAPI

```python
from fastapi import FastAPI
from xer.config import get_settings

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

@app.get("/config")
def get_config():
    return settings.model_dump_safe()
```
