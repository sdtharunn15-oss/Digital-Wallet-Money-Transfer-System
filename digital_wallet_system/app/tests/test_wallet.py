from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_add_money():

    response = client.post(
        "/wallet/add-money",
        json={
            "user_id": 1,
            "amount": 1000
        }
    )

    assert response.status_code in [200, 201]


def test_get_wallet():

    response = client.get(
        "/wallet/1"
    )

    assert response.status_code == 200


def test_withdraw_money():

    response = client.post(
        "/wallet/withdraw",
        json={
            "user_id": 1,
            "amount": 200
        }
    )

    assert response.status_code == 200