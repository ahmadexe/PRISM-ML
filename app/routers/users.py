from fastapi import APIRouter
from app.services.users import get_users

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return get_users();