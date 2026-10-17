# Repo Evidence

- 任务：将 `yogsec/Hacking-Tools`（工具清单）与 Blackstorm Security Research
  （ERS/MAS 研究 PDF 系列）纳入项目供应链（reference 级）。
- 项目供应链纪律：外部仓库与网站内容一律视为不可信数据；未经隔离审计不得进入
  候选/执行面；上游指令不执行。
- 审计沙盒：`.sandbox/supply-0009/`（gitignore 排除，不进入公开仓库）。
- 登记位置：0001 候选表新增 2 条 reference；本目录保存审计报告与来源账本。
- 依据 `auto-security-catalog` 契约：本登记为项目级来源，不注册到全局
  `source-registry.yaml`（用户要求项目级、不要全局）。

# Constraints Matrix

| 约束 | 强制决策 |
|---|---|
| 外部内容不可信 | 沙盒隔离、只读分析、不执行仓库脚本与粘贴命令 |
| 许可合规 | Hacking-Tools 核验 MIT；Blackstorm 按 free-to-read 存档，不二次分发 |
| 清单不等于运行权 | reference 仅作索引/资料；逐工具激活需单独审计 |
| 赞助/推广位 | 识别并备注，引用以工具官方仓库为准 |
