"""autonomous_agent runtime manager."""

from __future__ import annotations

import json
from pathlib import Path

from .agent_orchestrator import AgentOrchestrator
from .audit_engine import AuditEngine
from .context_injector import ContextInjector
from .evolution_engine import EvolutionEngine
from .tool_gateway import ToolGateway


class RuntimeManager:
    """统一运行 sub uas app 标准工作流。"""

    def __init__(self, app_root: Path) -> None:
        self.app_root = app_root.resolve()
        self.context_injector = ContextInjector()
        self.agent_orchestrator = AgentOrchestrator()
        self.tool_gateway = ToolGateway()
        self.audit_engine = AuditEngine(self.app_root)
        self.evolution_engine = EvolutionEngine()

    def run(
        self,
        topic: str,
        payload: dict | None = None,
        evaluate: bool = False,
    ) -> dict:
        context = self.context_injector.inject(self.app_root, topic, payload)
        workflow = context["configs"]["workflow_config"]
        state: dict = {"topic": topic}

        self.audit_engine.record({"event": "run_started", "topic": topic})

        for step in workflow["steps"]:
            step_type = step["type"]
            if step_type == "parallel":
                self.audit_engine.record({"event": "step_skipped_parallel_wrapper", "step_id": step["id"]})
                continue

            if step_type == "llm":
                output = self.agent_orchestrator.execute_llm_step(step, context, state)
                state.update(output)
                self.audit_engine.record(
                    {"event": "llm_step_completed", "step_id": step["id"], "output_keys": sorted(output.keys())}
                )
                continue

            if step_type == "script":
                output = self.tool_gateway.execute_script(self.app_root, step["script"], state)
                state[f"{step['id']}_result"] = output
                state.update(output)
                self.audit_engine.record(
                    {"event": "script_step_completed", "step_id": step["id"], "output_keys": sorted(output.keys())}
                )

        evaluation = None
        if evaluate:
            evaluation = self.evolution_engine.evaluate(self.app_root, state)
            state["evaluation"] = evaluation
            self.audit_engine.record(
                {
                    "event": "evaluation_completed",
                    "status": evaluation.get("status"),
                    "risk_count": len(evaluation.get("risks", [])),
                }
            )

        self.audit_engine.record({"event": "run_finished", "topic": topic})

        return {
            "status": "completed",
            "topic": topic,
            "state": state,
            "evaluation": evaluation,
            "audit_log": str(self.audit_engine.log_path.relative_to(self.app_root)),
        }

    def validate_assets(self) -> dict:
        required = [
            "CLAUDE.md",
            "configs/platform_manifest.json",
            "configs/runtime_config.json",
            "configs/governance_policy.json",
            "configs/evolution_policy.json",
            "configs/system_registry.json",
            "configs/swarm_agents.json",
            "configs/workflow_config.json",
        ]
        missing = [item for item in required if not (self.app_root / item).exists()]
        return {"missing": missing, "status": "ok" if not missing else "missing_assets"}

    def dump_state(self, path: Path, state: dict) -> None:
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
