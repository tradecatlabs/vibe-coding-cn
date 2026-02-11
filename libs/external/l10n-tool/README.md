# l10n-tool

轻量级多语言翻译脚本，定位：先用机器翻译批量落地，再由 AI/人工逐行润色。

## 特性
- 保护 Markdown 代码块，不误翻译代码
- 命令行一条跑完，便于批处理
- 依赖轻：`deep-translator`（封装 Google 翻译）

## 安装
```bash
pip install -r requirements.txt
```

## 使用示例
```bash
# 将中文 README 翻译到英文
python translate.py --input ../../README.md --output ../../README.md --src-lang zh --tgt-lang en --overwrite

# 批量翻译 prompts，可在外部脚本中循环调用
```

## 建议流程（快 ⇒ 精）
1) 机器翻译初稿：用本工具覆盖生成各语言版本。
2) AI 校润：对关键文档/提示词逐行复核，重点检查术语一致性与人称语气。
3) 人工抽检：挑核心页面人工对比源文，修正 AI 可能的误译。

## 语言代码参考
- 常用：zh, en, es, fr, de, ru, pt, ar, hi, ja, ko, he, it, tr, nl, pl, id, vi, th, fa, uk, bn, ta, ur, ms, sw, ha
- 更多代码可查 ISO 639-1。

## 注意
- 若需更高质量，可替换为官方 Google Cloud Translate / DeepL API，只需改写 `translate_blocks` 中的 translator 初始化逻辑。
- 如遇免费翻译频率限制，可分批或加重试/代理配置。
