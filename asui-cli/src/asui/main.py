#!/usr/bin/env python3
"""ASUI CLI 入口"""

import argparse
import sys
from pathlib import Path

from .init import run_init


def main():
    parser = argparse.ArgumentParser(
        prog="asui",
        description="ASUI 架构脚手架 - 快速初始化知识驱动型 AI 系统项目",
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # asui init
    init_parser = subparsers.add_parser("init", help="初始化 ASUI 项目")
    init_parser.add_argument(
        "project_name",
        nargs="?",
        default=".",
        help="项目名称或路径（默认当前目录）",
    )
    init_parser.add_argument(
        "-t",
        "--template",
        choices=["default", "customer-service", "recruitment", "selfpaw-swarm", "triadic-ideal-reality-swarm"],
        default="default",
        help="项目模板（default/customer-service/recruitment/selfpaw-swarm/triadic-ideal-reality-swarm）",
    )
    init_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="覆盖已存在的文件",
    )

    args = parser.parse_args()

    if args.command == "init":
        success = run_init(
            project_path=Path(args.project_name),
            template=args.template,
            force=args.force,
        )
        sys.exit(0 if success else 1)

    parser.print_help()
    sys.exit(0)
