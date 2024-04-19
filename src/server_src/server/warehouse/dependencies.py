

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from src.server_src.models import db_helper
from src.server_src.models import Product

from . import actions

async def get_product_via_id(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Product:
    product = await actions.get_product(
            session=session,
            product_id=product_id
        )


    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product id - {product_id} - NOT FOUND"
        )
    
    return product
