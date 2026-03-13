import json
import subprocess
import sys
from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from asui.init import run_init
from asui.runtime.runtime_manager import RuntimeManager
from asui.runtime.service import UASRuntimeService


def test_runtime_manager_executes_uas_subapp(tmp_path):
    target = tmp_path / "runtime-subapp"
    assert run_init(target, template="uas-subapp")

    payload = {
        "intent_model": ["面向运营团队的业务子应用"],
        "governance_controls": ["audit", "approval", "rollback"],
        "evolution_loop": ["intent_activation", "governance_check", "evolution_plan"],
    }

    manager = RuntimeManager(target)
    result = manager.run("ops-subapp", payload=payload, evaluate=True)

    assert result["status"] == "completed"
    assert result["evaluation"]["status"] == "pass"
    assert (target / result["audit_log"]).exists()
    report_path = target / result["state"]["report_path"]
    data_path = target / result["state"]["data_path"]
    assert report_path.exists()
    assert data_path.exists()


def test_ai_recruitment_os_conforms_and_runs(tmp_path):
    source_root = WORKSPACE_ROOT / "projects" / "ai-recruitment-os"
    app_root = tmp_path / "ai-recruitment-os"
    shutil.copytree(source_root, app_root)

    required_files = [
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
    ]
    for relative_path in required_files:
        assert (app_root / relative_path).exists(), relative_path

    workflow = json.loads((app_root / "configs" / "workflow_config.json").read_text(encoding="utf-8"))
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

    result = subprocess.run(
        [sys.executable, str(app_root / "scripts" / "run_subapp.py"), "AI全流程招聘智能OS", "--evaluate"],
        text=True,
        capture_output=True,
        cwd=app_root,
        check=True,
    )
    output = json.loads(result.stdout)
    assert output["status"] == "completed"
    assert output["evaluation"]["status"] == "pass"
    assert (app_root / output["audit_log"]).exists()


def test_uas_runtime_service_discovers_and_runs_multiple_subapps(tmp_path):
    projects_root = tmp_path / "projects"
    projects_root.mkdir()

    assert run_init(projects_root / "finance-subapp", template="uas-subapp")

    source_root = WORKSPACE_ROOT / "projects" / "ai-recruitment-os"
    shutil.copytree(source_root, projects_root / "ai-recruitment-os")

    service = UASRuntimeService(tmp_path, projects_root="projects")
    apps = service.list_apps()
    app_ids = {app["app_id"] for app in apps}

    assert "finance-subapp" in app_ids
    assert "ai-recruitment-os" in app_ids

    validation = service.validate_app("ai-recruitment-os")
    assert validation["status"] == "ok"

    result = service.run_app("finance-subapp", "shared-runtime-topic", payload={"governance_controls": ["audit"], "evolution_loop": ["intent_activation"]}, evaluate=True)
    assert result["status"] == "completed"
    assert result["evaluation"]["status"] == "pass"
