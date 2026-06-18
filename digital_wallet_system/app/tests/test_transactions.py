from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.transaction import Transaction


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
    db: Session = Depends(get_db)
):

    query = db.query(Transaction)


    # filter by transaction type
    if type:
        query = query.filter(
            Transaction.transaction_type == type
        )


    # filter by status
    if status:
        query = query.filter(
            Transaction.status == status
        )


    # filter by date
    if date_filter:
        query = query.filter(
            Transaction.created_at >= date_filter
        )


    # total records
    total_records = query.count()


    # pagination
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