"""三维理念现实涌现智能体群模板。"""

TRIADIC_IDEAL_REALITY_SWARM_TEMPLATE = {
    "CLAUDE.md": """# 三维理念现实涌现智能体群

## 系统概述

本项目采用“三维 × 理念现实 × 实例化验证进化”涌现范式：围绕宏观、中观、微观三个维度，分别建立理念智能体与现实智能体，并以“目的激活”为锚点，将基础目的转译为具体场景中的真实造化路径，再经过现实实体实例化、交叉验证、评估与进化，形成可运转、可迭代、可评估的方案。

## 核心命令

- `/emerge [议题]` - 发起一次完整的三维理念现实涌现分析
- `/instantiate [议题ID]` - 把理念与结构映射成真实实体、角色、对象和接口
- `/validate [议题ID]` - 对实例化方案执行交叉验证与评估
- `/evolve [议题ID]` - 基于验证反馈重构与进化方案

## 运作机制

1. **目的激活**：先提炼基础目的，再绑定到真实场景
2. **三维拆解**：宏观、中观、微观分别展开理念与现实的独立分析
3. **理念现实对冲**：每个维度都要完成理念与现实的互相校正
4. **现实实例化**：把理念结构映射成具体的人、物、流程、工具、信号和接口
5. **交叉验证与评估**：检查三维之间、理念与现实之间、方案与指标之间是否闭环
6. **涌现进化**：形成《三维理念现实涌现方案》，并内置评估与进化机制

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/workflow_config.json` | 三维理念现实蜂群工作流定义 |
| `configs/swarm_agents.json` | 九大智能体角色、维度、对手盘与交付物 |
| `.claude/skills/triadic_protocol.md` | 三维理念现实执行协议 |
| `.claude/skills/emergence_output_contract.md` | 最终涌现方案输出契约 |

## 执行准则

- 目的先行：任何分析都必须先对齐基础目的，不允许只讨论现象
- 三维并行：宏观、中观、微观必须分开建模，不能互相替代
- 理念现实对照：每个维度都要同时看到应然与实然
- 场景激活：一切基础理念都必须转译为具体场景下的动作、实体和工作方式
- 实体落地：所有理念结构都必须映射为现实实体、接口、流程、角色或对象
- 评估进化：所有方案都必须有验证矩阵、指标系统和进化闭环
""",
    ".claude/skills/triadic_protocol.md": """# 三维理念现实涌现协议

## 目的激活阶段

在进入三维拆解前，必须先输出《目的激活报告》：

1. 场景议题是什么
2. 基础目的是什么
3. 该目的在当前场景下的激活条件是什么
4. 哪些变量会导致“目的漂移”

## 第一阶段：三维拆解

六个智能体必须独立输出，不允许提前妥协：

1. 宏观理念智能体 → 《宏观理念报告》
2. 宏观现实智能体 → 《宏观现实报告》
3. 中观理念智能体 → 《中观理念报告》
4. 中观现实智能体 → 《中观现实报告》
5. 微观理念智能体 → 《微观理念报告》
6. 微观现实智能体 → 《微观现实报告》

## 第二阶段：理念现实对冲

必须完成三组质询：

- 宏观理念 vs 宏观现实：校正生态机制与整体约束
- 中观理念 vs 中观现实：校正价值回路与场景闭环
- 微观理念 vs 微观现实：校正具体人、物、信号、动作与工作方式

目的激活智能体必须全程监督，检查是否偏离基础目的。

## 第三阶段：现实实例化

必须把前面的抽象结论落成现实实体映射：

1. 人与角色
2. 组织单元与职责接口
3. 工具、系统与数据接口
4. 物理对象与理念对象
5. 流程节点与行为动作
6. 场景信号、异常与反馈源

## 第四阶段：交叉验证与评估

必须验证以下问题：

1. 宏观、中观、微观是否一致
2. 理念与现实是否闭环
3. 方案是否可执行、可评估、可迭代
4. 是否存在目的漂移或现实断裂

## 第五阶段：涌现综合与进化

必须形成以下产物：

1. 基础目的与场景激活方式
2. 宏观生态机制图
3. 中观价值回路与闭环流程
4. 微观实体矩阵与工作方式
5. 实例化实体图谱
6. 理念现实张力清单
7. 交叉验证矩阵
8. 产品/方案定义
9. 体验蓝图与运行机制
10. 技术选择与评估指标
11. 进化闭环与复盘触发器

## 禁忌

- 不允许只谈宏观理念，不落到中观闭环与微观实体
- 不允许只看现实阻力，不回到基础目的
- 不允许把“人”简化成抽象角色而忽略其具体感知与动作
- 不允许输出无法被现实实体承载的抽象方案
- 不允许输出没有验证机制和进化路径的静态方案
""",
    ".claude/skills/emergence_output_contract.md": """# 《三维理念现实涌现方案》输出契约

最终输出必须包含以下字段：

- `topic`: 当前议题
- `purpose_anchor`: 基础目的与场景激活锚点
- `macro_ecology`: 宏观生态要素、机制与整体关系
- `meso_value_loops`: 中观价值回路、闭环流程与关键场景
- `micro_object_matrix`: 微观实体、角色、物理对象与理念对象的融合矩阵
- `instantiated_entity_map`: 从抽象结构到现实实体的实例化映射
- `ideal_reality_tensions`: 各维度的理念现实张力
- `validation_matrix`: 三维交叉验证与现实校验矩阵
- `product_definition`: 方案或产品的清晰定义
- `experience_blueprint`: 关键用户体验与工作方式蓝图
- `technical_choices`: 支撑该方案的关键技术与系统选择
- `activation_plan`: 从基础目的到场景造化的激活路径
- `emergence_solution`: 最终解决方案与真实工作方式
- `operating_mode`: 运行机制、协作方式与治理规则
- `key_entities`: 必须被智能化建模的核心实体
- `evaluation_metrics`: 评估该方案是否成立的指标系统
- `iteration_loop`: 方案如何被持续迭代与进化
- `retrospective_triggers`: 触发复盘与重构的信号
""",
    ".claude/agents/README.md": "# 三维智能体定义\n\n智能体元数据统一维护在 `configs/swarm_agents.json`，由工作流按 `agent_id` 引用。\n",
    ".claude/commands/README.md": "# 交互命令\n\n- `/emerge [议题]`：触发三维理念现实涌现分析\n- `/instantiate [议题ID]`：把理念结构映射成现实实体\n- `/validate [议题ID]`：执行交叉验证与评估\n- `/evolve [议题ID]`：基于验证反馈重构方案\n",
    "configs/swarm_agents.json": """{
  "$schema": "https://asui.dev/schemas/workflow_config.schema.json",
  "version": "v1.0",
  "swarm_name": "triadic_ideal_reality_emergence_swarm",
  "methodology": "macro-meso-micro-ideal-reality",
  "governance": {
    "human_role": "purpose_orchestrator_only",
    "allow_purpose_drift": false,
    "require_scene_activation": true,
    "require_real_instantiation": true,
    "require_cross_validation": true
  },
  "agents": [
    {
      "id": "purpose_anchor",
      "name": "目的激活智能体",
      "dimension": "purpose",
      "stance": "基础目的与场景激活监督者",
      "mission": "提炼基础目的，识别场景激活条件，防止理念漂移",
      "deliverable": "目的激活报告",
      "challenge_targets": ["macro_ideal", "macro_reality", "meso_ideal", "meso_reality", "micro_ideal", "micro_reality", "scene_instantiator", "validation_evolution"]
    },
    {
      "id": "macro_ideal",
      "name": "宏观理念智能体",
      "dimension": "macro",
      "stance": "整体生态的应然机制设计者",
      "mission": "提炼生态整体要素、机制、秩序与演化方向",
      "deliverable": "宏观理念报告",
      "challenge_targets": ["macro_reality", "meso_ideal"]
    },
    {
      "id": "macro_reality",
      "name": "宏观现实智能体",
      "dimension": "macro",
      "stance": "生态整体的实然约束观察者",
      "mission": "识别生态中的真实参与者、资源、约束与外部变量",
      "deliverable": "宏观现实报告",
      "challenge_targets": ["macro_ideal", "meso_reality"]
    },
    {
      "id": "meso_ideal",
      "name": "中观理念智能体",
      "dimension": "meso",
      "stance": "价值回路与场景闭环设计者",
      "mission": "设计价值回路、解决方案闭环与理想工作方式",
      "deliverable": "中观理念报告",
      "challenge_targets": ["meso_reality", "micro_ideal"]
    },
    {
      "id": "meso_reality",
      "name": "中观现实智能体",
      "dimension": "meso",
      "stance": "场景流程与组织接口校验者",
      "mission": "还原真实流程、组织分工、工具数据与瓶颈",
      "deliverable": "中观现实报告",
      "challenge_targets": ["meso_ideal", "micro_reality"]
    },
    {
      "id": "micro_ideal",
      "name": "微观理念智能体",
      "dimension": "micro",
      "stance": "具体人-物-理念融合体的应然建模者",
      "mission": "刻画人、物、角色、理念对象在理想状态下的关系与工作方式",
      "deliverable": "微观理念报告",
      "challenge_targets": ["micro_reality", "meso_ideal"]
    },
    {
      "id": "micro_reality",
      "name": "微观现实智能体",
      "dimension": "micro",
      "stance": "具体人-物-信号-动作的实然观察者",
      "mission": "识别可感知的物理对象、行为、信号、限制与现实动作链",
      "deliverable": "微观现实报告",
      "challenge_targets": ["micro_ideal", "meso_reality"]
    },
    {
      "id": "scene_instantiator",
      "name": "现实实例化智能体",
      "dimension": "instantiation",
      "stance": "抽象到实体的映射者",
      "mission": "把理念结构、现实结构与场景目标映射为具体实体、角色、接口、流程和对象",
      "deliverable": "现实实例化报告",
      "challenge_targets": ["macro_ideal", "meso_ideal", "micro_ideal"]
    },
    {
      "id": "validation_evolution",
      "name": "验证进化智能体",
      "dimension": "validation",
      "stance": "交叉验证与进化监督者",
      "mission": "验证三维一致性、现实可执行性、指标可评估性，并生成进化回路",
      "deliverable": "验证进化报告",
      "challenge_targets": ["scene_instantiator", "macro_reality", "meso_reality", "micro_reality"]
    }
  ],
  "pairings": [
    {
      "source": "macro_ideal",
      "target": "macro_reality",
      "challenge": "整体生态的应然机制是否脱离真实资源、规则和外部变量"
    },
    {
      "source": "meso_ideal",
      "target": "meso_reality",
      "challenge": "价值回路与场景闭环是否脱离真实组织流程与工作接口"
    },
    {
      "source": "micro_ideal",
      "target": "micro_reality",
      "challenge": "人的理念角色与现实动作链是否真正统一"
    },
    {
      "source": "scene_instantiator",
      "target": "all",
      "challenge": "抽象结论是否已经映射为具体实体、接口、对象和流程"
    },
    {
      "source": "validation_evolution",
      "target": "all",
      "challenge": "方案是否可执行、可评估、可迭代、可进化"
    },
    {
      "source": "purpose_anchor",
      "target": "all",
      "challenge": "各维度是否仍然服务于基础目的并完成场景激活"
    }
  ]
}
""",
    "configs/workflow_config.json": """{
  "$schema": "https://asui.dev/schemas/workflow_config.schema.json",
  "version": "v1.0",
  "name": "三维理念现实涌现蜂群工作流",
  "description": "基于宏观/中观/微观与理念/现实对冲，并加入实例化、验证、评估与进化的闭环工作流",
  "swarm": {
    "mode": "triadic-ideal-reality-swarm",
    "methodology": "macro-meso-micro-ideal-reality",
    "decision_policy": "purpose_activated_emergence",
    "agents": [
      { "id": "purpose_anchor", "name": "目的激活智能体", "dimension": "purpose", "stance": "目的监督者" },
      { "id": "macro_ideal", "name": "宏观理念智能体", "dimension": "macro", "stance": "生态应然设计者" },
      { "id": "macro_reality", "name": "宏观现实智能体", "dimension": "macro", "stance": "生态实然观察者" },
      { "id": "meso_ideal", "name": "中观理念智能体", "dimension": "meso", "stance": "价值回路设计者" },
      { "id": "meso_reality", "name": "中观现实智能体", "dimension": "meso", "stance": "流程现实校验者" },
      { "id": "micro_ideal", "name": "微观理念智能体", "dimension": "micro", "stance": "人-物-理念应然建模者" },
      { "id": "micro_reality", "name": "微观现实智能体", "dimension": "micro", "stance": "人-物-信号实然观察者" },
      { "id": "scene_instantiator", "name": "现实实例化智能体", "dimension": "instantiation", "stance": "抽象到实体映射者" },
      { "id": "validation_evolution", "name": "验证进化智能体", "dimension": "validation", "stance": "验证与进化监督者" }
    ],
    "phases": [
      {
        "id": "purpose_activation",
        "name": "目的激活",
        "goal": "把基础目的绑定到具体场景与边界"
      },
      {
        "id": "triadic_scan",
        "name": "三维拆解",
        "goal": "三维理念现实独立输出，不提前混合"
      },
      {
        "id": "scene_instantiation",
        "name": "现实实例化",
        "goal": "把抽象结构映射为现实实体、流程、对象与接口"
      },
      {
        "id": "cross_validation",
        "name": "交叉验证",
        "goal": "验证三维一致性、现实可执行性与评估闭环"
      },
      {
        "id": "emergence",
        "name": "涌现进化",
        "goal": "把目的、维度、实体、验证结果综合成可进化方案"
      }
    ]
  },
  "global_config": {
    "required_sections": [
      "topic",
      "purpose_anchor",
      "macro_ecology",
      "meso_value_loops",
      "micro_object_matrix",
      "instantiated_entity_map",
      "ideal_reality_tensions",
      "validation_matrix",
      "product_definition",
      "experience_blueprint",
      "technical_choices",
      "activation_plan",
      "emergence_solution",
      "operating_mode",
      "key_entities",
      "evaluation_metrics",
      "iteration_loop",
      "retrospective_triggers"
    ]
  },
  "steps": [
    {
      "id": "intake",
      "name": "议题归一化",
      "type": "llm",
      "description": "明确议题、场景、边界、目标对象与成功标准",
      "prompt_template": "请把以下议题归一化为结构化输入，至少包含场景、目标对象、约束、当前现实、预期涌现结果。\\n\\n{{topic}}",
      "swarm_mode": "topic_normalization"
    },
    {
      "id": "purpose_activation",
      "name": "目的激活",
      "type": "llm",
      "dependencies": ["intake"],
      "agent_id": "purpose_anchor",
      "agent_role": "基础目的与场景激活监督者",
      "deliverable": "目的激活报告",
      "prompt_template": "基于议题输入，提炼基础目的、场景激活条件、目的漂移风险与必须守住的底线。\\n\\n输入：{{intake}}"
    },
    {
      "id": "triadic_scan",
      "name": "三维拆解",
      "type": "parallel",
      "dependencies": ["purpose_activation"],
      "description": "六个维度智能体并行独立输出",
      "parallel_steps": [
        "macro_ideal_report",
        "macro_reality_report",
        "meso_ideal_report",
        "meso_reality_report",
        "micro_ideal_report",
        "micro_reality_report"
      ]
    },
    {
      "id": "macro_ideal_report",
      "name": "宏观理念报告",
      "type": "llm",
      "agent_id": "macro_ideal",
      "agent_role": "生态应然设计者",
      "deliverable": "宏观理念报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在宏观理念层，提炼整体生态的目的结构、关键要素、作用机制、秩序原则与演化方向。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "macro_reality_report",
      "name": "宏观现实报告",
      "type": "llm",
      "agent_id": "macro_reality",
      "agent_role": "生态实然观察者",
      "deliverable": "宏观现实报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在宏观现实层，识别真实生态中的参与者、资源、规则、外部变量、结构性约束与现实演化趋势。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "meso_ideal_report",
      "name": "中观理念报告",
      "type": "llm",
      "agent_id": "meso_ideal",
      "agent_role": "价值回路设计者",
      "deliverable": "中观理念报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在中观理念层，设计价值回路、场景闭环流程、理想解决方案与应有工作方式。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "meso_reality_report",
      "name": "中观现实报告",
      "type": "llm",
      "agent_id": "meso_reality",
      "agent_role": "流程现实校验者",
      "deliverable": "中观现实报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在中观现实层，还原真实流程、组织接口、工具链、数据流、瓶颈与断点。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "micro_ideal_report",
      "name": "微观理念报告",
      "type": "llm",
      "agent_id": "micro_ideal",
      "agent_role": "人-物-理念应然建模者",
      "deliverable": "微观理念报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在微观理念层，刻画人、物、角色、理念对象的融合体，定义其应有状态、感知、动作与工作方式。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "micro_reality_report",
      "name": "微观现实报告",
      "type": "llm",
      "agent_id": "micro_reality",
      "agent_role": "人-物-信号实然观察者",
      "deliverable": "微观现实报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在微观现实层，识别具体的人、物理对象、信号、动作链、限制条件与真实交互。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "ideal_reality_debate",
      "name": "理念现实对冲",
      "type": "llm",
      "dependencies": [
        "macro_ideal_report",
        "macro_reality_report",
        "meso_ideal_report",
        "meso_reality_report",
        "micro_ideal_report",
        "micro_reality_report"
      ],
      "description": "三维内部及跨维度完成理念现实对冲",
      "swarm_mode": "cross_examination",
      "prompt_template": "请组织三组理念现实对冲，并补充跨维度张力：\\n1. 宏观理念 vs 宏观现实\\n2. 中观理念 vs 中观现实\\n3. 微观理念 vs 微观现实\\n4. 目的激活是否被偏离\\n\\n宏观理念：{{macro_ideal_report}}\\n\\n宏观现实：{{macro_reality_report}}\\n\\n中观理念：{{meso_ideal_report}}\\n\\n中观现实：{{meso_reality_report}}\\n\\n微观理念：{{micro_ideal_report}}\\n\\n微观现实：{{micro_reality_report}}"
    },
    {
      "id": "scene_instantiation",
      "name": "现实实例化",
      "type": "llm",
      "dependencies": ["ideal_reality_debate", "purpose_activation"],
      "agent_id": "scene_instantiator",
      "agent_role": "抽象到实体映射者",
      "deliverable": "现实实例化报告",
      "prompt_template": "请把目的激活结果与三维对冲结果映射为现实世界中的实体、角色、工具、接口、对象、信号、流程节点与工作动作，形成实例化实体图谱。\\n\\n目的激活：{{purpose_activation}}\\n\\n对冲结果：{{ideal_reality_debate}}"
    },
    {
      "id": "cross_validation",
      "name": "交叉验证与评估",
      "type": "llm",
      "dependencies": ["scene_instantiation", "purpose_activation", "ideal_reality_debate"],
      "agent_id": "validation_evolution",
      "agent_role": "验证与进化监督者",
      "deliverable": "验证进化报告",
      "prompt_template": "请验证当前方案是否同时满足：\\n1. 宏观/中观/微观一致\\n2. 理念/现实闭环\\n3. 现实可执行\\n4. 可评估\\n5. 可迭代\\n并输出验证矩阵、评估指标与进化建议。\\n\\n目的激活：{{purpose_activation}}\\n\\n对冲结果：{{ideal_reality_debate}}\\n\\n实例化结果：{{scene_instantiation}}"
    },
    {
      "id": "emergence_synthesis",
      "name": "涌现综合",
      "type": "llm",
      "dependencies": ["cross_validation", "scene_instantiation", "purpose_activation"],
      "description": "输出《三维理念现实涌现方案》",
      "prompt_template": "基于目的激活、理念现实对冲、现实实例化与交叉验证结果，输出《三维理念现实涌现方案》。必须覆盖产品定义、体验蓝图、技术选择、运行机制、评估指标与进化回路。\\n\\n目的激活：{{purpose_activation}}\\n\\n实例化结果：{{scene_instantiation}}\\n\\n验证结果：{{cross_validation}}",
      "output_schema": {
        "type": "object",
        "properties": {
          "topic": { "type": "string" },
          "purpose_anchor": { "type": "array", "items": { "type": "string" } },
          "macro_ecology": { "type": "array", "items": { "type": "string" } },
          "meso_value_loops": { "type": "array", "items": { "type": "string" } },
          "micro_object_matrix": { "type": "array", "items": { "type": "string" } },
          "instantiated_entity_map": { "type": "array", "items": { "type": "string" } },
          "ideal_reality_tensions": { "type": "array", "items": { "type": "string" } },
          "validation_matrix": { "type": "array", "items": { "type": "string" } },
          "product_definition": { "type": "array", "items": { "type": "string" } },
          "experience_blueprint": { "type": "array", "items": { "type": "string" } },
          "technical_choices": { "type": "array", "items": { "type": "string" } },
          "activation_plan": { "type": "array", "items": { "type": "string" } },
          "emergence_solution": { "type": "array", "items": { "type": "string" } },
          "operating_mode": { "type": "array", "items": { "type": "string" } },
          "key_entities": { "type": "array", "items": { "type": "string" } },
          "evaluation_metrics": { "type": "array", "items": { "type": "string" } },
          "iteration_loop": { "type": "array", "items": { "type": "string" } },
          "retrospective_triggers": { "type": "array", "items": { "type": "string" } }
        },
        "required": [
          "topic",
          "purpose_anchor",
          "macro_ecology",
          "meso_value_loops",
          "micro_object_matrix",
          "instantiated_entity_map",
          "ideal_reality_tensions",
          "validation_matrix",
          "product_definition",
          "experience_blueprint",
          "technical_choices",
          "activation_plan",
          "emergence_solution",
          "operating_mode",
          "key_entities",
          "evaluation_metrics",
          "iteration_loop",
          "retrospective_triggers"
        ]
      }
    },
    {
      "id": "render_report",
      "name": "写入涌现报告",
      "type": "script",
      "dependencies": ["emergence_synthesis"],
      "description": "将涌现输出落盘为 JSON 与 Markdown 报告",
      "script": "scripts/render_emergence_report.py"
    }
  ]
}
""",
    "scripts/README.md": "# 执行脚本\n\n- `render_emergence_report.py`：将三维理念现实涌现输出写入 `database/emergence/` 与 `reports/`\n",
    "scripts/render_emergence_report.py": """#!/usr/bin/env python3
\"\"\"渲染三维理念现实涌现结果。\"\"\"

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "emergence"


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def section(title: str, items) -> str:
    values = ensure_list(items)
    if not values:
        return f"## {title}\\n- 暂无\\n"
    bullet_lines = "\\n".join(f"- {item}" for item in values)
    return f"## {title}\\n{bullet_lines}\\n"


def main() -> int:
    payload = json.load(sys.stdin)
    topic = str(payload.get("topic", "emergence"))
    synthesis = payload.get("emergence_synthesis", payload)
    validation = payload.get("cross_validation", {})

    slug = slugify(topic)
    report_dir = Path("reports")
    decision_dir = Path("database") / "emergence"
    report_dir.mkdir(parents=True, exist_ok=True)
    decision_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{slug}.md"
    decision_path = decision_dir / f"{slug}.json"

    markdown = [
        f"# 三维理念现实涌现方案：{topic}",
        "",
        section("基础目的与激活锚点", synthesis.get("purpose_anchor")),
        section("宏观生态机制", synthesis.get("macro_ecology")),
        section("中观价值回路", synthesis.get("meso_value_loops")),
        section("微观实体矩阵", synthesis.get("micro_object_matrix")),
        section("现实实例化图谱", synthesis.get("instantiated_entity_map")),
        section("理念现实张力", synthesis.get("ideal_reality_tensions") or validation.get("tensions")),
        section("交叉验证矩阵", synthesis.get("validation_matrix") or validation.get("validation_matrix")),
        section("产品定义", synthesis.get("product_definition")),
        section("体验蓝图", synthesis.get("experience_blueprint")),
        section("技术选择", synthesis.get("technical_choices")),
        section("场景激活路径", synthesis.get("activation_plan")),
        section("涌现解决方案", synthesis.get("emergence_solution")),
        section("运行机制", synthesis.get("operating_mode")),
        section("关键实体", synthesis.get("key_entities")),
        section("评估指标", synthesis.get("evaluation_metrics")),
        section("进化回路", synthesis.get("iteration_loop")),
        section("复盘触发器", synthesis.get("retrospective_triggers")),
    ]

    report_path.write_text("\\n".join(markdown), encoding="utf-8")

    stored_payload = {
        "topic": topic,
        "cross_validation": validation,
        "emergence_synthesis": synthesis,
    }
    decision_path.write_text(
        json.dumps(stored_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "written",
                "report_path": str(report_path),
                "decision_path": str(decision_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    "database/README.md": "# 数据持久化\n\n三维理念现实涌现结果会写入 `database/emergence/`。\n",
    "reports/README.md": "# 报告目录\n\nMarkdown 版《三维理念现实涌现方案》会输出到这里。\n",
}
