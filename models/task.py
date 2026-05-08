from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import ForeignKey
from pydantic import BaseModel as PydanticBaseModel

from typing import Optional
from sqlalchemy.orm import relationship
class TaskResponse(PydanticBaseModel):

    id: int
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")


class TaskCreate(PydanticBaseModel):
    title: str
    description: str

class TaskUpdate(PydanticBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None