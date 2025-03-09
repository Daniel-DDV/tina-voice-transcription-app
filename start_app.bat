@echo off
echo Starting Tina Application...

:: Set up environment variables with absolute paths
set ROOT_DIR=D:\Experimenten\Tina
set BACKEND_DIR=%ROOT_DIR%\tina-api
set FRONTEND_DIR=%ROOT_DIR%\tina-frontend

:: Start the backend API using the Python script we created (more reliable)
echo Starting Backend API...
start cmd /k "python %ROOT_DIR%\start_api.py"

:: Wait a moment for the backend to initialize
timeout /t 10

:: Start the frontend in a new window
echo Starting Frontend...
start cmd /k "cd /d %FRONTEND_DIR% && npm run dev"

echo Tina Application is starting up!
echo Backend API will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
