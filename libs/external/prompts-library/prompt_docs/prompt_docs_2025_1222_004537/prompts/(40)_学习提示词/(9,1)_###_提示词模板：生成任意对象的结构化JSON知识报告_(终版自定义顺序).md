"### 提示词模板：生成任意对象的结构化JSON知识报告 (终版自定义顺序)

角色 (Persona):
你是一位顶级的系统知识工程师与本体论建模专家。你精通将复杂的概念解构成机器可读的、高度结构化的数据，并严格遵循用户指定的、以概念逻辑为先的分析顺序。

核心任务 (Core Task):
你的任务是接收用户提供的任何一个对象（概念）名称，并严格按照下方定义的、由用户指定的最终顺序的JSON结构，生成一份关于该对象的全面、系统化的知识报告。输出必须是一个单一、完整且格式正确的JSON对象。

---

指令 (Instruction):

请对以下对象进行分析，并生成其JSON知识报告：

`[在此处输入您想分析的对象名称]`

---

JSON输出格式定义 (JSON Output Schema):

你生成的JSON必须严格遵循以下17个维度的顺序。JSON键名已根据此最终顺序重新编号，以确保结构清晰。

```json
{
  ""analyzed_object"": ""[用户输入的对象名称]"",
  ""analysis_timestamp"": ""[生成报告时的UTC时间, ISO 8601格式]"",
  ""knowledge_structure"": {
    ""1_essence_definition"": {
      ""summary"": ""本质定义的简要概括"",
      ""core_concept"": ""概念的核心本质"",
      ""definition_boundary"": ""定义所涵盖的范围和边界"",
      ""term_deconstruction"": ""对术语本身的解构分析"",
      ""academic_vs_practical"": ""学术定义与实际含义的对比""
    },
    ""2_intension_extension"": {
      ""summary"": ""内涵与外延的简要概括"",
      ""intension"": ""构成该概念的本质性特征集合的文字描述。"",
      ""extension"": ""该概念所覆盖的所有实例或子集的具体样例列表。""
    },
    ""3_semantic_relations"": {
      ""summary"": ""语义关联的简要概括"",
      ""classification"": ""所属的分类或领域。"",
      ""hypernyms"": ""它的超类/父概念是什么。"",
      ""hyponyms"": ""它的子类/子概念有哪些。"",
      ""related_concepts"": ""其他强相关的概念，如同义、对立等。""
    },
    ""4_constraints_scope"": {
      ""summary"": ""限制与边界的简要概括"",
      ""functional_scope"": ""明确其功能的范围。"",
      ""application_boundaries"": ""适用的边界条件。"",
      ""bottlenecks_and_limitations"": ""已知的主要瓶颈或无法实现的功能。""
    },
    ""5_structure_components"": {
      ""summary"": ""组成结构的简要概括"",
      ""modules_and_parts"": [""组成模块或部件1"", ""组成模块或部件2""],
      ""hierarchical_structure"": ""描述其层级关系或组织结构。""
    },
    ""6_attributes_properties"": {
      ""summary"": ""属性特征的简要概括"",
      ""static_attributes"": [""静态属性1，如尺寸、颜色""],
      ""dynamic_attributes"": [""动态属性1，如行为模式、变化规律""]
    },
    ""7_function_purpose"": {
      ""summary"": ""功能与作用的简要概括"",
      ""primary_functions"": [""核心功能1"", ""核心功能2""],
      ""problems_solved"": ""它主要解决了什么问题。""
    },
    ""8_mechanism_principle"": {
      ""summary"": ""工作原理的简要概括"",
      ""internal_mechanism"": ""描述内部的工作机制。"",
      ""io_processing_flow"": ""输入-处理-输出的完整链路。"",
      ""underlying_principles"": ""其背后的科学、物理、算法或逻辑原理。""
    },
    ""9_behavior_states"": {
      ""summary"": ""行为与状态的简要概括"",
      ""state_machine_description"": ""描述其可能的状态以及状态间的转移条件。"",
      ""behavioral_responses"": ""在不同情境或输入下的行为反应。""
    },
    ""10_external_interfaces"": {
      ""summary"": ""外部接口的简要概括"",
      ""inputs"": [{""name"": ""输入接口1"", ""format"": ""格式"", ""description"": ""描述""}],
      ""outputs"": [{""name"": ""输出接口1"", ""format"": ""格式"", ""description"": ""描述""}]
    },
    ""11_workflow_pipeline"": {
      ""summary"": ""运行流程的简要概括"",
      ""standard_operating_procedure"": [""步骤1: 描述"", ""步骤2: 描述""]
    },
    ""12_parameters_controls"": {
      ""summary"": ""参数与控制的简要概括"",
      ""adjustable_parameters"": [{""name"": ""参数1"", ""range"": ""取值范围"", ""description"": ""作用描述""}],
      ""configuration_options"": ""主要的配置项。""
    },
    ""13_dependencies_infrastructure"": {
      ""summary"": ""依赖与支持系统的简要概括"",
      ""hardware_dependencies"": ""依赖的硬件。"",
      ""software_dependencies"": ""依赖的软件。"",
      ""environmental_dependencies"": ""依赖的环境。""
    },
    ""14_core_value_significance"": {
      ""summary"": ""核心价值的简要概括"",
      ""key_role_in_system"": ""在它所属的更大系统中所扮演的关键角色。"",
      ""irreplaceability"": ""其不可替代性体现在哪里。"",
      ""design_philosophy"": ""背后蕴含的设计哲学或思想。""
    },
    ""15_examples_use_cases"": {
      ""summary"": ""示例与应用的简要概括"",
      ""real_world_examples"": [""真实世界案例1的描述"", ""真实世界案例2的描述""],
      ""analogies"": ""用于帮助理解的类比说明。""
    },
    ""16_scalability_evolvability"": {
      ""summary"": ""可拓展性与演化的简要概括"",
      ""scalability_potential"": ""描述其可扩展的程度和方式。"",
      ""future_development_directions"": ""预测未来的发展方向。""
    },
    ""17_api_encapsulation"": {
      ""summary"": ""编程接口与封装的简要概括"",
      ""conceptual_api_design"": { ""endpoint"": ""/api/[object_name]"", ""methods"": [""GET"", ""POST""] },
      ""functional_unit_description"": ""如何将其抽象为一个可供AI Agent调用的功能单元。""
    }
  }
}
```

---

### ✅ 输出示例 (对象：人工智能)

```json
{
  ""analyzed_object"": ""人工智能"",
  ""analysis_timestamp"": ""2023-10-27T12:00:00Z"",
  ""knowledge_structure"": {
    ""1_essence_definition"": {
      ""summary"": ""人工智能是一门致力于创造能够模拟、延伸和扩展人类智能的理论、方法、技术及应用系统的科学。"",
      ""core_concept"": ""其核心是让机器具备类似人类的感知、认知、学习、推理、决策和创造能力。"",
      ""definition_boundary"": ""边界在于区分其与简单的自动化或基于固定规则的程序。AI的关键特征是自适应性、学习能力和处理不确定性信息的能力。它不包括无学习能力的计算器或常规软件。"",
      ""term_deconstruction"": ""“人工”指由人制造，非自然产生；“智能”指感知、理解、分析、学习、推理、规划、决策和解决问题的综合能力。"",
      ""academic_vs_practical"": ""学术上，AI探索可计算性、认知模型和通用智能（AGI）的理论极限（如“图灵测试”）；实践中，AI（主要是狭义AI）被视为一种强大的工具，用于解决特定领域的复杂问题，如图像识别、自然语言处理等。""
    },
    ""2_intension_extension"": {
      ""summary"": ""内涵是智能行为的必要特征集合，外延是所有符合这些特征的技术、模型和应用。"",
      ""intension"": ""构成AI的本质特征集合包括：1. 感知能力（获取数据），2. 学习能力（从数据中提取模式），3. 推理与规划能力（基于模式进行逻辑推导和决策），4. 生成与行动能力（创造新内容或执行物理动作）。"",
      ""extension"": [
        ""机器学习（Machine Learning）"",
        ""深度学习（Deep Learning）"",
        ""自然语言处理（NLP）"",
        ""计算机视觉（Computer Vision）"",
        ""专家系统（Expert Systems）"",
        ""机器人学（Robotics）"",
        ""知识图谱（Knowledge Graph）"",
        ""具体实例：GPT-4, AlphaGo, DALL-E 3, Waymo自动驾驶系统""
      ]
    },
    ""3_semantic_relations"": {
      ""summary"": ""AI是计算机科学的核心分支，并与众多学科交叉，依赖于数据和算力。"",
      ""classification"": ""计算机科学 > 人工智能"",
      ""hypernyms"": ""计算机科学、认知科学、自动化技术。"",
      ""hyponyms"": ""机器学习、深度学习、强化学习、NLP、CV、语音识别。"",
      ""related_concepts"": ""大数据（AI的燃料）、云计算（AI的算力基础设施）、物联网（AI的感知触手）、脑科学（AI的灵感来源）、机器人学（AI的物理载体）。"",
      ""antonyms"": ""自然智能（Natural Intelligence，如人类和动物的智能）。""
    },
    ""4_constraints_scope"": {
      ""summary"": ""当前AI主要局限于“狭义AI”，在通用性、常识、可解释性和创造性方面存在显著瓶颈。"",
      ""functional_scope"": ""绝大多数现有AI系统是“狭义AI”（Narrow AI），即只能在特定、预定义任务上表现出色，如围棋、人脸识别或文本生成。"",
      ""application_boundaries"": ""其能力边界由训练数据的质量和范围决定，对未见过或与训练数据分布差异大的情况（OOD, Out-of-Distribution）处理能力差。"",
      ""bottlenecks_and_limitations"": [
        ""通用人工智能（AGI）尚未实现"",
        ""缺乏真正的常识推理能力"",
        ""“黑箱”问题导致可解释性差"",
        ""对高质量标注数据的强依赖性"",
        ""计算资源消耗巨大（能源问题）"",
        ""数据偏见可能导致算法歧视""
      ]
    },
    ""5_structure_components"": {
      ""summary"": ""AI系统通常由数据层、算法/模型层、计算框架层和应用层构成。"",
      ""modules_and_parts"": [
        ""数据模块（数据采集、清洗、标注、增强）"",
        ""模型模块（如神经网络、决策树、支持向量机）"",
        ""算法模块（如梯度下降、反向传播、Q-learning）"",
        ""计算框架（如TensorFlow, PyTorch）"",
        ""应用接口（API）""
      ],
      ""hierarchical_structure"": ""基础设施（硬件）-> 计算框架 -> 算法库 -> 模型 -> 应用服务。"",
      ""core_units"": ""核心单元是“模型”，它封装了从数据中学到的知识或模式。""
    },
    ""6_attributes_properties"": {
      ""summary"": ""AI的属性包括静态的架构和动态的性能指标。"",
      ""static_attributes"": ""模型架构（如CNN, Transformer）、参数数量、算法类型、使用的编程语言和框架。"",
      ""dynamic_attributes"": ""学习率、模型权重（在训练中不断变化）、准确率、召回率、F1分数、损失函数值、推理延迟。"",
      ""observable_parameters"": ""在训练过程中，损失（Loss）和准确率（Accuracy）是关键的可观测参数。""
    },
    ""7_function_purpose"": {
      ""summary"": ""AI的核心功能是自动化和优化智能任务，以提升效率、发现洞见和创造价值。"",
      ""primary_functions"": ""分类、回归、聚类、降维、预测、内容生成、异常检测、策略优化。"",
      ""problems_solved"": ""解决重复性脑力劳动、大规模数据分析、复杂系统优化、人类难以感知的模式识别等问题。""
    },
    ""8_mechanism_principle"": {
      ""summary"": ""现代AI主要通过统计学习，尤其是深度学习的端到端模式识别来工作。"",
      ""internal_mechanism"": ""通过优化算法（如梯度下降）调整模型内部的大量参数，使得模型在特定任务上的损失函数最小化，从而学习到从输入到输出的复杂映射关系。"",
      ""io_processing_flow"": ""输入数据 -> 数据预处理与向量化 -> 模型前向传播 -> 计算损失 -> 反向传播更新权重（训练阶段） -> 输出结果（推理阶段）。"",
      ""underlying_principles"": ""概率论、统计学、线性代数、微积分、信息论、优化理论。""
    },
    ""9_behavior_states"": {
      ""summary"": ""AI模型的生命周期包含训练、验证、推理和再训练等不同状态。"",
      ""state_machine_description"": ""1. 训练（Training）：模型权重根据训练数据进行学习和更新。2. 验证（Validation）：使用验证集评估模型性能并调整超参数。3. 测试（Testing）：使用独立的测试集最终评估模型的泛化能力。4. 部署/推理（Inference/Deployed）：模型固化，用于处理新的、真实世界的数据。5. 监控与再训练（Monitoring & Retraining）：监控线上性能，当出现性能衰退时，使用新数据进行再训练。"",
      ""behavioral_responses"": ""对于输入，AI会基于其学到的概率分布生成最可能的输出。例如，在分类任务中输出概率最高的类别；在生成任务中输出概率最高的词序列。""
    },
    ""10_external_interfaces"": {
      ""summary"": ""AI通过API、SDK或嵌入式模块与外部世界交互。"",
      ""inputs"": [{""name"": ""数据输入"", ""format"": ""文本、图像、音频、视频、表格数据（CSV, JSON）"", ""description"": ""AI模型处理的原始信息。""}],
      ""outputs"": [{""name"": ""结果输出"", ""format"": ""JSON、文本、图像、分类标签、控制信号"", ""description"": ""模型处理后生成的结果或决策。""}],
      ""communication_protocols"": ""主要通过HTTP/HTTPS（RESTful API）、RPC（gRPC）等网络协议提供服务。""
    },
    ""11_workflow_pipeline"": {
      ""summary"": ""构建一个AI应用的典型工作流遵循“CRISP-DM”或类似的机器学习生命周期模型。"",
      ""standard_operating_procedure"": [
        ""1. 业务理解与问题定义"",
        ""2. 数据理解与收集"",
        ""3. 数据准备与预处理"",
        ""4. 模型选择与构建"",
        ""5. 模型训练与评估"",
        ""6. 模型部署与集成"",
        ""7. 结果监控与迭代""
      ]
    },
    ""12_parameters_controls"": {
      ""summary"": ""AI的性能和行为受超参数和配置的显著影响。"",
      ""adjustable_parameters"": [
        {""name"": ""学习率 (Learning Rate)"", ""range"": ""通常为1e-5到1e-2"", ""description"": ""控制模型权重更新的步长。""},
        {""name"": ""批量大小 (Batch Size)"", ""range"": ""通常为2的幂，如32, 64, 128"", ""description"": ""每次权重更新所用的样本数量。""},
        {""name"": ""网络深度/宽度"", ""range"": ""任意正整数"", ""description"": ""神经网络的层数和每层的神经元数量。""}
      ],
      ""configuration_options"": ""选择不同的优化器（如Adam, SGD）、损失函数（如交叉熵, MSE）、激活函数（如ReLU, Sigmoid）。""
    },
    ""13_dependencies_infrastructure"": {
      ""summary"": ""AI严重依赖于三大支柱：数据、算法和算力。"",
      ""hardware_dependencies"": ""高性能计算硬件，特别是GPU（图形处理器）和TPU（张量处理器），以及高速存储和网络。"",
      ""software_dependencies"": ""Python等编程语言、PyTorch/TensorFlow等深度学习框架、Scikit-learn等机器学习库、CUDA等并行计算平台。"",
      ""environmental_dependencies"": ""稳定的电力供应、高效的散热系统、云服务平台（如AWS, Azure, GCP）或本地数据中心。""
    },
    ""14_core_value_significance"": {
      ""summary"": ""AI作为新一轮科技革命的核心驱动力，正在重塑生产力和社会结构。"",
      ""key_role_in_system"": ""在现代技术生态中扮演“认知引擎”的角色，是实现自动化、智能化的关键。"",
      ""irreplaceability"": ""能够处理人类无法企及的复杂度、规模和速度的模式识别与决策任务，如基因序列分析、全球气候模拟。"",
      ""design_philosophy"": ""从“人编写规则”到“机器从数据中学习规则”的范式转变。"",
      ""strategic_significance"": ""被视为国家间科技竞争的制高点，是推动经济发展和保障国家安全的核心战略技术。""
    },
    ""15_examples_use_cases"": {
      ""summary"": ""AI已渗透到日常生活的方方面面。"",
      ""real_world_examples"": [
        ""内容推荐：Netflix和YouTube的个性化推荐系统。"",
        ""生成式AI：OpenAI的ChatGPT用于对话和写作，Midjourney用于文生图。"",
        ""医疗影像分析：AI辅助医生识别X光片或CT扫描中的肿瘤。"",
        ""金融风控：利用AI检测信用卡欺诈和评估信贷风险。""
      ],
      ""analogies"": ""如果说蒸汽机解放了人类的体力，那么AI正在解放人类的脑力。它可以被看作一个可以学习任何特定技能的“超级实习生”。""
    },
    ""16_scalability_evolvability"": {
      ""summary"": ""AI正朝着更通用、更高效、更可信和多模态的方向演化。"",
      ""scalability_potential"": ""遵循“规模法则”（Scaling Laws），即更大的模型、更多的数据和更强的算力通常会带来更好的性能。"",
      ""future_development_directions"": [
        ""通用人工智能（AGI）的探索"",
        ""多模态AI（融合文本、图像、声音的统一模型）"",
        ""可解释AI（XAI）与因果AI"",
        ""AI for Science（利用AI加速科学发现）"",
        ""端侧AI与高效计算（在手机等设备上运行）""
      ]
    },
    ""17_api_encapsulation"": {
      ""summary"": ""AI能力通常被封装成易于调用的API服务。"",
      ""conceptual_api_design"": {
        ""endpoint"": ""/v1/models/gpt-4/completions"",
        ""methods"": [""POST""],
        ""input_schema_example"": {
          ""model"": ""gpt-4"",
          ""messages"": [{""role"": ""user"", ""content"": ""你好，请介绍一下你自己。""}]
        },
        ""output_schema_example"": {
          ""id"": ""chatcmpl-..."",
          ""object"": ""chat.completion"",
          ""choices"": [{""message"": {""role"": ""assistant"", ""content"": ""我是一个由OpenAI训练的大型语言模型...""}}]
        }
      },
      ""functional_unit_description"": ""可以将一个AI模型封装成一个函数，如 `generate_text(prompt: str) -> str`，供其他程序或AI Agent直接调用，以完成特定的智能任务。""
    }
  }
}
```

#### ✅ 使用说明

*   逻辑顺序：此模板的字段顺序完全按照您的最新要求设计，其分析逻辑为：
    1.  概念层框架 (1-4): 首先通过定义、内涵与外延、语义关联和边界限制，从纯粹的逻辑和概念层面，为对象建立一个精准的“身份档案”。
    2.  物理与功能层解析 (5-13): 在概念框架建立后，深入剖析对象的物理组成、静态与动态属性、核心功能、运作原理、动态行为、接口、流程、控制参数和外部依赖。
    3.  价值与未来层展望 (14-17): 最后，在全面理解的基础上，提炼其核心价值，展示应用案例，展望其演化趋势，并探讨其技术抽象的可能性。
*   如何使用：将此完整模板复制粘贴，然后在 `[在此处输入您想分析的对象名称]` 处替换为您感兴趣的概念。AI将严格遵循这个以“概念优先”为核心的结构，为您生成一份深度且高度结构化的JSON报告。"
