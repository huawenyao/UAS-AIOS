import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from asui.init import run_init


def test_selfpaw_swarm_template_creates_native_assets(tmp_path):
    target = tmp_path / "selfpaw-swarm"

    assert run_init(target, template="selfpaw-swarm")

    expected_files = [
        "CLAUDE.md",
        "configs/workflow_config.json",
        "configs/swarm_agents.json",
        ".claude/skills/swarm_protocol.md",
        ".claude/skills/decision_output_contract.md",
        "scripts/render_decision.py",
        "reports/README.md",
    ]
    for relative_path in expected_files:
        assert (target / relative_path).exists(), relative_path

    workflow = json.loads((target / "configs" / "workflow_config.json").read_text(encoding="utf-8"))
    assert workflow["swarm"]["methodology"] == "negation-of-negation"
    assert workflow["steps"][-1]["script"] == "scripts/render_decision.py"

    agents = json.loads((target / "configs" / "swarm_agents.json").read_text(encoding="utf-8"))
    assert len(agents["agents"]) == 5
    assert agents["governance"]["allow_personal_override"] is False


def test_selfpaw_swarm_render_script_writes_report_and_decision(tmp_path):
    target = tmp_path / "selfpaw-swarm"
    assert run_init(target, template="selfpaw-swarm")

    payload = {
        "topic": "subscription-pricing-strategy",
        "second_negation": {
            "consensus": ["需要先验证中小商家的采用门槛"],
            "conflicts": ["首年定价力度与利润率之间存在冲突"],
        },
        "synthesis": {
            "final_decision": "先上线轻量订阅版，并以 90 天验证期控制投入。",
            "execution_path": [
                "筛选 20 家目标商户进行封闭试点",
                "按周追踪转化、留存和客服负载",
            ],
            "risk_preplan": ["当试点转化低于 15% 时暂停扩张"],
            "user_adaptation": ["首屏突出低门槛价值与迁移成本说明"],
            "cost_controls": ["试点阶段研发投入不超过既有季度预算的 20%"],
            "game_response": ["竞争对手降价时优先强化服务响应，不立即跟价"],
            "consensus": ["用户需要更低试错成本", "不能一次性重投入"],
            "open_conflicts": ["定价下探后是否影响高端客群定位"],
            "retrospective_triggers": ["连续两周试点留存下降", "竞争对手推出同类套餐"],
        },
    }

    result = subprocess.run(
        [sys.executable, str(target / "scripts" / "render_decision.py")],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        cwd=target,
        check=True,
    )

    output = json.loads(result.stdout)
    report_path = target / output["report_path"]
    decision_path = target / output["decision_path"]

    assert report_path.exists()
    assert decision_path.exists()
    assert "全维度辩证决策方案" in report_path.read_text(encoding="utf-8")

    stored = json.loads(decision_path.read_text(encoding="utf-8"))
    assert stored["topic"] == payload["topic"]
    assert stored["synthesis"]["final_decision"] == payload["synthesis"]["final_decision"]
