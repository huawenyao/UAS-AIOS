#!/usr/bin/env python3
"""
推荐名单生成器
生成可视化的推荐候选人列表页面
"""
import json
from pathlib import Path
from datetime import datetime

# 路径配置
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DB_DIR = PROJECT_DIR / "database"
REPORTS_DIR = PROJECT_DIR / "reports"


def load_data():
    """加载所有数据"""
    data = {}

    # 候选人
    candidates_file = DB_DIR / "candidates.json"
    if candidates_file.exists():
        with open(candidates_file, 'r', encoding='utf-8') as f:
            data['candidates'] = json.load(f)
    else:
        data['candidates'] = []

    # 岗位
    jobs_file = DB_DIR / "jobs.json"
    if jobs_file.exists():
        with open(jobs_file, 'r', encoding='utf-8') as f:
            data['jobs'] = json.load(f)
    else:
        data['jobs'] = []

    return data


def render_recommendation_html(data: dict) -> str:
    """生成推荐名单 HTML"""
    candidates = data.get('candidates', [])
    jobs = data.get('jobs', [])

    # 构建岗位映射
    job_titles = {}
    for job in jobs:
        job_id = job.get('job_id')
        title = job.get('parsed_profile', {}).get('title', job_id)
        job_titles[job_id] = title

    # 按得分排序
    candidates.sort(key=lambda x: x.get('scores', {}).get('total_score', 0), reverse=True)

    # 分类
    decision_labels = {
        "strong_recommend": ("🔥 强烈推荐", "#34c759"),
        "recommend": ("✅ 推荐", "#0071e3"),
        "borderline": ("⏸️ 待定", "#bf4800"),
        "not_recommend": ("❌ 不推荐", "#e85d04"),
    }

    # 生成候选人卡片
    candidate_cards = []
    for c in candidates:
        name = c.get('name', '未知')
        decision = c.get('decision', '')
        label, color = decision_labels.get(decision, (decision, '#666'))
        score = c.get('scores', {}).get('total_score', 0)
        job_id = c.get('job_id', '')
        job_title = job_titles.get(job_id, job_id)

        # 基本信息
        basic = c.get('basic_info', {})
        exp = basic.get('experience_years', 0) if basic else 0
        has_mgmt = basic.get('management_experience', False) if basic else False
        team_size = basic.get('team_size', 0) if basic else 0
        skills = basic.get('skills', []) if basic else []

        # 证据链摘要
        evidence = c.get('evidence', [])
        evidence_summary = evidence[0] if evidence else ''

        # 风险标识
        risk_flags = c.get('risk_flags', [])

        card = f'''
        <div class="candidate-card">
            <div class="card-header">
                <div class="candidate-info">
                    <span class="candidate-name">{name}</span>
                    <span class="decision-badge" style="background: {color}">{label}</span>
                </div>
                <div class="score">{score}<span class="score-label">分</span></div>
            </div>
            <div class="card-body">
                <div class="meta-row">
                    <span class="meta-item">📋 {job_title}</span>
                    <span class="meta-item">💼 {exp}年经验</span>
                    {f'<span class="meta-item">👥 团队{team_size}人</span>' if has_mgmt else ''}
                </div>
                {f'<div class="skills">{", ".join(skills[:8])}</div>' if skills else ''}
                {f'<div class="evidence">💡 {evidence_summary}</div>' if evidence_summary else ''}
                {f'<div class="risks">⚠️ {", ".join(risk_flags)}</div>' if risk_flags else ''}
            </div>
            <div class="card-footer">
                <a href="candidate_{c.get('candidate_id', '')}.html" class="btn-detail">查看详情 →</a>
            </div>
        </div>
        '''
        candidate_cards.append(card)

    # 统计
    total = len(candidates)
    decisions = {}
    for c in candidates:
        d = c.get('decision', 'unknown')
        decisions[d] = decisions.get(d, 0) + 1

    stats_html = f'''
    <div class="stats">
        <div class="stat-item">
            <span class="stat-num">{total}</span>
            <span class="stat-label">简历总数</span>
        </div>
        <div class="stat-item">
            <span class="stat-num" style="color: #34c759">{decisions.get('strong_recommend', 0) + decisions.get('recommend', 0)}</span>
            <span class="stat-label">推荐</span>
        </div>
        <div class="stat-item">
            <span class="stat-num" style="color: #bf4800">{decisions.get('borderline', 0)}</span>
            <span class="stat-label">待定</span>
        </div>
        <div class="stat-item">
            <span class="stat-num" style="color: #e85d04">{decisions.get('not_recommend', 0)}</span>
            <span class="stat-label">不推荐</span>
        </div>
    </div>
    '''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>推荐名单 - AI 招聘系统</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
            margin: 0;
            padding: 0;
            background: #f5f5f7;
            color: #1d1d1f;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 32px;
            font-weight: 600;
            margin: 0 0 8px;
        }}
        .header p {{
            color: #86868b;
            margin: 0;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 40px;
            padding: 24px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-num {{
            display: block;
            font-size: 36px;
            font-weight: 600;
            color: #0071e3;
        }}
        .stat-label {{
            font-size: 14px;
            color: #86868b;
        }}
        .candidate-list {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        .candidate-card {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .candidate-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        .candidate-info {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .candidate-name {{
            font-size: 20px;
            font-weight: 600;
        }}
        .decision-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            color: white;
            font-size: 13px;
            font-weight: 500;
        }}
        .score {{
            font-size: 28px;
            font-weight: 600;
            color: #0071e3;
        }}
        .score-label {{
            font-size: 14px;
            color: #86868b;
            font-weight: 400;
        }}
        .card-body {{
            color: #6e6e73;
            font-size: 14px;
        }}
        .meta-row {{
            display: flex;
            gap: 16px;
            margin-bottom: 8px;
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .skills {{
            margin: 8px 0;
            color: #86868b;
            font-size: 13px;
        }}
        .evidence {{
            margin-top: 8px;
            padding: 8px 12px;
            background: #e8f5e9;
            border-radius: 8px;
            color: #2e7d32;
            font-size: 13px;
        }}
        .risks {{
            margin-top: 8px;
            padding: 8px 12px;
            background: #ffebee;
            border-radius: 8px;
            color: #c62828;
            font-size: 13px;
        }}
        .card-footer {{
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid #f0f0f0;
        }}
        .btn-detail {{
            color: #0071e3;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }}
        .btn-detail:hover {{
            text-decoration: underline;
        }}
        .empty-state {{
            text-align: center;
            color: #86868b;
            padding: 60px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #86868b;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>📋 推荐名单</h1>
            <p>AI 智能匹配结果，按综合得分排序</p>
        </header>

        {stats_html}

        <div class="candidate-list">
            {''.join(candidate_cards) if candidate_cards else '<div class="empty-state">暂无候选人数据</div>'}
        </div>

        <footer class="footer">
            <p>本页面由 ASUI 架构自动生成</p>
            <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>'''

    return html


def generate_recommendation_list():
    """生成推荐名单"""
    # 确保目录存在
    REPORTS_DIR.mkdir(exist_ok=True)

    # 加载数据
    data = load_data()

    # 生成 HTML
    html = render_recommendation_html(data)

    # 保存
    output_file = REPORTS_DIR / "recommendation_list.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 推荐名单已生成: {output_file}")
    return output_file


def main():
    """主入口"""
    import argparse
    parser = argparse.ArgumentParser(description="推荐名单生成器")
    parser.add_argument('--open', '-o', action='store_true', help='生成后自动打开')
    args = parser.parse_args()

    output_file = generate_recommendation_list()

    if args.open:
        import webbrowser
        webbrowser.open(str(output_file))


if __name__ == "__main__":
    main()