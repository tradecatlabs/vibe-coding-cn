# 原GitHub Actions定义（已停用）

用户要求清除workflows目录，因此原定义直接平铺至Extensions，`.github/workflows/`不再保留。
GitHub不会自动发现本目录的定义；自动CI、PR打标签和首次贡献者欢迎均已停用，不是换路径后仍在运行。

## 原定义与职责

| 原定义 | 保全位置 | 历史职责 |
|---|---|---|
| CI | [github-actions-ci.yml](github-actions-ci.yml) | 原Markdown、本地导航/结构/索引与外链检查 |
| Labeler | [github-actions-labeler.yml](github-actions-labeler.yml) | 原PR自动标签 |
| Welcome | [github-actions-welcome.yml](github-actions-welcome.yml) | 原首次Issue/PR贡献者欢迎 |

3份YAML保持原字节，包括历史路径注释、事件、权限、Action版本及平台secret表达式；保全不是执行或重新授权。
原目录规则已并入本域AGENTS，不保留第二份治理文件、空目录或符号链接。

## 本地检查与保护

- 从仓库根运行`make test`；其检查范围不缩减，也不自动执行以上定义。
- 主Ruleset和main经典保护仅移除已无Actions生产者的`markdown-lint`、`link-checker`必需检查。
- 签名、线性历史、PR、禁止强推/删除及原审批规则保留，不伪造成功checks或独立审核。
- 原目录不得重建；如需恢复自动化，必须显式授权，并共同恢复原生发现路径和对应检查生产者。
- 外链规则仍在仓库根`.lychee.toml`；本地`make test`不包含原Lychee公网外链任务，不声称同等远端覆盖。
