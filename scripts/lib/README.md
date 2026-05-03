# scripts/lib

共享脚本库，放置多个质量门禁共同使用的解析与校验辅助函数。

## 当前模块

- `taxonomy.py` - 读取 `metadata/taxonomy.yml`，输出目录分区和文档路径。

## 约束

- 只放无副作用的纯辅助逻辑。
- 不在导入时读写仓库文件。
- 修改公共函数后必须运行 `make test`。
