@echo off
echo 安装打包工具...
pip install pyinstaller -q

echo 开始打包...
pyinstaller --onefile --name ai-chat-converter ^
    --add-data "src;src" ^
    --hidden-import tiktoken_ext.openai_public ^
    --hidden-import tiktoken_ext ^
    --collect-data tiktoken ^
    src/main.py

echo.
echo 完成! 输出: dist\ai-chat-converter.exe
pause
