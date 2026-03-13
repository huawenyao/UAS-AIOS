#!/usr/bin/env python3
"""在当前 UAS 元项目中创建标准 sub uas app。"""

import argparse
import sys
from pathlib import Path


def load_run_init():
    workspace_root = Path(__file__).resolve().parents[1]
    asui_src = workspace_root / "asui-cli" / "src"
    sys.path.insert(0, str(asui_src))
    from asui.init import run_init

    return workspace_root, run_init


def main() -> int:
    parser = argparse.ArgumentParser(description="在 projects/ 下创建标准 UAS 子应用")
    parser.add_argument("app_name", help="子应用名称，例如 ai-recruitment-os")
    parser.add_argument(
        "--target-root",
        default="projects",
        help="目标根目录，默认 projects",
    )
    parser.add_argument(
        "--template",
        default="uas-subapp",
        help="使用的模板，默认 uas-subapp",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="覆盖已存在文件",
    )
    args = parser.parse_args()

    workspace_root, run_init = load_run_init()
    target_root = (workspace_root / args.target_root).resolve()
    target_root.mkdir(parents=True, exist_ok=True)
    project_path = target_root / args.app_name

    success = run_init(project_path, template=args.template, force=args.force)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
