# 数学电子书文献库

本目录采用 Work → Edition → File 三层模型，并以 MSC2020 作为数学主题分类。一本书只保存一个文件实体，但可通过 MSC、研究用途和关系进入多个检索视图。

## 当前馆藏

### 数学大辞典（第二版）

- 主编：王元；副总主编：文兰、陈木法
- 出版社：科学出版社
- 版次与时间：第二版，2017 年 9 月
- ISBN：`978-7-03-053336-4`
- 分类：`MSC2020 00A20` — Dictionaries and other general reference works
- 类型：`dictionary`
- 研究角色：`reference`、`terminology_lookup`
- 阅读状态：`reference_only`
- 文件：[数学大辞典（第二版）.pdf](files/9787030533364/数学大辞典（第二版）.pdf)
- SHA-256：`84f60535a2056ea3ceee64b3b0a5f374cd1b41aff7c11fbd452e3ae43d71f148`

该书覆盖大量数学分支，但其书目本质是综合辞典，因此只使用 `00A20` 作为主分类；具体分支属于内容覆盖范围，不作为辅助 MSC 无限展开。

## Provider registry

`providers.json` 登记 arXiv、Crossref、OpenAlex 和 Semantic Scholar 的公开请求形状、timeout、重试和响应格式，并为每个响应设置 1 MiB 上限。凭据只从环境变量读取，默认检查离线运行；`--live` 只做 HTTPS 有界健康检查，不保存全文或 credential。

```bash
python3 scripts/check_literature_providers.py
python3 scripts/check_literature_providers.py --live --provider arxiv
```

## 维护

```bash
python3 scripts/validate_literature.py
```

validator 会校验 JSON Schema、ISBN-13 校验位、Work/Edition/File 引用、文件大小与 SHA-256。大型电子书只保存在 `files/`，目录记录和 schema 才是可版本化资产。
