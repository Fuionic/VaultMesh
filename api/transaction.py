from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from model.transactionmodel import TransactionCreate, TransactionDB
from repository.Database import get_db

router = APIRouter(tags=["transactions"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    db_transaction = TransactionDB(**transaction.model_dump())
    db.add(db_transaction)
  
    try:
     db.commit()
    except IntegrityError as exc:
      db.rollback()
      raise HTTPException(
        status_code=409,
        detail="Transaction already exists",
    ) from exc

    return {"message": "Transaction added successfully"}
