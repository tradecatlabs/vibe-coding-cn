# Security policy

## Scope

本仓库的安全范围包括公共发布边界、凭据/路径泄露、未受限外部命令、symlink 逃逸、无界输出以及会把候选误写成数学结论的验证路径。

数学命题本身的正确性不由本文件或 `make check` 认证；Result 仍必须遵守项目的 evidence、独立性和 statement-faithfulness 规则。

## Reporting a release or code issue

不要在公开 issue、讨论区或 pull request 中粘贴凭据、私密路径、内部端点或运行日志。请使用 GitHub 仓库的 [Security advisories](https://github.com/vibemathing/vibe-mathing-cn-public/security/advisories/new) 私密报告入口；若该入口不可用，先提交不含敏感细节的公开说明，并请求维护者提供安全沟通渠道。

## Built-in checks

提交前运行：

```bash
python3 scripts/test_validate_public_boundary.py
python3 scripts/validate_public_boundary.py --project-root .
python3 scripts/check_public_readme.py
python3 scripts/check_ai_citation_assets.py
make check
```

这些检查发现的是仓库边界和工程协议问题，不是外部安全认证，也不是数学证明。
