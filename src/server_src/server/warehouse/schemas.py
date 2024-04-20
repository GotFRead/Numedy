
from pydantic import BaseModel
from pydantic import ConfigDict


class ProductBase(BaseModel):
    name: str
    weight: int


class ProductCreate(BaseModel):
    pass


class ProductUpdate(ProductCreate):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    weight: int | None = None


class Response(BaseModel):
    pass

class AddProductResponse(BaseModel):
    id: int
    storage: int
    name: str
    weight: int
