from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from src.models import db_helper
from src.models import Product
from src.models import Storage
from src.server_src.server.warehouse.schemas import ProductUpdate
from src.server_src.server.warehouse.schemas import StorageUpdate

async def get_product_via_id(
    product_id: int,
    session: AsyncSession
) -> Product:
    product = await get_product(
            session=session,
            product_id=product_id
        )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product id - {product_id} - NOT FOUND"
        )
    
    return product

async def get_product(session: AsyncSession, product_id: int):
    return await session.get(Product, product_id)


async def update_product_partial(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate) -> Product: 
    
    for name, value in product_update.items():
        setattr(product, name, value)
    
    await session.commit()
    return product



async def get_storage_via_id(
    id_: int,
    session: AsyncSession
) -> Storage:
    storage = await get_storage(
            session=session,
            product_id=id_
        )

    if storage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Storage id - {id_} - NOT FOUND"
        )
    
    return storage

async def get_storage(session: AsyncSession, product_id: int):
    return await session.get(Storage, product_id)


async def update_storage_partial(
        session: AsyncSession,
        storage: Storage,
        product_update: StorageUpdate) -> Storage: 
    
    for name, value in product_update.items():
        setattr(storage, name, value)
    
    await session.commit()
    return storage