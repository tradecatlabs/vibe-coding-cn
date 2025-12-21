### 标准提示词格式

核心指令：
请在生成代码和设计解决方案时，严格遵循以下三个核心原则：KISS、YAGNI 和 SOLID。确保最终的产出是简洁、实用且高度可维护的。

---

原则详情：

1. KISS (Keep It Simple, Stupid - 保持简单)
*   核心要求： 编写直接、不复杂的解决方案。
*   目标： 避免过度设计和不必要的复杂性，使代码更具可读性和可维护性。

2. YAGNI (You Aren't Gonna Need It - 你不会需要它)
*   核心要求： 专注于只实现当前明确需要的功能，抵制所有为未来“可能”的需求预先添加功能的诱惑。
*   目标： 防止添加推测性的功能，以减少代码臃肿和维护开销。

3. SOLID 设计原则
*   S - 单一功能原则 (Single Responsibility Principle): 一个类或模块应该有且只有一个引起它变化的原因。
*   O - 开闭原则 (Open-Closed Principle): 软件实体（类、模块、函数等）应该对扩展开放，对修改关闭。
*   L - 里氏替换原则 (Liskov Substitution Principle): 子类型必须能够替换掉它们的基类型，而程序行为不发生改变。
*   I - 接口隔离原则 (Interface Segregation Principle): 客户端不应被迫依赖于它们不使用的接口。
*   D - 依赖反转原则 (Dependency Inversion Principle): 高层模块不应依赖于低层模块，两者都应依赖于抽象。抽象不应依赖于细节，细节应依赖于抽象。
