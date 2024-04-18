from typing import Annotated

from annotated_types import MinLen
from annotated_types import MaxLen
from annotated_types import *

from pydantic import BaseModel
from pydantic import EmailStr


class CreateUser(BaseModel):
    login: Annotated[str, MinLen(2), MaxLen(30)]
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(30)]


class User(BaseModel):
    login: str
    email: EmailStr