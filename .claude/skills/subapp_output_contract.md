---
name: subapp-output-contract
description: 定义Agent在方案设计阶段必须输出的结构化JSON格式。用于：(1) 规范输出格式 (2) 与render脚本兼容 (3) 映射到configs配置 (4) 验证方案完整性
---

# UAS Sub App 方案输出契约

## 用途

本契约定义 Agent 在「方案设计」阶段必须输出的结构化 JSON 格式。该格式与 `scripts/render_uas_plan.py` 的 payload 兼容，并扩展支持生产阶段的定制需求。

## 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `topic` | string | 业务议题名称 |
| `intent_model` | object/array | 意图模型，至少包含 goal, constraints, target_audience, success_metrics |
| `knowledge_assets` | array | 知识资产清单，如 workflow_config, swarm_agents, skills 列表 |
| `agent_fabric` | array | Agent 编织，每个 agent 的 id, name, dimension, stance, mission, deliverable |
| `governance_controls` | array | 治理控制，如 audit_required, permission_model, human_checkpoints |
| `evolution_loop` | array | 演化回路，如 validation_metrics, iteration_path, feedback_channels |

## 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `runtime_topology` | array | 运行时拓扑，context_injection, state_isolation 等 |
| `system_mesh` | array | 系统网格，需接入的业务系统、数据系统、工具 |
| `evaluation_metrics` | array | 评估指标 |
| `delivery_plan` | array | 交付计划，阶段与里程碑 |

## 示例

```json
{
  "topic": "跨境电商选品助手",
  "intent_model": {
    "goal": "支持多平台数据聚合与智能选品推荐",
    "constraints": ["ASUI 技术底座", "autonomous_agent 运行时"],
    "target_audience": "跨境电商运营人员",
    "success_metrics": ["选品准确率", "数据覆盖平台数", "响应时效"]
  },
  "knowledge_assets": [
    "configs/workflow_config.json",
    "configs/swarm_agents.json",
    ".claude/skills/selection_protocol.md",
    ".claude/skills/output_contract.md"
  ],
  "agent_fabric": [
    {
      "id": "intent_guard",
      "name": "意图守恒智能体",
      "dimension": "intent",
      "stance": "业务目标监督者",
      "mission": "确保选品始终服务于业务目标",
      "deliverable": "意图激活报告"
    },
    {
      "id": "data_aggregator",
      "name": "数据聚合智能体",
      "dimension": "data",
      "stance": "多平台数据整合者",
      "mission": "聚合各平台商品与销售数据",
      "deliverable": "聚合数据报告"
    },
    {
      "id": "selection_recommender",
      "name": "选品推荐智能体",
      "dimension": "recommendation",
      "stance": "智能选品决策者",
      "mission": "基于规则与模型输出选品建议",
      "deliverable": "选品推荐报告"
    }
  ],
  "governance_controls": [
    "audit_required: true",
    "permission_model: READ_ONLY, WRITE_SAFE, WRITE_RISK",
    "high_risk_requires_human_approval: true"
  ],
  "evolution_loop": [
    "validation_metrics: 选品准确率、用户满意度",
    "iteration_path: intent_activation → governance_check → evolution_plan",
    "feedback_channels: 用户反馈、A/B 测试结果"
  ],
  "system_mesh": [
    "电商平台 API（亚马逊、速卖通等）",
    "ASUI 知识库",
    "数据库（选品历史、用户偏好）"
  ]
}
```

## 与 render_uas_plan.py 的兼容

`scripts/render_uas_plan.py` 接收的 payload 字段：topic, intent_model, knowledge_assets, runtime_topology, agent_fabric, system_mesh, governance_controls, evaluation_metrics, evolution_loop, delivery_plan。

本契约的必填字段覆盖上述核心字段，确保生成的方案可直接用于 render 脚本。

## 与 configs 的映射

| 契约字段 | 映射到的 config |
|----------|-----------------|
| agent_fabric | configs/swarm_agents.json |
| governance_controls | configs/governance_policy.json |
| evolution_loop | configs/evolution_policy.json |
| knowledge_assets | configs/workflow_config.json + .claude/skills/ |
| system_mesh | configs/system_registry.json |
