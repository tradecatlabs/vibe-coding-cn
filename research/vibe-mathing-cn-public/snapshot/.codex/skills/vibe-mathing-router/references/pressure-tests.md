# Pressure Tests

## 混合请求不得全开

- Scenario：用户同时给出论文链接、公式和“证明一下”。
- Expected trigger：router。
- Tempting wrong behavior：同时启动检索、写作、计算和证明。
- Correct behavior：识别第一个未满足前置，只选择一个 owner。
- Pass：输出恰好一个主 skill 和一个停止条件。
