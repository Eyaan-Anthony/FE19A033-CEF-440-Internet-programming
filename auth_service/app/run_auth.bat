@echo off
cd "C:\Users\franc\Documents\Attendance project\back_end"
call venv\Scripts\activate
python -m uvicorn auth_service.app.main:app --reload --port 8000

".\run_auth.bat"