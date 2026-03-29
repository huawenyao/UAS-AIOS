#!/usr/bin/env python3
"""运行招聘智能OS sub uas app。"""

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
from asui.engine.runtime_manager import RuntimeManager


def main() -> int:
    parser = argparse.ArgumentParser(description="运行招聘智能OS sub uas app")
    parser.add_argument("topic", help="业务议题")
    parser.add_argument("--payload-json", help="额外 JSON payload")
    parser.add_argument("--evaluate", action="store_true", help="运行后执行评估")
    args = parser.parse_args()

    payload = json.loads(args.payload_json) if args.payload_json else None
    manager = RuntimeManager(Path(__file__).resolve().parents[1])
    result = manager.run(args.topic, payload=payload, evaluate=args.evaluate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
