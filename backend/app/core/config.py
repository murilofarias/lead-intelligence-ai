"""Application configuration loaded from environment variables."""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings — all values are env-driven."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    fixture_mode: bool = Field(default=True, alias="FIXTURE_MODE")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-sonnet-4-5", alias="ANTHROPIC_MODEL")

    salesforce_username: str = Field(default="", alias="SALESFORCE_USERNAME")
    salesforce_password: str = Field(default="", alias="SALESFORCE_PASSWORD")
    salesforce_token: str = Field(default="", alias="SALESFORCE_TOKEN")

    cors_origins: str = Field(default="http://localhost:3000", alias="CORS_ORIGINS")
    rate_limit: str = Field(default="60/minute", alias="RATE_LIMIT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
