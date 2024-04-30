from os import getenv
from pydantic_settings import BaseSettings

import os

class Settings(BaseSettings):
    db_url: str = f"postgresql+asyncpg://postgres:1234@{os.getenv('DB_HOST', 'localhost')}:5432/numedy_test_task"
    db_echo: bool = False

setting = Settings()