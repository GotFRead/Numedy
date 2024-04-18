
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Product(Base):
    __tablename__ = "products"
    name: Mapped[str]
    weight: Mapped[int]