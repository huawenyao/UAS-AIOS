"""上下文注入器。"""

from __future__ import annotations

import json
from pathlib import Path


class ContextInjector:
    """从 sub uas app 中提取运行时所需的上下文。"""

    def inject(self, app_root: Path, topic: str, payload: dict | None = None) -> dict:
        configs_dir = app_root / "configs"
        skills_dir = app_root / ".claude" / "skills"
        docs_dir = app_root / "docs"

        context = {
            "app_root": str(app_root),
            "topic": topic,
            "payload": payload or {},
            "claude_summary": self._read_text(app_root / "CLAUDE.md"),
            "configs": self._load_json_files(configs_dir),
            "skills": sorted(str(path.relative_to(app_root)) for path in skills_dir.glob("*.md")) if skills_dir.exists() else [],
            "docs": sorted(str(path.relative_to(app_root)) for path in docs_dir.glob("*.md")) if docs_dir.exists() else [],
        }
        return context

    def _load_json_files(self, directory: Path) -> dict:
        if not directory.exists():
            return {}

        loaded = {}
        for path in sorted(directory.glob("*.json")):
            loaded[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        return loaded

    def _read_text(self, path: Path) -> str:
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")
