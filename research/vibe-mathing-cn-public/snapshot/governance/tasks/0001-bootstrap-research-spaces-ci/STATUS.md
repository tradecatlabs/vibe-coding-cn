# Public task status

本任务已交付为公开、可移植的研究空间基础契约。该状态页只描述版本化能力，不记录临时工作区、运行会话、机器身份或动态执行回执。

## 已发布能力

- Problem、Attempt、Result schema 与只读 Solution View 派生规则；
- 可信 evidence receipt、独立 verifier registry、WAL/唯一 writer 与 bounded runtime；
- 公开 CI 使用的 `make check` 和治理 strict/health 入口。

## 当前边界

canonical Problem、Attempt、Result 和 Solution View 业务记录保持为空。公开仓只发布契约、合成 fixture、校验器和文档；ignored raw、电子书、供应链缓存与运行时产物由调用者在本地重建。

## 复核入口

```bash
make check
python3 scripts/validate_public_boundary.py --project-root .
python3 governance/tools/validate_governance_package.py --project-root . --strict
```

公开仓库：[vibemathing/vibe-mathing-cn-public](https://github.com/vibemathing/vibe-mathing-cn-public)。
