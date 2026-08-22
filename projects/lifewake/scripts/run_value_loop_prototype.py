#!/usr/bin/env python3
"""一条命令运行并持久化 LifeWake 最小价值闭环。"""

from __future__ import annotations

import argparse
import html
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from evaluate_lifewake_mvp import (  # noqa: E402
    ALL_CASES,
    load_governance,
    run_case,
)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def validate_ritual_envelope(ritual: dict[str, Any]) -> None:
    """标准库下执行 schema 的关键结构门禁。"""
    required = {
        "schema_version",
        "ritual_id",
        "title",
        "narrative",
        "artifact",
        "inspiration_trace",
        "emotion_impact",
        "actions",
    }
    missing = sorted(required - ritual.keys())
    if missing:
        raise ValueError(f"RitualEnvelope missing: {', '.join(missing)}")
    if ritual["schema_version"] != "1.0":
        raise ValueError("unsupported RitualEnvelope schema_version")
    if not isinstance(ritual["emotion_impact"].get("passed"), bool):
        raise ValueError("emotion_impact.passed must be boolean")


def render_ritual_html(
    ritual: dict[str, Any],
    *,
    run_id: str,
) -> str:
    validate_ritual_envelope(ritual)
    trace = "".join(
        "<li><strong>"
        + html.escape(str(item["signal"]))
        + "</strong> · "
        + html.escape(str(item["explanation"]))
        + "</li>"
        for item in ritual["inspiration_trace"]
    )
    impact = ritual["emotion_impact"]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(ritual["title"])}</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; min-height: 100vh; display: grid; place-items: center;
      background: radial-gradient(circle at top, #34235f, #100d1c 62%);
      color: #f8f3ff; font: 17px/1.65 system-ui, sans-serif; }}
    main {{ width: min(720px, calc(100% - 48px)); padding: 48px;
      border: 1px solid #ffffff24; border-radius: 28px;
      background: #ffffff0d; box-shadow: 0 30px 90px #0008; }}
    .eyebrow {{ color: #d8b4fe; letter-spacing: .18em; text-transform: uppercase; }}
    h1 {{ font: 700 clamp(2.3rem, 7vw, 4.8rem)/1.05 Georgia, serif; margin: .25em 0; }}
    .score {{ display: inline-block; padding: .35em .8em; border-radius: 999px;
      background: #9f7aea33; color: #eadcff; }}
    li {{ margin: .65em 0; }} button {{ border: 0; border-radius: 999px;
      padding: .9em 1.25em; margin-right: .5em; color: #160f28; background: #e9d5ff; }}
  </style>
</head>
<body><main>
  <div class="eyebrow">LifeWake · {html.escape(run_id)}</div>
  <h1>{html.escape(ritual["title"])}</h1>
  <p>{html.escape(ritual["narrative"])}</p>
  <p class="score">情感冲击 {impact["score"]:.2f} · 已通过可解释门禁</p>
  <h2>这份回响从何而来</h2><ul>{trace}</ul>
  <button type="button">记录此刻感受</button><button type="button">珍藏回响</button>
</main></body></html>
"""


def run_value_loop(
    payload: dict[str, Any],
    *,
    project_root: Path,
    storage_root: Path | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    storage_root = storage_root or project_root
    run_id = run_id or datetime.now(timezone.utc).strftime(
        "prototype_%Y%m%dT%H%M%SZ"
    )
    case = deepcopy(
        next(case for case in ALL_CASES if case["case_id"] == "CASE-014")
    )
    case["signals"] = payload.get("signals", case["signals"])
    case["timing_window"] = payload.get("timing_window", "boredom")
    case["post_delivery_feedback"] = payload.get(
        "feedback",
        case["post_delivery_feedback"],
    )
    case["curator_score"] = payload.get("curator_score", 0.9)

    simulation = {
        "connector": "mock_multimodal",
        "device": "not_required",
        "delivery_count_today": payload.get("delivery_count_today", 0),
    }
    case["delivery_count_today"] = simulation["delivery_count_today"]
    result = run_case(case, load_governance(project_root))
    if result["state"]["final"] != "delivered":
        raise RuntimeError(
            f"value loop did not deliver: {result['state']['final']}"
        )
    ritual = result["ritual"]
    validate_ritual_envelope(ritual)

    feedback = {
        **result["feedback"],
        "run_id": run_id,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    changeset = deepcopy(result["changeset"])
    changeset["changeset_id"] = f"cs_{run_id}"
    changeset["evidence"]["source_run_id"] = run_id
    benefit = {
        "run_id": run_id,
        "value_realized": True,
        "delivered": True,
        "feedback_captured": True,
        "evolution_candidate_created": changeset is not None,
        "emotion_score": ritual["emotion_impact"]["score"],
    }
    loop = {
        "run_id": run_id,
        "input": {
            "intent": payload.get("intent", "把潜意识旋律变成可感知回响"),
            "signals": case["signals"],
        },
        "simulation": simulation,
        "generation": result["artifact"],
        "interaction_feedback": feedback,
        "changeset": changeset,
        "output": ritual,
        "benefit_snapshot": benefit,
        "state": result["state"],
        "audit": result["audit"],
        "delivery_date": datetime.now(timezone.utc).date().isoformat(),
    }

    _write_json(storage_root / "database" / "runs" / f"{run_id}.json", loop)
    _write_json(
        storage_root / "database" / "feedback" / f"{run_id}.json",
        feedback,
    )
    _write_json(
        storage_root / "database" / "cognitive_state" / f"{run_id}.json",
        {
            "run_id": run_id,
            "latest_changeset": changeset,
            "benefit_snapshot": benefit,
            "auto_applied": False,
        },
    )
    report_path = storage_root / "reports" / f"{run_id}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                f"# LifeWake 价值闭环：{run_id}",
                "",
                "理念 → 体验 → 功能 → 反馈 → 演化",
                "",
                f"- 交付状态：`{result['state']['final']}`",
                f"- 情感冲击：`{ritual['emotion_impact']['score']}`",
                f"- 反馈评分：`{feedback['rating']}`",
                f"- ChangeSet：`{changeset['changeset_id']}`",
                "- 自动应用：`false`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    html_path = storage_root / "reports" / f"{run_id}_ritual.html"
    html_path.write_text(
        render_ritual_html(ritual, run_id=run_id),
        encoding="utf-8",
    )
    loop["paths"] = {
        "run": str(storage_root / "database" / "runs" / f"{run_id}.json"),
        "feedback": str(
            storage_root / "database" / "feedback" / f"{run_id}.json"
        ),
        "cognitive_state": str(
            storage_root
            / "database"
            / "cognitive_state"
            / f"{run_id}.json"
        ),
        "report": str(report_path),
        "ritual_html": str(html_path),
    }
    return loop


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--run-id")
    args = parser.parse_args()
    project_root = _SCRIPT_DIR.parent
    payload = (
        json.loads(args.input.read_text(encoding="utf-8"))
        if args.input
        else {}
    )
    loop = run_value_loop(
        payload,
        project_root=project_root,
        run_id=args.run_id,
    )
    print(
        json.dumps(
            {
                "run_id": loop["run_id"],
                "state": loop["state"]["final"],
                "changeset": loop["changeset"]["changeset_id"],
                "paths": loop["paths"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
