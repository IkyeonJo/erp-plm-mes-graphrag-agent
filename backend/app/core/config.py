from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_LOG_LEVEL: str = "INFO"

    # --- LLM Provider ---
    LLM_PROVIDER: str = "gemini"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    LOCAL_LLM_BASE_URL: str = "http://localhost:8001/v1"
    LOCAL_LLM_API_KEY: str = "not-needed-for-local"
    LOCAL_LLM_MODEL: str = "qwen2.5-7b-instruct"

    # --- SQLite (synthetic ERP/PLM/MES) ---
    SQLITE_PATH: str = "./.cache/portfolio.db"

    # --- Neo4j ---
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j-password"
    NEO4J_DATABASE: str = "neo4j"

    # --- Synthetic data dir ---
    SYNTHETIC_DATA_DIR: str = "./data/synthetic"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def sqlite_url(self) -> str:
        path = Path(self.SQLITE_PATH).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{path}"


settings = Settings()
