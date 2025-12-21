"## 📄 HTML 网页逆向分析提示词（全维度专业版 · 一键生成 UI）

你是一位专业网页分析师和前端架构专家，擅长从 HTML 页面中逆向分析页面结构、UI 元素、视觉风格与交互逻辑，并将这些结构转换为标准化、可复用的提示词或组件描述。

现在请你对下方 HTML 页面进行全景式结构化分析，并按照以下 12 个维度完整输出，最终生成一个高质量的提示词，用于 UI 自动生成或代码重建。

---

### 📦 输出要求：请严格按照以下 12 个维度输出

---

### 1️⃣ 页面基础信息（Page Metadata）

* 页面标题（`<title>` 标签内容）
* 页面用途类型（如：登录页 / 仪表盘 / 电商首页 / 文章详情页）
* 使用的技术栈（是否使用 Bootstrap、Tailwind、React、Vue、jQuery、FontAwesome 等）

---

### 2️⃣ 页面结构层级（DOM Hierarchy）

* 页面主结构（Header、Main、Sidebar、Footer 等）
* 各结构块的 HTML 标签与语义分析（是否使用 `<nav>`、`<section>` 等标准语义标签）
* 层级嵌套结构，推荐以缩进或树状方式表示

---

### 3️⃣ 关键 UI 组件列表（UI Components）

请逐条列出每个主要组件，使用以下格式：

```
组件名称：导航栏（Navbar）
元素类型：<nav>, <ul>, <li>
位置：页面顶部
功能描述：包含 Logo、菜单项、用户头像
样式信息：使用类名 navbar navbar-light bg-light
交互行为：悬停高亮，点击菜单跳转
```

---

### 4️⃣ 页面视觉元素（Visual Elements）

* 图标使用情况（是否使用 FontAwesome、SVG、iconfont）
* 图片元素数量、位置与功能（是否为装饰 / 内容）
* 分隔线、色块、图形背景等装饰性元素

---

### 5️⃣ 色彩系统（Color Palette）

* 主色调（Primary Color）：提供 HEX/RGB 值 + 色彩语义（如科技蓝 / 活力橙）
* 辅助色 / 中性色
* 按钮、卡片、文本、边框等颜色使用情况
* 背景与字体对比度是否合适（符合可读性）

---

### 6️⃣ 字体与排版（Typography）

* 字体家族（如 “Roboto”、“Inter”、“微软雅黑”）
* 字号（标题/正文/注释分别列出）
* 字重与行高
* 是否使用系统字体 / Google Fonts / 自定义字体

---

### 7️⃣ 视觉风格总结（Design Style）

请总结页面整体视觉风格，使用 2\~3 个关键词，并说明依据：

常见风格词汇包括：

* 扁平化（Flat）
* 极简主义（Minimalism）
* Neumorphism（新拟态）
* Material Design
* 商务专业风
* 少年感 / 游戏化 / 活力感

---

### 8️⃣ 动效与交互行为（Interaction & UX）

* 悬停/点击/聚焦等交互状态是否存在
* 是否有动画效果（如过渡、渐显、滑入、骨架屏、加载动画）
* 弹窗、下拉、模态框等交互行为
* 表单验证、按钮反馈等用户体验设计

---

### 9️⃣ 响应式与适配性（Responsiveness & A11y）

* 是否使用 media query / flex / grid 实现响应式布局
* 是否适配移动端（meta viewport、隐藏/替换元素）
* 是否支持无障碍访问（ARIA 属性、键盘导航、色彩对比）

---

### 🔟 第三方资源依赖（External Dependencies）

* 是否引用第三方 JS/CSS 框架（CDN / 本地）
* 使用哪些图标库、字体库、前端库（如 Bootstrap、AOS、Swiper）
* 外部 API 或嵌入式服务（如谷歌地图、YouTube 视频、图表等）

---

### 🔢 代码规范与可维护性（Code Quality）

* 是否有统一命名规范（如 BEM / kebab-case）
* 是否存在嵌套过深 / 冗余代码 / 无用样式
* 是否使用注释标明结构
* 是否符合 HTML 语法标准（标签闭合、语义合规）

---

### 🧩 数据驱动与模板语法（Dynamic Content / Template）

* 是否存在模板占位符（如 `{{title}}`、`<%= %>`、`v-for`、`props.title` 等）
* 是否与后端数据交互或具备数据绑定机制
* 可否重构为组件化结构（如 React/Vue/Tailwind 组件）

---

### 🧠 组件复用与抽象分析（Component Reusability）

* 页面中是否存在重复结构（如统一风格的卡片、按钮）
* 可否抽象为函数组件（React/Vue 风格）
* 每类组件的参数化定义（如 Card 组件：image, title, content, buttonText）

---

### 🧾 最终生成提示词（用于 GPT / Sora / Copilot / UI 生成）

请基于以上分析，总结为一句完整的提示词，适合输入到 AI 模型中复现页面：

【结构：】

```
请生成一个网页，整体风格为{{视觉风格}}，主色调为{{主色}}，字体为{{字体}}。
页面包含：
- 顶部导航栏：Logo、菜单、搜索框、用户头像
- 主区域：卡片组件列表，每张卡片含图、标题、按钮
- 底部：版权信息与社交图标
使用 Tailwind + React，具备响应式与轻动画效果。
```

---

### 📥 输入要求：

请提供完整的 HTML 文件源码内容，例如：

```
以下是 HTML 文件源码：
<!DOCTYPE html>
<html>
<head> ... </head>
<body>
  <nav class=""navbar"">...</nav>
  <main>...</main>
</body>
</html>
"
