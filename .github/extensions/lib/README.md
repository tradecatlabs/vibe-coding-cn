# Extensions共享库

本目录只支撑既有仓库检查与两本文集维护，不是资源加载器或程序运行框架。

| 文件 | 职责 |
|---|---|
| `__init__.py` | 迁移后的原第三方、镜像与研究缓存边界；各检查器保留自己的原范围差异 |
| `taxonomy.py` | 用原轻量YAML子集读取Context分类与文档导航 |
| `source_archive.py` | 严格读取JSON原始载荷，核对字节/模式/SHA、当前位置、当前实现及隔离复原 |
| `book_views.py` | 复用既有链接规则与markdown-it-py，生成文集的命名空间锚点、重定向与目录；代码示例不改写 |

`source_archive.py`在显式调用时读取原始资料；只有`export_documents`向调用者指定的新隔离目录还原，不生成旧运行目录。
导入阶段不写文件、不联网、不执行目标程序；book_views仅加载本仓既有链接检查器的规则函数。
修改后先运行相关协议和`make test-source-archive`，最终完整`make test`按根AGENTS执行。
