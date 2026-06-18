from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    wallet_id = Column(
        Integer,
        ForeignKey("wallets.id")
    )

    transaction_type = Column(String)

    amount = Column(Float)

    status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    wallet = relationship("Wallet")