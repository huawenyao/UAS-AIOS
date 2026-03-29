"""ASUI autonomous_agent 标准工作流阶段与步骤类型契约（Π）。"""

from __future__ import annotations

# 与 docs/ASUI_AUTONOMOUS_AGENT_STANDARD.md 中八阶段一致
STANDARD_WORKFLOW_STEP_IDS: tuple[str, ...] = (
    "intent_activation",
    "knowledge_binding",
    "agent_planning",
    "runtime_topology",
    "system_mapping",
    "governance_check",
    "evolution_plan",
    "render_report",
)

WORKFLOW_STEP_TYPES: frozenset[str] = frozenset({"llm", "script", "parallel"})


def is_standard_workflow_step(step_id: str) -> bool:
    return step_id in STANDARD_WORKFLOW_STEP_IDS
