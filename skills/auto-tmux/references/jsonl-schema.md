# auto-tmux JSONL Schema Notes

本文件记录 `auto-tmux` 机器可读输出的字段约定。当前脚本优先保持零依赖，因此 `scripts/check-jsonl.sh` 只做轻量字段门禁，不替代完整 JSON Schema 校验器。

## swarm-result

来源：`scripts/swarm-results.sh --jsonl`

| 字段 | 含义 |
|:---|:---|
| `type` | 固定为 `swarm-result` |
| `created_at` | 导出时间，ISO 8601 |
| `swarm_dir` | 状态目录 |
| `id` | 任务 ID |
| `status` | `DONE`、`FAIL` 或 `BLOCKED` |
| `owner` | worker pane 或 owner 标识 |
| `text` | 任务描述 |
| `result` | 结果摘要 |

最小门禁：

```bash
skills/auto-tmux/scripts/check-jsonl.sh /tmp/ai-swarm-results.jsonl \
  --require-key type \
  --require-key id \
  --require-key status
```

## remote-readonly

来源：`scripts/remote-readonly.sh`

| 字段 | 含义 |
|:---|:---|
| `type` | 固定为 `remote-readonly` |
| `created_at` | 采集时间，ISO 8601 |
| `host` | SSH host 参数 |
| `session` | tmux session，未指定时为 `<all>` |
| `lines` | 每个 pane 采集的行数 |
| `evidence_file` | 默认 `remote-tmux.txt` |
| `evidence_bytes` | 脱敏后证据文件字节数 |
| `evidence_lines` | 脱敏后证据文件行数 |
| `evidence_sha256` | 脱敏后证据文件 SHA-256；无 `sha256sum` 时为空 |
| `read_only` | 固定为 `true` |
| `redacted` | 固定为 `true` |

最小门禁：

```bash
skills/auto-tmux/scripts/check-jsonl.sh /tmp/auto-tmux-remote/metadata.jsonl \
  --require-key type \
  --require-key evidence_file \
  --require-key read_only \
  --require-key redacted
```

## auto-tmux-swarm-report-pack

来源：`scripts/swarm-report-pack.sh`

`manifest.json` 是单个 JSON 对象，不是 JSONL。当前由 `validate-auto-tmux.sh` 直接检查关键字段。

| 字段 | 含义 |
|:---|:---|
| `type` | 固定为 `auto-tmux-swarm-report-pack` |
| `created_at` | 打包时间，ISO 8601 |
| `swarm_dir` | 状态目录 |
| `session` | tmux session，未指定时为 `<not provided>` |
| `files` | 报告包核心文件列表 |
| `attachments` | 显式 `--attach` 加入的证据目录列表 |

## 维护规则

- 新增机器可读输出时，先写清字段含义，再把最小字段门禁接入 `validate-auto-tmux.sh`。
- 能用 Bash 轻量检查的字段，用 `check-jsonl.sh` 兜底；需要严格解析时再引入成熟 JSON Schema 工具。
- 证据字段默认描述脱敏后的文件，不记录原始敏感输出。
