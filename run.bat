@echo off
title Library Management System - Smart Launcher
cd /d "%~dp0"

:: 1. Check if Python is available (checks 'python' first, then 'py' launcher)
where python >nul 2>nul
if %errorlevel% == 0 (
    set PY_CMD=python
    goto FOUND_PYTHON
)

where py >nul 2>nul
if %errorlevel% == 0 (
    set PY_CMD=py
    goto FOUND_PYTHON
)

:: Python not found error prompt
cls
echo ============================================================
echo                    PYTHON NOT FOUND!
echo ============================================================
echo Python is not installed or not added to your system PATH.
echo.
echo Quick Fix:
echo 1. Download Python from: https://www.python.org/downloads/
echo 2. During installation, CHECK the box:
echo    "[X] Add Python to PATH"
echo ============================================================
echo.
pause
exit /b

:FOUND_PYTHON
cls
echo ============================================================
echo        LIBRARY MANAGEMENT SYSTEM (DBMS MINI PROJECT)
echo ============================================================
echo.
echo Select an option to launch:
echo.
echo   [1] Modern Web Application (Recommended - Opens in Browser)
echo   [2] Desktop GUI Application (Tkinter Window)
echo   [3] Reset / Re-seed Database with Sample Data
echo   [4] Exit
echo.
echo ============================================================
set /p choice="Enter your choice (1, 2, 3, or 4): "

if "%choice%"=="1" goto LAUNCH_WEB
if "%choice%"=="2" goto LAUNCH_GUI
if "%choice%"=="3" goto RESEED
if "%choice%"=="4" exit /b

echo Invalid choice. Starting Web Application by default...
timeout /t 2 >nul
goto LAUNCH_WEB

:LAUNCH_WEB
cls
echo ============================================================
echo Starting Web Server on http://localhost:5000...
echo Opening your web browser...
echo (Keep this terminal window open while using the application)
echo ============================================================
start http://localhost:5000
%PY_CMD% app_web.py
pause
exit /b

:LAUNCH_GUI
cls
echo ============================================================
echo Starting Desktop GUI Application...
echo ============================================================
%PY_CMD% app_gui.py
pause
exit /b

:RESEED
cls
echo ============================================================
echo Resetting and seeding database with 50 books and sample data...
echo ============================================================
%PY_CMD% database/seed_data.py
echo.
pause
goto FOUND_PYTHON
