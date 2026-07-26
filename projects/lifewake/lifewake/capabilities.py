"""能力契约层 — lw.* 注册表 + 通用调用/响应信封 + 幂等 + 审计。

规约来源：docs/lifewake/CAPABILITY_CONTRACTS.md
代理永不直接调用厂商 SDK，只走 lw.*。compose 类能力不可通知。
管线顺序不变量：compose → impact → timing → ritual。
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from dataclasses import dataclass, field
from typing import Any, Callable

from . import schemas

# 复用现有治理引擎（scripts/lifewake_policy.py）
_POLICY_PATH = __file__.replace(
    "lifewake/capabilities.py", "scripts/lifewake_policy.py"
).replace("lifewake\\capabilities.py", "scripts\\lifewake_policy.py")


def _load_policy() -> Any:
    spec = importlib.util.spec_from_file_location("lifewake_policy", _POLICY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load lifewake_policy from {_POLICY_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("lifewake_policy", module)
    spec.loader.exec_module(module)
    return module


_policy = _load_policy()


# === 通用调用/响应信封（规约 CAPABILITY_CONTRACTS.md） ===


@dataclass
class CapabilityCall:
    capability: str
    version: str = "1.0"
    tenant_id: str = "lifewake"
    trace_id: str = ""
    intent_ref: str = ""
    actor: dict[str, str] = field(default_factory=lambda: {"type": "person", "id": ""})
    on_behalf_of: str = ""
    idempotency_key: str = ""
    inputs: dict[str, Any] = field(default_factory=dict)
    policy: dict[str, Any] = field(
        default_factory=lambda: {
            "required_scopes": [],
            "max_risk_level": "G3",
            "purpose": "create_for_user",
        }
    )
    audit: dict[str, Any] = field(default_factory=lambda: {"audit_ref": ""})


@dataclass
class CapabilityResponse:
    status: str  # success | failed | needs_human_review
    result: dict[str, Any] = field(default_factory=dict)
    error: dict[str, Any] | None = None
    rollback: dict[str, Any] = field(
        default_factory=lambda: {"rollback_supported": False, "rollback_ref": ""}
    )
    capability: str = ""
    trace_id: str = ""

    def is_success(self) -> bool:
        return self.status == "success"


# === 幂等存储（进程内，按 idempotency_key 去重） ===


class IdempotencyStore:
    def __init__(self) -> None:
        self._cache: dict[str, CapabilityResponse] = {}

    def get(self, key: str) -> CapabilityResponse | None:
        return self._cache.get(key)

    def put(self, key: str, response: CapabilityResponse) -> None:
        if key:
            self._cache[key] = response


_idempotency = IdempotencyStore()


def _stable_key(call: CapabilityCall) -> str:
    if call.idempotency_key:
        return call.idempotency_key
    raw = f"{call.capability}:{call.trace_id}:{sorted(call.inputs.items())}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


# === 能力注册表 ===


class CapabilityRegistry:
    """lw.* 能力注册表。每个能力是一个纯函数 (call) -> response。"""

    def __init__(self) -> None:
        self._handlers: dict[str, Callable[[CapabilityCall], CapabilityResponse]] = {}

    def register(
        self, name: str, handler: Callable[[CapabilityCall], CapabilityResponse]
    ) -> None:
        self._handlers[name] = handler

    def invoke(self, call: CapabilityCall) -> CapabilityResponse:
        handler = self._handlers.get(call.capability)
        if handler is None:
            return CapabilityResponse(
                status="failed",
                capability=call.capability,
                trace_id=call.trace_id,
                error={
                    "code": "FEATURE_RESERVED",
                    "message": f"{call.capability} not registered",
                    "retryable": False,
                },
            )
        # 幂等：同 key 直接返回缓存
        key = _stable_key(call)
        cached = _idempotency.get(key)
        if cached is not None:
            return cached
        resp = handler(call)
        resp.capability = call.capability
        resp.trace_id = call.trace_id
        _idempotency.put(key, resp)
        return resp

    def names(self) -> list[str]:
        return sorted(self._handlers)


# === 审计钩子（红线 16 净化） ===

_audit_sink: list[dict[str, Any]] = []


def append_audit(event: str, trace_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    record = {
        "audit_id": f"audit_{len(_audit_sink) + 1:06d}",
        "event": event,
        "trace_id": trace_id,
        "payload": payload,
    }
    schemas.validate_audit_event(record)
    _audit_sink.append(record)
    return record


def audit_log() -> list[dict[str, Any]]:
    return list(_audit_sink)


def reset_audit() -> None:
    _audit_sink.clear()


# === P0 能力实现（包装 lifewake_policy） ===


def _lw_consent_check(call: CapabilityCall) -> CapabilityResponse:
    consent = call.inputs.get("consent")
    required_scopes = call.policy.get("required_scopes") or _policy.required_scopes_for(
        call.inputs.get("intent_type", "surprise_delivery"),
        call.inputs.get("governance", {}),
    )
    ok, code, detail = _policy.check_consent(
        consent,
        required_scopes,
        purpose=call.policy.get("purpose"),
        subject_age=call.inputs.get("subject_age"),
    )
    append_audit(
        "consent.checked",
        call.trace_id,
        {"ok": ok, "code": code, "consent_id": detail.get("consent_id")},
    )
    if not ok:
        return CapabilityResponse(
            status="failed",
            error={
                "code": code or "CONSENT_REQUIRED",
                "message": str(detail),
                "retryable": False,
            },
            rollback={"rollback_supported": True, "rollback_ref": "no_data_read"},
        )
    return CapabilityResponse(
        status="success",
        result={
            "allowed": True,
            "consent_id": detail.get("consent_id"),
            "missing_scopes": [],
        },
    )


def _lw_consent_revoke(call: CapabilityCall) -> CapabilityResponse:
    consent_id = call.inputs.get("consent_id", "")
    append_audit("consent.revoked", call.trace_id, {"consent_id": consent_id})
    # 红线 3：撤回后非审计处理 = 0（由 orchestrator 在后续 invoke 时阻断）
    return CapabilityResponse(
        status="success",
        result={"status": "CONSENT_REVOKED", "consent_id": consent_id},
        rollback={"rollback_supported": True, "rollback_ref": f"revoke:{consent_id}"},
    )


def _lw_policy_check(call: CapabilityCall) -> CapabilityResponse:
    ok, code, detail = _policy.check_safety_signal(call.inputs.get("safety_signal"))
    append_audit("policy.checked", call.trace_id, {"ok": ok, "code": code})
    if not ok:
        return CapabilityResponse(
            status="needs_human_review",
            error={
                "code": code or "SAFETY_HUMAN_REVIEW",
                "message": str(detail),
                "retryable": False,
            },
        )
    return CapabilityResponse(status="success", result=detail)


def _lw_surprise_compose(call: CapabilityCall) -> CapabilityResponse:
    bundle = call.inputs.get("signal_bundle", {})
    if not bundle.get("ok"):
        return CapabilityResponse(
            status="failed",
            error={
                "code": bundle.get("error", "VALIDATION_ERROR"),
                "message": "signal bundle invalid",
                "retryable": False,
            },
        )
    artifact = _policy.compose_surprise(
        bundle,
        call.inputs.get("timing_window", "evening"),
        call.inputs.get("governance", {}),
        user_feedback=call.inputs.get("user_feedback"),
        curator_score=call.inputs.get("curator_score"),
    )
    if not artifact.get("ok"):
        return CapabilityResponse(
            status="failed",
            error={
                "code": artifact.get("error", "VALIDATION_ERROR"),
                "message": "compose failed",
                "retryable": False,
            },
        )
    # 红线 11：uniqueness_refs 必须非空
    if not artifact.get("uniqueness_refs"):
        return CapabilityResponse(
            status="failed",
            error={
                "code": "VALIDATION_ERROR",
                "message": "missing uniqueness_refs",
                "retryable": False,
            },
        )
    append_audit(
        "surprise.composed",
        call.trace_id,
        {"surprise_id": artifact.get("surprise_id"), "kind": artifact.get("kind")},
    )
    return CapabilityResponse(status="success", result=artifact)


def _lw_pulse_compose(call: CapabilityCall) -> CapabilityResponse:
    result = _policy.compose_pulse_solo(
        call.inputs.get("person_id", ""),
        call.inputs.get("style", "nature"),
        call.inputs.get("device_linked", False),
    )
    if not result.get("ok"):
        return CapabilityResponse(
            status="failed",
            error={
                "code": result.get("error", "DEVICE_NOT_LINKED"),
                "message": "device not linked",
                "retryable": True,
            },
        )
    append_audit(
        "pulse.composed",
        call.trace_id,
        {"session_id": result.get("session_id"), "mode": "solo"},
    )
    return CapabilityResponse(status="success", result=result)


def _lw_pulse_duet(call: CapabilityCall) -> CapabilityResponse:
    result = _policy.compose_pulse_duet(
        call.inputs.get("participants", []),
        call.inputs.get("style", "nature"),
        call.inputs.get("bond_participants", []),
        share_keepsake=call.inputs.get("share_keepsake", True),
    )
    if not result.get("ok"):
        return CapabilityResponse(
            status="failed",
            error={
                "code": result.get("error", "BOND_ASYMMETRIC"),
                "message": "duet bond asymmetric",
                "retryable": False,
            },
        )
    append_audit(
        "pulse.duet",
        call.trace_id,
        {"session_id": result.get("session_id"), "mode": "duet"},
    )
    return CapabilityResponse(status="success", result=result)


def _lw_timing_decide(call: CapabilityCall) -> CapabilityResponse:
    result = _policy.decide_timing(
        call.inputs.get("run_history"),
        delivery_count_today=call.inputs.get("delivery_count_today"),
    )
    append_audit(
        "timing.decided",
        call.trace_id,
        {"allowed": result.get("allowed"), "code": result.get("code")},
    )
    if not result.get("allowed"):
        # 红线 13：SLOW_INSPIRATION_DEFERRED 不通知（由 orchestrator 不触发通知）
        return CapabilityResponse(
            status="success",
            result={
                "decision": "SLOW_INSPIRATION_DEFERRED",
                "reason_codes": ["frequency_guardrail"],
                "reconsider_after": "next_day",
            },
        )
    return CapabilityResponse(
        status="success",
        result={"decision": "DELIVER_NOW", "reason_codes": [], "reconsider_after": ""},
    )


def _lw_impact_evaluate(call: CapabilityCall) -> CapabilityResponse:
    artifact = call.inputs.get("artifact", {})
    impact = _policy.assess_emotion_impact(
        artifact,
        user_feedback=call.inputs.get("user_feedback"),
        curator_score=call.inputs.get("curator_score"),
        threshold=call.inputs.get("threshold", 0.7),
    )
    append_audit(
        "impact.evaluated",
        call.trace_id,
        {"passed": impact.get("passed"), "score": impact.get("score")},
    )
    if not impact.get("passed"):
        # 红线 10/12：模型不可单独 deliver；impact 失败不交付
        return CapabilityResponse(
            status="success",
            result={
                "decision": "rework",
                "impact": impact,
                "superseded_by_feedback": False,
            },
        )
    return CapabilityResponse(
        status="success",
        result={
            "decision": "deliver",
            "impact": impact,
            "superseded_by_feedback": False,
        },
    )


def _lw_ritual_render(call: CapabilityCall) -> CapabilityResponse:
    artifact = call.inputs.get("artifact", {})
    envelope = _policy.render_ritual(
        artifact,
        call.inputs.get("artifact_type", "surprise"),
        call.inputs.get("governance", {}),
    )
    artifact_ref = (
        envelope.get("artifact", {}).get("ref", "")
        or artifact.get("payload", {}).get("asset_ref")
        or artifact.get("composition_ref", "")
    )
    # 红线 15：envelope 必须含 timing/impact ref —— 由调用方在 orchestrator 注入
    full = {
        **envelope,
        "envelope_id": f"env_{envelope.get('ritual_id', 'unknown')}",
        "intent_ref": call.intent_ref,
        "artifact_ref": artifact_ref,
        "timing_decision_ref": call.inputs.get("timing_decision_ref", ""),
        "emotion_impact_ref": call.inputs.get("emotion_impact_ref", ""),
        "consent_refs": call.inputs.get("consent_refs", []),
        "owners": call.inputs.get("owners", []),
    }
    try:
        schemas.validate_ritual_envelope(full)
    except schemas.ValidationError as exc:
        return CapabilityResponse(
            status="failed",
            error={"code": "VALIDATION_ERROR", "message": str(exc), "retryable": False},
        )
    append_audit(
        "ritual.rendered",
        call.trace_id,
        {"ritual_id": full.get("ritual_id"), "state": "ready"},
    )
    return CapabilityResponse(status="success", result=full)


def _lw_share_revoke(call: CapabilityCall) -> CapabilityResponse:
    artifact = call.inputs.get("artifact", {})
    result = _policy.revoke_share(artifact, call.inputs.get("revoked_by", ""))
    if not result.get("ok"):
        return CapabilityResponse(
            status="failed",
            error={
                "code": result.get("error", "KEEPSAKE_NOT_FOUND"),
                "message": "no keepsake",
                "retryable": False,
            },
        )
    # 红线 5：立即 SHARE_REVOKED 全表面
    append_audit(
        "share.revoked",
        call.trace_id,
        {"revoked_by": call.inputs.get("revoked_by"), "status": "SHARE_REVOKED"},
    )
    return CapabilityResponse(
        status="success",
        result={
            "status": "SHARE_REVOKED",
            "revoked_surfaces": ["bond_space", "expiring_link"],
            "enforced_at": "immediate",
        },
    )


def _lw_feedback_capture(call: CapabilityCall) -> CapabilityResponse:
    # 结构化枚举（红线 16：自由文本不入 ChangeSet/遥测）
    rating = int(call.inputs.get("rating", 0))
    kind = call.inputs.get("kind", "meaning_feedback")
    append_audit("feedback.captured", call.trace_id, {"rating": rating, "kind": kind})
    return CapabilityResponse(
        status="success",
        result={"feedback_id": f"fb_{call.trace_id}", "rating": rating, "kind": kind},
    )


def _lw_changeset_draft(call: CapabilityCall) -> CapabilityResponse:
    feedback = call.inputs.get("feedback", {})
    cs = _policy.draft_changeset(
        feedback, source_run_id=call.inputs.get("source_run_id", call.trace_id)
    )
    if cs is None:
        return CapabilityResponse(
            status="success",
            result={"changeset": None, "reason": "rating>=4, no draft"},
        )
    # 红线 14：auto_apply 恒 false（domain.ChangeSet 已强制）
    append_audit(
        "changeset.drafted",
        call.trace_id,
        {"changeset_id": cs.get("changeset_id"), "auto_apply": cs.get("auto_apply")},
    )
    return CapabilityResponse(status="success", result={"changeset": cs})


def _lw_audit_append(call: CapabilityCall) -> CapabilityResponse:
    record = append_audit(
        call.inputs.get("event", "generic"),
        call.trace_id,
        call.inputs.get("payload", {}),
    )
    return CapabilityResponse(status="success", result=record)


def _lw_keepsake_save(call: CapabilityCall) -> CapabilityResponse:
    envelope_ref = call.inputs.get("envelope_ref", "")
    owners = call.inputs.get("owners", [])
    keepsake_id = f"keep_{envelope_ref or call.trace_id}"
    append_audit(
        "keepsake.saved", call.trace_id, {"keepsake_id": keepsake_id, "owners": owners}
    )
    return CapabilityResponse(
        status="success",
        result={
            "keepsake_id": keepsake_id,
            "envelope_ref": envelope_ref,
            "owners": owners,
            "retention": "session",
            "status": "saved",
        },
    )


# === 构建默认注册表 ===


def build_registry() -> CapabilityRegistry:
    reg = CapabilityRegistry()
    reg.register("lw.consent.check", _lw_consent_check)
    reg.register("lw.consent.revoke", _lw_consent_revoke)
    reg.register("lw.policy.check", _lw_policy_check)
    reg.register("lw.surprise.compose", _lw_surprise_compose)
    reg.register("lw.pulse.compose", _lw_pulse_compose)
    reg.register("lw.pulse.duet", _lw_pulse_duet)
    reg.register("lw.timing.decide", _lw_timing_decide)
    reg.register("lw.impact.evaluate", _lw_impact_evaluate)
    reg.register("lw.ritual.render", _lw_ritual_render)
    reg.register("lw.share.revoke", _lw_share_revoke)
    reg.register("lw.feedback.capture", _lw_feedback_capture)
    reg.register("lw.changeset.draft", _lw_changeset_draft)
    reg.register("lw.audit.append", _lw_audit_append)
    reg.register("lw.keepsake.save", _lw_keepsake_save)
    return reg


# P1/P2 保留能力（返回 FEATURE_RESERVED）
RESERVED = {
    "lw.memory.weave",
    "lw.bond.async_create",
    "lw.twin.draft",
    "lw.template.publish",
}
