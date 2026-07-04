"""企业数字人生态双轨闭环：SelfPaw → ΠPaw → cs.*（原型）。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .domain_binding import DomainBindingLoader
from .intent_hub import EscalateContext, IntentEscalationHub
from .org_identity import OrgIdentityResolver, OrgSessionRequest
from .pipaw_cs_agent import PipawCsAgentRuntime


def run_dual_track_cs_loop(
    workspace_root: Path,
    *,
    intent_path: Path | None = None,
    tenant_id: str = "t-acme-demo",
    user_id: str = "u-employee-1001",
) -> dict[str, Any]:
    root = workspace_root.resolve()
    intent_file = intent_path or (
        root / "configs" / "intent_samples" / "complaint_escalation.sample.json"
    )
    intent = json.loads(intent_file.read_text(encoding="utf-8"))

    identity = OrgIdentityResolver(root)
    session = identity.resolve(
        OrgSessionRequest(
            tenant_id=tenant_id,
            user_id=user_id,
            position_id=intent.get("actor", {}).get("position_id"),
        )
    )
    if session.status != "ok":
        return {"status": "failed", "phase": "org_identity", "deny_reason": session.deny_reason}

    domain_loader = DomainBindingLoader(root)
    domain_ctx = domain_loader.runtime_prompt_injection(
        {
            "position_code": session.position_code,
            "position_id": session.position_id,
            "domain_id": session.domain_id,
        }
    )

    hub = IntentEscalationHub(root)
    hub.reset_store()
    esc = hub.escalate(
        intent,
        EscalateContext(
            tenant_id=tenant_id,
            request_tenant_id=tenant_id,
            user_id=user_id,
            product_track="selfpaw",
            role_ids=session.role_ids,
        ),
    )
    if esc.status != "ok":
        return {
            "status": "failed",
            "phase": "escalation",
            "deny_reason": esc.deny_reason,
            "org_session": session.__dict__,
            "domain": domain_ctx,
        }

    agent = PipawCsAgentRuntime(root)
    task_id = (esc.working_task or {}).get("task_id", "")
    if task_id:
        agent.panel.open_task(task_id)
    step = agent.run_current_step(tenant_id=tenant_id)
    audit_chain = [
        {"event": "org_identity", "user_id": user_id, "position": session.position_code},
        {"event": "domain_bound", "domain_id": domain_ctx.get("domain_id")},
        {"event": "intent_escalated", "task_id": esc.working_task.get("task_id")},
        {"event": "pipaw_cs_step", "operation_ref": step.operation_ref, "status": step.status},
    ]

    ok = step.status == "ok" and esc.working_task is not None
    return {
        "status": "completed" if ok else "failed",
        "org_session": {
            "tenant_id": session.tenant_id,
            "position_code": session.position_code,
            "domain_id": session.domain_id,
            "role_ids": session.role_ids,
        },
        "domain": domain_ctx,
        "working_task_id": (esc.working_task or {}).get("task_id"),
        "cs_step": {
            "status": step.status,
            "operation_ref": step.operation_ref,
            "deny_reason": step.deny_reason,
        },
        "audit_chain": audit_chain,
        "business_closed_loop": ok,
    }
