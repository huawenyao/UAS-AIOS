#!/usr/bin/env python3
"""输出 ΠPaw Task Panel JSON（对接 Demo 待办/当前任务区）。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "asui-cli" / "src"))

from asui.pipaw_task_panel import PipawTaskPanel


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("show", help="渲染 Task Panel 视图")
    p.add_argument("--tenant-id", default="t-acme-demo")
    p.add_argument("--open-task", default=None, help="将指定 task_id 设为当前任务")
    args = parser.parse_args()

    panel = PipawTaskPanel(REPO_ROOT)
    if args.open_task:
        panel.open_task(args.open_task)
    view = panel.build_view(tenant_id=args.tenant_id)
    print(json.dumps(view, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
