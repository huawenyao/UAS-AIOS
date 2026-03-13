#!/usr/bin/env python3
"""共享 UAS Runtime Service 入口。"""

import argparse
import json
import sys
from pathlib import Path


def load_service():
    workspace_root = Path(__file__).resolve().parents[1]
    asui_src = workspace_root / "asui-cli" / "src"
    sys.path.insert(0, str(asui_src))
    from asui.runtime import UASRuntimeService

    return workspace_root, UASRuntimeService


def main() -> int:
    parser = argparse.ArgumentParser(description="运行共享 UAS Runtime Service")
    parser.add_argument("command", choices=["list", "validate", "run"], help="执行动作")
    parser.add_argument("--app-id", help="sub uas app ID")
    parser.add_argument("--topic", help="运行时的业务议题")
    parser.add_argument("--payload-json", help="额外 JSON payload")
    parser.add_argument("--evaluate", action="store_true", help="运行后执行评估")
    parser.add_argument("--projects-root", default="projects", help="sub uas app 根目录")
    args = parser.parse_args()

    workspace_root, service_cls = load_service()
    service = service_cls(workspace_root, projects_root=args.projects_root)

    if args.command == "list":
        print(json.dumps(service.list_apps(), ensure_ascii=False, indent=2))
        return 0

    if not args.app_id:
        parser.error("--app-id is required for validate/run")

    if args.command == "validate":
        print(json.dumps(service.validate_app(args.app_id), ensure_ascii=False, indent=2))
        return 0

    if not args.topic:
        parser.error("--topic is required for run")

    payload = json.loads(args.payload_json) if args.payload_json else None
    result = service.run_app(args.app_id, args.topic, payload=payload, evaluate=args.evaluate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
