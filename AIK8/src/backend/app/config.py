from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql://aik08_reader:reader_pw@localhost:5432/aik08"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    allowed_api_hosts: list[str] = Field(default_factory=lambda: ["api.example.org"])
    allowed_tools: list[str] = Field(default_factory=lambda: ["document_search", "http_get_api"])
    max_steps: int = Field(default=10, ge=1)
    max_tokens: int = Field(default=20_000, ge=1)
    max_seconds: int = Field(default=60, ge=1)
    frontend_origin: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()
