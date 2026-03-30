@echo off
REM Installation script for the Selenium pytest framework (Windows)
REM Run this script to set up the complete development environment

echo === Selenium Pytest Framework Setup ===

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=2" %%i in ('python --version') do echo ✓ Python version: %%i

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install production dependencies
echo 📚 Installing production dependencies...
pip install -r requirements.txt

REM Ask for development dependencies
set /p "install_dev=🤔 Install development dependencies? (y/N): "
if /i "%install_dev%"=="y" (
    echo 🛠️  Installing development dependencies...
    pip install -r requirements-dev.txt
)

REM Verify installation
echo ✅ Verifying installation...
python -c "import selenium, pytest, yaml, webdriver_manager; print('All core packages imported successfully!')"

echo.
echo 🎉 Setup complete!
echo.
echo Usage:
echo   - Activate environment: venv\Scripts\activate.bat
echo   - Run tests: pytest
echo   - Run tests with HTML report: pytest --html=reports/report.html
echo   - Run specific test markers: pytest -m smoke
echo   - Run tests in parallel: pytest -n auto
echo.

pause