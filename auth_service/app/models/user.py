from pydantic import BaseModel, EmailStr
from typing import Literal, List


#pydantic is a python module used to create and validate datamodels
#so we create a template for the data model, that helps us validate data automitcally, to avoid unexpected behaviour
class User(BaseModel):
  name : str
  password : str
  email: EmailStr
  role : Literal['student', 'instructor']
  faculty : str

class StudentCreate(User):
  """data model for a registering user"""
  level : Literal[200, 300, 400, 500, 550]
  pictures: List[float]
  student_id : str
  
  # i need five pictures for generation of embeddings


class InstructorCreate(User):
  """Instructor class"""
  pass


