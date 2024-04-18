from os import getenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:1234@localhost:5432/sqlalchemy"
    db_echo: bool = False

setting = Settings()