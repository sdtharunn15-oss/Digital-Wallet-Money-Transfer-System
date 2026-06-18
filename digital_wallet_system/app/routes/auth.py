from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import LoginRequest
from sqlalchemy.orm import Session
from fastapi import Request
from app.database import get_db
from app.utils.rate_limit import limiter
from app.models.user import User
from app.models.wallet import Wallet

from app.schemas.user import UserCreate

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.utils.logger import logger


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()


    if existing_user:
        return {
            "message": "User already exists"
        }


    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password)
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    wallet = Wallet(
        user_id=new_user.id,
        balance=0
    )


    db.add(wallet)
    db.commit()


    return {
        "message": "User registered successfully"
    }



@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    if not verify_password(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    token = create_access_token(
        {
            "user_id": user.id,
            "role": user.role
        }
    )


    return {
        "access_token": token,
        "token_type":"bearer"
    }