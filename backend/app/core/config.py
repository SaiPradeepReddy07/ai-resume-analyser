import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application Settings and Configuration.
    Reads from environment variables or .env file with safe defaults for local development.
    """
    PROJECT_NAME: str = "AI Resume Analyzer API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database: Defaults to local SQLite if DATABASE_URL is not set in environment
    DATABASE_URL: str = "sqlite:///./resume_analyzer.db"

    # JWT Authentication Settings
    JWT_SECRET_KEY: str = "super-secret-key-change-in-production-resume-analyzer-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS Settings
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"

    # File Upload Constraints
    MAX_FILE_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: str = ".pdf"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }


settings = Settings()
