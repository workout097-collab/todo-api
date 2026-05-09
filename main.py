from fastapi import FastAPI

from routes import users
from routes import tasks

from database import Base, engine

from models.user import User
from models.task import Task


app = FastAPI(
    title="VTaskForge API",
    description="Production-ready task management backend built with FastAPI, JWT authentication, PostgreSQL",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(tasks.router)