"""Essential configuration settings."""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5405/postgres")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # IMAP Configuration
    IMAP_SERVER: str = os.getenv("IMAP_SERVER", "")
    IMAP_PORT: int = int(os.getenv("IMAP_PORT", "993"))
    IMAP_USERNAME: str = os.getenv("IMAP_USERNAME", "")
    IMAP_PASSWORD: str = os.getenv("IMAP_PASSWORD", "")
    IMAP_USE_SSL: bool = os.getenv("IMAP_USE_SSL", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
