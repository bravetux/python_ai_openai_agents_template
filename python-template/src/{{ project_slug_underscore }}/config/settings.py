"""Application settings loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the agent."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    llm_provider: Literal["anthropic", "bedrock", "openai"] = "anthropic"

    anthropic_api_key: str | None = None
    model_id: str = "claude-sonnet-4-6"

    aws_region: str = "us-east-1"
    aws_profile: str | None = None
    bedrock_model_id: str = "anthropic.claude-sonnet-4-6-v1:0"

    openai_api_key: str | None = None
    openai_model_id: str = "gpt-4o-mini"

    max_tokens: int = Field(default=2048, ge=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return a cached `Settings` instance."""
    return Settings()
