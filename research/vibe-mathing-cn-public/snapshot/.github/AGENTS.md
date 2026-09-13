# GitHub Automation Agent Guide

本目录只管理 GitHub 平台入口。`workflows/ci.yml` 在 push 与 pull request 上执行可移植质量门，不访问网络来源、不读取本地电子书，也不发布研究结论。

## 目录结构

```text
.github/
├── AGENTS.md
└── workflows/
    ├── AGENTS.md
    └── ci.yml
```

## 边界

- workflow 只授予 `contents: read`。
- 不在 CI 中保存凭据、上传电子书、刷新网页快照或修改派生索引。
- 新增、删除或移动 workflow 时同步更新本文件和 `workflows/AGENTS.md`。
- 本地验证入口必须与 CI 共用 `make check`，避免两套真相。
