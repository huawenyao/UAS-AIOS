"""Service Registry for UAS Runtime Service."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


class ServiceRegistry:
    """管理 subapp 服务登记与状态快照。"""

    def __init__(self, workspace_root: Path, projects_root: Path) -> None:
        self.workspace_root = workspace_root
        self.projects_root = projects_root
        self.registry_path = self.projects_root / ".service_registry" / "registry.json"
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

    def build_entry(self, app_id: str, app_root: Path, manifest: dict, capability_registry: dict | None, health: dict) -> dict:
        capability_tags = self._extract_capability_tags(capability_registry)
        return {
            "app_id": app_id,
            "app_root": str(app_root),
            "version": manifest.get("version", "unknown"),
            "technical_base": manifest["platform"]["technical_base"],
            "runtime": manifest["platform"]["runtime"],
            "capability_tags": capability_tags,
            "health": health,
            "updated_at": datetime.now(UTC).isoformat(),
        }

    def save(self, entries: list[dict]) -> Path:
        self.registry_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
        return self.registry_path

    def load(self) -> list[dict]:
        if not self.registry_path.exists():
            return []
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def _extract_capability_tags(self, capability_registry: dict | None) -> list[str]:
        if not capability_registry:
            return []
        tags = set()
        for agent in capability_registry.get("agents", []):
            if agent.get("dimension"):
                tags.add(f"agent:{agent['dimension']}")
        for system in capability_registry.get("systems", []):
            if system.get("type"):
                tags.add(f"system:{system['type']}")
        return sorted(tags)
