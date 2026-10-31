@echo off
chcp 65001 >nul
title 水厂主体软件

echo ==========================================
echo   水厂主体软件 - 启动中...
echo ==========================================

:: 启动 MySQL（如果未运行）
tasklist /FI "IMAGENAME eq mysqld.exe" 2>nul | find /I "mysqld.exe" >nul
if errorlevel 1 (
    echo [启动] MySQL 服务...
    start /B "" "C:\mysql\bin\mysqld.exe" --console > C:\mysql\mysqld.log 2>&1
    timeout /t 3 /nobreak >nul
) else (
    echo [跳过] MySQL 已在运行
)

:: 启动主程序
echo [启动] 主程序（控制台 + Web）...
echo.
echo   Web 地址: http://127.0.0.1:5000
echo   按 Ctrl+C 停止
echo ==========================================
echo.

cd /d "%~dp0"
".venv\Scripts\python.exe" main.py

pause
