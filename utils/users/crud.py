from datetime import datetime
from sqlalchemy import and_
from database_settings.db_init import database

from models.users import users_table
from models.tokens import tokens_table
from schemas import users as user_schema
from utils.tokens import crud as tokens_utils
from utils.encryption_password import hash_password, get_random_string


async def get_all_users():
    query = users_table.select()
    return await database.fetch_all(query=query)


async def get_user_by_id(id_user: int):
    """ Возвращает информацию о пользователе """
    query = users_table.select().where(users_table.c.id == id_user)
    return await database.fetch_one(query=query)


async def get_user_by_email(email: str):
    """ Возвращает информацию о пользователе """
    query = users_table.select().where(users_table.c.email == email)
    return await database.fetch_one(query=query)


async def get_user_by_token(token: str):
    """ Возвращает информацию о владельце указанного токена """
    query = tokens_table.join(users_table).select().where(
        and_(
            tokens_table.c.token == token,
            tokens_table.c.expires > datetime.now()
        )
    )
    return await database.fetch_one(query=query)


async def create_user(user: user_schema.UserIn):
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        email=user.email, name=user.name, hashed_password=f"{salt}${hashed_password}"
    )
    user_id = await database.execute(query=query)
    token = await tokens_utils.create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}


async def update_user(id_user: int, data_user: dict):
    query = users_table.update().returning(users_table).where(users_table.c.id == id_user).values(**data_user)
    return await database.fetch_one(query=query)
