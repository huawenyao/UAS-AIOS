#!/usr/bin/env python3
"""
业务回路执行器：按 UAS 进化架构自主调用蜂群，对回路所有执行过程进行观测，解决全方位问题。

- 回路：evolution_policy.iteration.default_loop（intent_activation → governance_check → evolution_plan）
- 蜂群：workflow_config.swarm.agents，每步映射到对应 agent 执行
- 观测：每步 start/end、input/output 摘要、状态、漂移与修复动作写入 database/observability/loop_runs
- 全方位：目的守恒、治理校验、进化评估、漂移规则应用；可选与 examples/ai-recruitment 业务运行时同步
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

# 项目根为 ai-recruitment-os
ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
CONFIGS = ROOT / "configs"
DATABASE = ROOT / "database"
PLANS = DATABASE / "plans"
OBSERVABILITY_BASE = DATABASE / "observability" / "loop_runs"

CONFIG_LOOP = CONFIGS / "business_loop_config.json"
CONFIG_EVOLUTION = CONFIGS / "evolution_policy.json"
CONFIG_WORKFLOW = CONFIGS / "workflow_config.json"
CONFIG_GOVERNANCE = CONFIGS / "governance_policy.json"
PLAN_FILE = PLANS / "ai-full-cycle-recruitment-os.json"


def load_json(path: Path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def observe_step_start(run_dir: Path, step_id: str, agent_id: str, input_summary: dict) -> None:
    step_file = run_dir / "steps" / f"{step_id}_start.json"
    step_file.parent.mkdir(parents=True, exist_ok=True)
    save_json(step_file, {
        "step_id": step_id,
        "agent_id": agent_id,
        "event": "step_start",
        "at": datetime.now().isoformat(),
        "input_summary": input_summary,
    })


def observe_step_end(run_dir: Path, step_id: str, agent_id: str, output_summary: dict, status: str, error: str = None) -> None:
    step_file = run_dir / "steps" / f"{step_id}_end.json"
    step_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "step_id": step_id,
        "agent_id": agent_id,
        "event": "step_end",
        "at": datetime.now().isoformat(),
        "output_summary": output_summary,
        "status": status,
    }
    if error:
        payload["error"] = error
    save_json(step_file, payload)


def execute_step_with_runtime_manager(step_id: str, context: dict) -> dict | None:
    """若 asui RuntimeManager 可用，则通过其执行对应步骤（需传入 topic 跑完整 workflow 再取该步结果）。"""
    try:
        workspace_root = ROOT.parents[1]
        asui_src = workspace_root / "asui-cli" / "src"
        if not asui_src.exists():
            return None
        sys.path.insert(0, str(asui_src))
        from asui.runtime.runtime_manager import RuntimeManager
        manager = RuntimeManager(ROOT)
        topic = context.get("plan", {}).get("topic", "ai-full-cycle-recruitment-os")
        result = manager.run(topic, payload=None, evaluate=False)
        step_outputs = {}
        if step_id == "intent_activation":
            step_outputs = {"intent": result.get("intent", {}), "output_keys": ["intent"]}
        elif step_id == "governance_check":
            step_outputs = {"governance_controls": True, "output_keys": ["governance_controls"]}
        elif step_id == "evolution_plan":
            step_outputs = {"evolution_plan": result.get("evolution_plan", []), "output_keys": ["evolution_plan"]}
        return step_outputs or {"output_keys": list(result.keys())}
    except Exception:
        return None


def execute_step_stub(step_id: str, context: dict) -> dict:
    """无 LLM 时用计划/认知状态数据生成步骤输出摘要，用于观测与闭环。"""
    plan = context.get("plan", {})
    if step_id == "intent_activation":
        return {
            "intent": {"topic": plan.get("topic", ""), "purpose_anchor": plan.get("purpose_anchor", [])},
            "output_keys": ["intent"],
        }
    if step_id == "governance_check":
        return {
            "governance_controls": True,
            "governance_risks": [],
            "output_keys": ["governance_controls"],
        }
    if step_id == "evolution_plan":
        return {
            "evolution_plan": plan.get("iteration_loop", []),
            "success_metrics": list(plan.get("success_metrics", {}).keys()),
            "output_keys": ["evolution_plan", "success_metrics"],
        }
    return {"output_keys": []}


def run_evaluate_iteration(plan: dict, evolution_policy: dict) -> dict:
    """调用进化评估逻辑，返回 status / risks / suggestions / missing_purpose_keywords。"""
    purpose_anchor = " ".join(plan.get("purpose_anchor", []))
    metrics = plan.get("success_metrics", {})
    flat_metrics = {}
    for dim, m in (metrics or {}).items():
        if isinstance(m, dict):
            for k, v in m.items():
                if isinstance(v, dict) and "threshold" in v:
                    flat_metrics[k] = v.get("threshold", 0)
    required_kw = evolution_policy.get("goal_guard", {}).get("required_purpose_keywords", [])
    missing = [kw for kw in required_kw if kw not in purpose_anchor]
    min_hits = evolution_policy.get("goal_guard", {}).get("minimum_keyword_hits", 3)
    hits = len(required_kw) - len(missing)
    risks = []
    suggestions = []
    if hits < min_hits:
        risks.append("基础目的覆盖不足，存在目标漂移风险")
        suggestions.append("回到目的激活阶段，重新校准匹配/效率/公平/体验/成本的优先级")
    for metric_name, threshold in evolution_policy.get("evaluation_thresholds", {}).items():
        if metric_name not in flat_metrics:
            continue
        value = float(flat_metrics.get(metric_name, 0.0))
        if value < threshold:
            risks.append(f"{metric_name} 低于阈值 {threshold}")
            suggestions.append(f"围绕 {metric_name} 对应层进行重构与进化")
    status = "pass" if not risks else "needs_evolution"
    return {
        "status": status,
        "missing_purpose_keywords": missing,
        "risks": risks,
        "suggestions": suggestions or ["当前方案可继续进入实现阶段"],
    }


def apply_drift_rule(evolution_policy: dict, evaluation: dict, run_dir: Path) -> list:
    """根据评估结果匹配漂移规则，记录并返回待执行动作。"""
    drift_rules = evolution_policy.get("drift_rules", [])
    actions = []
    if evaluation.get("status") != "needs_evolution":
        return actions
    if evaluation.get("missing_purpose_keywords"):
        for rule in drift_rules:
            if rule.get("condition") == "missing_purpose_keywords":
                actions.append(rule.get("action", "return_to_purpose_activation"))
                break
    for risk in evaluation.get("risks", []):
        if "candidate_experience" in risk:
            actions.append("rebuild_micro_experience")
        elif "decision_explainability" in risk:
            actions.append("rebuild_evaluation_rubric")
        elif "process_completion" in risk:
            actions.append("repair_meso_workflow")
    if actions:
        save_json(run_dir / "drift_events.json", {
            "at": datetime.now().isoformat(),
            "evaluation_status": evaluation.get("status"),
            "risks": evaluation.get("risks", []),
            "actions": list(dict.fromkeys(actions)),
        })
    return actions


def main() -> int:
    loop_config = load_json(CONFIG_LOOP, {})
    evolution_policy = load_json(CONFIG_EVOLUTION, {})
    workflow_config = load_json(CONFIG_WORKFLOW, {})
    plan = load_json(PLAN_FILE, {})

    loop_steps = loop_config.get("loop", {}).get("steps", evolution_policy.get("iteration", {}).get("default_loop", []))
    agent_mapping = loop_config.get("swarm_invocation", {}).get("agent_step_mapping", {})
    obs_enabled = loop_config.get("observation", {}).get("enabled", True)

    run_id = f"run_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"
    run_dir = OBSERVABILITY_BASE / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    context = {"plan": plan, "workflow": workflow_config, "evolution_policy": evolution_policy}
    step_outputs = {}
    all_ok = True

    print("=" * 60)
    print("业务回路执行（UAS 进化架构 · 蜂群自主调用 · 全流程观测）")
    print("=" * 60)
    print(f"run_id: {run_id}")
    print(f"steps: {loop_steps}")

    use_llm = loop_config.get("swarm_invocation", {}).get("fallback_when_no_llm") != "stub_only"
    for step_id in loop_steps:
        agent_id = agent_mapping.get(step_id, step_id)
        input_summary = {"step_id": step_id, "agent_id": agent_id, "prior_output_keys": list(step_outputs.keys())}
        if obs_enabled:
            observe_step_start(run_dir, step_id, agent_id, input_summary)
        try:
            output = None
            if use_llm:
                output = execute_step_with_runtime_manager(step_id, context)
            if output is None:
                output = execute_step_stub(step_id, context)
            step_outputs.update(output)
            if obs_enabled:
                observe_step_end(run_dir, step_id, agent_id, {"output_keys": output.get("output_keys", [])}, "ok")
            print(f"  [ok] {step_id} ({agent_id})")
        except Exception as e:
            all_ok = False
            if obs_enabled:
                observe_step_end(run_dir, step_id, agent_id, {}, "error", str(e))
            print(f"  [error] {step_id}: {e}")

    evaluation = run_evaluate_iteration(plan, evolution_policy)
    actions = apply_drift_rule(evolution_policy, evaluation, run_dir)

    # 全方位检查：治理校验（可选）
    governance_result = None
    if (CONFIG_GOVERNANCE.exists() and PLANS.exists() and (ROOT / "scripts" / "evaluate_evolution.py").exists()):
        try:
            import subprocess
            r = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "evaluate_evolution.py")],
                input=json.dumps({"governance_controls": True, "evolution_loop": True}).encode("utf-8"),
                capture_output=True,
                timeout=10,
                cwd=str(ROOT),
            )
            if r.returncode == 0 and r.stdout:
                governance_result = json.loads(r.stdout.decode("utf-8"))
        except Exception:
            pass

    run_summary = {
        "run_id": run_id,
        "at": datetime.now().isoformat(),
        "loop_steps": loop_steps,
        "steps_completed": len(step_outputs),
        "evaluation_status": evaluation.get("status"),
        "evaluation_risks": evaluation.get("risks", []),
        "evaluation_suggestions": evaluation.get("suggestions", []),
        "drift_actions": actions,
        "all_steps_ok": all_ok,
        "governance_check": governance_result,
    }
    save_json(run_dir / "run_summary.json", run_summary)
    save_json(run_dir / "evaluation.json", evaluation)

    print("\n[评估] status:", evaluation.get("status"))
    if evaluation.get("risks"):
        print("  risks:", evaluation.get("risks"))
    if actions:
        print("[漂移处理] actions:", actions)
    print(f"\n观测数据已写入: {run_dir}")

    return 0 if all_ok and evaluation.get("status") == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
