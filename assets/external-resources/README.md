# External Resources

本目录存放从外部资源表格本地化后的资源注册表。

这里保存的是资源索引、分类、状态和治理字段，不保存第三方大段内容、工具源码或二进制附件。

## 入口

| 文件 | 用途 |
|:---|:---|
| `resources.yml` | 本地资源注册表总入口，登记分类文件、统计和治理策略 |
| `schema.yml` | 字段契约、枚举值和维护规则 |
| `quality-report.md` | 导入质量报告：缺失链接、非 URL、重复 URL 和风险标记 |
| `network-payment-services.yml` | 网络与支付服务 |
| `creator-accounts.yml` | 博主账号 |
| `tools-platforms.yml` | 工具与平台 |
| `communities-forums.yml` | 社区与论坛 |
| `repo-rules-scaffolds.yml` | 仓库、规则与脚手架 |
| `docs-courses.yml` | 文档与课程 |
| `books.yml` | 书单 |
| `archive.yml` | 下线、废弃或不再推荐的资源 |

## 存储原则

- 分类文件是资源数据的真相源，`resources.yml` 只做总入口和统计。
- 每条资源必须有稳定 `id`、`name`、`resource_type`、`link.kind`、`status` 和
  `verification_status`。
- 导入状态只代表结构化成功，不代表外链可用、内容合法、许可证可用或推荐等级。
- 第三方工具源码、完整仓库和 submodule 仍然放在 `tools/external/`。
- 图片、模板、轻量数据集仍然放在 `assets/images/`、`assets/templates/`
  和 `assets/datasets/`。

## 验证

```bash
make check-external-resources
```

修改本目录后，建议运行：

```bash
make test
```
