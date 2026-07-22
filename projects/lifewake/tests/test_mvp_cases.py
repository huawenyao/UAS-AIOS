from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_lifewake_mvp import (  # noqa: E402
    ALL_CASES,
    evaluate_all,
    load_governance,
    run_case,
)


def test_all_fourteen_cases_pass_behavioral_acceptance() -> None:
    summary = evaluate_all(load_governance(ROOT))
    assert summary["total"] == 14
    assert summary["passed"] == 14
    assert summary["failed"] == []


def test_case_inputs_do_not_contain_expected_outcomes() -> None:
    forbidden = {"expected", "expected_code", "expected_state", "should_pass"}
    assert all(not (forbidden & case.keys()) for case in ALL_CASES)


def test_low_wow_is_a_runtime_rubric_result() -> None:
    low_wow = deepcopy(
        next(case for case in ALL_CASES if case["case_id"] == "CASE-008")
    )
    result = run_case(low_wow, load_governance(ROOT))
    assert result["business_code"] == "EMOTION_IMPACT_FAILED"
    assert result["artifact"]["emotion_impact"]["score"] < 0.7


def test_changeset_is_derived_from_delivered_feedback_chain() -> None:
    chain = deepcopy(
        next(case for case in ALL_CASES if case["case_id"] == "CASE-014")
    )
    result = run_case(chain, load_governance(ROOT))
    assert result["state"]["final"] == "delivered"
    assert result["feedback"]["target_ref"] == result["ritual"]["ritual_id"]
    assert result["changeset"]["source"] == "delivered_user_feedback"
    assert result["changeset"]["auto_apply"] is False
    stages = {event["stage"] for event in result["audit"]}
    assert {
        "intent_activation",
        "knowledge_binding",
        "agent_planning",
        "system_mapping",
        "governance_check",
        "lifewake_execute",
        "emotion_kpi_snapshot",
        "evolution_plan",
        "render_report",
    }.issubset(stages)
    assert all(event.get("agent_id") for event in result["audit"])
