"""Configuration management using pydantic-settings."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file.
    
    This class uses pydantic-settings to manage configuration with support for:
    - Environment variables
    - .env files
    - Type validation
    - Default values
    
    Example:
        >>> from xer.config import get_settings
        >>> settings = get_settings()
        >>> print(settings.app_name)
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application Settings
    app_name: str = Field(
        default="Xer",
        description="Nome da aplicação"
    )
    
    app_version: str = Field(
        default="0.1.0",
        description="Versão da aplicação"
    )
    
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Ambiente de execução"
    )
    
    debug: bool = Field(
        default=True,
        description="Modo debug ativado"
    )
    
    # API Settings
    api_host: str = Field(
        default="0.0.0.0",
        description="Host da API"
    )
    
    api_port: int = Field(
        default=8000,
        description="Porta da API",
        ge=1,
        le=65535
    )
    
    # Database Settings
    database_url: str = Field(
        default="sqlite:///./data/xer.db",
        description="URL de conexão com o banco de dados"
    )
    
    # LangChain/LangGraph Settings
    langchain_api_key: str | None = Field(
        default=None,
        description="API key para LangChain/LangSmith"
    )
    
    langchain_project: str = Field(
        default="xer",
        description="Nome do projeto no LangSmith"
    )
    
    langchain_tracing_v2: bool = Field(
        default=False,
        description="Ativar tracing do LangSmith"
    )
    
    # OpenAI Settings (se for usar)
    openai_api_key: str | None = Field(
        default=None,
        description="API key da OpenAI"
    )
    
    openai_model: str = Field(
        default="gpt-4",
        description="Modelo da OpenAI a ser usado"
    )
    
    # Logging Settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Nível de log"
    )
    
    log_file: Path | None = Field(
        default=None,
        description="Arquivo de log (opcional)"
    )
    
    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Valida o ambiente."""
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
    
    @property
    def is_development(self) -> bool:
        """Verifica se está em ambiente de desenvolvimento."""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção."""
        return self.environment == "production"
    
    def model_dump_safe(self) -> dict:
        """Retorna as configurações sem expor dados sensíveis."""
        data = self.model_dump()
        # Remove chaves sensíveis
        sensitive_keys = [
            "langchain_api_key",
            "openai_api_key",
            "database_url",
        ]
        for key in sensitive_keys:
            if key in data and data[key]:
                data[key] = "***HIDDEN***"
        return data


@lru_cache
def get_settings() -> Settings:
    """Retorna uma instância singleton das configurações.
    
    Esta função usa cache para garantir que as configurações sejam
    carregadas apenas uma vez durante a execução da aplicação.
    
    Returns:
        Settings: Instância das configurações da aplicação
    """
    return Settings()
