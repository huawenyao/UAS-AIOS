#!/usr/bin/env python3
"""
候选人反馈生成器
从未通过候选人的评估结果中生成脱敏的反馈信息，供 HR 复制到拒信或系统中使用
"""
import json
from pathlib import Path
from datetime import datetime

# 路径配置
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DB_DIR = PROJECT_DIR / "database"
REPORTS_DIR = PROJECT_DIR / "reports"

# 风险标识中文映射
RISK_LABELS = {
    "education_below_requirement": "学历略低于岗位要求",
    "insufficient_experience": "工作经验相对岗位要求偏少",
    "insufficient_skills": "技能匹配度与岗位要求存在差距",
    "management_experience_missing": "缺少团队管理经验",
}

# 决策中文标签
DECISION_LABELS = {
    "strong_recommend": "强烈推荐",
    "recommend": "推荐",
    "borderline": "待定",
    "not_recommend": "不推荐",
}


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


def generate_rejection_feedback(candidate_data: dict, job_title: str = None) -> str:
    """
    为未通过候选人生成反馈内容

    Args:
        candidate_data: 候选人数据
        job_title: 岗位名称

    Returns:
        脱敏的反馈文本，可直接复制到拒信中
    """
    name = candidate_data.get('name', '候选人')
    scores = candidate_data.get('scores', {})
    risk_flags = candidate_data.get('risk_flags', [])
    evidence = candidate_data.get('evidence', [])

    # 岗位名称
    if not job_title:
        job_title = candidate_data.get('job_id', '该岗位')

    # 构建反馈内容
    feedback_parts = []

    # 开头
    feedback_parts.append(f"感谢您投递 {job_title} 岗位。")

    # 评估维度说明
    feedback_parts.append("")
    feedback_parts.append("经过我们的 AI 辅助评估，您在以下方面与岗位要求存在差距：")

    # 风险点
    if risk_flags:
        for risk in risk_flags:
            label = RISK_LABELS.get(risk, risk)
            feedback_parts.append(f"  • {label}")
    else:
        # 如果没有明确风险点，从证据中提取
        low_evidence = [e for e in evidence if '不足' in e or '缺少' in e or '未' in e]
        if low_evidence:
            for e in low_evidence[:3]:
                feedback_parts.append(f"  • {e}")
        else:
            feedback_parts.append("  • 综合评估结果未达到岗位要求")

    # 得分信息（可选，不对外显示具体分数，只说明维度）
    feedback_parts.append("")
    feedback_parts.append("评估维度包括：学历匹配、经验匹配、技能匹配、工程实践、领域经验、成长潜力。")

    # 综合得分
    total_score = scores.get('total_score', 0)
    feedback_parts.append(f"您的综合得分为 {total_score} 分。")

    # 结尾
    feedback_parts.append("")
    feedback_parts.append("我们已将您的简历纳入人才库，如有合适机会会再次与您联系。")
    feedback_parts.append("")
    feedback_parts.append("祝您求职顺利！")

    return "\n".join(feedback_parts)


def generate_batch_feedback():
    """批量生成未通过候选人的反馈"""
    candidates = load_candidates()
    jobs = load_jobs()

    if not candidates:
        print("⚠️ 暂无候选人数据！")
        return

    # 构建岗位ID到名称的映射
    job_titles = {}
    for job in jobs:
        job_id = job.get('job_id')
        title = job.get('parsed_profile', {}).get('title', job_id)
        job_titles[job_id] = title

    # 获取未通过的候选人
    not_passed = [c for c in candidates if c.get('decision') == 'not_recommend']

    if not not_passed:
        print("✅ 暂无未通过的候选人")
        return

    print(f"\n📋 共有 {len(not_passed)} 位未通过候选人：\n")

    feedback_results = []

    for c in not_passed:
        name = c.get('name', '未知')
        job_id = c.get('job_id', '')
        job_title = job_titles.get(job_id, job_id)
        candidate_id = c.get('candidate_id', '')

        feedback = generate_rejection_feedback(c, job_title)

        print(f"--- {name} ({job_title}) ---")
        print(feedback)
        print()

        feedback_results.append({
            "candidate_id": candidate_id,
            "name": name,
            "job_title": job_title,
            "feedback": feedback,
            "generated_at": datetime.now().isoformat()
        })

    # 保存反馈到文件
    feedback_dir = REPORTS_DIR / "feedback"
    feedback_dir.mkdir(exist_ok=True)

    feedback_file = feedback_dir / f"rejection_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(feedback_file, 'w', encoding='utf-8') as f:
        json.dump(feedback_results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 反馈已保存到: {feedback_file}")
    print("\n💡 提示：这些反馈仅供 HR 复制到拒信中使用，请根据实际情况调整后发送。")

    return feedback_results


def generate_single_feedback(candidate_id: str = None):
    """生成单个候选人的反馈"""
    candidates = load_candidates()
    jobs = load_jobs()

    if not candidates:
        print("⚠️ 暂无候选人数据！")
        return

    # 构建岗位ID到名称的映射
    job_titles = {}
    for job in jobs:
        job_id = job.get('job_id')
        title = job.get('parsed_profile', {}).get('title', job_id)
        job_titles[job_id] = title

    # 查找候选人
    target = None
    if candidate_id:
        for c in candidates:
            if c.get('candidate_id') == candidate_id:
                target = c
                break

    if not target:
        print("\n可选候选人:")
        for i, c in enumerate(candidates, 1):
            name = c.get('name', '未知')
            decision = DECISION_LABELS.get(c.get('decision', ''), c.get('decision', ''))
            print(f"  {i}. {name} - {decision}")

        print("\n请输入候选人编号:")
        choice = input("  > ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                target = candidates[idx]
        except ValueError:
            print("⚠️ 无效输入！")
            return

    if not target:
        print("⚠️ 未找到候选人！")
        return

    name = target.get('name', '候选人')
    job_id = target.get('job_id', '')
    job_title = job_titles.get(job_id, job_id)

    print(f"\n--- {name} ({job_title}) 的反馈 ---")
    feedback = generate_rejection_feedback(target, job_title)
    print(feedback)
    print("\n💡 提示：可复制以上内容到拒信中使用")

    return feedback


def main():
    """主入口"""
    import argparse

    parser = argparse.ArgumentParser(description="候选人反馈生成工具")
    parser.add_argument('--candidate-id', '-c', help='指定候选人ID')
    parser.add_argument('--batch', '-b', action='store_true', help='批量生成所有未通过候选人的反馈')

    args = parser.parse_args()

    if args.batch:
        generate_batch_feedback()
    elif args.candidate_id:
        generate_single_feedback(args.candidate_id)
    else:
        # 交互模式
        print("\n" + "="*50)
        print("📝 候选人反馈生成器")
        print("="*50)
        print("\n请选择操作:")
        print("  1. 生成单个候选人反馈")
        print("  2. 批量生成所有未通过候选人反馈")
        print("  0. 返回")

        choice = input("\n请输入选项 > ").strip()

        if choice == '1':
            generate_single_feedback()
        elif choice == '2':
            generate_batch_feedback()


if __name__ == "__main__":
    main()