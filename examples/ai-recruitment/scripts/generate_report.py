#!/usr/bin/env python3
"""招聘推荐报告生成 - ASUI AI 招聘验证"""
import json
import sys
from pathlib import Path
from datetime import datetime

DB_DIR = Path(__file__).parent.parent / "database"
REPORTS_DIR = Path(__file__).parent.parent / "reports"


def main():
    data = json.load(sys.stdin)
    DB_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    candidate_id = data.get("candidate_id", "unknown")
    scores = data.get("scores", {})

    # 持久化到数据库
    candidates_file = DB_DIR / "candidates.json"
    candidates = []
    if candidates_file.exists():
        candidates = json.loads(candidates_file.read_text(encoding="utf-8"))

    record = {
        "candidate_id": candidate_id,
        "scores": scores,
        "created_at": datetime.now().isoformat(),
    }
    candidates.append(record)
    candidates_file.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 生成 HTML 报告
    report_path = REPORTS_DIR / f"candidate_{candidate_id}.html"
    html = _render_report(candidate_id, scores)
    report_path.write_text(html, encoding="utf-8")

    print(json.dumps({"report_path": str(report_path), "status": "created"}))


def _render_report(candidate_id: str, scores: dict) -> str:
    rows = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in scores.items()
    )
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>候选人 {candidate_id} 评估报告</title></head>
<body>
<h1>AI 招聘评估报告</h1>
<p>候选人ID: {candidate_id}</p>
<p>生成时间: {datetime.now().isoformat()}</p>
<h2>匹配得分</h2>
<table border="1">
<tr><th>维度</th><th>得分</th></tr>
{rows}
</table>
<p><em>本报告由 ASUI 架构生成，可审计追溯。</em></p>
</body>
</html>"""


if __name__ == "__main__":
    main()
