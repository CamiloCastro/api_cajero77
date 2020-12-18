from pydantic import BaseModel
from datetime import datetime, date, time

class TransactionIn(BaseModel):
    username: str
    value: int

class TransactionOut(BaseModel):
    id: int
    username: str
    date: datetime
    value: int
    actual_balance: int

    class Config:
        orm_mode = True