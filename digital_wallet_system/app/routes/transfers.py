from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.models.wallet import Wallet
from app.models.transfer import Transfer
from app.models.transaction import Transaction
from app.models.user import User

from app.schemas.transfer import TransferRequest

from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"]
)


@router.post("/send")
def send_money(
    data: TransferRequest,
    db: Session = Depends(get_db)
):

    try:

        if data.sender_user_id == data.receiver_user_id:
            raise HTTPException(
                status_code=400,
                detail="Self transfer not allowed"
            )


        if data.amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )


        sender_wallet = db.query(Wallet).filter(
            Wallet.user_id == data.sender_user_id
        ).first()


        receiver_wallet = db.query(Wallet).filter(
            Wallet.user_id == data.receiver_user_id
        ).first()



        if not sender_wallet:

            raise HTTPException(
                status_code=404,
                detail="Sender wallet not found"
            )


        if not receiver_wallet:

            raise HTTPException(
                status_code=404,
                detail="Receiver wallet not found"
            )



        if sender_wallet.balance < data.amount:

            raise HTTPException(
                status_code=400,
                detail="Insufficient balance"
            )



        sender_wallet.balance -= data.amount

        receiver_wallet.balance += data.amount



        reference = str(uuid.uuid4())



        transfer = Transfer(

            sender_wallet_id=sender_wallet.id,

            receiver_wallet_id=receiver_wallet.id,

            amount=data.amount,

            transaction_reference=reference,

            status="Success"

        )


        db.add(transfer)



        db.add(
            Transaction(

                wallet_id=sender_wallet.id,

                transaction_type="Debit",

                amount=data.amount,

                status="Success"

            )
        )


        db.add(
            Transaction(

                wallet_id=receiver_wallet.id,

                transaction_type="Credit",

                amount=data.amount,

                status="Success"

            )
        )



        db.commit()

        db.refresh(transfer)



        return {

            "message":"Transfer successful",

            "transfer_id":transfer.id,

            "reference":reference

        }



    except HTTPException:

        raise



    except SQLAlchemyError:


        db.rollback()


        raise HTTPException(

            status_code=500,

            detail="Transfer failed and rolled back"

        )
@router.get("/all")
def get_all_transfers(
    db: Session = Depends(get_db)
):
    transfers = db.query(Transfer).all()

    return transfers
  




@router.get("/{transfer_id}")
def get_transfer(
    transfer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    transfer = db.query(Transfer).filter(
        Transfer.id == transfer_id
    ).first()


    if not transfer:
        raise HTTPException(
            status_code=404,
            detail="Transfer not found"
        )


    return transfer