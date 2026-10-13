#!/usr/bin/env python3
"""
Minecraft 基岩版角色导入工具
输入: .mcworld 文件 + .dat 角色文件
输出: 新的 .mcworld 文件
"""

import os
import sys
import zipfile
import tempfile
import shutil
from datetime import datetime

def import_player(mcworld_path, player_dat, output_path=None):
    """将角色数据导入到 .mcworld 文件"""
    
    if not os.path.exists(mcworld_path):
        print(f"错误: 文件不存在 - {mcworld_path}")
        return None
    
    if not os.path.exists(player_dat):
        print(f"错误: 角色文件不存在 - {player_dat}")
        return None
    
    # 读取角色数据
    with open(player_dat, 'rb') as f:
        player_data = f.read()
    print(f"读取角色数据: {len(player_data)} bytes")
    
    # 默认输出路径
    if output_path is None:
        base = os.path.splitext(mcworld_path)[0]
        output_path = f"{base}_imported.mcworld"
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        print(f"正在解压: {mcworld_path}")
        with zipfile.ZipFile(mcworld_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # 查找 db 目录
        db_path = os.path.join(temp_dir, 'db')
        world_root = temp_dir
        
        if not os.path.exists(db_path):
            for root, dirs, files in os.walk(temp_dir):
                if 'db' in dirs:
                    db_path = os.path.join(root, 'db')
                    world_root = root
                    break
        
        if not os.path.exists(db_path):
            print("错误: 找不到 db 目录")
            return None
        
        # 写入玩家数据
        import leveldb
        db = leveldb.LevelDB(db_path)
        db.put(b'~local_player', player_data)
        del db
        
        print("✓ 角色数据已写入")
        
        # 重新打包
        print(f"正在打包: {output_path}")
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(world_root):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, world_root)
                    zipf.write(file_path, arc_name)
        
        print(f"\n✓ 导入成功!")
        print(f"  输出文件: {output_path}")
        return output_path
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    if len(sys.argv) < 3:
        print("""
Minecraft 基岩版角色导入工具
============================

用法:
  python import_player.py <.mcworld文件> <.dat角色文件> [输出文件]

示例:
  python import_player.py "World.mcworld" "player.dat"
  python import_player.py "World.mcworld" "player.dat" "NewWorld.mcworld"
        """)
        return
    
    mcworld_path = sys.argv[1]
    player_dat = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    import_player(mcworld_path, player_dat, output_path)


if __name__ == '__main__':
    main()
