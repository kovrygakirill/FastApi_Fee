from os import environ

import databases

# берем параметры CACHE из переменных окружения
CACHE_HOST = environ.get("FAST_CACHE_HOST", "localhost")

# берем параметры БД из переменных окружения
DB_USER = environ.get("FAST_DB_USER", "user")
DB_PASSWORD = environ.get("FAST_DB_PASS", "password")
DB_HOST = environ.get("FAST_DB_HOST", "localhost")
DB_PORT = environ.get("FAST_DB_PORT", "5432")
TESTING = environ.get("FAST_DB_TESTING", False)

if TESTING:
    DB_NAME = "test_fast_api"
else:
    DB_NAME = environ.get("FAST_DB_NAME", "test_fast_api")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print(f'DB_PATH ---- {SQLALCHEMY_DATABASE_URL}')
database = databases.Database(SQLALCHEMY_DATABASE_URL)


if TESTING:
    from sqlalchemy import create_engine
    database_testing = create_engine(SQLALCHEMY_DATABASE_URL)


# from sqlalchemy import create_engine
#
# database_ = create_engine(SQLALCHEMY_DATABASE_URL)
# conn = database_.connect()
# conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
# conn.close()
