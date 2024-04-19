
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from . import actions
from . import schemas
from . import dependencies

from src.server_src.models import db_helper
from src.server_src.models import Product 


router = APIRouter(prefix="/products")


@router.get('/', response_model=list[schemas.Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.session_dependency)
    ):
    return await actions.get_products(session=session)


@router.get('/{product_id}', response_model=schemas.Product)
async def get_product(
    product_: Product = Depends(dependencies.get_product_via_id),
):
    return product_


@router.post('/', response_model=schemas.Product)
async def create_product(
    product_in: schemas.Product,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await actions.create_product(
        session=session,
        product_in=product_in
    )


@router.put('/{product_id}/')
async def update_product(
    product_in: schemas.ProductUpdatePartial,
    product_: Product = Depends(dependencies.get_product_via_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await actions.update_product(
        session=session,
        product=product_,
        product_update=product_in
    )


@router.patch('/{product_id}/')
async def update_product_partial(
    product_in: schemas.ProductUpdatePartial,
    product_: Product = Depends(dependencies.get_product_via_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await actions.update_product_partial(
        session=session,
        product=product_,
        product_update=product_in,
    )