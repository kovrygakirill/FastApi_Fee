import json

from main import app
from fastapi.testclient import TestClient
import pytest

from database_settings.db_init import database_testing

client = TestClient(app)


@pytest.fixture(scope="function")
def creating_data_in_db_for_test():
    users_data = [
        {
            "email": "kir@deathstar.com",
            "name": "Kolin Kow",
            "password": "sdcdscds"
        },
        {
            "email": "Vlad@mail.com",
            "name": "Vlad Rom",
            "password": "sdcdscdsc"
        }
    ]

    with TestClient(app) as client:
        for user_data in users_data:
            client.post("/sing_up/", json=user_data)


@pytest.fixture(scope="function")
def db_connect():
    conn = database_testing.connect()
    yield conn
    conn.close()


def test_user_get(temp_db, creating_data_in_db_for_test, db_connect):
    with TestClient(app) as client:
        user_id = 1
        response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "kir@deathstar.com"
    assert response.json()["name"] == "Kolin Kow"


def test_user_get_not_exist(temp_db, creating_data_in_db_for_test, db_connect):
    with TestClient(app) as client:
        user_id = 5
        response = client.get(f"/users/{user_id}")
    assert response.status_code == 400


def test_user_update(temp_db, creating_data_in_db_for_test, db_connect):
    with TestClient(app) as client:
        user_id = 1
        token = db_connect.execute(
            f"SELECT tokens.token FROM tokens JOIN users ON users.id = tokens.user_id WHERE users.id = {user_id};") \
            .fetchone()
        response = client.patch(
            f"/users/{user_id}",
            data=json.dumps({"name": "Kirill"}),
            headers={"Authorization": f"Bearer {token['token'].hex}"}
        )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "kir@deathstar.com"
    assert response.json()["name"] == "Kirill"


def test_user_update_without_data(temp_db, creating_data_in_db_for_test, db_connect):
    with TestClient(app) as client:
        user_id = 1
        token = db_connect.execute(
            f"SELECT tokens.token FROM tokens JOIN users ON users.id = tokens.user_id WHERE users.id = {user_id};") \
            .fetchone()
        response = client.patch(
            f"/users/{user_id}",
            data=json.dumps({}),
            headers={"Authorization": f"Bearer {token['token'].hex}"}
        )
    assert response.status_code == 400


def test_user_update_without_token(temp_db, creating_data_in_db_for_test, db_connect):
    with TestClient(app) as client:
        user_id = 1
        response = client.patch(
            f"/users/{user_id}",
            data=json.dumps({"name": "Kirill"}),
        )
    assert response.status_code == 401
