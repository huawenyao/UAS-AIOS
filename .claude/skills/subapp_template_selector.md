# UAS Sub App 模板选择逻辑

## 技能定位

本技能定义如何根据**世界模型分析输出**选择 sub app 模板。当用户未指定 `--template` 时，Agent 必须基于 `world_model_analysis` 的 `methodology_signals` 进行选择，禁止仅凭关键词匹配。

## 输入

- **world_model_analysis**（来自 subapp_producer_protocol 阶段 2）：含 subjects、objects、methodology_signals
- **可选的 --template**：用户显式指定时跳过本逻辑

## 可用模板

| 模板 ID | 适用场景 | 典型关键词 |
|---------|----------|------------|
| `uas-subapp` | 通用 UAS 标准 sub app | 业务自动化、流程、标准、通用 |
| `selfpaw-swarm` | 多角色博弈、对手盘、蜂群决策 | 多视角、博弈、对手盘、用户/关卡/决策/买单、认知蜂群 |
| `triadic-ideal-reality-swarm` | 理念-现实张力、宏观中观微观 | 理念、现实、宏观、中观、微观、涌现、实例化 |

## 选择规则

### 规则 1：显式指定优先

若用户提供 `--template <id>`，直接使用该模板，不做推断。

### 规则 2：基于 methodology_signals（主规则）

从 world_model_analysis.methodology_signals 读取：
- `multi_agent_game` > 0.6 → `selfpaw-swarm`
- `ideal_reality_tension` > 0.6 → `triadic-ideal-reality-swarm`
- `linear_flow` > 0.6 且另两者 < 0.4 → `uas-subapp`
- 混合或同分：取最高分对应模板；同分时优先 selfpaw > triadic > uas-subapp

### 规则 3：基于 subjects 数量与冲突（辅助）

若 methodology_signals 不明确：
- subjects ≥ 3 且存在明显立场冲突 → 倾向 `selfpaw-swarm`
- 需「目的激活」「实例化」「涌现」→ 倾向 `triadic-ideal-reality-swarm`

### 规则 4：默认

无法明确推断时，使用 `uas-subapp`，确保产出物满足 UAS Platform 标准。

### 规则 5：关键词匹配（仅作兜底）

当 world_model_analysis 不可用时（如旧版协议），可退化为关键词匹配，但应在报告中标注「未执行世界模型分析」。

## 模板能力差异

| 能力 | uas-subapp | selfpaw-swarm | triadic-ideal-reality-swarm |
|------|------------|---------------|-----------------------------|
| 标准 UAS 八元组 | ✓ | ✓ | ✓ |
| 蜂群五智能体 | - | ✓ | - |
| 三维理念现实 | - | - | ✓ |
| 第一次否定/第二次否定 | - | ✓ | - |
| 目的激活/实例化 | - | - | ✓ |

## 示例

- 「跨境电商选品助手」→ uas-subapp（业务流程、数据聚合）
- 「多角色博弈决策系统」→ selfpaw-swarm（多角色、博弈）
- 「战略规划的理念与现实对齐分析」→ triadic-ideal-reality-swarm（理念、现实）
