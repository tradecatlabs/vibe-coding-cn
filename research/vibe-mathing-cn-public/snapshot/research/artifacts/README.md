# 可信证据产物

本目录只保存由注册 verifier 产生、可现场重算摘要的输出与回执。Result 的 `locator` 必须指向本目录内的回执；回执再绑定底层输出。路径逃逸与 symlink 一律拒绝。

真实运行产物按 `outputs/<run-id>/` 保存，回执按 `receipts/<result-id>/` 保存。大体积或含隐私材料不得进入本目录。
