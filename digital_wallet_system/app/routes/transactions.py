from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db

from app.models.transaction import Transaction
from app.models.user import User

from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("/")
def get_transactions(

    type: str = None,
    status: str = None,
    date_filter: date = None,

    page: int = 1,
    limit: int = 10,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    query = db.query(Transaction)


    # USER -> only own transactions
    # ADMIN -> all transactions

    if current_user.role != "Admin":

        query = query.join(
            Transaction.wallet
        ).filter(
            Transaction.wallet.has(
                user_id=current_user.id
            )
        )


    if type:

        query = query.filter(
            Transaction.transaction_type == type
        )


    if status:

        query = query.filter(
            Transaction.status == status
        )


    if date_filter:

        query = query.filter(
            Transaction.created_at >= date_filter
        )


    total_records = query.count()


    transactions = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )


    total_pages = (
        total_records + limit - 1
    ) // limit


    return {

        "total_records": total_records,

        "current_page": page,

        "total_pages": total_pages,

        "data": transactions

    }