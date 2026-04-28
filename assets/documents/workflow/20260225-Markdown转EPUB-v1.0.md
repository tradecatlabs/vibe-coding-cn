---
title: "Markdown 转 EPUB（ebook-convert/Calibre）可复现执行文档"
asset_id: "ASSET-EPUB-MD2EPUB-20260225-3c7a9d1e"
version: "v1.0"
date: "2026-02-25"
maintainer: "<占位符>"
scope:
  - "Windows 环境下单个 Markdown 转 EPUB"
  - "以 Calibre ebook-convert 为核心的可复现转换流程（含证据与自检）"
non_scope:
  - "复杂排版需求（大量公式/引用文献/高级 Markdown 扩展）"
  - "DRM/受保护格式处理与分发合规审查"
min_input:
  - "Markdown 文件路径（绝对路径或相对路径）"
  - "书籍元数据（标题/作者/语言，可自动从 Markdown 头部提取）"
output_spec:
  deliverable_type: "EPUB 文件（主交付物）+ 可追溯证据（版本/日志/报告）"
  must_include:
    - "输出 EPUB 文件路径（可直接打开验证）"
    - "关键证据：工具版本、转换命令、转换日志/报告、自检结论"
  quality_bar:
    - "EPUB 可被 Calibre 或常见阅读器打开，且目录（NCX/NAV）存在"
    - "转换无 ERROR，输出文件大小非空且显著大于 0（建议 > 10KB）"
change_log:
  - ver: "v1.0"
    date: "2026-02-25"
    changes: "初始化"
tags:
  - "calibre"
  - "ebook-convert"
---

<!-- markdownlint-disable MD013 -->

## Markdown 转 EPUB（ebook-convert/Calibre）可复现执行文档

## 上下文背景（任务上下文源）

### 2.1 当前任务一句话背景

- 将 `C:\Users\lenovo\Downloads\逻辑 - 孟自黄.md` 转换为 EPUB，并完成工具选型与可复现构建（最终选用 Calibre `ebook-convert`）。

### 2.2 业务/项目背景要点（可选）

- 无/不适用

### 2.3 会话上下文源定义（默认信息源与优先级）

#### 2.3.1 信息源优先级（从高到低）

1. 会话内用户明确提供/确认的信息（含粘贴文本/附件/链接）
1. 会话内 AI 已执行得到的证据（命令输出/读到的文件片段）
1. 本地工作区文件与仓库（如存在）
1. 外部来源（仅限用户提供链接；若允许检索则必须记录链接与摘录为证据）
1. 必要时向用户提最少问题补齐

#### 2.3.2 工作目录/项目根定位规则（按需）

- 默认以会话提供的 `cwd` 作为工作目录；若输入为绝对路径，则以 Markdown 所在目录作为 `source-root`（用于解析本地资源）。

#### 2.3.3 关键文件/目录（README等）

- `C:\Users\lenovo\Downloads\逻辑 - 孟自黄.md`
- `C:\Users\lenovo\Downloads\逻辑 - 孟自黄.epub`
- `C:\Users\lenovo\Downloads\build_epub\report.json`
- `C:\Users\lenovo\.codex\skills\markdown-to-epub\scripts\build_epub.py`

#### 2.3.4 Git 状态/变更/提交历史（按需）

- 不适用（本任务不依赖 Git；如在仓库内执行，提交/推送/合并属于高风险动作，必须先请求用户批准）

#### 2.3.5 日志/配置/脚本/依赖信息

- 工具：Calibre `ebook-convert`（证据：`ebook-convert --version` 输出 `calibre 8.16.2`）
- 运行时：Python（证据：`python --version` 输出 `Python 3.14.2`）
- 可选工具：Pandoc（证据：`pandoc --version` 在本会话环境中不可用/未安装）
- 构建脚本（可选但推荐）：`C:\Users\lenovo\.codex\skills\markdown-to-epub\scripts\build_epub.py`（对本地图片与证据报告更友好；底层仍调用 `ebook-convert`）

#### 2.3.6 外部来源使用规则（按需）

- 默认仅用用户提供链接；本任务未使用外部链接检索

### 2.4 关键约束/假设（可选）

- 约束：尽量不改动源 Markdown；输出文件可覆盖需先征得用户同意
- 假设：输入 Markdown 为 UTF-8（本会话证据：用 `utf-8/utf-8-sig` 可正确解码，`gb18030/gbk/big5` 解码失败）

## 任务方法（可复现执行体：复制即让 AI 照着跑，必须可复现）

### A. 目标 & 成功标准

- 目标：将指定 Markdown 转为 EPUB（使用 `ebook-convert`），并落盘可追溯证据（版本/日志/报告/自检结论）
- 成功标准：
  - [ ] 产出 EPUB 文件，路径明确且可打开
  - [ ] EPUB 包含 OPF 且存在 NCX 或 NAV（目录可用）
  - [ ] 元数据（标题/作者/语言）正确
  - [ ] 关键内容结构不丢失（至少校验：章节标题与表格/段落）

### B. 复现总规则

- 少问用户、优先补齐；高风险先批准；每步记录证据；可回滚

### C. 复现主流程（Replay Workflow）

> 必须包含 Step1~Step6；每个 Step 严格按：输入→动作→证据→输出→自检→兜底

#### Step1 定位上下文

- 输入：
  - Markdown 路径："<输入 Markdown 路径>"
  - 工作目录（若给出）："<cwd 或占位符>"
- 动作（命令/读文件/搜索）：
  - 在 PowerShell 中确认文件存在：
    - `Test-Path -LiteralPath "<输入 Markdown 路径>"`
  - 读取开头 60 行用于提取标题/作者（注意编码）：
    - `Get-Content -LiteralPath "<输入 Markdown 路径>" -Encoding utf8 -TotalCount 60`
- 证据：
  - 记录 `Test-Path` 结果（True/False）
  - 记录前 60 行中是否存在 `# <标题>`、`**作者**：<作者>` 等可提取信息
- 输出：
  - 输入文件绝对路径
  - 可能的元数据候选：标题/作者/语言（若可从 Markdown 头部提取）
- 自检：
  - 若 `Get-Content` 输出乱码，优先改用 `-Encoding utf8`；仍异常则进入 Step2 做编码确认
- 兜底：
  - 若文件不存在：请求用户确认路径或提供文件
  - 若路径含空格/特殊字符：所有命令统一使用 `-LiteralPath` 或对参数加双引号

#### Step2 自动补全

- 输入：
  - Step1 的元数据候选（可能为空）
- 动作（命令/读文件/搜索）：
  - 检查 `ebook-convert` 是否可用并记录版本：
    - `ebook-convert --version`
  - （可选）检查 `pandoc` 是否可用（仅用于信息收集，不作为主路径）：
    - `pandoc --version`
  - 如需确认编码（推荐仅在出现乱码/异常时做）：
    - 运行 Python 尝试以 UTF-8 解码并打印前几行（示例）：
      - `@' ... '@ | python - "<输入 Markdown 路径>"`
- 证据：
  - `ebook-convert --version` 输出（例如：`ebook-convert.exe (calibre 8.16.2)`）
  - `pandoc --version` 输出或失败信息（若失败也需记录）
  - 编码确认输出（例如：`utf-8 -> # 逻辑 | **作者**：孟自黄 ...`）
- 输出：
  - 最终采用的工具与路径：优先 `ebook-convert`（Calibre）
  - 最终元数据：标题/作者/语言（无法自动提取则保留 `<占位符>` 待用户确认）
- 自检：
  - 若 `ebook-convert` 不可用：进入 E.4（环境异常）
- 兜底：
  - 若元数据无法自动提取：仅向用户提最少问题（标题/作者/语言）

#### Step3 计划

- 输入：
  - 输入 Markdown 路径
  - 输出 EPUB 目标路径（若未指定则默认与输入同目录/同名）
  - 元数据（标题/作者/语言）
- 动作（命令/读文件/搜索）：
  - 明确两条执行路径（按内容复杂度择一）：
    - 路径 A（最小路径）：直接调用 `ebook-convert` 生成 EPUB
    - 路径 B（稳健路径，仍以 `ebook-convert` 为核心）：使用构建脚本生成报告与可追溯证据（适合有本地图片/需要报告/需要更强可复跑性）
  - 检查是否会覆盖文件/删除目录（不可逆需先批准）：
    - 若输出 EPUB 已存在：必须先问用户是否覆盖
    - 若要清理构建目录（例如 `build_epub`）：必须先问用户是否允许删除
- 证据：
  - 记录用户对“覆盖/清理”的明确批准或拒绝
  - 记录最终选择的执行路径（A 或 B）及理由（1 句话）
- 输出：
  - 可执行命令（单条或两条）+ 预计输出路径
- 自检：
  - 命令必须非交互式；路径包含空格时必须加引号
- 兜底：
  - 若用户拒绝覆盖：改用新文件名（例如追加日期或版本号）
  - 若用户拒绝清理：禁用清理参数，改为新建 build 目录（例如 `build_epub_<YYYYMMDDHHMM>`）

#### Step4 执行取证

- 输入：
  - 最终确认的执行路径（A 或 B）
  - 输出 EPUB 路径
  - 元数据（标题/作者/语言）
- 动作（命令/读文件/搜索）：
  - 路径 A（直接转换）示例：
    - `ebook-convert "<输入 Markdown 路径>" "<输出 EPUB 路径>" --title "<标题>" --authors "<作者>" --language "<语言>"`
  - 路径 B（稳健转换，底层仍用 ebook-convert；推荐用于留证与处理本地资源）示例：
    - `python "C:/Users/lenovo/.codex/skills/markdown-to-epub/scripts/build_epub.py" --input-md "<输入 Markdown 路径>" --output-epub "<输出 EPUB 路径>" --title "<标题>" --authors "<作者>" --language "<语言>" --clean-build-dir`
  - 注意：`--clean-build-dir` 会删除构建目录，属于不可逆动作；执行前必须有用户批准
- 证据：
  - 记录完整命令行（含所有参数）
  - 记录命令输出（stdout/stderr）与生成的日志/报告路径
  - 本会话转换成功证据（示例摘要，供对照）：

    ```json
    {
      "output_epub": "C:\\Users\\lenovo\\Downloads\\逻辑 - 孟自黄.epub",
      "build_dir": "C:\\Users\\lenovo\\Downloads\\build_epub",
      "total_image_refs": 0,
      "missing_images": [],
      "epub": {
        "file_size": 158236,
        "has_opf": true,
        "has_ncx_or_nav": true,
        "ncx_nav_points": 58
      }
    }
    ```

- 输出：
  - 生成的 EPUB 文件（路径）
  - （若路径 B）构建目录与报告：`build_epub\report.json`、`build_epub\conversion.log`
- 自检：
  - 校验输出文件存在且大小合理（建议 > 10KB）
- 兜底：
  - 若转换失败：收集错误信息并进入 E.4
  - 若提示编码相关问题：优先确保输入为 UTF-8 或在工具侧指定编码/改用稳健路径 B

#### Step5 自检验收

- 输入：
  - 输出 EPUB 路径
  - （若有）报告 JSON 路径
- 动作（命令/读文件/搜索）：
  - 最小自检（结构完整性）：
    - （路径 B 已自动生成）检查 `report.json` 中 `has_opf`、`has_ncx_or_nav`、`missing_images`
  - 内容自检（抽样验证关键文本存在）示例：
    - 用 Python 读取 EPUB（zip）并搜索标题/作者/关键句：
      - 搜索 `"逻辑"`、`"孟自黄"` 是否在 HTML 中出现
  - 表格自检（如 Markdown 含表格）：
    - 搜索表格关键行是否被转换为 `<table>`（例如包含 `"妥善处理污水"` 的表格）
- 证据：
  - 本会话自检证据（示例）：
    - 在 EPUB 内找到标题与作者：`found in index_split_000.html`
    - 表格存在：`has_table True`，`tr_count 6`
- 输出：
  - 验收结论（通过/不通过）+ 不通过原因（若有）
- 自检：
  - 若发现目录缺失、章节结构异常：回到 Step3 调整分章/目录策略（必要时改用稳健路径 B）
- 兜底：
  - 若阅读器显示乱码：优先确认输入/转换链路全程 UTF-8，并检查语言参数（`--language "zh-CN"`）

#### Step6 交付落盘更新

- 输入：
  - 最终通过验收的 EPUB 文件
  - 证据材料（命令输出/日志/报告/自检结论）
- 动作（命令/读文件/搜索）：
  - 交付文件落盘（若需归档目录，先确认目标路径存在）：
    - 将 EPUB 与证据文件（`report.json`、`conversion.log`）复制到用户指定目录
  - 更新本资产文档（如复跑后遇到新分支/新坑）：
    - 版本号 `v1.0 -> v1.1`，并在 `change_log` 新增一条记录
- 证据：
  - 记录最终交付路径清单（EPUB + 报告/日志）
  - 记录校验结论（Step5 输出）
- 输出：
  - 最终交付物路径列表
- 自检：
  - 确保交付路径下文件齐全且可打开
- 兜底：
  - 若用户不需要报告/日志：至少保留 `ebook-convert --version` 与最终命令行作为最小证据

### D. 固定步格式（强制约束）

- 每步必须且仅包含：输入 / 动作 / 证据 / 输出 / 自检 / 兜底

### E. 必要分支

#### E.1 信息不足

- 触发条件：
  - 无法从 Markdown 头部可靠提取标题/作者/语言，或用户未提供输出路径与覆盖策略
- 最小问题集（最多 3 个）：
  1. 输出 EPUB 文件名/路径是否固定？若已存在是否允许覆盖？
  1. 书籍元数据：标题、作者（语言默认 `zh-CN` 是否接受）？
  1. 是否需要生成/保留证据（report/log）用于复跑与追溯？
- 默认策略（用户不回时）：
  - 不覆盖任何既有文件；输出文件名追加日期；语言默认 `zh-CN`；保留最小证据（版本+命令行）

#### E.2 信息冲突

- 触发条件：
  - 标题/作者在文件头部与用户口述不一致；或同名输出文件存在但覆盖策略不明确
- 冲突点清单：
  - "<占位符>"
- 推荐决策与理由：
  - 以“用户明确确认”的元数据为准；若未确认，以 Markdown 文件头部为准（并在交付中标注来源）
- 需要用户批准的选项：
  - 覆盖现有输出文件
  - 删除/清理构建目录（如 `--clean-build-dir`）

#### E.3 时间紧（先交付 MVP）

- 触发条件：
  - 用户只要尽快拿到可读 EPUB，不要求详尽证据或复杂校验
- MVP 交付定义：
  - 直接 `ebook-convert` 生成 EPUB；仅做“能打开 + 目录存在 + 标题/作者正确”的最小自检
- 后续迭代清单：
  - 增加报告落盘（report/log）
  - 增加内容抽样自检（关键章节/表格/脚注）
  - 增加图片资产归一化（若后续出现本地图片）

#### E.4 命令失败/环境异常

- 触发条件：
  - `ebook-convert` 不存在/不可执行；转换报错；输出 EPUB 不生成或损坏
- 诊断步骤：
  1. `ebook-convert --version` 是否可用
  1. 记录完整错误输出（stderr）
  1. 检查输入文件编码与路径（空格/中文/权限）
  1. 若为资源问题（图片缺失）：改用稳健路径 B 并查看 `missing_images`
- 回退/替代方案：
  - 安装/修复 Calibre 后重试
  - 不清理构建目录，换新 build 目录与新输出名避免破坏现有文件
- 需要用户提供的信息（最少）：
  - 错误输出全文
  - 输入 Markdown 路径与（若有）相关资源文件目录结构截图/列表

### F. 交付模板（最终输出格式/命名/落盘路径）

- 命名规则：`YYYYMMDD-Markdown转EPUB-<版本>.md`
- 落盘路径：`<项目根>/docs/Markdown转EPUB/`
- 交付物模板：
  - 交付文件：
    - "<输出 EPUB 路径>"
  - 证据索引：
    - EVID-001 工具版本：`ebook-convert --version` 输出
    - EVID-002 转换命令：最终命令行全文
    - EVID-003 转换日志/报告（如有）：`conversion.log`、`report.json`
    - EVID-004 自检结论：目录存在/元数据命中/关键内容抽样命中

### G. 更新规则（用完写回：版本 + 0.1）

- 每次复跑后将新坑/新分支写回 D/E/F，并把版本 `v1.0 → v1.1`；变更记录新增一条
