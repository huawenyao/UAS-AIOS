---
name: subapp-producer-protocol
description: Agent自主生产UAS sub app的完整流程协议。用于：(1) 创建新的subapp (2) 生成业务应用框架 (3) 规范生产阶段 (4) 校验产出物
---

# UAS Sub App 生产协议

## 技能定位

本协议定义 Agent 自主生产 UAS sub app 的完整流程、阶段、输入输出与约束。Agent 执行 `/createSubApp` 命令时必须遵循本协议。

## 生产阶段

### 1. intent_normalization（意图归一化）

**输入**：用户业务描述（自然语言）

**输出**：结构化意图对象
```json
{
  "topic": "业务议题名称",
  "goal": "核心目标",
  "constraints": ["约束1", "约束2"],
  "target_audience": "目标对象",
  "success_metrics": ["成功标准1", "成功标准2"]
}
```

**规则**：必须明确目标、约束、对象、成功标准，缺一不可。

### 2. world_model_analysis（世界模型分析）

**输入**：意图对象

**输出**：世界模型分析对象（见 `theory_to_template_derivation.md`）
```json
{
  "subjects": [...],
  "objects": [...],
  "feedback_channels": [...],
  "methodology_signals": {
    "multi_agent_game": 0.0,
    "ideal_reality_tension": 0.0,
    "linear_flow": 0.0
  }
}
```

**规则**：
- 必须产出 subjects、objects、feedback_channels、methodology_signals
- methodology_signals 为 0-1 标量，三者之和可大于 1
- 参考 `.claude/skills/theory_to_template_derivation.md`

### 3. template_selection（模板选择）

**输入**：意图对象 + world_model_analysis 输出 + 可选的 `--template` 参数

**输出**：模板 ID（uas-subapp | selfpaw-swarm | triadic-ideal-reality-swarm）

**规则**：
- 若用户指定 `--template`，优先使用
- 否则根据 world_model_analysis.methodology_signals 选模板（见 theory_to_template_derivation）
- 禁止仅凭关键词匹配，必须基于 world_model_analysis

### 4. blueprint_design（方案设计）

**输入**：意图对象 + 模板 ID + UAS 标准知识

**输出**：符合 `subapp_output_contract.md` 的完整方案 JSON

**规则**：
- 必须包含 intent_model, knowledge_assets, agent_fabric, governance_controls, evolution_loop
- 方案中的 workflow、swarm_agents 需与模板结构兼容
- 参考 `docs/UAS_PLATFORM_STANDARD.md`、`docs/ASUI_AUTONOMOUS_AGENT_STANDARD.md`
- 生产报告必须包含 world_model_analysis 与 methodology_signals，便于审计

### 5. asset_generation（资产生成）

**输入**：方案 JSON + 模板 ID + 目标路径

**输出**：完整的 sub app 目录树

**规则**：
1. 调用 `python3 scripts/create_sub_uas_app.py <app_id> --target-root <subapp_root> --template <template_id>`
2. 根据方案覆盖/补充：
   - `configs/workflow_config.json`：步骤、agent、prompt 定制
   - `configs/swarm_agents.json`：agent 角色与使命定制
   - `CLAUDE.md`：业务概述、核心命令
   - `.claude/skills/`：业务协议与输出契约
   - `docs/APP_BLUEPRINT.md`：产品定义

### 6. validate（校验）

**输入**：生成路径

**输出**：校验结果 { status, risks, suggestions }

**规则**：调用 `run_uas_runtime_service.py validate --app-id <app_id>`，或执行 `scripts/evaluate_evolution.py`

### 7. register（注册，可选）

**规则**：创建与运行必须使用相同的 subapp_root。创建到 `projects/` 则运行需 `--projects-root projects`；创建到 `examples/` 则运行需 `--projects-root examples`。二者为同一概念（见 docs/TEMPLATE_PROJECT_RELATIONSHIP.md）。

### 8. report（生产报告）

**输出**：写入 `database/productions/<app_id>_<timestamp>.json`，包含意图、方案、校验结果、生成路径。

## 禁忌

- 禁止生成缺少 `platform_manifest.json`、`governance_policy.json`、`evolution_policy.json` 的 sub app
- 禁止生成 `technical_base` 非 ASUI、`runtime` 非 autonomous_agent 的 sub app
- 禁止在未得到 `--force` 确认时覆盖已存在的项目目录
- 禁止跳过 governance_check、evolution_plan 阶段的设计

## 与 UAS 标准工作流阶段的对应

| 生产阶段 | UAS 标准阶段 |
|----------|--------------|
| intent_normalization | intent_activation |
| world_model_analysis | （理论推演，无直接对应） |
| template_selection | （模板选择，无直接对应） |
| blueprint_design | knowledge_binding, agent_planning, runtime_topology, system_mapping, governance_check, evolution_plan |
| asset_generation | render_report（写入资产生成） |
| validate | governance_check, evolution 评估 |

## 参考文档

- `.claude/skills/theory_to_template_derivation.md`（理论→模板推演）
- `.claude/skills/subapp_template_selector.md`（模板选择细则）
- `docs/UAS_PLATFORM_STANDARD.md`
- `docs/ASUI_AUTONOMOUS_AGENT_STANDARD.md`
- `asui-cli/src/asui/uas_subapp_template.py`（模板结构）
