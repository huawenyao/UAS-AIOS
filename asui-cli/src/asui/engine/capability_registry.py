"""能力注册表。"""

from __future__ import annotations

from pathlib import Path


class CapabilityRegistry:
    """从 subapp 资产中提取 agent 能力与系统能力。"""

    def __init__(self, app_root: Path, configs: dict) -> None:
        self.app_root = app_root
        self.configs = configs

    def build(self) -> dict:
        swarm_agents = self.configs.get("swarm_agents", {}).get("agents", [])
        system_registry = self.configs.get("system_registry", {}).get("systems", [])
        workflow_steps = self.configs.get("workflow_config", {}).get("steps", [])

        return {
            "agents": [
                {
                    "id": agent.get("id"),
                    "name": agent.get("name"),
                    "dimension": agent.get("dimension"),
                    "stance": agent.get("stance"),
                    "mission": agent.get("mission"),
                    "deliverable": agent.get("deliverable"),
                }
                for agent in swarm_agents
            ],
            "systems": [
                {
                    "id": system.get("id"),
                    "type": system.get("type"),
                    "mode": system.get("mode"),
                }
                for system in system_registry
            ],
            "workflow_capabilities": [
                {
                    "step_id": step.get("id"),
                    "type": step.get("type"),
                    "agent_id": step.get("agent_id"),
                }
                for step in workflow_steps
            ],
        }
