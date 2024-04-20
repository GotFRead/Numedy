
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from . import actions
from . import schemas
from . import dependencies
from .broker_connector import BrokerConnector

from src.models.db_helper import db_helper
from src.models.product import Product 


import json

# __router__

router = APIRouter(prefix="/products")

# __service__

broker_connector = BrokerConnector()


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


@router.post('/', response_model=schemas.AddProductResponse)
async def create_product(
    product_in: schemas.Product,
    request: Request,
):
    client_id = f'{request.client.host}:{request.client.port}'
    product_json = json.loads(product_in.json())

    result = await broker_connector.add_product(
        client_id, 
        product_json['name'],
        product_json['weight'],
        product_json['id'],
    )

    return result['product_info']


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
    
    # TODO Получить Статус можно ли изменить продукт
    return await actions.update_product_partial(
        session=session,
        product=product_,
        product_update=product_in,
    )

@router.delete('/{product_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def update_product_partial(
    product_: Product = Depends(dependencies.get_product_via_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    
    # TODO Получить Статус можно ли изменить продукт
    
    await actions.delete_product(
        session=session,
        product=product_)

    return None