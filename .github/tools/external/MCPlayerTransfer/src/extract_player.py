#!/usr/bin/env python3
"""
Minecraft 基岩版角色提取工具
输入: .mcworld 文件
输出: 角色数据文件 (.dat)
"""

import os
import sys
import zipfile
import tempfile
import shutil
from datetime import datetime

def extract_player(mcworld_path, output_dir="output"):
    """从 .mcworld 文件提取角色数据"""
    
    if not os.path.exists(mcworld_path):
        print(f"错误: 文件不存在 - {mcworld_path}")
        return None
    
    if not mcworld_path.endswith('.mcworld'):
        print("错误: 请提供 .mcworld 文件")
        return None
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取世界名称
    world_name = os.path.splitext(os.path.basename(mcworld_path))[0]
    
    # 创建临时目录解压
    temp_dir = tempfile.mkdtemp()
    
    try:
        print(f"正在解压: {mcworld_path}")
        with zipfile.ZipFile(mcworld_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # 查找 db 目录
        db_path = os.path.join(temp_dir, 'db')
        if not os.path.exists(db_path):
            # 可能在子目录里
            for root, dirs, files in os.walk(temp_dir):
                if 'db' in dirs:
                    db_path = os.path.join(root, 'db')
                    break
        
        if not os.path.exists(db_path):
            print("错误: 找不到 db 目录")
            return None
        
        print(f"找到数据库: {db_path}")
        
        # 打开 LevelDB
        import leveldb
        db = leveldb.LevelDB(db_path)
        
        # 提取玩家数据
        player_data = db.get(b'~local_player')
        
        if not player_data:
            print("错误: 找不到本地玩家数据")
            return None
        
        # 保存到输出目录
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, f"{world_name}_{timestamp}.dat")
        
        with open(output_file, 'wb') as f:
            f.write(player_data)
        
        print(f"\n✓ 提取成功!")
        print(f"  世界名称: {world_name}")
        print(f"  数据大小: {len(player_data)} bytes")
        print(f"  输出文件: {output_file}")
        
        del db
        return output_file
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    if len(sys.argv) < 2:
        print("""
Minecraft 基岩版角色提取工具
============================

用法:
  python extract_player.py <.mcworld文件> [输出目录]

示例:
  python extract_player.py "World.mcworld"
  python extract_player.py "World.mcworld" ./output

输出:
  角色数据文件 (.dat)，可导入到其他存档
        """)
        return
    
    mcworld_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    extract_player(mcworld_path, output_dir)


if __name__ == '__main__':
    main()
