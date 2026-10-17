#!/usr/bin/env python3
"""
Minecraft 基岩版角色转移工具
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from extract_player import extract_player
from import_player import import_player


def main():
    if len(sys.argv) < 2:
        print("""
Minecraft 基岩版角色转移工具
============================

用法:
  python main.py extract <.mcworld文件>
  python main.py import <.mcworld文件> <.dat角色文件>

示例:
  python main.py extract "input/World.mcworld"
  python main.py import "input/World.mcworld" "output/player.dat"
        """)
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'extract':
        if len(sys.argv) < 3:
            print("错误: 请提供 .mcworld 文件路径")
            return
        extract_player(sys.argv[2], "output")
    
    elif cmd == 'import':
        if len(sys.argv) < 4:
            print("错误: 请提供 .mcworld 文件和 .dat 角色文件")
            return
        import_player(sys.argv[2], sys.argv[3])
    
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()
