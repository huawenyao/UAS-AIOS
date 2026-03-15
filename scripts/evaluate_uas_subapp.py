#!/usr/bin/env python3
"""UAS sub app 四维评价：业务、产品、技术、运行效果，驱动自主进化。"""

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def score_business(criteria: dict, payload: dict, app_root: Path) -> tuple[float, list[str]]:
    """业务维度：目标、价值闭环、主客体、成功标准"""
    items = criteria.get("items", [])
    total_max = sum(i["max_score"] for i in items) or 100
    score = 0.0
    suggestions = []

    intent = payload.get("intent_model") or payload.get("topic")
    if intent or payload.get("goal"):
        score += 25
    else:
        suggestions.append("补充业务目标、约束与成功标准")

    if payload.get("evolution_loop") or payload.get("evaluation_metrics"):
        score += 25
    else:
        suggestions.append("完善 evolution_loop、验证指标与迭代路径")

    if payload.get("target_audience") or payload.get("intent_model"):
        score += 25
    else:
        suggestions.append("明确目标对象与利益相关方")

    if payload.get("success_metrics") or payload.get("evaluation_metrics"):
        score += 25
    else:
        suggestions.append("定义可量化的成功指标")

    return min(100, score), suggestions


def score_product(criteria: dict, payload: dict, app_root: Path) -> tuple[float, list[str]]:
    """产品维度：Agent编织、交付物、评估指标、工作流"""
    score = 0.0
    suggestions = []

    agents = payload.get("agent_fabric") or []
    config_agents = load_json(app_root / "configs" / "swarm_agents.json")
    if agents or (config_agents and config_agents.get("agents")):
        score += 25
    else:
        suggestions.append("完善 swarm_agents 角色与交付物")

    if payload.get("delivery_plan") or payload.get("knowledge_assets"):
        score += 25
    else:
        suggestions.append("明确各步骤产出与报告格式")

    if payload.get("evaluation_metrics"):
        score += 25
    else:
        suggestions.append("补充 evaluation_metrics")

    workflow = load_json(app_root / "configs" / "workflow_config.json")
    steps = (workflow or {}).get("steps", [])
    step_ids = [s.get("id", "") for s in steps]
    if "intent_activation" in step_ids and "governance_check" in step_ids and ("evolution_plan" in step_ids or "render_report" in step_ids):
        score += 25
    else:
        suggestions.append("确保 workflow 含 intent→governance→evolution→render")

    return min(100, score), suggestions


def score_technology(criteria: dict, payload: dict, app_root: Path) -> tuple[float, list[str]]:
    """技术维度：ASUI、autonomous_agent、治理、知识资产"""
    score = 0.0
    suggestions = []

    manifest = load_json(app_root / "configs" / "platform_manifest.json")
    if manifest and manifest.get("platform", {}).get("technical_base") == "ASUI":
        score += 25
    else:
        suggestions.append("确保 technical_base 为 ASUI")

    if manifest and manifest.get("platform", {}).get("runtime") == "autonomous_agent":
        score += 25
    else:
        suggestions.append("确保 runtime 为 autonomous_agent")

    governance = load_json(app_root / "configs" / "governance_policy.json")
    if governance and governance.get("governance"):
        score += 25
    else:
        suggestions.append("补充 governance_policy、审计与权限")

    skills_dir = app_root / ".claude" / "skills"
    configs = list((app_root / "configs").glob("*.json")) if (app_root / "configs").exists() else []
    if (skills_dir.exists() and list(skills_dir.glob("*.md"))) or len(configs) >= 5:
        score += 25
    else:
        suggestions.append("完善 configs 与 .claude/skills")

    return min(100, score), suggestions


def score_operational(criteria: dict, payload: dict, app_root: Path) -> tuple[float, list[str]]:
    """运行效果：执行完成、审计、输出、演化就绪"""
    score = 0.0
    suggestions = []

    step_outputs = payload.get("step_outputs", {})
    if step_outputs or payload.get("render_report_result") or payload.get("status") == "written":
        score += 25
    else:
        suggestions.append("检查 workflow 步骤是否全部执行")

    audit_dir = app_root / "database" / "audit"
    if audit_dir.exists() and list(audit_dir.glob("*.jsonl")):
        score += 25
    else:
        suggestions.append("确保 database/audit 有记录")

    reports_dir = app_root / "reports"
    db_plans = app_root / "database" / "plans"
    if (reports_dir.exists() and list(reports_dir.glob("*.md"))) or (db_plans.exists() and list(db_plans.glob("*.json"))):
        score += 25
    else:
        suggestions.append("确保 reports 或 database 有产出")

    if payload.get("evaluation") or payload.get("evolution"):
        score += 25
    else:
        suggestions.append("确保 cognitive_state 含 evolution 建议")

    return min(100, score), suggestions


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="UAS sub app 四维评价")
    parser.add_argument("--app-root", help="sub app 根目录，默认 cwd")
    args, _ = parser.parse_known_args()
    app_root = Path(args.app_root).resolve() if args.app_root else Path.cwd()
    payload = json.load(sys.stdin)

    criteria_path = app_root / "configs" / "evaluation_criteria.json"
    if not criteria_path.exists():
        criteria_path = Path(__file__).resolve().parents[1] / "configs" / "evaluation_criteria.example.json"
    criteria = load_json(criteria_path) or {}

    dimensions_cfg = criteria.get("dimensions", {})
    weights = criteria.get("dimension_weights") or {
        "business": 0.25, "product": 0.25, "technology": 0.25, "operational": 0.25
    }
    threshold = criteria.get("evolution_threshold", 70)

    scorers = {
        "business": score_business,
        "product": score_product,
        "technology": score_technology,
        "operational": score_operational,
    }

    scores = {}
    all_suggestions = []
    weighted_sum = 0.0
    weight_total = 0.0

    for dim_id, scorer in scorers.items():
        dim_cfg = dimensions_cfg.get(dim_id, {})
        dim_score, dim_suggestions = scorer(dim_cfg, payload, app_root)
        scores[dim_id] = {
            "score": round(dim_score, 1),
            "name": dim_cfg.get("name", dim_id),
            "suggestions": dim_suggestions,
        }
        all_suggestions.extend(dim_suggestions)
        w = weights.get(dim_id, 0.25)
        weighted_sum += dim_score * w
        weight_total += w

    total_score = round(weighted_sum / weight_total if weight_total else 0, 1)
    status = "pass" if total_score >= threshold else "needs_evolution"
    risks = [f"{k}维度得分{scores[k]['score']}低于预期" for k, v in scores.items() if v["score"] < 60]

    output = {
        "status": status,
        "total_score": total_score,
        "evolution_threshold": threshold,
        "dimension_scores": scores,
        "risks": risks,
        "suggestions": list(dict.fromkeys(all_suggestions)) or ["当前满足评价标准"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
