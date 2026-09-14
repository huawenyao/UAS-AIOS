from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from uas_hub.compose import try_attach_fixtures
from uas_hub.errors import ERROR_HTTP, EXPLAIN, Envelope, HubError
from uas_hub.graph_store import GraphStore
from uas_hub.insight_task import InsightTaskService
from uas_hub.policy import PolicyChain
from uas_hub.registry import Registry
from uas_hub.outer_loop import InMemoryOuterLoop, OuterLoopPort
from uas_hub.wm_store import WmStore

REPO = Path(__file__).resolve().parents[3]


class Hub:
    def __init__(
        self,
        registry: Registry,
        graphs: GraphStore,
        insights: InsightTaskService | None = None,
        wm: WmStore | None = None,
        outer_loop: OuterLoopPort | None = None,
    ) -> None:
        self.registry = registry
        self.graphs = graphs
        self.chain = PolicyChain(registry)
        self.insights = insights or InsightTaskService()
        self.wm = wm or WmStore()
        self.outer_loop = outer_loop or InMemoryOuterLoop()
        self.outer_loop.bind_hub(self)
        self.threads: dict[str, str] = {}
        self.audit: list[dict[str, Any]] = []
        self.cube = None
        self.kg = None
        self.memory = None
        self.inner_loop = None
        self.broker = None
        self.mcp = None
        self.skill = None
        self.law = None
        self.evolution = None
        self.artifact = None
        self.connector = None
        self.iam = None
        self.review = None

    @classmethod
    def from_repo(cls, root: Path | None = None) -> "Hub":
        root = root or REPO
        registry = Registry.from_file(root / "configs" / "capability_registry.json")
        sample = json.loads((root / "configs" / "accountability_graph.sample.json").read_text(encoding="utf-8"))
        hub = cls(registry, GraphStore([sample]))
        return try_attach_fixtures(hub)

    def bind_thread(self, thread_id: str, profile: str) -> None:
        existing = self.threads.get(thread_id)
        if existing and existing != profile:
            raise HubError("THREAD_PROFILE_IMMUTABLE")
        self.threads[thread_id] = profile

    def explain(self, code: str) -> dict[str, Any]:
        exp = EXPLAIN.get(code)
        if not exp:
            raise HubError("OPERATION_NOT_FOUND", code)
        return {"code": code, "http": ERROR_HTTP.get(code, 400), **exp}

    def pack_open(self, env: Envelope, position_id: str, cube_ok: bool = True) -> dict[str, Any]:
        env.profile = "scene"
        if not env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        if not position_id:
            raise HubError("SCOPE_DENIED")
        env.position_id = position_id
        pack = self.graphs.pack_open(env.tenant_id, position_id, cube_ok=cube_ok)
        if self.iam is not None:
            bound = self.iam.position_of(env.actor_id, env.tenant_id)
            if not bound or bound != position_id:
                raise HubError("SCOPE_DENIED", "no position")
        if self.cube:
            for node in pack["nodes"]:
                kpi = dict(node.get("kpi") or {})
                kpi_id = kpi.get("kpi_id")
                if not kpi_id:
                    continue
                result = self.cube.query(str(kpi_id), available=cube_ok)
                kpi["is"] = result.get("value", kpi.get("is"))
                kpi["stale"] = bool(result.get("stale", not cube_ok))
                if result.get("caliber_id"):
                    kpi["caliber_id"] = result["caliber_id"]
                if result.get("as_of"):
                    kpi["as_of"] = result["as_of"]
                node["kpi"] = kpi
        return pack

    def list_tools(self, env: Envelope) -> list[str]:
        return self.registry.list_for_profile(env.profile)

    def invoke_cs(self, env: Envelope, operation: str, payload: dict[str, Any] | None = None, claimed_profile: str | None = None) -> dict[str, Any]:
        # 客户端伪造的 profile 作废
        _ = claimed_profile
        if env.track == "pipaw" and operation.startswith("hub.memory"):
            raise HubError("MEMORY_TRACK_FORBIDDEN")

        def execute(op, scoped):
            self.audit.append(
                {
                    "operation": operation,
                    "tenant_id": env.tenant_id,
                    "profile": env.profile,
                    "track": env.track,
                    "correlation_id": env.correlation_id,
                }
            )
            clean = {k: v for k, v in scoped.items() if not k.startswith("_")}
            if op.get("side_effects") and self.connector is not None:
                key = env.idempotency_key or f"{env.correlation_id}:{operation}:{clean.get('customer_id', '')}"
                result = self.connector.invoke(
                    operation,
                    clean,
                    {"tenant_id": env.tenant_id},
                    key,
                )
                if self.cube is not None and hasattr(self.cube, "note_runtime_write"):
                    self.cube.note_runtime_write()
                return {
                    "ok": True,
                    "operation": operation,
                    "echo": clean,
                    "result_code": result.get("result_code"),
                }
            if operation == "cs.metric.query" and self.cube is not None:
                queried = self.cube.query(str(clean.get("kpi_id") or ""), available=True)
                return {
                    "ok": True,
                    "operation": operation,
                    "echo": clean,
                    "value": queried.get("value"),
                    "stale": queried.get("stale"),
                    "caliber_id": queried.get("caliber_id"),
                }
            return {"ok": True, "operation": operation, "echo": clean}

        return self.chain.run_cs(env, operation, payload or {}, execute)

    def insight_drill(self, env: Envelope, source_node_id: str, evidence_refs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        node = self.graphs.node(env.tenant_id, source_node_id)
        refs = evidence_refs
        if refs is None:
            refs = []
            if self.kg is not None:
                for obj in node.get("object_refs") or []:
                    for ep in self.kg.search(object_ref=str(obj)):
                        eid = ep.get("id")
                        if eid:
                            refs.append({"kind": "kg", "id": eid})
            if self.inner_loop is not None:
                allow = ["hub.kg.search", "hub.metric.query", "cs.visit.list"]
                thread_id = self.inner_loop.start_thread("explore", allow, env.track)
                self.inner_loop.turn(
                    thread_id,
                    {"tool_calls": [{"name": "hub.kg.search", "arguments": {"query": source_node_id}}]},
                )
        return self.insights.drill(env.tenant_id, source_node_id, node, refs)

    def task_issue(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        source = payload.get("source_node_id")
        if not source:
            raise HubError("TASK_SOURCE_REQUIRED")
        node = self.graphs.node(env.tenant_id, source)
        return self.insights.issue(env.tenant_id, payload, node)

    def memory_self(self, env: Envelope, action: str, text: str = "", memory_id: str = "", query: str = "") -> dict[str, Any]:
        if env.track != "selfpaw":
            raise HubError("MEMORY_TRACK_FORBIDDEN")
        if self.memory is None:
            return {"ok": True, "action": action}
        if action == "add":
            return self.memory.add(env.actor_id, text)
        if action == "search":
            return {"hits": self.memory.search(env.actor_id, query)}
        if action == "forget":
            return self.memory.forget(env.actor_id, memory_id)
        return {"ok": True, "action": action}

    def metric_query(self, env: Envelope, kpi_id: str, cube_ok: bool = True) -> dict[str, Any]:
        if self.cube is None:
            return self.invoke_cs(env, "cs.metric.query", {"kpi_id": kpi_id})
        return self.cube.query(kpi_id, available=cube_ok)

    def kg_search(self, env: Envelope, object_ref: str | None = None, query: str | None = None) -> dict[str, Any]:
        if self.kg is None:
            raise HubError("OPERATION_NOT_FOUND", "kg")
        return {"episodes": self.kg.search(object_ref=object_ref, query=query)}

    def kg_ingest(self, env: Envelope, episode: dict[str, Any]) -> dict[str, Any]:
        if env.profile == "scene":
            raise HubError("PROFILE_FORBIDS_SIDE_EFFECT")
        if self.kg is None:
            raise HubError("OPERATION_NOT_FOUND", "kg")
        return self.kg.ingest_episode(episode)

    def skill_transition(self, env: Envelope, skill_id: str, to_state: str) -> dict[str, Any]:
        if self.skill is None:
            raise HubError("OPERATION_NOT_FOUND", "skill")
        return self.skill.transition(skill_id, to_state, env.profile)

    def law_compile(self, env: Envelope, pack_id: str, changeset_approved: bool) -> dict[str, Any]:
        if self.law is None:
            raise HubError("OPERATION_NOT_FOUND", "law")
        return self.law.compile(pack_id, changeset_approved)

    def evolution_draft(self, env: Envelope, signal: dict[str, Any]) -> dict[str, Any]:
        if self.evolution is None:
            raise HubError("OPERATION_NOT_FOUND", "evolution")
        return self.evolution.draft(signal)

    def evolution_apply(self, env: Envelope, changeset_id: str, approved: bool) -> dict[str, Any]:
        if self.evolution is None:
            raise HubError("OPERATION_NOT_FOUND", "evolution")
        return self.evolution.apply(changeset_id, approved)

    def artifact_put(self, env: Envelope, kind: str, body: Any) -> dict[str, Any]:
        if self.artifact is None:
            raise HubError("OPERATION_NOT_FOUND", "artifact")
        return self.artifact.put(kind, body)

    def mcp_list(self, env: Envelope) -> dict[str, Any]:
        if self.mcp is None:
            return {"tools": [{"name": n, "description": "能力"} for n in self.list_tools(env)]}
        return {"tools": self.mcp.list_tools(env)}

    def mcp_call(self, env: Envelope, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        if self.mcp is None:
            return self.invoke_cs(env, name, arguments or {})
        return self.mcp.call_tool(env, name, arguments)

    def inner_turn(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        if self.inner_loop is None:
            raise HubError("OPERATION_NOT_FOUND", "inner_loop")
        allow = list(payload.get("tool_allowlist") or self.list_tools(env))
        thread_id = payload.get("thread_id") or self.inner_loop.start_thread(env.profile, allow, env.track)
        return self.inner_loop.turn(thread_id, payload)

    def broker_complete(self, env: Envelope, route_id: str, messages: list[dict[str, Any]]) -> dict[str, Any]:
        if self.broker is None:
            raise HubError("OPERATION_NOT_FOUND", "broker")
        return self.broker.complete(route_id, messages)

    def task_transfer(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        task_id = str(payload.get("task_id") or "")
        task = self.insights.tasks.get(task_id)
        if not task:
            raise HubError("TASK_NOT_ISSUED")
        if task.get("tenant_id") != env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        assignee = payload.get("assignee") or {}
        task["assignee"] = assignee
        self.audit.append(
            {
                "operation": "hub.task.transfer",
                "tenant_id": env.tenant_id,
                "task_id": task_id,
                "source_node_id": task.get("source_node_id"),
            }
        )
        return task

    def review_export(self, env: Envelope, query: str) -> dict[str, Any]:
        if self.review is None:
            return {"candidates": [], "write_path": False}
        result = self.review.export_candidates(query)
        result["write_path"] = False
        return result

    def invoke_connector(self, env: Envelope, operation: str, payload: dict[str, Any], idempotency_key: str = "") -> dict[str, Any]:
        if self.connector is None:
            return self.invoke_cs(env, operation, payload)
        return self.connector.invoke(operation, payload, {"tenant_id": env.tenant_id}, idempotency_key or env.idempotency_key)

    def wm_patch(self, env: Envelope, world_model_id: str, lifetime: str, body: dict[str, Any]) -> dict[str, Any]:
        return self.wm.patch(world_model_id, lifetime, env.profile, body)

    def exec_open(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        env.profile = "runtime"
        if not env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        task_id = str(payload.get("task_id") or "")
        task = self.insights.tasks.get(task_id)
        if not task or task.get("status") not in {"issued", "awaiting_approval", "opened"}:
            raise HubError("TASK_NOT_ISSUED")
        if task.get("tenant_id") != env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        self.insights.temporal_starts += 1
        run = self.outer_loop.start(
            {
                "tenant_id": env.tenant_id,
                "task_id": task_id,
                "source_node_id": task["source_node_id"],
                "track": task.get("track") or env.track,
                "cs_write": list(task.get("cs_write") or []),
            }
        )
        task["workflow_id"] = run["workflow_id"]
        task["status"] = run["status"]
        return {
            "task_id": task_id,
            "workflow_id": run["workflow_id"],
            "workflow_type": run.get("workflow_type") or "RuntimeCycleWorkflow",
            "status": run["status"],
        }

    def cycle_step(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        env.profile = "runtime"
        task_id = str(payload.get("task_id") or "")
        task = self.insights.tasks.get(task_id)
        if not task or not task.get("workflow_id"):
            raise HubError("TASK_NOT_ISSUED")
        run = self.outer_loop.signal(str(task["workflow_id"]), str(payload.get("signal") or ""), payload)
        task["status"] = run["status"]
        return {
            "task_id": task_id,
            "workflow_id": run["workflow_id"],
            "status": run["status"],
        }

    def exec_events(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "events": self.outer_loop.events_for_task(task_id)}

    def export_scene_fixture(self) -> dict[str, Any]:
        env = Envelope(
            tenant_id="t-hengchuan",
            actor_id="cowen.hua",
            profile="scene",
            track="pipaw",
            position_id="pos-cm",
        )
        pack = self.pack_open(env, "pos-cm")
        write_blocked = None
        try:
            self.invoke_cs(env, "cs.visit.schedule", {"customer_id": "UEC-10293", "when": "2026-08-25T10:00:00Z"})
        except HubError as exc:
            write_blocked = exc.as_body()
        insight = self.insight_drill(
            env,
            "an-stage-visit",
            evidence_refs=[{"kind": "kg", "id": "ep-visit-20260715"}],
        )
        task = self.task_issue(
            env,
            {
                "source_node_id": "an-stage-visit",
                "insight_id": insight["insight_id"],
                "cs_write": ["cs.visit.schedule"],
                "assignee": {"owner_id": "zhangsan", "position_id": "pos-bd"},
            },
        )
        return {
            "envelope": {
                "tenant_id": env.tenant_id,
                "actor_id": env.actor_id,
                "profile": "scene",
                "track": env.track,
                "position_id": env.position_id,
            },
            "pack": pack,
            "tools_scene": self.list_tools(env),
            "tools_runtime": self.list_tools(
                Envelope(
                    tenant_id=env.tenant_id,
                    actor_id=env.actor_id,
                    profile="runtime",
                    track=env.track,
                    position_id=env.position_id,
                )
            ),
            "write_blocked": write_blocked,
            "issued_task": task,
            "explain": dict(EXPLAIN),
        }
