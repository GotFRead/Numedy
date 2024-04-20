
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Users(Base):
    __tablename__ = "users"
    login: Mapped[str]
    password: Mapped[str]
    # role: Mapped[str]
