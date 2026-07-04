"""Enterprise Sales OS 治理策略引擎（对齐 GOVERNANCE_MATRIX.md）。"""

from __future__ import annotations

from typing import Any


FINANCE_AMOUNT_THRESHOLD = 500_000
DISCOUNT_G3_THRESHOLD = 0.15
DISCOUNT_HARD_BLOCK = 0.40


def classify_risk(
    net_amount: float,
    discount_rate: float,
    account: dict | None,
    governance: dict,
) -> tuple[str, list[str]]:
    account = account or {}
    tier = account.get("tier", "mid_market")
    credit = account.get("credit_level", "A")
    threshold = governance.get("discount_approval_threshold", DISCOUNT_G3_THRESHOLD)

    if credit == "blocked":
        return "G4", []

    if discount_rate > DISCOUNT_HARD_BLOCK and tier != "strategic":
        return "G4", ["sales_manager", "finance_reviewer"]

    if net_amount >= FINANCE_AMOUNT_THRESHOLD or discount_rate > 0.25:
        return "G4", ["sales_manager", "finance_reviewer"]

    if discount_rate > threshold or net_amount >= 100_000:
        return "G3", ["sales_manager"]

    return "G2", []


def check_evidence(lead: dict, evidence: list) -> tuple[bool, str | None]:
    pain = lead.get("pain_points") or []
    if not pain and "customer_need" not in evidence:
        return False, "EVIDENCE_REQUIRED"
    if "customer_need" not in evidence:
        return False, "EVIDENCE_REQUIRED"
    return True, None


def check_credit(account: dict | None) -> tuple[bool, str | None]:
    if (account or {}).get("credit_level") == "blocked":
        return False, "BUSINESS_RULE_BLOCKED"
    return True, None


def simulate_connector(case: dict, qualified: bool) -> dict[str, Any]:
    mock = case.get("mock_failure") or {}
    if not mock or not qualified:
        return {"ok": True, "retries": 0, "final_state": None}

    error = mock.get("error", "CONNECTOR_UNAVAILABLE")
    max_retries = 3
    # MVP：第 3 次重试成功
    return {
        "ok": True,
        "retries": max_retries,
        "errors": [{"attempt": i, "code": error} for i in range(1, max_retries)],
        "final_state": "report_rendered",
    }
