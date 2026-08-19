"""真实输入边界 — CLI / JSON 入口。

规约来源：docs/lifewake/FUNCTIONAL_DESIGN.md
非仅 CASE 夹具：接受真实 Intent JSON，走完整状态机，持久化运行事实与审计。
用法：
  python3 -m lifewake.cli --intent '{"intent_type":"surprise_delivery",...}'
  echo '{"intent_type":"surprise_delivery",...}' | python3 -m lifewake.cli
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .capabilities import audit_log, reset_audit
from .orchestrator import IntentRun, Orchestrator
from .store import Store
from . import metrics as metrics_mod


def _load_governance() -> dict[str, Any]:
    import pathlib

    root = pathlib.Path(__file__).resolve().parents[1]
    path = root / "configs" / "governance_policy.json"
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def run_intent(
    payload: dict[str, Any],
    *,
    store: Store | None = None,
    orchestrator: Orchestrator | None = None,
) -> dict[str, Any]:
    """真实输入边界：把用户 Intent 走完状态机并持久化。"""
    store = store or Store()
    gov = _load_governance()
    orch = orchestrator or Orchestrator(
        governance={**gov, **payload.get("governance_override", {})}
    )

    intent_id = (
        payload.get("intent_id")
        or f"intent_{payload.get('intent_type', 'surprise')}_{abs(hash(json.dumps(payload, sort_keys=True))) % 100000:05d}"
    )
    run = IntentRun(
        intent_id=intent_id, intent_type=payload.get("intent_type", "surprise_delivery")
    )

    reset_audit()
    if payload.get("intent_type", "surprise_delivery") in (
        "surprise_delivery",
        "surprise",
    ):
        orch.run_surprise(
            run,
            consent=payload.get("consent"),
            raw_signals=payload.get("raw_signals", []),
            timing_window=payload.get("timing_window", "evening"),
            safety_signal=payload.get("safety_signal"),
            user_feedback=payload.get("user_feedback"),
            curator_score=payload.get("curator_score"),
        )
    else:
        # pulse / duet 等走通用入口（本版聚焦 surprise 闭环，其余返回 reserved）
        run.transition("consent_checking")
        run.transition("closed")

    # 持久化运行事实
    record = {
        "run_id": intent_id,
        "intent_type": run.intent_type,
        "state": {"final": run.state},
        "history": run.history,
        "capability_calls": run.capability_calls,
        "artifacts": run.artifacts,
        "audit": audit_log(),
        "ritual_revealed": run.state in {"delivered", "closed", "changeset_drafted"},
        "consent_valid": run.state not in {"consent_required", "consent_revoked"},
        "delivery_date": payload.get("delivery_date"),
    }
    store.save_run(intent_id, record)
    if run.artifacts.get("envelope"):
        store.save_envelope(run.artifacts["envelope"])
    for event in audit_log():
        store.append_audit_jsonl(event)
    if run.artifacts.get("changeset") and run.artifacts["changeset"].get("changeset"):
        cs = run.artifacts["changeset"]["changeset"]
        store.save_changeset(cs.get("changeset_id", intent_id), cs)

    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LifeWake 真实输入边界")
    parser.add_argument("--intent", help="Intent JSON 字符串")
    parser.add_argument("--metrics", action="store_true", help="输出指标快照")
    parser.add_argument("--pretty", action="store_true", help="格式化输出")
    args = parser.parse_args(argv)

    if args.metrics:
        out = metrics_mod.compute_metrics()
        print(json.dumps(out, ensure_ascii=False, indent=2 if args.pretty else None))
        return 0

    payload_str = args.intent
    if not payload_str and not sys.stdin.isatty():
        payload_str = sys.stdin.read()
    if not payload_str:
        parser.error("需要 --intent 或 stdin 提供 Intent JSON")
        return 2

    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError as exc:
        print(
            json.dumps(
                {"error": "invalid json", "detail": str(exc)}, ensure_ascii=False
            ),
            file=sys.stderr,
        )
        return 2

    record = run_intent(payload)
    print(
        json.dumps(
            record, ensure_ascii=False, indent=2 if args.pretty else None, default=str
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
