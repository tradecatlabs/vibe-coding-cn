"""自有检查器共享的资源边界；迁移不扩大原有第三方/来源镜像检查范围。"""
from pathlib import Path

VENDOR_SUBTREES = tuple(map(Path, (
    '.github/extensions/Skill_Seekers-development',
    '.github/extensions/claude-official-skills',
    '.github/extensions/tmux',
    '.github/extensions/oh-my-tmux',
)))
SOURCE_PREFIXES = VENDOR_SUBTREES + tuple(map(Path, (
    '.github/wiki',
    '.github/context/research/vibe-cybersecurity-cn',
    '.github/context/research/vibe-harness-cn',
    '.github/context/research/vibe-mathing-cn-public',
    '.github/context/research/facts',
)))


def is_research_repository_snapshot(relative):
    parts = Path(relative).parts
    return (len(parts) >= 6 and parts[:3] == ('.github', 'context', 'research')
            and parts[4:6] == ('raw', 'repository'))
