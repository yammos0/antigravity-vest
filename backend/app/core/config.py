import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Antigravity Unlock Engine"
    API_V1_STR: str = "/api/v1"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Database
    DUCKDB_PATH: str = "data/antigravity.db"

    # API Keys & Secrets
    BINANCE_API_KEY: Optional[str] = None
    BINANCE_SECRET: Optional[str] = None
    BYBIT_API_KEY: Optional[str] = None
    BYBIT_SECRET: Optional[str] = None
    OKX_API_KEY: Optional[str] = None
    OKX_SECRET: Optional[str] = None
    OKX_PASSPHRASE: Optional[str] = None

    TOKEN_UNLOCKS_API_KEY: Optional[str] = None
    MESSARI_API_KEY: Optional[str] = None
    CRYPTORANK_API_KEY: Optional[str] = None
    ALCHEMY_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
