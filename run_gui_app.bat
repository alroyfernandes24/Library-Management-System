@echo off
title Library Management System - Desktop GUI
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% == 0 (
    set PY_CMD=python
    goto RUN
)
where py >nul 2>nul
if %errorlevel% == 0 (
    set PY_CMD=py
    goto RUN
)

cls
echo ============================================================
echo [ERROR] Python is not installed or not in PATH!
echo Please install Python and check "Add Python to PATH".
echo ============================================================
pause
exit /b

:RUN
echo ========================================================
echo Starting Library Management System Desktop Application...
echo ========================================================
%PY_CMD% app_gui.py
pause
