"""RuntimeCycleWorkflow 产品形态。本文件是 Workflow 定义：禁止 LLM、httpx、CRM SDK。"""

from __future__ import annotations

# 步骤名冻结；实现可换 Temporal，语义不可换。
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

# Activity 名 = Hub 回调，不在本模块执行副作用。
ACTIVITIES = (
    "activity_invoke_cs",
    "activity_refresh_kpi",
    "activity_patch_live_wm",
)


def workflow_plan(needs_l2: bool) -> list[str]:
    steps = ["LoadTask", "RunInnerLoop"]
    if needs_l2:
        steps.append("WaitForSignal")
    steps.extend(["InvokeCs", "PatchLiveWm", "RefreshKpi", "WriteAudit"])
    return steps
