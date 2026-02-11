# 人生K线 LLM 用户提示词模板（完整原文）

本文件摘自 `libs/external/web/lifekline-main/services/geminiService.ts` 中 `userPrompt` 拼装逻辑，已替换为模板变量，便于直接复用。

```
请根据以下**已经排好的**八字四柱和**指定的大运信息**进行分析。
    
【基本信息】
性别：${genderStr}
姓名：${input.name || "未提供"}
出生年份：${input.birthYear}年 (阳历)
    
【八字四柱】
年柱：${input.yearPillar} (天干属性：${yearStemPolarity === 'YANG' ? '阳' : '阴'})
月柱：${input.monthPillar}
日柱：${input.dayPillar}
时柱：${input.hourPillar}
    
【大运核心参数】
1. 起运年龄：${input.startAge} 岁 (虚岁)。
2. 第一步大运：${input.firstDaYun}。
3. **排序方向**：${daYunDirectionStr}。
    
【必须执行的算法 - 大运序列生成】
请严格按照以下步骤生成数据：
    
1. **锁定第一步**：确认【${input.firstDaYun}】为第一步大运。
2. **计算序列**：根据六十甲子顺序和方向（${daYunDirectionStr}），推算出接下来的 9 步大运。
   ${directionExample}
3. **填充 JSON**：
   - Age 1 到 ${startAgeInt - 1}: daYun = "童限"
   - Age ${startAgeInt} 到 ${startAgeInt + 9}: daYun = [第1步大运: ${input.firstDaYun}]
   - Age ${startAgeInt + 10} 到 ${startAgeInt + 19}: daYun = [第2步大运]
   - Age ${startAgeInt + 20} 到 ${startAgeInt + 29}: daYun = [第3步大运]
   - ...以此类推直到 100 岁。
    
【特别警告】
- **daYun 字段**：必须填大运干支（10年一变），**绝对不要**填流年干支。
- **ganZhi 字段**：填入该年份的**流年干支**（每年一变，例如 2024=甲辰，2025=乙巳）。
    
任务：
1. 确认格局与喜忌。
2. 生成 **1-100 岁 (虚岁)** 的人生流年K线数据。
3. 在 `reason` 字段中提供流年详批。
4. 生成带评分的命理分析报告（包含性格分析、币圈交易分析、发展风水分析）。
    
请严格按照系统指令生成 JSON 数据。
```

# 使用说明
- 作为 `user` 消息传入 `/chat/completions`，与系统提示词配套使用。
- 变量含义：`genderStr` 由性别+乾坤文字组成；`startAgeInt` 为起运年龄整数；`directionExample` 随顺/逆行变化；其余变量直接取用户输入或排盘结果。
- 输出需为纯 JSON，`geminiService` 会自动剥离代码块并校验 `chartPoints`。

