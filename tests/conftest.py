import os
import pytest

# Устанавливаем `os.environ`, чтобы использовать тестовую БД
os.environ['FAST_DB_TESTING'] = 'True'

from alembic import command
from alembic.config import Config

from sqlalchemy_utils import create_database, drop_database
from database_settings.db_init import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine


@pytest.fixture(scope="module")
def temp_db():
    try:
        create_database(SQLALCHEMY_DATABASE_URL)  # Создаем БД
    except Exception:
        pass

    base_dir = os.path.dirname(os.path.dirname(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))  # Загружаем конфигурацию alembic
    alembic_cfg.set_main_option("script_location", f'{base_dir}/migrations/')
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

    # for resolve error, when create table token(error -> 'uuid_generate_v4()')
    database = create_engine(SQLALCHEMY_DATABASE_URL)
    conn = database.connect()
    conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    conn.close()

    try:
        command.upgrade(alembic_cfg, "head")  # выполняем миграции
        yield SQLALCHEMY_DATABASE_URL
    finally:
        drop_database(SQLALCHEMY_DATABASE_URL)  # удаляем БД
