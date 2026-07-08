@echo off
setlocal EnableDelayedExpansion

title AO_Forge Launcher

echo.
echo ==========================================
echo           AO_Forge Launcher
echo ==========================================
echo.

REM --------------------------------------------------
REM Repository Root
REM --------------------------------------------------

set "ROOT=%~dp0"
cd /d "%ROOT%"

REM --------------------------------------------------
REM Read launcher.ini
REM --------------------------------------------------

if not exist "launcher.ini" (
    echo [ERROR] launcher.ini not found.
    pause
    exit /b
)

for /f "usebackq tokens=1,* delims==" %%A in ("launcher.ini") do (
    if /I "%%A"=="NUKE_EXE" (
        set "NUKE_EXE=%%B"
    )
)

REM --------------------------------------------------
REM Validate Nuke Path
REM --------------------------------------------------

if not exist "%NUKE_EXE%" (
    echo.
    echo [ERROR] Nuke executable not found:
    echo.
    echo %NUKE_EXE%
    echo.
    pause
    exit /b
)

REM --------------------------------------------------
REM Update AO_Forge
REM --------------------------------------------------

echo Checking for updates...
echo.

git rev-parse --is-inside-work-tree >nul 2>&1

if errorlevel 1 (
    echo [INFO] Not a Git repository.
    echo [INFO] Skipping update.
) else (
    git pull
)

echo.
echo ==========================================
echo Launching Nuke...
echo ==========================================
echo.

start "" "%NUKE_EXE%"

endlocal
exit