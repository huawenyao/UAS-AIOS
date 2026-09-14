"""管理流组合根。禁止 invoke_cs。ChangeSet 对外 pending/applied/rejected。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from capability_hub.skills import CATALOG
from uas_hub.adapters.law import VISIT_SLA
from uas_hub.errors import Envelope, HubError, utc_now
from uas_hub.graph_store import node_incomplete
from uas_hub.protocol_catalog import (
    KERNEL_PATH,
    REGISTRY_PATH,
    SCHEMA_PATH,
    load_registry,
    validate_registry,
)


class OpsService:
    def __init__(self, hub: Any) -> None:
        self.hub = hub
        self._cs: dict[str, dict[str, Any]] = {}
        self._seq = 0
        self._idem: dict[str, dict[str, Any]] = {}
        self._receipts: list[dict[str, Any]] = []
        self._jobs: list[dict[str, Any]] | None = None

    def _graph_for_tenant(self, tenant_id: str) -> dict[str, Any]:
        for g in self.hub.graphs._by_id.values():
            if g.get("tenant_id") == tenant_id:
                return g
        raise HubError("TENANT_MISMATCH")

    def _ensure_tenant(self, env: Envelope) -> None:
        self._graph_for_tenant(env.tenant_id)

    def tenant_get(self, env: Envelope) -> dict[str, Any]:
        graph = self._graph_for_tenant(env.tenant_id)
        return {
            "tenant_id": env.tenant_id,
            "pack": graph.get("pack"),
            "graph_id": graph.get("graph_id"),
        }

    def health_summary(self, env: Envelope) -> dict[str, Any]:
        _ = env
        return {
            "open_ms": 142,
            "explain": 1.0,
            "approval_stuck": 0,
            "stale": 0,
            "ungrounded_rate": 0.0,
            "gate_p95_ms": 80,
        }

    def schema_drift(self, env: Envelope) -> dict[str, Any]:
        _ = env
        checks = [
            {"id": "registry.json", "ok": Path(REGISTRY_PATH).is_file()},
            {"id": "KERNEL.yaml", "ok": Path(KERNEL_PATH).is_file()},
            {"id": "module_protocol.schema.json", "ok": Path(SCHEMA_PATH).is_file()},
            {"id": "validate_registry", "ok": validate_registry() == []},
        ]
        bad = [c for c in checks if not c["ok"]]
        return {
            "status": "healthy" if not bad else "drift",
            "count": len(bad),
            "checks": checks,
        }

    def policy_explain(self, env: Envelope, code: str) -> dict[str, Any]:
        _ = env
        return self.hub.explain(code)

    def policy_simulate(self, env: Envelope, body: dict[str, Any]) -> dict[str, Any]:
        profile = str(body.get("profile") or "scene")
        operation = str(body.get("operation") or "")
        sim = Envelope(
            tenant_id=env.tenant_id,
            actor_id=env.actor_id,
            profile=profile,
            track=env.track,
            correlation_id=env.correlation_id,
            idempotency_key=env.idempotency_key,
        )
        try:
            self.hub.chain.run_cs(
                sim,
                operation,
                dict(body.get("payload") or {}),
                execute_fn=lambda _op, _scoped: {"dry_run": True},
            )
            return {"allowed": True, "code": None, "profile": profile, "operation": operation}
        except HubError as exc:
            return {
                "allowed": False,
                "code": exc.code,
                "profile": profile,
                "operation": operation,
                "detail": exc.detail,
            }

    def protocol_registry(self, env: Envelope) -> dict[str, Any]:
        _ = env
        return load_registry()

    def protocol_contracts(self, env: Envelope) -> dict[str, Any]:
        _ = env
        modules = load_registry().get("modules") or []
        return {
            "contracts": [
                {
                    "id": m.get("id"),
                    "protocol_id": m.get("protocol_id"),
                    "port": m.get("port"),
                    "hub_methods": m.get("hub_methods"),
                }
                for m in modules
            ]
        }

    def graph_get(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        gid = payload.get("graph_id")
        if gid:
            graph = self.hub.graphs.get(str(gid))
            if graph is None or graph.get("tenant_id") != env.tenant_id:
                raise HubError("TENANT_MISMATCH")
            return graph
        return self._graph_for_tenant(env.tenant_id)

    def graph_validate(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        graph = self.graph_get(env, body)
        bad_nodes = []
        for node in graph.get("nodes") or []:
            miss = node_incomplete(node)
            if miss:
                bad_nodes.append({"node_id": node.get("node_id"), "missing": miss})
        if bad_nodes:
            return {"ok": False, "code": "WM_INCOMPLETE", "nodes": bad_nodes}
        return {"ok": True, "graph_id": graph.get("graph_id")}

    def graph_publish(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        val = self.graph_validate(env, body)
        if not val.get("ok"):
            raise HubError("INVARIANT_FAILED", "graph incomplete")
        graph = self.graph_get(env, body)
        return self._put_pending(
            env,
            kind="graph.publish",
            summary=f"publish {graph.get('graph_id')}",
            payload={"graph_id": graph.get("graph_id")},
        )

    def _put_pending(
        self,
        env: Envelope,
        *,
        kind: str,
        summary: str = "",
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        key = (env.idempotency_key or "").strip()
        if key and key in self._idem:
            return dict(self._idem[key])
        self._seq += 1
        cid = f"cs-ops-{self._seq:04d}"
        rec = {
            "changeset_id": cid,
            "status": "pending",
            "auto_apply": False,
            "kind": kind,
            "summary": summary,
            "payload": payload or {},
            "tenant_id": env.tenant_id,
            "actor_id": env.actor_id,
        }
        self._cs[cid] = rec
        if key:
            self._idem[key] = rec
        return dict(rec)

    def changeset_list(self, env: Envelope) -> dict[str, Any]:
        self._ensure_tenant(env)
        items = [dict(v) for v in self._cs.values() if v.get("tenant_id") == env.tenant_id]
        for item in items:
            if item.get("status") == "draft":
                item["status"] = "pending"
        return {"items": items}

    def changeset_submit(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return self._put_pending(
            env,
            kind=str(payload.get("kind") or "manual"),
            summary=str(payload.get("summary") or ""),
            payload=payload,
        )

    def changeset_decide(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        cid = str(payload.get("changeset_id") or "")
        rec = self._cs.get(cid)
        if rec is None or rec.get("status") != "pending":
            raise HubError("INVARIANT_FAILED", "not pending")
        if rec.get("tenant_id") != env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        approved = bool(payload.get("approved"))
        rec["status"] = "applied" if approved else "rejected"
        rec["auto_apply"] = False
        if approved and rec.get("kind") == "connector.rotate":
            pl = rec.get("payload") or {}
            cid = str(pl.get("connector_id") or "")
            ref = str(pl.get("secret_ref") or "")
            if cid and ref.startswith("vault://"):
                live = getattr(self, "_connector_live", None)
                if live is None:
                    self.connector_list(env)
                    live = self._connector_live
                row = live.get(cid) or {"id": cid, "status": "connected"}
                row = dict(row)
                row["secret_ref"] = ref
                live[cid] = row
        return dict(rec)

    def registry_list(self, env: Envelope) -> dict[str, Any]:
        _ = env
        return {"operations": sorted(self.hub.registry._ops.keys())}

    def registry_patch(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._put_pending(
            env,
            kind="registry.patch",
            summary="registry patch",
            payload=body or {},
        )

    def mcp_preview(self, env: Envelope, profile: str) -> dict[str, Any]:
        _ = env
        names = self.hub.registry.list_for_profile(profile or "scene")
        return {"tools": [{"name": n} for n in names]}

    def skill_list(self, env: Envelope) -> dict[str, Any]:
        _ = env
        return {"skills": [{**dict(s), "executable": False} for s in CATALOG]}

    def connector_list(self, env: Envelope) -> dict[str, Any]:
        _ = env
        live = getattr(self, "_connector_live", None)
        if live is None:
            self._connector_live = {
                "connector.crm.sandbox": {
                    "id": "connector.crm.sandbox",
                    "status": "connected",
                    "secret_ref": "vault://crm/sandbox",
                }
            }
            live = self._connector_live
        return {"connectors": [dict(v) for v in live.values()]}

    def connector_rotate(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        cid = str(payload.get("connector_id") or payload.get("connector") or "connector.crm.sandbox")
        # candidate only — live list unchanged until changeset decide (not auto)
        secret_ref = f"vault://{cid.split('.')[-1] if '.' in cid else cid}/rotated"
        pending = self._put_pending(
            env,
            kind="connector.rotate",
            summary=f"rotate {cid}",
            payload={"connector_id": cid, "secret_ref": secret_ref},
        )
        out = dict(pending)
        out["secret_ref"] = secret_ref
        out["connector_id"] = cid
        return out

    def iam_bindings(self, env: Envelope) -> dict[str, Any]:
        self._ensure_tenant(env)
        if self.hub.iam is None:
            return {"bindings": []}
        out = []
        for (actor_id, tenant_id), position_id in self.hub.iam._bindings.items():
            if tenant_id != env.tenant_id:
                continue
            out.append(
                {
                    "actor_id": actor_id,
                    "tenant_id": tenant_id,
                    "position_id": position_id,
                }
            )
        return {"bindings": out}

    def law_diff(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = env
        payload = body or {}
        current = dict(VISIT_SLA)
        candidate = dict(VISIT_SLA)
        candidate["source"] = "pending"
        return {
            "pack_id": payload.get("pack_id"),
            "current": current,
            "candidate": candidate,
        }

    def wm_get(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = env
        payload = body or {}
        return self.hub.wm.get(
            str(payload.get("world_model_id") or ""),
            str(payload.get("lifetime") or "draft"),
        )

    def audit_search(self, env: Envelope, q: str = "") -> dict[str, Any]:
        self._ensure_tenant(env)
        rows = [r for r in self.hub.audit if r.get("tenant_id") == env.tenant_id]
        if q:
            rows = [r for r in rows if q in json.dumps(r, ensure_ascii=False)]
        return {"records": rows}

    def audit_export(self, env: Envelope, q: str = "") -> dict[str, Any]:
        result = self.audit_search(env, q)
        self.hub.audit.append(
            {
                "operation": "hub.ops.audit.export",
                "tenant_id": env.tenant_id,
                "actor_id": env.actor_id,
                "q": q,
            }
        )
        return result

    def caliber_status(self, env: Envelope) -> dict[str, Any]:
        _ = env
        keys = ["kpi-visit-dwell", "kpi-spend"]
        cube = getattr(self.hub, "cube", None)
        items: list[dict[str, Any]] = []
        if cube is not None:
            osi = getattr(cube, "_osi", {}) or {}
            if osi:
                keys = sorted(osi.keys())
            for key in keys:
                row = cube.query(key)
                items.append(
                    {
                        "key": key,
                        "stale": bool(row.get("stale")),
                        "caliber_id": row.get("caliber_id"),
                        "as_of": row.get("as_of"),
                        "value": row.get("value"),
                        "status": "stale" if row.get("stale") else "fresh",
                    }
                )
        else:
            items = [
                {
                    "key": "kpi-visit-dwell",
                    "stale": False,
                    "caliber_id": "now - stage_entered_at",
                    "as_of": "",
                    "value": 28,
                    "status": "fresh",
                }
            ]
        return {"items": items}

    def kg_ingest_status(self, env: Envelope) -> dict[str, Any]:
        _ = env
        return {
            "lag_minutes": 12,
            "status": "ok",
            "last_episode": "ep-visit-20260715",
            "failures": [],
        }

    def kg_search(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = env
        payload = body or {}
        kg = getattr(self.hub, "kg", None)
        if kg is None:
            return {"hits": []}
        hits = kg.search(
            object_ref=payload.get("object_ref"),
            query=str(payload.get("q") or payload.get("query") or ""),
        )
        return {"hits": hits}

    def runtime_task(self, env: Envelope, q: str = "") -> dict[str, Any]:
        _ = env
        loop = getattr(self.hub, "outer_loop", None)
        runs = getattr(loop, "runs", {}) if loop is not None else {}
        tasks = []
        for run in runs.values():
            row = {
                "task_id": run.get("task_id"),
                "status": run.get("status"),
            }
            if q and q not in json.dumps(row, ensure_ascii=False):
                continue
            tasks.append(row)
        return {"tasks": tasks}

    def runtime_retry(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = env
        payload = body or {}
        task_id = str(payload.get("task_id") or "")
        loop = getattr(self.hub, "outer_loop", None)
        runs = getattr(loop, "runs", {}) if loop is not None else {}
        target = None
        for run in runs.values():
            if run.get("task_id") == task_id:
                target = run
                break
        if target is None:
            raise HubError("TASK_NOT_ISSUED", task_id)
        wid = str(target.get("workflow_id") or "")
        run = loop.signal(wid, "approved", payload)
        return {"task_id": task_id, "status": run.get("status")}

    def artifact_list(self, env: Envelope) -> dict[str, Any]:
        _ = env
        art = getattr(self.hub, "artifact", None)
        items: list[dict[str, Any]] = []
        if art is not None and getattr(art, "_items", None):
            for rec in art._items.values():
                items.append(
                    {
                        "id": rec.get("artifact_id"),
                        "kind": rec.get("kind"),
                        "pack_state": bool(art.usable_as_pack_state(rec.get("artifact_id") or "")),
                    }
                )
        if not items:
            items = [{"id": "art-demo", "kind": "report", "pack_state": False}]
        return {"items": items}

    def model_route(self, env: Envelope) -> dict[str, Any]:
        _ = env
        return {
            "routes": [
                {"id": "route-default", "provider": "fixture", "rpm": 60},
            ]
        }

    def memory_receipt(self, env: Envelope, q: str = "") -> dict[str, Any]:
        _ = env
        rows = list(self._receipts)
        if q:
            rows = [r for r in rows if q in json.dumps(r, ensure_ascii=False)]
        return {"receipts": rows}

    def memory_forget(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        actor_id = str(payload.get("actor_id") or env.actor_id)
        memory_id = str(payload.get("memory_id") or "")
        mem = getattr(self.hub, "memory", None)
        if mem is None:
            raise HubError("OPERATION_NOT_FOUND", "memory")
        out = mem.forget(actor_id, memory_id)
        receipt = {
            "receipt_id": out.get("receipt_id"),
            "actor_id": actor_id,
            "memory_id": memory_id,
            "forgotten": bool(out.get("forgotten")),
            "tenant_id": env.tenant_id,
            "ts": utc_now(),
        }
        self._receipts.append(receipt)
        self.hub.audit.append(
            {
                "operation": "hub.ops.memory.forget",
                "tenant_id": env.tenant_id,
                "actor_id": env.actor_id,
                "receipt_id": receipt["receipt_id"],
            }
        )
        return receipt

    def automation_jobs(self, env: Envelope) -> dict[str, Any]:
        _ = env
        if self._jobs is None:
            self._jobs = [
                {
                    "id": "wm_drift_scan",
                    "name": "经营模型漂移扫描",
                    "schedule": "daily",
                    "findings": [
                        {"id": "f-wm-1", "label": "节点五维缺反馈维", "severity": "medium"},
                    ],
                },
                {
                    "id": "dual_track_scan",
                    "name": "双轨升级巡检",
                    "schedule": "hourly",
                    "findings": [
                        {"id": "f-dt-1", "label": "selfpaw 写经营未带证据", "severity": "high"},
                    ],
                },
            ]
        return {"jobs": list(self._jobs)}

    def automation_run(self, env: Envelope, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        job_id = str(payload.get("job_id") or "")
        jobs = self.automation_jobs(env)["jobs"]
        job = next((j for j in jobs if j["id"] == job_id), None)
        if job is None:
            raise HubError("OPERATION_NOT_FOUND", job_id or "job")
        job["last_run"] = utc_now()
        return self._put_pending(
            env,
            kind=f"automation.{job_id}",
            summary=f"作业建议 · {job.get('name')}",
            payload={"job_id": job_id, "findings": job.get("findings") or []},
        )

    def wm_list(self, env: Envelope) -> dict[str, Any]:
        _ = env
        wm = getattr(self.hub, "wm", None)
        items: list[dict[str, Any]] = []
        docs = getattr(wm, "_docs", {}) if wm is not None else {}
        for (wid, lifetime, version), body in docs.items():
            items.append(
                {
                    "world_model_id": wid,
                    "lifetime": lifetime,
                    "version": version,
                    "keys": sorted(body.keys()) if isinstance(body, dict) else [],
                }
            )
        if not items:
            items = [
                {"world_model_id": "wm-fixture", "lifetime": "draft", "version": 0, "keys": []},
            ]
        return {"items": items}
