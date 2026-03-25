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
| `configs/evaluation_criteria.json` | 四维评价标准（业务/产品/技术/运行效果） |
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
  },
  "evolution_phases": {
    "drive": "intent_activation",
    "feedback": ["step_outputs", "evaluation"],
    "reflexivity": "evolution_plan"
  },
  "human_feedback_path": "database/feedback/{topic_slug}.json"
}
""",
    "configs/evaluation_criteria.json": """{
  "$schema": "https://asui.dev/schemas/evaluation_criteria.schema.json",
  "version": "v1.0",
  "evolution_threshold": 70,
  "dimension_weights": {
    "business": 0.25,
    "product": 0.25,
    "technology": 0.25,
    "operational": 0.25
  },
  "dimensions": {
    "business": {
      "name": "业务",
      "items": [
        { "id": "goal_clarity", "name": "目标明确度", "max_score": 25 },
        { "id": "value_loop", "name": "价值闭环", "max_score": 25 },
        { "id": "stakeholder_coverage", "name": "主客体覆盖", "max_score": 25 },
        { "id": "success_metrics", "name": "成功标准可量化", "max_score": 25 }
      ]
    },
    "product": {
      "name": "产品",
      "items": [
        { "id": "agent_fabric", "name": "Agent编织完整", "max_score": 25 },
        { "id": "deliverable_clarity", "name": "交付物清晰", "max_score": 25 },
        { "id": "evaluation_metrics", "name": "评估指标定义", "max_score": 25 },
        { "id": "workflow_completeness", "name": "工作流闭环", "max_score": 25 }
      ]
    },
    "technology": {
      "name": "技术",
      "items": [
        { "id": "asui_compliance", "name": "ASUI技术底座", "max_score": 25 },
        { "id": "autonomous_agent", "name": "autonomous_agent运行时", "max_score": 25 },
        { "id": "governance_complete", "name": "治理完整", "max_score": 25 },
        { "id": "knowledge_assets", "name": "知识资产完整", "max_score": 25 }
      ]
    },
    "operational": {
      "name": "运行效果",
      "items": [
        { "id": "run_completed", "name": "执行完成", "max_score": 25 },
        { "id": "audit_trace", "name": "审计可追溯", "max_score": 25 },
        { "id": "output_written", "name": "输出落盘", "max_score": 25 },
        { "id": "evolution_ready", "name": "演化就绪", "max_score": 25 }
      ]
    }
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
    "scripts/README.md": "# 执行脚本\n\n- `run_subapp.py`：通过 autonomous_agent runtime 运行 sub uas app\n- `render_uas_plan.py`：生成 sub uas app 结构化方案\n- `evaluate_evolution.py`：校验目标守恒与治理完整性\n",
    "scripts/run_subapp.py": """#!/usr/bin/env python3
\"\"\"运行 sub uas app。\"\"\"

import argparse
import json
from pathlib import Path

from asui.runtime.runtime_manager import RuntimeManager


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 UAS sub app")
    parser.add_argument("topic", help="业务议题")
    parser.add_argument("--payload-json", help="额外 JSON payload")
    parser.add_argument("--evaluate", action="store_true", help="运行后执行评估")
    args = parser.parse_args()

    payload = json.loads(args.payload_json) if args.payload_json else None
    manager = RuntimeManager(Path(__file__).resolve().parents[1])
    result = manager.run(args.topic, payload=payload, evaluate=args.evaluate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
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
\"\"\"UAS sub app 四维评价：业务、产品、技术、运行效果，驱动自主进化。\"\"\"

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def score_business(criteria: dict, payload: dict, app_root: Path) -> tuple[float, list[str]]:
    score, suggestions = 0.0, []
    intent = payload.get("intent_model") or payload.get("intent") or {}
    if isinstance(intent, dict):
        intent = intent.get("goal") or intent.get("topic") or intent
    if intent or payload.get("goal") or payload.get("topic"):
        score += 25
    else:
        suggestions.append("补充业务目标、约束与成功标准")
    if payload.get("evolution_loop") or payload.get("evaluation_metrics"):
        score += 25
    else:
        suggestions.append("完善 evolution_loop、验证指标与迭代路径")
    if payload.get("target_audience") or (isinstance(payload.get("intent_model"), dict) and payload["intent_model"].get("target_audience")):
        score += 25
    else:
        suggestions.append("明确目标对象与利益相关方")
    if payload.get("success_metrics") or payload.get("evaluation_metrics"):
        score += 25
    else:
        suggestions.append("定义可量化的成功指标")
    return min(100, score), suggestions


def score_product(criteria: dict, payload: dict, app_root: Path) -> tuple[float, list[str]]:
    score, suggestions = 0.0, []
    agents = payload.get("agent_fabric") or []
    config_agents = load_json(app_root / "configs" / "swarm_agents.json")
    if agents or (config_agents and config_agents.get("agents")):
        score += 25
    else:
        suggestions.append("完善 swarm_agents 角色与交付物")
    if payload.get("delivery_plan") or payload.get("knowledge_assets"):
        score += 25
    else:
        suggestions.append("明确各步骤产出与报告格式")
    if payload.get("evaluation_metrics"):
        score += 25
    else:
        suggestions.append("补充 evaluation_metrics")
    workflow = load_json(app_root / "configs" / "workflow_config.json")
    steps = (workflow or {}).get("steps", [])
    step_ids = [s.get("id", "") for s in steps]
    if "intent_activation" in step_ids and "governance_check" in step_ids and ("evolution_plan" in step_ids or "render_report" in step_ids):
        score += 25
    else:
        suggestions.append("确保 workflow 含 intent→governance→evolution→render")
    return min(100, score), suggestions


def score_technology(criteria: dict, payload: dict, app_root: Path) -> tuple[float, list[str]]:
    score, suggestions = 0.0, []
    manifest = load_json(app_root / "configs" / "platform_manifest.json")
    if manifest and manifest.get("platform", {}).get("technical_base") == "ASUI":
        score += 25
    else:
        suggestions.append("确保 technical_base 为 ASUI")
    if manifest and manifest.get("platform", {}).get("runtime") == "autonomous_agent":
        score += 25
    else:
        suggestions.append("确保 runtime 为 autonomous_agent")
    governance = load_json(app_root / "configs" / "governance_policy.json")
    if governance and governance.get("governance"):
        score += 25
    else:
        suggestions.append("补充 governance_policy、审计与权限")
    skills_dir = app_root / ".claude" / "skills"
    configs = list((app_root / "configs").glob("*.json")) if (app_root / "configs").exists() else []
    if (skills_dir.exists() and list(skills_dir.glob("*.md"))) or len(configs) >= 5:
        score += 25
    else:
        suggestions.append("完善 configs 与 .claude/skills")
    return min(100, score), suggestions


def score_operational(criteria: dict, payload: dict, app_root: Path) -> tuple[float, list[str]]:
    score, suggestions = 0.0, []
    step_outputs = payload.get("step_outputs", {})
    if step_outputs or payload.get("render_report_result") or payload.get("status") == "written":
        score += 25
    else:
        suggestions.append("检查 workflow 步骤是否全部执行")
    audit_dir = app_root / "database" / "audit"
    if audit_dir.exists() and list(audit_dir.glob("*.jsonl")):
        score += 25
    else:
        suggestions.append("确保 database/audit 有记录")
    reports_dir = app_root / "reports"
    db_plans = app_root / "database" / "plans"
    if (reports_dir.exists() and list(reports_dir.glob("*.md"))) or (db_plans.exists() and list(db_plans.glob("*.json"))):
        score += 25
    else:
        suggestions.append("确保 reports 或 database 有产出")
    if payload.get("evaluation") or payload.get("evolution"):
        score += 25
    else:
        suggestions.append("确保 cognitive_state 含 evolution 建议")
    return min(100, score), suggestions


def main() -> int:
    payload = json.load(sys.stdin)
    app_root = Path.cwd()
    criteria = load_json(app_root / "configs" / "evaluation_criteria.json") or {}
    dimensions_cfg = criteria.get("dimensions", {})
    weights = criteria.get("dimension_weights") or {"business": 0.25, "product": 0.25, "technology": 0.25, "operational": 0.25}
    threshold = criteria.get("evolution_threshold", 70)
    scorers = {"business": score_business, "product": score_product, "technology": score_technology, "operational": score_operational}
    scores = {}
    all_suggestions = []
    weighted_sum = 0.0
    weight_total = 0.0
    for dim_id, scorer in scorers.items():
        dim_cfg = dimensions_cfg.get(dim_id, {})
        dim_score, dim_suggestions = scorer(dim_cfg, payload, app_root)
        scores[dim_id] = {"score": round(dim_score, 1), "name": dim_cfg.get("name", dim_id), "suggestions": dim_suggestions}
        all_suggestions.extend(dim_suggestions)
        w = weights.get(dim_id, 0.25)
        weighted_sum += dim_score * w
        weight_total += w
    total_score = round(weighted_sum / weight_total if weight_total else 0, 1)
    status = "pass" if total_score >= threshold else "needs_evolution"
    risks = [f"{k}维度得分{scores[k]['score']}低于预期" for k, v in scores.items() if v["score"] < 60]
    output = {"status": status, "total_score": total_score, "evolution_threshold": threshold, "dimension_scores": scores, "risks": risks, "suggestions": list(dict.fromkeys(all_suggestions)) or ["当前满足评价标准"]}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    "database/README.md": "# 数据持久化\n\n- `database/plans/`：存放结构化 sub uas app 方案\n- `database/audit/`：存放运行时审计日志\n- `database/cognitive_state/`：存放认知状态快照\n- `database/capabilities/`：存放能力注册表快照\n- `database/feedback/`：人机协同反馈（human_review 步骤写入）\n- `database/evolution_backups/`：演化回写前的配置备份\n",
    "database/audit/README.md": "# 审计目录\n\nRuntime 审计日志（如 `execution_log.jsonl`）会写入这里。\n",
    "database/cognitive_state/README.md": "# 认知状态目录\n\n每次运行的认知状态快照会写入这里。\n",
    "database/capabilities/README.md": "# 能力注册目录\n\n每个 sub uas app 的能力注册表快照会写入这里。\n",
    "database/feedback/README.md": "# 人机协同反馈\n\nhuman_review 步骤等待用户将反馈写入此处。格式：{topic_slug}.json。\n",
    "database/evolution_backups/README.md": "# 演化回写备份\n\n/evolveApply 执行前的 configs/skills 备份。\n",
    "reports/README.md": "# 报告目录\n\nMarkdown 版 sub uas app 方案会输出到这里。\n",
}
