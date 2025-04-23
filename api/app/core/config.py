# api/app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EquityLens"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://equitylens:equitylens_password@timescaledb:5432/equitylens_data"
    )
    CORS_ORIGINS: list = ["*"]  # In production, replace with specific origins
    
settings = Settings()