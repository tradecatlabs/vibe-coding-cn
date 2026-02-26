#!/usr/bin/env python3
"""
图片ZIP转PDF脚本
将ZIP文件中的图片按序号排序并拼接成PDF文件
"""

import zipfile
import os
import re
from PIL import Image
import shutil

def 自然排序键(文件名):
    """将文件名转换为自然排序键，支持数字排序"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', 文件名)]

def zip转pdf(zip路径):
    """
    将ZIP文件中的图片排序后转换为PDF

    Args:
        zip路径: ZIP文件的完整路径

    Returns:
        成功返回PDF路径，失败返回None
    """
    try:
        # 获取ZIP文件名（不含扩展名）
        zip目录, zip文件名 = os.path.split(zip路径)
        pdf名称 = os.path.splitext(zip文件名)[0] + '.pdf'
        pdf路径 = os.path.join(zip目录, pdf名称)

        print(f"正在处理: {zip文件名}")

        # 创建临时目录解压文件
        临时目录 = os.path.join(zip目录, 'temp_extract')
        if os.path.exists(临时目录):
            shutil.rmtree(临时目录)
        os.makedirs(临时目录)

        # 解压ZIP文件
        with zipfile.ZipFile(zip路径, 'r') as zip文件:
            zip文件.extractall(临时目录)

        # 获取所有图片文件
        支持的格式 = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
        图片文件 = []

        for 根目录, 目录, 文件列表 in os.walk(临时目录):
            for 文件 in 文件列表:
                if any(文件.lower().endswith(格式) for 格式 in 支持的格式):
                    完整路径 = os.path.join(根目录, 文件)
                    图片文件.append(完整路径)

        if not 图片文件:
            print("错误: ZIP文件中没有找到图片文件")
            shutil.rmtree(临时目录)
            return None

        # 按文件名自然排序
        图片文件.sort(key=lambda x: 自然排序键(os.path.basename(x)))

        print(f"找到 {len(图片文件)} 张图片，开始转换...")

        # 打开第一张图片作为基础
        图片对象列表 = []
        for 图片路径 in 图片文件:
            try:
                图片 = Image.open(图片路径)
                # 转换为RGB模式（确保兼容性）
                if 图片.mode != 'RGB':
                    图片 = 图片.convert('RGB')
                图片对象列表.append(图片)
            except Exception as e:
                print(f"警告: 无法打开图片 {图片路径}: {e}")
                continue

        if not 图片对象列表:
            print("错误: 没有成功加载任何图片")
            shutil.rmtree(临时目录)
            return None

        # 保存为PDF（第一张作为主图，其余附加）
        图片对象列表[0].save(
            pdf路径,
            "PDF",
            quality=95,
            optimize=True,
            save_all=True,
            append_images=图片对象列表[1:]
        )

        # 关闭所有图片对象
        for 图片 in 图片对象列表:
            图片.close()

        # 清理临时文件
        shutil.rmtree(临时目录)

        # 删除原ZIP文件
        os.remove(zip路径)

        print(f"✓ 成功创建PDF: {pdf名称}")
        print(f"✓ 已删除原ZIP文件: {zip文件名}")

        return pdf路径

    except zipfile.BadZipFile:
        print(f"错误: {zip路径} 不是有效的ZIP文件")
        return None
    except Exception as e:
        print(f"处理过程中出错: {e}")
        # 清理临时文件
        if '临时目录' in locals() and os.path.exists(临时目录):
            shutil.rmtree(临时目录)
        return None

def 批量处理当前目录():
    """批量处理当前目录下所有ZIP文件"""
    当前目录 = os.getcwd()
    zip文件列表 = []

    # 扫描当前目录所有ZIP文件
    for 文件 in os.listdir(当前目录):
        if 文件.lower().endswith('.zip'):
            zip文件列表.append(os.path.join(当前目录, 文件))

    if not zip文件列表:
        print("当前目录下没有找到ZIP文件")
        return

    print(f"发现 {len(zip文件列表)} 个ZIP文件，开始批量处理...")
    print("-" * 50)

    成功计数 = 0
    失败计数 = 0

    for zip路径 in zip文件列表:
        print(f"\n[{zip文件列表.index(zip路径) + 1}/{len(zip文件列表)}] 处理: {os.path.basename(zip路径)}")

        # 执行转换
        结果 = zip转pdf(zip路径)

        if 结果:
            成功计数 += 1
        else:
            失败计数 += 1

    print("-" * 50)
    print(f"批量处理完成！成功: {成功计数} 个，失败: {失败计数} 个")

def 处理指定文件(zip路径):
    """处理指定的单个ZIP文件"""
    if not os.path.exists(zip路径):
        print(f"错误: 找不到文件 {zip路径}")
        return False

    if not zip路径.lower().endswith('.zip'):
        print("错误: 请提供ZIP格式的文件")
        return False

    # 执行转换
    结果 = zip转pdf(zip路径)

    if 结果:
        print(f"\n🎉 任务完成！PDF文件已保存为: {结果}")
        return True
    else:
        print("\n❌ 任务失败，请检查错误信息")
        return False

def 主函数():
    """主函数：智能处理模式"""
    import sys

    # 优先处理指定文件（如果存在）
    指定文件路径 = r"C:\Users\lenovo\Desktop\新建文件夹\剥头皮量化策略全拆解：低延迟、高频的底层.zip"

    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        # 命令行指定了ZIP文件路径
        zip路径 = sys.argv[1]
        print(f"通过命令行参数指定文件: {zip路径}")
        处理指定文件(zip路径)
    elif os.path.exists(指定文件路径):
        # 处理默认指定文件
        print(f"处理默认指定文件: {os.path.basename(指定文件路径)}")
        处理指定文件(指定文件路径)
    else:
        # 自动扫描当前目录所有ZIP文件
        print("开始扫描当前目录所有ZIP文件...")
        批量处理当前目录()

if __name__ == "__main__":
    主函数()