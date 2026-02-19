#!/bin/bash

# 一键备份项目脚本
# 自动读取 .gitignore 规则并排除匹配的文件
# bash backups/一键备份.sh

set -e

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 项目根目录（脚本所在目录的父目录）
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 项目backups目录
BACKUPS_DIR="${PROJECT_ROOT}/backups"

# 备份脚本路径（始终在项目的backups目录中）
BACKUP_SCRIPT="${BACKUPS_DIR}/快速备份.py"

# 检查备份脚本是否存在
if [ ! -f "${BACKUP_SCRIPT}" ]; then
    echo -e "${YELLOW}⚠️  错误: 备份脚本不存在${NC}"
    echo ""
    echo "备份工具应位于项目的 backups/ 目录中："
    echo "  ${BACKUPS_DIR}/"
    echo ""
    echo "请确保："
    echo "  1. 复制快速备份.py到 ${BACKUPS_DIR}/"
    echo "  2. 复制一键备份.sh到 ${BACKUPS_DIR}/"
    echo ""
    echo "或者使用方式："
    echo "  • 在项目根目录执行: bash backups/一键备份.sh"
    echo "  • 或直接执行: python3 backups/快速备份.py"
    exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}     项目快速备份工具${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}✓${NC} 找到备份脚本: backups/快速备份.py"

# 检查 Python3 是否可用
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  错误: 未找到 python3 命令${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} 项目目录: ${PROJECT_ROOT}"
echo -e "${GREEN}✓${NC} 备份脚本: ${BACKUP_SCRIPT}"
echo -e "${GREEN}✓${NC} Python 版本: $(python3 --version)"
echo ""

# 执行备份
echo -e "${YELLOW}▶ 正在执行备份...${NC}"
echo ""

# 切换到项目根目录
cd "${PROJECT_ROOT}"

# 运行备份脚本
python3 "${BACKUP_SCRIPT}"

# 检查执行结果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}     ✓ 备份完成！${NC}"
    echo -e "${GREEN}========================================${NC}"
else
    echo ""
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}     ✗ 备份失败${NC}"
    echo -e "${YELLOW}========================================${NC}"
    exit 1
fi
