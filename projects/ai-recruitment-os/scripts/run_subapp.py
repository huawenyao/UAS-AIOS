#!/usr/bin/env python3
"""运行招聘智能OS sub uas app。"""

import argparse
import json
from pathlib import Path

from asui.runtime.runtime_manager import RuntimeManager


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
