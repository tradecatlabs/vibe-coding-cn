# Literature Library Agent Guide

本目录管理数学电子书的书目事实、研究分类和本地文件。`catalog/*.jsonl` 是机器真相源；`files/` 是不进入 Git 的本地二进制馆藏；不得从文件夹位置反推一本书只能属于一个主题。

## 目录结构

```text
literature/
├── AGENTS.md                         # 本目录边界与维护规则
├── README.md                         # 分类方法、馆藏说明与运行方式
├── catalog/
│   ├── works.jsonl                   # 作品、作者角色、MSC 与研究用途
│   ├── editions.jsonl                # 版次、出版社、ISBN 与书目来源
│   ├── files.jsonl                   # 本地文件路径、格式、大小和 SHA-256
│   └── relations.jsonl               # Work → Edition → File 及研究关系
├── schema/
│   ├── literature-records.schema.json # 四类目录记录契约
│   └── literature-providers.schema.json # 文献 provider 请求契约
├── providers.json                       # 非敏感 provider registry
└── files/
    └── 9787030533364/
        └── 数学大辞典（第二版）.pdf  # 本地馆藏，不进入 Git
```

## 分类与职责边界

- 主题分类采用 MSC2020；每个 Work 一个主 MSC、零至五个辅助 MSC。
- 跨领域综合参考书使用 `00A20`，不复制到每个数学分支目录。
- Work 表达知识作品；Edition 表达语言、版次、出版信息和 ISBN；File 表达本机具体 PDF/EPUB。
- 书内 CIP、版权页和 PDF 元数据优先于零售网页；冲突必须记入 `cataloging_notes`，不得静默覆盖。
- 权利未知时写 `unknown`；不得根据文件存在推断所有权、开放许可或再分发权。
- `files/` 不进入 Git，不自动上传，不从未知来源补齐电子书。
- `providers.json` 只保存公开 endpoint、timeout、重试、响应格式和可选环境变量名；credential 值只能来自进程环境，live health 必须显式开启且不保存正文。

## 维护命令

```bash
python3 scripts/validate_literature.py
python3 scripts/check_literature_providers.py
```

新增电子书前先计算 SHA-256 去重，再建 Work/Edition/File；移动、重命名或替换文件后必须同步目录并运行 validator。
