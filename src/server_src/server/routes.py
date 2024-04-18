
# __prepare__

import server.prepare as prepare

# __fastapi_depend__

from fastapi import APIRouter
from fastapi import Request

from helpers.file_helper import get_static_file
# __router__

router = APIRouter(tags=["base"])

# __static__handler__

@router.get("/js/{item}")
async def get_static(item: str):
    return get_static_file(direction='js', filename=item)


@router.get("/img/{item}")
async def get_static(item: str):
    return get_static_file(direction='img', filename=item)


@router.get("/css/{item}")
async def get_static(item: str):
    return get_static_file(direction='css', filename=item)


@router.get("/")
async def get(request: Request):
    return get_static_file('pages', 'index.html')
