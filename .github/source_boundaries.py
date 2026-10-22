"""自有检查器共享的排除边界；本机研究档案不参与公开仓库默认文档检查。"""
from pathlib import Path

VENDOR_SUBTREES = tuple(map(Path, (
    '.github/extensions/tmux',
    '.github/extensions/oh-my-tmux',
)))
SOURCE_PREFIXES = VENDOR_SUBTREES + tuple(map(Path, (
    '.github/wiki',
    '.github/context/research',
)))


def is_research_repository_snapshot(relative):
    parts = Path(relative).parts
    return (len(parts) >= 6 and parts[:3] == ('.github', 'context', 'research')
            and parts[4:6] == ('raw', 'repository'))
