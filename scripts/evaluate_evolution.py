#!/usr/bin/env python3
"""平台级演化评估入口：优先委托 subapp 内脚本，否则使用通用四维检查。"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def generic_evaluate(manifest: dict, payload: dict) -> dict:
    risks: list[str] = []
    suggestions: list[str] = []

    if manifest.get("platform", {}).get("technical_base") != "ASUI":
        risks.append("技术底座不是 ASUI")
        suggestions.append("统一 platform_manifest technical_base 为 ASUI")

    if manifest.get("platform", {}).get("runtime") != "autonomous_agent":
        risks.append("运行架构不是 autonomous_agent")
        suggestions.append("统一 runtime 为 autonomous_agent")

    if not payload.get("governance_controls"):
        risks.append("缺少治理控制设计")
        suggestions.append("补充 governance_controls")

    if not payload.get("evolution_loop"):
        risks.append("缺少演化回路")
        suggestions.append("补充 evolution_loop")

    status = "pass" if not risks else "needs_evolution"
    return {
        "status": status,
        "risks": risks,
        "suggestions": suggestions or ["当前方案满足平台标准"],
    }


def delegate_subapp(app_root: Path, payload: dict) -> dict | None:
    script = app_root / "scripts" / "evaluate_evolution.py"
    if not script.is_file():
        return None
    result = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        encoding="utf-8",
        capture_output=True,
        cwd=app_root,
        check=False,
    )
    if result.returncode != 0:
        return {
            "status": "error",
            "risks": [result.stderr or "subapp evaluate_evolution failed"],
            "suggestions": [],
        }
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="UAS 演化评估（平台入口）")
    parser.add_argument("--app-root", help="subapp 根目录")
    parser.add_argument("--app-id", default="ai-recruitment-os", help="projects/<id>")
    args = parser.parse_args()

    workspace = Path(__file__).resolve().parents[1]
    app_root = Path(args.app_root) if args.app_root else workspace / "projects" / args.app_id
    if not app_root.is_dir():
        print(json.dumps({"error": "app_root not found", "path": str(app_root)}, ensure_ascii=False))
        return 1

    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    delegated = delegate_subapp(app_root, payload)
    if delegated is not None:
        print(json.dumps(delegated, ensure_ascii=False, indent=2))
        return 0 if delegated.get("status") in ("pass", "needs_evolution") else 1

    manifest_path = app_root / "configs" / "platform_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    out = generic_evaluate(manifest, payload)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
