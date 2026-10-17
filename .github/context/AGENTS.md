# Context维护规则

## 职责与边界

- 仅维护既有规则、文档、知识、数据、研究及参考资料；对象在本域平铺，不把每条记录拆成目录。
- `getting-started/`保留实例学习；`research/`保留具体对象事实；`prompts/`保留原提示词入口。
- `external-resources/`维护原资源事实；`ai-citation/`维护当前项目引用；`metadata/`只做导航和术语，不另建本体或登记。
- 执行指令归`../skills/`，程序归`../extensions/`；不得把参考材料全部提升为系统指令。

## 功法与法器

- 两者各只有`data.json`维护源和生成的`README.md`；不新增并行登记、旧目录兼容树或活动Excel。
- 载荷`documents`以历史路径为身份。保存原字节、文件模式、SHA、ID、版本、选择器、来源修订、原分类、历史意见及排除项；不得全局改写历史路径。
- `locations`、`live_sources`、`projections`分别描述当前位置、当前实现摘要与现有引用。当前实现绑定不替代原SHA、固定来源、选区或原初审，不自动表示新实现已受审。
- 原始登记仍按载荷内既有Schema和检查器维护。修改原文后须更新其真实摘要；冻结来源、人工初评和正式评级分开，不自动合并语义身份、注册候选、恢复排除或赋级。
- 功法当前80项登记、411条历史/当前总表记录；原迁移基线为79/410，不改历史候选或旧意见。用户新增Lambda演算并指定天级上品，对应`tian-advanced`；总表和原文文集紧随拼好码，正式效果记录仍为零。
- 新整理正文可以直接加入JSON载荷的逻辑文档，不重新创建旧物理目录。先提交首发正文，再以该真实Git修订及JSON载荷选区冻结来源；不能用一个尚不存在正文的基线冒充来源版本。
- 法器73个来源选区、10项来源限定实现、13条本地记录、9条排除、12项依赖对象、8类依赖、158条关联资源和30项重要性赋级各有分母，不能相加为独立产品数。
- `independent_review`、`runtime_verified`、`effectiveness_verified`、`license_approved`未因迁移改变；源码初审不等于许可、身份语义、安装包完整语义或效果验证。

## 来源保护

- 三个`research/vibe-*`源事实镜像按`research/facts/sources.yml`核对文件数、内容摘要、隐私和非公开边界；不得批量格式化。
- `research/*/raw/`的原始API、README、来源清单与Git缓存保持原事实；历史puller路径是来源身份，不冒充当前活动命令。
- 固定外部Git仓库及研究缓存不执行、不抓取、不上传；私有模板、真实会话/数据库、凭据和个人资料不得纳入公开提交。

## 验证与维护

- 运行对应`make sync-gongfa-catalog`或`make sync-faqi-catalog`生成阅读视图；只读检查用`make check-gongfa-catalog`、`make check-faqi-catalog`。
- 资料变更运行相关协议、来源档案、内链、索引与结构检查；最终完整`make test`绑定实际代码和工件，不冒称生产或效果验证。
- 根`README.md`仍是唯一主页；文集和Context入口只负责阅读导航，维护者规则写本文件或既有子域`AGENTS.md`。
