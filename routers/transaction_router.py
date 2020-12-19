from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.db_connection import get_db
from db.user_db import UserInDB
from db.transaction_db import TransactionInDB
from models.user_models import UserIn, UserOut
from models.transaction_models import TransactionIn, TransactionOut, verify_transaction

router = APIRouter()
@router.put("/user/transaction/", response_model=TransactionOut)
async def make_transaction(transaction_in: TransactionIn, db: Session = Depends(get_db)):

    verify_transaction(transaction_in)

    user_in_db = db.query(UserInDB).get(transaction_in.username)

    if user_in_db == None:
         raise HTTPException(status_code=404,detail="El usuario no existe")
    if user_in_db.balance < transaction_in.value:
        raise HTTPException(status_code=400, detail="No se tienen los fondos suficientes")

    user_in_db.balance = user_in_db.balance - transaction_in.value
    db.commit()
    db.refresh(user_in_db)
    transaction_in_db = TransactionInDB(**transaction_in.dict(), actual_balance = user_in_db.balance)
    db.add(transaction_in_db)    
    db.commit()
    db.refresh(transaction_in_db)
    return transaction_in_db