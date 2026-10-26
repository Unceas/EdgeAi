@echo off
title Edge AI Smart Prosthetic Hand Launcher
echo ================================================================
echo Starting Edge AI Smart Prosthetic Hand Prototype Services...
echo ================================================================
echo.

:: Launch Backend in separate window
echo [1/3] Starting FastAPI Backend (Port 8000)...
start "Backend - FastAPI Brain" cmd /k "cd /d "%~dp0backend" && python -m uvicorn main:app --host 127.0.0.1 --port 8000"

:: Wait 2 seconds
timeout /t 2 /nobreak >nul

:: Launch Frontend in separate window
echo [2/3] Starting React Frontend Dashboard (Port 5173)...
start "Frontend - Vite React Dashboard" cmd /k "cd /d "%~dp0frontend" && npm run dev -- --host 127.0.0.1 --port 5173"

:: Wait 2 seconds
timeout /t 2 /nobreak >nul

:: Open default browser
echo [3/3] Opening Browser at http://localhost:5173...
start "" "http://localhost:5173"

echo.
echo ================================================================
echo Prototype is now LIVE!
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo ================================================================
echo Keep the backend and frontend terminal windows open while testing.
echo Press any key to close this launcher window.
pause >nul
