from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CRUD Server"
    database_file: Path = Field(default=Path("./data/db.json"))

    class Config:
        env_prefix = ""
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


