# Completion Exemplar：公开数学问题目录本地化

## 目标与边界

把 Wikipedia 指定列表页和 UnsolvedMath 全部分页转为可追溯、可重建、可离线查询的问题库。完整性只覆盖来源目录条目；不镜像 UnsolvedMath 详情正文、评论或登录后数据。

## 实际完成路径

1. 先探测许可、`robots.txt`、`sitemap.xml`、分页总数和代表性 DOM。
2. Wikipedia 使用官方 MediaWiki API，绑定 revision、SHA-1 和 CC BY-SA 4.0 归属。
3. UnsolvedMath 串行限速抓取 109 个服务端目录页，保存每页原始 HTML 与 SHA-256。
4. 两个来源规范化为统一 JSONL，并生成来源、分类和统计索引。
5. 从原始快照重算覆盖率、schema、哈希、冲突账本和索引，拒绝自报完成。

## 关键决策

- UnsolvedMath 的 5,426 个目录行只有 5,375 个不同源 ID；保留全部行，用卡片内容指纹生成本地 ID，并公开 35 组冲突和 51 个超额行。
- 原始缓存与派生记录分层；默认缓存重建，只有 `--refresh` 发起网络请求。
- 未知许可来源只保存目录事实、短摘要与链接，不复制详情全文。

## 失败与修复

- Wikipedia 初次解析错误地从 `body` 直接遍历，得到 0 条；原始快照证明章节位于 `.mw-parser-output`，最小修复容器根并补回归测试。
- 初版错误假设 UnsolvedMath 源 ID/URL 唯一；全量门禁发现冲突后改为内容指纹主键，没有静默丢弃数据。

## 验证与恢复

```bash
python3 scripts/validate_problem_library.py
python3 scripts/test_problem_library.py
python3 scripts/query_problem_library.py --text Riemann --limit 10
```

恢复方式：原始缓存完整时直接运行抓取脚本重建；需更新来源时使用 `--refresh`。结构漂移、页数不全、schema/哈希/计数不一致时必须非零终止。

## 复用边界

适用于公开、分页、允许合理访问的目录型知识来源。若来源要求认证、禁止抓取、许可不允许本地复制、分页依赖不稳定会话或数据规模达到当前 100 倍，应重新设计授权、存储和增量策略。

这是单次完成范例，不是 active SOP；晋升至少还需要独立重复成功、外部审查和版本绑定回执。
