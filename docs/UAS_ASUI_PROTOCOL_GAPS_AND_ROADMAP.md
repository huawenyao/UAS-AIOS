# UAS-ASUI 协议化标准与智能化推演的不足与改进路线图

> 理想效果：UAS-ASUI 根据业务目标，从理论原理推演构建起业务场景的闭环智能应用模板；自主演化；模板项目实例化后与用户共同迭代改进；业务层无限进化，交付形式标准化 ASUI 架构，可复用 UAS 运行时。

---

## 一、理想效果 vs 当前状态

| 理想效果 | 当前状态 | 差距等级 |
|----------|----------|----------|
| 根据业务目标，从理论原理推演构建闭环智能应用模板 | 模板选择基于关键词匹配，理论→模板无显式推导链 | 🔴 核心缺失 |
| 自主演化 | 演化引擎产出 suggestions，无自动回写知识 | 🟡 部分实现 |
| 实例化后与用户共同迭代改进 | 无结构化人机协同步骤，无反馈回流 | 🔴 核心缺失 |
| 业务层无限进化 | 演化建议未自动写入 configs/skills | 🟡 部分实现 |
| 交付形式标准化 ASUI，可复用 UAS 运行时 | ✅ 已实现 | ✅ 已对齐 |

---

## 二、协议化标准的不足

### 2.1 理论→模板的推演协议缺失

**理想**：业务目标 → 世界模型维度 → 方法论 → 模板，形成可追溯的推导链。

**当前**：
- `subapp_template_selector.md` 使用关键词匹配（「多角色」「博弈」→ selfpaw；「理念」「现实」→ triadic）
- 无「世界模型五维」「推动—反馈—反身」「主客体」「价值闭环」与模板的显式映射
- 模板为代码中预定义，非理论推导生成

**缺失协议**：
- `theory_to_template_derivation_protocol.md`：定义业务目标如何映射到世界模型维度、如何选择方法论、如何对应模板
- 理论原理与模板的**可验证映射表**：如「主客体博弈明显」→ selfpaw；「理念-现实张力」→ triadic

### 2.2 闭环语义未协议化

**理想**：价值闭环 7 步（输入→模拟→生成→交互→进化→输出→收益）在协议中显式定义，工作流步骤与之对应。

**当前**（见 THEORY_ARCHITECTURE_CONSISTENCY_AUDIT）：
- 输入、生成、输出：有对应
- 模拟：无
- 交互（人机协同）：无
- 进化：有 evolution_plan，但与 WM 未挂钩
- 收益：无

**缺失协议**：
- `value_loop_protocol.md`：7 步与 workflow step 的映射，标明哪些已实现、哪些为占位
- `evolution_phase_protocol.md`：推动—反馈—反身与 workflow 阶段的对应（推动≈intent_activation；反馈≈evaluation；反身≈evolution_plan）

### 2.3 世界模型未纳入协议

**理想**：世界模型为一级公民，主客体、反馈通道、推动/阻碍/连接在配置与产出中显式存在。

**当前**：无 world_model 配置，无主客体 schema，无推动/阻碍/连接产出字段。

**缺失**：
- `configs/world_model.json` 的 schema 与占位
- workflow 或报告模板中「主客体视图」「推动/阻碍/连接」的产出要求

---

## 三、智能化推演的不足

### 3.1 业务目标→模板：非理论驱动

**理想推导链**：
```
业务目标「跨境电商选品」
  → 世界模型分析：主体（运营、供应商、平台）、客体（商品、数据）、反馈（销量、转化）
  → 方法论匹配：多主体博弈？理念-现实张力？线性流程？
  → 模板选择：若多主体博弈明显 → selfpaw；若理念落地推演 → triadic；否则 → uas-subapp
```

**当前**：仅「跨境电商选品」→ 关键词无匹配 → 默认 uas-subapp，无世界模型分析步骤。

**改进方向**：
- 在 `subapp_producer_protocol` 中增加 `world_model_analysis` 阶段：产出主体、客体、反馈通道、方法论倾向
- 模板选择基于该阶段输出，而非仅关键词

### 3.2 闭环构建：缺模拟与人机交互

**理想**：模板内嵌「模拟」「人机交互」的可选步骤或占位，支持后续扩展。

**当前**：workflow 为线性执行，无模拟步骤，无 human_review 类型。

**改进方向**：
- 在 workflow_config schema 中增加可选 step 类型：`simulation`、`human_review`
- 在 evolution_policy 中增加 `human_feedback_path`：如 `database/feedback/*.json`，供 evolution 脚本读取

### 3.3 自主演化：仅建议不落盘

**理想**：演化建议自动或半自动回写 configs、skills，驱动下一轮运行改进。

**当前**：
- EvolutionEngine 调用 evaluate 脚本 → 产出 suggestions
- state_store.update_evolution 写入认知状态
- **无**将 suggestions 写回 workflow_config、swarm_agents、skills 的机制

**改进方向**：
- 定义 `evolution_writeback_protocol`：在 governance 允许下，将特定类型的 suggestion 写回知识资产
- 或增加 `evolution_apply` 命令：用户确认后，将 evolution 建议应用到 configs

### 3.4 人机共迭代：无结构化反馈

**理想**：实例化后，用户通过结构化反馈（如评分、修正意见）参与迭代，反馈写入并驱动 evolution。

**当前**：
- human_checkpoints 仅在高风险时暂停
- 无「用户对结果打分」「用户提出修正」的结构化入口
- 无 database/feedback 或等价机制

**改进方向**：
- 增加 `human_review` step 类型：暂停等待用户输入，写入 database/feedback/{topic_slug}.json
- evolution 脚本可读取 feedback，将「用户修正」纳入 suggestions 生成

---

## 四、改进路线图（按优先级）

### P0：协议补全（低代码改动）

| 项目 | 内容 |
|------|------|
| 理论→模板推演协议 | 新增 `.claude/skills/theory_to_template_derivation.md`，定义业务目标→世界模型→方法论→模板的映射规则 |
| 价值闭环映射表 | 在 docs 中增加 7 步与当前 workflow 的映射，标明模拟、人机交互、收益为待建设 |
| 推动—反馈—反身对应 | 在 evolution_policy 或文档中写明三相位与现有步骤的对应 |

### P1：智能化推演增强（中代码改动）

| 项目 | 内容 |
|------|------|
| 生产协议增加 world_model_analysis | 在 subapp_producer_protocol 的 template_selection 前增加世界模型分析阶段，产出主客体、反馈、方法论倾向 |
| 模板选择基于世界模型 | subapp_template_selector 接收 world_model_analysis 输出，按主客体/方法论选模板 |
| human_review step 类型 | workflow schema 支持 human_review；runtime 暂停并写入 database/feedback |

### P2：演化闭环（高代码改动）

| 项目 | 内容 |
|------|------|
| evolution_writeback 协议 | 定义哪些 suggestion 可写回、写回路径、需人工确认的阈值 |
| evolution_apply 命令 | `/evolveApply [topic]` 将已确认的 evolution 建议应用到 configs/skills |
| 反馈回流 | evolution 脚本读取 database/feedback，将用户反馈纳入 suggestions |

### P3：世界模型与收益反哺（战略级）

| 项目 | 内容 |
|------|------|
| world_model 配置占位 | configs/world_model.json schema，含 subjects、objects、feedback_sources |
| 主客体产出 | workflow 或报告模板要求输出主客体视图、推动/阻碍/连接 |
| 收益指标与反哺 | 定义收益指标配置，evolution 可读取并驱动资源分配 |

---

## 五、与理想效果的对应关系

| 理想效果 | 改进项 |
|----------|--------|
| 根据业务目标从理论推演构建闭环模板 | P0 理论→模板协议；P1 world_model_analysis；P1 模板选择基于世界模型 |
| 自主演化 | P2 evolution_writeback；P2 evolution_apply |
| 实例化后与用户共同迭代 | P1 human_review；P2 反馈回流 |
| 业务层无限进化 | P2 演化闭环；P3 世界模型 |
| 交付标准化、复用 UAS 运行时 | ✅ 已满足，保持 |

---

## 六、总结

**当前主要不足**：

1. **协议层**：理论→模板无推演协议；价值闭环、推动—反馈—反身未与 workflow 显式对应；世界模型未纳入配置。
2. **推演层**：模板选择靠关键词，非理论驱动；缺世界模型分析阶段；缺模拟、人机交互步骤。
3. **演化层**：演化仅产出建议，不落盘；无人机结构化反馈入口；无 evolution 回写知识机制。

**已对齐**：交付形式标准化 ASUI、可复用 UAS 运行时。

**实施状态**（见 git 历史）：
- P0：theory_to_template_derivation、value_loop_protocol 已创建
- P1：world_model_analysis、模板选择基于世界模型、human_review/simulation step 已实现
- P2：evolution_writeback_protocol、/evolveApply 命令已创建
- P3：world_model schema、configs/world_model.example.json 已创建
