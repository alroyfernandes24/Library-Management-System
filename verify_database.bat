@echo off
title Library Database Verification Tool
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% == 0 (set PY_CMD=python) else (set PY_CMD=py)

cls
echo ============================================================
echo          LIVE DATABASE QUERY & VERIFICATION TOOL
echo ============================================================
echo.
echo 1. Show Latest 5 Books in Database Table (books)
echo 2. Show Latest 5 Registered Members (members)
echo 3. Show Active Borrow Transactions (borrow_transactions)
echo 4. Show Outstanding Fines (fines)
echo 5. Show Latest Audit Logs (audit_logs - Trigger Output)
echo 6. Interactive Custom SQL Query Prompt
echo 7. Exit
echo.
echo ============================================================
set /p opt="Enter choice (1-7): "

if "%opt%"=="1" (
    %PY_CMD% -c "import sqlite3; c=sqlite3.connect('library.db'); r=c.execute('SELECT book_id, isbn, title, total_copies, available_copies FROM books ORDER BY book_id DESC LIMIT 5').fetchall(); print('\n--- LATEST 5 BOOKS IN SQL TABLE ---'); [print(row) for row in r]"
    pause
    goto :EOF
)
if "%opt%"=="2" (
    %PY_CMD% -c "import sqlite3; c=sqlite3.connect('library.db'); r=c.execute('SELECT member_id, first_name, last_name, email, membership_type, status FROM members ORDER BY member_id DESC LIMIT 5').fetchall(); print('\n--- LATEST 5 MEMBERS IN SQL TABLE ---'); [print(row) for row in r]"
    pause
    goto :EOF
)
if "%opt%"=="3" (
    %PY_CMD% -c "import sqlite3; c=sqlite3.connect('library.db'); r=c.execute('SELECT transaction_id, book_id, member_id, issue_date, due_date, status FROM borrow_transactions WHERE return_date IS NULL LIMIT 5').fetchall(); print('\n--- ACTIVE LOANS IN SQL TABLE ---'); [print(row) for row in r]"
    pause
    goto :EOF
)
if "%opt%"=="4" (
    %PY_CMD% -c "import sqlite3; c=sqlite3.connect('library.db'); r=c.execute('SELECT fine_id, transaction_id, member_id, fine_amount, paid_status FROM fines ORDER BY fine_id DESC LIMIT 5').fetchall(); print('\n--- FINES IN SQL TABLE ---'); [print(row) for row in r]"
    pause
    goto :EOF
)
if "%opt%"=="5" (
    %PY_CMD% -c "import sqlite3; c=sqlite3.connect('library.db'); r=c.execute('SELECT log_id, table_name, action_type, description, created_at FROM audit_logs ORDER BY log_id DESC LIMIT 5').fetchall(); print('\n--- AUDIT LOGS TRIGGER OUTPUT ---'); [print(row) for row in r]"
    pause
    goto :EOF
)
if "%opt%"=="6" (
    echo.
    set /p sqlquery="Enter SQL SELECT Query: "
    %PY_CMD% -c "import sqlite3; c=sqlite3.connect('library.db'); r=c.execute('%sqlquery%').fetchall(); [print(row) for row in r]"
    pause
    goto :EOF
)
