from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from model.transactionmodel import TransactionCreate, TransactionDB, DuplicateTransaction
from repository.Database import get_db
from rag.Embedding import to_text
from rag.Ingestion_pipeline import vector_store

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

      db_duplicate_transaction = DuplicateTransaction(transaction_id = transaction.transaction_id, received_at = transaction.transaction_time)
      db.add(db_duplicate_transaction)
      db.commit()
         
      raise HTTPException(
        status_code=409,
        detail="Transaction already exists",
    ) from exc

    transaction_text = to_text(db_transaction)
    vector_store(transaction_text, db_transaction.transaction_id)

    return {"message": "Transaction added successfully"}
