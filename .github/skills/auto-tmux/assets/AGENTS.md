# .github/skills/auto-tmux/assets Agent 指南

本目录只承载 auto-tmux 的外部资源入口。

## 规则

- 只允许保存指向仓库内 `.github/extensions/` 的相对软链接。
- 不要复制 `tmux` 或 `oh-my-tmux` 源码到本目录。
- 上游内容更新必须通过 `.github/extensions/` 下的 Git submodule 指针完成。
- 修改软链接后，运行 `find .github/skills/auto-tmux/assets -maxdepth 1 -type l -printf '%p -> %l\n'` 核对目标。

## 当前状态与历史边界

当前`oh-my-tmux`和`tmux-src`均为相对软链接，分别指向已登记的`.github/extensions/oh-my-tmux`与`.github/extensions/tmux` submodule；`metadata/faqi.json`将链接分别关联到`faqi-oh-my-tmux`与`faqi-tmux`。固定来源修订`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`保留两条旧路径的0字节普通文件历史基线，校验器只允许登记目标与当前软链接精确匹配且目标属于`.gitmodules`已登记submodule。此链接修复不代表源码执行、许可或效能验证。`git submodule update`只更新目标仓库，不会创建或修复链接；`auto-tmux doctor`只检查路径存在，不能证明链接可用。

历史核对显示，偏差早于 `.github` 目录迁移：迁移提交 `99adc940a5660763a780c3abc6b4b77465600264` 的父提交中旧路径已是 0 字节普通文件，迁移前README虽要求软链接，实际Git blob仍为空。目录迁移不是这两个入口失效的根因；该历史也不证明更早曾存在有效链接。
