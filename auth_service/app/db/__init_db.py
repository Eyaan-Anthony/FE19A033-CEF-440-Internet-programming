from .session import db_engine
from .auth_orm import Base

def create_tables():
    Base.metadata.create_all(bind=db_engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    create_tables()
  
#python -m auth_service.app.db.__init_db
