from fastapi import Depends
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schemas import users
from utils.users import crud as users_utils
from utils.tokens import crud as tokens_utils
from utils.encryption_password import validate_password

router = APIRouter()


@router.post("/", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not validate_password(
            password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await tokens_utils.create_user_token(user_id=user["id"])
