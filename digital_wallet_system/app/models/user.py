from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    phone = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(String, nullable=False)

    role = Column(String, default="User")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    wallet = relationship(
        "Wallet",
        back_populates="user",
        uselist=False
    )