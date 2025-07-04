"""Essential configuration settings."""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    class Config:
        env_file = ".env"

settings = Settings()
