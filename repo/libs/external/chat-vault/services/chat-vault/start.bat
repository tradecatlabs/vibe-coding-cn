@echo off
cd /d "%~dp0src"
echo 正在启动 AI Chat Converter...
echo 按 Ctrl+C 停止
echo.
python main.py --watch
pause
