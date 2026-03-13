"""多 subapp 共用的 UAS Runtime Service。"""

from __future__ import annotations

import json
from pathlib import Path

from .capability_registry import CapabilityRegistry
from .cognitive_state_store import slugify
from .queue_manager import QueueManager
from .runtime_manager import RuntimeManager
from .service_registry import ServiceRegistry


class UASRuntimeService:
    """发现、校验并运行多个 sub uas app。"""

    def __init__(self, workspace_root: Path, projects_root: str = "projects") -> None:
        self.workspace_root = workspace_root.resolve()
        self.projects_root = (self.workspace_root / projects_root).resolve()
        self.registry = ServiceRegistry(self.workspace_root, self.projects_root)
        self.queue = QueueManager(self.projects_root)

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
            registry = self._safe_load_json(app_root / "database" / "capabilities" / "registry.json")
            if registry is None:
                configs = self._load_configs(app_root)
                registry = CapabilityRegistry(app_root, configs).build()
            health = self.health_check(app_id)
            apps.append(
                self.registry.build_entry(app_id, app_root, manifest, registry, health)
            )
        self.registry.save(apps)
        return apps

    def registry_snapshot(self) -> dict:
        entries = self.list_apps()
        return {
            "registry_path": str(self.registry.registry_path),
            "entries": entries,
        }

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

    def health_check(self, app_id: str) -> dict:
        validation = self.validate_app(app_id)
        return {
            "status": "healthy" if validation["status"] == "ok" else "degraded",
            "missing_assets": validation.get("missing", []),
            "queue": self.queue.stats(),
        }

    def get_cognitive_state(self, app_id: str, topic_slug: str | None = None, topic: str | None = None) -> dict:
        apps = self.discover_apps()
        if app_id not in apps:
            raise KeyError(f"Unknown subapp: {app_id}")
        if topic_slug is None:
            if topic is None:
                raise ValueError("topic_slug or topic must be provided")
            topic_slug = slugify(topic)
        state_path = apps[app_id] / "database" / "cognitive_state" / f"{topic_slug}.json"
        return self._load_json(state_path)

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

    def enqueue_job(self, app_id: str, topic: str, payload: dict | None = None, evaluate: bool = False) -> dict:
        path = self.queue.enqueue(app_id, topic, payload=payload, evaluate=evaluate)
        return {"status": "queued", "job_path": str(path)}

    def process_next_job(self) -> dict:
        item = self.queue.pop_next()
        if item is None:
            return {"status": "empty"}
        job, path = item
        result = self.run_app(job["app_id"], job["topic"], payload=job.get("payload"), evaluate=job.get("evaluate", False))
        self.queue.complete(path, result)
        return {"status": "processed", "job_id": job["job_id"], "result": result}

    def queue_status(self) -> dict:
        return self.queue.stats()

    def _load_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _safe_load_json(self, path: Path) -> dict | None:
        if not path.exists():
            return None
        return self._load_json(path)

    def _load_configs(self, app_root: Path) -> dict:
        configs_dir = app_root / "configs"
        loaded = {}
        for path in sorted(configs_dir.glob("*.json")):
            loaded[path.stem] = self._load_json(path)
        return loaded
