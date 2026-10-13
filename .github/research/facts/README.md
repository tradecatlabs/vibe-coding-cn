# 外部源事实层

本目录只记录外部源仓库的可核验事实，不是研究域，不承载分析、迁移判断或深度研究格式。

## 事实对象

- `../vibe-cybersecurity-cn/`：`vibe-cybersecurity-cn` 的已提交源文件树。
- `../vibe-harness-cn/`：`vibe-harness-cn` 的已提交源文件树。
- `../vibe-mathing-cn-public/`：`vibemathing/vibe-mathing-cn-public` 的已提交源文件树。

三个目录都保持源仓库根目录布局；本仓库不复制源仓库 `.git`、历史、未跟踪文件、缓存、运行产物或私密材料。源文件中发现的本机路径必须先替换为可移植占位符，并在事实登记中记录。

## 事实登记

- [`sources.yml`](sources.yml)：源仓库提交、树哈希、文件数、归档哈希、镜像内容摘要、镜像路径和审计边界。
- [`privacy-audit.yml`](privacy-audit.yml)：只记录路径、行号、类别和处置状态，不记录凭据值、邮箱值或本机绝对路径；同时明确区分当前工作树与未改写的历史。
- 此前错误研究域导入产生的附加材料已移入仓库外的 ignored 内部归档，不进入公开事实层；需要复核时只能从内部归档重新取证。

## 维护边界

源镜像只能从源仓库已提交分支重新生成；不得在镜像目录内添加本仓库的 README、AGENTS、domain、analysis、deep-dive 或其他包装层。需要增加事实字段时，更新 `sources.yml`；隐私修复只能做最小可移植化替换，并记录变更。
