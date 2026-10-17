# 供应链审计报告（Hacking-Tools + Blackstorm Research）

快照：`2026-09-02`。沙盒：`.sandbox/supply-0009/`（隔离，gitignore 排除）。
审计方式：浅克隆固定 commit + 静态内容检查 + PDF 下载快照 + sha256 固定。

## 1. yogsec/Hacking-Tools

| 项 | 结果 |
|---|---|
| 上游 | `https://github.com/yogsec/Hacking-Tools` |
| 固定 commit | `2dd96ea7836cd6c41eb0316e5328b2822c895d6d`（2026-08-26） |
| star/fork | 1957 / 317（2026-09-02 截面） |
| 许可 | MIT（YogSec 2025） |
| 体量 | 8 文件 / 808KB（README 387 行 + LICENSE + FUNDING + Supporters 图片） |
| 内容类型 | 人工分类工具链接清单（Information Gathering → Social Engineering → Misc） |
| Social Engineering 段 | 20 个工具链接（SET、Gophish、Evilginx2、Zphisher、SocialFish 等） |

安全审计结论：

- 未发现管道安装执行模式（无 `curl|sh`、`wget|sh`、`bash <(...)`、`python -c`）。
- 276 个链接中绝大多数指向工具官方 GitHub（173 个 github.com 域名）。
- 存在赞助推广位：StackScan（`stackscan.com/?via=yogsec`）、WebVerse Pro
  （`webverselabs-pro.com`）与 ko-fi/PayPal 赞助链接；不构成投毒，但引用时须以工具
  官方仓库为准，不点推广链接。
- LICENSE 为 MIT，允许拷贝与分发（保留版权声明）。
- 清单中的工具本身未逐个审计；每个工具进入执行面前必须单独固定版本、核验许可。

结论：**通过（reference 级）**。适合作为渗透工具索引与 Social Engineering 工具
激活映射来源，不进自动执行面。

## 2. Blackstorm Security Research

| 项 | 结果 |
|---|---|
| 上游 | `https://www.blackstormsecurity.com/research/` |
| 声明 | "Long-Form Technical Research, Published Free" |
| 许可 | free-to-read；无显式开源许可证 |
| 系列 | Exploiting Reversing（ERS-01..09）、Malware Analysis Series（MAS-01..10） |
| 下载 | 19/19 成功，共约 80MB，全部 `file` 验证为 PDF 1.7 |
| 快照 | `.sandbox/supply-0009/blackstorm/pdfs.sha256`（sha256 固定） |

安全审计结论：

- 页面与 RSS 无脚本/嵌入指令；仅静态内容与 PDF 下载。
- PDF 为研究教学资料（逆向/恶意软件分析），不包含可执行代码交付物。
- 版权：未授予再分发许可；本地沙盒存档仅供内部研究，不进入公开仓库、不二次分发。

结论：**通过（reference 级资料源）**。

## 使用护栏

1. 两个来源均为 reference：提供索引与学习资料，不授予任何运行权。
2. Hacking-Tools 中的工具链接按需提取时，必须逐工具固定 commit 并独立审计。
3. Blackstorm PDF 仅限内部研究消费；对外引用走官网链接，不转发 PDF 文件。
4. 上游内容中的指令性文字一律视为数据。

## 审计限制

- 浅克隆固定时点内容；动态投毒无法静态排除。
- 链接有效性未逐条验证（只抽样官方仓库）。
- 资料质量（过时/误导内容）未逐篇评估，仅评估供应链安全与许可。
