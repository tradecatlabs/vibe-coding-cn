# Telegram 生态开发资源索引

## 官方文档

### Bot API
**主文档:** https://core.telegram.org/bots/api  
**描述:** Telegram Bot API 完整参考文档

**核心功能：**
- 消息发送和接收
- 媒体文件处理
- 内联模式
- 支付集成
- Webhook 配置
- 游戏和投票

### Mini Apps (Web Apps)
**主文档:** https://core.telegram.org/bots/webapps  
**完整平台:** https://docs.telegram-mini-apps.com  
**描述:** Telegram 小程序开发文档

**核心功能：**
- WebApp API
- 主题和 UI 控件
- 存储（Cloud/Device/Secure）
- 生物识别认证
- 位置和传感器
- 支付集成

### Telegram API & MTProto
**主文档:** https://core.telegram.org  
**描述:** 完整的 Telegram 协议和客户端开发

**核心功能：**
- MTProto 协议
- TDLib 客户端库
- 认证和加密
- 文件操作
- Secret Chats

## 官方 GitHub 仓库

### Bot API 服务器
**仓库:** https://github.com/tdlib/telegram-bot-api  
**描述:** Telegram Bot API 服务器实现  
**特点:**
- 本地模式部署
- 支持大文件（最高 2000 MB）
- C++ 实现
- TDLib 基础

### Android 客户端
**仓库:** https://github.com/DrKLO/Telegram  
**描述:** 官方 Android 客户端源代码  
**特点:**
- 完整的 Android 实现
- Material Design
- 可自定义编译

### Desktop 客户端
**仓库:** https://github.com/telegramdesktop/tdesktop  
**描述:** 官方桌面客户端 (Windows, macOS, Linux)  
**特点:**
- Qt/C++ 实现
- 跨平台支持
- 完整功能

### 官方组织
**组织页面:** https://github.com/orgs/TelegramOfficial/repositories  
**包含:**
- Beta 版本
- 支持工具
- 示例代码

## API 方法分类

### 更新管理
- `getUpdates` - 长轮询
- `setWebhook` - 设置 Webhook
- `deleteWebhook` - 删除 Webhook  
- `getWebhookInfo` - Webhook 信息

### 消息操作
**发送消息：**
- `sendMessage` - 文本消息
- `sendPhoto` - 图片
- `sendVideo` - 视频
- `sendDocument` - 文档
- `sendAudio` - 音频
- `sendVoice` - 语音
- `sendLocation` - 位置
- `sendVenue` - 地点
- `sendContact` - 联系人
- `sendPoll` - 投票
- `sendDice` - 骰子/飞镖

**编辑消息：**
- `editMessageText` - 编辑文本
- `editMessageCaption` - 编辑标题
- `editMessageMedia` - 编辑媒体
- `editMessageReplyMarkup` - 编辑键盘
- `deleteMessage` - 删除消息

**其他操作：**
- `forwardMessage` - 转发消息
- `copyMessage` - 复制消息
- `sendChatAction` - 发送动作（输入中...）

### 文件操作
- `getFile` - 获取文件信息
- 文件下载 URL: `https://api.telegram.org/file/bot<token>/<file_path>`
- 文件上传：支持 multipart/form-data
- 最大文件：50 MB (标准), 2000 MB (本地 Bot API)

### 内联模式
- `answerInlineQuery` - 响应内联查询
- 结果类型：article, photo, gif, video, audio, voice, document, location, venue, contact, game, sticker

### 回调查询
- `answerCallbackQuery` - 响应按钮点击
- 可显示通知或警告

### 支付
- `sendInvoice` - 发送发票
- `answerPreCheckoutQuery` - 预结账
- `answerShippingQuery` - 配送查询
- 支持提供商：Stripe, Yandex.Money, Telegram Stars

### 游戏
- `sendGame` - 发送游戏
- `setGameScore` - 设置分数
- `getGameHighScores` - 获取排行榜

### 群组管理
- `kickChatMember` / `unbanChatMember` - 封禁/解封
- `restrictChatMember` - 限制权限
- `promoteChatMember` - 提升管理员
- `setChatTitle` / `setChatDescription` - 设置信息
- `setChatPhoto` - 设置头像
- `pinChatMessage` / `unpinChatMessage` - 置顶消息

## Mini Apps API 详解

### 初始化
```javascript
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();
```

### 主要对象
- **WebApp** - 主接口
- **MainButton** - 主按钮
- **SecondaryButton** - 次要按钮
- **BackButton** - 返回按钮
- **SettingsButton** - 设置按钮
- **HapticFeedback** - 触觉反馈
- **CloudStorage** - 云存储
- **BiometricManager** - 生物识别
- **LocationManager** - 位置服务
- **Accelerometer** - 加速度计
- **Gyroscope** - 陀螺仪
- **DeviceOrientation** - 设备方向

### 事件系统
40+ 事件包括：
- `themeChanged` - 主题改变
- `viewportChanged` - 视口改变
- `mainButtonClicked` - 主按钮点击
- `backButtonClicked` - 返回按钮点击
- `settingsButtonClicked` - 设置按钮点击
- `invoiceClosed` - 支付完成
- `popupClosed` - 弹窗关闭
- `qrTextReceived` - 扫码结果
- `clipboardTextReceived` - 剪贴板文本
- `writeAccessRequested` - 写入权限请求
- `contactRequested` - 联系人请求

### 主题参数
```javascript
tg.themeParams = {
    bg_color,           // 背景色
    text_color,         // 文本色
    hint_color,         // 提示色
    link_color,         // 链接色
    button_color,       // 按钮色
    button_text_color,  // 按钮文本色
    secondary_bg_color, // 次要背景色
    header_bg_color,    // 头部背景色
    accent_text_color,  // 强调文本色
    section_bg_color,   // 区块背景色
    section_header_text_color, // 区块头文本色
    subtitle_text_color,       // 副标题色
    destructive_text_color     // 危险操作色
}
```

## 开发工具

### @BotFather 命令
创建和管理 Bot 的核心工具：

**Bot 管理：**
- `/newbot` - 创建新 Bot
- `/mybots` - 管理我的 Bots
- `/deletebot` - 删除 Bot
- `/token` - 重新生成 token

**设置命令：**
- `/setname` - 设置名称
- `/setdescription` - 设置描述
- `/setabouttext` - 设置关于文本
- `/setuserpic` - 设置头像

**功能配置：**
- `/setcommands` - 设置命令列表
- `/setinline` - 启用内联模式
- `/setinlinefeedback` - 内联反馈
- `/setjoingroups` - 允许加入群组
- `/setprivacy` - 隐私模式

**支付和游戏：**
- `/setgamescores` - 游戏分数
- `/setpayments` - 配置支付

**Mini Apps：**
- `/newapp` - 创建 Mini App
- `/myapps` - 管理 Mini Apps
- `/setmenubutton` - 设置菜单按钮

### API ID 获取
访问 https://my.telegram.org
1. 登录账号
2. 进入 API development tools
3. 创建应用
4. 获取 API ID 和 API Hash

## 常用 Python 库

### python-telegram-bot
```bash
pip install python-telegram-bot
```

**特点：**
- 完整的 Bot API 包装
- 异步和同步支持
- 丰富的扩展
- 活跃维护

**基础示例：**
```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('你好！')

app = Application.builder().token("TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
```

### aiogram
```bash
pip install aiogram
```

**特点：**
- 纯异步
- 高性能
- FSM 状态机
- 中间件系统

### Telethon / Pyrogram
MTProto 客户端库：
```bash
pip install telethon
pip install pyrogram
```

**用途：**
- 自定义客户端
- 用户账号自动化
- 完整 Telegram 功能

## 常用 Node.js 库

### node-telegram-bot-api
```bash
npm install node-telegram-bot-api
```

### Telegraf
```bash
npm install telegraf
```

**特点：**
- 现代化
- 中间件架构
- TypeScript 支持

### grammY
```bash
npm install grammy
```

**特点：**
- 轻量级
- 类型安全
- 插件生态

## 部署选项

### Webhook 托管
**推荐平台：**
- Heroku
- AWS Lambda
- Google Cloud Functions
- Azure Functions
- Vercel
- Railway
- Render

**要求：**
- HTTPS 支持
- 公网可访问
- 支持的端口：443, 80, 88, 8443

### 长轮询托管
**推荐平台：**
- VPS (Vultr, DigitalOcean, Linode)
- Raspberry Pi
- 本地服务器

**优点：**
- 无需 HTTPS
- 简单配置
- 适合开发测试

## 安全最佳实践

1. **Token 安全**
   - 不要提交到 Git
   - 使用环境变量
   - 定期轮换

2. **数据验证**
   - 验证 initData
   - 服务器端验证
   - 不信任客户端

3. **权限控制**
   - 检查用户权限
   - 管理员验证
   - 群组权限

4. **速率限制**
   - 实现请求限制
   - 防止滥用
   - 监控异常

## 调试技巧

### Bot 调试
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Mini App 调试
```javascript
// 开启调试模式
tg.showAlert(JSON.stringify(tg.initDataUnsafe, null, 2));

// 控制台日志
console.log('WebApp version:', tg.version);
console.log('Platform:', tg.platform);
console.log('Theme:', tg.colorScheme);
```

### Webhook 测试
使用 ngrok 本地测试：
```bash
ngrok http 5000
# 将生成的 https URL 设置为 webhook
```

## 社区资源

- **Telegram 开发者群组**: @BotDevelopers
- **Telegram API 讨论**: @TelegramBots
- **Mini Apps 讨论**: @WebAppChat

## 更新日志

**最新功能：**
- Paid Media (付费媒体)
- Checklist Tasks (检查列表任务)
- Gift Conversion (礼物转换)
- Business Features (商业功能)
- Poll 选项增加到 12 个
- Story 发布和编辑

---

## 完整实现模板 (新增)

### Telegram Bot 按钮和键盘实现指南
**文件:** `Telegram_Bot_按钮和键盘实现模板.md`
**行数:** 404 行
**大小:** 12 KB
**语言:** 中文

精简实用的 Telegram Bot 交互式功能实现指南：

**核心内容：**
- 三种按钮类型详解（Inline/Reply/Command Menu）
- python-telegram-bot 和 Telethon 双实现对比
- 完整的代码示例（即拿即用）
- 项目结构和模块化设计
- Handler 优先级和事件处理
- 生产环境部署方案
- 安全和错误处理最佳实践

**特色：**
- 核心代码精简，去除冗余示例
- 聚焦常用场景和实用技巧
- 完整的快速参考表

---

### 动态视图对齐 - 数据展示指南
**文件:** `动态视图对齐实现文档.md`
**行数:** 407 行
**大小:** 12 KB
**语言:** 中文

专业的等宽字体数据对齐和格式化方案：

**核心功能：**
- 智能动态视图对齐算法（三步法）
- 自动计算列宽，无需硬编码
- 智能对齐规则（文本左，数字右）
- 完整的格式化系统：
  - 交易量智能缩写（B/M/K）
  - 价格智能精度（自适应小数位）
  - 涨跌幅格式化（+/- 符号）
  - 资金流向智能显示

**应用场景：**
- 排行榜、数据表格、实时行情
- 任何需要专业数据展示的 Telegram Bot

**技术特点：**
- O(n×m) 线性复杂度，高效实用
- 1000 行数据处理仅需 5-10ms
- 支持中文字符宽度扩展

**视觉效果示例：**
```
1.   BTC      $1.23B    $45,000   +5.23%
2.   ETH    $890.5M     $2,500   +3.12%
3.   SOL    $567.8M       $101   +8.45%
```

---

**这些模板提供了从基础到生产级别的完整 Telegram Bot 开发解决方案！**
