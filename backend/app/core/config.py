from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://topshope:topshope123@localhost:5432/topshope"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TopShopE"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Scraping
    SCRAPING_DELAY: float = 1.0  # seconds between requests
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 30
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # External APIs
    SIMILARWEB_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 