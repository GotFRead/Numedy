from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from src.models import db_helper
from src.models import Product
from src.server_src.server.warehouse.schemas import ProductUpdate

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