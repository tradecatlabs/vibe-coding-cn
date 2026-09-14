# 外部源事实层维护规则

## 目录职责

`research/facts/` 只保存外部源仓库的事实登记和隐私审计记录。它不是普通研究域，不使用 `domain.yml`、`analysis.md` 或 `deep-dive.md` 作为入口。

## 源镜像规则

- `research/vibe-cybersecurity-cn/`、`research/vibe-harness-cn/` 和
  `research/vibe-mathing-cn-public/` 是源仓库根目录的已提交文件树；只有隐私安全所需的本机路径可替换为可移植占位符。
- 同步使用源仓库固定分支的 `git archive`；必须记录 commit、tree、文件数和 archive SHA-256。
- 不复制 `.git`、Git 历史、未跟踪文件、ignored 缓存、虚拟环境或私密材料；源仓库已提交的证据/日志文件若属于固定树则保留，源文件中出现的机器路径必须在纳入前清除。
- 不在源镜像目录添加本仓库的研究包装文件，也不把源文件移动到 `snapshot/` 等二级目录。
- 源仓库有独立验证契约时，按源仓库自己的入口验证；父仓库只验证事实登记和边界。

## 审计与历史材料

此前重分类产生的附加文件和被改写的源文件版本已移出公开工作树，存放在父仓库 ignored 的内部归档中。它们不属于源镜像，不注册为 skill，不自动执行，也不作为研究结论。

## 变更验证

```bash
make check-source-facts
make test
```
