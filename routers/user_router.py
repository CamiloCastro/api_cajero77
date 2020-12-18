from typing import List
from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session
from db.db_connection import get_db

from db.user_db import UserInDB
from db.transaction_db import TransactionInDB
from models.user_models import UserIn, UserOut
from models.transaction_models import TransactionIn, TransactionOut

router = APIRouter()

@router.get("/examples")
async def examples(db: Session = Depends(get_db)):

    '''
    user = UserInDB(username = "juan25", password = "contrasena", balance=150000)
    db.add(user)
    db.commit()
    db.refresh(user)
    '''
    users = db.query(UserInDB).filter(UserInDB.username.like('%a%') )   
    for u in users:
        print(u.username)
    



@router.post("/user/auth/")
async def auth_user(user_in: UserIn, db: Session = Depends(get_db)):

    user_in_db = db.query(UserInDB).get(user_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    if user_in_db.password != user_in.password:
        raise HTTPException(status_code=403, detail="Error de autenticacion")
    return {"Autenticado": True}

@router.get("/user/balance/{username}", response_model=UserOut)
async def get_balance(username: str, db: Session = Depends(get_db)):
    user_in_db = db.query(UserInDB).get(username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    return user_in_db

@router.post("/user/register/")
async def register_user(user_in: UserIn, db: Session = Depends(get_db)):

    
    user_in_db = UserInDB(**user_in.dict(), balance = 100000)

    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)
    
    return {"Mensaje": "El usuario fue creado correctamente"}