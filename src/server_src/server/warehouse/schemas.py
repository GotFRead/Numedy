
from pydantic import BaseModel
from pydantic import ConfigDict


class ProductBase(BaseModel):
    name: str
    weight: int
    storage: int

class ProductStorageBase(BaseModel):
    address: str
    max_weight: int
    id: int

class Storage(ProductStorageBase):
    pass

class StorageCreate(ProductStorageBase):
    pass

class StorageUpdate(StorageCreate):
    pass



class ProductCreate(BaseModel):
    pass


class ProductUpdate(ProductCreate):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = -1


class ProductUpdatePartial(ProductCreate):
    id: int
    name: str | None = None
    weight: int | None = None
    curr_weight: int | None = None
    storage: int | None = -1


class ProductRemove(ProductCreate):
    id: int


class Response(BaseModel):
    pass


class AddProductResponse(BaseModel):
    id: int = -1
    storage: int
    name: str
    weight: int
    status: str


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


class AddStorageResponse(BaseModel):
    id: int
    address: str
    max_weight: int
    curr_weight: int
    status: str

class DeleteStorageResponse(BaseModel):
    id: int
    address: str
    max_weight: int
    curr_weight: int
    status: str

class PatchStorageResponse(BaseModel):
    id: int
    address: str
    max_weight: int
    curr_weight: int
    status: str

class SearchResponse(BaseModel):
    founded_objects: list
    status: str

class SearchRequest(BaseModel):
    pattern: str