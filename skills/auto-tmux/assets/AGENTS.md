# skills/auto-tmux/assets Agent 指南

本目录只承载 auto-tmux 的外部资源入口。

## 规则

- 只允许保存指向仓库内 `tools/external/` 的相对软链接。
- 不要复制 `tmux` 或 `oh-my-tmux` 源码到本目录。
- 上游内容更新必须通过 `tools/external/` 下的 Git submodule 指针完成。
- 修改软链接后，运行 `find skills/auto-tmux/assets -maxdepth 1 -type l -printf '%p -> %l\n'` 核对目标。
