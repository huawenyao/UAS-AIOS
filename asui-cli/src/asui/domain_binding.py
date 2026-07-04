"""岗位 Domain 自动绑定（REQ-EDH-SP-002 Phase-0 原型）。"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DomainFragment:
    domain_id: str
    display_name: str
    capability_whitelist: list[str] = field(default_factory=list)
    compliance_tags: list[str] = field(default_factory=list)
    prompt_context: str = ""


class DomainBindingLoader:
    """HR 岗位码 → Domain Pack 片段，供 Runner / Prompt 注入。"""

    def __init__(
        self,
        workspace_root: Path,
        *,
        bindings_path: Path | None = None,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.bindings_path = bindings_path or (
            self.workspace_root / "configs" / "role_domain_bindings.json"
        )

    def _catalog(self) -> dict:
        return json.loads(self.bindings_path.read_text(encoding="utf-8"))

    def bind_by_position_code(self, position_code: str) -> DomainFragment | None:
        for item in self._catalog().get("bindings", []):
            if item.get("position_code") == position_code:
                whitelist = list(item.get("capability_whitelist", []))
                prompt = (
                    f"岗位域 {item.get('display_name')}；"
                    f"可用能力 {', '.join(whitelist[:6])}"
                    f"{'...' if len(whitelist) > 6 else ''}"
                )
                return DomainFragment(
                    domain_id=item.get("domain_id", ""),
                    display_name=item.get("display_name", ""),
                    capability_whitelist=whitelist,
                    compliance_tags=list(item.get("compliance_tags", [])),
                    prompt_context=prompt,
                )
        return None

    def bind_for_session(self, session: dict[str, Any]) -> DomainFragment | None:
        code = session.get("position_code") or session.get("position", {}).get("code")
        if not code and session.get("position_id"):
            code = self._code_from_position_id(session.get("position_id", ""))
        if not code:
            return None
        return self.bind_by_position_code(code)

    def _code_from_position_id(self, position_id: str) -> str:
        mapping = {
            "pos-sales-rep": "SALES_REP",
            "pos-cs-agent": "CS_AGENT",
            "pos-hr": "HR_GENERALIST",
        }
        return mapping.get(position_id, "")

    def runtime_prompt_injection(self, session: dict[str, Any]) -> dict[str, Any]:
        frag = self.bind_for_session(session)
        if not frag:
            return {"domain_bound": False}
        return {
            "domain_bound": True,
            "domain_id": frag.domain_id,
            "capability_whitelist": frag.capability_whitelist,
            "compliance_tags": frag.compliance_tags,
            "prompt_fragment": frag.prompt_context,
        }
