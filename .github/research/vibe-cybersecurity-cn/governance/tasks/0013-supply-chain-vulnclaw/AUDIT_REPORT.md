# 供应链审计报告：VulnClaw

快照：`2026-09-02`。沙盒：`.sandbox/supply-0013/VulnClaw/`（gitignore 排除）。

## 元数据

| 项 | 结果 |
|---|---|
| 上游 | `https://github.com/Netw0rkNoob/VulnClaw` |
| 固定 commit | `76b14c34f1d511ef34ef8f77e09a3a83d20e0cd3` |
| star/fork | 3111 / 426（2026-09-02 截面） |
| 许可 | MIT（Copyright 2026 UncleC） |
| 版本 | v0.3.8（PyPI 同步） |
| 体量 | 13M；Python 54,841 行；83 个测试文件 |
| 定位 | AI 渗透测试 CLI：LLM Agent + MCP 工具链 + Skill 参考资料，自然语言驱动信息收集→漏洞发现→利用→报告 |

## 安全审计项

| 检查 | 结果 |
|---|---|
| 管道安装模式（curl\|sh / bash <( 等） | 无 |
| 代码投毒（eval/exec 滥用、base64、/dev/tcp） | 无；命中项均为注入检测/反序列化分析的功能代码 |
| 网络回传/外带（telegram/webhook/矿池） | 无；CHATGPT_TOKEN_URL 为官方 OAuth 端点；exfil 字面量为 MITRE ATT&CK 知识库 |
| 凭据处理 | `.env.example` 全部占位符（sk-your-key-here）；审计事件敏感字段自动脱敏 |
| Docker | 两阶段构建、非特权用户（uid 1000）、数据卷 /data、默认 0.0.0.0 有容器边界说明 |
| 嵌入式指令 | `CODEX_REDTEAM_MODE_SOURCE.md` 为来源声明：仅导入 4 个授权知识卡，明确排除 jailbreak/prompt patcher 素材；skill 参考资料化，不强制注入正文 |
| 上游 skill | 50+ 内置 skill（redteam-* 系列 30+）；导入的 4 个上游 skill 需抽样复核（未逐文件审计） |
| 工程成熟度 | CHANGELOG 显示子代理扇出预算硬顶（max_depth=2）、上下文脱敏、TUI 转义防注入、子进程三段式清理 |

## 结论

**通过（reference 级）**。架构理念（证据闸门、授权声明、资源预算）与项目治理高度一致，
值得作为 Agent 编排参考与 skill 知识交叉来源；不进入自动执行面。

## 风险记录

- 高自主渗透 Agent：执行面必须绑定 ScopeGrant 三通道授权（active-high）。
- 若引入依赖：固定 PyPI 版本 + hash 校验。
- 上游 chAng-L19/codex-redteam-mode 的 4 个导入 skill 需抽样审计。
- traffic 模块（mitmproxy/playwright）默认未启用，启用前单独评估。
