# auto-tmux assets

本目录只保存指向仓库内外部 submodule 的软链接入口，不保存上游源码副本。2026-10-14已将两个入口恢复为相对软链接，分别指向已登记的`.github/extensions/oh-my-tmux`与`.github/extensions/tmux`；法器登记记录当前目标，并由固定来源修订保留原0字节占位历史。链接修复只确认仓内路径关系，不等于执行、许可或效能验证，详见[法器登记](../../../context/faqi/data.json)。

Git历史核对确认，该偏差早于 `.github` 目录迁移：迁移提交 `99adc940a5660763a780c3abc6b4b77465600264` 的父提交中，旧路径 `skills/auto-tmux/assets/oh-my-tmux` 与 `tmux-src` 已是 0 字节普通文件；迁移前 README 虽要求软链接，实际文件却与迁移后同为Git空文件blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`。因此不能把问题归因于目录迁移，也没有可从该父提交恢复的有效软链接；此历史不证明更早曾存在可用链接。

| 入口 | 预期目标 | 当前状态 | 用途 |
|:---|:---|:---|:---|
| `oh-my-tmux` | `../../../tools/external/.tmux` | 相对软链接，关联`faqi-oh-my-tmux` | gpakosz/oh-my-tmux 配置参考 |
| `tmux-src` | `../../../tools/external/tmux` | 相对软链接，关联`faqi-tmux` | tmux 上游源码参考 |

初始化或更新 submodule（只准备目标仓库，不会把占位文件转换成软链接）：

```bash
git submodule update --init --recursive
```
