from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, Header

from sqlalchemy.orm import Session
from db.db_connection import get_db

from db.user_db import UserInDB
from db.transaction_db import TransactionInDB
from db.role_db import RoleInDB
from models.user_models import UserIn, UserOut, UserInCreate, ModifyBalanceIn, verify_user_in_create
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

@router.post("/user/transfer/")
async def user_transfer(user_modify_balance: ModifyBalanceIn,db: Session = Depends(get_db), authentication: Optional[str] = Header(None)):

    if authentication == None:
        raise HTTPException(status_code=403, detail="No está autorizado")

    lista_roles = db.query(RoleInDB).\
        filter(RoleInDB.username == authentication).\
            filter(RoleInDB.role_name == "USUARIO").all()

    if not lista_roles:
        raise HTTPException(status_code=403, detail="No está autorizado")

    user_in_db = db.query(UserInDB).get(user_modify_balance.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    user_in_auth = db.query(UserInDB).get(authentication)

    if user_in_auth.balance < user_modify_balance.balance:
        raise HTTPException(status_code=400, detail="El usuario no tiene saldo suficiente")

    user_in_auth.balance = user_in_auth.balance - user_modify_balance.balance
    db.commit()
    db.refresh(user_in_auth)

    user_in_db.balance = user_in_db.balance + user_modify_balance.balance
    db.commit()
    db.refresh(user_in_db)
    return {"Message": "La transferencia fue exitosa"}


@router.post("/user/balance/modify/")
async def modify_balance(user_modify_balance: ModifyBalanceIn,db: Session = Depends(get_db), authentication: Optional[str] = Header(None)):

    if authentication == None:
        raise HTTPException(status_code=403, detail="No está autorizado")

    lista_roles = db.query(RoleInDB).\
        filter(RoleInDB.username == authentication).\
            filter(RoleInDB.role_name == "BANCO").all()

    if not lista_roles:
        raise HTTPException(status_code=403, detail="No está autorizado")

    user_in_db = db.query(UserInDB).get(user_modify_balance.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    user_in_db.balance = user_modify_balance.balance
    db.commit()
    db.refresh(user_in_db)
    return {"Message" : "Balance modificado correctamente"}



@router.post("/user/create/")
async def create_user(user_in_create: UserInCreate, db: Session = Depends(get_db), authentication: Optional[str] = Header(None)):

    if authentication == None:
        raise HTTPException(status_code=403, detail="No está autorizado")

    lista_roles = db.query(RoleInDB).\
        filter(RoleInDB.username == authentication).\
            filter(RoleInDB.role_name == "BANCO").all()

    if not lista_roles:
        raise HTTPException(status_code=403, detail="No está autorizado")

    verify_user_in_create(user_in_create)

    user_in_db = UserInDB(username = user_in_create.username, password = user_in_create.password, balance = user_in_create.balance)
    db.add(user_in_db)    
    db.commit()
    db.refresh(user_in_db)

    role_in_db = RoleInDB(username = user_in_create.username, role_name = "USUARIO")
    db.add(role_in_db)
    db.commit()
    db.refresh(role_in_db)

    return {"message": "El usuario fue creado existosamente"}


    

@router.get("/user/roles/{username}")
async def get_roles(username: str, db: Session = Depends(get_db)):

    list_roles = db.query(RoleInDB).\
        filter(RoleInDB.username == username).\
            order_by(RoleInDB.role_name).all()

    return list_roles


@router.post("/user/auth/")
async def auth_user(user_in: UserIn, db: Session = Depends(get_db)):

    user_in_db = db.query(UserInDB).get(user_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    if user_in_db.password != user_in.password:
        raise HTTPException(status_code=403, detail="Error de autenticacion")

    list_roles = db.query(RoleInDB).\
        filter(RoleInDB.username == user_in.username).\
            order_by(RoleInDB.role_name).all()

    return list_roles

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