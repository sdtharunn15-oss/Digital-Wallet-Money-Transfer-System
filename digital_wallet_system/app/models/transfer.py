from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Index
from datetime import datetime

from app.database import Base


class Transfer(Base):

    __tablename__ = "transfers"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    sender_wallet_id = Column(
        Integer,
        ForeignKey("wallets.id"),
        index=True
    )


    receiver_wallet_id = Column(
        Integer,
        ForeignKey("wallets.id"),
        index=True
    )


    amount = Column(
        Float,
        nullable=False
    )


    transaction_reference = Column(
        String,
        unique=True,
        index=True
    )


    status = Column(
        String,
        default="Success",
        index=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )



Index(
    "idx_transfer_wallets",
    Transfer.sender_wallet_id,
    Transfer.receiver_wallet_id
)