from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    faculty = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Student-specific fields
    level = Column(Integer, nullable=True)         # nullable for instructors
    student_id = Column(String, nullable=True)     # nullable for instructors

    # Face embeddings (optional, added later via facial recognition service)
    face_embeddings = Column(JSON, nullable=True)  # stored as list of floats

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
