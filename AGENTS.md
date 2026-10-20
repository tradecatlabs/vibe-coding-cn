# Vibe Coding工具箱：仓库操作指南

## 目标与边界

- 以Pi Agent和已授权的OpenAI GPT作为主体底座，复用原生工具、资源加载与模型选择；不新造Agent、模型客户端、Lambda解释器或资源管理框架。
- 只组织现有资产；三域为`.github/context/`、`.github/skills/`、`.github/extensions/`，域内对象平铺。包内部源码、资料集合与共享实现不另算新的一级资源分类。
- 根`README.md`是唯一主页；`.github/README.md`禁止创建。`llms.txt`是AI短入口；大资料按需读取，不全部注入系统上下文。
- 读者按问题、设计、实现、代价及比较/共性/适用条件理解工具；Lambda记号只辅助表达输入输出与组合，不证明纯函数、正确、确定或终止。
- 功法与法器441个对象的活动说明使用`.github/context/assets/templates/tool-explanation-template-v1.md`：保留v0的15项并新增“结论、连接规则、依据”，共18项；v0仅作历史模板。第16项为主张、第18项为事实依据、第17项须按图尔敏模型写明从证据到主张的具体推理规则；不得用字段交叉引用冒充连接规则。不得用AI自拟版本替代已登记模板，不借模板迁移改写原15项、来源或评级。主页集合级说明仍按既有15项结构展示。

## 目录职责

| 路径 | 唯一职责 |
|---|---|
| `.github/context/` | 既有规则、知识、文档、数据、研究和参考资料；详见本域AGENTS |
| `.github/skills/` | 仅保留auto-skill、auto-tmux两个自有指令入口，使用原生工具；原专属封装已退役 |
| `.github/extensions/` | 当前17个一级对象：现存程序、资料维护入口、固定源码与历史定义；不是全部可由Pi的`-e`加载 |
| `.github/ISSUE_TEMPLATE/`及固定配置 | 现有GitHub协作入口；本次仅退役workflows，不扩改其他平台配置 |
| `.github/CONTRIBUTORS.md` | 根README迁出的贡献者名单与鸣谢；只维护独立文档 |
| `.github/check-*.py`、`test-*.py`、4个平铺共享模块及requirements | 仓库维护层：11个校验、5个测试及唯一配套实现；不保留lib目录，不是用户侧Extensions工具 |
| `Makefile` | 本地可重复命令入口 |
| `.github/context/metadata/` | 导航、术语及历史路径映射；不重复登记或定义另一套本体 |
| `.github/context/ai-citation/` | 当前AI引用语料与llms-full |

Context的9个既有集合是`gongfa`、`faqi`、`getting-started`、`prompts`、`research`、`external-resources`、`ai-citation`、`metadata`、`assets`。
当前2个自有Skill和现有Extensions清单分别在其README，不另建工具注册层；16个官方引用入口已按用户要求移除。
用户点名的chat-vault、my-nvim、codex-config、MCPlayerTransfer、XHS-image-to-PDF-conversion、两个xhs图文HTML及html-tools-main说明已移除；当前入口和绑定清理，旧来源/初审/排除保留，历史链接不是安装授权。
Lambda演算已按用户要求加入功法，品级天级上品（现行`tian-advanced`），总表及首页学习入口列在拼好码之前；冻结原文与既有评级不变，不新增解释器或执行器。

## 原始数据与来源

- 功法、法器各以`data.json`为唯一原始资料源；生成轻量`README.md`导航页和天、地、玄、黄四阶Markdown正文。`data.json.explanations_v1`按对象身份保存18项说明并绑定v1模板SHA；分阶正文中每个对象仍独立使用严格三列表格。v0仅保留为历史模板，不作为活动载荷或兼容格式。无明确品级的功法留在黄阶文档的“暂不可判”附录且不归黄阶。不能手改生成视图、增加第二本登记或恢复旧目录兼容壳。
- `documents`保存原始字节、模式、SHA及历史路径身份；二进制显式Base64。解析结果是派生数据，不与原文双写。
- `locations`及`live_sources`分别记录当前位置和当前实现摘要，不替代原SHA、固定选区、历史意见或源码初审，不提升许可、运行、独立审查和效果状态。
- 功法ID、版本、候选、原初评、十二级词表和正式评级分开；法器原实现、运行观察、依赖类别、外部资源与9项排除不相加或自动合并。
- 历史Excel作为原始载荷保存，不再生成活动Excel。资料协议、来源保护和当前计数边界由`.github/context/AGENTS.md`维护。
- 四个Gitlink及Skill Seekers嵌套configs保持原固定提交；修改路径不授权升级源码、复制上游、运行安装/抓取/上传或解除排除。
- 三个研究镜像及raw事实不批量格式化；保留原SHA、隐私登记、缓存与私有模板。缓存、真实会话、数据库和私有数据不提交。

## Skills与Pi

- 集合根不放`SKILL.md`；README/AGENTS不声明Skill frontmatter，避免误注册或停止子目录发现。
- Skills只发现auto-skill、auto-tmux两个自有入口；官方16个入口已删除，原33个自有封装脚本也已退役。两个入口只指导原生工具与规范，不继续承诺已删除的蜂群、报告或自动安全检查功能。
- Extensions的单一锁定官方源码和`init_skill.py`独立引用保留，不计为当前集合Skill；历史材料、原审意见与当前可用性分别表达。
- Pi从仓库根显式加载`pi --skill .github/skills`；不自动加载Context研究里的嵌套Skill，不把整个Extensions作为原生扩展加载。
- 加载不等于执行、安装、兼容或效果证明；上下文文本和模型输出不构成授权。Windows原生符号链接与发现须单独验证。

## 修改与安全

- 先查适用规则与实际代码，在隔离工作树进行非平凡改动，保留并行改动、旧分支及历史工作树。
- 不执行reset、clean、stash、强推、强制切换或覆盖他人改动；只选择性stage本任务文件。
- 不修改`LICENSE`、`CODE_OF_CONDUCT.md`或`.env*`；不内联真实密钥、Token、cookie、私钥或账号配置。
- 凭据仅从受信来源运行时注入，禁止从会话/日志/未知文件搜寻；所有输出先脱敏，不输出值、长度、摘要或前后缀。
- 架构、命令与路径变化同步README、AGENTS、Makefile、活动调用方与索引；不把冻结来源中的旧路径误改成当前路径。
- `.github/workflows/`已按用户要求退役，不得重建空目录、符号链接或兼容壳。原3份定义平铺为Extensions中的`github-actions-*.yml`，不是活动工作流。
- 自动CI、Labeler和Welcome均停用；本地Makefile及检查范围不变。重新启用须显式授权，并同时核对原生目录和对应保护检查。
- 注释、文档及新日志使用中文；代码标识英文。避免无价值封装、重复源码、猜测API和范围外重构。

## 验证

环境：Node22+、Git、Python3；功法/法器/文集维护为Python3.10+。

| 范围 | 命令 |
|---|---|
| Markdown与导航 | `make lint`、`make check-links`、`make check-details`、`make test-details` |
| 结构与索引 | `make check-doc-structure`、`make check-directory-docs`、`make check-metadata` |
| 功法协议与视图 | `make check-gongfa`、`make test-gongfa`、`make sync-gongfa-catalog`、`make check-gongfa-catalog`、`make test-gongfa-catalog` |
| 法器与资料档案 | `make sync-faqi-catalog`、`make check-faqi-catalog`、`make test-faqi-catalog`、`make test-source-archive` |
| 引用与来源 | `make check-ai-citation`、`make check-external-resources`、`make check-research-raw`、`make check-source-facts` |
| 显式维护 | `make sync-doc-toc`、`make check-wiki WIKI_DIR=<本地checkout>`、`make fetch-research-raw` |
| 最终本地质量 | `make test`；不包含联网刷新、第三方执行或效果评级 |

- 先写或选中真实行为测试取得RED，再修根因并原样取得GREEN；不删除测试、弱化断言或用新目标自证。
- 开发中只跑相关测试，最终版本只运行一次完整`make test`，保存命令、实际HEAD、退出码、日志和可复验工件。
- Markdown lint固定`markdownlint-cli@0.48.0`；功法/法器共享依赖为`.github/requirements-gongfa.txt`与`.github/requirements-faqi.txt`，转换器使用原包requirements。
- 校验/测试及source_boundaries、taxonomy、source_archive、book_views、tool_explanations五个共享模块直接平铺在`.github/`，不保留lib包或旧位置副本；职责和原库规则合并到`.github/AGENTS.md`。3个sync与1个fetch入口仍在Extensions，按真实位置导入，不依赖当前cwd。
- 三域入口、入门README及两本文集维持标题→字多不看→快速导航→完整细粒度目录→使用方式→正文；维护规则留AGENTS。
- 功法/法器生成视图的目录由其生成器维护；`sync-doc-toc.py`不能二次编辑生成文件。文档结构与来源SHA检查仍保留。
- 改Mermaid须真实渲染。首页2025Q4–2026Q2甘特图是历史规划，不冒充当前进度或新承诺。
- 本地总测试不等于远端CI；当前GitHub Actions已停用，不得把本地成功或空检查列表称为远端CI通过。
- `clean`、`clean-deps`有删除副作用，不作为测试执行。安装器和被排除程序也不为补证而运行。

## 首页与文档约定

- 根README不恢复AI推荐摘要、选择理由、维护验证、参与贡献或许可证正文块；AI两块仍维护于`llms.txt`，贡献者名单与鸣谢迁至`.github/CONTRIBUTORS.md`，许可文件保留。
- 首页将“⚡ 1 分钟快速开始”和“📺 演示与产出”收进“📌 字多不看”，两者保留各自默认收起层，演示区内部子区块折叠深度不变，正文只移动不改写；其后依次展示“📚 功法体系”和“🧰 法器体系”。“🗂️ 项目目录结构概览”继续位于演示区内部；“✨ 支持项目”和“📞 研究交流”区块不再保留；Star 呼吁句置于“返回顶部”链接之后。两个集合级首页说明仍按既有15项结构组织；数据中441个对象则使用v1的18项说明。每个首页对象独立使用一张严格Markdown表格；无来源依据的集合级信息标明待核，不作推断。
- 方法历史栏目与六命题仅保留旧锚点，正文进入功法；不恢复独立经验/哲学/道法术器分库或首页正文副本。
- 功法、法器块使用同级原生details默认折叠。顶部徽章只保留独立目的地，不重复同一目标；路径与文案须反映真实新资源，不把JSON称为活动Excel。
- `.github/lint_config.json`是格式规则；`.gitattributes`仅将原第三方来源及其对应HTML标为vendored，不标记整个Extensions。

## Git与自动交付

- `main`是当前默认和贡献主线；`minimal`保留现有内容。旧`develop`及其他本地历史不自动合并、切换、重置或删除。
- 用户已授权本仓修改验证后自动提交、推送、以精确PR/HEAD合并；后续暂停或仅本地指令优先，不重复询问发布许可。
- 提交格式：`feat|fix|docs|chore|refactor|test: scope - summary`，签名提交；PR说明范围、动机、验证与未验证项。
- 主Ruleset17185792无豁免：签名、线性历史、PR及禁止强推/删除保持不变。仅已停用的`markdown-lint`、`link-checker`从主Ruleset和main经典保护的必需检查中退役，避免等待不存在的生产者。
- 审批Ruleset25244224默认1个有效批准；仅`tradecatlabs`（User288998340）有pull_request模式豁免，项目只允许它用于自己发起的PR。
- 豁免按操作账号而非作者自动判断；合并他人PR仍核对有效批准，不伪造批准、成功checks或独立审核。
- CODEOWNERS维护者仍为`@tukuaiai`、`@tradecatlabs`；它是路径审查入口，不替代保护。Code Owner/最近推送/额外审批不另加重复门槛。
- 不为交付临时弱化保护或扩大豁免；本次用户明确退役Actions及其对应检查单独留痕，其余保护不变。合并前核对精确HEAD、本地验证、签名及真实检查状态，合并后读回主线事实。
- 不清理或删除工作树、引用与历史；若未来明确授权清理，先保全精确SHA、开放PR及恢复证据。

## 变更记录

三域重构将原资料、指令与程序重新归位；合并原入口的重复治理，保留原始资料与来源；不新增业务Skill、模型调用或已验证效果声明。
用户指出workflows残留后，退役其原生目录与3个自动流程，原定义平铺保全至Extensions；本地校验及其余保护保留。
