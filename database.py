

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://admin:1234@localhost/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

from sqlalchemy.orm import declarative_base

Base = declarative_base()
