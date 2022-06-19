from fastapi import APIRouter, Depends
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend

from database_settings.db_init import database, CACHE_HOST

router = APIRouter()


def redis_cache():
    return caches.get(CACHE_KEY)


@router.on_event("startup")
async def startup():
    rc = RedisCacheBackend(f'redis://{CACHE_HOST}:6379')
    if caches.get(CACHE_KEY):
        caches.remove(CACHE_KEY)
    caches.set(CACHE_KEY, rc)

    # когда приложение запускается устанавливаем соединение с БД
    try:
        await database.connect()
    except Exception:
        print("DATABASE DON'T CONNECT!!!")
        raise OSError


@router.on_event("shutdown")
async def shutdown():
    # когда приложение останавливается разрываем соединение с БД
    await database.disconnect()

    await redis_cache().flush()
    await close_caches()


@router.get("/")
async def read_home(cache: RedisCacheBackend = Depends(redis_cache)):
    in_cache = await cache.get('Hello')
    if not in_cache:
        await cache.set('Hello', 'Hello world')
        in_cache = 'Hello world'
    return in_cache
