---
name: "📖 文档改进"
description: "提出关于文档的改进建议或报告错误。"
title: "docs: "
labels: ["documentation"]
body:
  - type: markdown
    attributes:
      value: |
        感谢您花时间来改进我们的文档！

  - type: textarea
    id: problem-description
    attributes:
      label: "您想改进或报告的问题是什么？"
      description: "请清晰、简洁地描述问题。例如：某个链接失效、某个步骤不清晰、某个概念解释有误等。"
    validations:
      required: true

  - type: textarea
    id: suggested-solution
    attributes:
      label: "您的建议方案"
      description: "您认为应该如何修正？请提供具体的修改建议。"
    validations:
      required: true

  - type: dropdown
    id: document-scope
    attributes:
      label: "涉及的文档范围"
      description: "这个问题主要影响哪个部分的文档？"
      multiple: true
      options:
        - "README 主页"
        - "Wiki"
        - "教程与指南"
        - "方法论与原则"
        - "其他"
    validations:
      required: true
