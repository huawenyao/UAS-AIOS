"""双轨闭环：SelfPaw（个人轨）→ Business AGI 工作任务（经营轨）。

ΠPaw 仅保留编排身份；执行不再走客服数字人 / Task Panel。
经营动作落地到 World Model Studio（认知实践世界模型），禁止模型直连业务系统。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .domain_binding import DomainBindingLoader
from .intent_hub import EscalateContext, IntentEscalationHub
from .org_identity import OrgIdentityResolver, OrgSessionRequest

WORLD_MODEL_STUDIO = "examples/world-model-studio"


def run_dual_track_loop(
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

    task = esc.working_task or {}
    studio = root / WORLD_MODEL_STUDIO
    handoff = {
        "product_form": "world_model_studio",
        "orchestration_identity": "pipaw",
        "path": WORLD_MODEL_STUDIO,
        "exists": studio.is_dir(),
        "next": "run_cognitive_cycle",
        "note": "经营轨不执行数字人对话；进入世界模型 7 步闭环",
    }
    audit_chain = [
        {"event": "org_identity", "user_id": user_id, "position": session.position_code},
        {"event": "domain_bound", "domain_id": domain_ctx.get("domain_id")},
        {"event": "intent_escalated", "task_id": task.get("task_id"), "product_track": "pipaw"},
        {"event": "handoff_world_model_studio", "path": WORLD_MODEL_STUDIO},
    ]
    ok = bool(task.get("task_id"))
    return {
        "status": "completed" if ok else "failed",
        "org_session": {
            "tenant_id": session.tenant_id,
            "position_code": session.position_code,
            "domain_id": session.domain_id,
            "role_ids": session.role_ids,
        },
        "domain": domain_ctx,
        "working_task_id": task.get("task_id"),
        "handoff": handoff,
        "audit_chain": audit_chain,
        "business_closed_loop": ok,
    }


# 兼容旧测试名：不再调用客服 Agent
run_dual_track_cs_loop = run_dual_track_loop
