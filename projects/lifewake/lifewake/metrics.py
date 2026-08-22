"""指标层 — MRCR 北极星 + M-01~M-18 + 护栏否决。

规约来源：docs/lifewake/METRICS_GROWTH_AND_BUSINESS.md
从 database/runs/*.json 聚合运行事实，计算指标。遥测事件净化（红线 16）。
"""

from __future__ import annotations

from typing import Any

from .store import Store

# 遥测禁含字段（红线 16）
TELEMETRY_FORBIDDEN = {
    "raw_pulse_stream",
    "hum_content",
    "photo_content",
    "free_text_feedback_body",
    "partner_rejection_reason",
    "health_inference",
}

# 护栏否决触发（即使 MRCR↑也回滚实验）
GUARDRAIL_VETO = [
    "post_revoke_processing_gt_zero",  # M-08 > 0
    "minor_or_external_violation",
    "duet_missing_both_consent",
    "model_overrides_negative_feedback",
    "intrusive_threshold_breach",
    "commercial_erosion_free_sovereignty",
]


class MetricsError(ValueError):
    pass


def sanitize_telemetry(event: dict[str, Any]) -> dict[str, Any]:
    """净化遥测事件（红线 16）。"""
    props = event.get("properties", {})
    leaked = TELEMETRY_FORBIDDEN & set(props.keys())
    if leaked:
        raise MetricsError(f"telemetry contains forbidden keys: {sorted(leaked)}")
    return event


def compute_mrcr(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """MRCR = meaningful_rituals / eligible_revealed_rituals。

    meaningful_ritual = consent_valid AND ritual_revealed AND user_feedback in
    {meaningful, moved, worth_keeping} AND no safety/privacy violation AND
    no regret_revoke_within_safety_window.
    """
    eligible = [r for r in runs if r.get("ritual_revealed") and r.get("consent_valid")]
    meaningful = [
        r
        for r in eligible
        if r.get("user_feedback_label") in {"meaningful", "moved", "worth_keeping"}
        and not r.get("safety_violation")
        and not r.get("regret_revoke_within_safety_window")
    ]
    rate = len(meaningful) / len(eligible) if eligible else 0.0
    return {
        "mrcr": round(rate, 4),
        "meaningful_rituals": len(meaningful),
        "eligible_revealed_rituals": len(eligible),
    }


def compute_metrics(store: Store | None = None) -> dict[str, Any]:
    """从 store.runs 聚合 M-01~M-18。"""
    store = store or Store()
    runs = store.runs.list_all()

    post_revoke_processing = sum(
        1 for r in runs if r.get("post_revoke_processing_count", 0) > 0
    )
    duet_runs = [r for r in runs if r.get("intent_type") == "pulse_duet"]
    duet_both_consent = sum(1 for r in duet_runs if r.get("both_consent_complete"))
    share_revokes = [r for r in runs if r.get("share_revoked")]
    share_revoke_success = sum(
        1 for r in share_revokes if r.get("share_revoke_enforced")
    )
    changesets = [r for r in runs if r.get("changeset")]
    changeset_evidence_complete = sum(
        1 for r in changesets if r.get("changeset", {}).get("evidence")
    )

    metrics = {
        "M-01_mrcr": compute_mrcr(runs)["mrcr"],
        "M-02_user_meaning_confirmation_rate": _avg(runs, "meaning_confirmation"),
        "M-03_source_comprehension_rate": _avg(runs, "trace_viewed"),
        "M-04_trace_coverage": _avg(runs, "trace_coverage"),
        "M-05_low_impact_interception_rate": _avg(runs, "low_impact_intercepted"),
        "M-06_curation_rubric_consistency": _avg(runs, "rubric_consistency"),
        "M-07_valid_consent_completeness": _avg(runs, "consent_complete"),
        "M-08_post_revoke_new_processing_count": post_revoke_processing,
        "M-09_revoke_enforcement_p95_latency_ms": _p95(runs, "revoke_latency_ms"),
        "M-10_bilateral_consent_completeness_duet": _ratio(
            duet_both_consent, len(duet_runs)
        ),
        "M-11_share_revoke_success_rate": _ratio(
            share_revoke_success, len(share_revokes)
        ),
        "M-12_intrusive_feedback_rate": _avg(runs, "intrusive_feedback"),
        "M-13_defer_acceptance_rate": _avg(runs, "defer_accepted"),
        "M-14_safe_disconnect_recovery_rate": _avg(runs, "disconnect_recovered"),
        "M-15_active_revisit_rate": _avg(runs, "revisited_no_push"),
        "M-16_voluntary_reduet_rate_30d": _avg(runs, "voluntary_reduet"),
        "M-17_changeset_evidence_completeness": _ratio(
            changeset_evidence_complete, len(changesets)
        ),
        "M-18_value_qualified_paid_conversion": _avg(runs, "paid_conversion"),
    }
    metrics["guardrail_veto"] = _guardrail_veto(metrics, runs)
    return metrics


def _avg(runs: list[dict[str, Any]], key: str) -> float:
    vals = [r.get(key) for r in runs if r.get(key) is not None]
    return round(sum(vals) / len(vals), 4) if vals else 0.0


def _ratio(numer: int, denom: int) -> float:
    return round(numer / denom, 4) if denom else 0.0


def _p95(runs: list[dict[str, Any]], key: str) -> float:
    vals = sorted(r.get(key, 0) for r in runs if r.get(key) is not None)
    if not vals:
        return 0.0
    idx = max(0, int(len(vals) * 0.95) - 1)
    return round(vals[idx], 2)


def _guardrail_veto(metrics: dict[str, Any], runs: list[dict[str, Any]]) -> list[str]:
    vetoed: list[str] = []
    if metrics.get("M-08_post_revoke_new_processing_count", 0) > 0:
        vetoed.append("post_revoke_processing_gt_zero")
    if any(r.get("minor_or_external_violation") for r in runs):
        vetoed.append("minor_or_external_violation")
    if any(
        r.get("intent_type") == "pulse_duet" and not r.get("both_consent_complete")
        for r in runs
    ):
        vetoed.append("duet_missing_both_consent")
    if any(r.get("model_overrides_negative_feedback") for r in runs):
        vetoed.append("model_overrides_negative_feedback")
    return vetoed
