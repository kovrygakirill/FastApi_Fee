from fastapi import APIRouter

from api.endpoints import sing_up, auth, home, users

api_router = APIRouter()

api_router.include_router(home.router, tags=["home"])
api_router.include_router(sing_up.router, prefix="/sing_up", tags=["sing_up"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
