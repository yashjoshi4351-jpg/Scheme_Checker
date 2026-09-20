from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# backend/app/
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Application-wide configuration.

    Values can be provided through environment variables.
    """

    # Application
    APP_NAME: str = "Government Scheme Eligibility Checker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'scheme_checker.db'}"

    # API
    API_PREFIX: str = "/api"

    # CORS
    ALLOW_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()