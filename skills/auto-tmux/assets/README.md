# auto-tmux assets

本目录只保存指向仓库内外部 submodule 的软链接入口，不保存上游源码副本。

| 入口 | 指向 | 用途 |
|:---|:---|:---|
| `oh-my-tmux` | `../../../tools/external/.tmux` | gpakosz/oh-my-tmux 配置参考 |
| `tmux-src` | `../../../tools/external/tmux` | tmux 上游源码参考 |

初始化或更新 submodule：

```bash
git submodule update --init --recursive
```
