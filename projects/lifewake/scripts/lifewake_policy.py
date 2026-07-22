"""LifeWake 治理与创作策略（对齐 docs/lifewake/GOVERNANCE_MATRIX.md）。"""

from __future__ import annotations

from typing import Any


ALLOWED_PURPOSE = "create_for_user"
DENIED_PURPOSES = {"profile_user", "ads", "score_user"}


def required_scopes_for(intent_type: str, governance: dict) -> list[str]:
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
    consent: dict | None,
    required_scopes: list[str],
    *,
    purpose: str | None = None,
) -> tuple[bool, str | None, dict]:
    """返回 (allowed, error_code, detail)。"""
    consent = consent or {}
    status = consent.get("status", "missing")
    purpose = purpose or consent.get("purpose") or ALLOWED_PURPOSE

    if purpose in DENIED_PURPOSES or purpose != ALLOWED_PURPOSE:
        return False, "POLICY_DENIED", {"reason": "purpose_not_create_for_user", "purpose": purpose}

    if status == "revoked":
        return False, "CONSENT_REVOKED", {"status": status}

    if status != "granted":
        return False, "CONSENT_REQUIRED", {"status": status, "missing_scopes": required_scopes}

    granted = set(consent.get("scopes") or [])
    missing = [s for s in required_scopes if s not in granted]
    if missing:
        return False, "CONSENT_REQUIRED", {"missing_scopes": missing}

    return True, None, {"consent_id": consent.get("consent_id", "consent_ok"), "scopes": list(granted)}


def check_multi_consent(
    consent_by_person: dict[str, dict],
    participants: list[str],
    required_scopes: list[str],
) -> tuple[bool, str | None, dict]:
    details: dict[str, Any] = {}
    for pid in participants:
        ok, code, detail = check_consent(consent_by_person.get(pid), required_scopes)
        details[pid] = detail
        if not ok:
            return False, code, {"failed_person": pid, "detail": detail, "by_person": details}
    return True, None, {"by_person": details}


def check_bond_bidirectional(needs_met: list[str] | None, participants: list[str]) -> tuple[bool, str | None]:
    met = set(needs_met or [])
    if not participants or not set(participants).issubset(met):
        return False, "BOND_ASYMMETRIC"
    return True, None


def compose_surprise(signals: list[dict], timing_window: str, governance: dict) -> dict[str, Any]:
    if not signals:
        return {"ok": False, "error": "VALIDATION_ERROR", "message": "signals_required"}

    kinds_priority = []
    kinds_map = {
        "hum_melody": "song",
        "favorite_artist_style": "song",
        "late_night_search": "artwork",
        "geo_coarse": "inspiration_task",
        "mood_hint": "inspiration_task",
    }
    for s in signals:
        k = kinds_map.get(s.get("kind"))
        if k and k not in kinds_priority:
            kinds_priority.append(k)
    kind = kinds_priority[0] if kinds_priority else "song"

    uniqueness_refs = [s.get("kind") for s in signals if s.get("kind")]
    if not uniqueness_refs:
        return {"ok": False, "error": "VALIDATION_ERROR", "message": "uniqueness_refs_required"}

    trace = []
    for s in signals:
        trace.append(
            {
                "signal": s.get("kind"),
                "explanation": f"基于你的「{s.get('kind')}」信号（{s.get('value')}）写入作品基因",
            }
        )

    titles = {
        "song": "潜意识旋律 · 回响",
        "artwork": "隐秘关键词 · 画幅",
        "inspiration_task": "街角微行动 · 灵感任务",
    }
    payload = {
        "asset_ref": f"mock://{kind}/sur_generated",
        "title": titles[kind],
        "summary": f"在 {timing_window} 窗口为你炼成的{kind}惊喜",
    }
    # mock：有特有信号即视为高情感冲击
    wow_score = 0.86 if len(uniqueness_refs) >= 2 else 0.74
    threshold = float(governance.get("wow_score_threshold", 0.7))
    return {
        "ok": True,
        "surprise_id": "sur_generated",
        "kind": kind,
        "payload": payload,
        "inspiration_trace": trace,
        "uniqueness_refs": uniqueness_refs,
        "timing_window": timing_window,
        "wow_score": wow_score,
        "impact_passed": wow_score >= threshold,
    }


def compose_pulse_solo(person_id: str, style: str, device_linked: bool) -> dict[str, Any]:
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


def compose_pulse_duet(
    participants: list[str],
    style: str,
    needs_met: list[str] | None,
    share_keepsake: bool = True,
) -> dict[str, Any]:
    ok, code = check_bond_bidirectional(needs_met, participants)
    if not ok:
        return {"ok": False, "error": code}
    return {
        "ok": True,
        "session_id": "pulse_duet_" + "_".join(participants),
        "mode": "duet",
        "style": style,
        "composition_ref": "mock://audio/pulse_duet.wav",
        "sync_visual": {"correlation": 0.82, "motif": "interwoven_waves"},
        "keepsake_ref": "mock://keepsake/pulse_duet" if share_keepsake else None,
        "bond_check": {"bidirectional": True, "needs_met": list(participants)},
        "wow_score": 0.9,
        "risk_level": "G3",
    }


def simulate_connector(case: dict) -> dict[str, Any]:
    mock = case.get("mock_failure") or {}
    if not mock:
        return {"ok": True, "retries": 0}
    error = mock.get("error", "CONNECTOR_UNAVAILABLE")
    max_retries = 3
    return {
        "ok": True,
        "retries": max_retries,
        "errors": [{"attempt": i, "code": error} for i in range(1, max_retries)],
        "recovered": True,
    }


def render_ritual(artifact: dict, artifact_type: str, governance: dict) -> dict[str, Any]:
    threshold = float(governance.get("wow_score_threshold", 0.7))
    wow = float(artifact.get("wow_score", 0))
    passed = wow >= threshold and artifact.get("impact_passed", wow >= threshold)
    narrative = {
        "surprise": "这是你潜意识写给自己的回信。",
        "pulse": "你的身体正在歌唱；此刻被听见、被铭记。",
    }.get(artifact_type, "一次自我确认的仪式。")
    return {
        "ritual_id": f"ritual_{artifact.get('surprise_id') or artifact.get('session_id') or 'x'}",
        "narrative": narrative,
        "inspiration_trace": artifact.get("inspiration_trace") or [],
        "emotion_impact": {"wow_score": wow, "passed": passed, "threshold": threshold},
    }
