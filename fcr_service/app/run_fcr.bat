@echo off
cd "C:\Users\franc\Documents\Attendance project\back_end"
call venv\Scripts\activate
python -m uvicorn fcr_service.app.main:app --reload --port 8001

".\run_fcr.bat"