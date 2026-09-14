"""FastAPI 壳：只暴露 /hub/v1，剖面由路径强制，包同一 Hub。"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from uas_hub.errors import Envelope, HubError
from uas_hub.hub import Hub


def create_app(hub: Hub | None = None) -> FastAPI:
    hub = hub or Hub.from_repo()
    app = FastAPI(title="UAS Capability Hub", version="0.1.0")
    app.state.hub = hub
    app.state.idempotency: dict[str, Any] = {}
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(HubError)
    async def _hub_error(_request: Request, exc: HubError) -> JSONResponse:
        return JSONResponse(status_code=exc.http, content=exc.as_body())

    def envelope(request: Request, profile: str) -> Envelope:
        tenant = request.headers.get("x-tenant-id") or ""
        actor = request.headers.get("x-actor-id") or "anonymous"
        track = request.headers.get("x-track") or "pipaw"
        thread = request.headers.get("x-thread-id")
        env = Envelope(
            tenant_id=tenant,
            actor_id=actor,
            profile=profile,
            track=track,
            correlation_id=request.headers.get("x-correlation-id") or "corr-http",
            idempotency_key=request.headers.get("idempotency-key") or "",
            thread_id=thread,
            position_id=None,
        )
        if thread:
            hub.bind_thread(thread, profile)
        return env

    @app.get("/health")
    def health() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/hub/v1/policy/explain")
    def explain(code: str) -> dict[str, Any]:
        return hub.explain(code)

    @app.get("/hub/v1/scene/tools")
    def scene_tools(request: Request) -> dict[str, Any]:
        env = envelope(request, "scene")
        return {"tools": hub.list_tools(env), "profile": "scene"}

    @app.post("/hub/v1/scene/pack/open")
    def pack_open(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "scene")
        payload = body or {}
        return hub.pack_open(env, str(payload.get("position_id") or ""))

    @app.post("/hub/v1/scene/insight/drill")
    def insight_drill(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "scene")
        payload = body or {}
        return hub.insight_drill(env, str(payload.get("source_node_id") or ""), payload.get("evidence_refs"))

    @app.post("/hub/v1/scene/task/issue")
    def task_issue(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "scene")
        key = env.idempotency_key
        if key and key in app.state.idempotency:
            return app.state.idempotency[key]
        result = hub.task_issue(env, body or {})
        if key:
            app.state.idempotency[key] = result
        return result

    @app.post("/hub/v1/scene/invoke_cs")
    def scene_invoke_cs(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "scene")
        payload = body or {}
        return hub.invoke_cs(
            env,
            str(payload.get("operation") or ""),
            payload.get("input") or {},
            claimed_profile=payload.get("profile"),
        )

    @app.post("/hub/v1/instance/invoke_cs")
    def runtime_invoke_cs(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "runtime")
        payload = body or {}
        return hub.invoke_cs(
            env,
            str(payload.get("operation") or ""),
            payload.get("input") or {},
            claimed_profile=payload.get("profile"),
        )

    @app.post("/hub/v1/exec/open")
    def exec_open(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "runtime")
        return hub.exec_open(env, body or {})

    @app.post("/hub/v1/instance/cycle_step")
    def cycle_step(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "runtime")
        return hub.cycle_step(env, body or {})

    @app.get("/hub/v1/exec/{task_id}/events")
    def exec_events(task_id: str) -> dict[str, Any]:
        return hub.exec_events(task_id)

    @app.post("/hub/v1/metric/query")
    def metric_query(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "scene")
        payload = body or {}
        return hub.metric_query(env, str(payload.get("kpi_id") or ""))

    @app.post("/hub/v1/kg/search")
    def kg_search(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "explore")
        payload = body or {}
        return hub.kg_search(env, payload.get("object_ref"), payload.get("query"))

    @app.post("/hub/v1/memory/self/{action}")
    def memory_self(action: str, request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "explore")
        payload = body or {}
        return hub.memory_self(
            env,
            action,
            text=str(payload.get("text") or ""),
            memory_id=str(payload.get("memory_id") or ""),
            query=str(payload.get("query") or ""),
        )

    @app.post("/hub/v1/skill/transition")
    def skill_transition(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, str((body or {}).get("profile") or "explore"))
        payload = body or {}
        env.profile = str(payload.get("profile") or env.profile)
        return hub.skill_transition(env, str(payload.get("skill_id") or ""), str(payload.get("to_state") or ""))

    @app.post("/hub/v1/task/transfer")
    def task_transfer(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "runtime")
        return hub.task_transfer(env, body or {})

    @app.post("/hub/v1/mcp/tools/list")
    def mcp_list(request: Request) -> dict[str, Any]:
        env = envelope(request, "scene")
        return hub.mcp_list(env)

    @app.post("/hub/v1/mcp/tools/call")
    def mcp_call(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "scene")
        payload = body or {}
        return hub.mcp_call(env, str(payload.get("name") or ""), payload.get("arguments") or {})

    @app.post("/hub/v1/law/compile")
    def law_compile(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = envelope(request, "builder")
        payload = body or {}
        return hub.law_compile(env, str(payload.get("pack_id") or ""), bool(payload.get("changeset_approved")))

    return app


app = create_app()
