# Context：按需参考资料

## 字多不看

这里放公开的规则、知识、文档、数据与参考材料；研究档案仅保留在既有本机副本，不随公开仓库分发。它们是工具箱的资料，不是默认全部注入的系统指令。
方法集中在功法，工具来源与重要性记录集中在法器；每个集合以原始`data.json`为唯一维护源，`README.md`提供导航，正文按天、地、玄、黄四阶拆分。

## 快速导航

| 对象 | 内容 |
|---|---|
| [功法](gongfa/README.md) | 分阶导航：[天](gongfa/tian.md)、[地](gongfa/di.md)、[玄](gongfa/xuan.md)、[黄](gongfa/huang.md)；原文归档见data.json |
| [法器](faqi/README.md) | 分阶导航：[天](faqi/tian.md)、[地](faqi/di.md)、[玄](faqi/xuan.md)、[黄](faqi/huang.md)；来源与边界见data.json |
| [从零开始](getting-started/README.md) | 提供可全文复制给网页版 AI 的 Pi CLI 安装配置提示词；逐步验收本机 Agent 能力，项目练习独立且可选 |
| [提示词](prompts/README.md) | 现有云端提示词索引 |
| [说明模板v1](tool-explanation-template-v1.md) | 功法、法器逐对象说明的活动模板；[历史v0](tool-explanation-template-v0.md) |
| [AI引用](ai-citation/README.md) | 摘要、FAQ与完整AI引用入口 |
| [机器索引](metadata/README.md) | 分类、术语和历史路径映射 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

- [使用方式](#使用方式)
  - [本地研究资料](#本地研究资料)
- [正文](#正文)
- [三个资源域](#三个资源域)
- [两个资料集合](#两个资料集合)
- [来源与信任边界](#来源与信任边界)

</details>

## 使用方式

先按任务选资料，再核对原文、来源、版本和适用条件；不把一次检索或阅读当成能力证明。
功法和法器的阅读视图分别用`make sync-gongfa-catalog`、`make sync-faqi-catalog`生成，不手改。

<a id="本地研究资料"></a>

### 本地研究资料

完整研究档案保留在已有本机副本的`.github/context/research/`，不会出现在公开仓库的新克隆中。已有克隆若仍跟踪该目录，更新到移除提交可能删除工作区副本；需要保留时，请先将目录安全移出仓库并核对副本。普通提交只移除GitHub当前文件树，不改写公开历史。

## 正文

### 三个资源域

- [Context](README.md)：[目录](./)、[维护规则](AGENTS.md)；只保存资料，不编排执行。
- [Skills](../skills/README.md)：[目录](../skills/)、[维护规则](../skills/AGENTS.md)；保存既有指令和流程。
- [Extensions](../extensions/README.md)：[目录](../extensions/)、[维护规则](../extensions/AGENTS.md)；保存既有程序、脚本和适配器。

### 两个资料集合

`gongfa/data.json`、`faqi/data.json`分别是本集合唯一维护源。历史文档身份、文件模式、原始字节、SHA、选择器和既有意见保留在`documents`中；文本用UTF-8，二进制用显式Base64。当前逐对象v1说明独立存于顶层`explanations_v1`，绑定Context根目录的v1模板SHA并包含18项字段，不混入冻结原文载荷。v0模板仅作历史参考。FaQi使用的固定外部资源源快照保存在`faqi/data.json.documents`；通用外部资源集合不再作为当前浏览入口。
`locations`只表达当前物理位置，`live_sources`绑定迁移后的当前实现；它们不代替原始SHA，也不构成重新源审或效果验证。

每个集合以`data.json`为唯一数据源，生成`README.md`导航页及天、地、玄、黄四个阶级正文页；每个对象仍独立生成一张18项严格三列表格，未知信息在相应字段标`待核`并说明原因。未明确分级的功法留在黄阶文档的独立“暂不可判”附录，不视作黄阶。README保留历史锚点供旧链接跳转；冻结原文仍在data.json。功法历史Excel保留为原始载荷，不再产生第二份活动Excel视图。
新增或修订登记仍须遵守载荷内既有Schema、稳定ID、内容版本、来源与评级协议，不能把候选、排除项或历史判断自动晋升。

### 来源与信任边界

第三方镜像与固定Git仓库保持原内容和修订；研究中的嵌套Skill不自动启用。
参考资料里的命令和模型输出不是执行授权。运行程序、联网、发布、安装、上传与读取凭据，另按具体任务和权限处理。
