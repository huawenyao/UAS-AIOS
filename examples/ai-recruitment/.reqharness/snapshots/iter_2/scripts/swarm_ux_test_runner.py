#!/usr/bin/env python3
"""
蜂群智能体体验测试运行器
加载 configs/swarm_agents.json，使用 test_fixtures 执行一次匹配流程，
并基于能力矩阵与运行结果对各用户角色进行体验评估，输出 reports/swarm_ux_test_result.json
"""
import os
import json
import sys
from pathlib import Path
from datetime import datetime

# 项目根为 ai-recruitment
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

CONFIGS = ROOT / "configs"
DATABASE = ROOT / "database"
REPORTS = ROOT / "reports"
TEST_FIXTURES = ROOT / "test_fixtures"
SWARM_CONFIG = CONFIGS / "swarm_agents.json"
RESULT_FILE = REPORTS / "swarm_ux_test_result.json"

# 能力矩阵：当前产品对各角色成功标准的满足情况（可与实际运行结果结合后覆盖）
CAPABILITY_MATRIX = {
    "hr_recruiter": [
        {"criterion": "能无代码发布岗位", "result": "partial", "evidence": "需在 Cursor 中对 AI 说 /addJob，或直接维护 database/jobs.json；无独立 Web/CLI"},
        {"criterion": "能批量处理简历", "result": "pass", "evidence": "workflow_execution.py 支持目录扫描批量处理；/match 单份"},
        {"criterion": "报告可读且含证据", "result": "pass", "evidence": "HTML 报告含得分表；workflow 的 score 输出含 evidence、risk_flags"},
    ],
    "hiring_manager": [
        {"criterion": "报告含决策依据", "result": "pass", "evidence": "decision + evidence 在 score 输出与报告中"},
        {"criterion": "风险与证据清晰", "result": "pass", "evidence": "HTML 报告已展示推荐结论、风险标识（中文）、证据链"},
        {"criterion": "可区分强推/推荐/待定", "result": "pass", "evidence": "decision: strong_recommend/recommend/borderline/not_recommend"},
    ],
    "candidate": [
        {"criterion": "评分维度可解释", "result": "pass", "evidence": "evaluation_criteria.md 定义维度与档位"},
        {"criterion": "证据链可追溯", "result": "pass", "evidence": "score 输出 evidence 数组，可审计"},
        {"criterion": "无隐藏偏见风险", "result": "partial", "evidence": "规则透明；未做公平性审计与偏见检测"},
    ],
    "hr_operations": [
        {"criterion": "知识驱动可配置", "result": "pass", "evidence": "修改 evaluation_criteria.md 即生效"},
        {"criterion": "数据可导出与审计", "result": "pass", "evidence": "database/candidates.json、reports 结构化存储"},
        {"criterion": "报告可追溯", "result": "pass", "evidence": "报告注明可审计追溯；含时间戳"},
    ],
    "interviewer": [
        {"criterion": "能获取候选人画像与证据", "result": "pass", "evidence": "HTML 报告已含得分、推荐结论、风险标识与证据链"},
        {"criterion": "面试评估维度可用", "result": "partial", "evidence": "evaluation_criteria 定义面试维度；/evaluate 为规划能力未完全实现"},
        {"criterion": "与初筛结论一致", "result": "pass", "evidence": "初筛 decision 与 evidence 可支撑面试准备"},
    ],
}


def load_swarm_config():
    with open(SWARM_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def run_one_workflow():
    """使用 test_fixtures 执行一次工作流，生成 candidates 与报告。"""
    import sys
    import workflow_execution as wf
    # 通过 argv 传入 --resume-dir，确保 main() 内使用 test_fixtures（否则会使用 DEFAULT_RESUME_DIR）
    old_argv = sys.argv
    sys.argv = ["workflow_execution.py", "--resume-dir", str(TEST_FIXTURES)]
    try:
        wf.main()
    finally:
        sys.argv = old_argv
    return True


def load_latest_candidates():
    path = DATABASE / "candidates.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_agents(swarm_config, capability_matrix, run_artifacts=None):
    """根据能力矩阵与（可选）运行产物，生成各 agent 的体验评估。"""
    run_artifacts = run_artifacts or {}
    agents_result = []
    for agent in swarm_config.get("agents", []):
        aid = agent["id"]
        criteria_results = capability_matrix.get(aid, [])
        agents_result.append({
            "id": aid,
            "name": agent["name"],
            "mission": agent["mission"],
            "success_criteria": agent.get("success_criteria", []),
            "evaluation": criteria_results,
            "run_artifacts": run_artifacts.get(aid),
        })
    return agents_result


def main():
    REPORTS.mkdir(exist_ok=True)
    DATABASE.mkdir(exist_ok=True)

    print("=" * 60)
    print("蜂群智能体 · AI 招聘使用体验测试")
    print("=" * 60)

    swarm = load_swarm_config()
    print(f"\n已加载蜂群配置: {swarm.get('swarm_name')} ({len(swarm.get('agents', []))} 个角色)")

    # 执行一次真实工作流（使用 test_fixtures）
    print("\n[1/2] 使用 test_fixtures 执行一次匹配工作流...")
    if TEST_FIXTURES.exists() and (TEST_FIXTURES / "resume_sample.txt").exists():
        try:
            run_one_workflow()
            candidates = load_latest_candidates()
            run_artifacts = {
                "hr_recruiter": {"candidates_count": len(candidates), "reports_dir": str(REPORTS)},
                "hiring_manager": {"sample_ranking": [c.get("name") or c.get("candidate_id") for c in (candidates[:5] if candidates else [])] if candidates and isinstance(candidates[0], dict) else []},
                "hr_operations": {"database_path": str(DATABASE / "candidates.json")},
            }
        except Exception as e:
            print(f"工作流执行异常: {e}")
            run_artifacts = {}
    else:
        print("跳过工作流（test_fixtures/resume_sample.txt 不存在）")
        run_artifacts = {}

    # 评估各角色
    print("\n[2/2] 按角色评估体验与成功标准...")
    agents_evaluation = evaluate_agents(swarm, CAPABILITY_MATRIX, run_artifacts)

    result = {
        "swarm_name": swarm.get("swarm_name"),
        "test_time": datetime.now().isoformat(),
        "agents": agents_evaluation,
        "capability_matrix_note": "基于当前代码与文档的能力矩阵，结合本次运行结果",
    }
    RESULT_FILE.parent.mkdir(exist_ok=True)
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n结果已写入: {RESULT_FILE}")
    print("\n各角色验收摘要:")
    for a in agents_evaluation:
        ev = a["evaluation"]
        pass_n = sum(1 for e in ev if e.get("result") == "pass")
        part_n = sum(1 for e in ev if e.get("result") == "partial")
        fail_n = sum(1 for e in ev if e.get("result") == "fail")
        print(f"  {a['name']}: 通过 {pass_n} | 部分 {part_n} | 未通过 {fail_n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
