
from .schemas import CreateUser


def create_user(getted_user: CreateUser):
    user = getted_user.model_dump()
    return {
        "success": True,
        "user": user
    }