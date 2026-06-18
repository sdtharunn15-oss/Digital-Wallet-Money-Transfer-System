from fastapi import FastAPI
from app.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.wallet import router as wallet_router
import app.models
from app.routes.transfers import router as transfer_router
from app.routes.transactions import router as transaction_router
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.utils.rate_limit import limiter
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Digital Wallet System"
)
app.state.limiter = limiter


app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

from passlib.context import CryptContext
from jose import jwt

from datetime import datetime, timedelta

from dotenv import load_dotenv
import os


load_dotenv()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



SECRET_KEY = os.getenv(
    "SECRET_KEY"
)


ALGORITHM = os.getenv(
    "ALGORITHM"
)


EXPIRE_HOURS = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_HOURS",
        1
    )
)



def hash_password(password):

    return pwd_context.hash(password)




def verify_password(
    plain,
    hashed
):

    return pwd_context.verify(
        plain,
        hashed
    )




def create_access_token(data: dict):

    to_encode = data.copy()


    expire = (
        datetime.utcnow()
        +
        timedelta(
            hours=EXPIRE_HOURS
        )
    )


    to_encode.update(
        {
            "exp": expire
        }
    )


    return jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM

    )




def decode_token(token):

    try:

        return jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )


    except Exception:

        return None
    
app.include_router(auth_router)
app.include_router(wallet_router)
app.include_router(transfer_router)
app.include_router(transaction_router)
@app.get("/")
def home():
    return {"message": "Wallet API Running"}

