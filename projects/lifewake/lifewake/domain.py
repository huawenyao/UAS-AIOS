"""类型化领域模型 — 15 个实体 + 6 不变量。

规约来源：docs/lifewake/DOMAIN_MODEL.md
所有实体为不可变 dataclass，提供 to_dict / from_dict 与不变量校验。
治理核心仍由 scripts/lifewake_policy.py 提供，本模块只做类型化与契约对齐。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

# === 枚举（与规约状态码对齐） ===

ConsentStatus = Literal["granted", "revoked", "expired"]
SurpriseStatus = Literal["composed", "delivered", "saved", "dismissed"]
PulseMode = Literal["solo", "duet"]
PulseStatus = Literal["linking", "live", "paused", "completed", "aborted"]
BondStatus = Literal["active", "paused", "dissolved"]
EnvelopeState = Literal[
    "draft", "ready", "revealed", "saved", "dismissed", "deleted", "cancelled_by_revoke"
]
TimingDecisionCode = Literal["DELIVER_NOW", "SLOW_INSPIRATION_DEFERRED", "CANCELLED"]
ImpactDecision = Literal["deliver", "rework", "curate", "defer", "reject"]
ShareStatus = Literal["draft", "active", "SHARE_REVOKED", "expired"]
RiskLevel = Literal["G0", "G1", "G2", "G3", "G4"]
ChangeSetStatus = Literal["draft", "approved", "applied", "rolled_back", "rejected"]

ALLOWED_PURPOSE = "create_for_user"
DENIED_PURPOSES = {"profile_user", "ads", "score_user"}


class DomainError(ValueError):
    """领域不变量违反。"""


# === 实体 ===


@dataclass(frozen=True)
class Person:
    person_id: str
    display_name: str
    persona_tags: tuple[str, ...] = ()
    style_prefs: tuple[str, ...] = ()
    locale: str = "zh-CN"


@dataclass(frozen=True)
class ConsentGrant:
    consent_id: str
    person_id: str
    scopes: tuple[str, ...]
    purpose: str = ALLOWED_PURPOSE
    status: ConsentStatus = "granted"
    granted_at: str = ""
    revoked_at: str | None = None
    withdrawable: bool = True
    beneficiaries: tuple[str, ...] = ()
    expires_at: str = ""
    processor_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.purpose != ALLOWED_PURPOSE:
            raise DomainError(
                f"purpose must be {ALLOWED_PURPOSE!r}, got {self.purpose!r}"
            )
        if self.purpose in DENIED_PURPOSES:
            raise DomainError(f"denied purpose {self.purpose!r}")
        if not self.withdrawable:
            raise DomainError("consent must be withdrawable")
        if not self.expires_at:
            raise DomainError(
                "consent must have explicit expires_at (no indefinite implicit grant)"
            )
        if not self.scopes:
            raise DomainError("consent must declare at least one scope")


@dataclass(frozen=True)
class SignalBundle:
    bundle_id: str
    person_id: str
    signals: tuple[dict[str, str], ...]
    sensitivity: Literal["low"] = "low"
    consent_ref: str = ""


@dataclass(frozen=True)
class Surprise:
    surprise_id: str
    kind: Literal["song", "artwork", "inspiration_task"]
    payload: dict[str, Any]
    inspiration_trace: tuple[dict[str, str], ...]
    timing_window: str
    impact_ref: str = ""
    status: SurpriseStatus = "composed"
    uniqueness_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.uniqueness_refs:
            raise DomainError("surprise requires non-empty uniqueness_refs (E-02)")


@dataclass(frozen=True)
class PulseSession:
    session_id: str
    mode: PulseMode
    participants: tuple[str, ...]
    device_refs: tuple[str, ...] = ()
    style: str = ""
    mix_ratio: float | None = None
    composition_ref: str = ""
    sync_visual: dict[str, Any] | None = None
    status: PulseStatus = "linking"


@dataclass(frozen=True)
class Bond:
    bond_id: str
    members: tuple[str, ...]
    needs: dict[str, dict[str, Any]]
    shared_artifacts: tuple[str, ...] = ()
    status: BondStatus = "active"

    def __post_init__(self) -> None:
        if len(self.members) != 2:
            raise DomainError("bond must have exactly 2 members")


@dataclass(frozen=True)
class Intent:
    intent_id: str
    intent_type: str
    goal: str
    actor_ref: str
    risk_level: RiskLevel = "G0"
    business_object_ref: str = ""


@dataclass(frozen=True)
class AuditEvent:
    audit_id: str
    event: str
    trace_id: str
    payload: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        forbidden = {
            "raw_pulse_stream",
            "free_text_feedback",
            "partner_rejection_reason",
            "exact_age",
            "diagnostic_inference",
        }
        leaked = forbidden & set(self.payload.keys())
        if leaked:
            raise DomainError(f"audit payload must not contain {leaked} (red line 16)")


@dataclass(frozen=True)
class EmotionImpact:
    impact_id: str
    artifact_ref: str
    user_feedback: dict[str, Any] = field(default_factory=dict)
    curation_rubric: dict[str, Any] = field(default_factory=dict)
    model_auxiliary: dict[str, Any] = field(default_factory=dict)
    decision: ImpactDecision = "deliver"
    rationale: tuple[str, ...] = ()
    superseded_by_feedback: bool = False


@dataclass(frozen=True)
class TimingDecision:
    timing_id: str
    decision: TimingDecisionCode
    reason_codes: tuple[str, ...] = ()
    reconsider_after: str = ""
    policy_version: str = "1.0"
    user_overridable: bool = False


@dataclass(frozen=True)
class Keepsake:
    keepsake_id: str
    envelope_ref: str
    owners: tuple[str, ...]
    retention: str = "session"
    status: Literal["saved", "revoked", "expired"] = "saved"


@dataclass(frozen=True)
class ShareGrant:
    share_id: str
    keepsake_ref: str
    grantor: str
    surface: str
    expires_at: str = ""
    status: ShareStatus = "draft"


@dataclass(frozen=True)
class PolicyDecision:
    decision_id: str
    risk_level: RiskLevel
    rules: tuple[str, ...]
    result: str
    next_action: str = ""


@dataclass(frozen=True)
class ChangeSet:
    changeset_id: str
    source: str
    target_pack: str
    summary: str
    evidence: tuple[dict[str, Any], ...] = ()
    hypothesis: str = ""
    impact_scope: str = ""
    guardrails: tuple[str, ...] = ()
    regression_cases: tuple[str, ...] = ()
    rollback_ref: str = ""
    auto_apply: bool = False
    status: ChangeSetStatus = "draft"

    def __post_init__(self) -> None:
        if self.auto_apply:
            raise DomainError("ChangeSet auto_apply must be false (EV-02)")
        if self.target_pack not in {
            "surprise_policy",
            "pulse_policy",
            "consent_copy",
            "agent",
        }:
            raise DomainError(f"unknown target_pack {self.target_pack!r}")


@dataclass(frozen=True)
class RitualEnvelope:
    envelope_id: str
    ritual_id: str
    intent_ref: str
    artifact_ref: str
    content_blocks: tuple[dict[str, Any], ...] = ()
    inspiration_trace: tuple[dict[str, str], ...] = ()
    consent_refs: tuple[str, ...] = ()
    timing_decision_ref: str = ""
    emotion_impact_ref: str = ""
    owners: tuple[str, ...] = ()
    actions: tuple[dict[str, str], ...] = ()
    accessibility: dict[str, Any] = field(default_factory=dict)
    state: EnvelopeState = "draft"

    def __post_init__(self) -> None:
        if not self.timing_decision_ref or not self.emotion_impact_ref:
            raise DomainError(
                "RitualEnvelope requires timing_decision_ref + emotion_impact_ref (red line 15)"
            )


# === 序列化辅助 ===


def to_dict(entity: Any) -> dict[str, Any]:
    return asdict(entity)


def from_dict(cls: type, data: dict[str, Any]) -> Any:
    """从 dict 重建实体（容忍多余字段，按字段名过滤）。"""
    import dataclasses as dc

    if not dc.is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass")
    names = {f.name for f in dc.fields(cls)}
    filtered = {k: v for k, v in data.items() if k in names}
    return cls(**filtered)
