#!/usr/bin/env python3
"""打包脚本 - 生成独立可执行文件"""
import subprocess
import sys
import os
import shutil

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    for d in ['build', 'dist']:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    print("开始打包...")
    
    sep = ";" if sys.platform == "win32" else ":"
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "ai-chat-converter",
        f"--add-data=src{sep}src",
        "--hidden-import", "tiktoken_ext.openai_public",
        "--hidden-import", "tiktoken_ext",
        "--hidden-import", "dotenv",
        "--collect-data", "tiktoken",
        "--collect-all", "watchdog",
        "--collect-all", "dotenv",
        "src/main.py"
    ]
    
    subprocess.run(cmd, check=True)
    
    exe = "dist/ai-chat-converter.exe" if sys.platform == "win32" else "dist/ai-chat-converter"
    size = os.path.getsize(exe) / 1024 / 1024
    print(f"\n✓ 打包完成: {exe} ({size:.1f} MB)")

if __name__ == "__main__":
    main()
