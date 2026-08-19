"""结构化存储 — 仓储模式持久化。

规约来源：docs/lifewake/DOMAIN_MODEL.md、README.md
替代散落 JSON 文件，提供统一仓储接口。仍基于文件系统（无 SQL 依赖），
但每个实体类型有独立仓储，写入带 schema 校验。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import schemas

DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "database"


class Repository:
    """单实体类型的文件仓储。"""

    def __init__(self, root: Path, sub: str) -> None:
        self.dir = root / sub
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        safe = "".join(c for c in key if c.isalnum() or c in "-_.")
        return self.dir / f"{safe}.json"

    def save(self, key: str, data: dict[str, Any]) -> dict[str, Any]:
        data = {**data, "_key": key}
        with self._path(key).open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, default=str)
        return data

    def load(self, key: str) -> dict[str, Any] | None:
        path = self._path(key)
        if not path.exists():
            return None
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)

    def list_all(self) -> list[dict[str, Any]]:
        items = []
        for path in sorted(self.dir.glob("*.json")):
            with path.open(encoding="utf-8") as fh:
                items.append(json.load(fh))
        return items

    def delete(self, key: str) -> bool:
        path = self._path(key)
        if path.exists():
            path.unlink()
            return True
        return False


class Store:
    """LifeWake 持久化门面：runs / feedback / cognitive_state / audit / keepsakes / consents。"""

    def __init__(self, root: Path | str | None = None) -> None:
        self.root = Path(root) if root else DEFAULT_ROOT
        self.runs = Repository(self.root, "runs")
        self.feedback = Repository(self.root, "feedback")
        self.cognitive_state = Repository(self.root, "cognitive_state")
        self.audit = Repository(self.root, "audit")
        self.keepsakes = Repository(self.root, "keepsakes")
        self.consents = Repository(self.root, "consents")

    def save_run(self, run_id: str, run: dict[str, Any]) -> dict[str, Any]:
        return self.runs.save(run_id, run)

    def save_envelope(self, envelope: dict[str, Any]) -> dict[str, Any]:
        """保存 RitualEnvelope（带 schema 校验，红线 15）。"""
        schemas.validate_ritual_envelope(envelope)
        key = envelope.get("envelope_id", envelope.get("ritual_id", "unknown"))
        return self.keepsakes.save(key, envelope)

    def append_audit_jsonl(self, event: dict[str, Any]) -> None:
        """审计事件追加到 JSONL（红线 16 净化）。"""
        schemas.validate_audit_event(event)
        path = self.audit.dir / "execution_log.jsonl"
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")

    def save_consent(self, consent_id: str, consent: dict[str, Any]) -> dict[str, Any]:
        schemas.validate_entity("ConsentGrant", consent)
        return self.consents.save(consent_id, consent)

    def save_changeset(
        self, changeset_id: str, changeset: dict[str, Any]
    ) -> dict[str, Any]:
        schemas.validate_entity("ChangeSet", changeset)
        return self.cognitive_state.save(changeset_id, changeset)

    def save_feedback(
        self, feedback_id: str, feedback: dict[str, Any]
    ) -> dict[str, Any]:
        return self.feedback.save(feedback_id, feedback)
