# skills/auto-tmux/scripts

本目录承载 `auto-tmux` 的可执行脚本层。脚本必须安全封装 tmux 常用操作，减少手写 `capture-pane` / `send-keys` 时的误控风险。

## 目录结构

```text
scripts/
├── AGENTS.md       # 本文件：脚本维护规则
├── README.md       # 面向人类的脚本入口说明
├── auto-tmux.sh    # 统一 tmux 自动化命令入口
├── swarm-state.sh  # 蜂群状态、任务、锁和报告管理
├── swarm-brief.sh  # 只读生成蜂群交接报告
├── swarm-watch.sh  # 有限轮次只读巡检和状态采样
├── swarm-archive.sh # 打包 brief、snapshot 和 swarm state
├── safety-check.sh # 发送/粘贴/分发前的 payload 安全预检
├── render-swarm-prompt.sh # commander/worker/reviewer 提示词渲染
├── swarm-dispatch.sh # 渲染并可选下发蜂群提示词
├── auto-tmux-smoke-test.sh # 临时 tmux 会话端到端自测
└── validate-auto-tmux.sh # auto-tmux 专属质量门禁
```

## 维护规则

- 脚本必须使用 Bash 标准能力，不引入额外运行时依赖。
- 发送按键类功能必须先验证目标 pane 存在，并优先打印上下文。
- 捕获输出默认脱敏；只有显式 `--no-redact` 才允许输出原文。
- 批量救援必须通过 pattern 匹配触发，不允许无条件向所有 pane 发送输入。
- 批量广播必须要求显式 session，并支持 `--dry-run`。
- Prompt 渲染脚本只输出文本，不直接控制 tmux。
- Prompt 下发脚本默认只写文件；真实发送必须显式 `--send`，批量使用前先 `--dry-run`。
- 交接报告脚本只读调用 doctor/topology/scan/report，不直接发送按键。
- 巡检脚本必须是有限轮次，不允许默认无限循环。
- 归档脚本只复制状态和只读证据，不修改 tmux pane 或 swarm state。
- 安全预检脚本只能读取文本或文件，不控制 tmux，不写状态目录。
- 状态脚本只能写入显式状态目录，不保存密钥、Token、密码或私密项目内容。
- 自测脚本必须创建独立临时 tmux session，并在退出时清理。
- 专属校验脚本必须覆盖脚本权限、语法、help 输出、关键索引、strict 校验和 smoke test。
- 新增脚本后必须更新 `README.md`、`SKILL.md`、`references/index.md`，并运行 `bash -n` 与 skill strict 校验。
