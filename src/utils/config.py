"""Configuration management for the content planner application."""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    # Customer agent (default) configuration
    OLLAMA_API_KEY: str = os.getenv('OLLAMA_API_KEY', '')
    OLLAMA_MODEL: str = os.getenv('OLLAMA_MODEL', 'deepseek-v3.1:671b-cloud')
    OLLAMA_HOST: str = 'https://ollama.com'
    
    # Salesman agent configuration (optional, falls back to customer agent config)
    OLLAMA_API_KEY_SALESMAN: str = os.getenv('OLLAMA_API_KEY_SALESMAN', os.getenv('OLLAMA_API_KEY', ''))
    OLLAMA_MODEL_SALESMAN: str = os.getenv('OLLAMA_MODEL_SALESMAN', os.getenv('OLLAMA_MODEL', 'deepseek-v3.1:671b-cloud'))
    
    # Application settings
    MAX_QUESTIONS_PER_ROUND: int = int(os.getenv('MAX_QUESTIONS_PER_ROUND', '5'))
    CONTENT_IDEAS_PER_ROUND: int = int(os.getenv('CONTENT_IDEAS_PER_ROUND', '10'))
    AUTOSAVE_INTERVAL_SECONDS: int = int(os.getenv('AUTOSAVE_INTERVAL_SECONDS', '300'))
    
    # Output configuration
    OUTPUT_DIR: str = 'out'
    OUTPUT_FILE: str = 'out/content_ideas.json'
    CONTEXT_FILE: str = 'out/context.md'

    @classmethod
    def is_api_configured(cls) -> bool:
        """Check if the API key is configured."""
        return bool(cls.OLLAMA_API_KEY and cls.OLLAMA_API_KEY != 'your_api_key_here')
    
    @classmethod
    def is_salesman_api_configured(cls) -> bool:
        """Check if the salesman API key is configured."""
        return bool(cls.OLLAMA_API_KEY_SALESMAN and cls.OLLAMA_API_KEY_SALESMAN != 'your_api_key_here')
