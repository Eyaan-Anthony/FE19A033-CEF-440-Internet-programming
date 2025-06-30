#configuration file
import os

class Settings : 

  Project_name: str = "Authentication service"

  #we'll add the database url here as well
  Database_url = "postgresql://postgres:password123@localhost:5432/auth_service"


settings = Settings()