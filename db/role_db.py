from sqlalchemy import Column, ForeignKey
from sqlalchemy import String
from db.db_connection import Base, engine

class RoleInDB(Base):
    __tablename__ = "user_role"
    role_name = Column(String, primary_key=True)
    username = Column(String, ForeignKey("users.username"), primary_key=True)

Base.metadata.create_all(bind=engine)