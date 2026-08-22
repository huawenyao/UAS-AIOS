# 基于 SIO-MMOS/DIKW 的 Agent 世界模型与本体论语义操作层调研报告

> **定位**：用本仓库已有的 SIO-MMOS 与 DIKW 方法，把「Agent 世界模型」「本体论语义操作层」「行业研究进展与设计实现」收成同一条可执行调研—设计—验证链。  
> **调研时点**：2026-08；行业事实覆盖 2018–2026 公开材料。本仓库既有理论见 `docs/THEORY_SYSTEM.md`、`docs/AGI_WORLD_MODEL_UAS.md`、`docs/世界模型/`。  
> **实现锚点**：`scripts/semantic_operation_layer.py`、`schemas/semantic_operation.schema.json`、`examples/semantic-operation-layer/`。

---

## 0. 方法约定与调研边界

### 0.1 为何用 SIO-MMOS/DIKW，而不是另起一套框架

用户要求「使用我的 SIO-MMOS/DIKW 方法体系」。本仓库已经把它落成可操作定义，而不是外部猜测：

| 符号 | 仓库内含义 | 运行时同构 | 主要出处 |
|------|------------|------------|----------|
| **SIO** | Subject–Interaction–Object（主体–交互–客体） | Situation–Intent–Operation（情境–意图–操作） | `wm_theory.md` 主客二元；`AGI_WORLD_MODEL_UAS.md`「主客体—交互—交付」；`.claude/skills/loop-thinking-enhanced` |
| **MMOS** | Multi-level Meta-model Ontology System（多层级元模型–本体–操作系统） | 道/德/势/术/器 × WM L0–L5 × UAS (I,K,R,A,S,G,E,Π) | `THEORY_SYSTEM.md` §二；`wm_system_logic_and_product_stack.md` |
| **DIKW** | Data–Information–Knowledge–Wisdom | 压缩回路（Wisdom→Data）与价值回路（Data→Wisdom）；可延伸为 DIKWP（Purpose） | `THEORY_SYSTEM.md` §4.4；战略文档中的 DIKWP 仪表盘 |

**同构声明**：知识建模用 S/I/O = 主体/交互/客体；Agent 运行时用 S/I/O = 情境/意图/操作。二者不是两套理论，而是同一三元组在「存在」与「执行」两个投影上的表现。若你的私有定义与此有差异，可按下列映射替换，不破坏后文结构：

```
你的 SIO  ⟷  本报告 SIO（Subject|Situation / Interaction|Intent / Object|Operation）
你的 MMOS ⟷  元模型 + 领域模型 + 本体 + 操作模型 + 服务层
你的 DIKW ⟷  数据/信息/知识/智慧（可加 Purpose 为 DIKWP）
```

### 0.2 SIO-MMOS/DIKW 作为调研操作法（不是事后贴标签）

每个研究对象都按同一张卡片拆解，禁止只堆产品名单：

```
SIO 卡片
  S  Situation / Subject   当前世界快照：谁、在什么时空、对什么客体、反馈通道是什么
  I  Intent / Interaction  目标、约束、价值、交互协议（谁对谁施加什么）
  O  Operation / Object    可验证的语义操作：前置、后置、副作用、回滚、工具绑定

MMOS 卡片
  Meta     词汇封闭、公理、分层禁令（事实≠认识≠规范≠价值）
  Model    状态/转移/观测/效用
  Ontology 类、关系、约束、动作类型
  Operation 操作演算表（INGEST/ASSERT/PREDICT/ACT/OBSERVE…）
  Service  API、SDK、策略引擎、审计

DIKW 卡片
  D  覆盖、新鲜、完整、来源
  I  实体解析、模式一致、时间一致
  K  本体一致、规则覆盖、因果可识别
  W  任务成功、约束不破、可审计、可反身
```

### 0.3 调研问题

1. Agent 世界模型在研究与产品上有哪些形态，各自填补认知/执行/知识哪条鸿沟？  
2. 「基于本体论的语义操作层」与 RAG、Function Calling、工作流编排的产品边界在哪里？  
3. 行业 2023–2026 的可落地设计是什么（不是口号）？  
4. 如何用 SIO-MMOS/DIKW 做成可版本化、可门控、可评测的产品？

---

## 1. 执行摘要（关键判断）

1. **世界模型不是「更大的 LLM」。** 它是对环境的可查询、可预测、可干预表征。神经潜变量模型（Dreamer、JEPA、Cosmos）强在控制与生成；符号/本体模型强在审计与写回。企业 Agent 缺的是后者对前者的**类型系统**。  
2. **语义操作层（Semantic Operation Layer, SOL）是产品化的真正切口。** RAG 检索文本；Function Calling 调工具；SOL 把自然语言意图编译为**本体约束的操作**（查询/断言/计划/执行），并强制前置条件、权限、审计、回滚。Palantir Ontology 的 Action Types、Salesforce Agentforce 的 grounded actions、MCP 的 tool/resource 协议，都在逼近这一层，但完整程度不同。  
3. **LLM 是软世界模型，本体是硬骨架。** 参数记忆不可审计、易幻觉；本体提供身份同一性、引用完整性、操作演算。正确架构是：LLM 当编译器与规划器，本体当类型系统，图/时序库当状态，策略引擎当门控。  
4. **产品化必须走「只读 → 建议 → 受控写回 → 有限自治」。** 直接让 Agent 写 ERP 是失败模式。DIKW 成熟度应成为发布门槛，而不是事后报表。  
5. **本仓库已有理论与占位，缺的是 SOL 作为一等产品模块。** 世界模型五维、L0–L5 操作表、G 层治理已经写清；本报告把它们收成 SIO 运行时与可运行参考实现。

---

## 2. SIO-MMOS/DIKW 形式化（调研坐标系）

### 2.1 世界快照与 SIO 实例

沿用 `wm_system_logic_and_product_stack.md` 的世界快照：

\[
\mathcal{W} = (O, S, M, V)
\]

- \(O\)：客观子结构（实体、时空、事件、关系）  
- \(S\)：主观子结构（意图、认知、实践、反馈）  
- \(M\)：元数据（schema 版本、域、租户）  
- \(V\)：认识论包裹（证据、置信、视角）

一次 Agent 回合是一个 **SIO 实例**：

\[
\text{SIO} = (\Sigma, \Iota, \Omega)
\]

| 分量 | 定义 | 从 \(\mathcal{W}\) 投影 |
|------|------|-------------------------|
| \(\Sigma\) Situation | 任务相关的世界切片 | \(\Pi_{\text{task}}(\mathcal{W})\)：主体清单、客体状态、约束、不确定度 |
| \(\Iota\) Intent | 目标 + 成功度量 + 硬约束 + 期限 + 可接受风险 | \(S.\text{Intention}\) 经 G 层规范化后的可计算目标 |
| \(\Omega\) Operation | 有类型的操作序列 \(\sigma_1;\sigma_2;\ldots\) | L3 操作表的实例化，每步绑定工具/工作流/人审 |

**公理 SIO-A1（主客锚定）**：\(\Iota\) 与 \(\Omega\) 中凡指向世界内容的字段，必须解析为 \(O\) 中已有 id，或显式 `pending_resolution`。禁止静默悬空引用。  
**公理 SIO-A2（预测与事实分离）**：`PREDICT`/`SIMULATE` 的结果不得自动写入 \(O\)；合流必须经 `OBSERVE` 或门控 `ASSERT`。  
**公理 SIO-A3（操作类型封闭）**：\(\Omega\) 只能实例化已注册的动作类型；LLM 不得发明未登记的副作用。

### 2.2 MMOS：五层元模型（与道德势术器对齐）

```
道  Meta-model     词汇、公理、分层禁令（事实/认识/规范/价值）
德  Domain Model   价值函数、目标、允许集、组织规范
势  Ontology       主客体、关系、差异矩阵、博弈结构
术  Operation      策略、计划、语义操作 DSL
器  Service        Runtime、API、SDK、连接器、UI
```

这就是 **MMOS**：不是又一个知识图谱产品名，而是「多层级模型如何被本体约束、再被操作服务化」。缺少任何一层，都会退化为 RAG 或裸 Function Calling。

### 2.3 DIKW 双向回路（作为能力与发布轴）

| 层 | 内涵 | Agent 世界模型对应 | 语义操作层对应 | 发布门槛示例 |
|----|------|--------------------|----------------|--------------|
| **D Data** | 原始感知、日志、文档、传感器 | 观测流、事件日志 | INGEST | 关键源覆盖 ≥ 约定 SLA |
| **I Information** | 结构化事实、实体、时间 | 规范化状态、实体解析 | ASSERT（待确认） | 实体解析准确率、schema 通过率 |
| **K Knowledge** | 本体、规则、因果、技能 | 类/关系/转移/约束 | QUERY / PLAN 的类型检查 | SHACL/规则零致命冲突 |
| **W Wisdom** | 目标权衡、治理、反身 | 策略、价值、演化 | ACT 门控 + 评估 + 回滚 | 约束违反率、审批漏过率、收益指标 |

压缩回路（问题求解）：Wisdom → Knowledge → Information → Data → 现实。  
价值回路（能力进化）：现实 → Data → Information → Knowledge → Wisdom。  
E 层演化必须同时走两向，否则系统会「内部自洽但与现实脱钩」。

### 2.4 与 UAS-AIOS 的映射

| SIO-MMOS/DIKW | UAS 层 | 工程落点 |
|---------------|--------|----------|
| Intent \(\Iota\) | I 意图 | 目标规范化、约束抽取 |
| Ontology / Knowledge | K 知识 | Domain Pack、OWL/JSON Schema、法则库 |
| Runtime of \(\mathcal{W}\) | R 运行时 | 状态存储、投影、仿真 |
| Operation \(\Omega\) | A Agent 编织 | 规划器、工具绑定、多 Agent |
| Tool / System bindings | S 系统网格 | OpenAPI、MCP、工作流、ERP 写回 |
| Wisdom / Policy | G 治理 | RBAC/ABAC、审批、审计、OPA/Cedar |
| DIKW 价值回路 | E 演化 | 漂移检测、evolveApply、评测基线 |
| 操作协议 | Π 协议栈 | SIO JSON、MCP、A2A、输出契约 |

---

## 3. Agent 世界模型全景

### 3.1 定义（避免三种常见偷换）

**Agent 世界模型** = 对环境的可学习 / 可查询 / 可推理表征，使 Agent 能预测、规划、仿真、评估与（在门控下）行动。

它回答四件事：世界里有什么、如何变化、何为价值、能做什么。  
它**不是**：更大的聊天模型、更长的上下文窗口、或单纯的向量库。

形式最小集：

\[
(W, A, T, Z, R, G, C)
\]

状态 \(W\)、动作 \(A\)、转移 \(T(W'|W,A)\)、观测 \(Z\)、奖励/效用 \(R\)、目标 \(G\)、约束 \(C\)。  
企业场景还必须加：实体关系、事件、因果、时序、权限、证据。

### 3.2 八条技术路线（SIO-MMOS/DIKW 扫描）

| 路线 | 世界模型形态 | S 情境 | I 意图 | O 操作 | 本体角色 | DIKW 短板 | 产品化启示 |
|------|--------------|--------|--------|--------|----------|-----------|------------|
| 1 神经潜变量 | RSSM/Dreamer/TD-MPC | 隐状态 | 奖励最大化 | 连续/离散控制 | 弱/无 | K/W 不可审计 | 作仿真器，外挂本体接口 |
| 2 视频/生成式 | GAIA-1/2、Sora 类、Cosmos | 像素未来 | 场景描述 | 生成轨迹 | 弱接地 | I 缺身份同一性 | 作 What-if 与数据合成 |
| 3 表征预测 JEPA | V-JEPA / V-JEPA 2 | 潜空间未来 | 物理任务 | 零样本规划 | 无符号层 | K 不可查询 | 具身感知骨干，不替代企业本体 |
| 4 价值等价模型 | MuZero | 搜索树 | 胜率/回报 | 规划 | 无 | 不可解释 | 封闭规则域，难进 ERP |
| 5 LLM 软世界模型 | ReAct、Reflexion、Generative Agents | 文本记忆 | 自然语言目标 | 工具/对话 | 易幻觉 | D→K 无硬约束 | 必须加 grounding |
| 6 代码/程序世界模型 | Voyager、WorldCoder、Code-as-Policies | 程序状态 | 技能库 | 代码执行 | 类型≈本体 | 沙箱与副作用 | 技能即操作类型 |
| 7 知识图谱/本体 | Cyc、OWL、GraphRAG、企业 Ontology | 图快照 | SPARQL/目标 | 类型化 Action | 一等公民 | 构建成本 | **企业 SOL 主干** |
| 8 混合神经符号 | LLM+PDDL、OAG、本报告 SOL | 图+向量+隐变量 | 约束目标 | 编译后的操作 | 类型系统 | 集成复杂 | **推荐主路径** |

### 3.3 代表性研究（按设计实现，不只列名字）

**控制/想象类**

- Ha & Schmidhuber, *World Models* (2018)：VAE + MDN-RNN + 控制器；在「梦」中训练策略。实现要点：观测压缩 → 动力学 → 策略；无本体。  
- PlaNet / Dreamer / DreamerV2 / **DreamerV3**（Hafner 等；DreamerV3 于 2025 年 *Nature* 发表）：RSSM 学潜动力学，Actor-Critic 在想象中优化；V3 用固定超参覆盖 150+ 任务，并在 Minecraft 从零收集钻石。实现要点：离散潜变量、归一化与损失平衡、想象 rollout。  
- TD-MPC / TD-MPC2：可微 MPC + 世界模型，短视界轨迹优化。  
- MuZero（2019）：不建显式环境模型，学价值等价模型做 MCTS。对「规则封闭、奖励清晰」强，对「企业对象+权限」弱。

**表征/具身类**

- LeCun (2022) JEPA 路线：预测表征而非像素，降低生成负担。  
- **V-JEPA 2**（Meta，约 2025）：约 12 亿参数，视频潜空间预测，支持陌生环境零样本机器人规划，并放出物理推理基准。实现要点：非生成式、动作条件预测、规划在潜空间。  
- SayCan / Inner Monologue / RT 系列：语言提议 + 价值/可执行性过滤。本体在此表现为 **affordance 清单**（哪些技能在当前状态可执行）。  
- NVIDIA **Cosmos**（开放物理 AI 世界模型族，演进至 Cosmos 3）：场景理解、世界生成、动作预测；并出现 World-Action Model（视频骨干与动作头联合，如 DreamZero、Cosmos Policy）。实现要点：大规模视频预训练 → 动作微调；仿真（Omniverse）作测试台。  
- Wayve **GAIA-1 / GAIA-2**：驾驶生成式世界模型，用于安全关键场景合成。实现要点：动作/语言条件视频；评价在分布外场景，而非聊天质量。

**Agent/文本类**

- ReAct (Yao 等, 2023)、Toolformer、HuggingGPT：推理与工具交错。  
- Reflexion、Generative Agents（Park 等, 2023）：记忆流 + 反思 + 规划；「记忆」仍是文本，不是类型化状态。  
- Voyager (Wang 等, 2023)：技能库 + 自动课程 + 代码执行；**技能签名**已接近操作类型，但缺企业级权限与写回。  
- MemGPT / Letta、Zep/Graphiti、Mem0：分层记忆或时序图记忆。产品价值在 I/K 层的持续性，不自动等于 Wisdom。

**符号/本体/神经符号**

- 经典：BDI、AgentSpeak、Situation Calculus、PDDL、Cyc、OWL 2 / RDF / SPARQL / SHACL。  
- GraphRAG（Microsoft Research, 2024）：从文本抽实体关系，Leiden 社区层次 + 社区摘要；查询分 Global / Local / DRIFT。实现要点：索引贵、适合全局问题；**默认只读**，不是操作层。  
- LLM+PDDL / 约束解码：LLM 出草图，经典规划器或 JSON Schema 做合法化。  
- Palantir **OAG（Ontology Augmented Generation）**：用对象、链、动作、逻辑函数接地，而不是段落检索。这是目前最接近「企业世界模型 + 语义操作」的商业实现。

### 3.4 世界模型组件清单（做产品时的拆件）

| 组件 | 职责 | DIKW | 缺了会怎样 |
|------|------|------|------------|
| 感知编码器 | 文档/API/传感器 → 候选事实 | D→I | 垃圾进、幻觉出 |
| 实体解析 | 身份同一性 | I | 重复对象、错误写回 |
| 本体索引 | 类/关系/约束 | K | 无法类型检查 |
| 状态存储 | 图 + 时序 + 向量 | I/K | 无单一事实来源 |
| 动力学/预测头 | \(T(W'|W,A)\) | K | 不能 What-if |
| 规划器 | \(\Iota \to \Omega\) | K→W | 只会聊天 |
| 执行器 | 绑定工具/工作流 | 器 | 计划停在纸面 |
| 门控/治理 | allow/deny/escalate | W | 不可上生产 |
| 评估器 | 预测误差、约束、业务 KPI | 全层 | 无法反身 |

### 3.5 评测：不要只用「任务成功率」

| 族 | 指标 | 说明 |
|----|------|------|
| 预测 | 重构误差、rollout 时域、校准 ECE | 神经 WM 主指标 |
| 接地 | 有证据断言占比、实体链接 F1 | 防脱钩 |
| 本体 | SHACL 通过率、引用完整性、规则冲突数 | MMOS L1 |
| 计划 | 计划合法率、第一步成功率、约束违反率 | SOL 核心 |
| 行动 | 写回成功率、回滚率、审批时延 | 生产 |
| 智慧 | 目标达成、成本、风险、各主客体可接受度 | W / 价值闭环 |
| Agent 基准（参考） | GAIA、WebArena、OSWorld、SWE-bench、τ-bench、AgentBench | 测工具使用，不测本体忠实度 |

行业缺口：**几乎没有「语义忠实度 + 写回安全」基准。** 产品必须自建：本体单测、回放、反事实、对抗性越权。

---

## 4. 基于本体论的语义操作层：产品化方案

### 4.1 定义与边界

**语义操作层（SOL）** 位于 LLM/Agent 与底层系统之间：把自然语言意图编译为**本体约束的动作/查询/策略**，统一 schema，支持权限、审计、可验证执行。

| 相邻能力 | 做什么 | 不做什么 | 与 SOL 关系 |
|----------|--------|----------|-------------|
| 向量 RAG | 找相似段落 | 不保证对象身份，不写系统 | SOL 的 D/I 辅助通道 |
| GraphRAG | 从文本建图并回答全局问题 | 默认不定义 Action | SOL 的只读子模式 |
| Function Calling | 调工具 | 工具签名 ≠ 企业对象生命周期 | SOL 的器层绑定 |
| 工作流引擎 | 跑预定 BPMN | 不理解世界状态 | SOL 编译结果可下发到工作流 |
| 数字孪生/仿真 | 预测物理/流程 | 不一定有权限模型 | SOL 的 PREDICT 后端 |
| Palantir Ontology | 对象+链+动作+安全的一体化 | 重平台、非 OWL 推理 | SOL 的商业对标 |

Palantir 自己强调：Ontology **不是**薄语义层；它是 Data + Logic + Action + Security 的四位一体。本报告同意这一产品判断，但把「Language / Engine / Toolchain」收成 MMOS，并用 SIO 作为每次调用的交易单元。

### 4.2 产品模块（可售卖的切分）

```
┌─────────────────────────────────────────────────────────────┐
│                     Semantic Operation Layer                │
├──────────┬──────────┬──────────┬──────────┬─────────────────┤
│ Ontology │ Grounding│ Compiler │ Planner  │ Guardrail       │
│ Hub      │ Engine   │ (SIO)    │          │ + Policy        │
├──────────┼──────────┼──────────┼──────────┼─────────────────┤
│ State    │ Action   │ Observa- │ Eval     │ SDK / API /     │
│ Store    │ Registry │ bility   │ Harness  │ Low-code Canvas │
└──────────┴──────────┴──────────┴──────────┴─────────────────┘
```

| 模块 | 用户可感知能力 | 最低实现 |
|------|----------------|----------|
| Ontology Hub | 类/关系/动作/规则的版本化编辑、导入 OWL/JSON Schema | Git + JSON Schema |
| Grounding Engine | 实体链接、文档抽取、API 对齐 | 规则 + LLM 抽取 + 人工确认 |
| SIO Compiler | NL → SIO 计划；失败时返回类型错误而非散文 | JSON Schema + 校验器 |
| Planner | 在合法操作上搜索/生成计划 | LLM 规划 + 规则过滤；可加 PDDL |
| Guardrail | 只读/建议/需审批/禁止；预算；PII | 策略函数 + 审批单 |
| State Store | 当前对象图、双时态、向量 | 图库或 Postgres JSONB + 向量 |
| Action Registry | 每个动作的 IO、前置、效果、幂等、工具绑定 | 注册表 JSON |
| Observability | trace、图 diff、操作日志、反事实 | OpenTelemetry + 事件日志 |
| Eval Harness | 本体单测、回放、对抗越权 | pytest + 金样本 |
| SDK/Canvas | `plan/query/act/explain`；低代码画布 | REST + Python SDK |

### 4.3 核心数据模型（操作类型）

```json
{
  "id": "replenishment.create_purchase_order",
  "object_types": ["SKU", "Warehouse", "Supplier", "PurchaseOrder"],
  "input_schema": {
    "sku_id": "id",
    "warehouse_id": "id",
    "supplier_id": "id",
    "quantity": "positive_int"
  },
  "precondition": ["stockout_risk > threshold", "budget_remaining >= estimated_cost"],
  "effect": ["PurchaseOrder.status=created", "expected_on_hand += quantity"],
  "side_effects": ["notify.procurement", "writeback.erp"],
  "risk": "medium",
  "approval": true,
  "idempotency_key": "sku_id+warehouse_id+day",
  "rollback": "cancel_purchase_order"
}
```

这对应 Palantir 的 Action Type，也对应本仓库 L3 操作表的领域实例化。W3C OWL 可以描述类与约束，但**动作的权限与写回**必须作为一等对象，不能只靠推理引擎。

### 4.4 API 设计（SIO 为交易单元）

```
POST /v1/operations/plan
POST /v1/operations/simulate
POST /v1/operations/execute
GET  /v1/operations/{id}
GET  /v1/operations/{id}/explain
POST /v1/query
POST /v1/world/ingest
GET  /v1/world/snapshot
```

`plan` 请求最小集：

```json
{
  "situation_ref": "wm:warehouse-A:2026-08-15T00:00:00Z",
  "intent": {
    "goal": "两周内将 A 仓缺货风险降至 5% 以下",
    "constraints": {"max_budget": 500000, "deadline": "2026-08-29"},
    "success_metric": "stockout_risk_p90 < 0.05"
  },
  "mode": "plan"
}
```

`plan` 响应必须包含：SIO 三元组、校验报告、逐步操作、风险与审批点、图 diff 预览。禁止只返回一段自然语言。

### 4.5 安全、权限、审计（Wisdom 层不可选）

| 控制 | 机制 |
|------|------|
| 身份 | 主体（人/Agent/服务）作为 Ontology 对象，非提示词角色扮演 |
| 授权 | 对象级 ABAC：谁能对哪类对象执行哪类 Action |
| 模式 | `query` / `simulate` / `suggest` / `execute` 权限分离 |
| 高风险 | 金额、不可逆、跨租户、PII → escalate |
| 审计 | append-only：谁、何时、凭何证据、图 diff、模型版本、提示版本 |
| 回滚 | 每个写操作声明补偿动作；不能补偿则禁止自治 |
| 数据 | 租户隔离、最小化投影、推理链路不落敏感原文 |

公理对应：L3-A1 预测与事实分离；L4-A1 单调审计；SIO-A3 操作类型封闭。

### 4.6 DIKW 数据流（产品管道）

```
Data        事件流 / 文档 / API / 传感器
  │ INGEST + 清洗
Information 实体、事实、有效时间、来源
  │ 实体解析 + schema
Knowledge   本体、规则、技能、因果（已承诺事实 vs 假设）
  │ 规划 + 门控
Wisdom      目标权衡、策略、批准的 ACT、反身更新
  │ OBSERVE
Data        新观测（回路）
```

**与 RAG 的关键差别**：RAG 在 Information 层把文本塞进上下文；SOL 在 Knowledge 层做类型检查，在 Wisdom 层做是否允许改世界的决定。

### 4.7 产品化阶段

| 阶段 | 范围 | 退出标准（DIKW） |
|------|------|------------------|
| 0 边界 | 一个域、5–8 个核心对象、只读 | 主客体清单与反馈通道书面化 |
| 1 本体骨架 | 20–100 类、50–200 关系、10 动作类型 | K：一致性检查全绿 |
| 2 只读 SOL | `/query` + `/explain` | I：实体链接达标；W：零写操作 |
| 3 建议模式 | `/plan` + `/simulate`，人审执行 | 计划合法率 ≥ 约定；约束违反 = 0 进入执行 |
| 4 受控写回 | 低风险 Action 自动，中高风险审批 | 回滚可用；审计可检索 |
| 5 平台化 | 多域包、多租户、Eval 看板、Domain Pack 市场 | WM-CMM ≥ 3（动态级） |

商业上不要从第 4 阶段卖「自主 Agent」。先卖「决策级数字孪生 + 建议」，再卖「受控动作」。

---

## 5. 行业研究进展与设计实现扫描

### 5.1 研究侧：2023–2026 的结构性变化

1. **世界模型从 RL 论文走向物理 AI 基础模型。** DreamerV3 证明「一个算法、固定超参、多样控制」；Cosmos / GAIA-2 / V-JEPA 2 把世界模型做成可预训练资产。含义：具身侧会有「世界模型 API」（生成、预测、规划），企业侧仍缺对象与权限。  
2. **World-Action Model 出现。** 视频扩散骨干与动作 token 联合去噪（DreamZero、LingBot-VA、Cosmos Policy 等）。含义：操作开始进入生成模型内部，但这些操作是关节/控制，不是 `create_purchase_order`。  
3. **Agent 协议层爆发。** Anthropic **MCP**（2024-11）把工具与资源标准化；Google **A2A**（2025-04，后交 Linux Foundation）把 Agent 间任务委派标准化。含义：器层互操作在收敛，**语义层仍是各家私有本体**。  
4. **图谱增强从检索走向层次摘要。** GraphRAG 证明全局问题需要社区结构，不只是 top-k 向量。含义：只读 K 层有开源配方；写操作仍缺。  
5. **企业竞争从「模型」转向「语义层」。** Palantir Ontology、Salesforce Data Cloud/Agentforce、Microsoft Graph/Fabric Copilot、Neo4j GraphRAG，都在争「对象世界谁说了算」。

### 5.2 产品侧对照表

| 系统 | 世界模型形态 | 本体/语义角色 | 操作/写回 | 治理 | 对 UAS/SOL 的启示 |
|------|--------------|---------------|-----------|------|-------------------|
| Palantir Foundry + AIP | 决策中心数字孪生 | Object/Link/Property；非 OWL | Action Types + writeback | 对象级安全、审批 | **最完整对标**：Language+Engine+Toolchain |
| Salesforce Agentforce | CRM/Data Cloud 对象图 | DMO 预置企业本体 | Invocable / Flow / MCP（路线图） | Einstein Trust Layer | 预置本体降低冷启动 |
| Microsoft Graph + Copilot Studio | 工作图 + 连接器 | 弱意见本体，开发者自建 | Topics/Actions/Connectors | 租户与 DLP | 覆盖广，语义要自建 |
| AWS Bedrock Agents + Neptune | 工具+记忆+图分析 | 可选图 | 工具调用 | IAM | 云原组件装，缺统一对象模型 |
| Neo4j GraphRAG / Aura | 属性图+向量 | 开发者模型 | 查询为主，Action 需自建 | 角色 | 好的 K 存储，不是完整 SOL |
| Stardog / GraphDB | RDF + 推理 + 虚拟图 | OWL/SHACL 强 | SPARQL Update 需自管 | 企业 ACL | 适合强推理域（金融/生命科学） |
| LangGraph / Semantic Kernel / AutoGen | 状态图/插件/多 Agent | 通常无 | 工具 | 弱 | 编排层，需外挂本体 |
| Letta / Zep / Mem0 | 记忆世界 | 时序图或块 | 记忆读写 | 弱 | 补 I 层持续性 |
| NVIDIA Cosmos + Omniverse | 物理世界模型 | 场景/传感器本体 | 仿真与策略 | 安全评测台 | 阶段 2（现实世界）的器 |
| Open-source GraphRAG | 文本派生 KG | 抽取出的类型不稳定 | 只读 | 无 | 加速 D→K，不能当 Action 注册表 |

### 5.3 设计实现要点（可抄的，不是口号）

**Palantir Ontology（商业参考实现）**

- Language：对象、链、属性、动作、自动化、逻辑函数。  
- Engine：可扩展读（SQL、订阅）与写（事务、批量、CDC 镜像）。  
- Toolchain：OSDK、Workshop、AIP Logic。  
- OAG：LLM 先碰对象与逻辑工具，再生成；CoT 对用户可见。  
- 关键产品决策：不走开放世界 OWL 推理，而走**受治理的共享词汇 + 动作**。对多数运营工作流，这个赌注是对的。

**MCP / A2A（协议参考实现）**

- MCP：Agent ↔ 工具/资源（垂直）。JSON-RPC，stdio 或 Streamable HTTP。  
- A2A：Agent ↔ Agent（水平）。Agent Card、任务委派。  
- SOL 应把每个 Action Type **投影为 MCP tool**，把每个 Domain Agent **投影为 A2A Agent Card**，但权限仍以本体对象为准，而不是以 tool 名为准。

**GraphRAG（只读 K 层参考实现）**

- 切块 → LLM 抽取实体关系 → 图 → Leiden 社区 → 社区摘要 → 查询时选 Global/Local。  
- 成本：索引贵；类型漂移：抽取类型不等于受管本体。  
- 接入 SOL 的正确方式：抽取结果进入 **待确认池**（ASSERT 门控），不得直接成为 Action 的前置事实。

**神经世界模型（PREDICT 后端参考实现）**

- Dreamer 式：学 \(z_{t+1}=f(z_t,a_t)\)，在潜空间做策略。  
- JEPA 式：预测表征，规划更便宜。  
- 生成式：像素/视频 rollout，贵，适合展示与安全场景挖掘。  
- 接入 SOL：一律标为 `PREDICT`，输出分布或轨迹，**禁止**直接改 `PurchaseOrder`。

### 5.4 开源与标准栈（选型矩阵）

| 需求 | 优先选项 | 何时不选 |
|------|----------|----------|
| 形式本体 + 约束 | OWL 2 + SHACL + JSON-LD；Protégé；pySHACL | 运营域只需属性图时不要一上来 OWL |
| 图遍历性能 | Neo4j、FalkorDB | 需要 OWL 推理时不够 |
| RDF 推理 | Jena、GraphDB、Stardog | 要超低延迟写回时偏重 |
| 云托管图 | Amazon Neptune、Azure 图能力 | 避免单云锁定可上开源 |
| 向量 | pgvector、Qdrant、FAISS | 单独向量库不能当对象源 |
| 时序/事件 | Kafka + 双时态表 | 只用聊天日志当状态 |
| 规划 | JSON Schema 约束解码 → PDDL/Fast Downward → 优化器 | 纯 LLM 计划无校验 |
| 策略 | OPA、Cedar、自研 ABAC | 提示词里写「你必须遵守政策」 |
| Agent 编排 | LangGraph、Semantic Kernel、AutoGen | 不要让编排框架拥有本体 |
| 评测 | 自建金样本 + 约束检查；参考 GAIA/OSWorld | 只看 BLEU/「看起来对」 |

---

## 6. 参考架构与端到端设计实现

### 6.1 运行时控制面

```
NL / Event / API
        │
        ▼
   Intent Normalizer  ──→  I 层目标+约束（JSON Schema）
        │
        ▼
   Situation Projector ──→ 从 WM 取任务切片（主客体、约束、证据）
        │
        ▼
   SIO Compiler (LLM as compiler, Ontology as type system)
        │  候选操作 ∈ Action Registry
        ▼
   Validator (引用完整、前置条件、SHACL/规则、预算)
        │
        ├─ fail → 类型错误 + 修复建议（不执行）
        ▼
   Policy Gate (allow / deny / escalate)
        │
        ├─ simulate → PREDICT 后端（规则 / 优化器 / 神经 WM）
        ├─ execute → Tool / MCP / 工作流 / 人
        ▼
   OBSERVE → 更新 W → DIKW 度量 → 反身（E 层）
```

### 6.2 参考实现（本仓库）

可运行编译器：`scripts/semantic_operation_layer.py`  
契约：`schemas/semantic_operation.schema.json`  
场景：`examples/semantic-operation-layer/`（库存补货）

场景的 SIO：

| 分量 | 内容 |
|------|------|
| S | SKU-A 在仓 W1 的库存、在途、预测需求、预算余额、缺货风险 |
| I | 14 天内把缺货风险压到 5% 以下，采购预算不超过 50 万 |
| O | `query.risk` → `create_purchase_order`（需审批）→ `notify.procurement` |

DIKW：

| 层 | 本场景 |
|----|--------|
| D | 销售流水、库存快照、供应商交期 |
| I | `InventoryPosition`、`DemandForecast` 规范化事实 |
| K | ABC、提前期分布、再订货点、本体约束 |
| W | 新闻贩约束 + 预算 + 审批；禁止无审批写 ERP |

实现刻意**不调用 LLM**：先证明类型系统、门控、仿真、审计在没有模型时也能闭环。LLM 只应替换 Compiler 的「候选生成」，不应替换 Validator。

### 6.3 与本仓库世界模型栈的衔接

| 已有资产 | SOL 用法 |
|----------|----------|
| `schemas/world_model.schema.json` | Situation 的主客体占位 |
| `schemas/world_model_v2.schema.json` | 法则库、降维、意图守恒 |
| `docs/世界模型/wm_system_logic_and_product_stack.md` | L0–L5 公理；SOL 实现 L3 操作表 |
| `scripts/world_model_runtime.py` | 法则/降维运行时；SOL 作为其执行前端 |
| Domain Pack / G 层 | 行业本体与审批 |
| MCP 类协议（Π） | Action 的器层投影 |

---

## 7. 风险、反模式与最佳实践

| 风险 | 症状 | 对策 |
|------|------|------|
| 本体过度工程 | 上线前 6 个月还在画 OWL | 先 5–8 个核心对象、10 个动作 |
| Schema 膨胀 | 类比表还多 | 领域包治理、弃用策略 |
| LLM 幻觉操作 | 捏造字段/动作 | 封闭 Action Registry + Schema 校验 |
| GraphRAG 类型漂移 | 每次抽取类型不同 | 映射到受管本体，进待确认池 |
| 预测写成事实 | 仿真结果进 ERP | SIO-A2 / L3-A1 |
| 提示词治理 | 「请遵守政策」 | 策略引擎，失败默认 deny |
| 不可逆动作自治 | 无法回滚的自动采购 | 审批 + 补偿动作 |
| 评测虚高 | 只测问答 | 计划合法率、越权测试、回放 |
| 隐私 | 全量图谱进提示词 | 最小化投影、对象级 ACL |
| 成本 | 全量 LLM 抽图 | 规则/NLP 预抽 + LLM 补全 |

**反模式**：把 LangGraph 当世界模型；把向量库当本体；把 MCP tool 名当权限边界；把 Dreamer 潜状态直接映射成财务对象。

---

## 8. 结论与路线图

行业正在把「世界模型」和「企业本体」从两边同时做厚：一边是可预训练的物理/视频世界模型，一边是可写回的对象–动作系统。**语义操作层是两边的接缝。** SIO-MMOS/DIKW 给出接缝上的交易单元（SIO）、分层禁令（MMOS）和发布轴（DIKW）。

建议本仓库的工程顺序：

1. 把 SOL 作为 K/R/A 之间的稳定接口（已提供 schema 与参考编译器）。  
2. 选一个 Domain Pack（补货 / 客服 / 销售 OS）走完 query→simulate→escalate。  
3. 将 Action 投影为 MCP tools，Agent 投影为 A2A cards，权限仍在本体。  
4. 神经世界模型只作为 PREDICT 插件接入。  
5. 用 DIKW 看板作为发布门槛，而不是演示文稿。

---

## 附录 A. SIO 调研卡片模板

```
对象：<论文/产品/模块>
S：它把什么当作世界状态？主客体是谁？
I：优化什么？硬约束是什么？谁的价值？
O：允许哪些操作？如何校验？如何回滚？
MMOS：元模型/模型/本体/操作/服务各在哪一层？缺哪层？
DIKW：D/I/K/W 哪层已闭合？哪层在演戏？
可吸收：<一条工程决策>
应规避：<一条反模式>
```

## 附录 B. 文献与产品追踪清单（后续可续刷）

DreamerV3 (Nature 2025)；V-JEPA 2；NVIDIA Cosmos / World-Action Models；Wayve GAIA-2；GraphRAG (arXiv 2404.16130)；Anthropic MCP (2024-11)；Google A2A (2025-04)；Palantir Ontology Architecture Center；Salesforce Agentforce + Data Cloud；Neo4j GraphRAG；OSWorld；τ-bench；GAIA agent benchmark。

## 附录 C. 本报告与既有文档的分工

| 文档 | 分工 |
|------|------|
| `THEORY_SYSTEM.md` | 元方法论与 DIKW 双向回路 |
| `AGI_WORLD_MODEL_UAS.md` | 双轨 AGI 与五维 WM |
| `wm_theory.md` / `wm_system_logic_and_product_stack.md` | 主客本体与 L0–L5 |
| `world_model_research.md` 等 | 早期产品形态推演 |
| **本文** | 用 SIO-MMOS/DIKW 收束行业进展，并给出 SOL 产品与参考实现 |
| `AWM_PRODUCT_DEFINITION_CUSTOMERS_SCENARIOS_UX.md` | 把世界模型定义为可售卖产品：客户、场景、SKU、竞争与 UX |

---

*版本：2026-08-15。行业条目随公开资料更新；公理与 SIO 交易单元应保持稳定。*
