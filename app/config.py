import sys
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Required secret for webhook signature validation
    WEBHOOK_SECRET: str

    # Database connection string (SQLite)
    DATABASE_URL: str = "sqlite:////data/app.db"

    # Logging level
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


# Load settings at import time
# If WEBHOOK_SECRET is missing, app should not start
try:
    settings = Settings()
except Exception:
    print("FATAL: WEBHOOK_SECRET is not set")
    sys.exit(1)
