"""状态机编排器 — intent_created → closed + 顺序不变量。

规约来源：docs/lifewake/WORKFLOW_STATE_MACHINE.md
不变量：impact_checking 必须在 timing_deciding 之前，timing_deciding 在 ritual_rendering 之前。
consent 撤回可在任意执行态抢占。duet 断连不可静默降级为 solo（红线 17）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .capabilities import CapabilityCall, CapabilityRegistry, build_registry

# === 状态 ===

STATES = {
    "intent_created",
    "consent_checking",
    "signal_weaving",
    "device_linking",
    "composing",
    "impact_checking",
    "timing_deciding",
    "ritual_rendering",
    "delivered",
    "changeset_drafted",
    "closed",
    # 终态/错误
    "consent_required",
    "consent_revoked",
    "bond_blocked",
    "device_paused",
    "emotion_impact_failed",
    "slow_inspiration_deferred",
    "share_revoked",
    "safety_hold",
    "failed_retryable",
    "failed_final",
    "cancelled",
    "human_takeover",
}

TERMINAL = {
    "closed",
    "consent_required",
    "consent_revoked",
    "bond_blocked",
    "device_paused",
    "emotion_impact_failed",
    "slow_inspiration_deferred",
    "share_revoked",
    "safety_hold",
    "failed_final",
    "cancelled",
    "human_takeover",
}

# 合法迁移图
TRANSITIONS: dict[str, set[str]] = {
    "intent_created": {"consent_checking"},
    "consent_checking": {
        "signal_weaving",
        "device_linking",
        "consent_required",
        "consent_revoked",
        "safety_hold",
    },
    "signal_weaving": {"composing"},
    "device_linking": {"composing", "device_paused"},
    "composing": {"impact_checking", "consent_revoked", "failed_retryable"},
    "impact_checking": {"timing_deciding", "emotion_impact_failed"},
    "timing_deciding": {"ritual_rendering", "slow_inspiration_deferred"},
    "ritual_rendering": {"delivered", "failed_retryable"},
    "delivered": {"changeset_drafted", "closed"},
    "changeset_drafted": {"closed"},
}

# 顺序不变量：impact 必须在 timing 之前，timing 在 ritual 之前
ORDER = ["impact_checking", "timing_deciding", "ritual_rendering"]


class StateMachineError(RuntimeError):
    pass


@dataclass
class IntentRun:
    intent_id: str
    intent_type: str
    state: str = "intent_created"
    trace_id: str = ""
    consent_revoked: bool = False
    history: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    capability_calls: list[dict[str, Any]] = field(default_factory=list)

    def transition(self, target: str) -> None:
        if self.consent_revoked and target not in {
            "consent_revoked",
            "cancelled",
            "closed",
        }:
            # 红线 3：撤回后非审计处理 = 0
            raise StateMachineError(f"consent revoked: cannot transition to {target}")
        allowed = TRANSITIONS.get(self.state, set())
        if target not in allowed and target not in TERMINAL:
            raise StateMachineError(f"illegal transition {self.state} -> {target}")
        self.state = target
        self.history.append(target)


class Orchestrator:
    """驱动一个 Intent 走完状态机，强制顺序不变量与治理红线。"""

    def __init__(
        self,
        registry: CapabilityRegistry | None = None,
        governance: dict[str, Any] | None = None,
    ) -> None:
        self.registry = registry or build_registry()
        self.governance = governance or {}

    def run_surprise(
        self,
        run: IntentRun,
        *,
        consent: dict[str, Any] | None,
        raw_signals: list[dict[str, Any]],
        timing_window: str = "evening",
        safety_signal: dict[str, Any] | None = None,
        user_feedback: float | None = None,
        curator_score: float | None = None,
    ) -> IntentRun:
        trace = run.trace_id or run.intent_id
        run.trace_id = trace

        # 1. consent_checking
        run.transition("consent_checking")
        consent_resp = self.registry.invoke(
            CapabilityCall(
                capability="lw.consent.check",
                trace_id=trace,
                intent_ref=run.intent_id,
                inputs={
                    "consent": consent,
                    "intent_type": run.intent_type,
                    "governance": self.governance,
                },
                policy={
                    "required_scopes": _scopes(run.intent_type),
                    "purpose": "create_for_user",
                },
            )
        )
        run.capability_calls.append(
            {"capability": "lw.consent.check", "status": consent_resp.status}
        )
        if not consent_resp.is_success():
            run.transition(
                "consent_required"
                if consent_resp.error
                and consent_resp.error["code"] == "CONSENT_REQUIRED"
                else "consent_revoked"
            )
            return run

        # 2. safety（高危抢占）
        if safety_signal:
            pol = self.registry.invoke(
                CapabilityCall(
                    capability="lw.policy.check",
                    trace_id=trace,
                    intent_ref=run.intent_id,
                    inputs={"safety_signal": safety_signal},
                )
            )
            run.capability_calls.append(
                {"capability": "lw.policy.check", "status": pol.status}
            )
            if pol.status == "needs_human_review":
                run.transition("safety_hold")
                return run

        # 3. signal_weaving
        run.transition("signal_weaving")
        bundle = _policy_weave(raw_signals, consent_resp.result.get("consent_id", ""))
        if not bundle.get("ok"):
            run.transition("failed_final")
            return run
        run.artifacts["bundle"] = bundle

        # 4. composing
        run.transition("composing")
        comp = self.registry.invoke(
            CapabilityCall(
                capability="lw.surprise.compose",
                trace_id=trace,
                intent_ref=run.intent_id,
                inputs={
                    "signal_bundle": bundle,
                    "timing_window": timing_window,
                    "governance": self.governance,
                    "user_feedback": user_feedback,
                    "curator_score": curator_score,
                },
            )
        )
        run.capability_calls.append(
            {"capability": "lw.surprise.compose", "status": comp.status}
        )
        if not comp.is_success():
            run.transition("failed_retryable")
            return run
        artifact = comp.result
        run.artifacts["artifact"] = artifact

        # 5. impact_checking（顺序不变量：必须在 timing 之前）
        run.transition("impact_checking")
        impact = self.registry.invoke(
            CapabilityCall(
                capability="lw.impact.evaluate",
                trace_id=trace,
                intent_ref=run.intent_id,
                inputs={
                    "artifact": artifact,
                    "user_feedback": user_feedback,
                    "curator_score": curator_score,
                    "threshold": self.governance.get("wow_score_threshold", 0.7),
                },
            )
        )
        run.capability_calls.append(
            {"capability": "lw.impact.evaluate", "status": impact.status}
        )
        if impact.result.get("decision") != "deliver":
            run.transition("emotion_impact_failed")
            return run
        impact_ref = impact.result.get("impact", {}).get("score", 0)
        run.artifacts["impact"] = impact.result

        # 6. timing_deciding（顺序不变量：必须在 ritual 之前）
        run.transition("timing_deciding")
        timing = self.registry.invoke(
            CapabilityCall(
                capability="lw.timing.decide",
                trace_id=trace,
                intent_ref=run.intent_id,
                inputs={
                    "delivery_count_today": self.governance.get(
                        "delivery_count_today", 0
                    )
                },
            )
        )
        run.capability_calls.append(
            {"capability": "lw.timing.decide", "status": timing.status}
        )
        if timing.result.get("decision") != "DELIVER_NOW":
            # 红线 13：SLOW_INSPIRATION_DEFERRED 不通知
            run.transition("slow_inspiration_deferred")
            return run
        timing_ref = timing.result.get("decision", "DELIVER_NOW")
        run.artifacts["timing"] = timing.result

        # 7. ritual_rendering（顺序不变量：最后）
        run.transition("ritual_rendering")
        ritual = self.registry.invoke(
            CapabilityCall(
                capability="lw.ritual.render",
                trace_id=trace,
                intent_ref=run.intent_id,
                inputs={
                    "artifact": artifact,
                    "artifact_type": "surprise",
                    "governance": self.governance,
                    "timing_decision_ref": timing_ref,
                    "emotion_impact_ref": str(impact_ref),
                    "consent_refs": (
                        [consent_resp.result.get("consent_id")]
                        if consent_resp.result.get("consent_id")
                        else []
                    ),
                    "owners": [consent.get("person_id", "")] if consent else [],
                },
            )
        )
        run.capability_calls.append(
            {"capability": "lw.ritual.render", "status": ritual.status}
        )
        if not ritual.is_success():
            run.transition("failed_retryable")
            return run
        run.artifacts["envelope"] = ritual.result

        # 8. delivered
        run.transition("delivered")
        keep = self.registry.invoke(
            CapabilityCall(
                capability="lw.keepsake.save",
                trace_id=trace,
                intent_ref=run.intent_id,
                inputs={
                    "envelope_ref": ritual.result.get("envelope_id"),
                    "owners": ritual.result.get("owners", []),
                },
            )
        )
        run.capability_calls.append(
            {"capability": "lw.keepsake.save", "status": keep.status}
        )
        run.artifacts["keepsake"] = keep.result

        # 9. feedback → changeset（可选）
        if user_feedback is not None and user_feedback < 0.4:
            run.transition("changeset_drafted")
            cs = self.registry.invoke(
                CapabilityCall(
                    capability="lw.changeset.draft",
                    trace_id=trace,
                    intent_ref=run.intent_id,
                    inputs={
                        "feedback": {"rating": int(user_feedback * 5), "comment": ""},
                        "source_run_id": run.intent_id,
                    },
                )
            )
            run.capability_calls.append(
                {"capability": "lw.changeset.draft", "status": cs.status}
            )
            run.artifacts["changeset"] = cs.result

        run.transition("closed")
        return run

    def revoke_consent(self, run: IntentRun, *, consent_id: str) -> IntentRun:
        """撤回抢占：任意执行态 → consent_revoked，后续 invoke 阻断（红线 3）。"""
        self.registry.invoke(
            CapabilityCall(
                capability="lw.consent.revoke",
                trace_id=run.trace_id or run.intent_id,
                intent_ref=run.intent_id,
                inputs={"consent_id": consent_id},
            )
        )
        run.consent_revoked = True
        if run.state not in TERMINAL:
            run.transition("consent_revoked")
        return run


def _scopes(intent_type: str) -> list[str]:
    return _policy_required_scopes(intent_type)


def _policy_weave(
    raw_signals: list[dict[str, Any]], consent_ref: str
) -> dict[str, Any]:
    from .capabilities import _policy

    return _policy.weave_signal_bundle(raw_signals, consent_ref)


def _policy_required_scopes(intent_type: str) -> list[str]:
    from .capabilities import _policy

    return _policy.required_scopes_for(intent_type, {})


def verify_order_invariant(history: list[str]) -> bool:
    """校验顺序不变量：impact 在 timing 之前，timing 在 ritual 之前。"""
    indices = {name: history.index(name) for name in ORDER if name in history}
    if "timing_deciding" in indices and "impact_checking" in indices:
        if indices["timing_deciding"] <= indices["impact_checking"]:
            return False
    if "ritual_rendering" in indices and "timing_deciding" in indices:
        if indices["ritual_rendering"] <= indices["timing_deciding"]:
            return False
    return True
