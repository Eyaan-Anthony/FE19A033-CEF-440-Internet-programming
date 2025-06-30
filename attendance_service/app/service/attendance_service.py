# app/service/attendance_service.py

import httpx
from datetime import datetime, timedelta, timezone, UTC
from app.db.attendance_orm import Attendance
from app.db.db import SessionLocal
from app.models.attendance_model import AttendanceCreate, AttendanceResponse
from sqlalchemy.orm import Session
import uuid

FACIAL_RECOGNITION_URL = "http://facial_recognition_service:8001/verify"
GEOLOCATION_URL = "http://geolocation_service:8002/check-location"

# Set how close (in meters) the student must be
LOCATION_RADIUS_METERS = 10


async def mark_attendance(data: AttendanceCreate) -> AttendanceResponse:
    async with httpx.AsyncClient() as client:
        # Step 1: Verify face
        face_response = await client.post(FACIAL_RECOGNITION_URL, json={
            "student_id": data.student_id,
            "image_data": data.image_data
        })
        if face_response.status_code != 200 or not face_response.json().get("verified"):
            return AttendanceResponse(success=False, reason="Face verification failed")

        # Step 2: Verify location
        geo_response = await client.post(GEOLOCATION_URL, json={
            "target_lat": data.class_lat,
            "target_long": data.class_long,
            "student_lat": data.student_lat,
            "student_long": data.student_long,
            "radius_meters": LOCATION_RADIUS_METERS
        })
        geo_data = geo_response.json()
        if geo_response.status_code != 200 or not geo_data.get("within_radius"):
            return AttendanceResponse(success=False, reason="Outside allowed location")

        # Step 3: Check time window logic (15 minutes before to 30 minutes after start)
        now = datetime.utcnow(datetime.timezone.utc)
        if not (data.start_time - timedelta(minutes=15) <= now <= data.start_time + timedelta(minutes=30)):
            return AttendanceResponse(success=False, reason="Not within allowed time window")

        # Step 4: Save to DB
        db: Session = SessionLocal()
        record = Attendance(
            id=str(uuid.uuid4()),
            student_id=data.student_id,
            session_id=data.session_id,
            timestamp=now
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return AttendanceResponse(success=True, reason="Attendance marked")


def get_attendance_stats(session_id: str = None):
    db: Session = SessionLocal()
    query = db.query(Attendance)

    if session_id:
        query = query.filter(Attendance.session_id == session_id)

    results = query.all()

    stats = {}
    for record in results:
        stats.setdefault(record.session_id, []).append(record.student_id)

    return stats
