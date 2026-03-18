#!/usr/bin/env python3
"""
AI 招聘 - 交互式入口
降低使用门槛，无需记忆命令，HR 也可轻松使用
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 配置路径
SCRIPT_DIR = Path(__file__).resolve().parent
DB_DIR = SCRIPT_DIR / "database"
REPORTS_DIR = SCRIPT_DIR / "reports"


def print_header():
    """打印欢迎头"""
    print("\n" + "="*60)
    print("🤖 AI 招聘智能分析系统")
    print("   ASUI 架构 | 简历筛选 | 智能匹配 | 可解释决策")
    print("="*60)


def print_menu():
    """打印主菜单"""
    print("\n请选择操作:")
    print("  1. 📄 扫描简历并匹配岗位")
    print("  2. 📋 查看候选人名单")
    print("  3. 📊 查看推荐报告")
    print("  4. 👤 查看候选人详情")
    print("  5. 📈 生成招聘统计")
    print("  0. ❌ 退出")
    print("-"*40)


def load_candidates():
    """加载候选人数据"""
    candidates_file = DB_DIR / "candidates.json"
    if candidates_file.exists():
        with open(candidates_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def load_jobs():
    """加载岗位数据"""
    jobs_file = DB_DIR / "jobs.json"
    if jobs_file.exists():
        with open(jobs_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def run_resume_scan():
    """扫描简历并匹配"""
    print("\n" + "-"*40)
    print("📄 扫描简历并匹配岗位")
    print("-"*40)

    # 显示可选岗位
    jobs = load_jobs()
    if not jobs:
        print("⚠️ 暂无岗位，请先添加岗位！")
        return

    print("\n可选岗位:")
    for i, job in enumerate(jobs, 1):
        status = "🟢 进行中" if job.get('status') == 'open' else "🔴 已关闭"
        print(f"  {i}. {job.get('parsed_profile', {}).get('title', '未知')} [{status}]")

    # 选择简历目录
    print("\n请输入简历目录路径:")
    print("  (直接回车使用默认: ./test_fixtures)")
    resume_dir = input("  > ").strip()

    if not resume_dir:
        resume_dir = str(SCRIPT_DIR / "test_fixtures")
    else:
        resume_dir = os.path.abspath(resume_dir)

    if not os.path.exists(resume_dir):
        print(f"⚠️ 目录不存在: {resume_dir}")
        return

    print(f"\n📂 简历目录: {resume_dir}")
    print("正在执行匹配，请稍候...")

    # 调用主流程（复用 workflow_execution 的逻辑）
    from workflow_execution import main as run_workflow
    # 临时修改 RESUME_DIR
    os.environ['RESUME_DIR'] = resume_dir
    # 重新加载
    import importlib
    import workflow_execution
    importlib.reload(workflow_execution)
    # 执行
    sys.argv = ['workflow_execution.py', '--resume-dir', resume_dir]
    try:
        workflow_execution.main()
    except Exception as e:
        print(f"⚠️ 执行出错: {e}")


def view_candidates():
    """查看候选人名单"""
    print("\n" + "-"*40)
    print("📋 候选人名单")
    print("-"*40)

    candidates = load_candidates()
    if not candidates:
        print("⚠️ 暂无候选人数据，请先运行简历扫描！")
        return

    # 按得分排序
    candidates.sort(key=lambda x: x.get('scores', {}).get('total_score', 0), reverse=True)

    decision_labels = {
        "strong_recommend": "🔥强推",
        "recommend": "✅推荐",
        "borderline": "⏸️待定",
        "not_recommend": "❌不推荐"
    }

    print(f"\n共 {len(candidates)} 位候选人:\n")
    print(f"{'排名':<4} {'姓名':<12} {'决策':<8} {'总分':<6} {'经验':<6}")
    print("-"*50)

    for i, c in enumerate(candidates, 1):
        name = c.get('name', '未知')[:10]
        decision = decision_labels.get(c.get('decision', ''), c.get('decision', ''))
        score = c.get('scores', {}).get('total_score', 0)
        exp = c.get('basic_info', {}).get('experience_years', 0) if c.get('basic_info') else 0

        print(f"{i:<4} {name:<12} {decision:<8} {score:<6} {exp}年")

    print("-"*50)
    print("提示: 选择「查看候选人详情」输入编号可查看详细报告")


def view_reports():
    """查看推荐报告"""
    print("\n" + "-"*40)
    print("📊 推荐报告")
    print("-"*40)

    # 检查报告目录
    if not REPORTS_DIR.exists():
        print("⚠️ 报告目录不存在！")
        return

    html_files = list(REPORTS_DIR.glob("candidate_*.html"))
    if not html_files:
        print("⚠️ 暂无候选人报告，请先运行简历扫描！")
        return

    # 查找推荐名单
    rec_file = REPORTS_DIR / "recommendation_list.html"
    if rec_file.exists():
        print(f"\n📋 推荐名单: {rec_file}")

    print(f"\n📄 个人报告 (共 {len(html_files)} 份):")
    for f in sorted(html_files)[:10]:
        print(f"  • {f.name}")

    if len(html_files) > 10:
        print(f"  ... 还有 {len(html_files) - 10} 份")

    print("\n💡 提示: 使用浏览器打开 HTML 文件查看详细报告")


def view_candidate_detail():
    """查看候选人详情"""
    print("\n" + "-"*40)
    print("👤 候选人详情")
    print("-"*40)

    candidates = load_candidates()
    if not candidates:
        print("⚠️ 暂无候选人数据！")
        return

    # 按得分排序
    candidates.sort(key=lambda x: x.get('scores', {}).get('total_score', 0), reverse=True)

    print(f"\n可选候选人 (共 {len(candidates)} 位):")
    for i, c in enumerate(candidates, 1):
        name = c.get('name', '未知')
        score = c.get('scores', {}).get('total_score', 0)
        print(f"  {i}. {name} (得分: {score})")

    print("\n请输入候选人编号 (直接回车返回):")
    choice = input("  > ").strip()

    if not choice:
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(candidates):
            c = candidates[idx]
            print("\n" + "="*50)
            print(f"👤 候选人: {c.get('name', '未知')}")
            print("="*50)

            # 基本信息
            basic = c.get('basic_info', {})
            print(f"\n📌 基本信息:")
            print(f"   • 经验: {basic.get('experience_years', 0)} 年")
            print(f"   • 管理经验: {'是' if basic.get('management_experience') else '否'}")
            print(f"   • 团队规模: {basic.get('team_size', 0)} 人")

            # 技能
            skills = c.get('basic_info', {}).get('skills', [])
            if skills:
                print(f"\n💡 技能: {', '.join(skills[:10])}")

            # 得分
            scores = c.get('scores', {})
            print(f"\n📊 各维度得分:")
            score_labels = {
                "education_score": "学历匹配",
                "experience_score": "经验匹配",
                "skill_score": "技能匹配",
                "engineering_score": "工程实践",
                "domain_score": "领域经验",
                "potential_score": "成长潜力",
                "total_score": "综合得分"
            }
            for k, v in scores.items():
                if k != 'total_score':
                    label = score_labels.get(k, k)
                    print(f"   • {label}: {v}")
            print(f"   ─────────────")
            print(f"   • 综合得分: {scores.get('total_score', 0)}")

            # 决策
            decision_labels = {
                "strong_recommend": "🔥 强烈推荐",
                "recommend": "✅ 推荐",
                "borderline": "⏸️ 待定",
                "not_recommend": "❌ 不推荐"
            }
            decision = decision_labels.get(c.get('decision', ''), c.get('decision', ''))
            print(f"\n🎯 决策: {decision}")

            # 证据链
            evidence = c.get('evidence', [])
            if evidence:
                print(f"\n📋 推荐理由:")
                for e in evidence[:5]:
                    print(f"   • {e}")

            # 风险标识
            risk_flags = c.get('risk_flags', [])
            if risk_flags:
                risk_chinese = {
                    "education_below_requirement": "学历略低于要求",
                    "insufficient_experience": "工作经验不足",
                    "insufficient_skills": "技能匹配度偏低"
                }
                print(f"\n⚠️ 风险提示:")
                for r in risk_flags:
                    print(f"   • {risk_chinese.get(r, r)}")

            print("\n" + "="*50)

        else:
            print("⚠️ 编号无效！")

    except ValueError:
        print("⚠️ 请输入有效的数字编号！")


def view_statistics():
    """生成招聘统计"""
    print("\n" + "-"*40)
    print("📈 招聘统计")
    print("-"*40)

    candidates = load_candidates()
    jobs = load_jobs()

    if not candidates:
        print("⚠️ 暂无数据！")
        return

    # 统计
    total = len(candidates)
    decisions = {}
    for c in candidates:
        d = c.get('decision', 'unknown')
        decisions[d] = decisions.get(d, 0) + 1

    decision_labels = {
        "strong_recommend": "🔥 强推",
        "recommend": "✅ 推荐",
        "borderline": "⏸️ 待定",
        "not_recommend": "❌ 不推荐"
    }

    print(f"\n📊 候选人统计:")
    print(f"   • 总人数: {total} 人")

    for d, count in decisions.items():
        label = decision_labels.get(d, d)
        pct = count / total * 100
        print(f"   • {label}: {count} 人 ({pct:.1f}%)")

    # 平均分
    avg_score = sum(c.get('scores', {}).get('total_score', 0) for c in candidates) / total
    print(f"\n📈 平均得分: {avg_score:.1f} 分")

    # 效率估算
    saved_minutes = total * 25
    print(f"\n⏱️ 预估节省时间: {saved_minutes} 分钟")
    print(f"   (按每份简历人工阅读 25 分钟计)")

    # 岗位信息
    if jobs:
        print(f"\n📋 开放岗位: {len([j for j in jobs if j.get('status') == 'open'])} 个")

    print("\n" + "-"*40)


def main():
    """主入口"""
    print_header()

    while True:
        print_menu()
        choice = input("请输入选项 > ").strip()

        if choice == '0':
            print("\n👋 感谢使用，再见！\n")
            break
        elif choice == '1':
            run_resume_scan()
        elif choice == '2':
            view_candidates()
        elif choice == '3':
            view_reports()
        elif choice == '4':
            view_candidate_detail()
        elif choice == '5':
            view_statistics()
        else:
            print("\n⚠️ 请输入有效的选项编号！")


if __name__ == "__main__":
    main()