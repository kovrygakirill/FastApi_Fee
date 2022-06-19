from datetime import datetime, timedelta
from models.tokens import tokens_table

from database_settings.db_init import database
from models.users import users_table


async def create_user_token(user_id: int):
    """ Создает токен для пользователя с указанным user_id """
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )
    return await database.fetch_one(query)


async def get_token_by_user_id(user_id: int):
    query = (
        tokens_table.join(users_table)
        .select(tokens_table.c.token)
        .where(users_table.c.id == user_id)
    )
    return await database.fetch_one(query)
