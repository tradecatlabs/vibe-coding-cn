# MC Player Transfer

Minecraft 基岩版角色转移工具 - 像泰拉瑞亚一样转移角色

## 项目结构

```
MCPlayerTransfer/
├── main.py              # 主入口
├── requirements.txt     # 依赖
├── README.md
├── src/
│   ├── __init__.py
│   ├── extract_player.py   # 提取模块
│   └── import_player.py    # 导入模块
├── input/               # 放入 .mcworld 文件
└── output/              # 输出 .dat 角色文件
```

## 安装

```bash
pip install -r requirements.txt
```

## 使用

### 提取角色
```bash
python main.py extract "input/World.mcworld"
```

### 导入角色
```bash
python main.py import "input/另一个世界.mcworld" "output/player.dat"
```

## 数据说明

提取的 `.dat` 文件包含角色全部数据：
- 背包物品
- 末影箱物品
- 潜影盒及内容
- 装备栏
- 经验等级
- 生命/饥饿值
- 位置坐标

## 注意事项

- 操作前备份存档
- 关闭游戏后操作
