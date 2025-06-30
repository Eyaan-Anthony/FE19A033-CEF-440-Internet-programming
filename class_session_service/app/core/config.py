import os

class Settings : 

  Project_name: str = "Class Session service"

  #we'll add the database url here as well
  Database_url = "postgresql://postgres:password123@localhost:5432/auth_service"
  #maybe create a new database


settings = Settings()