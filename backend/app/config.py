from typing import List, Optional, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    app_name: str = "Shop"
    cors_origins: List[str]

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    ALGORITHM: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    )

    def get_database_url_for_postgress(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    def get_database_url_for_sqlite(self) -> str:
        return "sqllite:///./shop.db"


settings = Settings()
database_url = settings.get_database_url_for_postgress()
