from __future__ import annotations

from typing import Any

from uas_hub.errors import Envelope, HubError, PolicyTrace
from uas_hub.registry import Registry

WRITE_PROFILES = {"runtime"}


class PolicyChain:
    """判定序不可颠倒。步骤名供单测断言。"""

    ORDER = (
        "inject",
        "tenant",
        "registry",
        "rbac",
        "approval",
        "gates",
        "scope",
        "execute",
        "audit",
    )

    def __init__(self, registry: Registry) -> None:
        self.registry = registry

    def run_cs(
        self,
        env: Envelope,
        operation: str,
        payload: dict[str, Any],
        execute_fn,
    ) -> dict[str, Any]:
        trace = PolicyTrace()
        trace.add("inject")
        if env.profile not in ("scene", "explore", "builder", "runtime"):
            raise HubError("SCOPE_DENIED", "bad profile")
        trace.add("tenant")
        if not env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        op = self.registry.get(operation)
        trace.add("registry")
        if op is None:
            raise HubError("OPERATION_NOT_FOUND", operation)
        if not op.get("enabled", True):
            raise HubError("OPERATION_NOT_FOUND", "disabled")
        trace.add("rbac")
        if env.track == "selfpaw" and op.get("side_effects"):
            raise HubError("TRACK_ESCALATION_REQUIRED")
        trace.add("approval")
        level = op.get("approval_level", "L1")
        trace.add("gates")
        if not op.get("gates"):
            raise HubError("GATE_BLOCKED", "gates required")
        if env.profile not in WRITE_PROFILES and op.get("side_effects"):
            raise HubError("PROFILE_FORBIDS_SIDE_EFFECT")
        trace.add("scope")
        scoped = dict(payload)
        scoped["_scope_tenant"] = env.tenant_id
        trace.add("execute")
        result = execute_fn(op, scoped)
        trace.add("audit")
        result["_policy_trace"] = list(trace.steps)
        result["_approval_level"] = level
        return result
