@echo off
chcp 65001 >nul
cd /d "%~dp0..\.."
echo ========================================
echo  水厂主体软件 - 生产环境启动（Windows）
echo ========================================
echo.
call .venv\Scripts\activate.bat
python 生产环境\windows\run_prod.py
pause
