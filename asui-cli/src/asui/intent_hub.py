"""SelfPaw Intent Hub：意图分类与升级 ΠPaw Working Task（Phase-0 内存+文件持久化）。"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class EscalateContext:
    tenant_id: str
    request_tenant_id: str
    user_id: str
    product_track: str = "selfpaw"
    role_ids: list[str] = field(default_factory=list)


@dataclass
class EscalateResponse:
    status: str
    working_task: dict[str, Any] | None = None
    intent: dict[str, Any] | None = None
    deny_reason: str = ""
    audit_id: str = ""


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class IntentEscalationHub:
    """实现 POST /intent/escalate 语义；禁止无 Evidence 静默升级经营类意图。"""

    def __init__(
        self,
        workspace_root: Path,
        *,
        policy_path: Path | None = None,
        tasks_store_path: Path | None = None,
        tenant_catalog_path: Path | None = None,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.policy_path = policy_path or (
            self.workspace_root / "configs" / "intent_escalation_policy.sample.json"
        )
        self.tasks_store_path = tasks_store_path or (
            self.workspace_root / "database" / "edh" / "working_tasks.json"
        )
        self.tenant_catalog_path = tenant_catalog_path or (
            self.workspace_root / "configs" / "tenant_catalog.sample.json"
        )
        self._policy = self._load_json(self.policy_path)
        self._tenant_catalog = self._load_json(self.tenant_catalog_path)

    @staticmethod
    def _load_json(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_tasks(self, store: dict) -> None:
        self.tasks_store_path.parent.mkdir(parents=True, exist_ok=True)
        self.tasks_store_path.write_text(
            json.dumps(store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _load_tasks(self) -> dict:
        if not self.tasks_store_path.is_file():
            return {"version": "1.0.0", "tasks": []}
        return self._load_json(self.tasks_store_path)

    def _rule_for_class(self, intent_class: str) -> dict | None:
        for rule in self._policy.get("rules", []):
            if rule.get("intent_class") == intent_class:
                return rule
        return None

    def _validate_tenant(self, intent: dict, ctx: EscalateContext) -> str | None:
        tid = intent.get("tenant_id", "")
        if tid != ctx.tenant_id or tid != ctx.request_tenant_id:
            return "TENANT_ISOLATION_VIOLATION"
        if ctx.product_track != "selfpaw":
            return "ESCALATION_REQUIRES_SELFPaw_SESSION"
        actor = intent.get("actor") or {}
        if actor.get("product_track") != "selfpaw":
            return "ACTOR_TRACK_MISMATCH"
        return None

    def _resolve_target(self, intent: dict, rule: dict) -> dict:
        explicit = intent.get("escalation_target")
        if explicit:
            return explicit
        return rule.get("default_target") or {}

    def escalate(self, intent: dict, ctx: EscalateContext) -> EscalateResponse:
        audit_id = f"aud-{uuid.uuid4().hex[:12]}"
        deny = self._validate_tenant(intent, ctx)
        if deny:
            return EscalateResponse(status="denied", deny_reason=deny, audit_id=audit_id)

        intent_class = intent.get("intent_class", "")
        rule = self._rule_for_class(intent_class)
        if not rule:
            return EscalateResponse(
                status="denied",
                deny_reason="UNKNOWN_INTENT_CLASS",
                audit_id=audit_id,
            )
        if not rule.get("allow_escalate"):
            return EscalateResponse(
                status="denied",
                deny_reason="ESCALATION_NOT_ALLOWED_FOR_CLASS",
                audit_id=audit_id,
            )

        evidence = intent.get("evidence_refs") or []
        if rule.get("requires_evidence") and len(evidence) < int(rule.get("min_evidence_count", 1)):
            return EscalateResponse(
                status="denied",
                deny_reason="EVIDENCE_REQUIRED",
                audit_id=audit_id,
            )

        target = self._resolve_target(intent, rule)
        if target.get("product_track") != "pipaw":
            return EscalateResponse(
                status="denied",
                deny_reason="INVALID_ESCALATION_TARGET",
                audit_id=audit_id,
            )

        now = _utc_now()
        task_id = f"wt-{uuid.uuid4().hex[:12]}"
        working_task = {
            "task_id": task_id,
            "tenant_id": intent["tenant_id"],
            "source_intent_id": intent.get("intent_id", ""),
            "source": "selfpaw_escalation",
            "product_track": "pipaw",
            "position_id": target.get("position_id", ""),
            "domain_id": target.get("domain_id", ""),
            "assignee_role_id": target.get("role_id", ""),
            "title": intent.get("summary") or intent.get("goal", ""),
            "goal": intent.get("goal", ""),
            "status": "open",
            "priority": intent.get("urgency", "normal"),
            "business_context": intent.get("business_context") or {},
            "evidence_refs": list(evidence),
            "audit_id": audit_id,
            "created_at": now,
            "updated_at": now,
        }

        store = self._load_tasks()
        store.setdefault("tasks", []).append(working_task)
        self._save_tasks(store)

        updated_intent = dict(intent)
        updated_intent["status"] = "escalated"
        updated_intent["updated_at"] = now
        if not updated_intent.get("escalation_target"):
            updated_intent["escalation_target"] = target

        return EscalateResponse(
            status="ok",
            working_task=working_task,
            intent=updated_intent,
            audit_id=audit_id,
        )

    def list_tasks(
        self,
        *,
        tenant_id: str,
        position_id: str | None = None,
        assignee_role_id: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        tasks = self._load_tasks().get("tasks", [])
        out: list[dict[str, Any]] = []
        for t in tasks:
            if t.get("tenant_id") != tenant_id:
                continue
            if position_id and t.get("position_id") != position_id:
                continue
            if assignee_role_id and t.get("assignee_role_id") != assignee_role_id:
                continue
            if status and t.get("status") != status:
                continue
            out.append(t)
        return out

    def reset_store(self) -> None:
        """测试用：清空 Working Task 存储。"""
        self._save_tasks({"version": "1.0.0", "tasks": []})
