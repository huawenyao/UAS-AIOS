"""ΠPaw Task Panel：将 Working Task 转为可渲染任务态（非日志流）。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .intent_hub import IntentEscalationHub


class PipawTaskPanel:
    def __init__(
        self,
        workspace_root: Path,
        *,
        roster_path: Path | None = None,
        playbook_path: Path | None = None,
        tasks_store_path: Path | None = None,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.roster_path = roster_path or (
            self.workspace_root / "configs" / "pipaw_business_agent_roster.json"
        )
        self.playbook_path = playbook_path or (
            self.workspace_root / "configs" / "pipaw_cs_agent_playbook.json"
        )
        self._roster = self._load_json(self.roster_path)
        self._playbooks = {
            p["playbook_id"]: p
            for p in self._load_json(self.playbook_path).get("playbooks", [])
        }
        self._intent_hub = IntentEscalationHub(
            self.workspace_root, tasks_store_path=tasks_store_path
        )
        self._current_id: str | None = None
        self._step_progress: int = 0

    @staticmethod
    def _load_json(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def get_cs_agent(self) -> dict | None:
        for agent in self._roster.get("agents", []):
            if agent.get("agent_id") == "agent.cs_specialist":
                return agent
        agents = self._roster.get("agents", [])
        return agents[0] if agents else None

    def _playbook_for_agent(self, agent: dict) -> dict:
        pid = agent.get("playbook_id", "")
        return self._playbooks.get(pid, {"steps": []})

    def _build_steps(self, playbook: dict, *, progress: int = 0) -> list[dict[str, Any]]:
        steps_out: list[dict[str, Any]] = []
        for i, step in enumerate(playbook.get("steps", [])):
            steps_out.append(
                {
                    "step_id": step["step_id"],
                    "label": step["label"],
                    "operation_ref": step.get("operation_ref"),
                    "done": i < progress,
                    "current": i == progress,
                }
            )
        return steps_out

    def _working_task_to_item(
        self,
        wt: dict[str, Any],
        playbook: dict,
        *,
        display_phase: str,
        step_progress: int = 0,
        status: str | None = None,
    ) -> dict[str, Any]:
        st = status or wt.get("status", "open")
        if display_phase == "current":
            st = "in_progress"
        return {
            "item_id": wt["task_id"],
            "source_type": "working_task",
            "status": st,
            "display_phase": display_phase,
            "title": wt.get("title") or wt.get("goal", ""),
            "subtitle": wt.get("goal", ""),
            "priority": wt.get("priority", "normal"),
            "due_at": wt.get("sla_due_at"),
            "sla_label": self._sla_label(wt),
            "business_context": wt.get("business_context") or {},
            "evidence_count": len(wt.get("evidence_refs") or []),
            "steps": self._build_steps(playbook, progress=step_progress),
            "actions": [
                {"label": "处理", "action": "open"},
                {"label": "完成当前步骤", "action": "complete_step"},
                {"label": "升级主管", "action": "escalate"},
            ],
        }

    @staticmethod
    def _sla_label(wt: dict) -> str:
        pri = wt.get("priority", "normal")
        if pri in ("high", "critical"):
            return "剩余时间：今日内"
        return "截止时间：按 SLA 策略"

    def build_view(
        self,
        *,
        tenant_id: str,
        assignee_role_id: str = "role.cs_agent",
    ) -> dict[str, Any]:
        agent = self.get_cs_agent()
        if not agent:
            return {
                "tenant_id": tenant_id,
                "assignee_role_id": assignee_role_id,
                "agent_id": "",
                "summary": {"backlog_count": 0, "has_current": False, "sla_at_risk": 0},
                "backlog": [],
                "current": None,
            }

        playbook = self._playbook_for_agent(agent)
        tasks = self._intent_hub.list_tasks(
            tenant_id=tenant_id,
            position_id=agent.get("position_id"),
            assignee_role_id=assignee_role_id,
        )

        backlog: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        progress = self._step_progress

        for wt in tasks:
            if wt.get("status") in ("done", "cancelled"):
                continue
            item = self._working_task_to_item(
                wt,
                playbook,
                display_phase="backlog",
            )
            if self._current_id and wt["task_id"] == self._current_id:
                current = self._working_task_to_item(
                    wt,
                    playbook,
                    display_phase="current",
                    step_progress=progress,
                )
            else:
                backlog.append(item)

        if self._current_id and current is None:
            for wt in tasks:
                if wt["task_id"] == self._current_id:
                    current = self._working_task_to_item(
                        wt,
                        playbook,
                        display_phase="current",
                        step_progress=progress,
                    )
                    backlog = [b for b in backlog if b["item_id"] != self._current_id]
                    break

        sla_at_risk = sum(1 for b in backlog if b.get("priority") in ("high", "critical"))
        if current and current.get("priority") in ("high", "critical"):
            sla_at_risk += 1

        return {
            "tenant_id": tenant_id,
            "assignee_role_id": assignee_role_id,
            "agent_id": agent["agent_id"],
            "summary": {
                "backlog_count": len(backlog),
                "has_current": current is not None,
                "sla_at_risk": sla_at_risk,
            },
            "backlog": backlog,
            "current": current,
        }

    def open_task(self, task_id: str) -> None:
        self._current_id = task_id

    def advance_current_step(self) -> int:
        self._step_progress += 1
        return self._step_progress

    def reset_session(self) -> None:
        self._current_id = None
        self._step_progress = 0
