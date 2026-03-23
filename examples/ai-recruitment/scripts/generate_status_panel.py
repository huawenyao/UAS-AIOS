#!/usr/bin/env python3
"""
招聘流程状态面板生成器
生成可视化的招聘流程状态页面，展示当前招聘进度
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

    # 任务
    tasks_file = DB_DIR / "tasks.json"
    if tasks_file.exists():
        with open(tasks_file, 'r', encoding='utf-8') as f:
            data['tasks'] = json.load(f)
    else:
        data['tasks'] = []

    # 事件
    events_file = DB_DIR / "events.json"
    if events_file.exists():
        with open(events_file, 'r', encoding='utf-8') as f:
            data['events'] = json.load(f)
    else:
        data['events'] = []

    # 评估
    evaluations_file = DB_DIR / "evaluations.json"
    if evaluations_file.exists():
        with open(evaluations_file, 'r', encoding='utf-8') as f:
            data['evaluations'] = json.load(f)
    else:
        data['evaluations'] = []

    return data


def get_stage_status(data: dict) -> dict:
    """获取各阶段状态"""
    candidates = data.get('candidates', [])
    jobs = data.get('jobs', [])
    tasks = data.get('tasks', [])
    events = data.get('events', [])
    evaluations = data.get('evaluations', [])

    # 阶段定义
    stages = {
        "screening": {
            "name": "📋 初筛完成",
            "description": "简历筛选与匹配",
            "completed": False,
            "count": 0,
            "icon": "✅"
        },
        "interview": {
            "name": "🎤 面试安排",
            "description": "面试通知与安排",
            "completed": False,
            "count": 0,
            "icon": "⏳"
        },
        "evaluation": {
            "name": "📝 面试评估",
            "description": "面试表现评估",
            "completed": False,
            "count": 0,
            "icon": "⏳"
        },
        "offer": {
            "name": "📄 offer 发放",
            "description": "录用通知",
            "completed": False,
            "count": 0,
            "icon": "⏳"
        },
        "onboarding": {
            "name": "🚀 入职",
            "description": "新员工入职",
            "completed": False,
            "count": 0,
            "icon": "⏳"
        }
    }

    # 初筛阶段
    if candidates:
        stages["screening"]["completed"] = True
        stages["screening"]["count"] = len(candidates)

        # 统计各决策
        decisions = {}
        for c in candidates:
            d = c.get('decision', 'unknown')
            decisions[d] = decisions.get(d, 0) + 1

        recommend_count = decisions.get('strong_recommend', 0) + decisions.get('recommend', 0)
        stages["screening"]["description"] = f"已处理 {len(candidates)} 份简历，推荐 {recommend_count} 人"

    # 检查是否有面试安排
    interview_tasks = [t for t in tasks if t.get('task_type') == 'interview' or 'interview' in str(t.get('task_type', '')).lower()]
    if interview_tasks:
        stages["interview"]["completed"] = True
        stages["interview"]["count"] = len(interview_tasks)

    # 检查是否有面试评估
    if evaluations:
        stages["evaluation"]["completed"] = True
        stages["evaluation"]["count"] = len(evaluations)

    return stages


def get_job_status(data: dict) -> list:
    """获取各岗位状态"""
    jobs = data.get('jobs', [])
    candidates = data.get('candidates', [])

    job_status = []
    for job in jobs:
        job_id = job.get('job_id')
        title = job.get('parsed_profile', {}).get('title', job_id)
        status = job.get('status', 'open')

        # 统计该岗位的候选人
        job_candidates = [c for c in candidates if c.get('job_id') == job_id]

        decisions = {}
        for c in job_candidates:
            d = c.get('decision', 'unknown')
            decisions[d] = decisions.get(d, 0) + 1

        job_status.append({
            "job_id": job_id,
            "title": title,
            "status": status,
            "total_candidates": len(job_candidates),
            "recommend": decisions.get('strong_recommend', 0) + decisions.get('recommend', 0),
            "borderline": decisions.get('borderline', 0),
            "not_recommend": decisions.get('not_recommend', 0)
        })

    return job_status


def render_status_html(data: dict) -> str:
    """生成状态面板 HTML"""
    stages = get_stage_status(data)
    job_status = get_job_status(data)
    candidates = data.get('candidates', [])

    # 计算总体进度
    completed_stages = sum(1 for s in stages.values() if s['completed'])
    total_stages = len(stages)
    progress_pct = int(completed_stages / total_stages * 100)

    # 候选人统计
    total_candidates = len(candidates)
    decisions = {}
    for c in candidates:
        d = c.get('decision', 'unknown')
        decisions[d] = decisions.get(d, 0) + 1

    # 阶段 HTML
    stages_html = []
    for stage_id, stage in stages.items():
        icon = stage['icon']
        name = stage['name']
        desc = stage['description']
        is_completed = stage['completed']

        cls = "stage-completed" if is_completed else "stage-pending"
        stages_html.append(f'''
        <div class="stage {cls}">
            <div class="stage-icon">{icon}</div>
            <div class="stage-info">
                <div class="stage-name">{name}</div>
                <div class="stage-desc">{desc}</div>
            </div>
        </div>
        ''')

    # 岗位状态 HTML
    job_html = []
    for job in job_status:
        status_badge = '<span class="badge-open">进行中</span>' if job['status'] == 'open' else '<span class="badge-closed">已关闭</span>'
        job_html.append(f'''
        <div class="job-card">
            <div class="job-header">
                <span class="job-title">{job['title']}</span>
                {status_badge}
            </div>
            <div class="job-stats">
                <div class="stat"><span class="stat-num">{job['total_candidates']}</span><span class="stat-label">简历</span></div>
                <div class="stat"><span class="stat-num">{job['recommend']}</span><span class="stat-label">推荐</span></div>
                <div class="stat"><span class="stat-num">{job['borderline']}</span><span class="stat-label">待定</span></div>
            </div>
        </div>
        ''')

    # 推荐候选人列表
    recommend_candidates = [c for c in candidates if c.get('decision') in ['strong_recommend', 'recommend']]
    recommend_html = []
    for c in recommend_candidates[:5]:
        name = c.get('name', '未知')
        score = c.get('scores', {}).get('total_score', 0)
        decision_label = {
            'strong_recommend': '🔥强推',
            'recommend': '✅推荐'
        }.get(c.get('decision'), '')
        recommend_html.append(f'''
        <div class="candidate-row">
            <span class="candidate-name">{name}</span>
            <span class="candidate-score">{score}分</span>
            <span class="candidate-decision">{decision_label}</span>
        </div>
        ''')

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>招聘流程状态 - AI 招聘系统</title>
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
            max-width: 900px;
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
        .card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }}
        .card-title {{
            font-size: 18px;
            font-weight: 600;
            margin: 0 0 20px;
        }}
        .progress-bar {{
            height: 8px;
            background: #e5e5e5;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 12px;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #34c759, #30d158);
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        .progress-text {{
            text-align: center;
            color: #86868b;
            font-size: 14px;
        }}
        .stages {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .stage {{
            display: flex;
            align-items: center;
            padding: 16px;
            border-radius: 12px;
            background: #f5f5f7;
        }}
        .stage-completed {{
            background: #e8f5e9;
        }}
        .stage-icon {{
            font-size: 24px;
            margin-right: 16px;
        }}
        .stage-name {{
            font-weight: 600;
            font-size: 16px;
        }}
        .stage-desc {{
            color: #86868b;
            font-size: 14px;
            margin-top: 2px;
        }}
        .job-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
        }}
        .job-card {{
            background: #f5f5f7;
            border-radius: 12px;
            padding: 16px;
        }}
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        .job-title {{
            font-weight: 600;
        }}
        .badge-open {{
            background: #34c759;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
        }}
        .badge-closed {{
            background: #86868b;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
        }}
        .job-stats {{
            display: flex;
            gap: 16px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-num {{
            display: block;
            font-size: 20px;
            font-weight: 600;
            color: #0071e3;
        }}
        .stat-label {{
            font-size: 12px;
            color: #86868b;
        }}
        .candidate-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .candidate-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background: #f5f5f7;
            border-radius: 8px;
        }}
        .candidate-name {{
            font-weight: 500;
        }}
        .candidate-score {{
            color: #0071e3;
            font-weight: 600;
        }}
        .candidate-decision {{
            font-size: 14px;
        }}
        .empty-state {{
            text-align: center;
            color: #86868b;
            padding: 40px;
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
            <h1>📊 招聘流程状态</h1>
            <p>实时跟踪招聘进度与候选人状态</p>
        </header>

        <!-- 进度概览 -->
        <div class="card">
            <h2 class="card-title">总体进度</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_pct}%"></div>
            </div>
            <div class="progress-text">已完成 {completed_stages}/{total_stages} 个阶段 ({progress_pct}%)</div>
        </div>

        <!-- 招聘阶段 -->
        <div class="card">
            <h2 class="card-title">招聘流程</h2>
            <div class="stages">
                {''.join(stages_html)}
            </div>
        </div>

        <!-- 岗位状态 -->
        <div class="card">
            <h2 class="card-title">岗位招聘情况</h2>
            {f'<div class="job-list">{''.join(job_html)}</div>' if job_html else '<div class="empty-state">暂无岗位数据</div>'}
        </div>

        <!-- 推荐候选人 -->
        <div class="card">
            <h2 class="card-title">推荐候选人</h2>
            {f'<div class="candidate-list">{''.join(recommend_html)}</div>' if recommend_html else '<div class="empty-state">暂无推荐候选人</div>'}
        </div>

        <footer class="footer">
            <p>本页面由 ASUI 架构自动生成</p>
            <p>更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>'''

    return html


def generate_status_panel():
    """生成状态面板"""
    # 确保目录存在
    REPORTS_DIR.mkdir(exist_ok=True)

    # 加载数据
    data = load_data()

    # 生成 HTML
    html = render_status_html(data)

    # 保存
    output_file = REPORTS_DIR / "status.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 状态面板已生成: {output_file}")
    return output_file


def main():
    """主入口"""
    import argparse
    parser = argparse.ArgumentParser(description="招聘流程状态面板生成器")
    parser.add_argument('--open', '-o', action='store_true', help='生成后自动打开')
    args = parser.parse_args()

    output_file = generate_status_panel()

    if args.open:
        import webbrowser
        webbrowser.open(str(output_file))


if __name__ == "__main__":
    main()