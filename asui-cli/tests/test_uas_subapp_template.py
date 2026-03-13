import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from asui.init import run_init


def test_uas_subapp_template_creates_platform_assets(tmp_path):
    target = tmp_path / "business-subapp"

    assert run_init(target, template="uas-subapp")

    expected_files = [
        "CLAUDE.md",
        "configs/platform_manifest.json",
        "configs/runtime_config.json",
        "configs/governance_policy.json",
        "configs/evolution_policy.json",
        "configs/system_registry.json",
        "configs/workflow_config.json",
        "configs/swarm_agents.json",
        ".claude/skills/platform_protocol.md",
        ".claude/skills/output_contract.md",
        "scripts/run_subapp.py",
        "scripts/render_uas_plan.py",
        "scripts/evaluate_evolution.py",
        "docs/APP_BLUEPRINT.md",
        "database/audit/README.md",
    ]
    for relative_path in expected_files:
        assert (target / relative_path).exists(), relative_path

    manifest = json.loads((target / "configs" / "platform_manifest.json").read_text(encoding="utf-8"))
    assert manifest["platform"]["technical_base"] == "ASUI"
    assert manifest["platform"]["runtime"] == "autonomous_agent"
    assert manifest["platform"]["formal_definition"] == ["I", "K", "R", "A", "S", "G", "E", "Π"]

    workflow = json.loads((target / "configs" / "workflow_config.json").read_text(encoding="utf-8"))
    step_ids = [step["id"] for step in workflow["steps"]]
    assert step_ids == [
        "intent_activation",
        "knowledge_binding",
        "agent_planning",
        "runtime_topology",
        "system_mapping",
        "governance_check",
        "evolution_plan",
        "render_report",
    ]


def test_uas_subapp_scripts_render_and_evaluate(tmp_path):
    target = tmp_path / "business-subapp"
    assert run_init(target, template="uas-subapp")

    payload = {
        "topic": "finance-ops-subapp",
        "intent_model": ["面向财务运营场景的子应用"],
        "knowledge_assets": ["workflow", "policies", "skills"],
        "runtime_topology": ["autonomous_agent runtime + task isolation"],
        "agent_fabric": ["orchestrator + finance specialist + governance agent"],
        "system_mesh": ["ERP", "BI", "knowledge base"],
        "governance_controls": ["audit", "approval", "rollback"],
        "evaluation_metrics": ["处理时延", "解释率"],
        "evolution_loop": ["偏差校验失败后回退到intent_activation"],
        "delivery_plan": ["先交付只读闭环，再扩展写入能力"],
    }

    render_result = subprocess.run(
        [sys.executable, str(target / "scripts" / "render_uas_plan.py")],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        cwd=target,
        check=True,
    )
    output = json.loads(render_result.stdout)
    assert (target / output["report_path"]).exists()
    assert (target / output["data_path"]).exists()

    evaluate_result = subprocess.run(
        [sys.executable, str(target / "scripts" / "evaluate_evolution.py")],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        cwd=target,
        check=True,
    )
    evaluation = json.loads(evaluate_result.stdout)
    assert evaluation["status"] == "pass"

    runtime_result = subprocess.run(
        [
            sys.executable,
            str(target / "scripts" / "run_subapp.py"),
            "finance-ops-subapp",
            "--payload-json",
            json.dumps(payload, ensure_ascii=False),
            "--evaluate",
        ],
        text=True,
        capture_output=True,
        cwd=target,
        check=True,
    )
    runtime_output = json.loads(runtime_result.stdout)
    assert runtime_output["status"] == "completed"
    assert runtime_output["evaluation"]["status"] == "pass"
    assert (target / runtime_output["audit_log"]).exists()


def test_create_sub_uas_app_script_creates_project(tmp_path):
    script_path = WORKSPACE_ROOT / "scripts" / "create_sub_uas_app.py"
    target_root = tmp_path / "projects"
    project_name = "generated-subapp"

    result = subprocess.run(
        [sys.executable, str(script_path), project_name, "--target-root", str(target_root)],
        text=True,
        capture_output=True,
        cwd=WORKSPACE_ROOT,
        check=True,
    )

    assert "ASUI 项目已初始化" in result.stdout
    generated = target_root / project_name
    assert (generated / "configs" / "platform_manifest.json").exists()
