from pydantic import BaseModel
from fastapi import HTTPException
import re

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    balance: int

    class Config:
        orm_mode = True

class UserInCreate(BaseModel):
    username: str
    password: str
    repeat_password: str
    balance: int

class ModifyBalanceIn(BaseModel):
    username: str
    balance: int

def verify_user_in_create(user_in_create: UserInCreate):

    if user_in_create.password != user_in_create.repeat_password:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    if user_in_create.balance < 0:
        raise HTTPException(status_code=400, detail="El balance debe ser positivo")

    if not user_in_create.username:
        raise HTTPException(status_code=400, detail="El username no debe estar vacío")

    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}"

    pat = re.compile(reg)

    mat = re.search(pat, user_in_create.password)

    if not mat:
        raise HTTPException(status_code=400, detail="La contraseña debe tener un número, una minúscula, una mayúscula y longitud mínima de 6")

