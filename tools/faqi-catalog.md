<!-- generated: sync-faqi-catalog.py -->
# 法器清单与资源初审

来源限定的静态初审，不是效果、可用性、许可证或独立语义批准。仅修改[法器初审数据](../metadata/faqi.json)，不手改此视图。
类型与关系复用[唯一本体](../docs/gongfa/cultivation-ontology-taxonomy.md#唯一分类树)，不维护第二主树，不套功法四阶十二级。

## 总体概览

初审时间：2026-10-09T14:12:00+00:00；父仓库来源修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
本地入口 13 个，来源限定法器实现初审 16 条，另有 3 条明确范围排除；外部资源逐行分流 158 条。不是按目录或资源行计算独立产品数。
程序源码修订和下表声明版本不等于已核发布版、已安装版本或已部署入口；同内容副本、多入口不重复登记。

```text
+---------------------+------------+
| 外部分流状态        | 资源行数   |
|---------------------+------------|
| 软件实现候选        | 67         |
| 托管入口候选        | 22         |
| 排除：资料/规约内容 | 38         |
| 排除：模型名称所指  | 4          |
| 待核：对象身份      | 22         |
| 关联已审本地来源    | 2          |
| 待核：受限服务所指  | 3          |
+---------------------+------------+
```

## 本地来源限定法器

以下记录只指选定来源的程序指令内容；不同内容实现是否属于同一产品/派生版本，仍须另有演化证据。用途不作为主父。

```text
+-----------------------------+-----------------------------------+-------------------+--------------+
| 实现ID                      | 名称                              | 已有类型ID        | 实现来源ID   |
|-----------------------------+-----------------------------------+-------------------+--------------|
| faqi-prompt-converter       | 提示词格式转换程序                | software-artifact | S02          |
| faqi-codex-config-installer | Codex配置安装与恢复脚本           | software-artifact | S06          |
| faqi-auto-skill-create      | auto-skill模板生成脚本            | software-artifact | S08          |
| faqi-auto-skill-validate    | auto-skill结构校验脚本            | software-artifact | S09          |
| faqi-skill-seekers-adapter  | Skill Seekers本地运行适配脚本     | software-artifact | S10          |
| faqi-auto-tmux              | auto-tmux命令封装程序             | software-artifact | S12          |
| faqi-skill-seekers          | Skill Seekers程序                 | software-artifact | S16          |
| faqi-oh-my-tmux             | oh-my-tmux可执行配置程序          | software-artifact | S18          |
| faqi-tmux                   | tmux终端复用程序                  | software-artifact | S21          |
| faqi-claude-skill-init      | 官方Skill初始化脚本               | software-artifact | S23          |
| faqi-html-epub-css          | EPUB CSS清理网页程序              | software-artifact | S25          |
| faqi-html-markdown-text     | Markdown预览与文本导出网页程序    | software-artifact | S26          |
| faqi-html-task-card         | 任务卡片PNG导出网页程序           | software-artifact | S27          |
| faqi-html-xhs-card          | 小红书内容卡片PNG导出网页程序     | software-artifact | S28          |
| faqi-html-markdown-sync-png | Markdown同步预览与PNG导出网页程序 | software-artifact | S29          |
| faqi-my-nvim-lua            | my-nvim的LazyVim引导配置程序      | software-artifact | S32          |
+-----------------------------+-----------------------------------+-------------------+--------------+
```

### faqi-prompt-converter

提示词格式转换程序：指main.py及其转换实现所表达的程序内容；Excel、Markdown和JSONL是输入/输出，不随转换模式复制工具身份。未验证转换正确性。
实现来源 `S02`，佐证来源 `S01`；声明版本：未核/无明确发布版本声明。

### faqi-codex-config-installer

Codex配置安装与恢复脚本：纳入安装脚本的程序指令；不是Codex CLI实现，不包含账号授权，safe/power配置、全局指令文本另作规约内容。备份/覆盖能力尚未运行验证。
实现来源 `S06`，佐证来源 `S05`；声明版本：未核/无明确发布版本声明。

### faqi-auto-skill-create

auto-skill模板生成脚本：指渲染Skill模板与建立目录的程序，不是生成出的Skill内容或整个元技能。--force可覆盖目标，未执行。
实现来源 `S08`，佐证来源 `S07`；声明版本：未核/无明确发布版本声明。

### faqi-auto-skill-validate

auto-skill结构校验脚本：指frontmatter和结构校验程序；成功结构检查不证明Skill语义、执行正确或效果。
实现来源 `S09`，佐证来源 `S07`；声明版本：未核/无明确发布版本声明。

### faqi-skill-seekers-adapter

Skill Seekers本地运行适配脚本：设置venv/PYTHONPATH并exec上游CLI的本地适配程序。指令内容不同于上游核心，不能把封装当同一副本，也不因同一用途合并其他生成脚本。
实现来源 `S10`，佐证来源 `S07`；声明版本：未核/无明确发布版本声明。

### faqi-auto-tmux

auto-tmux命令封装程序：指统一操控脚本，不是SKILL.md、tmux二进制、session/pane或某次操作；支持多命令不增加身份。未发送按键、创建会话或读取pane。
实现来源 `S12`，佐证来源 `S11`；声明版本：未核/无明确发布版本声明。

### faqi-skill-seekers

Skill Seekers程序：指固定submodule修订的软件实现；多个CLI入口及可选MCP模块不机械复制产品身份。3.5.1仅为pyproject源码声明，不是已核发布或运行版。
实现来源 `S16`，佐证来源 `S14, S15`；声明版本：3.5.1（仅源码声明）。

### faqi-oh-my-tmux

oh-my-tmux可执行配置程序：配置文件含run、cut&#124;sh调用链及可执行shell指令，按实际程序内容归software-artifact，不能仅因.conf后缀归纯规约；不是tmux本身。
实现来源 `S18`，佐证来源 `S17, S19`；声明版本：未核/无明确发布版本声明。

### faqi-tmux

tmux终端复用程序：指固定源码修订的程序内容，不是物理终端、pane、socket地址或一次会话。Git describe的邻近tag不作为已核发布版本。
实现来源 `S21`，佐证来源 `S20`；声明版本：未核/无明确发布版本声明。

### faqi-claude-skill-init

官方Skill初始化脚本：只纳入skill-creator下生成目录/模板的独立Python程序，不把官方Skill集合、自然语言方法、模板或其他全部辅助脚本称作同一程序。
实现来源 `S23`，佐证来源 `S22`；声明版本：未核/无明确发布版本声明。

### faqi-html-epub-css

EPUB CSS清理网页程序：HTML内JavaScript负责读取、改写CSS和重新打包；是浏览器程序内容，不是纯文章。需JSZip等外部脚本，未启动浏览器或处理书籍。
实现来源 `S25`，佐证来源 `S24`；声明版本：未核/无明确发布版本声明。

### faqi-html-markdown-text

Markdown预览与文本导出网页程序：指marked驱动的预览/复制/文本导出实现；源码sanitize:false且innerHTML，不能把预览声明当安全处理不可信Markdown的证据。
实现来源 `S26`，佐证来源 `S24`；声明版本：未核/无明确发布版本声明。

### faqi-html-task-card

任务卡片PNG导出网页程序：指html2canvas驱动的任务卡片导出实现；卡片内容、导出图片和一次生成过程不等于程序。
实现来源 `S27`，佐证来源 `S24`；声明版本：未核/无明确发布版本声明。

### faqi-html-xhs-card

小红书内容卡片PNG导出网页程序：指可编辑内容卡片的PNG导出实现；不是图文资料或抓取客户端，未核依赖/CDN可用性。
实现来源 `S28`，佐证来源 `S24`；声明版本：未核/无明确发布版本声明。

### faqi-html-markdown-sync-png

Markdown同步预览与PNG导出网页程序：文件名带1.0，但实际title与指令所指为Markdown同步预览/调整宽度/PNG导出；不凭文件名当小红书产品版本。与其他页面内容不同，产品同一/前驱关系未批准。
实现来源 `S29`，佐证来源 `S24`；声明版本：未核/无明确发布版本声明。

### faqi-my-nvim-lua

my-nvim的LazyVim引导配置程序：Lua含git clone、异常分支、setup等可执行指令，不是纯参数表；是Neovim/LazyVim配置程序，不是Neovim实现。README v0.11.5指宿主Neovim，不作为配置版本。
实现来源 `S32`，佐证来源 `S30, S31`；声明版本：未核/无明确发布版本声明。

## 按本次范围排除的本地程序所指

下列源码确有程序实现所指，但应用户要求不作为本清单纳入对象；不代表它们不是软件。保留排除证据，重新纳入须满足各自复核条件。

### Chat Vault同步与查询程序

入口：`tools/chat-vault`；证据选区 `S04`；佐证选区 `S03`。
按用户指定从当前法器清单排除。源码会自动探测Codex/Kiro/Gemini/Claude会话目录，将消息/cwd写入SQLite，并提供搜索、导出、watch和prune；入口在参数解析前会创建虚拟环境并安装依赖。属于私人对话数据、运行安装及持久副作用边界；未读取数据或执行，排除不等于否认其程序实现。

重新纳入前：只有明确需要纳入时，再以合成会话和隔离临时目录验证数据最小化、路径授权、日志/数据库访问控制、导出/删除语义、依赖安装副作用及恢复；不得用真实用户会话做验证。

### Minecraft基岩版角色迁移程序

入口：`tools/external/MCPlayerTransfer`；证据选区 `S34`；佐证选区 `S33`。
按用户指定从当前法器清单排除。源码对.mcworld调用ZIP extractall，读取~local_player LevelDB记录；导入会写入LevelDB并以w模式创建目标归档。未验证不可信归档路径、目标文件覆盖、存档一致性和部分失败恢复；未处理真实存档，排除不等于否认其程序实现。

重新纳入前：如明确需要纳入，先在合成存档副本中验证归档路径/资源上限、无覆盖的临时输出、LevelDB读写一致性、失败清理与可恢复性；禁止用唯一真实存档作为测试输入。

### 小红书图片ZIP转PDF程序

入口：`tools/external/XHS-image-to-PDF-conversion`；证据选区 `S36`；佐证选区 `S35`。
按用户指定从当前法器清单排除。源码把外部ZIP解到输入旁固定temp_extract，运行前会递归删除同名目录；保存PDF后会删除原ZIP，异常时也会清理临时目录。缺少路径安全、覆盖保护、备份和失败恢复证据，未处理真实文件；排除不等于否认其程序实现。

重新纳入前：如明确需要纳入，先在隔离副本验证ZIP成员路径和展开上限、唯一随机临时目录、输入/PDF不覆盖、原ZIP保留、原子输出和所有失败路径恢复；不得使用真实业务ZIP测试。

## 13个本地入口的分离结果

### tools/prompts-library

本次纳入对象：`faqi-prompt-converter`。纳入程序，不把提示词资产或生成目录当工具实现。
佐证来源：`S01, S02`。

### tools/chat-vault

本次纳入对象：`无（见范围排除记录）`。代码确有会话同步/查询程序所指，但按本轮用户范围排除，不作为当前法器对象。
佐证来源：`S03, S04`。
- 待核：会话文件自动探测、SQLite持久化、搜索/导出及启动时环境创建/安装涉及私人数据和副作用；未运行，也未读取用户数据。

### tools/config/.codex

本次纳入对象：`faqi-codex-config-installer`。配置与AGENTS文本不等于CLI；脚本本身有独立程序所指。
佐证来源：`S05, S06`。
- 待核：Codex实际程序、已安装版本、权限及账户不由本目录证明。

### skills/auto-skill

本次纳入对象：`faqi-auto-skill-create, faqi-auto-skill-validate, faqi-skill-seekers-adapter`。Skill说明/规约与三个独立入口脚本分离，不把整Skill包登记成一件软件。
佐证来源：`S07, S08, S09, S10`。
- 待核：其他辅助模块未逐模块登记，不能将本次选区称为全包能力审查。

### skills/auto-tmux

本次纳入对象：`faqi-auto-tmux`。Skill方法/规约、执行脚本、被依赖程序及运行入口分别指认。
佐证来源：`S11, S12, S13`。
- 待核：两个assets引用实际上是零字节普通占位文件，不是README声称的软链接；本次记录缺口，不冒称已修复或上游源码可经此引用到达。
- 待核：蜂群附属脚本不逐一登记，不启动蜂群，也不将蜂群状态/日志算软件。

### tools/external/Skill_Seekers-development

本次纳入对象：`faqi-skill-seekers`。源码内容与仓库载体、接口规范、抓取过程、输入资料和生成Skill分开。
佐证来源：`S14, S15, S16`。
- 待核：CLI与MCP各实现的完整对应关系、许可/可用性与外部I/O权限未作完整审查。

### tools/external/.tmux

本次纳入对象：`faqi-oh-my-tmux`。配置数据与嵌入程序按实际所指区分；本条纳入可执行配置程序，未安装或source配置。
佐证来源：`S17, S18, S19`。
- 待核：源码含条件性kill-server；纳入不等于可安全对当前会话执行。

### tools/external/tmux

本次纳入对象：`faqi-tmux`。tmux程序与配置、操控封装、终端会话和显示记录分开。
佐证来源：`S20, S21`。

### tools/external/claude-official-skills

本次纳入对象：`faqi-claude-skill-init`。集合入口不等于法器身份；指令内容与脚本实现分别判断。
佐证来源：`S22, S23`。
- 待核：README明确部分文档Skill仅source-available，不能把整个集合称为同一开源许可证；本次不批准再分发/商用许可。
- 待核：其余辅助脚本未逐模块展开。

### tools/external/html-tools-main

本次纳入对象：`faqi-html-epub-css, faqi-html-markdown-text, faqi-html-task-card, faqi-html-xhs-card, faqi-html-markdown-sync-png`。五个页面确有不同JavaScript实现，登记来源限定内容记录，不按HTML目录或README宣传登记一件全能工具。
佐证来源：`S24, S25, S26, S27, S28, S29`。
- 待核：两个Markdown相关实现以及文件名“1.0”的产品同一/版本演化仍待核，不自动合并或填predecessor。
- 待核：README的index.html/tools/示意与当前目录实际平铺不同；“无需额外依赖”不等于无需网络/CDN脚本。

### tools/external/my-nvim

本次纳入对象：`faqi-my-nvim-lua`。配置程序、宿主Neovim、LazyVim依赖与说明宣传各有自己的所指。
佐证来源：`S30, S31, S32`。
- 待核：配置会尝试克隆插件并启用更新检查；未运行，未核实际依赖锁定或README“全面测试”主张。

### tools/external/MCPlayerTransfer

本次纳入对象：`无（见范围排除记录）`。代码确有存档角色提取/导入程序所指，但按本轮用户范围排除，不作为当前法器对象。
佐证来源：`S33, S34`。
- 待核：对压缩包extractall、LevelDB角色写入及目标归档直接写入的路径安全、覆盖、完整性和失败恢复未测试。

### tools/external/XHS-image-to-PDF-conversion

本次纳入对象：`无（见范围排除记录）`。代码确有ZIP图片转PDF程序所指，但按本轮用户范围排除，不作为当前法器对象。
佐证来源：`S35, S36`。
- 待核：源码固定temp_extract并先递归删除同名目录，解压外部ZIP、写PDF且成功后删除原ZIP；未运行或验证恢复。

## 静态依赖与引用入口

`requires`只记录源码/说明声明的依赖；相关本地实现ID是源码参照，不证明运行时加载了该版本，更不证明实际使用、符合协议或已获权限。

```text
+----------------------------+----------+------------------------------------+--------------------+----------+
| 主体实现                   | 谓词     | 依赖所指                           | 相关来源实现       | 证据ID   |
|----------------------------+----------+------------------------------------+--------------------+----------|
| faqi-auto-tmux             | requires | tmux程序（运行版本未知）           | faqi-tmux          | S13      |
| faqi-oh-my-tmux            | requires | tmux>=2.6及awk/perl/grep/sed       | faqi-tmux          | S17      |
| faqi-skill-seekers-adapter | requires | 链接源码中的skill_seekers.cli.main | faqi-skill-seekers | S10      |
| faqi-my-nvim-lua           | requires | Neovim运行环境、lazy.nvim和LazyVim | 未知               | S32      |
+----------------------------+----------+------------------------------------+--------------------+----------+
```

- `faqi-auto-tmux`：脚本调用PATH中的tmux；本地上游源码仅作相关参照，不证明实际安装二进制来自该修订。
- `faqi-oh-my-tmux`：README声明版本下限，不将配置修订误写成tmux版本，也不保证当前环境满足依赖。
- `faqi-skill-seekers-adapter`：源码路径确由软链接指到选定submodule；这是静态加载意图，venv实际依赖、Python解析和运行结果未核。
- `faqi-my-nvim-lua`：不把配置包当Neovim；源码可联网克隆/更新插件，实际宿主与依赖版本未绑定。

- `skills/auto-skill/scripts/Skill_Seekers-development`：`symlink`；目标 `../../../tools/external/Skill_Seekers-development`。同一仓库源码的引用入口，不新增法器副本；封装脚本另有指令内容。
- `skills/claude-official-skills`：`symlink`；目标 `../tools/external/claude-official-skills`。指向Skill集合而非一件软件，不能再因引用入口登记整集合。
- `skills/auto-tmux/assets/oh-my-tmux`：`empty-placeholder`；目标 `无`。实际Git模式100644、0字节；README称软链接，但此路径不能提供上游来源到达证据。
- `skills/auto-tmux/assets/tmux-src`：`empty-placeholder`；目标 `无`。实际Git模式100644、0字节；独立tmux源码已按真实submodule审，不把占位文件算副本。

## 158条外部资源逐行分流

名称、原ID、状态、验证状态与风险只读自原YAML。`active`与`imported-unverified`不证明可用、许可或推荐。
未核远端实现/版本的候选不登记为本地法器；模型名称所指与聊天平台分开。资料排除仅针对当前条目所指，不断言整个仓库没有程序。
同名或同网址只产生重复入口核查线索，不自动合并软件身份；网络/金融分流不授权开户、交易、账户读取或实际网络操作。

### 软件实现候选

原行明确描述程序、编辑器、CLI、插件、库或生成工具，保留软件实现候选；只有名称/介绍地址，未核具体实现、版本、许可证或能力，不直接赋型/登记。

```text
+-----------------------------------------------------+-----------------------+--------------+---------------------+--------------+
| 原资源ID                                            | 名称                  | 原状态       | 原验证状态          | 原风险标记   |
|-----------------------------------------------------+-----------------------+--------------+---------------------+--------------|
| tools-platforms-codex-cli-362bc20a                  | Codex CLI             | active       | imported-unverified | 无           |
| tools-platforms-droid-1b66f6e0                      | Droid                 | active       | imported-unverified | 无           |
| tools-platforms-docusaurus-09c54423                 | Docusaurus            | active       | imported-unverified | 无           |
| tools-platforms-vitepress-da10a919                  | VitePress             | active       | imported-unverified | 无           |
| tools-platforms-lazyvim-2f22a781                    | LazyVim               | active       | imported-unverified | 无           |
| tools-platforms-neovim-a8b85739                     | Neovim                | active       | imported-unverified | 无           |
| tools-platforms-pearai-0683754c                     | PearAI                | active       | imported-unverified | 无           |
| tools-platforms-vs-code-e8f2d385                    | VS Code               | active       | imported-unverified | 无           |
| tools-platforms-void-b1594346                       | Void                  | active       | imported-unverified | 无           |
| tools-platforms-django-e05156b6                     | Django                | active       | imported-unverified | 无           |
| tools-platforms-excalidraw-02ba0cb2                 | Excalidraw            | active       | imported-unverified | 无           |
| tools-platforms-mermaid-cc6f6e7e                    | Mermaid               | active       | imported-unverified | 无           |
| tools-platforms-dbeaver-aa2fc821                    | DBeaver               | active       | imported-unverified | 无           |
| tools-platforms-tableplus-9950f31a                  | TablePlus             | active       | imported-unverified | 无           |
| tools-platforms-warp-14bec77a                       | Warp                  | active       | imported-unverified | 无           |
| tools-platforms-claude-code-11b1e88d                | Claude Code           | active       | imported-unverified | 无           |
| tools-platforms-opencode-ada070db                   | OpenCode              | active       | imported-unverified | 无           |
| tools-platforms-gemini-cli-d077e5cc                 | Gemini CLI            | active       | imported-unverified | 无           |
| tools-platforms-gemini-cli-row40-d077e5cc           | Gemini CLI            | active       | imported-unverified | 无           |
| tools-platforms-qwen-cli-a1b92a34                   | Qwen CLI              | active       | imported-unverified | 无           |
| tools-platforms-bito-0c0619b5                       | Bito                  | active       | imported-unverified | 无           |
| tools-platforms-codeium-668488a9                    | Codeium               | active       | imported-unverified | 无           |
| tools-platforms-continue-edb7b3bf                   | Continue              | active       | imported-unverified | 无           |
| tools-platforms-cursor-8ebf3977                     | Cursor                | active       | imported-unverified | 无           |
| tools-platforms-zed-07b4820e                        | Zed                   | active       | imported-unverified | 无           |
| tools-platforms-chatgpt-exporter-a03efe97           | ChatGPT Exporter      | active       | imported-unverified | 无           |
| repo-rules-scaffolds-autogen-fc00be5e               | autogen               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-browser-use-268f0f95           | browser-use           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-crewai-d9a56566                | crewai                | active       | imported-unverified | 无           |
| repo-rules-scaffolds-dspy-d8bdba82                  | dspy                  | active       | imported-unverified | 无           |
| repo-rules-scaffolds-langchain-089a07ab             | langchain             | active       | imported-unverified | 无           |
| repo-rules-scaffolds-pydantic-ai-cb69369e           | pydantic-ai           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-smolagents-790ade5e            | smolagents            | active       | imported-unverified | 无           |
| repo-rules-scaffolds-aider-adccc23a                 | aider                 | active       | imported-unverified | 无           |
| repo-rules-scaffolds-claude-code-ef1ef8b6           | claude-code           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-cline-644a6623                 | cline                 | active       | imported-unverified | 无           |
| repo-rules-scaffolds-continue-d5516851              | continue              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-gemini-cli-be45a9ce            | gemini-cli            | active       | imported-unverified | 无           |
| repo-rules-scaffolds-gpt-engineer-eaa2e8a8          | gpt-engineer          | active       | imported-unverified | 无           |
| repo-rules-scaffolds-oh-my-opencode-0348827b        | oh-my-opencode        | active       | imported-unverified | 无           |
| repo-rules-scaffolds-open-interpreter-a514262e      | open-interpreter      | active       | imported-unverified | 无           |
| repo-rules-scaffolds-opencode-e1b762af              | opencode              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-spec-kit-a9a40ae2              | spec-kit              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-avante-nvim-29a0c49f           | avante.nvim           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-codecompanion-nvim-a6f68dc2    | codecompanion.nvim    | active       | imported-unverified | 无           |
| repo-rules-scaffolds-codeium-b0b85053               | codeium               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-copilot-vim-c06b7933           | copilot.vim           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-gitingest-ee7a3f76             | gitingest             | active       | imported-unverified | 无           |
| repo-rules-scaffolds-jan-c4cdcb50                   | jan                   | active       | imported-unverified | 无           |
| repo-rules-scaffolds-lmstudio-8b9fe81d              | lmstudio              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-localai-ea1fbd8b               | localai               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-ollama-33222b83                | ollama                | active       | imported-unverified | 无           |
| repo-rules-scaffolds-repomix-5aa70b79               | repomix               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-text-generation-webui-8ec0aebb | text-generation-webui | active       | imported-unverified | 无           |
| repo-rules-scaffolds-anythingllm-a3e8a5fc           | AnythingLLM           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-dify-4f89d10f                  | Dify                  | active       | imported-unverified | 无           |
| repo-rules-scaffolds-privategpt-c615ca94            | PrivateGPT            | active       | imported-unverified | 无           |
| repo-rules-scaffolds-quivr-5cc2ab96                 | Quivr                 | active       | imported-unverified | 无           |
| repo-rules-scaffolds-ragflow-c92a0918               | RAGFlow               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-devdocs-62126dcb               | DevDocs               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-create-next-app-1bebc93a       | create-next-app       | active       | imported-unverified | 无           |
| repo-rules-scaffolds-create-t3-app-daf8fe4b         | create-t3-app         | active       | imported-unverified | 无           |
| repo-rules-scaffolds-shadcn-ui-d7cf613e             | shadcn/ui             | active       | imported-unverified | 无           |
| repo-rules-scaffolds-vite-3e45b462                  | vite                  | active       | imported-unverified | 无           |
| repo-rules-scaffolds-codex-e3c8be51                 | openai/codex          | active       | imported-unverified | 无           |
| repo-rules-scaffolds-roo-code-36e77dcc              | RooCodeInc/Roo-Code   | needs-review | imported-unverified | 无           |
| network-payment-services-flclash-a974428b           | FlClash               | active       | imported-unverified | 无           |
+-----------------------------------------------------+-----------------------+--------------+---------------------+--------------+
```

- `tools-platforms-codex-cli-362bc20a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/0`。描述混有“最强模型”、CLI、配置与旧地址；只保留CLI候选，不使用宣传赋级，本地Codex安装脚本不等于CLI。
- `tools-platforms-droid-1b66f6e0`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/5`。
- `tools-platforms-docusaurus-09c54423`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/13`。
- `tools-platforms-vitepress-da10a919`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/15`。
- `tools-platforms-lazyvim-2f22a781`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/17`。
- `tools-platforms-neovim-a8b85739`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/18`。
- `tools-platforms-pearai-0683754c`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/19`。
- `tools-platforms-vs-code-e8f2d385`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/20`。
- `tools-platforms-void-b1594346`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/21`。
- `tools-platforms-django-e05156b6`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/22`。
- `tools-platforms-excalidraw-02ba0cb2`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/23`。
- `tools-platforms-mermaid-cc6f6e7e`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/24`。
- `tools-platforms-dbeaver-aa2fc821`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/26`。
- `tools-platforms-tableplus-9950f31a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/27`。
- `tools-platforms-warp-14bec77a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/28`。
- `tools-platforms-claude-code-11b1e88d`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/30`。
- `tools-platforms-opencode-ada070db`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/32`。官网品牌与另行opencode-ai/opencode仓库不能凭同名自动合并，需核来源与演化。
- `tools-platforms-gemini-cli-d077e5cc`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/31`。与另一Gemini CLI行指同一官网，属于重复介绍线索，不把两个资源ID登记为两程序。
- `tools-platforms-gemini-cli-row40-d077e5cc`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/38`。与前一Gemini CLI行同名同网址，原ID仍保留；还需与GitHub实现核具体版本。
- `tools-platforms-qwen-cli-a1b92a34`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/39`。
- `tools-platforms-bito-0c0619b5`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/41`。
- `tools-platforms-codeium-668488a9`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/42`。
- `tools-platforms-continue-edb7b3bf`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/43`。
- `tools-platforms-cursor-8ebf3977`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/59`。
- `tools-platforms-zed-07b4820e`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/62`。
- `tools-platforms-chatgpt-exporter-a03efe97`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/68`。
- `repo-rules-scaffolds-autogen-fc00be5e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/5`。
- `repo-rules-scaffolds-browser-use-268f0f95`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/6`。
- `repo-rules-scaffolds-crewai-d9a56566`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/7`。
- `repo-rules-scaffolds-dspy-d8bdba82`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/8`。
- `repo-rules-scaffolds-langchain-089a07ab`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/9`。
- `repo-rules-scaffolds-pydantic-ai-cb69369e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/10`。
- `repo-rules-scaffolds-smolagents-790ade5e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/11`。
- `repo-rules-scaffolds-aider-adccc23a`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/12`。
- `repo-rules-scaffolds-claude-code-ef1ef8b6`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/13`。
- `repo-rules-scaffolds-cline-644a6623`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/14`。
- `repo-rules-scaffolds-continue-d5516851`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/15`。
- `repo-rules-scaffolds-gemini-cli-be45a9ce`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/16`。
- `repo-rules-scaffolds-gpt-engineer-eaa2e8a8`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/17`。
- `repo-rules-scaffolds-oh-my-opencode-0348827b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/18`。
- `repo-rules-scaffolds-open-interpreter-a514262e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/19`。
- `repo-rules-scaffolds-opencode-e1b762af`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/20`。仓库URL为opencode-ai/opencode；不据名称与opencode.ai官网或其他研究来源认定同一实现。
- `repo-rules-scaffolds-spec-kit-a9a40ae2`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/21`。
- `repo-rules-scaffolds-avante-nvim-29a0c49f`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/24`。
- `repo-rules-scaffolds-codecompanion-nvim-a6f68dc2`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/25`。
- `repo-rules-scaffolds-codeium-b0b85053`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/26`。此行指codeium.vim插件，不能与Codeium平台或Windsurf品牌合并。
- `repo-rules-scaffolds-copilot-vim-c06b7933`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/27`。
- `repo-rules-scaffolds-gitingest-ee7a3f76`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/41`。
- `repo-rules-scaffolds-jan-c4cdcb50`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/42`。
- `repo-rules-scaffolds-lmstudio-8b9fe81d`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/43`。
- `repo-rules-scaffolds-localai-ea1fbd8b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/44`。
- `repo-rules-scaffolds-ollama-33222b83`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/45`。
- `repo-rules-scaffolds-repomix-5aa70b79`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/46`。
- `repo-rules-scaffolds-text-generation-webui-8ec0aebb`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/47`。
- `repo-rules-scaffolds-anythingllm-a3e8a5fc`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/55`。
- `repo-rules-scaffolds-dify-4f89d10f`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/56`。
- `repo-rules-scaffolds-privategpt-c615ca94`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/57`。
- `repo-rules-scaffolds-quivr-5cc2ab96`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/58`。
- `repo-rules-scaffolds-ragflow-c92a0918`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/59`。
- `repo-rules-scaffolds-devdocs-62126dcb`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/60`。
- `repo-rules-scaffolds-create-next-app-1bebc93a`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/65`。链接是CLI文档，文档不是程序；条目所指的生成器实现仍需版本核查。
- `repo-rules-scaffolds-create-t3-app-daf8fe4b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/66`。
- `repo-rules-scaffolds-shadcn-ui-d7cf613e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/68`。
- `repo-rules-scaffolds-vite-3e45b462`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/69`。
- `repo-rules-scaffolds-codex-e3c8be51`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/81`。
- `repo-rules-scaffolds-roo-code-36e77dcc`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/82`。原描述称archive且status=needs-review；仅保留源码候选，不冒称当前可用或已核归档状态。
- `network-payment-services-flclash-a974428b`：[原始资源行](../assets/external-resources/network-payment-services.yml) `/resources/1`。源码候选仅指代理客户端内容，不授权代理连接或实际网络配置。

### 托管入口候选

按原行服务功能与网址保留托管入口候选；网址不是实现、部署或设备证据，平台/模型/账号/实际调用仍需分离，未访问账户或核部署版本。

```text
+----------------------------------------------+----------------+----------+---------------------+--------------+
| 原资源ID                                     | 名称           | 原状态   | 原验证状态          | 原风险标记   |
|----------------------------------------------+----------------+----------+---------------------+--------------|
| tools-platforms-apps-script-e6b8bbbb         | Apps Script    | active   | imported-unverified | 无           |
| tools-platforms-google-sheets-32b827b0       | Google Sheets  | active   | imported-unverified | 无           |
| tools-platforms-mintlify-0f0b6833            | Mintlify       | active   | imported-unverified | 无           |
| tools-platforms-mermaid-chart-302f49f0       | Mermaid Chart  | active   | imported-unverified | 无           |
| tools-platforms-zread-6c1ee1d6               | Zread          | active   | imported-unverified | 无           |
| tools-platforms-notebooklm-e1b56ba1          | NotebookLM     | active   | imported-unverified | 无           |
| tools-platforms-kimi-53c18eae                | Kimi           | active   | imported-unverified | 无           |
| tools-platforms-chatglm-cn-ebc410ba          | 智谱清言       | active   | imported-unverified | 无           |
| tools-platforms-www-doubao-com-b4d6c78b      | 豆包           | active   | imported-unverified | 无           |
| tools-platforms-tongyi-aliyun-com-a528848f   | 通义千问       | active   | imported-unverified | 无           |
| tools-platforms-ai-studio-2cd869be           | AI Studio      | active   | imported-unverified | 无           |
| tools-platforms-antigravity-528a772a         | antigravity    | active   | imported-unverified | 无           |
| tools-platforms-chatgpt-935111f5             | ChatGPT        | active   | imported-unverified | 无           |
| tools-platforms-claude-13dd5e3a              | Claude         | active   | imported-unverified | 无           |
| tools-platforms-gemini-dc8a36f7              | Gemini         | active   | imported-unverified | 无           |
| tools-platforms-bolt-new-06379d16            | Bolt.new       | active   | imported-unverified | 无           |
| tools-platforms-devin-f5a69caf               | Devin          | active   | imported-unverified | 无           |
| tools-platforms-lovable-5eb584a1             | Lovable        | active   | imported-unverified | 无           |
| tools-platforms-replit-agent-bbd1c2ac        | Replit Agent   | active   | imported-unverified | 无           |
| tools-platforms-v0-by-vercel-fe818ef0        | v0 by Vercel   | active   | imported-unverified | 无           |
| repo-rules-scaffolds-github-e755441d         | GitHub         | active   | imported-unverified | 无           |
| repo-rules-scaffolds-github-copilot-102fb5f8 | GitHub Copilot | active   | imported-unverified | 无           |
+----------------------------------------------+----------------+----------+---------------------+--------------+
```

- `tools-platforms-apps-script-e6b8bbbb`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/2`。
- `tools-platforms-google-sheets-32b827b0`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/8`。
- `tools-platforms-mintlify-0f0b6833`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/14`。
- `tools-platforms-mermaid-chart-302f49f0`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/10`。
- `tools-platforms-zread-6c1ee1d6`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/16`。
- `tools-platforms-notebooklm-e1b56ba1`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/25`。
- `tools-platforms-kimi-53c18eae`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/33`。仅保留平台网址候选；Kimi K2.5能力描述与服务实现/实际加载模型未核。
- `tools-platforms-chatglm-cn-ebc410ba`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/34`。平台与GLM-4描述不作为同一对象/版本证据。
- `tools-platforms-www-doubao-com-b4d6c78b`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/35`。模型与聊天客户端品牌并置，当前只保留网页入口候选。
- `tools-platforms-tongyi-aliyun-com-a528848f`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/36`。Qwen模型、聊天服务及免费额度声明分别核，不继承“免费”或能力主张。
- `tools-platforms-ai-studio-2cd869be`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/37`。AI Studio入口、Gemini模型与免费额度不是同一实体。
- `tools-platforms-antigravity-528a772a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/40`。
- `tools-platforms-chatgpt-935111f5`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/45`。保留对话入口候选，不据GPT-5.1/支持Codex描述批准具体模型或CLI版本。
- `tools-platforms-claude-13dd5e3a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/46`。保留平台入口候选，不沿用Opus4.6能力/Artifacts宣传为实现效果。
- `tools-platforms-gemini-dc8a36f7`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/47`。模型名、免费额度与长上下文宣传未核，网页入口与模型内容分开。
- `tools-platforms-bolt-new-06379d16`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/63`。
- `tools-platforms-devin-f5a69caf`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/64`。
- `tools-platforms-lovable-5eb584a1`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/65`。
- `tools-platforms-replit-agent-bbd1c2ac`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/66`。
- `tools-platforms-v0-by-vercel-fe818ef0`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/67`。
- `repo-rules-scaffolds-github-e755441d`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/2`。
- `repo-rules-scaffolds-github-copilot-102fb5f8`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/71`。订阅/服务入口与copilot.vim插件、模型或免费资格分别核，原免费描述未核。

### 排除：资料/规约内容

当前条目所指为知识、教程、索引、规则、提示词或模板内容，不作为法器程序登记；不删除原资源，也不断言整个仓库没有程序，其内具体实现须另选来源。

```text
+---------------------------------------------------------------------+----------------------------------------+--------------+---------------------+------------------------+
| 原资源ID                                                            | 名称                                   | 原状态       | 原验证状态          | 原风险标记             |
|---------------------------------------------------------------------+----------------------------------------+--------------+---------------------+------------------------|
| tools-platforms-prompt-jsonl-8e9b2066                               | prompt_jsonl                           | needs-review | imported-unverified | non-url-locator        |
| tools-platforms-bilibili-23287176                                   | Bilibili                               | active       | imported-unverified | 无                     |
| tools-platforms-z-library-31b0d982                                  | Z-Library                              | active       | imported-unverified | access-legality-review |
| repo-rules-scaffolds-vibe-coding-e16848e0                           | Vibe Coding 指南                       | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-github-com-e0a40b2e                            | 开发者基础知识库                       | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-mcaf-47f07717                                  | MCAF                                   | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-github-topics-bcc7e192                         | GitHub Topics                          | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-github-trending-d46be94c                       | GitHub Trending                        | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-mcp-servers-d91d6430                   | awesome-mcp-servers                    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-2025-ai-engineer-reading-list-70f4fbd3         | 2025 AI Engineer Reading List          | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-ai-547bb859                                    | AI 编程最佳实践                        | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-ai-engineering-d04a5b40                        | ai-engineering                         | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-explorables-2cedba5b                   | awesome-explorables                    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-llm-02e83378                           | awesome-llm                            | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-generative-ai-for-beginners-3b1db321           | generative-ai-for-beginners            | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-llm-course-9227aca8                            | llm-course                             | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-lovable-for-beginners-38de2782                 | lovable-for-beginners                  | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-prompt-engineering-guide-5130a915              | prompt-engineering-guide               | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-vibe-vibe-c80a5961                             | vibe-vibe                              | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-chatgpt-prompts-ebaf3df7               | awesome-chatgpt-prompts                | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-chatgpt-prompts-zh-966cbb5b            | awesome-chatgpt-prompts-zh             | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-claude-code-system-prompts-3f0438e1            | claude-code-system-prompts             | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-system-prompts-and-models-of-ai-tools-8290b642 | system-prompts-and-models-of-ai-tools  | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-cursorrules-7f259f16                   | awesome-cursorrules                    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-cursor-directory-807839d9                      | cursor.directory                       | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-dotcursorrules-ad20d456                        | dotcursorrules                         | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-langgpt-d6b7fb87                               | LangGPT                                | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-chatgpt-prompts-4c4b8064               | Awesome ChatGPT Prompts                | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-system-prompts-b5948bc8                        | System Prompts 仓库                    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-easy-vibe-3c217e96                             | datawhalechina/easy-vibe               | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-ai-guide-c12bbbfd                              | liyupi/ai-guide                        | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-vibe-coding-guide-cf65840a                     | wendy7756/vibe-coding-guide            | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-ai-coding-c221421b                             | Daotin/ai-coding                       | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-vibe-coding-skill-a5e7c42d                     | earyantLe/vibe-coding-skill            | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-vibe-coding-e5ab67eb                   | filipecalegario/awesome-vibe-coding    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-vibe-coding-e3ea2b5b                   | ai-for-developers/awesome-vibe-coding  | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-claude-code-best-practice-01224898             | shanraisshan/claude-code-best-practice | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-claude-code-5e3406a1                   | hesreallyhim/awesome-claude-code       | active       | imported-unverified | 无                     |
+---------------------------------------------------------------------+----------------------------------------+--------------+---------------------+------------------------+
```

- `tools-platforms-prompt-jsonl-8e9b2066`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/1`。
- `tools-platforms-bilibili-23287176`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/3`。
- `tools-platforms-z-library-31b0d982`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/12`。按本条“电子书资源”所指排除程序登记；保留access-legality-review，不批准访问/下载或许可。
- `repo-rules-scaffolds-vibe-coding-e16848e0`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/0`。
- `repo-rules-scaffolds-github-com-e0a40b2e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/3`。
- `repo-rules-scaffolds-mcaf-47f07717`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/4`。
- `repo-rules-scaffolds-github-topics-bcc7e192`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/22`。
- `repo-rules-scaffolds-github-trending-d46be94c`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/23`。
- `repo-rules-scaffolds-awesome-mcp-servers-d91d6430`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/28`。
- `repo-rules-scaffolds-2025-ai-engineer-reading-list-70f4fbd3`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/30`。
- `repo-rules-scaffolds-ai-547bb859`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/31`。
- `repo-rules-scaffolds-ai-engineering-d04a5b40`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/32`。
- `repo-rules-scaffolds-awesome-explorables-2cedba5b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/34`。
- `repo-rules-scaffolds-awesome-llm-02e83378`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/35`。
- `repo-rules-scaffolds-generative-ai-for-beginners-3b1db321`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/36`。
- `repo-rules-scaffolds-llm-course-9227aca8`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/37`。
- `repo-rules-scaffolds-lovable-for-beginners-38de2782`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/38`。
- `repo-rules-scaffolds-prompt-engineering-guide-5130a915`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/39`。
- `repo-rules-scaffolds-vibe-vibe-c80a5961`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/40`。
- `repo-rules-scaffolds-awesome-chatgpt-prompts-ebaf3df7`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/48`。与另一f/awesome-chatgpt-prompts行是重复来源线索；保原两ID，不登记两个工具。
- `repo-rules-scaffolds-awesome-chatgpt-prompts-zh-966cbb5b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/49`。
- `repo-rules-scaffolds-claude-code-system-prompts-3f0438e1`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/50`。
- `repo-rules-scaffolds-system-prompts-and-models-of-ai-tools-8290b642`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/51`。
- `repo-rules-scaffolds-awesome-cursorrules-7f259f16`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/52`。
- `repo-rules-scaffolds-cursor-directory-807839d9`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/53`。
- `repo-rules-scaffolds-dotcursorrules-ad20d456`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/54`。
- `repo-rules-scaffolds-langgpt-d6b7fb87`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/61`。
- `repo-rules-scaffolds-awesome-chatgpt-prompts-4c4b8064`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/63`。原description=null；仅依原名称和仓库路径关联提示词合集线索，不补造产品能力。
- `repo-rules-scaffolds-system-prompts-b5948bc8`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/64`。原description=null；与另一同URL条目关联提示词来源线索，不声称模型参数或工具实现。
- `repo-rules-scaffolds-easy-vibe-3c217e96`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/72`。
- `repo-rules-scaffolds-ai-guide-c12bbbfd`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/73`。
- `repo-rules-scaffolds-vibe-coding-guide-cf65840a`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/74`。
- `repo-rules-scaffolds-ai-coding-c221421b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/75`。
- `repo-rules-scaffolds-vibe-coding-skill-a5e7c42d`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/76`。
- `repo-rules-scaffolds-awesome-vibe-coding-e5ab67eb`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/79`。
- `repo-rules-scaffolds-awesome-vibe-coding-e3ea2b5b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/80`。
- `repo-rules-scaffolds-claude-code-best-practice-01224898`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/83`。
- `repo-rules-scaffolds-awesome-claude-code-5e3406a1`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/84`。

### 排除：模型名称所指

当前名义所指是模型名称/版本，不当作法器程序；未取得参数/结构版本证据，不批准model-artifact实例，所附平台URL不证明模型与服务同一。

```text
+------------------------------------------+-----------------+--------------+---------------------+--------------+
| 原资源ID                                 | 名称            | 原状态       | 原验证状态          | 原风险标记   |
|------------------------------------------+-----------------+--------------+---------------------+--------------|
| tools-platforms-claude-opus-4-6-f751380c | Claude Opus 4.6 | active       | imported-unverified | 无           |
| tools-platforms-gpt-5-1-codex-1ad522a5   | GPT-5.1 Codex   | needs-review | imported-unverified | missing-link |
| tools-platforms-gemini-2-5-pro-0661c69f  | Gemini 2.5 Pro  | needs-review | imported-unverified | missing-link |
| tools-platforms-dall-e-3-26dc583b        | DALL-E 3        | active       | imported-unverified | 无           |
+------------------------------------------+-----------------+--------------+---------------------+--------------+
```

- `tools-platforms-claude-opus-4-6-f751380c`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/4`。claude.ai平台不是Opus参数内容或具体模型版本的验证证据。
- `tools-platforms-gpt-5-1-codex-1ad522a5`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/6`。
- `tools-platforms-gemini-2-5-pro-0661c69f`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/7`。
- `tools-platforms-dall-e-3-26dc583b`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/48`。名称指模型，但网址是chatgpt.com；图像模型与其调用平台必须分离。

### 待核：对象身份

信息不足、对象名/目标不一致或复合包未展开，保留待核；不凭品牌、后缀、Skill/仓库包装复制软件身份，先明确具体模块、入口及版本。

```text
+----------------------------------------------------+--------------------------+--------------+---------------------+--------------+
| 原资源ID                                           | 名称                     | 原状态       | 原验证状态          | 原风险标记   |
|----------------------------------------------------+--------------------------+--------------+---------------------+--------------|
| tools-platforms-local-history-2b05b2c1             | Local History            | needs-review | imported-unverified | missing-link |
| tools-platforms-partial-diff-4787875c              | Partial Diff             | needs-review | imported-unverified | missing-link |
| tools-platforms-zsh-d6d24951                       | zsh                      | active       | imported-unverified | 无           |
| tools-platforms-tabnine-0b2c09aa                   | Tabnine                  | active       | imported-unverified | 无           |
| tools-platforms-elevenlabs-5a58d635                | ElevenLabs               | active       | imported-unverified | 无           |
| tools-platforms-ideogram-efb6a3b8                  | Ideogram                 | active       | imported-unverified | 无           |
| tools-platforms-kling-253d44f3                     | Kling                    | active       | imported-unverified | 无           |
| tools-platforms-leonardo-ai-26816634               | Leonardo AI              | active       | imported-unverified | 无           |
| tools-platforms-meshy-549051bc                     | Meshy                    | active       | imported-unverified | 无           |
| tools-platforms-midjourney-976ad67d                | Midjourney               | active       | imported-unverified | 无           |
| tools-platforms-runway-6c8ab136                    | Runway                   | active       | imported-unverified | 无           |
| tools-platforms-sora-3b1d49f7                      | Sora                     | active       | imported-unverified | 无           |
| tools-platforms-suno-fb9344c5                      | Suno                     | active       | imported-unverified | 无           |
| tools-platforms-udio-0d39f909                      | Udio                     | active       | imported-unverified | 无           |
| tools-platforms-kiro-47d2b0fc                      | Kiro                     | active       | imported-unverified | 无           |
| tools-platforms-windsurf-fdd489a7                  | Windsurf                 | active       | imported-unverified | 无           |
| repo-rules-scaffolds-scientific-skills-0f3f6b96    | scientific-skills        | active       | imported-unverified | 无           |
| repo-rules-scaffolds-mcp-servers-5d60dee4          | mcp-servers              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-ai-for-grant-writing-0a634380 | ai-for-grant-writing     | active       | imported-unverified | 无           |
| repo-rules-scaffolds-fastapi-template-c97cc061     | fastapi-template         | active       | imported-unverified | 无           |
| repo-rules-scaffolds-ai-coding-lab-6dc927c2        | luzhenqian/ai-coding-lab | active       | imported-unverified | 无           |
| repo-rules-scaffolds-cs146s-cn-eaea3651            | ShouZhengAI/CS146S_CN    | active       | imported-unverified | 无           |
+----------------------------------------------------+--------------------------+--------------+---------------------+--------------+
```

- `tools-platforms-local-history-2b05b2c1`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/9`。缺链接；同名插件可能有多个实现，需厂商/仓库和版本。
- `tools-platforms-partial-diff-4787875c`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/11`。缺链接；需补具体插件来源，保留missing-link与needs-review。
- `tools-platforms-zsh-d6d24951`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/29`。名称是zsh，但网址指ohmyz.sh；Shell程序与配置框架需消歧，不按标题选择软件身份。
- `tools-platforms-tabnine-0b2c09aa`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/44`。
- `tools-platforms-elevenlabs-5a58d635`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/49`。
- `tools-platforms-ideogram-efb6a3b8`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/50`。
- `tools-platforms-kling-253d44f3`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/51`。
- `tools-platforms-leonardo-ai-26816634`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/52`。
- `tools-platforms-meshy-549051bc`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/53`。
- `tools-platforms-midjourney-976ad67d`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/54`。
- `tools-platforms-runway-6c8ab136`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/55`。
- `tools-platforms-sora-3b1d49f7`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/56`。
- `tools-platforms-suno-fb9344c5`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/57`。
- `tools-platforms-udio-0d39f909`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/58`。
- `tools-platforms-kiro-47d2b0fc`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/60`。
- `tools-platforms-windsurf-fdd489a7`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/61`。
- `repo-rules-scaffolds-scientific-skills-0f3f6b96`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/1`。Skill集合可能包含方法与脚本，需逐实际内容选区；集合自身不直接注册成一件软件。
- `repo-rules-scaffolds-mcp-servers-5d60dee4`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/29`。服务器集合需按独立实现选区，不把MCP协议、多个示例、部署和整仓库作同一实例。
- `repo-rules-scaffolds-ai-for-grant-writing-0a634380`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/33`。
- `repo-rules-scaffolds-fastapi-template-c97cc061`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/67`。模板可能包含可执行应用或生成器，须分清模板内容、应用源码与新生成实例。
- `repo-rules-scaffolds-ai-coding-lab-6dc927c2`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/77`。项目实战复合仓库包含多种项目类型，不能把教程或整个仓库纳为一程序。
- `repo-rules-scaffolds-cs146s-cn-eaea3651`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/78`。课程、作业与工具混合，需明确具体程序选区。

### 关联已审本地来源

原仓库网址与已审本地submodule来源对应，仅建立来源参照，不新增重复法器；不把未版本化仓库入口等同本次固定源码版本。

```text
+--------------------------------------+---------------+----------+---------------------+--------------+
| 原资源ID                             | 名称          | 原状态   | 原验证状态          | 原风险标记   |
|--------------------------------------+---------------+----------+---------------------+--------------|
| repo-rules-scaffolds-skills-cd973130 | Skills 制作器 | active   | imported-unverified | 无           |
| repo-rules-scaffolds-tmux-9f36981a   | tmux          | active   | imported-unverified | 无           |
+--------------------------------------+---------------+----------+---------------------+--------------+
```

- `repo-rules-scaffolds-skills-cd973130`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/62`。 对应本地来源参照 faqi-skill-seekers；不把未版本化的仓库URL等同该固定源码版本。
- `repo-rules-scaffolds-tmux-9f36981a`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/70`。 对应本地来源参照 faqi-tmux；不把未版本化的仓库URL等同该固定源码版本。

### 待核：受限服务所指

网络/金融服务品牌、推广入口或账号产品所指待核；保留全部风险与原状态，不批准交易、注册、权限、设备或运行实例。

```text
+-----------------------------------------------------+--------------+----------+---------------------+-----------------------------------------------------+
| 原资源ID                                            | 名称         | 原状态   | 原验证状态          | 原风险标记                                          |
|-----------------------------------------------------+--------------+----------+---------------------+-----------------------------------------------------|
| network-payment-services-www-bsmkweb-com-0960fe59   | 币安支付     | active   | imported-unverified | referral-or-tracking-link, financial-service-review |
| network-payment-services-xn-9kqz23b19z-com-a271e5a7 | 网络服务     | active   | imported-unverified | referral-or-tracking-link                           |
| network-payment-services-bybit-81d32c91             | Bybit 虚拟卡 | active   | imported-unverified | referral-or-tracking-link, financial-service-review |
+-----------------------------------------------------+--------------+----------+---------------------+-----------------------------------------------------+
```

- `network-payment-services-www-bsmkweb-com-0960fe59`：[原始资源行](../assets/external-resources/network-payment-services.yml) `/resources/0`。资源自称“币安支付”，网址为bsmkweb.com并带ref；品牌/网址所指一致性未核，不据名称认定官方服务。
- `network-payment-services-xn-9kqz23b19z-com-a271e5a7`：[原始资源行](../assets/external-resources/network-payment-services.yml) `/resources/2`。注册推广入口只有泛化云服务说明，实际服务、提供方与合规边界待核。
- `network-payment-services-bybit-81d32c91`：[原始资源行](../assets/external-resources/network-payment-services.yml) `/resources/3`。卡产品/账户/支付过程与网站或程序内容分开，不触发开户或支付。

## 来源与选区

选区是一基半开区间 `[start,end)`；SHA-256对应固定Git blob的完整字节与选区原字节，不归一化或复制源码。
校验还核当前文件字节及submodule指针；源码存在和指针匹配不等于完整仓库语义、许可证或能力已审。

### S01

[来源文件](../tools/prompts-library/README.md)：`tools/prompts-library/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`4c2d5f97a6cfa67e033e166676d12eeaab6a562fa83c39b0f2474ae2afbcdae2`。
- 选区：`[1,95)`；SHA-256：`4c2d5f97a6cfa67e033e166676d12eeaab6a562fa83c39b0f2474ae2afbcdae2`。

### S02

[来源文件](../tools/prompts-library/main.py)：`tools/prompts-library/main.py`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`ed0113d3ecbe9c9d4ca48ee7dde2c76c9a6fd1f54a1ae890fd3689d617347691`。
- 选区：`[625,689)`；SHA-256：`757b82c3bba30f1d62359c39f7c110d425463326e854acef2de085f14d90cf6d`。

### S03

[来源文件](../tools/chat-vault/README.md)：`tools/chat-vault/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`938ddcce3ba06fad18a05d072cfc47cb8427064c72745f557e4b782de8a2c753`。
- 选区：`[1,104)`；SHA-256：`deecf873b9392e27cbae073fd6f75fcb1865af9d6461232dd517ba945cafa3d1`。

### S04

[来源文件](../tools/chat-vault/services/chat-vault/src/main.py)：`tools/chat-vault/services/chat-vault/src/main.py`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`561c611909714d358f9968c45078f037bd46cdb037969d598cfed27d94affd72`。
- 选区：`[65,107)`；SHA-256：`43279c5004b34ef3de79da4dd5c103e741f0a9ed47683e7c262a79bd35f8b551`。

### S05

[来源文件](../tools/config/.codex/README.md)：`tools/config/.codex/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`4cd23bbafa069d8bd651e9997951ac99252cf13310d1c9fda14dcf01de818a53`。
- 选区：`[1,78)`；SHA-256：`b290d2842b0290ee9701e41c046634d2cd90684c0c53d1e97e3781a05d695e87`。

### S06

[来源文件](../tools/config/.codex/install.sh)：`tools/config/.codex/install.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`a2ba28d5a48d46aa7d508408519be117f8726c8d66e632d8736deab9175b04a4`。
- 选区：`[43,100)`；SHA-256：`99ccf88c8d5ec6f7b7eda53fc4fd3af29a0ca08d9eef74ad3283cdf649d6a7cf`。

### S07

[来源文件](../skills/auto-skill/README.md)：`skills/auto-skill/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0`。
- 选区：`[1,21)`；SHA-256：`2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0`。

### S08

[来源文件](../skills/auto-skill/scripts/create-skill.sh)：`skills/auto-skill/scripts/create-skill.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`3eb16d2f24cc2af3e7d7a0f4175e06b0258504795d079ba0920be9dd75f2f7fc`。
- 选区：`[80,182)`；SHA-256：`e769660515ada48debbd022fdfb85ec934b4d3413cf3501e06ef075b6d36b1a4`。

### S09

[来源文件](../skills/auto-skill/scripts/validate-skill.sh)：`skills/auto-skill/scripts/validate-skill.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`deb5cf2529a93c87c8b7323b55ffc6d7798e6b59652351ba795340ac8c0061c9`。
- 选区：`[67,160)`；SHA-256：`dbd460af6a32307709a11281c7b90925b9fd9820128eb04881c80c020a99f0dc`。

### S10

[来源文件](../skills/auto-skill/scripts/skill-seekers.sh)：`skills/auto-skill/scripts/skill-seekers.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`fdbf73b1faa1a0f445663b5c7c1c9792bbfb6dcdf5f5308198503e14ea0c64dc`。
- 选区：`[28,66)`；SHA-256：`f678142dddda161372feb5c5af96bbbf5e1b3e76b9e2c7dc905a4d1ba18070f2`。

### S11

[来源文件](../skills/auto-tmux/README.md)：`skills/auto-tmux/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`d21ca4f1c4adb6a799a76f7a7446b1ebca70d2402f73e80600cda1c2a6d24c25`。
- 选区：`[1,18)`；SHA-256：`0c0e46b950949789a6b85addd85f3a9ec0b2945e6a44134f82c7b46acc59b308`。

### S12

[来源文件](../skills/auto-tmux/scripts/auto-tmux.sh)：`skills/auto-tmux/scripts/auto-tmux.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`f473fddada7a7f5fd85afe94deccd16e2aba26195423dc87afbac176315b6567`。
- 选区：`[701,725)`；SHA-256：`701db6430b20faa4bf2477001f584b15a1dea31e6c4a9d32747be343988dd3c2`。

### S13

[来源文件](../skills/auto-tmux/scripts/auto-tmux.sh)：`skills/auto-tmux/scripts/auto-tmux.sh`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`f473fddada7a7f5fd85afe94deccd16e2aba26195423dc87afbac176315b6567`。
- 选区：`[65,95)`；SHA-256：`a745cc41ed28208894954fccadc603a2f11e4e7888bd9df4f85d1dc0c84ca564`。

### S14

[来源文件](../tools/external/Skill_Seekers-development/pyproject.toml)：`tools/external/Skill_Seekers-development/pyproject.toml`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/Skill_Seekers-development`；Git修订：`26638b248279a3b001b651475e0f28975f5ff069`。
- 完整文件SHA-256：`40820d20d8f56c1dc24c8f432141fa438d54473acbfecfa716fc9d188cbc8294`。
- 选区：`[1,15)`；SHA-256：`8fc8e7df82f18edc826b13f63f097661c1f40b19d2e7ab576e25854b453919e3`。

### S15

[来源文件](../tools/external/Skill_Seekers-development/pyproject.toml)：`tools/external/Skill_Seekers-development/pyproject.toml`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/Skill_Seekers-development`；Git修订：`26638b248279a3b001b651475e0f28975f5ff069`。
- 完整文件SHA-256：`40820d20d8f56c1dc24c8f432141fa438d54473acbfecfa716fc9d188cbc8294`。
- 选区：`[301,327)`；SHA-256：`ac6771e334ffad6fe8cb4934797de797375c87d4c33a16afff72de8d1642893f`。

### S16

[来源文件](../tools/external/Skill_Seekers-development/src/skill_seekers/cli/main.py)：`tools/external/Skill_Seekers-development/src/skill_seekers/cli/main.py`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/Skill_Seekers-development`；Git修订：`26638b248279a3b001b651475e0f28975f5ff069`。
- 完整文件SHA-256：`8c02660dacd304f51fe8c4a9685d3f6d5324a7eef7779b6baa7325827bf01985`。
- 选区：`[39,116)`；SHA-256：`60fba27fbe444499a1e95b5dc69edc8b0d34d6c26a30039dcbf9d9205ffdfb14`。

### S17

[来源文件](../tools/external/.tmux/README.md)：`tools/external/.tmux/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/.tmux`；Git修订：`87dcd13a28aeb5f18baee630e24b3f5765ae3a4f`。
- 完整文件SHA-256：`10b0cca6bb2a4ab7af39d76d27f51b91ca1df4dead015315400041695c9471e7`。
- 选区：`[9,78)`；SHA-256：`243d5ab2936723c61f781dd6906e61de92cceea6069e570ca107b6c19236aeb7`。

### S18

[来源文件](../tools/external/.tmux/.tmux.conf)：`tools/external/.tmux/.tmux.conf`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/.tmux`；Git修订：`87dcd13a28aeb5f18baee630e24b3f5765ae3a4f`。
- 完整文件SHA-256：`6807d44735b7b11e64c4488a0c3fdcbd2809cc73efedcc349d098e80a690aeeb`。
- 选区：`[150,190)`；SHA-256：`e39dd4f98da410b88e110772d21d1eb14d3bfb6e2c6e8c36e2cb19129d9c98f8`。

### S19

[来源文件](../tools/external/.tmux/.tmux.conf)：`tools/external/.tmux/.tmux.conf`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/.tmux`；Git修订：`87dcd13a28aeb5f18baee630e24b3f5765ae3a4f`。
- 完整文件SHA-256：`6807d44735b7b11e64c4488a0c3fdcbd2809cc73efedcc349d098e80a690aeeb`。
- 选区：`[1829,1891)`；SHA-256：`3065f39bd62e8cb3bb4095dfaf9784840368d5760137ad01d3f96eb55ede68a1`。

### S20

[来源文件](../tools/external/tmux/README)：`tools/external/tmux/README`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/tmux`；Git修订：`615c27c11789948df2db09e113e882f82dfb3e1c`。
- 完整文件SHA-256：`9fb75e6c7f10c25b73e41b8214336d0dc2acfbe4c99984514ccaf7327192d53e`。
- 选区：`[1,20)`；SHA-256：`68e51dd5a0148fa1d22f5c7565d3da74dc6619207d1c5238658d5fd873c63e5b`。

### S21

[来源文件](../tools/external/tmux/tmux.c)：`tools/external/tmux/tmux.c`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/tmux`；Git修订：`615c27c11789948df2db09e113e882f82dfb3e1c`。
- 完整文件SHA-256：`58a9bef0d1d424fd2e2a79c6d998dab96aab81ee771b7c2653928451f3bf11a8`。
- 选区：`[350,492)`；SHA-256：`cd3c886c9a155f70dcddaeec88b4a86253c565b2e18753327f83446d92a7e8f4`。

### S22

[来源文件](../tools/external/claude-official-skills/README.md)：`tools/external/claude-official-skills/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/claude-official-skills`；Git修订：`1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563`。
- 完整文件SHA-256：`d7c5c2f9b248c7c0b31f093cf22b9a7407f5b093c8ca9ebe75a5b6845b02b76e`。
- 选区：`[1,28)`；SHA-256：`672c572d34a077a534754b7311d19db68a8402c86fe64e35be5e80da3ae7453a`。

### S23

[来源文件](../tools/external/claude-official-skills/skills/skill-creator/scripts/init_skill.py)：`tools/external/claude-official-skills/skills/skill-creator/scripts/init_skill.py`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/claude-official-skills`；Git修订：`1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563`。
- 完整文件SHA-256：`cf12790f1d4958799281920d599f56aea38fb5c26e2812a61dd740bf3d4b6b99`。
- 选区：`[194,304)`；SHA-256：`f3ef6ff82946a9596d5cacfc1ed0405765187e5ffec5a4ede6c15f5e8dd248dd`。

### S24

[来源文件](../tools/external/html-tools-main/README.md)：`tools/external/html-tools-main/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`6aeb3fbdd0ad484f15b44b8c0e26caa7228cede0a659292893617d19d99b6df3`。
- 选区：`[1,18)`；SHA-256：`c58731ae7c6b900a386e03571782503c366959db1a623c21c7de2a08fc04442d`。

### S25

[来源文件](../tools/external/html-tools-main/clean_epub_css.html)：`tools/external/html-tools-main/clean_epub_css.html`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`1716a7ea5f4bf4837bc044c9c164e58b3dbb04d492f677b7766b506edd1c0d2a`。
- 选区：`[317,405)`；SHA-256：`4d07dac2850cbf4860f628b5c26d52976aea9cc8dd981851da5141dc7b18a7cb`。

### S26

[来源文件](../tools/external/html-tools-main/markdown-bianjiqi.html)：`tools/external/html-tools-main/markdown-bianjiqi.html`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`e4c76015749bf42e898412ec7b8e1229c847575ef740bcf6900311d7212dc61e`。
- 选区：`[181,260)`；SHA-256：`cbc5a64c27eefb0801c95a87cbf4ed0a149e25000a41e53e3387eb274ca40894`。

### S27

[来源文件](../tools/external/html-tools-main/task%20card%20generator.html)：`tools/external/html-tools-main/task card generator.html`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`0eba89d2f674bb0bc26690c4e406f99b7a2bcd40ecd838c1c19e1f970f7b5670`。
- 选区：`[217,284)`；SHA-256：`8b710f5b6f6b1c1f0fcaafead15e6f63e5800684a1c8ae49dad6a7681659eb19`。

### S28

[来源文件](../tools/external/html-tools-main/xhs%20graphic%20production.html)：`tools/external/html-tools-main/xhs graphic production.html`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`1835e29563d4cf7f01cb9cf837d3f57d1b2e48304cc202e1061240bccf6e7e0e`。
- 选区：`[96,147)`；SHA-256：`52b9c7a45cd3d5c8409ee1cde59c31296b608e35c0d668c2833bd7b35639a0f8`。

### S29

[来源文件](../tools/external/html-tools-main/xhs%20graphic%20production%20-%201.0.html)：`tools/external/html-tools-main/xhs graphic production - 1.0.html`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`14a60fa5cc9fa3b7a8beac146277c1ef15729eb5e18cd7889fbcf498d5d1411a`。
- 选区：`[177,312)`；SHA-256：`abe37a7bfbc4b1035be0ff037decbc49b6f336a59e8b8e5501e810d721f45ab9`。

### S30

[来源文件](../tools/external/my-nvim/README.md)：`tools/external/my-nvim/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`905c3a248d5208f001f3eb6924beaf768454c70cdbc4c41cf67e906dba7ca8c0`。
- 选区：`[1,36)`；SHA-256：`5476e2380b6412a4d29ce37ad4ded76cd39bc5928e5cf716d98749f3ae8a31ea`。

### S31

[来源文件](../tools/external/my-nvim/nvim-config/init.lua)：`tools/external/my-nvim/nvim-config/init.lua`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`3b2d6e9976a515b7c8df08ed7c7f61a5751e9c08a6ff5579d621b87312c9e2c6`。
- 选区：`[1,3)`；SHA-256：`3b2d6e9976a515b7c8df08ed7c7f61a5751e9c08a6ff5579d621b87312c9e2c6`。

### S32

[来源文件](../tools/external/my-nvim/nvim-config/lua/config/lazy.lua)：`tools/external/my-nvim/nvim-config/lua/config/lazy.lua`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`5fd03a47dc423a46b7c141149d35ba20cbbd96eb2c90f48f74dbff94c202802e`。
- 选区：`[1,56)`；SHA-256：`5fd03a47dc423a46b7c141149d35ba20cbbd96eb2c90f48f74dbff94c202802e`。

### S33

[来源文件](../tools/external/MCPlayerTransfer/README.md)：`tools/external/MCPlayerTransfer/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`f48b3081530011171ee6761115613c5eb7811a9ec3059cdec53e3b50c632f0e3`。
- 选区：`[1,47)`；SHA-256：`939c69119628dd9eea9c16461c41428db4e5faf6d7c9ab4024e7a2f8ffa0bce9`。

### S34

[来源文件](../tools/external/MCPlayerTransfer/main.py)：`tools/external/MCPlayerTransfer/main.py`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`11bfdb47774247c32ad8cd0de441d56a13a17e9c12bcb3e2d9e81895958e1450`。
- 选区：`[1,51)`；SHA-256：`11bfdb47774247c32ad8cd0de441d56a13a17e9c12bcb3e2d9e81895958e1450`。

### S35

[来源文件](../tools/external/XHS-image-to-PDF-conversion/README.md)：`tools/external/XHS-image-to-PDF-conversion/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`19f65c7b6afe56c57789a30d1aed3c214051474fd21ea97f1ec10cc1ec774f13`。
- 选区：`[21,51)`；SHA-256：`271e08cdfc793b500025c6d2f7d8e768a1ba6f5a03fe86b86f1aee5c5a2517de`。

### S36

[来源文件](../tools/external/XHS-image-to-PDF-conversion/pdf.py)：`tools/external/XHS-image-to-PDF-conversion/pdf.py`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`ee045272a0ba361676c1ee908758e7316e96438774716c79472fb05cc5055539`。
- 选区：`[17,120)`；SHA-256：`4b4eb47d3545b5bcba80384c1aa81cee4d973d006736ea7a664f69ef9b759e70`。

## 维护与未完成事项

```bash
make sync-faqi-catalog
make check-faqi-catalog
make test-faqi-catalog
```

检查复用jsonschema/PyYAML，表格复用tabulate；来源、ID、选区、范围或只读视图漂移均失败，不联网补证或静默升级。
此初审不维护等级、账户、设备、部署或运行证据。独立语义审查、运行/效果/许可核验、产品同一/版本演化及未逐模块展开的复合包仍待核。
