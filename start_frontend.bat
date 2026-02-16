@echo off
echo Starting AI Consular Frontend...
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

echo.
echo ========================================
echo Frontend server starting on http://localhost:5173
echo ========================================
echo.

REM Start the frontend
call npm run dev
