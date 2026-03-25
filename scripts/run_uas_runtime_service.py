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
    parser.add_argument("command", choices=["list", "registry", "health", "validate", "run", "state", "enqueue", "process", "queue"], help="执行动作")
    parser.add_argument("--app-id", help="sub uas app ID")
    parser.add_argument("--topic", help="运行时的业务议题")
    parser.add_argument("--topic-slug", help="认知状态文件的 slug")
    parser.add_argument("--payload-json", help="额外 JSON payload")
    parser.add_argument("--evaluate", action="store_true", help="运行后执行评估")
    parser.add_argument(
        "--projects-root",
        "--subapp-root",
        dest="projects_root",
        default="projects",
        help="sub app 根目录（与 create_sub_uas_app --target-root 一致），默认 projects",
    )
    args = parser.parse_args()

    workspace_root, service_cls = load_service()
    service = service_cls(workspace_root, projects_root=args.projects_root)

    if args.command == "list":
        print(json.dumps(service.list_apps(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "registry":
        print(json.dumps(service.registry_snapshot(), ensure_ascii=False, indent=2))
        return 0

    if not args.app_id:
        if args.command not in {"process", "queue"}:
            parser.error("--app-id is required for health/validate/run/state/enqueue")

    if args.command == "queue":
        print(json.dumps(service.queue_status(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "process":
        print(json.dumps(service.process_next_job(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "health":
        print(json.dumps(service.health_check(args.app_id), ensure_ascii=False, indent=2))
        return 0

    if args.command == "validate":
        print(json.dumps(service.validate_app(args.app_id), ensure_ascii=False, indent=2))
        return 0

    if args.command == "state":
        if not args.topic_slug and not args.topic:
            parser.error("--topic-slug or --topic is required for state")
        print(
            json.dumps(
                service.get_cognitive_state(args.app_id, topic_slug=args.topic_slug, topic=args.topic),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if not args.topic:
        if args.command != "enqueue":
            parser.error("--topic is required for run/enqueue")

    if args.command == "enqueue":
        payload = json.loads(args.payload_json) if args.payload_json else None
        print(json.dumps(service.enqueue_job(args.app_id, args.topic, payload=payload, evaluate=args.evaluate), ensure_ascii=False, indent=2))
        return 0

    payload = json.loads(args.payload_json) if args.payload_json else None
    result = service.run_app(args.app_id, args.topic, payload=payload, evaluate=args.evaluate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
