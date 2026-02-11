# Obsidian Canvas JSON 规范

## 文件格式

Canvas 文件是 `.canvas` 扩展名的 JSON 文件。

## 顶层结构

```json
{
  "nodes": [],
  "edges": []
}
```

## 节点 (nodes)

### 通用属性

| 属性 | 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `id` | string | ✅ | 唯一标识符 |
| `type` | string | ✅ | 节点类型 |
| `x` | number | ✅ | X 坐标 |
| `y` | number | ✅ | Y 坐标 |
| `width` | number | ✅ | 宽度 |
| `height` | number | ✅ | 高度 |
| `color` | string | ❌ | 颜色编号 (1-6) |

### 文本节点 (text)

```json
{
  "id": "node-1",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 100,
  "text": "# 标题\n\n内容支持 Markdown"
}
```

### 文件节点 (file)

```json
{
  "id": "node-2",
  "type": "file",
  "x": 300,
  "y": 0,
  "width": 200,
  "height": 100,
  "file": "path/to/file.md"
}
```

### 链接节点 (link)

```json
{
  "id": "node-3",
  "type": "link",
  "x": 600,
  "y": 0,
  "width": 200,
  "height": 100,
  "url": "https://example.com"
}
```

### 分组节点 (group)

```json
{
  "id": "group-1",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 500,
  "height": 300,
  "label": "分组名称"
}
```

## 连线 (edges)

### 属性

| 属性 | 类型 | 必需 | 说明 |
|:---|:---|:---|:---|
| `id` | string | ✅ | 唯一标识符 |
| `fromNode` | string | ✅ | 起始节点 id |
| `toNode` | string | ✅ | 目标节点 id |
| `fromSide` | string | ❌ | 起始边 (top/right/bottom/left) |
| `toSide` | string | ❌ | 目标边 (top/right/bottom/left) |
| `fromEnd` | string | ❌ | 起始端样式 (none/arrow) |
| `toEnd` | string | ❌ | 目标端样式 (none/arrow) |
| `label` | string | ❌ | 连线标签 |

### 示例

```json
{
  "id": "edge-1",
  "fromNode": "node-1",
  "toNode": "node-2",
  "fromSide": "right",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "调用"
}
```

## 颜色编码

| color | 颜色 | 建议用途 |
|:---|:---|:---|
| `1` | 红色 | 缓存、热点、警告 |
| `2` | 橙色 | 消息队列、异步 |
| `3` | 黄色 | 上游依赖、外部输入 |
| `4` | 绿色 | 数据库、持久化 |
| `5` | 蓝色 | 搜索、外部服务 |
| `6` | 紫色 | 注释、设计决策 |

## 布局建议

### 三层架构布局

```
x: -400    x: 0      x: 400    x: 800
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ 前端   │→│ API    │→│ 服务   │→│ 数据   │
└────────┘ └────────┘ └────────┘ └────────┘
```

### 间距建议

- 节点宽度: 200-280
- 节点高度: 80-150
- 水平间距: 100-150
- 垂直间距: 120-150

## 完整示例

```json
{
  "nodes": [
    {
      "id": "group-api",
      "type": "group",
      "x": -50,
      "y": -50,
      "width": 300,
      "height": 200,
      "label": "API 层"
    },
    {
      "id": "api-user",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 200,
      "height": 100,
      "text": "# UserAPI\n\n- GET /users\n- POST /users"
    },
    {
      "id": "svc-user",
      "type": "text",
      "x": 350,
      "y": 0,
      "width": 200,
      "height": 100,
      "text": "# UserService\n\n- get_user()\n- create_user()"
    },
    {
      "id": "db",
      "type": "text",
      "x": 700,
      "y": 0,
      "width": 200,
      "height": 80,
      "text": "# PostgreSQL",
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "api-user",
      "toNode": "svc-user",
      "fromSide": "right",
      "toSide": "left",
      "label": "调用"
    },
    {
      "id": "e2",
      "fromNode": "svc-user",
      "toNode": "db",
      "fromSide": "right",
      "toSide": "left"
    }
  ]
}
```
