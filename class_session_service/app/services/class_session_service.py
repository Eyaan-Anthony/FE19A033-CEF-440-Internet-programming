from sqlalchemy.orm import Session
from models.class_session_models import ClassSessionCreate
from db.class_session_orm import ClassSessionDB


def create_class_session(db: Session, data: ClassSessionCreate) -> ClassSessionDB:
    session = ClassSessionDB(
        course_name=data.course_name,
        instructor_id=data.instructor_id,
        location_lat=data.location_lat,
        location_lng=data.location_lng,
        start_time=data.start_time,
        end_time=data.end_time
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_class_session(db: Session, session_id: str) -> ClassSessionDB:
    session = db.query(ClassSessionDB).filter_by(session_id=session_id).first()
    if not session:
        raise ValueError("Class session not found")
    return session
