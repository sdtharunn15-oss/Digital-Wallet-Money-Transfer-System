Digital Wallet System

A backend wallet management system built using **FastAPI**, **SQLAlchemy**, and **JWT Authentication**.
The system supports user registration, login, wallet management, money transfer, and transaction history tracking.

Features

* User Registration
* User Login with JWT Authentication
* Secure Password Hashing
* Wallet Creation Automatically During Registration
* Add Money to Wallet
* Withdraw Money from Wallet
* Wallet Balance Checking
* Money Transfer Between Users
* Transfer History
* Transaction History
* API Documentation using Swagger UI
* Pytest API Testing
* Docker Support



Tech Stack

* Python 3.12+
* FastAPI
* SQLAlchemy
* SQLite / PostgreSQL
* Pydantic
* JWT Authentication
* Passlib (bcrypt)
* Pytest
* Docker



Project Structure


digital_wallet_system/

│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── wallet.py
│   │   ├── transaction.py
│   │   └── transfer.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── wallet.py
│   │   ├── transfers.py
│   │   └── transactions.py
│   │
│   ├── schemas/
│   │
│   ├── dependencies/
│   │
│   ├── utils/
│   │
│   └── tests/
│
├── requirements.txt
├── Dockerfile
└── README.md



Installation

Clone Project

bash
git clone <repository-url>


Go inside project:

bash
cd digital_wallet_system


Create Virtual Environment

bash
python -m venv venv


Activate:

Windows:

bash
venv\Scripts\activate



Install Dependencies

bash
pip install -r requirements.txt



Environment Variables

Create `.env` file:


SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=1




Run Application

Start FastAPI server:

bash
uvicorn app.main:app --reload


Application runs at:

http://127.0.0.1:8000


Swagger documentation:


http://127.0.0.1:8000/docs




API Flow

1. Register User

Endpoint:


POST /auth/register


Request:

json
{
 "name":"User",
 "email":"user@gmail.com",
 "phone":"9876543210",
 "password":"123456"
}


2. Login

Endpoint:

POST /auth/login


Request:

json
{
 "email":"user@gmail.com",
 "password":"123456"
}


Response:

json
{
 "access_token":"token",
 "token_type":"bearer"
}




3. Add Money

Endpoint:


POST /wallet/add-money


Request:

json
{
 "user_id":1,
 "amount":1000
}




4. Check Wallet Balance

Endpoint:


GET /wallet/{user_id}


Example:


GET /wallet/1




5. Transfer Money

Endpoint:


POST /transfers/send


Request:

json
{
 "sender_user_id":1,
 "receiver_user_id":2,
 "amount":100
}


Response:

json
{
 "message":"Transfer successful",
 "transfer_id":1,
 "reference":"xxxx"
}




6. Transfer History

Endpoint:


GET /transfers/all




7. Transaction History

Endpoint:

GET /wallet/transactions/{user_id}


Example:


GET /wallet/transactions/1



Database Schema

Users Table

| Column   | Type    |
| -------- | ------- |
| id       | Integer |
| name     | String  |
| email    | String  |
| phone    | String  |
| password | String  |
| role     | String  |



Wallets Table

| Column  | Type    |
| ------- | ------- |
| id      | Integer |
| user_id | Integer |
| balance | Float   |



Transactions Table

| Column           | Type     |
| ---------------- | -------- |
| id               | Integer  |
| wallet_id        | Integer  |
| transaction_type | String   |
| amount           | Float    |
| status           | String   |
| created_at       | DateTime |



Transfers Table

| Column                | Type    |
| --------------------- | ------- |
| id                    | Integer |
| sender_wallet_id      | Integer |
| receiver_wallet_id    | Integer |
| amount                | Float   |
| transaction_reference | String  |
| status                | String  |



Running Tests

Run:

bash
pytest


Expected:


7 passed




Docker

Build image:

bash
docker build -t digital-wallet-system .


Run container:

bash
docker run -p 8000:8000 digital-wallet-system


Author
Tharun
Digital Wallet System Backend Project
