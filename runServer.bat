@echo off

netstat -ano | findstr :8002 > nul
if %errorlevel% == 0 (
    echo Server is running
    pause
    exit
)

cd /d %~dp0
call venv_Fast_ZK_v2\Scripts\activate.bat
cd /d app
start /B python manage.py runserver 0.0.0.0:8002 --noreload
exit