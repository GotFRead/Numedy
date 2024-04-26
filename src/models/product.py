
from .base import Base
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class Product(Base):
    __tablename__ = "products"
    name: Mapped[str]
    weight: Mapped[int]
    storage: Mapped[int] = mapped_column(ForeignKey("storage.id", ondelete='CASCADE')) 