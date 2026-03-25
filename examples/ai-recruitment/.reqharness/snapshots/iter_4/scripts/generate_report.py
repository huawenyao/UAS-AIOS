#!/usr/bin/env python3
"""招聘推荐报告生成 - ASUI AI 招聘验证（含证据链与风险标识）"""
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_renderer import render_html

DB_DIR = Path(__file__).parent.parent / "database"
REPORTS_DIR = Path(__file__).parent.parent / "reports"


def main():
    data = json.load(sys.stdin)
    DB_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    candidate_id = data.get("candidate_id", "unknown")
    scores = data.get("scores", {})

    # 持久化到数据库（保留 evidence/risk_flags/decision 等完整字段）
    candidates_file = DB_DIR / "candidates.json"
    candidates = []
    if candidates_file.exists():
        candidates = json.loads(candidates_file.read_text(encoding="utf-8"))

    record = {
        "candidate_id": candidate_id,
        "scores": scores,
        "created_at": datetime.now().isoformat(),
    }
    for key in ("decision", "risk_flags", "evidence", "name", "job_id"):
        if key in data:
            record[key] = data[key]
    candidates.append(record)
    candidates_file.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 生成 HTML 报告（含证据链与风险时使用增强版）
    report_path = REPORTS_DIR / f"candidate_{candidate_id}.html"
    html = render_html(
        candidate_id,
        scores,
        decision=data.get("decision"),
        risk_flags=data.get("risk_flags"),
        evidence=data.get("evidence"),
        name=data.get("name"),
        job_id=data.get("job_id"),
    )
    report_path.write_text(html, encoding="utf-8")

    print(json.dumps({"report_path": str(report_path), "status": "created"}))


if __name__ == "__main__":
    main()
