from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@gmail.com",
            "phone": "9876543210",
            "password": "123456"
        }
    )

    assert response.status_code in [200, 201]


def test_login_user():

    response = client.post(
        "/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200