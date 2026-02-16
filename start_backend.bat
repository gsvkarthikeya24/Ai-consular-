@echo off
echo Starting AI Consular Backend...
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Backend server starting on http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo ========================================
echo.

REM Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
