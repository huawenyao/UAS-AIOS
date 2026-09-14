"""WorkStudio 入口：复用 hub-api 路由，补齐 T1 §11。"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request

from capability_hub.facade import CapabilityHub
from capability_hub.ops_service import OpsService
from uas_hub.errors import Envelope, HubError
from uas_hub.http_app import create_app as create_core_app


def _envelope(request: Request, hub: CapabilityHub, profile: str) -> Envelope:
    tenant = request.headers.get("x-tenant-id") or ""
    actor = request.headers.get("x-actor-id") or "anonymous"
    track = request.headers.get("x-track") or "pipaw"
    env = Envelope(
        tenant_id=tenant,
        actor_id=actor,
        profile=profile,
        track=track,
        correlation_id=request.headers.get("x-correlation-id") or "corr-http",
        idempotency_key=request.headers.get("idempotency-key") or "",
        thread_id=request.headers.get("x-thread-id"),
        position_id=None,
    )
    if env.thread_id:
        hub.core.bind_thread(env.thread_id, env.profile)
    return env


_OPS_ROLES = {"admin", "operator", "sre", "frontline"}
_OPS_WRITES = (
    "/hub/v1/ops/graph/publish",
    "/hub/v1/ops/registry/patch",
    "/hub/v1/ops/changeset/submit",
    "/hub/v1/ops/changeset/decide",
    "/hub/v1/ops/connector/rotate",
)


def ops_envelope(request: Request, hub: CapabilityHub) -> Envelope:
    tenant = request.headers.get("x-tenant-id") or ""
    if not tenant:
        raise HubError("TENANT_MISMATCH")
    role = (request.headers.get("x-ops-role") or "").strip().lower()
    if role not in _OPS_ROLES:
        raise HubError("GATE_BLOCKED", "X-Ops-Role required")
    if role == "frontline":
        raise HubError("SCOPE_DENIED", "一线账号看不到 /console")
    env = Envelope(
        tenant_id=tenant,
        actor_id=request.headers.get("x-actor-id") or "anonymous",
        profile="builder",
        track=request.headers.get("x-track") or "pipaw",
        correlation_id=request.headers.get("x-correlation-id") or "corr-ops",
        idempotency_key=request.headers.get("idempotency-key") or "",
        thread_id=None,
        position_id=None,
    )
    path = request.url.path
    if env.track == "selfpaw" and path in _OPS_WRITES:
        raise HubError("TRACK_ESCALATION_REQUIRED")
    _ = hub
    return env


def create_app(hub: CapabilityHub | None = None) -> FastAPI:
    ch = hub or CapabilityHub.from_repo()
    ops = OpsService(ch.core)
    app = create_core_app(ch.core)
    app.state.ch = ch
    app.state.ops = ops

    @app.get("/hub/v1/ops/profile/matrix")
    def profile_matrix(request: Request) -> dict[str, Any]:
        ops_envelope(request, ch)
        return ch.matrix()

    @app.get("/hub/v1/ops/tenant/get")
    def ops_tenant_get(request: Request) -> dict[str, Any]:
        return ops.tenant_get(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/health/summary")
    def ops_health(request: Request) -> dict[str, Any]:
        return ops.health_summary(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/schema/drift")
    def ops_drift(request: Request) -> dict[str, Any]:
        return ops.schema_drift(ops_envelope(request, ch))

    @app.post("/hub/v1/ops/policy/explain")
    def ops_policy_explain(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ops.policy_explain(ops_envelope(request, ch), str(payload.get("code") or ""))

    @app.post("/hub/v1/ops/policy/simulate")
    def ops_policy_simulate(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.policy_simulate(ops_envelope(request, ch), body or {})

    @app.get("/hub/v1/ops/protocol/registry")
    def ops_protocol_registry(request: Request) -> dict[str, Any]:
        return ops.protocol_registry(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/protocol/contracts")
    def ops_protocol_contracts(request: Request) -> dict[str, Any]:
        return ops.protocol_contracts(ops_envelope(request, ch))

    @app.post("/hub/v1/ops/graph/get")
    def ops_graph_get(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.graph_get(ops_envelope(request, ch), body or {})

    @app.post("/hub/v1/ops/graph/validate")
    def ops_graph_validate(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.graph_validate(ops_envelope(request, ch), body or {})

    @app.post("/hub/v1/ops/graph/publish")
    def ops_graph_publish(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.graph_publish(ops_envelope(request, ch), body or {})

    @app.get("/hub/v1/ops/changeset/list")
    def ops_changeset_list(request: Request) -> dict[str, Any]:
        return ops.changeset_list(ops_envelope(request, ch))

    @app.post("/hub/v1/ops/changeset/submit")
    def ops_changeset_submit(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.changeset_submit(ops_envelope(request, ch), body or {})

    @app.post("/hub/v1/ops/changeset/decide")
    def ops_changeset_decide(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.changeset_decide(ops_envelope(request, ch), body or {})

    @app.get("/hub/v1/ops/registry/list")
    def ops_registry_list(request: Request) -> dict[str, Any]:
        return ops.registry_list(ops_envelope(request, ch))

    @app.post("/hub/v1/ops/registry/patch")
    def ops_registry_patch(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.registry_patch(ops_envelope(request, ch), body or {})

    @app.get("/hub/v1/ops/mcp/preview")
    def ops_mcp_preview(request: Request, profile: str = "scene") -> dict[str, Any]:
        return ops.mcp_preview(ops_envelope(request, ch), profile)

    @app.get("/hub/v1/ops/skill/list")
    def ops_skill_list(request: Request) -> dict[str, Any]:
        return ops.skill_list(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/connector/list")
    def ops_connector_list(request: Request) -> dict[str, Any]:
        return ops.connector_list(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/iam/bindings")
    def ops_iam_bindings(request: Request) -> dict[str, Any]:
        return ops.iam_bindings(ops_envelope(request, ch))

    @app.post("/hub/v1/ops/law/diff")
    def ops_law_diff(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.law_diff(ops_envelope(request, ch), body or {})

    @app.post("/hub/v1/ops/wm/get")
    def ops_wm_get(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.wm_get(ops_envelope(request, ch), body or {})

    @app.get("/hub/v1/ops/audit/search")
    def ops_audit_search(request: Request, q: str = "") -> dict[str, Any]:
        return ops.audit_search(ops_envelope(request, ch), q)

    @app.get("/hub/v1/ops/audit/export")
    def ops_audit_export(request: Request, q: str = "") -> dict[str, Any]:
        return ops.audit_export(ops_envelope(request, ch), q)

    @app.get("/hub/v1/ops/artifact/list")
    def ops_artifact_list(request: Request) -> dict[str, Any]:
        return ops.artifact_list(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/caliber/status")
    def ops_caliber_status(request: Request) -> dict[str, Any]:
        return ops.caliber_status(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/kg/ingest_status")
    def ops_kg_ingest_status(request: Request) -> dict[str, Any]:
        return ops.kg_ingest_status(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/memory/receipt")
    def ops_memory_receipt(request: Request, q: str = "") -> dict[str, Any]:
        return ops.memory_receipt(ops_envelope(request, ch), q)

    @app.post("/hub/v1/ops/memory/forget")
    def ops_memory_forget(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.memory_forget(ops_envelope(request, ch), body or {})

    @app.get("/hub/v1/ops/automation/jobs")
    def ops_automation_jobs(request: Request) -> dict[str, Any]:
        return ops.automation_jobs(ops_envelope(request, ch))

    @app.post("/hub/v1/ops/automation/run")
    def ops_automation_run(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.automation_run(ops_envelope(request, ch), body or {})

    @app.get("/hub/v1/ops/wm/list")
    def ops_wm_list(request: Request) -> dict[str, Any]:
        return ops.wm_list(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/runtime/task")
    def ops_runtime_task(request: Request, q: str = "") -> dict[str, Any]:
        return ops.runtime_task(ops_envelope(request, ch), q)

    @app.get("/hub/v1/ops/model/route")
    def ops_model_route(request: Request) -> dict[str, Any]:
        return ops.model_route(ops_envelope(request, ch))

    @app.post("/hub/v1/ops/connector/rotate")
    def ops_connector_rotate(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.connector_rotate(ops_envelope(request, ch), body or {})

    @app.post("/hub/v1/ops/kg/search")
    def ops_kg_search(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.kg_search(ops_envelope(request, ch), body or {})

    @app.post("/hub/v1/ops/runtime/retry")
    def ops_runtime_retry(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ops.runtime_retry(ops_envelope(request, ch), body or {})

    @app.get("/hub/v1/scene/pack/list")
    def pack_list(request: Request) -> dict[str, Any]:
        return ch.pack_list(_envelope(request, ch, "scene"))

    @app.get("/hub/v1/scene/insight/list")
    def insight_list(request: Request) -> dict[str, Any]:
        return ch.insight_list(_envelope(request, ch, "scene"))

    @app.post("/hub/v1/scene/task/return")
    def task_return(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ch.task_return(_envelope(request, ch, "scene"), body or {})

    @app.post("/hub/v1/theme/create")
    def theme_create(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ch.theme_create(_envelope(request, ch, "explore"), body or {})

    @app.post("/hub/v1/theme/update")
    def theme_update(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ch.theme_update(_envelope(request, ch, "explore"), str(payload.get("theme_id") or ""), payload)

    @app.post("/hub/v1/theme/get")
    def theme_get(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ch.theme_get(_envelope(request, ch, "explore"), str(payload.get("theme_id") or ""))

    @app.post("/hub/v1/theme/promote")
    def theme_promote(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ch.theme_promote(_envelope(request, ch, "explore"), str(payload.get("theme_id") or ""))

    def _app_step(name: str):
        def handler(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
            env = _envelope(request, ch, "builder")
            payload = body or {}
            fn = getattr(ch, f"app_{name}")
            if name == "normalize":
                return fn(env, payload)
            if name == "validate":
                return fn(env, str(payload.get("app_id") or ""), bool(payload.get("pass_invariants", True)))
            if name == "release":
                return fn(env, str(payload.get("app_id") or ""))
            return fn(env, str(payload.get("app_id") or ""))

        handler.__name__ = f"app_{name}"
        return handler

    for step in ("normalize", "analyze_wm", "select_template", "design", "generate", "validate", "release"):
        app.post(f"/hub/v1/app/{step}")(_app_step(step))

    @app.post("/hub/v1/instance/deploy")
    def instance_deploy(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ch.instance_deploy(_envelope(request, ch, "runtime"), body or {})

    @app.get("/hub/v1/instance/{instance_id}/artifacts")
    def instance_artifacts(instance_id: str, request: Request) -> dict[str, Any]:
        return ch.instance_list_artifacts(_envelope(request, ch, "runtime"), instance_id)

    @app.post("/hub/v1/instance/escalate")
    def instance_escalate(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ch.instance_escalate(_envelope(request, ch, "runtime"), body or {})

    @app.post("/hub/v1/skill/discover")
    def skill_discover(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = body
        return ch.skill_discover(_envelope(request, ch, "explore"))

    @app.post("/hub/v1/skill/preview")
    def skill_preview(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ch.skill_preview(_envelope(request, ch, "explore"), str(payload.get("skill_id") or ""))

    @app.post("/hub/v1/skill/cite")
    def skill_cite(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ch.skill_cite(
            _envelope(request, ch, "explore"),
            str(payload.get("skill_id") or ""),
            payload.get("theme_id"),
        )

    @app.post("/hub/v1/skill/install")
    def skill_install(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ch.skill_install(_envelope(request, ch, "builder"), str(payload.get("skill_id") or ""))

    @app.post("/hub/v1/skill/enable")
    def skill_enable(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ch.skill_enable(_envelope(request, ch, "runtime"), str(payload.get("skill_id") or ""))

    @app.post("/hub/v1/skill/execute")
    def skill_execute(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        env = _envelope(request, ch, "explore")
        try:
            return ch.skill_execute(env, str(payload.get("skill_id") or ""))
        except HubError:
            raise

    @app.post("/hub/v1/wm/get")
    def wm_get(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        return ch.wm_get(
            _envelope(request, ch, "explore"),
            str(payload.get("world_model_id") or ""),
            str(payload.get("lifetime") or "draft"),
            payload.get("version"),
        )

    @app.post("/hub/v1/wm/patch")
    def wm_patch(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        lifetime = str(payload.get("lifetime") or "draft")
        profile = "builder" if lifetime == "compiled" else "explore"
        return ch.wm_patch(
            _envelope(request, ch, profile),
            str(payload.get("world_model_id") or ""),
            lifetime,
            payload.get("body") or {},
        )

    @app.get("/hub/v1/audit/query")
    def audit_query(request: Request, q: str = "") -> dict[str, Any]:
        return ch.audit_query(_envelope(request, ch, "builder"), q)

    @app.post("/hub/v1/thread/start")
    def thread_start(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = body or {}
        profile = str(payload.get("profile") or request.headers.get("x-profile") or "explore")
        return ch.thread_start(_envelope(request, ch, profile), payload)

    @app.post("/hub/v1/iam/permission_changeset")
    def permission_changeset(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ch.permission_changeset(_envelope(request, ch, "builder"), body or {})

    @app.post("/hub/v1/iam/bindings")
    def iam_bindings(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return ch.iam_bind(_envelope(request, ch, "builder"), body or {})

    return app


app = create_app()
