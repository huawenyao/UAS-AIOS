#!/usr/bin/env python3
"""运行 Enterprise Sales OS subapp（UAS Runtime）。"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def _bootstrap_asui_path() -> None:
    if importlib.util.find_spec("asui") is not None:
        return
    here = Path(__file__).resolve()
    for i in range(2, min(12, len(here.parents))):
        base = here.parents[i]
        for candidate in (base / "asui-cli" / "src", base / "src"):
            if (candidate / "asui" / "engine" / "runtime_manager.py").is_file():
                sys.path.insert(0, str(candidate))
                return


_bootstrap_asui_path()
from asui.engine.runtime_manager import RuntimeManager  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 Enterprise Sales OS")
    parser.add_argument("topic", help="业务议题")
    parser.add_argument("--payload-json", help="额外 JSON payload")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--sales-case-id", default="CASE-001", help="MVP 用例 ID")
    args = parser.parse_args()

    payload = json.loads(args.payload_json) if args.payload_json else {}
    payload.setdefault("sales_case_id", args.sales_case_id)
    payload.setdefault("governance_controls", ["audit", "approval", "rollback"])
    payload.setdefault("evolution_loop", ["intent_activation", "governance_check", "sales_execute"])

    manager = RuntimeManager(Path(__file__).resolve().parents[1])
    result = manager.run(args.topic, payload=payload, evaluate=args.evaluate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
