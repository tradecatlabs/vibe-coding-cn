# 外部资源导入质量报告

- 导入日期：2026-07-03
- 导入来源：`assets_csv.xlsx`
- 资源总数：287
- 缺失链接：5
- 非 URL 定位符：2
- 重复 URL 组数：6

## 分类统计

| 分类 | 文件 | 数量 |
|:---|:---|---:|
| 网络与支付服务 | `network-payment-services.yml` | 4 |
| 博主账号 | `creator-accounts.yml` | 18 |
| 工具与平台 | `tools-platforms.yml` | 68 |
| 社区与论坛 | `communities-forums.yml` | 15 |
| 仓库规则脚手架 | `repo-rules-scaffolds.yml` | 72 |
| 文档与课程 | `docs-courses.yml` | 21 |
| 书单 | `books.yml` | 75 |

## 需要人工复核

导入阶段只做结构化和字段归一化，以下项目需要人工复核后再作为推荐资源展示。

### 缺失链接

- `creator-accounts-1cab5d79`：博主账号 / 美国的牛粪博士 / source row 11
- `tools-platforms-gpt-5-1-codex-1ad522a5`：工具与平台 / GPT-5.1 Codex / source row 8
- `tools-platforms-gemini-2-5-pro-0661c69f`：工具与平台 / Gemini 2.5 Pro / source row 9
- `tools-platforms-local-history-2b05b2c1`：工具与平台 / Local History / source row 11
- `tools-platforms-partial-diff-4787875c`：工具与平台 / Partial Diff / source row 13

### 非 URL 定位符

- `creator-accounts-a057117e`：博主账号 / 科学小神牛 / `抖音自己搜`
- `tools-platforms-prompt-jsonl-8e9b2066`：工具与平台 / prompt_jsonl / `prompt_jsonl`

### 重复 URL

- `https://z-lib.fm/`：76 项；工具与平台 / Z-Library；书单 / 从零开始大模型开发与微调：基于PyTorch与ChatGLM - 王晓华；书单 / 编程的原则：改善代码质量的101个方法 - 上田勋；书单 / 生成式 AI 设计模式 - Valliappa Lakshmanan & Hannes Hapke；书单 / 人月神话 - 弗雷德里克·布鲁克斯；书单 / 人件（原书第3版） - Tom DeMarco & Timothy Lister；书单 / 高效程序员的45个习惯：敏捷开发修炼之道 - Andy Hunt & Venkat Subramaniam；书单 / 项目管理修炼之道 - 罗斯曼；等 76 项
- `https://chatgpt.com/`：2 项；工具与平台 / ChatGPT；工具与平台 / DALL-E 3
- `https://claude.ai/`：2 项；工具与平台 / Claude Opus 4.6；工具与平台 / Claude
- `https://geminicli.com/`：2 项；工具与平台 / Gemini CLI；工具与平台 / Gemini CLI
- `https://github.com/f/awesome-chatgpt-prompts`：2 项；仓库规则脚手架 / awesome-chatgpt-prompts；仓库规则脚手架 / Awesome ChatGPT Prompts
- `https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools`：2 项；仓库规则脚手架 / system-prompts-and-models-of-ai-tools；仓库规则脚手架 / System Prompts 仓库

### 风险标记统计

- `access-legality-review`：76
- `financial-service-review`：2
- `missing-link`：5
- `non-url-locator`：2
- `referral-or-tracking-link`：3

## 后续治理动作

- 对 `missing-link` 和 `non-url-locator` 补齐稳定 URL 或明确保留原因。
- 对 `referral-or-tracking-link` 判断是否保留推广参数，必要时改成 canonical URL。
- 对 `financial-service-review` 标注地区、风险边界和非投资建议。
- 对 `access-legality-review` 资源复核合法性、许可证和公开推荐风险。
- 对重复 URL 判断是同源不同对象，还是应该合并。

## 增量导入：ChatGPT 中文 Vibe Coding 仓库

- 导入日期：2026-07-03
- 导入来源：`ChatGPT-中文Vibe Coding仓库 (2).md`
- 检出仓库资源：17
- 新增仓库资源：13
- 更新既有仓库口径：2
- 跳过已存在仓库：2
- 新增工具资源：1
- 未导入上下文链接：1 个 ChatGPT 对话链接，仅作为来源上下文，不作为资源推荐。

### 新增仓库

- `datawhalechina/easy-vibe`
- `liyupi/ai-guide`
- `wendy7756/vibe-coding-guide`
- `Daotin/ai-coding`
- `earyantLe/vibe-coding-skill`
- `luzhenqian/ai-coding-lab`
- `ShouZhengAI/CS146S_CN`
- `filipecalegario/awesome-vibe-coding`
- `ai-for-developers/awesome-vibe-coding`
- `openai/codex`
- `RooCodeInc/Roo-Code`
- `shanraisshan/claude-code-best-practice`
- `hesreallyhim/awesome-claude-code`

### 更新既有仓库口径

- `tradecatlabs/vibe-coding-cn`
- `aider-ai/aider`

### 跳过已存在仓库

- `datawhalechina/vibe-vibe`
- `cline/cline`

### 新增工具

- `ChatGPT Exporter`
