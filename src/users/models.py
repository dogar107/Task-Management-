from sqlalchemy  import Column, Integer, String, Boolean
from src.utils.db import Base

class UserModel(Base):
    __tablename__="user"
    id=Column(Integer, primary_key=True)
    name=Column(String)
    username=Column(String, unique=True)
    email=Column(String, unique=True)
    password=Column(String)