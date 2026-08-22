from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from lifewake_policy import (  # noqa: E402
    assess_emotion_impact,
    check_bond_bidirectional,
    check_consent,
    check_safety_signal,
    decide_timing,
    revoke_share,
    simulate_connector,
    weave_signal_bundle,
)


def test_consent_enforces_purpose_scope_and_revoke() -> None:
    consent = {
        "consent_id": "c1",
        "status": "granted",
        "purpose": "create_for_user",
        "scopes": ["signals.low_sensitivity"],
    }
    assert check_consent(consent, ["signals.low_sensitivity"])[0]
    assert check_consent(
        {**consent, "purpose": "profile_user"},
        ["signals.low_sensitivity"],
    )[1] == "POLICY_DENIED"
    assert check_consent(
        {**consent, "status": "revoked"},
        ["signals.low_sensitivity"],
    )[1] == "CONSENT_REVOKED"
    assert check_consent(consent, ["device.pulse"])[1] == "CONSENT_REQUIRED"


def test_signal_bundle_deduplicates_and_carries_consent() -> None:
    bundle = weave_signal_bundle(
        [
            {"kind": "hum_melody", "value": "A"},
            {"kind": "hum_melody", "value": "a"},
            {"kind": "mood_hint", "value": "curious"},
        ],
        "consent-1",
    )
    assert bundle["consent_ref"] == "consent-1"
    assert bundle["raw_count"] == 3
    assert bundle["deduplicated_count"] == 2
    assert bundle["uniqueness_refs"] == ["hum_melody", "mood_hint"]


def test_third_delivery_is_actually_deferred() -> None:
    assert decide_timing(delivery_count_today=1)["allowed"]
    decision = decide_timing(delivery_count_today=2)
    assert not decision["allowed"]
    assert decision["code"] == "SLOW_INSPIRATION_DEFERRED"


def test_emotion_rubric_can_fail_and_explains_score() -> None:
    impact = assess_emotion_impact(
        {
            "uniqueness_refs": ["mood_hint"],
            "inspiration_trace": [
                {"signal": "mood_hint", "explanation": "generic"}
            ],
            "actionability": 0.1,
        },
        user_feedback=0.0,
        curator_score=0.0,
    )
    assert not impact["passed"]
    assert impact["code"] == "EMOTION_IMPACT_FAILED"
    assert set(impact["breakdown"]) == {
        "uniqueness",
        "traceability",
        "actionability",
        "user_feedback",
        "curator_score",
    }


def test_connector_recovers_or_exhausts_real_retry_budget() -> None:
    recovered = simulate_connector({"fail_times": 2})
    assert recovered["ok"] and recovered["retries"] == 2
    exhausted = simulate_connector({"fail_times": 4})
    assert not exhausted["ok"]
    assert exhausted["exhausted"]
    assert exhausted["retries"] == 3


def test_bond_requires_declared_and_cross_acknowledged_needs() -> None:
    participants = ["ada", "lee"]
    ok, _, _ = check_bond_bidirectional(
        [
            {
                "person_id": "ada",
                "needs": ["heard"],
                "needs_acknowledged_by": ["lee"],
            },
            {
                "person_id": "lee",
                "needs": ["memory"],
                "needs_acknowledged_by": ["ada"],
            },
        ],
        participants,
    )
    assert ok
    blocked, code, _ = check_bond_bidirectional(
        [
            {
                "person_id": "ada",
                "needs": ["heard"],
                "needs_acknowledged_by": [],
            }
        ],
        participants,
    )
    assert not blocked and code == "BOND_ASYMMETRIC"


def test_share_revoke_changes_keepsake_state() -> None:
    artifact = {"keepsake": {"state": "shared", "keepsake_ref": "mock://k"}}
    assert revoke_share(artifact, "lee")["ok"]
    assert artifact["keepsake"] == {
        "state": "revoked",
        "keepsake_ref": "mock://k",
        "revoked_by": "lee",
    }


def test_high_risk_signal_stops_entertainment_generation() -> None:
    safe, code, detail = check_safety_signal(
        {"category": "possible_self_harm", "confidence": "uncertain"}
    )
    assert not safe
    assert code == "SAFETY_HUMAN_REVIEW"
    assert detail["diagnosis"] is None
    assert "local_crisis_resource" in detail["support_options"]
