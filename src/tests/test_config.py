"""Tests for configuration module."""

import os
from utils.config import Config


def test_config_defaults():
    """Test default configuration values."""
    assert Config.OLLAMA_HOST == 'https://ollama.com'
    assert Config.MAX_QUESTIONS_PER_ROUND == 5
    assert Config.CONTENT_IDEAS_PER_ROUND == 10
    assert Config.AUTOSAVE_INTERVAL_SECONDS == 300
    assert Config.OUTPUT_FILE == 'out/content_ideas.json'
    assert Config.OUTPUT_DIR == 'out'
    assert Config.CONTEXT_FILE == 'out/context.md'


def test_config_api_check():
    """Test API configuration check."""
    # This will depend on environment
    result = Config.is_api_configured()
    assert isinstance(result, bool)


def test_config_model_default():
    """Test default model configuration."""
    if not os.getenv('OLLAMA_MODEL'):
        assert Config.OLLAMA_MODEL == 'deepseek-v3.1:671b-cloud'
