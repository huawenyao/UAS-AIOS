#!/usr/bin/env python3
"""LifeWake MVP 验收 CASE-001～008。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lifewake_policy import (  # noqa: E402
    check_consent,
    check_multi_consent,
    compose_pulse_duet,
    compose_pulse_solo,
    compose_surprise,
    render_ritual,
    required_scopes_for,
    simulate_connector,
)

ALL_CASES: list[dict] = [
    {
        "case_id": "CASE-001",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": {
            "consent_id": "c_ada_signals",
            "scopes": ["signals.low_sensitivity"],
            "status": "granted",
            "purpose": "create_for_user",
        },
        "signals": [
            {"kind": "hum_melody", "value": "motif_jazzy_03"},
            {"kind": "favorite_artist_style", "value": "jazz_vocal"},
        ],
        "timing_window": "boredom",
    },
    {
        "case_id": "CASE-002",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": {"scopes": [], "status": "missing"},
    },
    {
        "case_id": "CASE-003",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": {
            "scopes": ["signals.low_sensitivity"],
            "status": "revoked",
            "purpose": "create_for_user",
        },
    },
    {
        "case_id": "CASE-004",
        "intent_type": "pulse_solo",
        "person_id": "person_ada",
        "consent": {
            "scopes": ["device.pulse"],
            "status": "granted",
            "purpose": "create_for_user",
        },
        "device_linked": True,
        "style": "nature",
    },
    {
        "case_id": "CASE-005",
        "intent_type": "pulse_duet",
        "bond_id": "bond_ada_lee",
        "participants": ["person_ada", "person_lee"],
        "consent_by_person": {
            "person_ada": {
                "scopes": ["device.pulse", "share.partner"],
                "status": "granted",
                "purpose": "create_for_user",
            },
            "person_lee": {
                "scopes": ["device.pulse", "share.partner"],
                "status": "granted",
                "purpose": "create_for_user",
            },
        },
        "needs_met": ["person_ada", "person_lee"],
        "style": "classical",
    },
    {
        "case_id": "CASE-006",
        "intent_type": "pulse_duet",
        "participants": ["person_ada", "person_lee"],
        "consent_by_person": {
            "person_ada": {
                "scopes": ["device.pulse", "share.partner"],
                "status": "granted",
                "purpose": "create_for_user",
            },
            "person_lee": {
                "scopes": ["device.pulse", "share.partner"],
                "status": "granted",
                "purpose": "create_for_user",
            },
        },
        "needs_met": ["person_ada"],
        "style": "classical",
    },
    {
        "case_id": "CASE-007",
        "intent_type": "surprise_delivery",
        "person_id": "person_ada",
        "consent": {
            "scopes": ["signals.low_sensitivity"],
            "status": "granted",
            "purpose": "create_for_user",
        },
        "signals": [{"kind": "mood_hint", "value": "lonely_curious"}],
        "timing_window": "commute",
        "mock_failure": {"capability": "lw.surprise.compose", "error": "CONNECTOR_UNAVAILABLE"},
    },
    {
        "case_id": "CASE-008",
        "intent_type": "feedback_review",
        "feedback": {
            "feedback_type": "wow_rating",
            "target_ref": "sur_meh_001",
            "rating": 2,
            "wow_score": 0.42,
            "comment": "灵感任务太空泛，不够可执行",
            "suggested_change": {
                "target_pack": "surprise_policy",
                "summary": "灵感任务必须落到一句话可执行动作",
            },
        },
    },
]


def validate_expectations(case_id: str, result: dict[str, Any]) -> list[dict]:
    errors: list[dict] = []
    state = result.get("state", {})
    codes = {result.get("business_code")} if result.get("business_code") else set()
    codes |= {e.get("code") for e in result.get("errors", []) if e.get("code")}

    def fail(msg: str) -> list[dict]:
        return [{"code": f"E-{case_id}", "message": msg}]

    checks = {
        "CASE-001": lambda: (
            []
            if state.get("final") in ("delivered", "closed")
            and result.get("artifact", {}).get("uniqueness_refs")
            and result.get("ritual", {}).get("emotion_impact", {}).get("passed")
            else fail("CASE-001 mismatch")
        ),
        "CASE-002": lambda: (
            []
            if "CONSENT_REQUIRED" in codes and state.get("final") == "consent_required"
            and not result.get("artifact")
            else fail("CASE-002 mismatch")
        ),
        "CASE-003": lambda: (
            []
            if "CONSENT_REVOKED" in codes and state.get("final") == "consent_revoked"
            else fail("CASE-003 mismatch")
        ),
        "CASE-004": lambda: (
            []
            if state.get("final") in ("delivered", "closed")
            and result.get("artifact", {}).get("mode") == "solo"
            and result.get("artifact", {}).get("composition_ref")
            else fail("CASE-004 mismatch")
        ),
        "CASE-005": lambda: (
            []
            if state.get("final") in ("delivered", "closed")
            and result.get("artifact", {}).get("bond_check", {}).get("bidirectional")
            and result.get("artifact", {}).get("sync_visual")
            and result.get("intent", {}).get("risk_level") == "G3"
            else fail("CASE-005 mismatch")
        ),
        "CASE-006": lambda: (
            []
            if "BOND_ASYMMETRIC" in codes and state.get("final") == "bond_blocked"
            else fail("CASE-006 mismatch")
        ),
        "CASE-007": lambda: (
            []
            if result.get("connector", {}).get("ok")
            and result.get("connector", {}).get("retries", 0) <= 3
            and state.get("final") in ("delivered", "closed")
            else fail("CASE-007 mismatch")
        ),
        "CASE-008": lambda: (
            []
            if result.get("changeset")
            and result.get("changeset", {}).get("auto_apply") is False
            and state.get("final") == "changeset_drafted"
            else fail("CASE-008 mismatch")
        ),
    }
    if case_id in checks:
        errors.extend(checks[case_id]())
    return errors


def _base_intent(case: dict, risk: str = "G2") -> dict:
    return {
        "intent_id": f"intent-{case['case_id']}",
        "actor": case.get("person_id") or (case.get("participants") or ["unknown"])[0],
        "intent_type": case.get("intent_type"),
        "risk_level": risk,
        "business_object": case.get("intent_type"),
    }


def _wm(subjects: list[str], objects: list[str], drive: list[str], blockers: list[str], connectors: list[str]) -> dict:
    return {
        "subjects": subjects,
        "objects": objects,
        "drive": drive,
        "blockers": blockers,
        "connectors": connectors,
    }


def run_case(case: dict, governance: dict) -> dict[str, Any]:
    case_id = case["case_id"]
    intent_type = case.get("intent_type", "surprise_delivery")
    audit: list[dict] = [{"event": "intent", "case_id": case_id, "intent_type": intent_type}]
    errors: list[dict] = []

    if intent_type == "feedback_review":
        fb = case["feedback"]
        changeset = {
            "changeset_id": f"cs-draft-{case_id}",
            "target_pack": fb["suggested_change"]["target_pack"],
            "summary": fb["suggested_change"]["summary"],
            "auto_apply": False,
            "source": "human_feedback",
            "evidence": {"wow_score": fb.get("wow_score"), "comment": fb.get("comment")},
        }
        audit.extend(
            [
                {"event": "feedback", "rating": fb["rating"], "comment": fb["comment"]},
                {"event": "changeset_draft", "changeset_id": changeset["changeset_id"]},
            ]
        )
        result = {
            "case_id": case_id,
            "passed": True,
            "intent": _base_intent(case, "G1"),
            "consent": {"skipped": True},
            "audit": audit,
            "report": {"conclusion": "changeset_drafted", "next_step": "human_approval_for_apply"},
            "world_model_view": _wm(["reviewer"], ["feedback"], [], [], ["evolution_listener"]),
            "state": {"final": "changeset_drafted"},
            "changeset": changeset,
            "errors": [],
        }
        result["errors"] = validate_expectations(case_id, result)
        result["passed"] = not result["errors"]
        return result

    # Consent gate
    if intent_type == "pulse_duet":
        participants = case.get("participants") or []
        scopes = required_scopes_for(intent_type, governance)
        ok, code, detail = check_multi_consent(case.get("consent_by_person") or {}, participants, scopes)
        audit.append({"event": "consent", "ok": ok, "detail": detail})
        if not ok:
            errors.append({"code": code, "message": "multi_consent_failed", "next_step": "request_partner_consent"})
            result = {
                "case_id": case_id,
                "passed": False,
                "business_code": code,
                "intent": _base_intent(case, "G3"),
                "consent": detail,
                "audit": audit,
                "report": {"conclusion": "blocked", "next_step": "request_partner_consent"},
                "world_model_view": _wm(participants, ["consent"], ["duet_desire"], [code or ""], ["lw.consent.check"]),
                "state": {"final": "consent_required" if code == "CONSENT_REQUIRED" else "consent_revoked"},
                "errors": errors,
            }
            result["errors"] = errors + validate_expectations(case_id, result)
            result["passed"] = not validate_expectations(case_id, {**result, "errors": errors})
            # re-validate cleanly
            result["errors"] = validate_expectations(case_id, result)
            result["passed"] = len(result["errors"]) == 0
            return result

        pulse = compose_pulse_duet(participants, case.get("style", "classical"), case.get("needs_met"))
        audit.append({"event": "capability", "name": "lw.pulse.duet", "ok": pulse.get("ok")})
        if not pulse.get("ok"):
            code = pulse.get("error", "BOND_ASYMMETRIC")
            errors.append({"code": code, "message": "bond_check_failed", "next_step": "balance_both_needs"})
            result = {
                "case_id": case_id,
                "passed": False,
                "business_code": code,
                "intent": _base_intent(case, "G3"),
                "consent": detail,
                "audit": audit + [{"event": "result", "error": code}],
                "report": {"conclusion": "bond_blocked", "next_step": "balance_both_needs"},
                "world_model_view": _wm(participants, ["bond"], ["connection"], [code], ["lw.pulse.duet"]),
                "state": {"final": "bond_blocked"},
                "errors": errors,
            }
            result["errors"] = validate_expectations(case_id, result)
            result["passed"] = not result["errors"]
            return result

        ritual = render_ritual(pulse, "pulse", governance)
        audit.append({"event": "ritual", "ritual_id": ritual["ritual_id"], "wow": ritual["emotion_impact"]})
        audit.append({"event": "result", "status": "delivered"})
        result = {
            "case_id": case_id,
            "passed": True,
            "intent": _base_intent(case, pulse.get("risk_level", "G3")),
            "consent": detail,
            "artifact": pulse,
            "ritual": ritual,
            "audit": audit,
            "report": {
                "conclusion": "duet_delivered",
                "composition_ref": pulse.get("composition_ref"),
                "sync_visual": pulse.get("sync_visual"),
                "next_step": "save_keepsake",
            },
            "world_model_view": _wm(
                participants,
                ["pulse_session", "bond", "ritual"],
                ["longing", "connection"],
                [],
                ["lw.pulse.duet", "lw.ritual.render"],
            ),
            "state": {"final": "delivered"},
            "errors": [],
        }
        result["errors"] = validate_expectations(case_id, result)
        result["passed"] = not result["errors"]
        return result

    # Single-person consent paths
    scopes = required_scopes_for(intent_type, governance)
    ok, code, detail = check_consent(case.get("consent"), scopes)
    audit.append({"event": "consent", "ok": ok, "detail": detail})
    if not ok:
        final = "consent_revoked" if code == "CONSENT_REVOKED" else "consent_required"
        if code == "POLICY_DENIED":
            final = "failed_final"
        errors.append({"code": code, "message": "consent_gate_failed", "next_step": "guide_consent"})
        result = {
            "case_id": case_id,
            "passed": False,
            "business_code": code,
            "intent": _base_intent(case),
            "consent": detail,
            "audit": audit,
            "report": {"conclusion": "blocked", "next_step": "guide_consent"},
            "world_model_view": _wm(
                [case.get("person_id", "person")],
                ["consent"],
                [],
                [code or ""],
                ["lw.consent.check"],
            ),
            "state": {"final": final},
            "errors": errors,
            "artifact": None,
        }
        result["errors"] = validate_expectations(case_id, result)
        result["passed"] = not result["errors"]
        return result

    connector = simulate_connector(case)
    if case.get("mock_failure"):
        audit.extend(connector.get("errors", []))
        audit.append({"event": "connector", "result": "recovered_after_retry", "retries": connector.get("retries")})

    if intent_type == "pulse_solo":
        pulse = compose_pulse_solo(case.get("person_id", "person"), case.get("style", "nature"), case.get("device_linked", False))
        audit.append({"event": "capability", "name": "lw.pulse.compose", "ok": pulse.get("ok")})
        if not pulse.get("ok"):
            code = pulse.get("error", "DEVICE_NOT_LINKED")
            result = {
                "case_id": case_id,
                "passed": False,
                "business_code": code,
                "intent": _base_intent(case),
                "consent": detail,
                "audit": audit,
                "report": {"conclusion": "blocked", "next_step": "link_device"},
                "world_model_view": _wm([case.get("person_id")], ["device"], ["meditation"], [code], ["lw.pulse.compose"]),
                "state": {"final": "device_not_linked"},
                "errors": [{"code": code}],
            }
            result["errors"] = validate_expectations(case_id, result)
            result["passed"] = not result["errors"]
            return result
        ritual = render_ritual(pulse, "pulse", governance)
        audit.append({"event": "ritual", "ritual_id": ritual["ritual_id"]})
        audit.append({"event": "result", "status": "delivered"})
        result = {
            "case_id": case_id,
            "passed": True,
            "intent": _base_intent(case),
            "consent": detail,
            "artifact": pulse,
            "ritual": ritual,
            "connector": connector,
            "audit": audit,
            "report": {"conclusion": "solo_pulse_delivered", "composition_ref": pulse["composition_ref"]},
            "world_model_view": _wm(
                [case.get("person_id")],
                ["pulse_session", "ritual"],
                ["embodiment"],
                [],
                ["lw.pulse.compose", "lw.ritual.render"],
            ),
            "state": {"final": "delivered"},
            "errors": [],
        }
        result["errors"] = validate_expectations(case_id, result)
        result["passed"] = not result["errors"]
        return result

    # surprise_delivery
    surprise = compose_surprise(case.get("signals") or [], case.get("timing_window", "boredom"), governance)
    audit.append({"event": "capability", "name": "lw.surprise.compose", "ok": surprise.get("ok")})
    if not surprise.get("ok"):
        code = surprise.get("error", "VALIDATION_ERROR")
        result = {
            "case_id": case_id,
            "passed": False,
            "business_code": code,
            "intent": _base_intent(case),
            "consent": detail,
            "audit": audit,
            "report": {"conclusion": "failed", "next_step": "fix_signals"},
            "world_model_view": _wm([case.get("person_id")], ["surprise"], [], [code], ["lw.surprise.compose"]),
            "state": {"final": "failed_final"},
            "errors": [{"code": code}],
        }
        result["errors"] = validate_expectations(case_id, result)
        result["passed"] = not result["errors"]
        return result

    ritual = render_ritual(surprise, "surprise", governance)
    if not ritual["emotion_impact"]["passed"]:
        result = {
            "case_id": case_id,
            "passed": False,
            "business_code": "EMOTION_IMPACT_FAILED",
            "intent": _base_intent(case),
            "consent": detail,
            "artifact": surprise,
            "ritual": ritual,
            "audit": audit + [{"event": "impact", "failed": True}],
            "report": {"conclusion": "emotion_impact_failed", "next_step": "recompose_or_curate"},
            "world_model_view": _wm([case.get("person_id")], ["surprise"], ["boredom"], ["EMOTION_IMPACT_FAILED"], ["lw.ritual.render"]),
            "state": {"final": "emotion_impact_failed"},
            "errors": [{"code": "EMOTION_IMPACT_FAILED"}],
        }
        result["errors"] = validate_expectations(case_id, result)
        result["passed"] = not result["errors"]
        return result

    audit.append({"event": "ritual", "ritual_id": ritual["ritual_id"], "wow": ritual["emotion_impact"]})
    audit.append({"event": "result", "status": "delivered"})
    result = {
        "case_id": case_id,
        "passed": True,
        "intent": _base_intent(case),
        "consent": detail,
        "artifact": surprise,
        "ritual": ritual,
        "connector": connector,
        "audit": audit,
        "report": {
            "conclusion": "surprise_delivered",
            "kind": surprise.get("kind"),
            "inspiration_trace": surprise.get("inspiration_trace"),
            "next_step": "optional_save",
        },
        "world_model_view": _wm(
            [case.get("person_id")],
            ["surprise", "ritual"],
            [case.get("timing_window", "boredom")],
            [],
            ["lw.surprise.compose", "lw.ritual.render"],
        ),
        "state": {"final": "delivered"},
        "errors": [],
    }
    result["errors"] = validate_expectations(case_id, result)
    result["passed"] = not result["errors"]
    return result


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    governance = json.loads((root / "configs" / "governance_policy.json").read_text(encoding="utf-8")).get(
        "governance", {}
    )

    results = [run_case(c, governance) for c in ALL_CASES]
    summary = {
        "app": "lifewake",
        "mvp_version": "v0.1",
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": [r["case_id"] for r in results if not r["passed"]],
        "results": results,
    }

    out_dir = root / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "lifewake_mvp_acceptance.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# LifeWake MVP 验收报告",
        "",
        f"- 通过: {summary['passed']}/{summary['total']}",
        f"- 失败: {', '.join(summary['failed']) if summary['failed'] else '无'}",
        "",
    ]
    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        lines.append(f"- `{r['case_id']}` {mark} → `{r.get('state', {}).get('final')}`")
    (out_dir / "lifewake_mvp_acceptance.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"passed": summary["passed"], "total": summary["total"], "failed": summary["failed"]}, ensure_ascii=False))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
