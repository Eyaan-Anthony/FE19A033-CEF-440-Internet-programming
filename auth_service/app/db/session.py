#deals with database connection (creation, handling)

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_engine = create_engine(settings.Database_url) #to actually create a connection to the database using the url

SessionLocal = sessionmaker(bind=db_engine, autocomit=False,autoflush=False) #session here is akin to the context,
#within the confines of the database connection. All objects created or loaded are available in the session

