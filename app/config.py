"""Application settings, loaded from environment variables / .env.

Uses pydantic-settings so configuration is typed and validated. When
``azure_openai_endpoint`` is empty the app runs in deterministic MOCK mode,
which keeps the project runnable for learning without any Azure resources.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    app_env: str = "local"
    app_name: str = "azure-agentic-ai-masterclass"
    log_level: str = "INFO"

    # Azure OpenAI / Foundry
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment: str = "gpt-4o"
    azure_openai_api_version: str = "2024-10-21"

    # Grounding / state (later weeks)
    azure_ai_search_endpoint: str = ""
    azure_ai_search_key: str = ""
    cosmos_connection_string: str = ""
    redis_connection_string: str = ""

    # Identity / security (later weeks)
    azure_tenant_id: str = ""
    azure_client_id: str = ""
    key_vault_uri: str = ""

    @property
    def use_azure_openai(self) -> bool:
        """True when real Azure OpenAI calls should be attempted."""
        return bool(self.azure_openai_endpoint and self.azure_openai_api_key)


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
