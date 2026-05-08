from fastapi import FastAPI
from routes import users
from routes import tasks
app = FastAPI()

from database import Base
from database import engine
from models.task import Task
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(tasks.router)