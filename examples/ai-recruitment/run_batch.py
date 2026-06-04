#!/usr/bin/env python3
"""
AI 招聘 — 一键批次入口（P0）

用法（在 examples/ai-recruitment 目录下）:
  python run_batch.py
  python run_batch.py --resume-dir ./test_fixtures
  python run_batch.py --resume-dir ./test_fixtures --feedback
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"


def _import_script(name: str, module_file: str):
    import importlib.util

    path = SCRIPTS / module_file
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    parser = argparse.ArgumentParser(
        description="一键跑通：扫描简历 → 打分报告 → 价值摘要 → 推荐名单（可选拒信反馈）",
    )
    parser.add_argument(
        "--resume-dir",
        default=None,
        help="简历目录（默认 test_fixtures 或环境变量 RESUME_DIR）",
    )
    parser.add_argument(
        "--feedback",
        action="store_true",
        help="批次结束后为未通过同学生成脱敏拒信话术",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="不尝试打开推荐名单 HTML",
    )
    args = parser.parse_args()

    resume_dir = args.resume_dir or str(ROOT / "test_fixtures")
    resume_path = Path(resume_dir).resolve()
    if not resume_path.is_dir():
        print(f"错误: 简历目录不存在: {resume_path}")
        return 1

    print("\n" + "=" * 60)
    print("AI 招聘 · 一键批次")
    print("  扫描 → 匹配打分 → 报告 → 价值摘要 → 闭环事件")
    print("=" * 60)
    print(f"简历目录: {resume_path}\n")

    t0 = time.perf_counter()
    cmd = [sys.executable, str(ROOT / "workflow_execution.py"), "--resume-dir", str(resume_path)]
    proc = subprocess.run(cmd, cwd=str(ROOT))
    if proc.returncode != 0:
        return proc.returncode
    elapsed = time.perf_counter() - t0

    candidates_file = ROOT / "database" / "candidates.json"
    if not candidates_file.exists():
        print("警告: 未生成 candidates.json")
        return 1

    with open(candidates_file, encoding="utf-8") as f:
        results = json.load(f)

    value_summary = _import_script("value_summary", "value_summary.py")
    vs = value_summary.build_value_summary(results, elapsed_seconds=elapsed)
    print(value_summary.format_value_summary_console(vs))

    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    summary_path = reports_dir / f"value_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    summary_path.write_text(json.dumps(vs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n价值摘要 JSON: {summary_path}")

    closed_loop = _import_script("recruitment_closed_loop", "recruitment_closed_loop.py")
    loop_input = [
        {"candidate_id": r.get("candidate_id"), "total_score": r.get("scores", {}).get("total_score", 0)}
        for r in results
    ]
    loop_out = closed_loop.run_recruitment_closed_loop(loop_input)
    loop_path = reports_dir / "closed_loop_last.json"
    loop_path.write_text(json.dumps(loop_out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"闭环编排快照: {loop_path}")

    if args.feedback:
        feedback = _import_script("candidate_feedback", "candidate_feedback.py")
        feedback.generate_batch_feedback()

    rec_list = ROOT / "reports" / "recommendation_list.html"
    if rec_list.exists() and not args.no_open:
        print(f"\n打开推荐名单: {rec_list}")
        if sys.platform == "win32":
            subprocess.run(["cmd", "/c", "start", "", str(rec_list)], check=False)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(rec_list)], check=False)
        else:
            subprocess.run(["xdg-open", str(rec_list)], check=False)

    print("\n完成。HR 可直接打开 reports/recommendation_list.html 做面试名单决策。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
