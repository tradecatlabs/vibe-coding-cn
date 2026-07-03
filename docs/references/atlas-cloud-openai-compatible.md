# Atlas Cloud OpenAI-compatible 接入边界

## 字多不看

- Atlas Cloud 的 LLM endpoint 兼容 OpenAI Chat Completions，base URL 是 `https://api.atlascloud.ai/v1`。
- 图像、视频生成走独立的 Media API，base URL 是 `https://api.atlascloud.ai/api/v1`，通常是提交任务再轮询结果。
- 不要把真实 `ATLASCLOUD_API_KEY` 写进仓库；在本地 shell、CI secret 或部署平台 secret 里注入。
- 不要在示例里写死模型 ID、价格或参数枚举；先查询模型列表和目标模型 schema，再填入当前可用值。
- Codex CLI 里 `wire_api = "responses"` 的 provider 配置不是 Chat Completions 配置，不能直接把 Atlas Cloud LLM endpoint 当成 Responses provider 替换，除非客户端明确支持 OpenAI-compatible Chat Completions provider。

## 适用场景

适合接入 Atlas Cloud 的位置：

- 已经使用 OpenAI SDK、LangChain、LlamaIndex、LiteLLM 或其他 OpenAI-compatible adapter 的应用。
- 允许配置 `base_url` / `baseURL`、`api_key` 和 `model` 的 agent、脚本或服务。
- 需要把图像、视频生成作为异步任务接入的创作工具、工作流或后台服务。

不建议硬接的场景：

- 客户端只支持 Responses API 或其他非 Chat Completions wire protocol。
- 项目没有外部模型调用边界，只是 prompt、规范或纯本地工具。
- 需要在文档里给出具体模型 ID、参数或价格，但还没有查询当前模型列表和 schema。

## LLM Chat Completions

推荐只把三类配置暴露给用户：

| 配置 | 建议值 |
|:---|:---|
| API key | `ATLASCLOUD_API_KEY` |
| Base URL | `https://api.atlascloud.ai/v1` |
| Model | 先查询当前模型列表，再填入已确认可用的模型 ID |

模型列表可以从公开 endpoint 查询：

```bash
curl -s https://api.atlascloud.ai/api/v1/models
```

实际接入前检查两件事：

1. 目标模型在当前模型列表中可见，并且是面向控制台或公开调用的模型。
2. 如果要写图像或视频请求体，先查看目标模型 schema，只发送 schema 中存在的字段。

### Python

```python
import os

from openai import OpenAI


client = OpenAI(
    api_key=os.environ["ATLASCLOUD_API_KEY"],
    base_url="https://api.atlascloud.ai/v1",
)

response = client.chat.completions.create(
    model=os.environ["ATLASCLOUD_MODEL"],
    messages=[
        {"role": "system", "content": "You are a concise engineering assistant."},
        {"role": "user", "content": "Summarize the release checklist."},
    ],
)

print(response.choices[0].message.content)
```

### TypeScript

```typescript
import OpenAI from "openai";

const apiKey = process.env.ATLASCLOUD_API_KEY;
const model = process.env.ATLASCLOUD_MODEL;

if (!apiKey || !model) {
  throw new Error("Set ATLASCLOUD_API_KEY and ATLASCLOUD_MODEL before running this script.");
}

const client = new OpenAI({
  apiKey,
  baseURL: "https://api.atlascloud.ai/v1",
});

const response = await client.chat.completions.create({
  model,
  messages: [
    { role: "system", content: "You are a concise engineering assistant." },
    { role: "user", content: "Summarize the release checklist." },
  ],
});

console.log(response.choices[0]?.message?.content);
```

## Media API

图像和视频生成不要复用 Chat Completions endpoint。它们是独立的异步任务接口：

| 能力 | Endpoint |
|:---|:---|
| 提交图像任务 | `POST https://api.atlascloud.ai/api/v1/model/generateImage` |
| 提交视频任务 | `POST https://api.atlascloud.ai/api/v1/model/generateVideo` |
| 查询任务结果 | `GET https://api.atlascloud.ai/api/v1/model/prediction/{prediction_id}` |

Media API 的稳妥接入原则：

- 先从模型列表选择当前可用模型，再按模型 schema 构造请求体。
- 对 `GET` 轮询可以做有限重试；对提交任务的 `POST` 不要自动无脑重试，避免重复创建计费任务。
- 轮询间隔用固定下限加最大次数，例如每 3 秒查询一次，超过业务允许时间后返回可恢复错误。
- 把任务 ID、状态和错误信息记录下来，方便用户继续查询或重试。

## Codex CLI 配置边界

本仓库的 Codex 配置样例如果使用 `wire_api = "responses"`，说明客户端在走 Responses API 语义。Atlas Cloud 的 LLM endpoint 是 OpenAI-compatible Chat Completions：

```toml
# 仅当客户端明确支持 Chat Completions provider 时才使用类似配置。
# 不要把这段直接替换到只支持 Responses API 的 Codex provider 中。
[model_providers.atlascloud]
name = "Atlas Cloud"
base_url = "https://api.atlascloud.ai/v1"
env_key = "ATLASCLOUD_API_KEY"
```

如果当前工具只支持 Responses API，保守做法是保持原 provider 配置不变，把 Atlas Cloud 放到单独的 SDK、agent 或 media workflow 代码路径中。

## 接入前检查清单

- [ ] `ATLASCLOUD_API_KEY` 只来自环境变量或 secret store。
- [ ] `ATLASCLOUD_MODEL` 来自当前模型列表，不在教程里写死。
- [ ] 图像、视频请求体来自目标模型 schema，不猜参数名。
- [ ] Chat Completions 与 Media API 的 base URL 分开配置。
- [ ] `POST` 生成任务没有自动无限重试。
- [ ] 只在客户端支持 Chat Completions provider 时配置 Atlas Cloud LLM endpoint。
