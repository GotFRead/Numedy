
import server.warehouse.prepare

from models.product import Product

from .schemas import ProductCreate
from .schemas import ProductUpdate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from sqlalchemy import select


def create_product(received_product: Product):
    user = received_product.model_dump()
    return {
        "success": True,
        "user": user
    }


def patch_product(received_product: Product):
    product = received_product.model_dump()
    return {
        "success": True,
        "product": product
    }


def get_product(received_product: Product):
    return {
        "success": True
    }


def delete_product(received_product: Product):
    return {
        "success": True
    }


async def get_products(session: AsyncSession) -> list[Product] | list:
    request = select(Product).order_by(Product.id)
    result: Result = await session.execute(request)
    products = result.scalars().all()  # (id, prod)
    return products


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh() # ? Needed
    return product


async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate) -> Product: 
    
    for name, value in product_update.model_dump().items():
        setattr(product, name, value)
    
    await session.commit()
    return product

async def update_product_partial(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate) -> Product: 
    
    for name, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, name, value)
    
    await session.commit()
    return product

async def put_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdate 
): 
    product_update.model_dump(exclude_unset=True)
    for name, value in product_update.model_dump().items():
        setattr(product, name, value)
    
    await session.commit()
    return product

async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    await session.delete(product)
    await session.commit()