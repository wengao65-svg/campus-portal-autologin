@echo off
title Campus AutoConnect Remove

echo ========================================================
echo   Remove GXUST Campus AutoConnect Task
echo ========================================================
echo.

set TASK_NAME="GXUST_Campus_AutoConnect"
set BASE_DIR=%~dp0
set VBS_PATH=%BASE_DIR%run_hidden.vbs

echo [INFO] Deleting task...
schtasks /delete /tn %TASK_NAME% /f

if exist "%VBS_PATH%" (
    del "%VBS_PATH%"
    echo [INFO] Hidden startup script removed.
)

echo.
echo [SUCCESS] Auto-start task has been completely removed!
echo.
pause