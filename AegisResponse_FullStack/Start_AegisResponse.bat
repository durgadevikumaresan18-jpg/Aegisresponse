@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python is not installed or not available in PATH.
  echo Install Python from https://www.python.org/downloads/windows/
  echo Select "Add python.exe to PATH" during installation.
  pause
  exit /b 1
)
py -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed. Check your internet connection.
  pause
  exit /b 1
)
py app.py
pause
