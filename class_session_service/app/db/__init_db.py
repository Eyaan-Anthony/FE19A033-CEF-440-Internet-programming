from .db import engine
from .class_session_orm import Base

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()

#python db/init_db.py
