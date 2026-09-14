"""外环端口：产品形态对齐 Temporal RuntimeCycleWorkflow；实验室默认内存实现。"""

from __future__ import annotations

import copy
from typing import Any, Protocol

from uas_hub.cycle import TASK_QUEUE, WORKFLOW_TYPE, invoke_and_finish
from uas_hub.errors import HubError, utc_now


class OuterLoopPort(Protocol):
    def bind_hub(self, hub: Any) -> None: ...
    def start(self, args: dict[str, Any]) -> dict[str, Any]: ...
    def signal(self, workflow_id: str, name: str, payload: dict[str, Any] | None = None) -> dict[str, Any]: ...
    def snapshot(self) -> dict[str, Any]: ...
    def restore(self, snap: dict[str, Any]) -> None: ...
    def events_for_task(self, task_id: str) -> list[dict[str, Any]]: ...


class InMemoryOuterLoop:
    """Compose Temporal 未就绪时的可替换实现。禁止当成第三套产品引擎。"""

    workflow_type = WORKFLOW_TYPE
    task_queue = TASK_QUEUE

    def __init__(self) -> None:
        self.hub: Any = None
        self.runs: dict[str, dict[str, Any]] = {}

    def bind_hub(self, hub: Any) -> None:
        self.hub = hub

    def start(self, args: dict[str, Any]) -> dict[str, Any]:
        if self.hub is None:
            raise HubError("INVARIANT_FAILED", "outer loop unbound")
        task_id = str(args.get("task_id") or "")
        wid = f"wf-{task_id}"
        run: dict[str, Any] = {
            "workflow_id": wid,
            "workflow_type": self.workflow_type,
            "task_queue": self.task_queue,
            "task_id": task_id,
            "tenant_id": args.get("tenant_id"),
            "source_node_id": args.get("source_node_id"),
            "profile": "runtime",
            "track": args.get("track") or "pipaw",
            "cs_write": list(args.get("cs_write") or []),
            "status": "awaiting_approval" if self._needs_l2(args.get("cs_write")) else "opened",
            "events": [{"type": "started", "ts": utc_now()}],
        }
        if run["status"] == "awaiting_approval":
            run["events"].append({"type": "awaiting_approval", "ts": utc_now()})
        else:
            self._invoke_and_finish(run)
        self.runs[wid] = run
        return run

    def _needs_l2(self, ops: list[str] | None) -> bool:
        for name in ops or []:
            op = self.hub.registry.get(name)
            if op and str(op.get("approval_level", "L1")) in {"L2", "L3", "L4"}:
                return True
        return False

    def signal(self, workflow_id: str, name: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = payload
        run = self.runs.get(workflow_id)
        if not run:
            raise HubError("OPERATION_NOT_FOUND", workflow_id)
        if name == "rejected":
            run["status"] = "rejected"
            run["events"].append({"type": "rejected", "ts": utc_now()})
            return run
        if name == "more_context":
            run["events"].append({"type": "more_context", "ts": utc_now()})
            return run
        if name == "approved":
            invoke_and_finish(self.hub, run)
            return run
        raise HubError("INVARIANT_FAILED", name)

    def _invoke_and_finish(self, run: dict[str, Any]) -> None:
        invoke_and_finish(self.hub, run)

    def events_for_task(self, task_id: str) -> list[dict[str, Any]]:
        for run in self.runs.values():
            if run.get("task_id") == task_id:
                return list(run.get("events") or [])
        return []

    def snapshot(self) -> dict[str, Any]:
        return {"runs": copy.deepcopy(self.runs)}

    def restore(self, snap: dict[str, Any]) -> None:
        self.runs = copy.deepcopy(snap.get("runs") or {})
