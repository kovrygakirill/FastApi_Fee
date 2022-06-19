from main import app
from fastapi.testclient import TestClient
import pytest

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


def test_auth(temp_db, creating_data_in_db_for_test):
    request_data = {"username": "kir@deathstar.com", "password": "sdcdscds"}
    with TestClient(app) as client:
        response = client.post("/auth/", data=request_data)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires"] is not None
    assert response.json()["access_token"] is not None


def test_auth_with_invalid_password(temp_db, creating_data_in_db_for_test):
    request_data = {"username": "kir@deathstar.com", "password": "121212"}
    with TestClient(app) as client:
        response = client.post("/auth/", data=request_data)
    assert response.status_code == 400


def test_auth_with_invalid_email(temp_db, creating_data_in_db_for_test):
    request_data = {"username": "kir@lol.com", "password": "sdcdscds"}
    with TestClient(app) as client:
        response = client.post("/auth/", data=request_data)
    assert response.status_code == 400
