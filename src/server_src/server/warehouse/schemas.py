
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
    id: int
    name: str | None = None
    weight: int | None = None

class ProductRemove(ProductCreate):
    id: int 

class Response(BaseModel):
    pass

class AddProductResponse(BaseModel):
    id: int
    storage: int
    name: str
    weight: int

class DeleteProductResponse(BaseModel):
    id: int
    storage: int
    name: str
    weight: int
    status: str


class PatchProductResponse(BaseModel):
    id: int
    storage: int
    name: str
    weight: int
    status: str
