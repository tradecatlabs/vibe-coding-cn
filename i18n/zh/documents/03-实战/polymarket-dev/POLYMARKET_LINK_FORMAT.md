# Polymarket 链接格式规范

## 问题描述

生成的 Polymarket 链接返回 "Oops...we didn't forecast this" 错误页面，即使 HTTP 状态码是 200。

## 根本原因

Polymarket API 返回两种不同的 slug：

| 字段 | 名称 | 用途 |
|------|------|------|
| `slug` | Market Slug | 市场标识，**不能用于 URL** |
| `events[0].slug` | Event Slug | 事件标识，**必须用于 URL** |

### 示例对比

```
市场: "Lighter market cap (FDV) >$1B one day after launch?"

API 返回:
  slug: "lighter-market-cap-fdv-1b-one-day-after-launch"        ❌ 错误
  events[0].slug: "lighter-market-cap-fdv-one-day-after-launch" ✅ 正确

错误链接: https://polymarket.com/event/lighter-market-cap-fdv-1b-one-day-after-launch
正确链接: https://polymarket.com/event/lighter-market-cap-fdv-one-day-after-launch
```

注意差异：market slug 包含 `-1b-`，event slug 不包含。

## 为什么 HTTP 200 但页面报错？

Polymarket 前端是 SPA（单页应用）：
- 所有 `/event/*` 路径都返回 HTTP 200（返回 HTML 壳）
- 前端 JS 加载后再请求数据
- 如果 slug 无效，前端显示 "Oops" 错误

**结论：HTTP 状态码无法验证链接有效性。**

## 正确的链接生成方式

```javascript
// ✅ 正确
const getLink = (market) => {
  const events = market.events || [];
  const slug = events[0]?.slug || market.slug;  // 优先用 event slug
  return `https://polymarket.com/event/${slug}`;
};

// ❌ 错误
const getLink = (market) => {
  return `https://polymarket.com/event/${market.slug}`;
};
```

## API 响应结构

```json
{
  "question": "Lighter market cap (FDV) >$1B one day after launch?",
  "slug": "lighter-market-cap-fdv-1b-one-day-after-launch",
  "events": [
    {
      "slug": "lighter-market-cap-fdv-one-day-after-launch",
      "title": "Lighter Market Cap (FDV) One Day After Launch"
    }
  ]
}
```

## 验证方法

不能只检查 HTTP 状态码，需要：

```bash
# 方法1：检查页面内容是否包含错误
curl -s "https://polymarket.com/event/xxx" | grep -q "didn't forecast" && echo "无效"

# 方法2：对比 API 返回的 slug
curl -s "https://gamma-api.polymarket.com/markets?slug=xxx" | jq '.events[0].slug'
```

## 受影响的文件

修复时需检查以下文件中的链接生成逻辑：

- `scripts/csv-report-api.js`
- `scripts/csv-report.js`
- `signals/*/formatter.js`（如有生成链接）

## 修复记录

- **日期**: 2024-12-31
- **问题**: csv-report-api.js 使用 `m.slug` 生成链接
- **修复**: 改为 `m.events[0]?.slug || m.slug`

---

**规则：任何生成 Polymarket 链接的代码，必须使用 `events[0].slug`，不能使用 `slug`。**
