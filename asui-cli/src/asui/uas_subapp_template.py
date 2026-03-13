"""UAS sub app 标准模板。"""

UAS_SUBAPP_TEMPLATE = {
    "CLAUDE.md": """# UAS Sub App

## 系统概述

本项目是一个基于 UAS-Platform 标准生成的 sub uas app。

默认约束：

- 产品架构遵循 `UAS-Platform = (I, K, R, A, S, G, E, Π)`
- 技术架构默认采用 `ASUI`
- 运行架构默认采用 `autonomous_agent runtime`
- 所有业务实现都必须满足：目标驱动 + 知识驱动 + Agent协作 + 系统执行 + 审计治理 + 演化闭环

## 核心命令

- `/intent [议题]` - 归一化业务目标与场景
- `/design [议题ID]` - 生成业务子应用方案
- `/validate [议题ID]` - 进行偏差校验与评估
- `/evolve [议题ID]` - 生成下一轮进化建议

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/platform_manifest.json` | UAS平台清单与标准约束 |
| `configs/workflow_config.json` | autonomous_agent 工作流 |
| `configs/swarm_agents.json` | Agent 注册与分工 |
| `configs/runtime_config.json` | runtime 配置 |
| `configs/governance_policy.json` | 审计治理与权限策略 |
| `configs/evolution_policy.json` | 目标守恒与进化策略 |
| `configs/system_registry.json` | 专业系统接入清单 |
| `.claude/skills/*.md` | 项目知识与协议 |

## 运行原则

1. 先定义业务意图，再生成子应用
2. 先形成最小可运行闭环，再扩展功能
3. 所有 agent 行为都必须被审计
4. 所有输出都必须可验证、可回滚、可演化
""",
    ".claude/skills/platform_protocol.md": """# UAS Sub App 执行协议

## 标准阶段

每个 sub uas app 必须至少包含以下阶段：

1. `intent_activation`：明确业务目标、约束、成功标准
2. `knowledge_binding`：把目标绑定到知识资产和业务规则
3. `agent_planning`：生成 agent 分工与协作计划
4. `system_mapping`：映射系统接口、数据、工具和流程
5. `governance_check`：执行风险、权限、偏差与治理校验
6. `evolution_plan`：形成下一轮迭代策略

## 禁忌

- 不允许缺少目标守恒策略
- 不允许缺少审计治理配置
- 不允许缺少演化回路
- 不允许把业务子应用做成纯文档、不可运行的空壳
""",
    ".claude/skills/output_contract.md": """# 《UAS Sub App 方案》输出契约

最终输出必须包含以下字段：

- `topic`
- `intent_model`
- `knowledge_assets`
- `runtime_topology`
- `agent_fabric`
- `system_mesh`
- `governance_controls`
- `evaluation_metrics`
- `evolution_loop`
- `delivery_plan`
""",
    ".claude/agents/README.md": "# Agent 注册表\n\n项目智能体元数据统一维护在 `configs/swarm_agents.json`。\n",
    ".claude/commands/README.md": "# 交互命令\n\n- `/intent [议题]`\n- `/design [议题ID]`\n- `/validate [议题ID]`\n- `/evolve [议题ID]`\n",
    "configs/platform_manifest.json": """{
  "$schema": "https://asui.dev/schemas/uas_platform_manifest.schema.json",
  "version": "v1.0",
  "platform": {
    "name": "UAS-Platform",
    "formal_definition": ["I", "K", "R", "A", "S", "G", "E", "Π"],
    "enterprise_agi_definition": "目标驱动 + 知识驱动 + Agent协作 + 系统执行 + 审计治理 + 演化闭环 的平台化统一",
    "technical_base": "ASUI",
    "runtime": "autonomous_agent"
  },
  "layers": {
    "I": "Intent Layer",
    "K": "Knowledge Substrate",
    "R": "Autonomous Agent Runtime",
    "A": "Agent Fabric",
    "S": "System Mesh",
    "G": "Governance Plane",
    "E": "Evolution Loop",
    "Π": "Protocol Stack"
  },
  "defaults": {
    "subapp_root": "projects",
    "require_governance": true,
    "require_evolution": true,
    "require_audit": true
  }
}
""",
    "configs/runtime_config.json": """{
  "version": "v1.0",
  "runtime_name": "autonomous_agent_runtime",
  "execution_mode": "knowledge_driven",
  "context_injection": true,
  "state_isolation": "task_level",
  "audit_enabled": true,
  "rollback_enabled": true,
  "human_checkpoints": ["WRITE_RISK", "SYSTEM_OP"]
}
""",
    "configs/governance_policy.json": """{
  "version": "v1.0",
  "governance": {
    "audit_required": true,
    "permission_model": ["READ_ONLY", "WRITE_SAFE", "WRITE_RISK", "SYSTEM_OP"],
    "require_explainability": true,
    "require_traceability": true,
    "high_risk_requires_human_approval": true
  }
}
""",
    "configs/evolution_policy.json": """{
  "version": "v1.0",
  "goal_guard": {
    "enabled": true,
    "require_goal_statement": true,
    "require_success_metrics": true
  },
  "iteration": {
    "enabled": true,
    "require_validation_before_evolution": true,
    "default_loop": ["intent_activation", "governance_check", "evolution_plan"]
  }
}
""",
    "configs/system_registry.json": """{
  "version": "v1.0",
  "systems": [
    {
      "id": "knowledge_base",
      "type": "asui_knowledge",
      "mode": "native"
    }
  ]
}
""",
    "configs/swarm_agents.json": """{
  "$schema": "https://asui.dev/schemas/workflow_config.schema.json",
  "version": "v1.0",
  "swarm_name": "uas_subapp_agent_fabric",
  "methodology": "platform-standard",
  "governance": {
    "require_goal_guard": true,
    "require_governance_audit": true,
    "require_evolution_loop": true
  },
  "agents": [
    {
      "id": "intent_guard",
      "name": "意图守恒智能体",
      "dimension": "intent",
      "stance": "业务目标监督者",
      "mission": "确保子应用始终服务于业务目标",
      "deliverable": "意图激活报告"
    },
    {
      "id": "knowledge_architect",
      "name": "知识架构智能体",
      "dimension": "knowledge",
      "stance": "ASUI知识底座设计者",
      "mission": "把业务规则、流程和约束沉淀为可执行知识",
      "deliverable": "知识绑定报告"
    },
    {
      "id": "runtime_architect",
      "name": "运行时智能体",
      "dimension": "runtime",
      "stance": "autonomous_agent运行架构设计者",
      "mission": "设计agent runtime、状态隔离、上下文注入与调度方式",
      "deliverable": "运行时拓扑报告"
    },
    {
      "id": "agent_fabric_architect",
      "name": "Agent编织智能体",
      "dimension": "agent",
      "stance": "Agent协作设计者",
      "mission": "规划主编排、专家agent、评估agent与演化agent的分工",
      "deliverable": "Agent分工报告"
    },
    {
      "id": "system_mesh_architect",
      "name": "系统网格智能体",
      "dimension": "system",
      "stance": "系统接入设计者",
      "mission": "映射业务系统、数据系统、工具与接口",
      "deliverable": "系统映射报告"
    },
    {
      "id": "governance_guard",
      "name": "治理审计智能体",
      "dimension": "governance",
      "stance": "治理与审计守门人",
      "mission": "校验权限、审计、解释链、风险与回滚机制",
      "deliverable": "治理校验报告"
    },
    {
      "id": "evolution_planner",
      "name": "进化规划智能体",
      "dimension": "evolution",
      "stance": "演化设计者",
      "mission": "输出验证指标、迭代路径与下一轮进化建议",
      "deliverable": "进化规划报告"
    }
  ]
}
""",
    "configs/workflow_config.json": """{
  "$schema": "https://asui.dev/schemas/workflow_config.schema.json",
  "version": "v1.0",
  "name": "UAS Sub App 工作流",
  "description": "基于ASUI与autonomous_agent runtime的标准sub uas app工作流",
  "swarm": {
    "mode": "uas-subapp-standard",
    "methodology": "platform-standard",
    "decision_policy": "goal-governed-evolution",
    "agents": [
      { "id": "intent_guard", "name": "意图守恒智能体", "dimension": "intent", "stance": "业务目标监督者" },
      { "id": "knowledge_architect", "name": "知识架构智能体", "dimension": "knowledge", "stance": "ASUI知识设计者" },
      { "id": "runtime_architect", "name": "运行时智能体", "dimension": "runtime", "stance": "运行架构设计者" },
      { "id": "agent_fabric_architect", "name": "Agent编织智能体", "dimension": "agent", "stance": "协作设计者" },
      { "id": "system_mesh_architect", "name": "系统网格智能体", "dimension": "system", "stance": "系统映射者" },
      { "id": "governance_guard", "name": "治理审计智能体", "dimension": "governance", "stance": "治理守门人" },
      { "id": "evolution_planner", "name": "进化规划智能体", "dimension": "evolution", "stance": "演化设计者" }
    ]
  },
  "steps": [
    {
      "id": "intent_activation",
      "name": "意图激活",
      "type": "llm",
      "agent_id": "intent_guard",
      "description": "归一化业务需求、目标、约束和成功标准",
      "prompt_template": "请把以下业务需求归一化为结构化意图，至少包含目标、约束、对象、成功标准。\\n\\n{{topic}}"
    },
    {
      "id": "knowledge_binding",
      "name": "知识绑定",
      "type": "llm",
      "dependencies": ["intent_activation"],
      "agent_id": "knowledge_architect",
      "description": "把业务规则绑定到ASUI知识资产",
      "prompt_template": "基于业务意图，定义应沉淀的知识资产、规则、workflow、schema 与 skills。"
    },
    {
      "id": "agent_planning",
      "name": "Agent规划",
      "type": "llm",
      "dependencies": ["knowledge_binding"],
      "agent_id": "agent_fabric_architect",
      "description": "生成agent分工与协作拓扑",
      "prompt_template": "为该sub uas app规划主编排agent、专家agent、治理agent和演化agent。"
    },
    {
      "id": "runtime_topology",
      "name": "运行时拓扑",
      "type": "llm",
      "dependencies": ["agent_planning"],
      "agent_id": "runtime_architect",
      "description": "生成 autonomous_agent runtime 设计",
      "prompt_template": "输出运行时拓扑、上下文注入、状态隔离、权限级别与执行模式。"
    },
    {
      "id": "system_mapping",
      "name": "系统映射",
      "type": "llm",
      "dependencies": ["runtime_topology"],
      "agent_id": "system_mesh_architect",
      "description": "定义系统网格与接入边界",
      "prompt_template": "列出必须接入的业务系统、数据系统、工具接口与知识系统。"
    },
    {
      "id": "governance_check",
      "name": "治理校验",
      "type": "llm",
      "dependencies": ["system_mapping"],
      "agent_id": "governance_guard",
      "description": "校验治理、审计、权限与回滚机制",
      "prompt_template": "检查该方案是否具备权限、审计、回滚、解释链与高风险审批。"
    },
    {
      "id": "evolution_plan",
      "name": "进化规划",
      "type": "llm",
      "dependencies": ["governance_check"],
      "agent_id": "evolution_planner",
      "description": "生成验证指标与迭代路径",
      "prompt_template": "输出评估指标、偏差风险、迭代回路和下一轮进化建议。"
    },
    {
      "id": "render_report",
      "name": "写入sub app方案",
      "type": "script",
      "dependencies": ["evolution_plan"],
      "script": "scripts/render_uas_plan.py"
    }
  ]
}
""",
    "docs/APP_BLUEPRINT.md": """# Sub UAS App 蓝图

## 产品定义

在这里补充该业务子应用的产品定义、目标对象、场景价值与关键闭环。

## 技术架构

- 技术底座：ASUI
- 运行架构：autonomous_agent runtime
- 核心构件：Intent / Knowledge / Runtime / Agent / System / Governance / Evolution
""",
    "docs/IMPLEMENTATION_ROADMAP.md": """# Sub UAS App 实施路线图

## Phase 1

- 业务意图归一化
- 知识资产绑定
- Agent拓扑设计

## Phase 2

- Runtime接入
- System Mesh映射
- Governance校验

## Phase 3

- 最小闭环运行
- 指标采集
- 进化迭代
""",
    "scripts/README.md": "# 执行脚本\n\n- `render_uas_plan.py`：生成 sub uas app 结构化方案\n- `evaluate_evolution.py`：校验目标守恒与治理完整性\n",
    "scripts/render_uas_plan.py": """#!/usr/bin/env python3
\"\"\"渲染 UAS sub app 方案。\"\"\"

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "sub-uas-app"


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
    return f"## {title}\\n" + "\\n".join(f"- {item}" for item in values) + "\\n"


def main() -> int:
    payload = json.load(sys.stdin)
    topic = str(payload.get("topic", "sub-uas-app"))
    slug = slugify(topic)

    report_dir = Path("reports")
    data_dir = Path("database") / "plans"
    report_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{slug}.md"
    data_path = data_dir / f"{slug}.json"

    markdown = [
        f"# UAS Sub App 方案：{topic}",
        "",
        section("意图模型", payload.get("intent_model")),
        section("知识资产", payload.get("knowledge_assets")),
        section("运行时拓扑", payload.get("runtime_topology")),
        section("Agent编织", payload.get("agent_fabric")),
        section("系统网格", payload.get("system_mesh")),
        section("治理控制", payload.get("governance_controls")),
        section("评估指标", payload.get("evaluation_metrics")),
        section("演化回路", payload.get("evolution_loop")),
        section("交付计划", payload.get("delivery_plan")),
    ]

    report_path.write_text("\\n".join(markdown), encoding="utf-8")
    data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"status": "written", "report_path": str(report_path), "data_path": str(data_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    "scripts/evaluate_evolution.py": """#!/usr/bin/env python3
\"\"\"评估 UAS sub app 是否满足平台标准。\"\"\"

import json
import sys
from pathlib import Path


def load_manifest() -> dict:
    manifest_path = Path("configs") / "platform_manifest.json"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def main() -> int:
    manifest = load_manifest()
    payload = json.load(sys.stdin)

    risks = []
    suggestions = []

    if manifest["platform"]["technical_base"] != "ASUI":
        risks.append("技术底座不是ASUI")
        suggestions.append("回退到平台清单，统一技术底座为ASUI")

    if manifest["platform"]["runtime"] != "autonomous_agent":
        risks.append("运行架构不是autonomous_agent")
        suggestions.append("回退到runtime配置，统一运行时为autonomous_agent")

    if not payload.get("governance_controls"):
        risks.append("缺少治理控制设计")
        suggestions.append("补充治理控制、审计、权限和高风险审批")

    if not payload.get("evolution_loop"):
        risks.append("缺少演化回路")
        suggestions.append("补充验证指标、偏差检测和迭代路径")

    status = "pass" if not risks else "needs_evolution"
    print(json.dumps({"status": status, "risks": risks, "suggestions": suggestions or ["当前方案满足平台标准"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    "database/README.md": "# 数据持久化\n\n- `database/plans/`：存放结构化 sub uas app 方案\n",
    "reports/README.md": "# 报告目录\n\nMarkdown 版 sub uas app 方案会输出到这里。\n",
}
