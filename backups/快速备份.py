#!/usr/bin/env python3
"""
快速备份项目工具
读取 .gitignore 规则并打包项目文件（排除匹配的文件）

bash backups/一键备份.sh

文件位置：
  backups/快速备份.py

工具清单（backups/目录）：
  • 快速备份.py         - 核心备份引擎（7.3 KB）
  • 一键备份.sh         - 一键执行脚本（2.4 KB）

使用方法：
  $ bash backups/一键备份.sh
  或
  $ python3 backups/快速备份.py

备份输出：
  backups/gz/备份_YYYYMMDD_HHMMSS.tar.gz

适用项目：
  任何包含 .gitignore 文件的项目（自动读取规则并排除匹配文件）

依赖：
  无需额外安装包，仅使用Python内置模块
"""

import os
import tarfile
import fnmatch
from pathlib import Path
from datetime import datetime
import argparse
import sys


class GitignoreFilter:
    """解析 .gitignore 文件并过滤文件"""

    def __init__(self, gitignore_path: Path, project_root: Path):
        self.project_root = project_root
        # 规则按照出现顺序存储，支持取反（!）语义，后匹配覆盖前匹配
        # 每项: {"pattern": str, "dir_only": bool, "negate": bool, "has_slash": bool}
        self.rules = []
        self.load_gitignore(gitignore_path)

    def load_gitignore(self, gitignore_path: Path):
        """加载并解析 .gitignore 文件"""
        if not gitignore_path.exists():
            print(f"⚠️  警告: {gitignore_path} 不存在，将不应用任何过滤规则")
            return

        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()

                    # 跳过空行和注释
                    if not line or line.startswith('#'):
                        continue

                    negate = line.startswith('!')
                    if negate:
                        line = line[1:].lstrip()
                        if not line:
                            continue

                    dir_only = line.endswith('/')
                    has_slash = '/' in line.rstrip('/')

                    self.rules.append({
                        "pattern": line,
                        "dir_only": dir_only,
                        "negate": negate,
                        "has_slash": has_slash,
                    })

            print(f"✓ 已加载 {len(self.rules)} 条规则（含取反）")

        except Exception as e:
            print(f"❌ 读取 .gitignore 失败: {e}")
            sys.exit(1)

    def _match_rule(self, rule: dict, relative_path_str: str, is_dir: bool) -> bool:
        """按规则匹配路径，返回是否命中"""
        pattern = rule["pattern"]
        dir_only = rule["dir_only"]
        has_slash = rule["has_slash"]

        # 目录规则：匹配目录自身或其子路径
        if dir_only:
            normalized = pattern.rstrip('/')
            if relative_path_str == normalized or relative_path_str.startswith(normalized + '/'):
                return True
            return False

        # 带路径分隔的规则：按相对路径匹配
        if has_slash:
            return fnmatch.fnmatch(relative_path_str, pattern)

        # 无斜杠：匹配任意层级的基本名
        if fnmatch.fnmatch(Path(relative_path_str).name, pattern):
            return True
        # 额外处理目录命中：无通配符时，若任一父级目录名等于 pattern 也视为命中
        if pattern.isalpha() and pattern in relative_path_str.split('/'):
            return True
        return False

    def should_exclude(self, path: Path, is_dir: bool = False) -> bool:
        """
        判断路径是否应该被排除（支持 ! 取反，后匹配覆盖前匹配）
        返回 True 表示应该排除（不备份）
        """
        try:
            # 统一使用 POSIX 路径风格进行匹配
            relative_path_str = path.relative_to(self.project_root).as_posix()
        except ValueError:
            return False  # 不在项目根目录内，不处理

        # Git 风格：从上到下最后一次匹配决定去留
        matched = None
        for rule in self.rules:
            if self._match_rule(rule, relative_path_str, is_dir):
                matched = not rule["negate"]  # negate 表示显式允许

        return bool(matched)


def create_backup(project_root: Path, output_file: Path, filter_obj: GitignoreFilter):
    """创建备份压缩包"""

    # 统计信息
    total_files = 0
    excluded_files = 0
    included_files = 0

    print(f"\n{'='*60}")
    print(f"开始备份项目: {project_root}")
    print(f"输出文件: {output_file}")
    print(f"{'='*60}\n")

    try:
        with tarfile.open(output_file, 'w:gz') as tar:
            # 使用 os.walk 可在目录层级提前剪枝，避免进入已忽略目录
            for root, dirs, files in os.walk(project_root, topdown=True):
                root_path = Path(root)

                # 目录剪枝：命中忽略规则或 .git 时不再深入
                pruned_dirs = []
                for d in dirs:
                    dir_path = root_path / d
                    if d == '.git' or filter_obj.should_exclude(dir_path, is_dir=True):
                        print(f"  排除目录: {dir_path.relative_to(project_root)}")
                        excluded_files += 1
                        continue
                    pruned_dirs.append(d)
                dirs[:] = pruned_dirs

                for name in files:
                    path = root_path / name
                    total_files += 1

                    # 文件忽略判定
                    if '.git' in path.parts or filter_obj.should_exclude(path):
                        excluded_files += 1
                        print(f"  排除: {path.relative_to(project_root)}")
                        continue

                    arcname = path.relative_to(project_root)
                    tar.add(path, arcname=arcname)
                    included_files += 1
                    print(f"  备份: {arcname}")

        print(f"\n{'='*60}")
        print("备份完成!")
        print(f"{'='*60}")
        print(f"总文件数: {total_files}")
        print(f"已备份: {included_files} 个文件")
        print(f"已排除: {excluded_files} 个文件/目录")
        print(f"压缩包大小: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"{'='*60}")

        return True

    except Exception as e:
        print(f"\n❌ 备份失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='快速备份项目（根据 .gitignore 排除文件）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 基本用法（备份到 backups/gz/ 目录）
  python backups/快速备份.py

  # 指定输出文件
  python backups/快速备份.py -o my_backup.tar.gz

  # 指定项目根目录
  python backups/快速备份.py -p /path/to/project
        """
    )

    parser.add_argument(
        '-p', '--project',
        type=str,
        default='.',
        help='项目根目录路径（默认: 当前目录）'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='输出文件路径（默认: backups/备份_YYYYMMDD_HHMMSS.tar.gz）'
    )

    parser.add_argument(
        '-g', '--gitignore',
        type=str,
        default='.gitignore',
        help='.gitignore 文件路径（默认: .gitignore）'
    )

    args = parser.parse_args()

    # 解析路径
    project_root = Path(args.project).resolve()
    gitignore_path = Path(args.gitignore).resolve()

    if not project_root.exists():
        print(f"❌ 错误: 项目目录不存在: {project_root}")
        sys.exit(1)

    # 确定输出文件路径
    if args.output:
        output_file = Path(args.output).resolve()
    else:
        # 默认输出到 backups/gz/ 目录
        backup_dir = project_root / 'backups' / 'gz'
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = backup_dir / f'备份_{timestamp}.tar.gz'

    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 创建过滤器
    filter_obj = GitignoreFilter(gitignore_path, project_root)

    # 执行备份
    success = create_backup(project_root, output_file, filter_obj)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
