"""LifeWake 的可审计治理、创作、情感评估与演化策略。"""

from __future__ import annotations

from datetime import date
from typing import Any, Iterable

ALLOWED_PURPOSE = "create_for_user"
DENIED_PURPOSES = {"profile_user", "ads", "score_user"}
DEFAULT_MAX_RETRIES = 3


def required_scopes_for(intent_type: str, governance: dict[str, Any]) -> list[str]:
    mapping = governance.get("consent_scopes") or {
        "surprise": ["signals.low_sensitivity"],
        "pulse_solo": ["device.pulse"],
        "pulse_duet": ["device.pulse", "share.partner"],
    }
    key = {
        "surprise_delivery": "surprise",
        "pulse_solo": "pulse_solo",
        "pulse_duet": "pulse_duet",
    }.get(intent_type, "surprise")
    return list(mapping.get(key, []))


def check_consent(
    consent: dict[str, Any] | None,
    required_scopes: Iterable[str],
    *,
    purpose: str | None = None,
    subject_age: int | None = None,
) -> tuple[bool, str | None, dict[str, Any]]:
    """检查用途、撤回、未成年人监护授权和精确 scope。"""
    consent = consent or {}
    resolved_purpose = purpose or consent.get("purpose")
    required = list(required_scopes)

    if resolved_purpose != ALLOWED_PURPOSE or resolved_purpose in DENIED_PURPOSES:
        return False, "POLICY_DENIED", {
            "reason": "purpose_not_create_for_user",
            "purpose": resolved_purpose,
        }
    if consent.get("status", "missing") == "revoked" or consent.get("revoked_at"):
        return False, "CONSENT_REVOKED", {
            "consent_id": consent.get("consent_id"),
            "revoked_at": consent.get("revoked_at"),
        }
    if subject_age is not None and subject_age < 18 and not consent.get("guardian_consent"):
        return False, "MINOR_GUARDIAN_REQUIRED", {"subject_age": subject_age}
    if consent.get("status") != "granted":
        return False, "CONSENT_REQUIRED", {
            "status": consent.get("status", "missing"),
            "missing_scopes": required,
        }

    granted = set(consent.get("scopes") or [])
    missing = [scope for scope in required if scope not in granted]
    if missing:
        return False, "CONSENT_REQUIRED", {"missing_scopes": missing}
    return True, None, {
        "consent_id": consent.get("consent_id"),
        "purpose": resolved_purpose,
        "scopes": sorted(granted),
    }


def check_multi_consent(
    consent_by_person: dict[str, dict[str, Any]],
    participants: list[str],
    required_scopes: list[str],
) -> tuple[bool, str | None, dict[str, Any]]:
    details: dict[str, Any] = {}
    for person_id in participants:
        ok, code, detail = check_consent(
            consent_by_person.get(person_id),
            required_scopes,
        )
        details[person_id] = detail
        if not ok:
            return False, code, {
                "failed_person": person_id,
                "detail": detail,
                "by_person": details,
            }
    return True, None, {"by_person": details}


def weave_signal_bundle(
    raw_signals: list[dict[str, Any]],
    consent_ref: str | None,
) -> dict[str, Any]:
    """将 raw signals 归一去重，并保留授权和独特性证据。"""
    if not consent_ref:
        return {"ok": False, "error": "CONSENT_REFERENCE_REQUIRED"}

    seen: set[tuple[str, str]] = set()
    signals: list[dict[str, Any]] = []
    for raw in raw_signals:
        kind = str(raw.get("kind", "")).strip()
        value = str(raw.get("value", "")).strip()
        if not kind or not value:
            continue
        identity = (kind, value.casefold())
        if identity in seen:
            continue
        seen.add(identity)
        signals.append({"kind": kind, "value": value})

    uniqueness_refs = list(dict.fromkeys(signal["kind"] for signal in signals))
    if not signals or not uniqueness_refs:
        return {"ok": False, "error": "VALIDATION_ERROR"}
    return {
        "ok": True,
        "bundle_id": f"bundle_{consent_ref}",
        "consent_ref": consent_ref,
        "signals": signals,
        "raw_count": len(raw_signals),
        "deduplicated_count": len(signals),
        "uniqueness_refs": uniqueness_refs,
    }


def decide_timing(
    run_history: list[dict[str, Any]] | None = None,
    *,
    delivery_count_today: int | None = None,
) -> dict[str, Any]:
    """第三次当日交付请求延后，避免“慢灵感”沦为装饰。"""
    if delivery_count_today is None:
        today = date.today().isoformat()
        delivery_count_today = sum(
            1
            for run in run_history or []
            if run.get("delivery_date") == today
            and run.get("state", {}).get("final") == "delivered"
        )
    if delivery_count_today >= 2:
        return {
            "allowed": False,
            "code": "SLOW_INSPIRATION_DEFERRED",
            "delivery_count_today": delivery_count_today,
            "retry": "next_day",
        }
    return {
        "allowed": True,
        "code": "TIMING_ALLOWED",
        "delivery_count_today": delivery_count_today,
        "slot": delivery_count_today + 1,
    }


def check_safety_signal(
    safety_signal: dict[str, Any] | None,
) -> tuple[bool, str | None, dict[str, Any]]:
    """高危信号只进入非诊断支持路径，不进入娱乐化创作。"""
    safety_signal = safety_signal or {}
    category = safety_signal.get("category")
    if category in {"possible_self_harm", "imminent_harm", "abuse_risk"}:
        return False, "SAFETY_HUMAN_REVIEW", {
            "category": category,
            "confidence": safety_signal.get("confidence", "unknown"),
            "support_options": ["trusted_person", "local_crisis_resource", "exit"],
            "diagnosis": None,
        }
    return True, None, {"category": category or "none"}


def assess_emotion_impact(
    artifact: dict[str, Any],
    *,
    user_feedback: float | None = None,
    curator_score: float | None = None,
    threshold: float = 0.7,
) -> dict[str, Any]:
    """用可解释 rubric 计算情感冲击，不接收预期通过值。"""
    refs = set(artifact.get("uniqueness_refs") or [])
    trace = artifact.get("inspiration_trace") or []
    traced_refs = {item.get("signal") for item in trace if item.get("explanation")}
    uniqueness = min(len(refs) / 2, 1.0)
    traceability = len(refs & traced_refs) / len(refs) if refs else 0.0
    actionability = float(artifact.get("actionability", 0.0))
    feedback = 0.5 if user_feedback is None else max(0.0, min(float(user_feedback), 1.0))
    curator = 0.5 if curator_score is None else max(0.0, min(float(curator_score), 1.0))
    components = {
        "uniqueness": round(uniqueness, 4),
        "traceability": round(traceability, 4),
        "actionability": round(actionability, 4),
        "user_feedback": round(feedback, 4),
        "curator_score": round(curator, 4),
    }
    weights = {
        "uniqueness": 0.30,
        "traceability": 0.25,
        "actionability": 0.20,
        "user_feedback": 0.15,
        "curator_score": 0.10,
    }
    score = round(sum(components[key] * weights[key] for key in weights), 4)
    passed = score >= threshold
    return {
        "score": score,
        "threshold": threshold,
        "passed": passed,
        "code": "EMOTION_IMPACT_PASSED" if passed else "EMOTION_IMPACT_FAILED",
        "breakdown": {
            key: {"score": components[key], "weight": weights[key]}
            for key in weights
        },
    }


def compose_surprise(
    signal_bundle: dict[str, Any],
    timing_window: str,
    governance: dict[str, Any],
    *,
    user_feedback: float | None = None,
    curator_score: float | None = None,
) -> dict[str, Any]:
    if not signal_bundle.get("ok"):
        return {
            "ok": False,
            "error": signal_bundle.get("error", "VALIDATION_ERROR"),
        }
    signals = signal_bundle["signals"]
    kinds_map = {
        "hum_melody": "song",
        "favorite_artist_style": "song",
        "late_night_search": "artwork",
        "geo_coarse": "inspiration_task",
        "mood_hint": "inspiration_task",
    }
    kind = next(
        (kinds_map[s["kind"]] for s in signals if s["kind"] in kinds_map),
        "song",
    )
    trace = [
        {
            "signal": signal["kind"],
            "explanation": f"授权信号「{signal['kind']}」被转译为作品动机",
        }
        for signal in signals
    ]
    actionability = (
        0.9
        if kind in {"song", "artwork"} or len(signals) >= 2
        else 0.25
    )
    artifact: dict[str, Any] = {
        "ok": True,
        "surprise_id": f"sur_{signal_bundle['bundle_id']}",
        "kind": kind,
        "payload": {
            "asset_ref": f"mock://{kind}/{signal_bundle['bundle_id']}",
            "title": {
                "song": "潜意识旋律 · 回响",
                "artwork": "隐秘关键词 · 画幅",
                "inspiration_task": "街角微行动 · 灵感任务",
            }[kind],
            "summary": f"在 {timing_window} 窗口炼成的 {kind} 惊喜",
        },
        "consent_ref": signal_bundle["consent_ref"],
        "inspiration_trace": trace,
        "uniqueness_refs": signal_bundle["uniqueness_refs"],
        "timing_window": timing_window,
        "actionability": actionability,
    }
    impact = assess_emotion_impact(
        artifact,
        user_feedback=user_feedback,
        curator_score=curator_score,
        threshold=float(governance.get("wow_score_threshold", 0.7)),
    )
    artifact["emotion_impact"] = impact
    artifact["wow_score"] = impact["score"]
    return artifact


def compose_pulse_solo(
    person_id: str,
    style: str,
    device_linked: bool,
) -> dict[str, Any]:
    if not device_linked:
        return {"ok": False, "error": "DEVICE_NOT_LINKED"}
    return {
        "ok": True,
        "session_id": f"pulse_solo_{person_id}",
        "mode": "solo",
        "style": style,
        "composition_ref": f"mock://audio/pulse_solo_{person_id}.wav",
        "waveform_ref": f"mock://visual/pulse_solo_{person_id}.json",
        "tempo_map": [{"t": 0, "bpm_from_hr": 72}, {"t": 30, "bpm_from_hr": 88}],
        "wow_score": 0.81,
    }


def check_bond_bidirectional(
    bond_participants: list[dict[str, Any]],
    participants: list[str],
) -> tuple[bool, str | None, dict[str, Any]]:
    """双方均须声明 needs，且其 needs 被另一方明确确认。"""
    by_id = {item.get("person_id"): item for item in bond_participants}
    missing: list[dict[str, str]] = []
    for person_id in participants:
        record = by_id.get(person_id) or {}
        if not record.get("needs"):
            missing.append({"person_id": person_id, "reason": "needs_missing"})
            continue
        acknowledgers = set(record.get("needs_acknowledged_by") or [])
        expected = set(participants) - {person_id}
        if not expected.issubset(acknowledgers):
            missing.append(
                {"person_id": person_id, "reason": "needs_not_acknowledged"}
            )
    if missing:
        return False, "BOND_ASYMMETRIC", {"failures": missing}
    return True, None, {"participants": participants, "bidirectional": True}


def compose_pulse_duet(
    participants: list[str],
    style: str,
    bond_participants: list[dict[str, Any]],
    share_keepsake: bool = True,
) -> dict[str, Any]:
    ok, code, bond_check = check_bond_bidirectional(
        bond_participants,
        participants,
    )
    if not ok:
        return {"ok": False, "error": code, "bond_check": bond_check}
    return {
        "ok": True,
        "session_id": "pulse_duet_" + "_".join(participants),
        "mode": "duet",
        "style": style,
        "composition_ref": "mock://audio/pulse_duet.wav",
        "sync_visual": {"correlation": 0.82, "motif": "interwoven_waves"},
        "keepsake": {
            "keepsake_ref": "mock://keepsake/pulse_duet",
            "state": "shared" if share_keepsake else "private",
        },
        "bond_check": bond_check,
        "wow_score": 0.9,
        "risk_level": "G3",
    }


def revoke_share(artifact: dict[str, Any], revoked_by: str) -> dict[str, Any]:
    keepsake = artifact.get("keepsake")
    if not keepsake:
        return {"ok": False, "error": "KEEPSAKE_NOT_FOUND"}
    keepsake["state"] = "revoked"
    keepsake["revoked_by"] = revoked_by
    return {"ok": True, "keepsake": keepsake}


def simulate_connector(
    failure: dict[str, Any] | None,
    *,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> dict[str, Any]:
    """失败 fail_times 次后恢复；超过重试预算则明确耗尽。"""
    failure = failure or {}
    fail_times = max(0, int(failure.get("fail_times", 0)))
    error = failure.get("error", "CONNECTOR_UNAVAILABLE")
    errors = [
        {"attempt": attempt, "code": error}
        for attempt in range(1, min(fail_times, max_retries) + 1)
    ]
    recovered = fail_times <= max_retries
    return {
        "ok": recovered,
        "recovered": recovered and fail_times > 0,
        "exhausted": not recovered,
        "retries": len(errors),
        "attempts": len(errors) + (1 if recovered else 0),
        "errors": errors,
        "error": None if recovered else "CONNECTOR_RETRY_EXHAUSTED",
    }


def draft_changeset(
    feedback: dict[str, Any],
    *,
    source_run_id: str,
) -> dict[str, Any] | None:
    rating = int(feedback.get("rating", 0))
    if rating >= 4:
        return None
    comment = str(feedback.get("comment", "")).strip()
    return {
        "changeset_id": f"cs_{source_run_id}",
        "target_pack": "surprise_policy",
        "summary": (
            "提升作品可执行性并保留反馈证据"
            if "执行" in comment or "空泛" in comment
            else "复核低评分体验的独特性与可追溯性"
        ),
        "auto_apply": False,
        "source": "delivered_user_feedback",
        "evidence": {
            "source_run_id": source_run_id,
            "rating": rating,
            "comment": comment,
        },
    }


def render_ritual(
    artifact: dict[str, Any],
    artifact_type: str,
    governance: dict[str, Any],
) -> dict[str, Any]:
    threshold = float(governance.get("wow_score_threshold", 0.7))
    impact = artifact.get("emotion_impact") or {
        "score": float(artifact.get("wow_score", 0)),
        "threshold": threshold,
        "passed": float(artifact.get("wow_score", 0)) >= threshold,
        "code": "EMOTION_IMPACT_PASSED"
        if float(artifact.get("wow_score", 0)) >= threshold
        else "EMOTION_IMPACT_FAILED",
        "breakdown": {},
    }
    narrative = {
        "surprise": "这是你潜意识写给自己的回信。",
        "pulse": "你的身体正在歌唱；此刻被听见、被铭记。",
    }.get(artifact_type, "一次自我确认的仪式。")
    artifact_id = (
        artifact.get("surprise_id") or artifact.get("session_id") or "unknown"
    )
    return {
        "schema_version": "1.0",
        "ritual_id": f"ritual_{artifact_id}",
        "title": artifact.get("payload", {}).get("title", "生命回响"),
        "narrative": narrative,
        "artifact": {
            "type": artifact_type,
            "ref": artifact.get("payload", {}).get("asset_ref")
            or artifact.get("composition_ref"),
        },
        "inspiration_trace": artifact.get("inspiration_trace") or [],
        "emotion_impact": impact,
        "actions": [
            {"id": "feedback", "label": "记录此刻感受"},
            {"id": "keep", "label": "珍藏回响"},
        ],
    }
