
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

# __products__


@router.post('/', response_model=schemas.AddProductResponse)
async def create_product(
    product_in: schemas.Product,
    request: Request,
):
    result = dict()
    client_id = f'{request.client.host}:{request.client.port}'
    product_json = json.loads(product_in.json())

    response = await broker_connector.add_product(
        client_id=client_id,
        product_name=product_json['name'],
        weight=product_json['weight'],
        storage=product_json['storage'],
        id_=product_json['id'],
    )
    result = response['product_info']
    result['status'] = response['status']

    return result


@router.put('/')
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


@router.patch('/')
async def update_product_partial(
    request: Request,
    product_: schemas.ProductUpdatePartial,
):
    client_id = f'{request.client.host}:{request.client.port}'
    product_json = json.loads(product_.json())

    response = await broker_connector.patch_product(
        client_id=client_id,
        product_name=product_json['name'],
        weight=product_json['weight'],
        id_=product_json['id'],
        storage=product_json['storage']
    )

    result = response['product_info']
    result['status'] = response['status']

    return result


@router.delete('/', response_model=schemas.DeleteProductResponse)
async def update_product_partial(
    request: Request,
    product_: schemas.ProductRemove,
) -> None:

    client_id = f'{request.client.host}:{request.client.port}'
    product_json = json.loads(product_.json())

    response = await broker_connector.delete_product(
        client_id,
        product_json['id'],
    )
    result = response['product_info']
    result['status'] = response['status']

    return result

# __storage__


@router.get('/storage/', response_model=list[schemas.Storage])
async def get_products(
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await actions.get_storage(session=session)


@router.post('/storage/', response_model=schemas.AddStorageResponse)
async def create_product_storage(
    product_in: schemas.Storage,
    request: Request,
):
    client_id = f'{request.client.host}:{request.client.port}'
    product_json = json.loads(product_in.json())

    response = await broker_connector.add_storage(
        client_id,
        product_json['address'],
        product_json['max_weight'],
        product_json['id'],
    )

    result = response['storage_info']
    result['status'] = response['status']

    return result


@router.put('/storage/')
async def update_product_storage(
    product_in: schemas.ProductUpdatePartial,
    product_: Product = Depends(dependencies.get_product_via_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await actions.patch_product(
        session=session,
        product=product_,
        product_update=product_in
    )


@router.patch('/storage/')
async def update_product_storage_partial(
    request: Request,
    product_: schemas.ProductUpdatePartial,
):
    client_id = f'{request.client.host}:{request.client.port}'
    product_json = json.loads(product_.json())

    response = await broker_connector.patch_storage(
        client_id=client_id,
        product_name=product_json['name'],
        weight=product_json['weight'],
        curr_weight=product_json['curr_weight'],
        id_=product_json['id'],
    )

    result = response['storage_info']
    result['status'] = response['status']

    return result


@router.delete('/storage/', response_model=schemas.DeleteStorageResponse)
async def delete_storage(
    request: Request,
    product_: schemas.ProductRemove,
) -> None:

    client_id = f'{request.client.host}:{request.client.port}'
    product_json = json.loads(product_.json())

    response = await broker_connector.delete_storage(
        client_id,
        product_json['id'],
    )
    result = response['storage_info']
    result['status'] = response['status']

    return result


@router.get('/search_product/{pattern}', response_model=schemas.SearchResponse)
async def search_product(
    request: Request,
    pattern: str,
) -> None:

    client_id = f'{request.client.host}:{request.client.port}'

    response = await broker_connector.search_product(
        client_id,
        pattern,
    )
    result = response['payload']
    result['status'] = response['status']
    return result


@router.get('/search_storage/{storage_address}', response_model=schemas.SearchResponse)
async def search_product(
    request: Request,
    storage_address: str,
) -> None:

    client_id = f'{request.client.host}:{request.client.port}'

    response = await broker_connector.search_storage(
        client_id,
        storage_address,
    )
    result = response['payload']
    result['status'] = response['status']
    return result
