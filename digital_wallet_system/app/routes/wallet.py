from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import MoneyRequest
from app.database import get_db
from app.models.wallet import Wallet


router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


@router.get("/{user_id}")
def get_wallet(
    user_id: int,
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id
    ).first()


    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )


    return {
        "wallet_id": wallet.id,
        "user_id": wallet.user_id,
        "balance": wallet.balance
    }



@router.post("/add-money")
def add_money(
    data: MoneyRequest,
    db: Session = Depends(get_db)
):

    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )


    wallet = db.query(Wallet).filter(
        Wallet.user_id == data.user_id
    ).first()


    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )


    wallet.balance += data.amount


    transaction = Transaction(
        wallet_id=wallet.id,
        transaction_type="Credit",
        amount=data.amount,
        status="Success"
    )


    db.add(transaction)

    db.commit()


    return {
        "message": "Money added successfully",
        "balance": wallet.balance
    }




@router.post("/withdraw")
def withdraw_money(
    data: MoneyRequest,
    db: Session = Depends(get_db)
):

    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )


    wallet = db.query(Wallet).filter(
        Wallet.user_id == data.user_id
    ).first()


    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )


    if wallet.balance < data.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )


    wallet.balance -= data.amount


    transaction = Transaction(
        wallet_id=wallet.id,
        transaction_type="Debit",
        amount=data.amount,
        status="Success"
    )


    db.add(transaction)

    db.commit()


    return {
        "message": "Money withdrawn successfully",
        "balance": wallet.balance
    }




@router.get("/transactions/{user_id}")
def get_transactions(
    user_id: int,
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id
    ).first()


    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )


    transactions = db.query(Transaction).filter(
        Transaction.wallet_id == wallet.id
    ).all()


    return transactions




@router.get("/all")
def get_all_wallets(
    db: Session = Depends(get_db)
):

    return db.query(Wallet).all()