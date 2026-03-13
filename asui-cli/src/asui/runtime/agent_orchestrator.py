"""Agent 编排与标准步骤输出。"""

from __future__ import annotations

from pathlib import Path


class AgentOrchestrator:
    """执行知识驱动步骤并生成结构化输出。"""

    def execute_llm_step(self, step: dict, context: dict, state: dict) -> dict:
        step_id = step["id"]
        payload = context.get("payload", {})
        configs = context.get("configs", {})

        if step_id == "intent_activation":
            return {
                "topic": context["topic"],
                "intent_model": payload.get(
                    "intent_model",
                    [f"围绕“{context['topic']}”生成的业务意图与成功标准"],
                ),
            }

        if step_id == "knowledge_binding":
            knowledge_assets = payload.get("knowledge_assets")
            if knowledge_assets is None:
                knowledge_assets = sorted(
                    ["CLAUDE.md"]
                    + [f"configs/{name}.json" for name in configs.keys()]
                    + context.get("skills", [])
                )
            return {"knowledge_assets": knowledge_assets}

        if step_id == "agent_planning":
            agents = configs.get("swarm_agents", {}).get("agents", [])
            agent_fabric = payload.get("agent_fabric") or [agent["name"] for agent in agents]
            return {"agent_fabric": agent_fabric}

        if step_id == "runtime_topology":
            runtime_cfg = configs.get("runtime_config", {})
            runtime_topology = payload.get("runtime_topology") or [
                f"runtime={runtime_cfg.get('runtime_name', 'autonomous_agent_runtime')}",
                f"context_injection={runtime_cfg.get('context_injection', False)}",
                f"state_isolation={runtime_cfg.get('state_isolation', 'unknown')}",
            ]
            return {"runtime_topology": runtime_topology}

        if step_id == "system_mapping":
            systems = configs.get("system_registry", {}).get("systems", [])
            system_mesh = payload.get("system_mesh") or [
                f"{system.get('id')}:{system.get('type')}" for system in systems
            ]
            return {"system_mesh": system_mesh}

        if step_id == "governance_check":
            governance_cfg = configs.get("governance_policy", {}).get("governance", {})
            governance_controls = payload.get("governance_controls") or [
                "audit" if governance_cfg.get("audit_required") else "no-audit",
                "approval" if governance_cfg.get("high_risk_requires_human_approval") else "no-approval",
                "rollback" if "WRITE_RISK" in governance_cfg.get("permission_model", []) else "no-rollback",
            ]
            return {"governance_controls": governance_controls}

        if step_id == "evolution_plan":
            evolution_cfg = configs.get("evolution_policy", {})
            metrics = payload.get("evaluation_metrics") or self._default_metrics(evolution_cfg)
            evolution_loop = payload.get("evolution_loop") or evolution_cfg.get("iteration", {}).get(
                "default_loop",
                ["intent_activation", "governance_check", "evolution_plan"],
            )
            delivery_plan = payload.get("delivery_plan") or self._default_delivery_plan(context["app_root"])
            return {
                "evaluation_metrics": metrics,
                "evolution_loop": evolution_loop,
                "delivery_plan": delivery_plan,
            }

        return {}

    def _default_metrics(self, evolution_cfg: dict) -> list[str]:
        thresholds = evolution_cfg.get("evaluation_thresholds", {})
        if thresholds:
            return [f"{key}>={value}" for key, value in thresholds.items()]
        if evolution_cfg.get("goal_guard", {}).get("require_success_metrics"):
            return ["必须定义成功指标"]
        return ["待定义评估指标"]

    def _default_delivery_plan(self, app_root: str) -> list[str]:
        roadmap = Path(app_root) / "docs" / "IMPLEMENTATION_ROADMAP.md"
        if not roadmap.exists():
            return ["先形成最小可运行闭环"]
        phases = []
        for line in roadmap.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                phases.append(line.replace("## ", "").strip())
        return phases or ["先形成最小可运行闭环"]
