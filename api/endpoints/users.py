from fastapi import APIRouter, HTTPException, Depends
from fastapi_cache.backends.redis import RedisCacheBackend
from typing import List
import json

from schemas import users as schema_users
from utils.users import crud as users_utils
from utils.users.dependecies_auth import get_current_user_by_token
from api.endpoints.home import redis_cache

router = APIRouter()


@router.get("/", response_model=List[schema_users.UserOut])
async def get_users():
    users = await users_utils.get_all_users()
    if not users:
        raise HTTPException(status_code=400, detail="There are no users")
    return users


@router.get("/{user_id}", response_model=schema_users.UserOut)
async def get_user(user_id: int, cache: RedisCacheBackend = Depends(redis_cache)):
    user = await cache.get(f'user_{user_id}')
    if not user:
        user = await users_utils.get_user_by_id(id_user=user_id)

        if not user:
            raise HTTPException(status_code=400, detail="The user doesn't exist")

        await cache.set(f'user_{user_id}', json.dumps(dict(user)))
        result = user
    else:
        result = json.loads(user)

    return result


@router.post("/", response_model=schema_users.User)
async def create_user(data_user: schema_users.UserIn):
    user_check = await users_utils.get_user_by_email(email=data_user.dict().get("email"))

    if user_check:
        raise HTTPException(status_code=400, detail="The user is already exist with this email")

    user = await users_utils.create_user(user=data_user)
    return user


@router.patch("/{user_id}", response_model=schema_users.UserOut)
async def update_user(user_id: int,
                      data_user: schema_users.UserUpdate,
                      user_by_token: schema_users.UserOut = Depends(get_current_user_by_token),
                      cache: RedisCacheBackend = Depends(redis_cache)):
    data_user = data_user.dict(exclude_unset=True)
    user = await users_utils.get_user_by_id(id_user=user_id)

    if not user:
        raise HTTPException(status_code=400, detail="User id is not exist!")
    if not data_user:
        raise HTTPException(status_code=400, detail="Not data for update!")
    if dict(user).get("email") != dict(user_by_token).get("email"):
        raise HTTPException(status_code=400, detail="Not valid token for this user id")

    user = await users_utils.update_user(id_user=user_id, data_user=data_user)
    await cache.delete(f'user_{user_id}')

    return user
