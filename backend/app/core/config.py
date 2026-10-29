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

    # Database: Defaults to local SQLite if DATABASE_URL is not set in environment.
    # Supabase/Postgres can be enabled by setting SUPABASE_DATABASE_URL or DATABASE_URL.
    DATABASE_URL: str = "sqlite:///./resume_analyzer.db"
    SUPABASE_DATABASE_URL: str | None = None

    # Supabase project settings
    SUPABASE_URL: str | None = None
    SUPABASE_ANON_KEY: str | None = None
    SUPABASE_SERVICE_ROLE_KEY: str | None = None
    SUPABASE_JWT_SECRET: str | None = None

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
    def database_url(self) -> str:
        return self.SUPABASE_DATABASE_URL or self.DATABASE_URL

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }


settings = Settings()
