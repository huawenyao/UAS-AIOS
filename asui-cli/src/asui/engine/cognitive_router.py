"""认知路由器。"""

from __future__ import annotations


class CognitiveRouter:
    """基于认知状态和能力注册表生成路由决策。"""

    def route(self, step: dict, cognitive_state: dict, capability_registry: dict) -> dict:
        step_id = step["id"]
        step_type = step["type"]
        target_agent_id = step.get("agent_id")

        if target_agent_id is None:
            target_agent_id = self._infer_agent_id(step_id, capability_registry)

        intent_keywords = self._extract_intent_keywords(cognitive_state.get("intent", {}))
        uncertainty = "low" if intent_keywords else "medium"

        return {
            "step_id": step_id,
            "step_type": step_type,
            "target_agent_id": target_agent_id,
            "reason": f"根据 step={step_id}、能力注册表与当前认知状态进行路由",
            "uncertainty": uncertainty,
            "intent_keywords": intent_keywords,
        }

    def _infer_agent_id(self, step_id: str, capability_registry: dict) -> str | None:
        for capability in capability_registry.get("workflow_capabilities", []):
            if capability.get("step_id") == step_id and capability.get("agent_id"):
                return capability["agent_id"]
        return None

    def _extract_intent_keywords(self, intent_state: dict) -> list[str]:
        keywords = []
        for value in intent_state.values():
            if isinstance(value, list):
                keywords.extend(str(item) for item in value[:3])
        return keywords[:5]
