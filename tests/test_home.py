from fastapi.testclient import TestClient
from main import app


def test_read_home(temp_db):
    with TestClient(app=app) as ac:
        response = ac.get("http://127.0.0.1:8000")
    assert response.status_code == 200
    assert response.json() == "Hello world"
