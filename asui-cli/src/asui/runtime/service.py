"""多 subapp 共用的 UAS Runtime Service。"""

from __future__ import annotations

import json
from pathlib import Path

from .runtime_manager import RuntimeManager


class UASRuntimeService:
    """发现、校验并运行多个 sub uas app。"""

    def __init__(self, workspace_root: Path, projects_root: str = "projects") -> None:
        self.workspace_root = workspace_root.resolve()
        self.projects_root = (self.workspace_root / projects_root).resolve()

    def discover_apps(self) -> dict[str, Path]:
        apps: dict[str, Path] = {}
        if not self.projects_root.exists():
            return apps

        for manifest_path in sorted(self.projects_root.glob("*/configs/platform_manifest.json")):
            app_root = manifest_path.parents[1]
            apps[app_root.name] = app_root
        return apps

    def list_apps(self) -> list[dict]:
        apps = []
        for app_id, app_root in self.discover_apps().items():
            manifest = self._load_json(app_root / "configs" / "platform_manifest.json")
            apps.append(
                {
                    "app_id": app_id,
                    "app_root": str(app_root),
                    "technical_base": manifest["platform"]["technical_base"],
                    "runtime": manifest["platform"]["runtime"],
                }
            )
        return apps

    def get_runtime(self, app_id: str) -> RuntimeManager:
        apps = self.discover_apps()
        if app_id not in apps:
            raise KeyError(f"Unknown subapp: {app_id}")
        return RuntimeManager(apps[app_id])

    def validate_app(self, app_id: str) -> dict:
        runtime = self.get_runtime(app_id)
        validation = runtime.validate_assets()
        validation["app_id"] = app_id
        return validation

    def run_app(
        self,
        app_id: str,
        topic: str,
        payload: dict | None = None,
        evaluate: bool = False,
    ) -> dict:
        runtime = self.get_runtime(app_id)
        result = runtime.run(topic, payload=payload, evaluate=evaluate)
        result["app_id"] = app_id
        return result

    def _load_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))
