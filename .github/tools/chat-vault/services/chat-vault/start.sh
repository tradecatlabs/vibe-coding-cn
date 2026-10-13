#!/bin/bash
# AI Chat Converter - 一键启动
cd "$(dirname "$0")/src"
echo "正在启动 AI Chat Converter..."
echo "按 Ctrl+C 停止"
echo ""
python3 main.py --watch
