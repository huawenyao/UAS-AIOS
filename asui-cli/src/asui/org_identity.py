"""SelfPaw 企业版组织身份解析（REQ-EDH-SP-001 Phase-0 原型）。"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class OrgSessionRequest:
    tenant_id: str
    user_id: str
    position_id: str | None = None
    product_track: str = "selfpaw"


@dataclass
class OrgSessionContext:
    status: str
    tenant_id: str = ""
    user_id: str = ""
    product_track: str = "selfpaw"
    org_unit_id: str = ""
    position_id: str = ""
    position_code: str = ""
    domain_id: str = ""
    role_ids: list[str] = field(default_factory=list)
    data_scopes: list[dict[str, Any]] = field(default_factory=list)
    feature_flags: dict[str, Any] = field(default_factory=dict)
    deny_reason: str = ""


class OrgIdentityResolver:
    """从租户目录 + RBAC 模板解析企业版用户上下文。"""

    def __init__(
        self,
        workspace_root: Path,
        *,
        tenant_catalog_path: Path | None = None,
        rbac_path: Path | None = None,
        feature_flags_path: Path | None = None,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.tenant_catalog_path = tenant_catalog_path or (
            self.workspace_root / "configs" / "tenant_catalog.sample.json"
        )
        self.rbac_path = rbac_path or (
            self.workspace_root / "configs" / "enterprise_rbac_template.json"
        )
        self.feature_flags_path = feature_flags_path or (
            self.workspace_root / "configs" / "selfpaw_enterprise.feature_flags.json"
        )

    @staticmethod
    def _load_json(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _tenant(self, tenant_id: str) -> dict | None:
        catalog = self._load_json(self.tenant_catalog_path)
        for t in catalog.get("tenants", []):
            if t.get("tenant_id") == tenant_id:
                return t
        return None

    def _position(self, tenant: dict, position_id: str | None, user_id: str) -> dict | None:
        positions = tenant.get("positions", [])
        if position_id:
            for p in positions:
                if p.get("id") == position_id:
                    return p
        for p in positions:
            if p.get("default_product_track") == "selfpaw":
                return p
        return positions[0] if positions else None

    def _roles_for_position(self, position_code: str) -> list[str]:
        rbac = self._load_json(self.rbac_path)
        out: list[str] = []
        for role in rbac.get("roles", []):
            if role.get("product_track") != "selfpaw":
                continue
            if position_code == "SALES_REP" and role.get("role_id") == "role.sales_rep":
                out.append(role["role_id"])
            elif position_code == "HR_GENERALIST" and role.get("role_id") == "role.employee":
                out.append(role["role_id"])
            elif role.get("role_id") == "role.employee" and not out:
                out.append(role["role_id"])
        return out or ["role.employee"]

    def resolve(self, req: OrgSessionRequest) -> OrgSessionContext:
        flags = self._load_json(self.feature_flags_path).get("flags", {})
        if not flags.get("enterprise_mode"):
            return OrgSessionContext(status="denied", deny_reason="ENTERPRISE_MODE_DISABLED")

        tenant = self._tenant(req.tenant_id)
        if not tenant or tenant.get("status") != "active":
            return OrgSessionContext(status="denied", deny_reason="TENANT_NOT_FOUND")

        position = self._position(tenant, req.position_id, req.user_id)
        if not position:
            return OrgSessionContext(status="denied", deny_reason="POSITION_NOT_FOUND")

        if position.get("default_product_track") != "selfpaw" and req.product_track == "selfpaw":
            pass

        code = position.get("code", "")
        role_ids = self._roles_for_position(code)
        rbac = self._load_json(self.rbac_path)
        data_scopes: list[dict] = []
        for role in rbac.get("roles", []):
            if role.get("role_id") in role_ids:
                data_scopes.extend(role.get("default_data_scopes", []))

        return OrgSessionContext(
            status="ok",
            tenant_id=req.tenant_id,
            user_id=req.user_id,
            product_track=req.product_track,
            org_unit_id="ou-sales" if code == "SALES_REP" else tenant.get("org_units", [{}])[0].get("id", ""),
            position_id=position.get("id", ""),
            position_code=code,
            domain_id=position.get("domain_id", ""),
            role_ids=role_ids,
            data_scopes=data_scopes,
            feature_flags=flags,
        )
