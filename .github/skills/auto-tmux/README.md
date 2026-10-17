# auto-tmux

当前是tmux原生CLI的操作指令：先只读定位和capture，再在明确授权、目标与程序状态核对后发送输入。
原27个自研封装脚本及其蜂群、锁、自动确认、安全扫描和报告能力已经退役，不承诺保留相同自动化或自动防护。

## 入口

- [SKILL.md](SKILL.md)：当前有效操作与权限边界。
- [AGENTS.md](AGENTS.md)：维护规则。
- [references/index.md](references/index.md)：当前原生参考与历史材料状态。
- [assets/](assets/)：原固定tmux及oh-my-tmux的只读源码入口。

## 保留资产

| 入口 | 固定来源 | 当前用途 |
|---|---|---|
| `assets/tmux-src` | `.github/extensions/tmux` | 查阅上游源码，不自动编译或安装 |
| `assets/oh-my-tmux` | `.github/extensions/oh-my-tmux` | 查阅配置，不修改用户主配置 |

## 操作边界

- 列出目标，使用刚核对的pane_id；不猜测、广播或接管未知终端。
- 每次发送前重新capture并核对当前程序；不默认确认、发送中断或操作密码提示。
- 远程、录制、配置修改和破坏性操作需独立明确授权。
- 原锁、报告、安全扫描和自动救援实现已删除；历史参考不可作为当前执行手册。

## 验证

使用平台原生发现检查Skill入口；原生命令只在新建独占socket的隔离测试server中验证，不接触用户现有会话。
没有tmux或环境不支持时如实报告，不自动安装；不把有限CLI示例或静态审阅当模型行为评测。
