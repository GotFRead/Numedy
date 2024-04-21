from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Storage(Base):
    __tablename__ = "storage"
    address: Mapped[str]
    max_weight: Mapped[int]
    curr_weight: Mapped[int]