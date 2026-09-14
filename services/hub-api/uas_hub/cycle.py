"""RuntimeCycle 共享 Activity：内存外环与 Temporal Worker 必须走同一套函数。

Workflow 只编排这些步骤；LLM / httpx / CRM SDK 禁止出现在 workflow 模块。
"""

from __future__ import annotations

from typing import Any

from uas_hub.errors import Envelope, utc_now

WORKFLOW_TYPE = "RuntimeCycleWorkflow"
TASK_QUEUE = "uas-runtime"
NAMESPACE = "uas"
STEPS = (
    "LoadTask",
    "RunInnerLoop",
    "InvokeCs",
    "WaitForSignal",
    "PatchLiveWm",
    "RefreshKpi",
    "WriteAudit",
)


def worker_envelope(run: dict[str, Any]) -> Envelope:
    return Envelope(
        tenant_id=str(run.get("tenant_id") or ""),
        actor_id="runtime-worker",
        profile="runtime",
        track=str(run.get("track") or "pipaw"),
        correlation_id=f"corr-{run.get('task_id')}",
        source_node_id=str(run.get("source_node_id") or "") or None,
    )


def invoke_cs_writes(hub: Any, run: dict[str, Any]) -> None:
    env = worker_envelope(run)
    node = hub.graphs.node(run["tenant_id"], run["source_node_id"])
    customer = (node.get("object_refs") or ["unknown"])[0]
    for op in run.get("cs_write") or []:
        hub.invoke_cs(env, op, {"customer_id": customer, "when": utc_now()})


def refresh_kpi(hub: Any, run: dict[str, Any]) -> None:
    env = worker_envelope(run)
    node = hub.graphs.node(run["tenant_id"], run["source_node_id"])
    kpi_id = (node.get("kpi") or {}).get("kpi_id")
    if kpi_id:
        hub.invoke_cs(env, "cs.metric.query", {"kpi_id": kpi_id})


def patch_live_wm(hub: Any, run: dict[str, Any]) -> None:
    env = worker_envelope(run)
    try:
        hub.wm.put("wm-hengchuan-ltc", "live", 1, {"hook": "cycle", "task_id": run.get("task_id")})
    except Exception:
        pass
    hub.wm_patch(env, "wm-hengchuan-ltc", "live", {"hook": "refresh", "task_id": run.get("task_id")})


def invoke_and_finish(hub: Any, run: dict[str, Any]) -> dict[str, Any]:
    invoke_cs_writes(hub, run)
    refresh_kpi(hub, run)
    patch_live_wm(hub, run)
    run["status"] = "opened"
    run.setdefault("events", [])
    run["events"].append({"type": "cs.invoked", "ts": utc_now()})
    run["events"].append({"type": "kpi.refreshed", "ts": utc_now()})
    return run
