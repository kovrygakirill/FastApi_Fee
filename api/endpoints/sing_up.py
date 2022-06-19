from fastapi import APIRouter, HTTPException
from schemas import users
from utils.users import crud as users_utils

router = APIRouter()


@router.post("/", response_model=users.User)
async def create_user(user: users.UserIn):
    db_user = await users_utils.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users_utils.create_user(user=user)
