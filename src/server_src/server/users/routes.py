
# __prepare__

import server.prepare as prepare

# __fastapi_depend__

from fastapi import APIRouter

from helpers.file_helper import get_static_file

from .actions import create_user
from .schemas import CreateUser

# __router__

router = APIRouter(prefix="/users", tags=["users"])

# __handlers__

@router.get("/login")
def login():
    return get_static_file('pages', 'login_page.html')

@router.post("/login")
def login(user: CreateUser):
    return create_user(user)