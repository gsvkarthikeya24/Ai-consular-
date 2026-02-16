@echo off
echo ============================================================
echo   Gemini API Configuration Helper
echo ============================================================
echo.

REM Check if API key is set
findstr /C:"GEMINI_API_KEY=AIzaSy" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Gemini API key appears to be configured!
    echo.
    echo Current configuration:
    findstr "LLM_PROVIDER" .env
    findstr "GEMINI_API_KEY" .env
    echo.
    echo Ready to test! Run: python test_gemini.py
) else (
    echo [!] Gemini API key NOT configured yet
    echo.
    echo STEP 1: Get your API key
    echo    Visit: https://aistudio.google.com/app/apikey
    echo    Sign in and click "Create API Key"
    echo.
    echo STEP 2: Update your .env file
    echo    Open: backend\.env
    echo    Set: LLM_PROVIDER=gemini
    echo    Set: GEMINI_API_KEY=YOUR_ACTUAL_KEY
    echo.
    echo STEP 3: Run this script again to verify
)

echo.
echo ============================================================
pause
