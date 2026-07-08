@echo off
echo 🎬 Starting MovieBuddy Web Application...
echo.

echo [1/2] Starting Flask Backend Server...
start "MovieBuddy Backend" cmd /c "cd /d "%~dp0backend" && python app.py"

echo [2/2] Starting React Frontend Server...
start "MovieBuddy Frontend" cmd /c "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ✅ Both servers are starting!
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:5000
echo.
echo Press any key to close this window...
pause >nul