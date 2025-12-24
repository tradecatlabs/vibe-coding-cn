# 工作流集合 (Workflows)

存放各类自动化工作流的目录。

## 目录结构

```
workflow/
├── auto-dev-loop/      # 全自动开发闭环工作流（五步Agent）
├── <其他工作流>/
└── README.md
```

## 已有工作流

| 工作流 | 说明 |
|--------|------|
| [auto-dev-loop](./auto-dev-loop/) | 基于状态机+Hook的五步AI Agent闭环开发流程 |

## 添加新工作流

1. 在此目录下创建子目录
2. 包含必要的配置文件和文档
3. 更新此 README
