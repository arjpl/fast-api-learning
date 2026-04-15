from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLACHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(SQLACHEMY_DATABASE_URL, connect_args={"check_same_thread": False })

SessionLocal = sessionmaker(autoflush=False, bind=engine)

with SessionLocal() as session:
    session.commit()
# Without commit() — changes are lost when the session closes.


Base = declarative_base()       



