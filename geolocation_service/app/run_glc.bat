@echo off
cd "C:\Users\franc\Documents\Attendance project\back_end"
call venv\Scripts\activate
python -m uvicorn geolocation_service.app.main:app --reload --port 8002

".\run_glc.bat"