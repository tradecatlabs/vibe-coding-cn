# TradeCat Sheets API 使用说明（公开表格 + API 注册表）

本文档用于把 TradeCat 的公开 Google Sheet 当作 **Agent 可消费的数据面（Data Plane）**：通过 `API` 表（注册表）发现端点，并用表内提供的请求命令拉取结构化 JSON（行情/指标/预测市场/实时新闻）。

> 更新时间：2026-03-17（以 `API` 表导出时间为准）

---

## 1. 公共链接

- 在线表格（含 `API` 注册表页）：  
  `https://docs.google.com/spreadsheets/d/1q-2sXGsFYsKf3nV5u5golTVrLH5sfc0doiWwz_kavE4/edit?usp=sharing`

---

## 2. 你得到的是什么

### 2.1 `API` 表 = Endpoint Registry（端点注册表）

`API` 表每一行对应一个端点，包含三列：

- `jsonl`：端点返回的 JSON（通常包含压缩 payload）
- `说明`：端点用途/结构（人读）
- `请求命令`：可复制执行的命令（机器读/人也可直接复制）

### 2.2 推荐用法：直接复制 `请求命令`

表中 `请求命令` 通常是 `curl ... | python3 -c ...`：

- `curl` 从 Google Sheets gviz 接口取出该行 `jsonl`
- `python3 -c` 负责解析 JSON、解压 `gzip_b64`（如存在）并输出最终结构化 JSON

这样做的好处：
- 不需要你自己实现 gzip_base64 解码逻辑
- 输出格式相对稳定（以表内命令为准）

---

## 3. 快速开始

### 3.1 拉取 API 注册表（CSV）

```bash
SHEET_ID="1q-2sXGsFYsKf3nV5u5golTVrLH5sfc0doiWwz_kavE4"
curl -fsSL "https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=API&headers=0" > api.csv
```

### 3.2 列出端点标题（从 `jsonl` 里解析）

```bash
python3 - <<'PY'
import csv, io, json, sys
raw=open("api.csv","r",encoding="utf-8",errors="replace").read()
rows=list(csv.reader(io.StringIO(raw)))
for r in rows[3:]:  # 跳过 banner/导出信息/表头
    if len(r) < 1 or not r[0].strip().startswith("{"):
        continue
    try:
        obj=json.loads(r[0])
    except Exception:
        continue
    sheet=(obj.get("data") or {}).get("sheet") or {}
    title=sheet.get("title")
    gid=sheet.get("gid")
    payload=(obj.get("data") or {}).get("payload") or {}
    schema=payload.get("schema") or payload.get("facts_schema") or ""
    if title:
        print(f"- {title} (gid={gid} schema={schema})")
PY
```

### 3.3 拉取某个端点（推荐）

到表格 `API` 页，找到目标端点行，复制其 `请求命令` 直接执行即可。

---

## 4. 返回格式（Envelope）

端点 JSON 通常遵循如下“信封”结构（字段名以实际返回为准）：

- `code` / `msg` / `success`：状态
- `data.banner`：公告/广告位等文本（消费方可选择忽略）
- `data.meta`：生成时间、生产者、语言等
- `data.sheet`：来源表格信息（`spreadsheet_id/gid/title`）
- `data.payload`：**真正的数据**（可能包含压缩编码或已解码后的事实列表）

强烈建议消费方至少校验：
- `data.payload.schema`（或 `facts_schema`）是否是预期的 schema
- `data.meta.generated_at` / `export_time` 是否足够新鲜

---

## 5. Schema 说明（当前已观察到）

> 以 `API` 表当前内容为准；未来可能新增 schema。

### 5.1 `table_rows_v2`

用于“表格快照”类数据（看板/Polymarket/新闻）。

典型用途：
- 看板总览、Top 列表、统计表、新闻流

消费建议：
- 以 `facts[]`（如存在）为单一事实来源
- 每条 fact 通常包含维度（dims）与字段（fields_text/fields_num）等

### 5.2 `symbol_query_v2`

用于“单币种多周期指标面板”类数据（BTC/ETH/BNB/SOL）。

典型用途：
- 单币画像、指标诊断、策略特征输入、AI 分析上下文

消费建议：
- 以 `facts[]`（如存在）为单一事实来源
- 不要依赖 UI 文案；依赖结构化指标字段

---

## 6. 端点清单（2026-03-17 快照）

以下端点来自 `API` 表当前解析结果（title/gid/schema）：

### 市场总览（table_rows_v2）

- 加密货币看板（gid=1277788455, schema=table_rows_v2）
- 宏观大宗看板（gid=1931661963, schema=table_rows_v2）

### 单币画像（symbol_query_v2）

- 币种查询_BTCUSDT（gid=1325757221, schema=symbol_query_v2）
- 币种查询_ETHUSDT（gid=904473439, schema=symbol_query_v2）
- 币种查询_BNBUSDT（gid=78880380, schema=symbol_query_v2）
- 币种查询_SOLUSDT（gid=208400041, schema=symbol_query_v2）

### 预测市场（table_rows_v2）

- PolymarketTop15（gid=1715937602, schema=table_rows_v2）
- Polymarket时段分布（gid=333189916, schema=table_rows_v2）
- Polymarket类别偏好（gid=1923964075, schema=table_rows_v2）

### 实时新闻（table_rows_v2）

- 实时新闻（gid=1419246950, schema=table_rows_v2）

---

## 7. 可靠性与调用建议（给 Agent/服务端）

由于底层是公开 Google Sheet：

- 建议做 **缓存**（例如 5～60 秒，按业务容忍度）
- 建议做 **退避重试**（遇到 429/5xx 时指数退避）
- 建议做 **降级策略**
  - 表不可用：降级为“只读旧缓存”
  - 新闻不可用：只跑行情/指标
  - schema 不匹配：拒绝消费该批数据

---

## 8. 合规与安全边界

- 本接口与本文档不构成投资建议；仅用于研究与协作交流。
- 不要在任何公开场合贴出内部密钥/Token（本表为公开资产，不应包含密钥；但消费方也不应添加敏感头部到公开日志里）。

