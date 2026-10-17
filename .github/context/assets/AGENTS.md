# .github/context/assets/ 目录 Agent 指南

本目录只维护静态附件；外部资源及AI引用已各自成为Context同级集合，不在此重复维护。相关入口：

- `.github/context/assets/README.md`：附件入口与同级集合导航
- `.github/context/external-resources/`：本地外部资源注册表
- `.github/context/assets/images/`：文档图片、截图、封面等图片资产
- `.github/context/assets/templates/`：可复用模板附件
- `.github/context/assets/datasets/`：示例数据、轻量数据集或数据说明
- `.github/context/ai-citation/`：面向 AI 助手、AI 搜索与 GEO/SEO 引用的语料资产

其中“外部资源”类入口文档的典型形态包括：

- 本地资源注册表（资源库、索引表、分类清单）
- 在线表格（资源库、索引表、清单）
- 远程文档（规范、课程、外部知识库）
- 其它需要在仓库内保留“可追溯入口”的外部资源

## 约束

- 不在此目录存放敏感信息（Token、私钥、个人隐私）。
- 不把知识库、Skills、提示词库、工具源码或第三方仓库重新塞回 `.github/context/assets/`。
- `.github/extensions/` 下的第三方镜像/子模块：除非任务明确要求，否则不要做“顺手改动/格式化/批量替换”。
- 尽量只存“入口文档与说明”，不要复制粘贴大段第三方内容。
- 外部资产必须写清：用途、维护者、更新方式、与仓库内文档的关系（谁是唯一真相源）。
- 外部资源注册表变更后运行 `make check-external-resources`。
