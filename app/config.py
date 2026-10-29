from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Log Analyzer"
    environment: str = "local"
    database_url: str = "sqlite:///./ai_log_analyzer.db"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"
    llm_mode: str = "mock"
    log_level: str = "INFO"
    @model_validator(mode="after")
    def validate_llm(self) -> "Settings":
        if self.llm_mode not in {"mock", "openai"}:
            raise ValueError("LLM_MODE must be 'mock' or 'openai'")
        if self.llm_mode == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_MODE=openai")
        return self

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
