
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.config import setting


class DataBaseHelper:
    def __init__(self, url: str = setting.db_url, echo = False) -> None:
        self.engine = create_async_engine(
            url=url, echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit= False
        )

db = DataBaseHelper(echo=True)