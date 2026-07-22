#!/usr/bin/env python3
"""执行 LifeWake CASE-001～014 的行为验收。"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lifewake_policy import (  # noqa: E402
    check_consent,
    check_multi_consent,
    check_safety_signal,
    compose_pulse_duet,
    compose_pulse_solo,
    compose_surprise,
    decide_timing,
    draft_changeset,
    render_ritual,
    required_scopes_for,
    revoke_share,
    simulate_connector,
    weave_signal_bundle,
)

GRANTED_SIGNAL_CONSENT = {
    "consent_id": "consent_signals",
    "scopes": ["signals.low_sensitivity"],
    "status": "granted",
    "purpose": "create_for_user",
}
GRANTED_PULSE_CONSENT = {
    "consent_id": "consent_pulse",
    "scopes": ["device.pulse"],
    "status": "granted",
    "purpose": "create_for_user",
}
GRANTED_DUET_CONSENT = {
    "consent_id": "consent_duet",
    "scopes": ["device.pulse", "share.partner"],
    "status": "granted",
    "purpose": "create_for_user",
}
GOOD_SIGNALS = [
    {"kind": "hum_melody", "value": "motif_jazzy_03"},
    {"kind": "favorite_artist_style", "value": "jazz_vocal"},
]
GOOD_BOND = [
    {
        "person_id": "person_ada",
        "needs": ["被听见"],
        "needs_acknowledged_by": ["person_lee"],
    },
    {
        "person_id": "person_lee",
        "needs": ["共同纪念"],
        "needs_acknowledged_by": ["person_ada"],
    },
]

ALL_CASES: list[dict[str, Any]] = [
    {
        "case_id": "CASE-001",
        "scenario": "正常惊喜",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": deepcopy(GRANTED_SIGNAL_CONSENT),
        "signals": deepcopy(GOOD_SIGNALS),
        "curator_score": 0.9,
    },
    {
        "case_id": "CASE-002",
        "scenario": "无同意",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": {"status": "missing", "purpose": "create_for_user"},
    },
    {
        "case_id": "CASE-003",
        "scenario": "撤回",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": {
            **deepcopy(GRANTED_SIGNAL_CONSENT),
            "status": "revoked",
            "revoked_at": "2026-07-22T00:00:00Z",
        },
    },
    {
        "case_id": "CASE-004",
        "scenario": "solo",
        "intent_type": "pulse_solo",
        "person_id": "person_ada",
        "consent": deepcopy(GRANTED_PULSE_CONSENT),
        "device_linked": True,
        "style": "nature",
    },
    {
        "case_id": "CASE-005",
        "scenario": "duet",
        "intent_type": "pulse_duet",
        "participants": ["person_ada", "person_lee"],
        "consent_by_person": {
            "person_ada": deepcopy(GRANTED_DUET_CONSENT),
            "person_lee": deepcopy(GRANTED_DUET_CONSENT),
        },
        "bond_participants": deepcopy(GOOD_BOND),
    },
    {
        "case_id": "CASE-006",
        "scenario": "非双向",
        "intent_type": "pulse_duet",
        "participants": ["person_ada", "person_lee"],
        "consent_by_person": {
            "person_ada": deepcopy(GRANTED_DUET_CONSENT),
            "person_lee": deepcopy(GRANTED_DUET_CONSENT),
        },
        "bond_participants": [
            deepcopy(GOOD_BOND[0]),
            {
                "person_id": "person_lee",
                "needs": ["共同纪念"],
                "needs_acknowledged_by": [],
            },
        ],
    },
    {
        "case_id": "CASE-007",
        "scenario": "connector recovery",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": deepcopy(GRANTED_SIGNAL_CONSENT),
        "signals": deepcopy(GOOD_SIGNALS),
        "connector_failure": {
            "fail_times": 2,
            "error": "CONNECTOR_UNAVAILABLE",
        },
        "curator_score": 0.9,
    },
    {
        "case_id": "CASE-008",
        "scenario": "低 wow",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": deepcopy(GRANTED_SIGNAL_CONSENT),
        "signals": [{"kind": "mood_hint", "value": "generic"}],
        "user_feedback": 0.1,
        "curator_score": 0.1,
    },
    {
        "case_id": "CASE-009",
        "scenario": "慢灵感 defer",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": deepcopy(GRANTED_SIGNAL_CONSENT),
        "signals": deepcopy(GOOD_SIGNALS),
        "delivery_count_today": 2,
    },
    {
        "case_id": "CASE-010",
        "scenario": "共享撤回",
        "intent_type": "pulse_duet",
        "participants": ["person_ada", "person_lee"],
        "consent_by_person": {
            "person_ada": deepcopy(GRANTED_DUET_CONSENT),
            "person_lee": deepcopy(GRANTED_DUET_CONSENT),
        },
        "bond_participants": deepcopy(GOOD_BOND),
        "revoke_share_by": "person_lee",
    },
    {
        "case_id": "CASE-011",
        "scenario": "未成年人受限路径",
        "intent_type": "pulse_duet",
        "person_id": "person_minor",
        "age_gate": "minor",
        "requested_actions": ["pulse_solo", "pulse_duet", "external_share"],
    },
    {
        "case_id": "CASE-012",
        "scenario": "Pulse 设备断连",
        "intent_type": "pulse_duet",
        "participants": ["person_ada", "person_lee"],
        "consent_by_person": {
            "person_ada": deepcopy(GRANTED_DUET_CONSENT),
            "person_lee": deepcopy(GRANTED_DUET_CONSENT),
        },
        "bond_participants": deepcopy(GOOD_BOND),
        "inject_event": {
            "after_state": "live",
            "participant": "person_lee",
            "event": "device.disconnected",
        },
        "user_resolution": "reconnect",
    },
    {
        "case_id": "CASE-013",
        "scenario": "高危信号停止娱乐化生成",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": deepcopy(GRANTED_SIGNAL_CONSENT),
        "safety_signal": {
            "category": "possible_self_harm",
            "confidence": "uncertain",
        },
    },
    {
        "case_id": "CASE-014",
        "scenario": "交付→反馈→ChangeSet 串联",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": deepcopy(GRANTED_SIGNAL_CONSENT),
        "signals": deepcopy(GOOD_SIGNALS),
        "curator_score": 0.9,
        "post_delivery_feedback": {
            "feedback_id": "fb_001",
            "rating": 2,
            "signal": "not_meaningful",
            "reason_category": "too_generic",
            "comment": "灵感任务太空泛，不够可执行",
        },
    },
]


def _audit(
    audit: list[dict[str, Any]],
    stage: str,
    agent_id: str,
    **detail: Any,
) -> None:
    audit.append({"stage": stage, "agent_id": agent_id, **detail})


def _result(
    case: dict[str, Any],
    audit: list[dict[str, Any]],
    final: str,
    **values: Any,
) -> dict[str, Any]:
    result = {
        "case_id": case["case_id"],
        "scenario": case["scenario"],
        "intent": {
            "intent_id": f"intent_{case['case_id']}",
            "intent_type": case["intent_type"],
            "purpose": (
                case.get("consent", {}).get("purpose")
                or "create_for_user"
            ),
        },
        "state": {"final": final},
        "audit": audit,
        **values,
    }
    errors = validate_case(case["case_id"], result)
    result["acceptance_errors"] = errors
    result["passed"] = not errors
    return result


def _blocked(
    case: dict[str, Any],
    audit: list[dict[str, Any]],
    code: str,
    detail: dict[str, Any],
) -> dict[str, Any]:
    states = {
        "CONSENT_REQUIRED": "consent_required",
        "CONSENT_REVOKED": "consent_revoked",
        "MINOR_GUARDIAN_REQUIRED": "minor_blocked",
        "POLICY_DENIED": "policy_denied",
        "BOND_ASYMMETRIC": "bond_blocked",
        "DEVICE_NOT_LINKED": "device_not_linked",
        "SLOW_INSPIRATION_DEFERRED": "deferred",
        "CONNECTOR_RETRY_EXHAUSTED": "connector_failed",
        "EMOTION_IMPACT_FAILED": "emotion_impact_failed",
        "SAFETY_HUMAN_REVIEW": "safety_hold",
        "DEVICE_DISCONNECTED": "device_disconnected",
    }
    return _result(
        case,
        audit,
        states.get(code, "failed"),
        business_code=code,
        detail=detail,
        artifact=None,
    )


def run_case(
    case: dict[str, Any],
    governance: dict[str, Any],
) -> dict[str, Any]:
    """按输入事实执行策略；验收预期仅在执行完成后独立检查。"""
    audit: list[dict[str, Any]] = []
    intent_type = case["intent_type"]
    _audit(
        audit,
        "intent_activation",
        "intent_guard",
        intent_type=intent_type,
    )

    if case.get("age_gate") == "minor" and (
        intent_type == "pulse_duet"
        or "external_share" in case.get("requested_actions", [])
    ):
        return _blocked(
            case,
            audit,
            "POLICY_DENIED",
            {
                "reason": "minor_duet_or_external_share_denied",
                "allowed_actions": ["pulse_solo_local_preview"],
            },
        )

    safe, safety_code, safety_detail = check_safety_signal(
        case.get("safety_signal")
    )
    if not safe:
        _audit(
            audit,
            "governance_check",
            "privacy_steward",
            allowed=False,
            code=safety_code,
            detail=safety_detail,
        )
        return _blocked(
            case,
            audit,
            safety_code or "SAFETY_HUMAN_REVIEW",
            safety_detail,
        )

    scopes = required_scopes_for(intent_type, governance)

    if intent_type == "pulse_duet":
        participants = case.get("participants") or []
        ok, code, consent_detail = check_multi_consent(
            case.get("consent_by_person") or {},
            participants,
            scopes,
        )
    else:
        ok, code, consent_detail = check_consent(
            case.get("consent"),
            scopes,
            subject_age=case.get("subject_age"),
        )
    _audit(
        audit,
        "governance_check",
        "privacy_steward",
        allowed=ok,
        code=code,
        detail=consent_detail,
    )
    if not ok:
        return _blocked(
            case,
            audit,
            code or "CONSENT_REQUIRED",
            consent_detail,
        )

    timing = decide_timing(
        case.get("run_history"),
        delivery_count_today=case.get("delivery_count_today"),
    )
    _audit(
        audit,
        "agent_planning",
        "signal_weaver",
        timing=timing,
    )
    if not timing["allowed"]:
        return _blocked(case, audit, timing["code"], timing)

    connector = simulate_connector(case.get("connector_failure"))
    _audit(
        audit,
        "system_mapping",
        "connector_orchestrator",
        connector=connector,
    )
    if not connector["ok"]:
        return _blocked(
            case,
            audit,
            connector["error"],
            connector,
        )

    if intent_type == "pulse_solo":
        artifact = compose_pulse_solo(
            case.get("person_id", "person"),
            case.get("style", "nature"),
            bool(case.get("device_linked")),
        )
        if not artifact["ok"]:
            return _blocked(
                case,
                audit,
                artifact["error"],
                artifact,
            )
        ritual = render_ritual(artifact, "pulse", governance)
    elif intent_type == "pulse_duet":
        if case.get("inject_event", {}).get("event") == "device.disconnected":
            _audit(
                audit,
                "lifewake_execute",
                "pulse_composer",
                event="device.disconnected",
                participant=case["inject_event"].get("participant"),
                session_action="paused",
                user_resolution=case.get("user_resolution"),
            )
            return _blocked(
                case,
                audit,
                "DEVICE_DISCONNECTED",
                {
                    "session_action": "paused",
                    "audio_transition": "fade_out",
                    "available_actions": ["reconnect", "degrade_with_mutual_consent", "end"],
                    "health_inference": None,
                },
            )
        artifact = compose_pulse_duet(
            case.get("participants") or [],
            case.get("style", "classical"),
            case.get("bond_participants") or [],
        )
        _audit(
            audit,
            "governance_check",
            "bond_guardian",
            bond_check=artifact.get("bond_check"),
        )
        if not artifact["ok"]:
            return _blocked(
                case,
                audit,
                artifact["error"],
                artifact.get("bond_check", {}),
            )
        if case.get("revoke_share_by"):
            revoke = revoke_share(
                artifact,
                case["revoke_share_by"],
            )
            _audit(
                audit,
                "lifewake_execute",
                "bond_guardian",
                share_revoke=revoke,
            )
        ritual = render_ritual(artifact, "pulse", governance)
    else:
        bundle = weave_signal_bundle(
            case.get("signals") or [],
            consent_detail.get("consent_id"),
        )
        _audit(
            audit,
            "knowledge_binding",
            "signal_weaver",
            bundle={
                "bundle_id": bundle.get("bundle_id"),
                "deduplicated_count": bundle.get("deduplicated_count"),
            },
        )
        artifact = compose_surprise(
            bundle,
            case.get("timing_window", "boredom"),
            governance,
            user_feedback=case.get("user_feedback"),
            curator_score=case.get("curator_score"),
        )
        if not artifact["ok"]:
            return _blocked(
                case,
                audit,
                artifact["error"],
                artifact,
            )
        if not artifact["emotion_impact"]["passed"]:
            _audit(
                audit,
                "emotion_kpi_snapshot",
                "ritual_host",
                impact=artifact["emotion_impact"],
            )
            return _result(
                case,
                audit,
                "emotion_impact_failed",
                business_code="EMOTION_IMPACT_FAILED",
                artifact=artifact,
                ritual=render_ritual(artifact, "surprise", governance),
                connector=connector,
            )
        ritual = render_ritual(artifact, "surprise", governance)

    _audit(
        audit,
        "lifewake_execute",
        "surprise_alchemist"
        if intent_type == "surprise_delivery"
        else "pulse_composer",
        artifact_id=artifact.get("surprise_id")
        or artifact.get("session_id"),
    )
    _audit(
        audit,
        "emotion_kpi_snapshot",
        "ritual_host",
        impact=ritual["emotion_impact"],
    )
    values: dict[str, Any] = {
        "artifact": artifact,
        "ritual": ritual,
        "connector": connector,
        "consent": consent_detail,
    }
    feedback = case.get("post_delivery_feedback")
    if feedback:
        values["feedback"] = {
            **feedback,
            "target_ref": ritual["ritual_id"],
        }
        values["changeset"] = draft_changeset(
            values["feedback"],
            source_run_id=case["case_id"],
        )
        _audit(
            audit,
            "evolution_plan",
            "evolution_listener",
            feedback_target=ritual["ritual_id"],
            changeset_id=(values["changeset"] or {}).get("changeset_id"),
        )
    _audit(
        audit,
        "render_report",
        "ritual_host",
        ritual_id=ritual["ritual_id"],
    )
    return _result(case, audit, "delivered", **values)


def _has_code(result: dict[str, Any], code: str) -> bool:
    return result.get("business_code") == code


def _delivered(result: dict[str, Any]) -> bool:
    return result.get("state", {}).get("final") == "delivered"


CASE_ASSERTIONS: dict[str, Callable[[dict[str, Any]], bool]] = {
    "CASE-001": lambda r: _delivered(r)
    and bool(r.get("ritual", {}).get("emotion_impact", {}).get("passed"))
    and bool(r.get("artifact", {}).get("consent_ref")),
    "CASE-002": lambda r: _has_code(r, "CONSENT_REQUIRED")
    and r.get("artifact") is None,
    "CASE-003": lambda r: _has_code(r, "CONSENT_REVOKED")
    and r.get("artifact") is None,
    "CASE-004": lambda r: _delivered(r)
    and r.get("artifact", {}).get("mode") == "solo",
    "CASE-005": lambda r: _delivered(r)
    and bool(r.get("artifact", {}).get("bond_check", {}).get("bidirectional")),
    "CASE-006": lambda r: _has_code(r, "BOND_ASYMMETRIC"),
    "CASE-007": lambda r: _delivered(r)
    and r.get("connector", {}).get("recovered") is True
    and r.get("connector", {}).get("retries") == 2,
    "CASE-008": lambda r: _has_code(r, "EMOTION_IMPACT_FAILED")
    and bool(r.get("artifact", {}).get("emotion_impact", {}).get("breakdown")),
    "CASE-009": lambda r: _has_code(r, "SLOW_INSPIRATION_DEFERRED")
    and r.get("artifact") is None,
    "CASE-010": lambda r: _delivered(r)
    and r.get("artifact", {}).get("keepsake", {}).get("state") == "revoked",
    "CASE-011": lambda r: _has_code(r, "POLICY_DENIED")
    and r.get("artifact") is None
    and "pulse_solo_local_preview"
    in r.get("detail", {}).get("allowed_actions", []),
    "CASE-012": lambda r: _has_code(r, "DEVICE_DISCONNECTED")
    and r.get("detail", {}).get("session_action") == "paused",
    "CASE-013": lambda r: _has_code(r, "SAFETY_HUMAN_REVIEW")
    and r.get("state", {}).get("final") == "safety_hold"
    and r.get("artifact") is None,
    "CASE-014": lambda r: _delivered(r)
    and r.get("feedback", {}).get("target_ref")
    == r.get("ritual", {}).get("ritual_id")
    and r.get("changeset", {}).get("evidence", {}).get("source_run_id")
    == "CASE-014"
    and r.get("changeset", {}).get("auto_apply") is False,
}


def validate_case(
    case_id: str,
    result: dict[str, Any],
) -> list[dict[str, str]]:
    check = CASE_ASSERTIONS.get(case_id)
    if check is None:
        return [{"code": "UNKNOWN_CASE", "message": case_id}]
    if check(result):
        return []
    return [{"code": f"ACCEPTANCE_{case_id}", "message": "行为与验收规则不符"}]


def load_governance(root: Path) -> dict[str, Any]:
    return json.loads(
        (root / "configs" / "governance_policy.json").read_text(
            encoding="utf-8"
        )
    )["governance"]


def evaluate_all(
    governance: dict[str, Any],
) -> dict[str, Any]:
    results = [run_case(deepcopy(case), governance) for case in ALL_CASES]
    return {
        "app": "lifewake",
        "mvp_version": "v0.2",
        "total": len(results),
        "passed": sum(result["passed"] for result in results),
        "failed": [
            result["case_id"] for result in results if not result["passed"]
        ],
        "results": results,
    }


def write_acceptance_reports(
    summary: dict[str, Any],
    report_dir: Path,
) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "lifewake_mvp_acceptance.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = [
        "# LifeWake MVP 14 CASE 验收报告",
        "",
        f"- 通过: {summary['passed']}/{summary['total']}",
        f"- 失败: {', '.join(summary['failed']) or '无'}",
        "",
    ]
    lines.extend(
        f"- `{result['case_id']}` {result['scenario']}: "
        f"{'PASS' if result['passed'] else 'FAIL'} → "
        f"`{result['state']['final']}`"
        for result in summary["results"]
    )
    (report_dir / "lifewake_mvp_acceptance.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    root = _SCRIPT_DIR.parent
    summary = evaluate_all(load_governance(root))
    write_acceptance_reports(summary, root / "reports")
    print(
        json.dumps(
            {
                "passed": summary["passed"],
                "total": summary["total"],
                "failed": summary["failed"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if not summary["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
