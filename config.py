"""
Configuration settings for the FastGraph application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # LLM Configuration
    DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your environment or .env file.")
        
        # Validate model name - accept any model from .env
        valid_models = [
            "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini",
            "gpt-4o*", "gpt-4o-mini*", "gpt-4-turbo*", "gpt-3.5-turbo*"
        ]
        if cls.DEFAULT_LLM_MODEL not in valid_models:
            print(f"Warning: Model '{cls.DEFAULT_LLM_MODEL}' may not be valid. Using 'gpt-4o' instead.")
            cls.DEFAULT_LLM_MODEL = "gpt-4o" 