#!/usr/bin/env python3
"""招聘评估报告 HTML 渲染 - 支持证据链与风险标识，供 generate_report 与 workflow_execution 共用"""
from datetime import datetime

DECISION_LABELS = {
    "strong_recommend": ("强烈推荐", "#22c55e"),
    "recommend": ("推荐", "#3b82f6"),
    "borderline": ("待定/可面试", "#eab308"),
    "not_recommend": ("不推荐", "#ef4444"),
}

# 风险标识英文 -> 中文（便于报告阅读）
RISK_LABELS = {
    "education_below_requirement": "学历低于岗位要求",
    "insufficient_experience": "工作经验不足",
    "insufficient_skills": "必备技能不足",
}


def render_html(
    candidate_id: str,
    scores: dict,
    *,
    decision: str = None,
    risk_flags: list = None,
    evidence: list = None,
    name: str = None,
    job_id: str = None,
) -> str:
    """生成带证据链与风险标识的 HTML 报告。"""
    rows = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in scores.items()
    )

    # 决策与风险区块
    decision_html = ""
    if decision:
        label, color = DECISION_LABELS.get(decision, (decision, "#6b7280"))
        decision_html = f"""
<h2>推荐结论</h2>
<p><strong style="color:{color};">{label}</strong></p>
"""

    risk_html = ""
    if risk_flags:
        labels = [RISK_LABELS.get(r, r) for r in risk_flags]
        risk_items = "".join(f"<li>{lb}</li>" for lb in labels)
        risk_html = f"""
<h2>风险标识</h2>
<ul>{risk_items}</ul>
"""

    evidence_html = ""
    if evidence:
        evidence_items = "".join(f"<li>{e}</li>" for e in evidence)
        evidence_html = f"""
<h2>证据链</h2>
<p>以下为各维度得分与推荐结论的依据，便于审计与反馈。</p>
<ol>{evidence_items}</ol>
"""

    meta = []
    if name:
        meta.append(f"姓名: {name}")
    if job_id:
        meta.append(f"岗位ID: {job_id}")
    meta.append(f"候选人ID: {candidate_id}")
    meta.append(f"生成时间: {datetime.now().isoformat()}")
    meta_str = " | ".join(meta)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>候选人 {candidate_id} 评估报告</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 1.5rem 2rem; max-width: 800px; }}
  table {{ border-collapse: collapse; margin: 0.5rem 0; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; }}
  th {{ background: #f5f5f5; }}
  h2 {{ margin-top: 1.2rem; color: #333; }}
  ul, ol {{ margin: 0.3rem 0; padding-left: 1.5rem; }}
</style>
</head>
<body>
<h1>AI 招聘评估报告</h1>
<p>{meta_str}</p>
<h2>匹配得分</h2>
<table>
<tr><th>维度</th><th>得分</th></tr>
{rows}
</table>
{decision_html}
{risk_html}
{evidence_html}
<p><em>本报告由 ASUI 架构生成，可审计追溯。</em></p>
</body>
</html>"""
