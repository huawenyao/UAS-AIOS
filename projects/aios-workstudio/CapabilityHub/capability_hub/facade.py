"""WorkStudio 只调这组语义。内核仍是 uas_hub.Hub，禁止平行门禁。"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from uuid import uuid4

from capability_hub.hooks import HookBus
from capability_hub.paths import HUB_API, REPO
from capability_hub.profiles import load_matrix, skill_max_state
from capability_hub.skills import CATALOG, assert_transition_allowed

if str(HUB_API) not in sys.path:
    sys.path.insert(0, str(HUB_API))

from uas_hub.errors import Envelope, HubError, WM_DIMS  # noqa: E402
from uas_hub.hub import Hub  # noqa: E402

_COMPLETE_WM = {dim: dim for dim in WM_DIMS}


class CapabilityHub:
    def __init__(self, core: Hub) -> None:
        self.core = core
        self.hooks = HookBus()
        self.themes: dict[str, dict[str, Any]] = {}
        self.apps: dict[str, dict[str, Any]] = {}
        self.releases: dict[str, dict[str, Any]] = {}
        self.instances: dict[str, dict[str, Any]] = {}
        self.permission_changes: dict[str, dict[str, Any]] = {}
        self._seq = 0

    def __getattr__(self, name: str) -> Any:
        return getattr(self.core, name)

    @classmethod
    def from_repo(cls, root: Path | None = None) -> "CapabilityHub":
        return cls(Hub.from_repo(root or REPO))

    def matrix(self) -> dict[str, Any]:
        return load_matrix()

    def pack_list(self, env: Envelope) -> dict[str, Any]:
        if not env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        packs = []
        for graph in self.core.graphs._by_id.values():
            if graph.get("tenant_id") == env.tenant_id:
                packs.append(
                    {
                        "graph_id": graph["graph_id"],
                        "period": graph.get("period"),
                        "position_id": env.position_id,
                    }
                )
        return {"packs": packs}

    def pack_open(self, env: Envelope, position_id: str, cube_ok: bool = True) -> dict[str, Any]:
        pack = self.core.pack_open(env, position_id, cube_ok=cube_ok)
        pack["insights_open_count"] = len(self.core.insights.insights)
        pack["tasks_open_count"] = len(self.core.insights.tasks)
        return pack

    def insight_drill(
        self,
        env: Envelope,
        source_node_id: str,
        evidence_refs: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return self.core.insight_drill(env, source_node_id, evidence_refs)

    def insight_list(self, env: Envelope) -> dict[str, Any]:
        items = [i for i in self.core.insights.insights.values() if i.get("tenant_id") == env.tenant_id]
        return {"insights": items}

    def task_issue(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        return self.core.task_issue(env, payload)

    def task_return(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        task_id = str(payload.get("task_id") or "")
        task = self.core.insights.tasks.get(task_id)
        if not task:
            raise HubError("TASK_NOT_ISSUED")
        if task.get("tenant_id") != env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        task["status"] = "returned"
        task["return_reason"] = payload.get("reason") or "returned"
        task["note"] = payload.get("note") or ""
        drafted = self.core.evolution_draft(
            env,
            {"kind": "task_return", "task_id": task_id, "reason": task["return_reason"]},
        )
        self.core.audit.append(
            {
                "operation": "hub.scene.task.return",
                "tenant_id": env.tenant_id,
                "task_id": task_id,
                "changeset_id": drafted["changeset_id"],
            }
        )
        return {
            "task_id": task_id,
            "status": "returned",
            "changeset_id": drafted["changeset_id"],
            "auto_apply": False,
        }

    def skill_discover(self, env: Envelope) -> dict[str, Any]:
        env.profile = env.profile or "explore"
        return {"skills": [dict(item) for item in CATALOG], "profile": env.profile}

    def skill_preview(self, env: Envelope, skill_id: str) -> dict[str, Any]:
        self._skill_move(env, skill_id, "previewed")
        rec = next((s for s in CATALOG if s["skill_id"] == skill_id), {"skill_id": skill_id})
        return {"skill_id": skill_id, "state": "previewed", "summary": rec.get("summary", "")}

    def skill_cite(self, env: Envelope, skill_id: str, theme_id: str | None = None) -> dict[str, Any]:
        moved = self._skill_move(env, skill_id, "cited")
        if theme_id and theme_id in self.themes:
            used = self.themes[theme_id].setdefault("knowledge_used", [])
            used.append({"skill_id": skill_id, "installed": False})
        return {**moved, "installed": False}

    def skill_install(self, env: Envelope, skill_id: str) -> dict[str, Any]:
        return self._skill_move(env, skill_id, "installed")

    def skill_enable(self, env: Envelope, skill_id: str) -> dict[str, Any]:
        return self._skill_move(env, skill_id, "enabled")

    def skill_execute(self, env: Envelope, skill_id: str) -> dict[str, Any]:
        return self._skill_move(env, skill_id, "executed")

    def _skill_move(self, env: Envelope, skill_id: str, to_state: str) -> dict[str, Any]:
        assert_transition_allowed(env.profile, to_state)
        return self.core.skill_transition(env, skill_id, to_state)

    def theme_create(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        used = payload.get("knowledge_used") or []
        for item in used:
            if "installed" not in item:
                raise HubError("INVARIANT_FAILED", "knowledge_used.installed required")
        self._seq += 1
        theme_id = f"thm-{self._seq:04d}"
        rec = {
            "theme_id": theme_id,
            "title": payload.get("title") or theme_id,
            "task_id": payload.get("task_id"),
            "knowledge_used": [dict(x) for x in used],
            "wm": dict(payload.get("wm") or _COMPLETE_WM),
            "status": "draft",
            "tenant_id": env.tenant_id,
        }
        self.themes[theme_id] = rec
        if self.core.artifact is not None:
            rec["artifact"] = self.core.artifact.put("theme", rec)
        return rec

    def theme_update(self, env: Envelope, theme_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        rec = self._theme(theme_id, env.tenant_id)
        if "knowledge_used" in payload:
            for item in payload["knowledge_used"]:
                if "installed" not in item:
                    raise HubError("INVARIANT_FAILED", "knowledge_used.installed required")
            rec["knowledge_used"] = [dict(x) for x in payload["knowledge_used"]]
        if "title" in payload:
            rec["title"] = payload["title"]
        if "wm" in payload:
            rec["wm"] = dict(payload["wm"])
        return rec

    def theme_get(self, env: Envelope, theme_id: str) -> dict[str, Any]:
        return dict(self._theme(theme_id, env.tenant_id))

    def theme_promote(self, env: Envelope, theme_id: str) -> dict[str, Any]:
        rec = self._theme(theme_id, env.tenant_id)
        self.hooks.pre_promote(rec.get("wm") or {})
        rec["status"] = "promoted"
        return rec

    def app_normalize(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        theme_id = str(payload.get("theme_id") or "")
        theme = self._theme(theme_id, env.tenant_id)
        self._seq += 1
        app_id = f"app-{self._seq:04d}"
        rec = {
            "app_id": app_id,
            "theme_id": theme_id,
            "tenant_id": env.tenant_id,
            "status": "normalized",
            "title": theme.get("title"),
            "validated": False,
            "world_model_analysis": None,
            "template_id": None,
            "blueprint": None,
        }
        self.apps[app_id] = rec
        return rec

    def app_analyze_wm(self, env: Envelope, app_id: str) -> dict[str, Any]:
        rec = self._app(app_id, env.tenant_id)
        theme = self._theme(rec["theme_id"], env.tenant_id)
        rec["world_model_analysis"] = {
            "complete": all(theme.get("wm", {}).get(d) for d in WM_DIMS),
            "dims": dict(theme.get("wm") or {}),
        }
        rec["status"] = "analyzed"
        return rec

    def app_select_template(self, env: Envelope, app_id: str) -> dict[str, Any]:
        rec = self._app(app_id, env.tenant_id)
        rec["template_id"] = "uas-ltc-workbench"
        rec["status"] = "templated"
        return rec

    def app_design(self, env: Envelope, app_id: str) -> dict[str, Any]:
        rec = self._app(app_id, env.tenant_id)
        rec["blueprint"] = {
            "routes": ["/today", "/room/:object_ref", "/command"],
            "template_id": rec.get("template_id"),
        }
        rec["status"] = "designed"
        return rec

    def app_generate(self, env: Envelope, app_id: str) -> dict[str, Any]:
        rec = self._app(app_id, env.tenant_id)
        self.hooks.pre_generate_assets(rec)
        rec["generated"] = True
        rec["status"] = "generated"
        if self.core.artifact is not None:
            rec["artifact"] = self.core.artifact.put("blueprint", rec["blueprint"] or {})
        return rec

    def app_validate(self, env: Envelope, app_id: str, pass_invariants: bool = True) -> dict[str, Any]:
        rec = self._app(app_id, env.tenant_id)
        rec["validated"] = bool(pass_invariants)
        rec["status"] = "validated" if pass_invariants else "validate_failed"
        return {"app_id": app_id, "ok": rec["validated"], "status": rec["status"]}

    def app_release(self, env: Envelope, app_id: str) -> dict[str, Any]:
        rec = self._app(app_id, env.tenant_id)
        self.hooks.pre_release(rec)
        rec["status"] = "released"
        self._seq += 1
        release_id = f"rel-{self._seq:04d}"
        release = {
            "release_id": release_id,
            "app_id": app_id,
            "tenant_id": env.tenant_id,
            "immutable": True,
        }
        self.releases[release_id] = release
        rec["release_id"] = release_id
        if self.core.artifact is not None:
            release["artifact"] = self.core.artifact.put("release", release)
        return release

    def instance_deploy(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        release_id = str(payload.get("release_id") or "")
        release = self.releases.get(release_id)
        if not release:
            raise HubError("INVARIANT_FAILED", "release missing")
        if release.get("tenant_id") != env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        self._seq += 1
        instance_id = f"inst-{self._seq:04d}"
        rec = {
            "instance_id": instance_id,
            "release_id": release_id,
            "task_id": payload.get("task_id"),
            "tenant_id": env.tenant_id,
            "track": env.track,
            "status": "deployed",
            "live_wm_id": "wm-cm",
        }
        self.instances[instance_id] = rec
        if payload.get("task_id"):
            task = self.core.insights.tasks.get(str(payload["task_id"]))
            if task:
                task["instance_id"] = instance_id
        return rec

    def instance_list_artifacts(self, env: Envelope, instance_id: str) -> dict[str, Any]:
        rec = self.instances.get(instance_id)
        if not rec or rec.get("tenant_id") != env.tenant_id:
            raise HubError("SCOPE_DENIED", instance_id)
        arts = []
        release = self.releases.get(rec["release_id"])
        if release and release.get("artifact"):
            arts.append(release["artifact"])
        app = self.apps.get(next((a["app_id"] for a in self.apps.values() if a.get("release_id") == rec["release_id"]), ""), {})
        if app.get("artifact"):
            arts.append(app["artifact"])
        return {"instance_id": instance_id, "artifacts": arts or [{"kind": "release", "release_id": rec["release_id"]}]}

    def instance_escalate(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        refs = payload.get("evidence_refs") or []
        if env.track == "selfpaw" and not refs:
            raise HubError("TRACK_ESCALATION_REQUIRED")
        env.track = "pipaw"
        return {"track": "pipaw", "evidence_refs": refs, "status": "escalated"}

    def thread_start(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        thread_id = env.thread_id or str(payload.get("thread_id") or f"th-{uuid4().hex[:8]}")
        self.core.bind_thread(thread_id, env.profile)
        env.thread_id = thread_id
        allow = self.core.list_tools(env)
        if self.core.inner_loop is not None:
            inner_id = self.core.inner_loop.start_thread(env.profile, allow, env.track)
        else:
            inner_id = thread_id
        return {
            "thread_id": thread_id,
            "inner_thread_id": inner_id,
            "profile": env.profile,
            "tools": allow,
            "matrix": load_matrix()["profiles"][env.profile],
        }

    def wm_get(self, env: Envelope, world_model_id: str, lifetime: str, version: int | None = None) -> dict[str, Any]:
        return self.core.wm.get(world_model_id, lifetime, version)

    def wm_patch(self, env: Envelope, world_model_id: str, lifetime: str, body: dict[str, Any]) -> dict[str, Any]:
        if lifetime == "live":
            raise HubError("INVARIANT_FAILED", "live only via cycle_step")
        return self.core.wm_patch(env, world_model_id, lifetime, body)

    def audit_query(self, env: Envelope, query: str = "") -> dict[str, Any]:
        records = list(self.core.audit)
        if query:
            records = [r for r in records if query in str(r)]
        return {"records": records}

    def permission_changeset(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        drafted = self.core.evolution_draft(env, {"kind": "permission", **payload})
        rec = {
            "changeset_id": drafted["changeset_id"],
            "kind": "permissionChangeSet",
            "payload": dict(payload),
            "approved": True,
            "auto_apply": False,
        }
        self.permission_changes[rec["changeset_id"]] = rec
        return rec

    def iam_bind(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        changeset_id = str(payload.get("changeset_id") or "")
        rec = self.permission_changes.get(changeset_id)
        if rec is None or rec.get("kind") != "permissionChangeSet":
            raise HubError("INVARIANT_FAILED", "permissionChangeSet required")
        actor_id = str(payload.get("actor_id") or env.actor_id)
        position_id = str(payload.get("position_id") or "")
        if self.core.iam is None:
            return {"actor_id": actor_id, "tenant_id": env.tenant_id, "position_id": position_id, "changeset_id": changeset_id}
        return {
            **self.core.iam.bind(actor_id, env.tenant_id, position_id),
            "changeset_id": changeset_id,
        }

    def invoke_cs(self, env: Envelope, operation: str, payload: dict[str, Any] | None = None, claimed_profile: str | None = None) -> dict[str, Any]:
        if operation.startswith("cs.") and env.profile != "runtime":
            self.hooks.pre_tool_use(env.profile, operation)
        result = self.core.invoke_cs(env, operation, payload, claimed_profile)
        self.hooks.post_tool_use(self.core.audit, {"operation": operation, "profile": env.profile})
        return result

    def _theme(self, theme_id: str, tenant_id: str) -> dict[str, Any]:
        rec = self.themes.get(theme_id)
        if not rec or rec.get("tenant_id") != tenant_id:
            raise HubError("SCOPE_DENIED", theme_id)
        return rec

    def _app(self, app_id: str, tenant_id: str) -> dict[str, Any]:
        rec = self.apps.get(app_id)
        if not rec or rec.get("tenant_id") != tenant_id:
            raise HubError("SCOPE_DENIED", app_id)
        return rec

    def explain(self, code: str) -> dict[str, Any]:
        return self.core.explain(code)
