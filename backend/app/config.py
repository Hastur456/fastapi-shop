from typing import List, Optional, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    app_name: str = "Shop"
    debug: bool = True
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000" 
    ]

    static_dir: str = "static"
    images_dir: str = "static/images"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    )

    def get_database_url_for_sqlite(self) -> str:
        return "sqlite:///./shop.db"


settings = Settings()
database_url = settings.get_database_url_for_sqlite()
