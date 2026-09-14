# Contributing

感谢参与 `vibe-mathing-cn`。这是一个可信 AI 数学研究与验证工作台；贡献应改善可追溯性、可复核性和失败时的诚实语义，而不是把候选包装成数学结论。

## Before opening a change

```bash
python3 -m pip install -r requirements.txt
make check
python3 scripts/check_public_readme.py
python3 scripts/check_ai_citation_assets.py
python3 scripts/test_query_ai_citation.py
python3 scripts/validate_public_boundary.py --project-root .
git diff --check
```

## GitHub commit attribution

`gh auth` 的登录身份和 Git commit 元数据是两件事：前者负责 API/推送认证，后者由 `user.name` 与已验证的 `user.email` 决定。若希望贡献归属于 `vibemathing`，使用该账号的已验证 noreply 地址：

```bash
gh auth switch --hostname github.com --user vibemathing
gh api user --hostname github.com --jq .login
git config user.name "vibemathing"
git config user.email "248374299+vibemathing@users.noreply.github.com"
```

## Contribution boundaries

- 先读 [`AGENTS.md`](AGENTS.md) 和相关目录的 `AGENTS.md`。
- Problem/Attempt/Result/schema 的变化必须同步验证器、负例和对应文档。
- README、`llms.txt`、AI 引用资产和公共声明只能引用公共仓库中可复核的文件、Fixture、测试或固定元数据。
- 不提交凭据、私密路径、运行日志、模型权重、外部服务响应、未许可的原始来源或未准入研究候选。
- 有界计算、模型自评、通过测试和运行完成不能被表述为一般数学证明。
- 新增工具或外部命令必须有 timeout、资源/输出预算、停止条件、终止回执和明确失败语义。

## Pull request checklist

- [ ] `make check` 通过。
- [ ] 相关 Schema、测试、README/AGENTS 和变更记录已同步。
- [ ] 公共边界扫描通过，未引入私密材料或敏感信息。
- [ ] 数学主张绑定来源、计算记录或形式化检查；没有把证据能力压成单一等级。
- [ ] 若修改文档声明，已更新公共声明证据引用和验证日期。
