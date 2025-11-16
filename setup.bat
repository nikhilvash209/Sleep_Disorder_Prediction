@echo off
echo ========================================
echo Sleep Disorder Predictor - Quick Setup
echo ========================================
echo.

echo [1/3] Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)
echo ✓ Packages installed successfully
echo.

echo [2/3] Checking environment file...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️ IMPORTANT: Edit .env file and add your Supabase credentials:
    echo    - SUPABASE_URL
    echo    - SUPABASE_KEY
    echo.
    echo Get these from: https://app.supabase.com/project/YOUR_PROJECT/settings/api
    echo.
) else (
    echo ✓ .env file already exists
)
echo.

echo [3/3] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Edit .env file with your Supabase credentials
echo 2. Run: streamlit run app.py
echo 3. Access at: http://localhost:8501
echo ========================================
echo.
pause
