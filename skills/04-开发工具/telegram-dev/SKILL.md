---
name: telegram-dev
description: Telegram 生态开发全栈指南 - 涵盖 Bot API、Mini Apps (Web Apps)、MTProto 客户端开发。包括消息处理、支付、内联模式、Webhook、认证、存储、传感器 API 等完整开发资源。
---

# Telegram 生态开发技能

全面的 Telegram 开发指南，涵盖 Bot 开发、Mini Apps (Web Apps)、客户端开发的完整技术栈。

## 何时使用此技能

当需要以下帮助时使用此技能：
- 开发 Telegram Bot（消息机器人）
- 创建 Telegram Mini Apps（小程序）
- 构建自定义 Telegram 客户端
- 集成 Telegram 支付和业务功能
- 实现 Webhook 和长轮询
- 使用 Telegram 认证和存储
- 处理消息、媒体和文件
- 实现内联模式和键盘

## Telegram 开发生态概览

### 三大核心 API

1. **Bot API** - 创建机器人程序
   - HTTP 接口，简单易用
   - 自动处理加密和通信
   - 适合：聊天机器人、自动化工具

2. **Mini Apps API** (Web Apps) - 创建 Web 应用
   - JavaScript 接口
   - 在 Telegram 内运行
   - 适合：小程序、游戏、电商

3. **Telegram API & TDLib** - 创建客户端
   - 完整的 Telegram 协议实现
   - 支持所有平台
   - 适合：自定义客户端、企业应用

## Bot API 开发

### 快速开始

**API 端点：**
```
https://api.telegram.org/bot<TOKEN>/METHOD_NAME
```

**获取 Bot Token：**
1. 与 @BotFather 对话
2. 发送 `/newbot`
3. 按提示设置名称
4. 获取 token

**第一个 Bot (Python)：**
```python
import requests

BOT_TOKEN = "your_bot_token_here"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 发送消息
def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    return requests.post(url, json=data)

# 获取更新（长轮询）
def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"offset": offset, "timeout": 30}
    return requests.get(url, params=params).json()

# 主循环
offset = None
while True:
    updates = get_updates(offset)
    for update in updates.get("result", []):
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        
        # 回复消息
        send_message(chat_id, f"你说了：{text}")
        
        offset = update["update_id"] + 1
```

### 核心 API 方法

**更新管理：**
- `getUpdates` - 长轮询获取更新
- `setWebhook` - 设置 Webhook
- `deleteWebhook` - 删除 Webhook
- `getWebhookInfo` - 查询 Webhook 状态

**消息操作：**
- `sendMessage` - 发送文本消息
- `sendPhoto` / `sendVideo` / `sendDocument` - 发送媒体
- `sendAudio` / `sendVoice` - 发送音频
- `sendLocation` / `sendVenue` - 发送位置
- `editMessageText` - 编辑消息
- `deleteMessage` - 删除消息
- `forwardMessage` / `copyMessage` - 转发/复制消息

**交互元素：**
- `sendPoll` - 发送投票（最多 12 个选项）
- 内联键盘 (InlineKeyboardMarkup)
- 回复键盘 (ReplyKeyboardMarkup)
- `answerCallbackQuery` - 响应回调查询

**文件操作：**
- `getFile` - 获取文件信息
- `downloadFile` - 下载文件
- 支持最大 2GB 文件（本地 Bot API 模式）

**支付功能：**
- `sendInvoice` - 发送发票
- `answerPreCheckoutQuery` - 处理支付
- Telegram Stars 支付（最高 10,000 Stars）

### Webhook 配置

**设置 Webhook：**
```python
import requests

BOT_TOKEN = "your_token"
WEBHOOK_URL = "https://yourdomain.com/webhook"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": WEBHOOK_URL}
)
```

**Flask Webhook 示例：**
```python
from flask import Flask, request
import requests

app = Flask(__name__)
BOT_TOKEN = "your_token"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    chat_id = update["message"]["chat"]["id"]
    text = update["message"]["text"]
    
    # 发送回复
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": f"收到: {text}"}
    )
    
    return "OK"

if __name__ == '__main__':
    app.run(port=5000)
```

**Webhook 要求：**
- 必须使用 HTTPS
- 支持 TLS 1.2+
- 端口：443, 80, 88, 8443
- 公共可访问的 URL

### 内联键盘

**创建内联键盘：**
```python
def send_inline_keyboard(chat_id):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "按钮 1", "callback_data": "btn1"},
                {"text": "按钮 2", "callback_data": "btn2"}
            ],
            [
                {"text": "打开链接", "url": "https://example.com"}
            ]
        ]
    }
    
    requests.post(
        f"{API_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": "选择一个选项：",
            "reply_markup": keyboard
        }
    )
```

**处理回调：**
```python
def handle_callback_query(callback_query):
    query_id = callback_query["id"]
    data = callback_query["data"]
    chat_id = callback_query["message"]["chat"]["id"]
    
    # 响应回调
    requests.post(
        f"{API_URL}/answerCallbackQuery",
        json={"callback_query_id": query_id, "text": f"你点击了 {data}"}
    )
    
    # 更新消息
    requests.post(
        f"{API_URL}/editMessageText",
        json={
            "chat_id": chat_id,
            "message_id": callback_query["message"]["message_id"],
            "text": f"你选择了：{data}"
        }
    )
```

### 内联模式

**配置内联模式：**
与 @BotFather 对话，发送 `/setinline`

**处理内联查询：**
```python
def handle_inline_query(inline_query):
    query_id = inline_query["id"]
    query_text = inline_query["query"]
    
    # 创建结果
    results = [
        {
            "type": "article",
            "id": "1",
            "title": "结果 1",
            "input_message_content": {
                "message_text": f"你搜索了：{query_text}"
            }
        }
    ]
    
    requests.post(
        f"{API_URL}/answerInlineQuery",
        json={"inline_query_id": query_id, "results": results}
    )
```

## Mini Apps (Web Apps) 开发

### 初始化 Mini App

**HTML 模板：**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <title>My Mini App</title>
</head>
<body>
    <h1>Telegram Mini App</h1>
    <button id="mainBtn">主按钮</button>
    
    <script>
        // 获取 Telegram WebApp 对象
        const tg = window.Telegram.WebApp;
        
        // 通知 Telegram 应用已准备好
        tg.ready();
        
        // 展开到全屏
        tg.expand();
        
        // 显示用户信息
        const user = tg.initDataUnsafe?.user;
        if (user) {
            console.log("用户名:", user.first_name);
            console.log("用户ID:", user.id);
        }
        
        // 配置主按钮
        tg.MainButton.text = "提交";
        tg.MainButton.show();
        tg.MainButton.onClick(() => {
            // 发送数据到 Bot
            tg.sendData(JSON.stringify({action: "submit"}));
        });
        
        // 添加返回按钮
        tg.BackButton.show();
        tg.BackButton.onClick(() => {
            tg.close();
        });
    </script>
</body>
</html>
```

### Mini App 核心 API

**WebApp 对象主要属性：**
```javascript
// 初始化数据
tg.initData           // 原始初始化字符串
tg.initDataUnsafe     // 解析后的对象

// 用户和主题
tg.initDataUnsafe.user       // 用户信息
tg.themeParams                // 主题颜色
tg.colorScheme                // 'light' 或 'dark'

// 状态
tg.isExpanded         // 是否全屏
tg.isFullscreen       // 是否全屏
tg.viewportHeight     // 视口高度
tg.platform           // 平台类型

// 版本
tg.version            // WebApp 版本
```

**主要方法：**
```javascript
// 窗口控制
tg.ready()            // 标记应用准备就绪
tg.expand()           // 展开到全高度
tg.close()            // 关闭 Mini App
tg.requestFullscreen() // 请求全屏

// 数据发送
tg.sendData(data)     // 发送数据到 Bot

// 导航
tg.openLink(url)      // 打开外部链接
tg.openTelegramLink(url) // 打开 Telegram 链接

// 对话框
tg.showPopup(params, callback)  // 显示弹窗
tg.showAlert(message)           // 显示警告
tg.showConfirm(message)         // 显示确认

// 分享
tg.shareMessage(message)        // 分享消息
tg.shareUrl(url)                // 分享链接
```

### UI 控件

**主按钮 (MainButton)：**
```javascript
tg.MainButton.setText("点击我");
tg.MainButton.show();
tg.MainButton.enable();
tg.MainButton.showProgress();  // 显示加载
tg.MainButton.hideProgress();

tg.MainButton.onClick(() => {
    console.log("主按钮被点击");
});
```

**次要按钮 (SecondaryButton)：**
```javascript
tg.SecondaryButton.setText("取消");
tg.SecondaryButton.show();
tg.SecondaryButton.onClick(() => {
    tg.close();
});
```

**返回按钮 (BackButton)：**
```javascript
tg.BackButton.show();
tg.BackButton.onClick(() => {
    // 返回逻辑
});
```

**触觉反馈：**
```javascript
tg.HapticFeedback.impactOccurred('light');  // light, medium, heavy
tg.HapticFeedback.notificationOccurred('success'); // success, warning, error
tg.HapticFeedback.selectionChanged();
```

### 存储 API

**云存储：**
```javascript
// 保存数据
tg.CloudStorage.setItem('key', 'value', (error, success) => {
    if (success) console.log('保存成功');
});

// 获取数据
tg.CloudStorage.getItem('key', (error, value) => {
    console.log('值:', value);
});

// 删除数据
tg.CloudStorage.removeItem('key');

// 获取所有键
tg.CloudStorage.getKeys((error, keys) => {
    console.log('所有键:', keys);
});
```

**本地存储：**
```javascript
// 普通本地存储
localStorage.setItem('key', 'value');
const value = localStorage.getItem('key');

// 安全存储（需要生物识别）
tg.SecureStorage.setItem('secret', 'value', callback);
tg.SecureStorage.getItem('secret', callback);
```

### 生物识别认证

```javascript
const bioManager = tg.BiometricManager;

// 初始化
bioManager.init(() => {
    if (bioManager.isInited) {
        console.log('支持的类型:', bioManager.biometricType);
        // 'finger', 'face', 'unknown'
        
        if (bioManager.isAccessGranted) {
            // 已授权，可以使用
        } else {
            // 请求授权
            bioManager.requestAccess({reason: '需要验证身份'}, (success) => {
                if (success) {
                    console.log('授权成功');
                }
            });
        }
    }
});

// 执行认证
bioManager.authenticate({reason: '确认操作'}, (success, token) => {
    if (success) {
        console.log('认证成功，token:', token);
    }
});
```

### 位置和传感器

**获取位置：**
```javascript
tg.LocationManager.init(() => {
    if (tg.LocationManager.isInited) {
        tg.LocationManager.getLocation((location) => {
            console.log('纬度:', location.latitude);
            console.log('经度:', location.longitude);
        });
    }
});
```

**加速度计：**
```javascript
tg.Accelerometer.start({refresh_rate: 100}, (started) => {
    if (started) {
        tg.Accelerometer.onEvent((event) => {
            console.log('加速度:', event.x, event.y, event.z);
        });
    }
});

// 停止
tg.Accelerometer.stop();
```

**陀螺仪：**
```javascript
tg.Gyroscope.start({refresh_rate: 100}, callback);
tg.Gyroscope.onEvent((event) => {
    console.log('旋转速度:', event.x, event.y, event.z);
});
```

**设备方向：**
```javascript
tg.DeviceOrientation.start({refresh_rate: 100}, callback);
tg.DeviceOrientation.onEvent((event) => {
    console.log('方向:', event.absolute, event.alpha, event.beta, event.gamma);
});
```

### 支付集成

**发起支付 (Telegram Stars)：**
```javascript
tg.openInvoice('https://t.me/$invoice_link', (status) => {
    if (status === 'paid') {
        console.log('支付成功');
    } else if (status === 'cancelled') {
        console.log('支付取消');
    } else if (status === 'failed') {
        console.log('支付失败');
    }
});
```

### 数据验证

**服务器端验证 initData (Python)：**
```python
import hmac
import hashlib
from urllib.parse import parse_qs

def validate_init_data(init_data, bot_token):
    # 解析数据
    parsed = parse_qs(init_data)
    received_hash = parsed.get('hash', [''])[0]
    
    # 移除 hash
    data_check_arr = []
    for key, value in parsed.items():
        if key != 'hash':
            data_check_arr.append(f"{key}={value[0]}")
    
    # 排序
    data_check_arr.sort()
    data_check_string = '\n'.join(data_check_arr)
    
    # 计算密钥
    secret_key = hmac.new(
        b"WebAppData",
        bot_token.encode(),
        hashlib.sha256
    ).digest()
    
    # 计算哈希
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return calculated_hash == received_hash
```

### 启动 Mini App

**从键盘按钮：**
```python
keyboard = {
    "keyboard": [[
        {
            "text": "打开应用",
            "web_app": {"url": "https://yourdomain.com/app"}
        }
    ]],
    "resize_keyboard": True
}

requests.post(
    f"{API_URL}/sendMessage",
    json={
        "chat_id": chat_id,
        "text": "点击按钮打开应用",
        "reply_markup": keyboard
    }
)
```

**从内联按钮：**
```python
keyboard = {
    "inline_keyboard": [[
        {
            "text": "启动应用",
            "web_app": {"url": "https://yourdomain.com/app"}
        }
    ]]
}
```

**从菜单按钮：**
与 @BotFather 对话：
```
/setmenubutton
→ 选择你的 Bot
→ 提供 URL: https://yourdomain.com/app
```

## 客户端开发 (TDLib)

### 使用 TDLib

**Python 示例 (python-telegram)：**
```python
from telegram.client import Telegram

tg = Telegram(
    api_id='your_api_id',
    api_hash='your_api_hash',
    phone='+1234567890',
    database_encryption_key='changeme1234',
)

tg.login()

# 发送消息
result = tg.send_message(
    chat_id=123456789,
    text='Hello from TDLib!'
)

# 获取聊天列表
result = tg.get_chats()
result.wait()
chats = result.update

print(chats)

tg.stop()
```

### MTProto 协议

**特点：**
- 端到端加密
- 高性能
- 支持所有 Telegram 功能
- 需要 API ID/Hash（从 https://my.telegram.org 获取）

## 最佳实践

### Bot 开发

1. **错误处理**
   ```python
   try:
       response = requests.post(url, json=data, timeout=10)
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       print(f"请求失败: {e}")
   ```

2. **速率限制**
   - 群组消息：最多 20 条/分钟
   - 私聊消息：最多 30 条/秒
   - 全局限制：避免过于频繁

3. **使用 Webhook 而非长轮询**
   - 更高效
   - 更低延迟
   - 更好的可扩展性

4. **数据验证**
   - 始终验证 initData
   - 不要信任客户端数据
   - 服务器端验证所有操作

### Mini Apps 开发

1. **响应式设计**
   ```javascript
   // 监听主题变化
   tg.onEvent('themeChanged', () => {
       document.body.style.backgroundColor = tg.themeParams.bg_color;
   });
   
   // 监听视口变化
   tg.onEvent('viewportChanged', () => {
       console.log('新高度:', tg.viewportHeight);
   });
   ```

2. **性能优化**
   - 最小化 JavaScript 包大小
   - 使用懒加载
   - 优化图片和资源

3. **用户体验**
   - 适配深色/浅色主题
   - 使用原生 UI 控件（MainButton 等）
   - 提供触觉反馈
   - 快速响应用户操作

4. **安全考虑**
   - HTTPS 强制
   - 验证 initData
   - 不在客户端存储敏感信息
   - 使用 SecureStorage 存储密钥

## 常用库和工具

### Python
- `python-telegram-bot` - 功能强大的 Bot 框架
- `aiogram` - 异步 Bot 框架
- `telethon` / `pyrogram` - MTProto 客户端

### Node.js
- `node-telegram-bot-api` - Bot API 包装器
- `telegraf` - 现代 Bot 框架
- `grammy` - 轻量级框架

### 其他语言
- PHP: `telegram-bot-sdk`
- Go: `telegram-bot-api`
- Java: `TelegramBots`
- C#: `Telegram.Bot`

## 参考资源

### 官方文档
- Bot API: https://core.telegram.org/bots/api
- Mini Apps: https://core.telegram.org/bots/webapps
- Mini Apps Platform: https://docs.telegram-mini-apps.com
- Telegram API: https://core.telegram.org

### GitHub 仓库
- Bot API 服务器: https://github.com/tdlib/telegram-bot-api
- Android 客户端: https://github.com/DrKLO/Telegram
- Desktop 客户端: https://github.com/telegramdesktop/tdesktop
- 官方组织: https://github.com/orgs/TelegramOfficial/repositories

### 工具
- @BotFather - 创建和管理 Bot
- https://my.telegram.org - 获取 API ID/Hash
- Telegram Web App 测试环境

## 参考文件

此技能包含详细的 Telegram 开发资源索引和完整实现模板：

- **index.md** - 完整的资源链接和快速导航
- **Telegram_Bot_按钮和键盘实现模板.md** - 交互式按钮和键盘实现指南（404 行，12 KB）
  - 三种按钮类型详解（Inline/Reply/Command Menu）
  - python-telegram-bot 和 Telethon 双实现对比
  - 完整的即用代码示例和项目结构
  - Handler 系统、错误处理和部署方案
- **动态视图对齐实现文档.md** - Telegram 数据展示指南（407 行，12 KB）
  - 智能动态对齐算法（三步法，O(n×m) 复杂度）
  - 等宽字体环境的完美对齐方案
  - 智能数值格式化系统（B/M/K 自动缩写）
  - 排行榜和数据表格专业展示

这些精简指南提供了核心的 Telegram Bot 开发解决方案：
- 按钮和键盘交互的所有实现方式
- 消息和数据的专业格式化展示
- 实用的最佳实践和快速参考

---

**使用此技能掌握 Telegram 生态的全栈开发！**
