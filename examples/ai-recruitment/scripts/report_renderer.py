#!/usr/bin/env python3
"""招聘评估报告 HTML 渲染 - Apple 官网风格模板，支持证据链与风险标识"""
from datetime import datetime

DECISION_LABELS = {
    "strong_recommend": ("强烈推荐", "#34c759"),
    "recommend": ("推荐", "#0071e3"),
    "borderline": ("待定 / 可面试", "#bf4800"),
    "not_recommend": ("不推荐", "#e85d04"),
}

RISK_LABELS = {
    "education_below_requirement": "学历低于岗位要求",
    "insufficient_experience": "工作经验不足",
    "insufficient_skills": "必备技能不足",
}

# 得分维度英文 -> 中文展示名
SCORE_LABELS = {
    "education_score": "学历匹配",
    "experience_score": "经验匹配",
    "skill_score": "技能匹配",
    "engineering_score": "工程实践",
    "domain_score": "领域经验",
    "potential_score": "成长潜力",
    "total_score": "综合得分",
}


def _score_rows(scores: dict) -> str:
    total = scores.get("total_score")
    rows = []
    for k, v in scores.items():
        if k == "total_score":
            continue
        label = SCORE_LABELS.get(k, k)
        rows.append(f'<div class="score-row"><span class="score-label">{label}</span><span class="score-value">{v}</span></div>')
    if total is not None:
        rows.append(f'<div class="score-row score-row-total"><span class="score-label">综合得分</span><span class="score-value">{total}</span></div>')
    return "\n".join(rows)


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
    """生成 Apple 官网风格的 HTML 报告。"""
    score_rows_html = _score_rows(scores)

    decision_html = ""
    if decision:
        label, color = DECISION_LABELS.get(decision, (decision, "#6e6e73"))
        decision_html = f'''
<section class="block">
  <h2 class="section-title">推荐结论</h2>
  <div class="decision-badge" style="--badge-color:{color}">{label}</div>
</section>'''

    risk_html = ""
    if risk_flags:
        labels = [RISK_LABELS.get(r, r) for r in risk_flags]
        risk_items = "".join(f'<li>{lb}</li>' for lb in labels)
        risk_html = f'''
<section class="block">
  <h2 class="section-title">风险标识</h2>
  <ul class="list">{risk_items}</ul>
</section>'''

    evidence_html = ""
    if evidence:
        evidence_items = "".join(f'<li>{e}</li>' for e in evidence)
        evidence_html = f'''
<section class="block">
  <h2 class="section-title">证据链</h2>
  <p class="section-desc">各维度得分与推荐结论的依据，便于审计与反馈。</p>
  <ol class="list list-ordered">{evidence_items}</ol>
</section>'''

    meta_name = f'<span class="meta-name">{name}</span>' if name else ""
    meta_parts = []
    if job_id:
        meta_parts.append(job_id)
    meta_parts.append(candidate_id)
    meta_parts.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
    meta_sub = " · ".join(meta_parts)
    meta_line = (meta_name + " · " if meta_name else "") + meta_sub

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>评估报告 · {name or candidate_id}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Helvetica Neue", sans-serif;
      margin: 0;
      padding: 0;
      background: #fbfbfd;
      color: #1d1d1f;
      font-size: 17px;
      line-height: 1.47059;
      font-weight: 400;
      letter-spacing: -0.022em;
    }}
    .page {{
      max-width: 980px;
      margin: 0 auto;
      padding: 48px 28px 80px;
    }}
    .hero {{
      text-align: center;
      padding: 56px 0 48px;
      border-bottom: 1px solid rgba(0,0,0,.08);
    }}
    .hero h1 {{
      font-size: 40px;
      font-weight: 600;
      letter-spacing: -0.025em;
      margin: 0 0 8px;
      color: #1d1d1f;
    }}
    .hero .meta {{
      font-size: 15px;
      color: #6e6e73;
    }}
    .hero .meta-name {{
      color: #1d1d1f;
      font-weight: 500;
    }}
    .block {{
      background: #fff;
      border-radius: 18px;
      padding: 32px 36px;
      margin-top: 24px;
      box-shadow: 0 2px 12px rgba(0,0,0,.06);
    }}
    .block:first-of-type {{
      margin-top: 32px;
    }}
    .section-title {{
      font-size: 22px;
      font-weight: 600;
      letter-spacing: -0.02em;
      margin: 0 0 20px;
      color: #1d1d1f;
    }}
    .section-desc {{
      font-size: 15px;
      color: #6e6e73;
      margin: 0 0 16px;
      line-height: 1.5;
    }}
    .score-card {{
      display: grid;
      gap: 0;
      background: #fff;
      border-radius: 18px;
      padding: 28px 36px;
      margin-top: 32px;
      box-shadow: 0 2px 12px rgba(0,0,0,.06);
    }}
    .score-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 0;
      border-bottom: 1px solid rgba(0,0,0,.06);
      font-size: 16px;
    }}
    .score-row:last-child {{
      border-bottom: none;
    }}
    .score-row-total {{
      padding-top: 20px;
      margin-top: 8px;
      border-top: 2px solid rgba(0,0,0,.1);
      font-size: 18px;
      font-weight: 600;
    }}
    .score-label {{
      color: #6e6e73;
    }}
    .score-value {{
      font-variant-numeric: tabular-nums;
      font-weight: 500;
      color: #1d1d1f;
    }}
    .decision-badge {{
      display: inline-block;
      padding: 10px 24px;
      border-radius: 980px;
      font-size: 17px;
      font-weight: 600;
      background: var(--badge-color);
      color: #fff;
    }}
    .list {{
      margin: 0;
      padding-left: 22px;
      color: #1d1d1f;
      line-height: 1.6;
    }}
    .list li {{
      margin-bottom: 8px;
    }}
    .list-ordered {{ list-style: decimal; }}
    .footer {{
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid rgba(0,0,0,.08);
      font-size: 13px;
      color: #86868b;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="page">
    <header class="hero">
      <h1>评估报告</h1>
      <p class="meta">{meta_line}</p>
    </header>

    <section class="score-card">
      <h2 class="section-title">匹配得分</h2>
      {score_rows_html}
    </section>
    {decision_html}
    {risk_html}
    {evidence_html}

    <footer class="footer">
      本报告由 ASUI 架构生成，可审计追溯。
    </footer>
  </div>
</body>
</html>"""
