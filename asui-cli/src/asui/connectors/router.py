"""能力服务路由：registry → 权限 → connector.invoke。"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .base import InvokeContext, InvokeResult, SystemConnector
from .mock_bpm import BpmMockConnector
from .mock_crm import CrmMockConnector
from .mock_itsm import ItsmMockConnector
from .mock_oa import OaMockConnector

OP_REF_RE = re.compile(r"^(cs\.[a-z][a-z0-9_.]+)\.([a-z][a-z0-9_]+)$")


@dataclass
class CapabilityInvokeContext(InvokeContext):
    request_tenant_id: str = ""


@dataclass
class CapabilityInvokeResponse:
    status: str
    output: dict[str, Any] = field(default_factory=dict)
    audit_id: str = ""
    deny_reason: str = ""
    connector_id: str = ""


class CapabilityServiceRouter:
    def __init__(
        self,
        workspace_root: Path,
        *,
        capability_registry_path: Path | None = None,
        rbac_path: Path | None = None,
        connectors_path: Path | None = None,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.capability_registry_path = capability_registry_path or (
            self.workspace_root / "configs" / "capability_registry.json"
        )
        self.rbac_path = rbac_path or (self.workspace_root / "configs" / "enterprise_rbac_template.json")
        self.connectors_path = connectors_path or (self.workspace_root / "configs" / "connectors.json")
        self._registry = self._load_json(self.capability_registry_path)
        self._rbac = self._load_json(self.rbac_path)
        self._connectors_cfg = self._load_json(self.connectors_path)
        self._connectors: dict[str, SystemConnector] = {
            CrmMockConnector.connector_id: CrmMockConnector(),
            OaMockConnector.connector_id: OaMockConnector(),
            ItsmMockConnector.connector_id: ItsmMockConnector(),
            BpmMockConnector.connector_id: BpmMockConnector(),
        }
        self._service_index = self._build_service_index()

    @staticmethod
    def _load_json(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _build_service_index(self) -> dict[str, dict]:
        index: dict[str, dict] = {}
        for svc in self._registry.get("services", []):
            index[svc["id"]] = svc
        return index

    def list_services(self) -> list[dict[str, Any]]:
        return [
            {
                "id": s["id"],
                "connector_id": s.get("connector_id"),
                "operations": [o["name"] for o in s.get("operations", [])],
            }
            for s in self._registry.get("services", [])
        ]

    def _authorize(self, ctx: CapabilityInvokeContext, operation_ref: str) -> str | None:
        if ctx.tenant_id != ctx.request_tenant_id:
            return "TENANT_ISOLATION_VIOLATION"
        roles = {r["role_id"]: r for r in self._rbac.get("roles", [])}
        for role_id in ctx.role_ids:
            role = roles.get(role_id)
            if not role:
                continue
            if role.get("product_track") not in (ctx.product_track, "shared"):
                return "PRODUCT_TRACK_DENIED"
            if operation_ref in role.get("denied_operations", []):
                return "OPERATION_DENIED"
            if operation_ref in role.get("allowed_operations", []):
                return None
        return "OPERATION_DENIED"

    def invoke(
        self,
        operation_ref: str,
        payload: dict[str, Any],
        ctx: CapabilityInvokeContext,
    ) -> CapabilityInvokeResponse:
        audit_id = f"aud-{uuid.uuid4().hex[:12]}"
        m = OP_REF_RE.match(operation_ref)
        if not m:
            return CapabilityInvokeResponse(
                status="denied",
                deny_reason="INVALID_OPERATION_REF",
                audit_id=audit_id,
            )
        service_id, op_name = m.group(1), m.group(2)
        deny = self._authorize(ctx, operation_ref)
        if deny:
            return CapabilityInvokeResponse(status="denied", deny_reason=deny, audit_id=audit_id)

        svc = self._service_index.get(service_id)
        if not svc or not svc.get("enabled", True):
            return CapabilityInvokeResponse(
                status="denied",
                deny_reason="SERVICE_NOT_FOUND",
                audit_id=audit_id,
            )

        op_def = next((o for o in svc.get("operations", []) if o["name"] == op_name), None)
        if not op_def:
            return CapabilityInvokeResponse(
                status="denied",
                deny_reason="OPERATION_NOT_FOUND",
                audit_id=audit_id,
            )

        connector_id = svc.get("connector_id", "")
        connector = self._connectors.get(connector_id)
        if not connector:
            return CapabilityInvokeResponse(
                status="error",
                deny_reason="CONNECTOR_NOT_IMPLEMENTED",
                audit_id=audit_id,
                connector_id=connector_id,
            )

        inner_ctx = InvokeContext(
            tenant_id=ctx.tenant_id,
            user_id=ctx.user_id,
            role_ids=ctx.role_ids,
            product_track=ctx.product_track,
            session_id=ctx.session_id,
            agent_id=ctx.agent_id,
        )
        result = connector.invoke(op_name, payload, inner_ctx)
        if result.status != "ok":
            return CapabilityInvokeResponse(
                status="error",
                deny_reason=result.message,
                audit_id=audit_id,
                connector_id=connector_id,
            )
        return CapabilityInvokeResponse(
            status="ok",
            output=result.output,
            audit_id=audit_id,
            connector_id=connector_id,
        )
