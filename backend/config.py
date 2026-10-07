"""Centralized configuration for NetCore.

Loads settings from environment variables (via .env file or system env).
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "NetCore"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "sqlite:///./switches.db"
    # Auto-fix postgres:// → postgresql:// for Railway/Render etc.
    @property
    def database_url_safe(self) -> str:
        url = self.DATABASE_URL
        if url and url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    # SSH
    SSH_USERNAME: str = ""
    SSH_PASSWORD: str = ""
    SSH_TIMEOUT: int = 30

    # Security
    SECRET_KEY: str = ""

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    # Containerlab
    CLAB_DIR: str = "/etc/containerlab/lab"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "case_sensitive": True}


settings = Settings()


# Validate security-critical configuration
if not settings.SECRET_KEY:
    import warnings
    warnings.warn(
        "SECRET_KEY is not set. Set a strong SECRET_KEY in your .env file "
        "for production use.",
        RuntimeWarning,
        stacklevel=2,
    )

if not settings.OPENAI_API_KEY:
    import warnings
    warnings.warn(
        "OPENAI_API_KEY is not set. The AI agent functionality will not work "
        "without a valid OpenAI API key.",
        RuntimeWarning,
        stacklevel=2,
    )

if not settings.DATABASE_URL:
    import warnings
    warnings.warn(
        "DATABASE_URL is not set. Using default SQLite. "
        "For production, set a proper database connection string.",
        RuntimeWarning,
        stacklevel=2,
    )

# Add additional warnings for production
import warnings
if settings.DEBUG:
    warnings.warn(
        "DEBUG mode is enabled. Do not use in production.",
        RuntimeWarning,
        stacklevel=2,
    )
