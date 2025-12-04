"""Tests for configuration management."""

import os
import pytest

from src.config import AppConfig, LLMConfig, VectorStoreConfig, load_config, get_llm_config_for_autogen


class TestLLMConfig:
    """Test cases for LLM configuration."""

    def test_default_values(self):
        """Test default LLM configuration values."""
        config = LLMConfig()
        assert config.model == "gpt-4"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
        assert config.api_key is None

    def test_custom_values(self):
        """Test custom LLM configuration values."""
        config = LLMConfig(
            model="gpt-3.5-turbo",
            api_key="test-key",
            temperature=0.5,
            max_tokens=1000,
        )
        assert config.model == "gpt-3.5-turbo"
        assert config.api_key == "test-key"
        assert config.temperature == 0.5


class TestVectorStoreConfig:
    """Test cases for vector store configuration."""

    def test_default_values(self):
        """Test default vector store configuration values."""
        config = VectorStoreConfig()
        assert config.collection_name == "products"
        assert config.persist_directory is None

    def test_custom_values(self):
        """Test custom vector store configuration values."""
        config = VectorStoreConfig(
            collection_name="custom_products",
            persist_directory="/tmp/chroma",
        )
        assert config.collection_name == "custom_products"
        assert config.persist_directory == "/tmp/chroma"


class TestAppConfig:
    """Test cases for application configuration."""

    def test_default_values(self):
        """Test default application configuration values."""
        config = AppConfig()
        assert config.debug is False
        assert isinstance(config.llm, LLMConfig)
        assert isinstance(config.vector_store, VectorStoreConfig)

    def test_get_llm_config_for_autogen(self):
        """Test converting config to Autogen format."""
        config = AppConfig(
            llm=LLMConfig(
                model="gpt-4",
                api_key="test-api-key",
                temperature=0.5,
                max_tokens=1500,
            )
        )
        autogen_config = get_llm_config_for_autogen(config)
        assert "config_list" in autogen_config
        assert len(autogen_config["config_list"]) == 1
        assert autogen_config["config_list"][0]["model"] == "gpt-4"
        assert autogen_config["config_list"][0]["api_key"] == "test-api-key"
        assert autogen_config["temperature"] == 0.5


class TestLoadConfig:
    """Test cases for loading configuration from environment."""

    def test_load_config_defaults(self, monkeypatch):
        """Test loading config with default values."""
        # Clear any existing env vars
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_MODEL", raising=False)

        config = load_config()
        assert config.llm.model == "gpt-4"
        assert config.debug is False

    def test_load_config_from_env(self, monkeypatch):
        """Test loading config from environment variables."""
        monkeypatch.setenv("OPENAI_API_KEY", "env-api-key")
        monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-turbo")
        monkeypatch.setenv("LLM_TEMPERATURE", "0.3")
        monkeypatch.setenv("DEBUG", "true")

        config = load_config()
        assert config.llm.api_key == "env-api-key"
        assert config.llm.model == "gpt-3.5-turbo"
        assert config.llm.temperature == 0.3
        assert config.debug is True
