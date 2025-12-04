"""Configuration management for Agentic RAG eCommerce system."""

import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv


class LLMConfig(BaseModel):
    """LLM configuration settings."""

    model: str = "gpt-4"
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000


class VectorStoreConfig(BaseModel):
    """Vector store configuration settings."""

    collection_name: str = "products"
    persist_directory: Optional[str] = None


class AppConfig(BaseModel):
    """Main application configuration."""

    llm: LLMConfig = LLMConfig()
    vector_store: VectorStoreConfig = VectorStoreConfig()
    debug: bool = False


def load_config() -> AppConfig:
    """Load configuration from environment variables.

    Returns:
        AppConfig with settings from environment.
    """
    # Load .env file if present
    load_dotenv()

    return AppConfig(
        llm=LLMConfig(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
        ),
        vector_store=VectorStoreConfig(
            collection_name=os.getenv("CHROMA_COLLECTION", "products"),
            persist_directory=os.getenv("CHROMA_PERSIST_DIR"),
        ),
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )


def get_llm_config_for_autogen(config: AppConfig) -> dict:
    """Get LLM config in Autogen format.

    Args:
        config: Application configuration.

    Returns:
        Dictionary with Autogen-compatible LLM configuration.
    """
    return {
        "config_list": [
            {
                "model": config.llm.model,
                "api_key": config.llm.api_key,
            }
        ],
        "temperature": config.llm.temperature,
        "max_tokens": config.llm.max_tokens,
    }
