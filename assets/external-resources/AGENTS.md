# assets/external-resources/ Agent 指南

本目录维护本地外部资源注册表，是外部资源从在线表格迁入仓库后的结构化真相源。

## 目录职责

```text
external-resources/
├── README.md                    # 入口说明
├── AGENTS.md                    # 本目录维护规则
├── resources.yml                # 分类索引、导入来源、统计和治理策略
├── schema.yml                   # 字段契约与枚举
├── quality-report.md            # 导入质量与人工复核清单
├── network-payment-services.yml # 网络与支付服务
├── creator-accounts.yml         # 博主账号
├── tools-platforms.yml          # 工具与平台
├── communities-forums.yml       # 社区与论坛
├── repo-rules-scaffolds.yml     # 仓库、规则与脚手架
├── docs-courses.yml             # 文档与课程
├── books.yml                    # 书单
└── archive.yml                  # 下线、失效、废弃或被替代资源
```

## 边界

- 这里保存资源索引，不复制第三方正文、课程内容、书籍内容、仓库源码或二进制附件。
- 外部工具源码、完整第三方仓库、fork 和 submodule 放在 `tools/external/`。
- 对单个资源形成研究结论时，放入 `research/`，并从资源记录回链。
- 资源被正式写入教程正文前，必须人工复核可用性、许可证、合规风险和推荐口径。

## 字段规则

- `id` 必须全局唯一，使用小写短横线风格，禁止改已有 ID；重命名资源只改 `name`。
- `link.kind=external_url` 时必须填写 `url` 和 `domain`。
- 非 URL 入口必须使用 `locator`，并保持 `status: needs-review`。
- 缺失链接、推广参数、金融服务、访问合法性风险必须写入 `risk_flags`。
- `verification_status: imported-unverified` 表示只完成导入，不能当作已推荐资源。

## 更新流程

1. 修改对应分类文件。
2. 必要时更新 `resources.yml` 的分类统计。
3. 对失效、废弃或不再推荐资源，迁入 `archive.yml`，不要直接删除历史。
4. 运行 `make check-external-resources`。
5. 如果入口、命令或目录边界变化，同步更新 `assets/README.md`、根 `README.md`、
   `AGENTS.md`、`llms.txt` 和相关 metadata。
