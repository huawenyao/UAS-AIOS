#!/usr/bin/env python3
"""SelfPaw 企业会话：组织身份 + 岗位 Domain 绑定。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve()
APP_ROOT = _SCRIPT.parents[1]
WORKSPACE = APP_ROOT.parents[1]
sys.path.insert(0, str(WORKSPACE / "asui-cli" / "src"))

from asui.domain_binding import DomainBindingLoader  # noqa: E402
from asui.org_identity import OrgIdentityResolver, OrgSessionRequest  # noqa: E402


def main() -> int:
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    topic = payload.get("topic", "个人效率任务")
    tenant_id = payload.get("tenant_id", "t-acme-demo")
    user_id = payload.get("user_id", "u-employee-1001")
    position_id = payload.get("position_id", "pos-sales-rep")

    resolver = OrgIdentityResolver(WORKSPACE)
    session = resolver.resolve(
        OrgSessionRequest(tenant_id=tenant_id, user_id=user_id, position_id=position_id)
    )
    if session.status != "ok":
        print(json.dumps({"status": "denied", "deny_reason": session.deny_reason}, ensure_ascii=False))
        return 1

    domain = DomainBindingLoader(WORKSPACE).runtime_prompt_injection(
        {"position_code": session.position_code, "position_id": session.position_id}
    )

    out = {
        "status": "completed",
        "topic": topic,
        "org_identity_bound": True,
        "session": {
            "tenant_id": session.tenant_id,
            "user_id": session.user_id,
            "position_code": session.position_code,
            "domain_id": session.domain_id,
            "role_ids": session.role_ids,
            "data_scopes": session.data_scopes,
        },
        "domain_binding": domain,
        "intent_model": [
            f"议题：{topic}",
            f"岗位域：{domain.get('domain_id', session.domain_id)}",
            domain.get("prompt_fragment", ""),
        ],
        "escalation_ready": bool(domain.get("domain_bound")),
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
