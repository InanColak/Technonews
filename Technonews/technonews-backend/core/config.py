import os
from typing import List
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    deepseek_api_key: str = os.getenv('DEEPSEEK_API_KEY', '')
    deepseek_api_url: str = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/completions')
    
    # Database
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./technonews.db')
    
    # CORS
    cors_origins: List[str] = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Files
    feeds_file: str = os.getenv('FEEDS_FILE', 'feeds.json')
    
    # API Settings
    api_title: str = "Technonews Summarizer API"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Validation: Critical settings must be present
def validate_settings():
    if not settings.deepseek_api_key:
        raise RuntimeError("DEEPSEEK_API_KEY environment variable is not set. Please set it in your .env file.")

# Auto-validate on import
validate_settings() 