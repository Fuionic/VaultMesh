from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint

from repository.Database import Base


class TransactionDB(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint("transaction_id", name="uq_transactions_transaction_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    merchant = Column(String(255), nullable=False)
    transaction_time = Column(DateTime(timezone=True), nullable=False)


class TransactionCreate(BaseModel):
    transaction_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    merchant: str = Field(min_length=1, max_length=255)
    transaction_time: datetime


class DuplicateTransaction(Base):
    __tablename__ = "Duplicate_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, nullable=False)
    received_at = Column(DateTime(timezone=True), nullable=False)
    