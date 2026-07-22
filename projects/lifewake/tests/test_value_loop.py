from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_emotion_kpi_snapshot import (  # noqa: E402
    aggregate_metrics,
    write_snapshot,
)
from run_value_loop_prototype import run_value_loop  # noqa: E402


def test_value_loop_persists_every_stage_and_renderable_ritual(
    tmp_path: Path,
) -> None:
    loop = run_value_loop(
        {
            "intent": "把我的哼唱变成今晚的回响",
            "feedback": {
                "rating": 2,
                "comment": "希望下一次动作更可执行",
            },
        },
        project_root=ROOT,
        storage_root=tmp_path,
        run_id="test_loop",
    )

    assert loop["state"]["final"] == "delivered"
    assert loop["changeset"]["auto_apply"] is False
    assert loop["changeset"]["evidence"]["source_run_id"] == "test_loop"
    assert loop["benefit_snapshot"]["value_realized"]
    for relative in [
        "database/runs/test_loop.json",
        "database/feedback/test_loop.json",
        "database/cognitive_state/test_loop.json",
        "reports/test_loop.md",
        "reports/test_loop_ritual.html",
    ]:
        assert (tmp_path / relative).is_file()

    ritual_html = (tmp_path / "reports/test_loop_ritual.html").read_text(
        encoding="utf-8"
    )
    assert "<!doctype html>" in ritual_html
    assert "这份回响从何而来" in ritual_html
    run_record = json.loads(
        (tmp_path / "database/runs/test_loop.json").read_text(
            encoding="utf-8"
        )
    )
    assert run_record["interaction_feedback"]["target_ref"] == (
        run_record["output"]["ritual_id"]
    )


def test_kpi_snapshot_uses_run_facts(tmp_path: Path) -> None:
    records = [
        {
            "state": {"final": "delivered"},
            "generation": {
                "kind": "song",
                "uniqueness_refs": ["hum_melody"],
                "emotion_impact": {"breakdown": {"uniqueness": {}}},
            },
            "changeset": {"changeset_id": "cs1"},
        },
        {
            "state": {"final": "delivered"},
            "artifact": {
                "mode": "duet",
                "bond_check": {"bidirectional": True},
            },
        },
        {
            "state": {"final": "deferred"},
            "business_code": "SLOW_INSPIRATION_DEFERRED",
        },
    ]
    metrics = aggregate_metrics(records)
    assert metrics["validated_uniqueness_rate"] == 1.0
    assert metrics["consent_violation_count"] == 0
    assert metrics["bidirectional_bond_rate"] == 1.0
    assert metrics["slow_inspiration_compliance"] == 1.0
    assert metrics["changeset_draft_count"] == 1

    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    (runs_dir / "one.json").write_text(
        json.dumps(records[0]),
        encoding="utf-8",
    )
    output = tmp_path / "snapshot.json"
    assert write_snapshot(runs_dir=runs_dir, output_path=output)[
        "sample_size"
    ] == 1
    assert output.is_file()
