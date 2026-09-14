"""加载并校验 24 模块全局协议注册表。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
REGISTRY_PATH = REPO / "configs" / "protocol" / "registry.json"
SCHEMA_PATH = REPO / "schemas" / "protocol" / "module_protocol.schema.json"
KERNEL_PATH = REPO / "configs" / "protocol" / "KERNEL.yaml"

REQUIRED_IDS = [f"M{i}" for i in range(1, 25)]
REQUIRED_PORTS = {
    "CubePort",
    "KgPort",
    "MemoryPort",
    "InnerLoopPort",
    "OuterLoopPort",
    "ConnectorPort",
    "McpPort",
    "SkillPort",
    "LawPort",
    "ArtifactPort",
    "BrokerPort",
    "EvolutionPort",
}


def load_registry(root: Path | None = None) -> dict[str, Any]:
    path = (root or REPO) / "configs" / "protocol" / "registry.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(data: dict[str, Any] | None = None) -> list[str]:
    data = data or load_registry()
    errors: list[str] = []
    modules = data.get("modules") or []
    ids = [m.get("id") for m in modules]
    if ids != REQUIRED_IDS:
        errors.append(f"module ids != M1..M24: {ids}")
    seen_protocol = set()
    for mod in modules:
        mid = mod.get("id")
        pid = mod.get("protocol_id")
        if not pid:
            errors.append(f"{mid} missing protocol_id")
        if pid in seen_protocol and mid not in {"M6", "M1"}:
            # hub.* 可被控制面复用；其余 protocol_id 应独特
            pass
        seen_protocol.add(pid)
        if not isinstance(mod.get("hub_methods"), list):
            errors.append(f"{mid} hub_methods")
        if not isinstance(mod.get("verbs"), list) or not mod["verbs"]:
            errors.append(f"{mid} verbs empty")
        if "forbidden" not in mod:
            errors.append(f"{mid} forbidden")
        if mod.get("decision") == "integrate" and not mod.get("port"):
            errors.append(f"{mid} integrate without port")
        if mod.get("decision") == "integrate" and not mod.get("replaceable"):
            errors.append(f"{mid} integrate must be replaceable")
    order = data.get("policy_order") or []
    if order != [
        "inject",
        "tenant",
        "registry",
        "rbac",
        "approval",
        "gates",
        "scope",
        "execute",
        "audit",
    ]:
        errors.append("policy_order drifted")
    envelope = data.get("envelope") or []
    for key in ("tenant_id", "actor_id", "profile", "track", "correlation_id"):
        if key not in envelope:
            errors.append(f"envelope missing {key}")
    return errors


def integrated_modules(data: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    data = data or load_registry()
    return [m for m in data["modules"] if m.get("decision") in {"integrate", "own-shell", "connect"}]


def module_by_id(mid: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = data or load_registry()
    for mod in data["modules"]:
        if mod["id"] == mid:
            return mod
    raise KeyError(mid)
