# Lilian Weng Harness RSI 提纲摘记

来源：[Harness Engineering for Self-Improvement](https://lilianweng.github.io/posts/2026-07-04-harness/)

当 Lilian 发博客，所有的人都放下手上的活，先读为快。

AI未来将进入“递归自我改进”（Recursive Self-improvement， RSI）阶段。Lilian博客讲的就是这个现在很热的话题RSI。

在博客中Lilian谈到：AI 自我改进不一定从模型直接改自己权重开始。更现实的近期路径，是先优化harness：它决定模型如何规划、调用工具、管理上下文、保存状态、评估结果、启动子任务，并在执行中不断迭代。她把 harness 定义为围绕基础模型的一整套执行系统，而不是简单的 prompt、memory、tools 拼装。

文章还拆分了几个现在已经比较明确的 harness 设计模式：
模式一：工作流自动化，让模型进入“计划、执行、观察/测试、改进、再执行”的循环。
模式二：把文件系统当作持久记忆，不把所有日志和状态都塞进上下文，而是把实验记录、代码 diff、错误轨迹、论文摘要等落到文件里。
模式三： 子代理和后台任务，让主代理可以并行探索、运行实验、监控日志，并把结果重新合并回来。

# 面向自我改进的 Harness 工程

日期：2026 年 7 月 4 日  
预计阅读时间：28 分钟  
作者：Lilian Weng

## 目录

## Harness 设计模式

### 模式 1：工作流自动化

### 模式 2：将文件系统作为持久记忆

### 模式 3：子代理与后端任务

### 案例研究：Coding Agent Harness

### Harness 层 vs 核心智能？

## Harness 优化

### 上下文工程

### 工作流设计

### 自我改进的 Harness

### 进化搜索

### 与模型权重的联合优化

## 未来挑战

## 引用

## 附录：一些有用的基准测试

## 参考文献
