from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_wallets():

    client.post(
        "/auth/register",
        json={
            "name": "Sender",
            "email": "sender@gmail.com",
            "phone": "1111111111",
            "password": "123456"
        }
    )

    client.post(
        "/auth/register",
        json={
            "name": "Receiver",
            "email": "receiver@gmail.com",
            "phone": "2222222222",
            "password": "123456"
        }
    )

    client.post(
        "/wallet/add-money",
        json={
            "user_id": 1,
            "amount": 1000
        }
    )


def test_send_money():

    create_wallets()

    response = client.post(
        "/transfers/send",
        json={
            "sender_user_id": 1,
            "receiver_user_id": 2,
            "amount": 100
        }
    )

    assert response.status_code == 200


def test_get_all_transfers():

    response = client.get(
        "/transfers/all"
    )

    assert response.status_code == 200