#!/usr/bin/env python3
"""从 LifeWake 运行事实聚合情感与治理 KPI。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 1.0


def aggregate_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    delivered_artifacts: list[dict[str, Any]] = []
    duet_artifacts: list[dict[str, Any]] = []
    slow_requests = 0
    slow_compliant = 0
    consent_violations = 0
    changesets = 0

    for record in records:
        result = record.get("lifewake_result", record)
        artifact = result.get("generation") or result.get("artifact")
        state = result.get("state", {}).get("final")
        if artifact and state == "delivered":
            delivered_artifacts.append(artifact)
            if artifact.get("mode") == "duet":
                duet_artifacts.append(artifact)
        if result.get("changeset"):
            changesets += 1
        code = result.get("business_code")
        if code in {
            "CONSENT_REQUIRED",
            "CONSENT_REVOKED",
            "POLICY_DENIED",
            "MINOR_GUARDIAN_REQUIRED",
        } and artifact:
            consent_violations += 1

        simulation = result.get("simulation", {})
        delivery_count = simulation.get("delivery_count_today")
        if delivery_count is not None and delivery_count >= 2:
            slow_requests += 1
            if state == "deferred":
                slow_compliant += 1
        if code == "SLOW_INSPIRATION_DEFERRED":
            slow_requests += 1
            slow_compliant += 1

    unique_validated = sum(
        bool(artifact.get("uniqueness_refs"))
        and bool(
            artifact.get("emotion_impact", {}).get("breakdown")
            or artifact.get("inspiration_trace")
        )
        for artifact in delivered_artifacts
        if artifact.get("kind")
    )
    surprise_count = sum(
        bool(artifact.get("kind")) for artifact in delivered_artifacts
    )
    bidirectional = sum(
        bool(artifact.get("bond_check", {}).get("bidirectional"))
        for artifact in duet_artifacts
    )
    return {
        "validated_uniqueness_rate": _ratio(
            unique_validated,
            surprise_count,
        ),
        "consent_violation_count": consent_violations,
        "bidirectional_bond_rate": _ratio(
            bidirectional,
            len(duet_artifacts),
        ),
        "slow_inspiration_compliance": _ratio(
            slow_compliant,
            slow_requests,
        ),
        "changeset_draft_count": changesets,
        "sample_size": len(records),
    }


def load_run_records(runs_dir: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted(runs_dir.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def write_snapshot(
    *,
    runs_dir: Path,
    output_path: Path,
) -> dict[str, Any]:
    snapshot = aggregate_metrics(load_run_records(runs_dir))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return snapshot


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runs-dir",
        type=Path,
        default=root / "database" / "runs",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "reports" / "emotion_kpi_snapshot.json",
    )
    args = parser.parse_args()
    snapshot = write_snapshot(
        runs_dir=args.runs_dir,
        output_path=args.output,
    )
    print(json.dumps(snapshot, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
