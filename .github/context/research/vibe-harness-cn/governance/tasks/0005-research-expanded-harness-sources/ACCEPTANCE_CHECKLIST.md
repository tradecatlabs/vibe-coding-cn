# Acceptance Checklist

# Global Standards
- [x] 研究报告覆盖 11 个新增 Harness，结论绑定 revision 与源码路径。
- [x] 未执行上游代码、未读取或输出凭据，checkout 保持 ignored。
- [x] 任务意图、验证计划、项目 capability、governance/task validators 全部 PASS。
- [x] 文档同步、审查边界与本地交付已记录。

# Task Package Checklists
## TP-01
- [x] 11 个 Harness 逐仓完成六类维度调研。
- Verify: `research/HARNESS_RESEARCH.md` 每仓小节。
- Gate: 结论可溯源，宣传/实现差异显式标注。

## TP-02
- [x] 横向比较表与元 Harness 治理借鉴已写入领域文档。
- Verify: `docs/HARNESS_MODEL.md`、`research/UPSTREAMS.md`。
- Gate: 借鉴结论与具体实现分离。

## TP-03
- [x] 文档校验、门禁、治理与本地提交完成。
- Verify: governance strict/health、task validators、15 源一致性。
- Gate: 当前输入无 BLOCK 且工作树 clean。
