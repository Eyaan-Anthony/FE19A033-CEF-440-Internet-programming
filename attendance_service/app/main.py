from fastapi import FastAPI
from app.api.attendance_routes import router as attendance_router
from app.db.__init_db import init_db

app = FastAPI()


def startup_event():
    init_db()

app.include_router(attendance_router, prefix="/attendance")