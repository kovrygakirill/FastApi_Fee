import pytest
from httpx import AsyncClient

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_sign_up(temp_db):
    request_data = {
        "email": "vader@deathstar.com",
        "name": "Darth Vader",
        "password": "rainbow"
    }
    with TestClient(app=app) as client:
        response = client.post("http://127.0.0.1:8000/sing_up/", json=request_data)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "vader@deathstar.com"
    assert response.json()["name"] == "Darth Vader"
    assert response.json()["token"]["expires"] is not None
    assert response.json()["token"]["access_token"] is not None


def test_sign_up_with_invalid_email(temp_db):
    request_data = {
        "email": "vader",
        "name": "Kirill",
        "password": "rmityu"
    }
    with TestClient(app) as client:
        response = client.post("/sing_up/", json=request_data)
    assert response.status_code == 422


def test_sign_up_with_exist_email(temp_db):
    request_data = {
        "email": "vader@deathstar.com",
        "name": "Kirill",
        "password": "rmityu"
    }
    with TestClient(app) as client:
        response = client.post("/sing_up/", json=request_data)
    assert response.status_code == 400
