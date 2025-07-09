import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file safely
try:
    load_dotenv()
except (UnicodeDecodeError, FileNotFoundError) as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Using default environment settings.")

class Settings(BaseSettings):
    # API Keys - Read from environment variables
    deepseek_api_key: str = os.getenv('DEEPSEEK_API_KEY', '')
    deepseek_api_url: str = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/completions')
    
    # Database
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./technonews.db')
    
    # CORS - Support both string and list formats
    cors_origins: str = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins string to list."""
        return [origin.strip() for origin in self.cors_origins.split(',')]
    
    # Files
    feeds_file: str = os.getenv('FEEDS_FILE', 'feeds.json')
    
    # API Settings
    api_title: str = "Technonews Summarizer API"
    api_version: str = "1.0.0"
    
    # Security
    secret_key: str = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
    
    class Config:
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Validation: Critical settings must be present
def validate_settings():
    if not settings.deepseek_api_key:
        print("WARNING: DEEPSEEK_API_KEY environment variable is not set.")
        print("The /summarize endpoint will not work without this API key.")
        print("Please set DEEPSEEK_API_KEY as an environment variable or in .env file.")
    
    if settings.secret_key == 'your-secret-key-here-change-in-production':
        print("WARNING: Using default SECRET_KEY. Change this in production!")

# Auto-validate on import
validate_settings() 