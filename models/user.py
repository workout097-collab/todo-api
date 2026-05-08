from pydantic import BaseModel

from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    tasks = relationship("Task", back_populates="owner")

class  UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserTaskResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True
class UserProfileResponse(BaseModel):
            id: int
            email: str
            tasks: list[UserTaskResponse]

class Config:
      from_attributes = True