"""Executable checks for the AI Recruitment OS agent runtime."""

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = ROOT / "projects" / "ai-recruitment-os"
RUNTIME_PATH = APP_ROOT / "scripts" / "agent_runtime.py"


def load_runtime_module():
    spec = importlib.util.spec_from_file_location("agent_runtime", RUNTIME_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_agent_runtime_executes_full_recruitment_journey():
    runtime = load_runtime_module()

    result = runtime.run_demo_journey(APP_ROOT)

    assert result["status"] == "completed"
    assert result["role_success_model"]["title"] == "Senior Backend Engineer"
    assert result["shortlist"][0]["candidate_id"] == "lin-chen"
    assert result["shortlist"][0]["recommendation"] == "strong"
    assert result["interview"]["score_suggestion"] >= 85
    assert result["decision"]["human_confirmation_required"] is True
    assert result["candidate_update"]["stage"] == "technical_interview"
    assert result["fairness_review"]["risk"] in {"low", "medium"}
    assert result["evolution_report"]["model_update_proposal"]
    assert len(result["audit_chain"]) >= 8


def test_agent_runtime_blocks_unknown_capability_calls():
    runtime = load_runtime_module()
    agent_system = runtime.load_agent_system(APP_ROOT)
    state = runtime.initial_demo_state()

    try:
        runtime.execute_capability(
            agent_system=agent_system,
            state=state,
            agent_id="mission_guard",
            capability_id="crm.raw.delete_candidate",
        )
    except runtime.CapabilityExecutionError as error:
        assert "not registered" in str(error)
    else:
        raise AssertionError("Unknown capabilities must be blocked")


def test_productized_prototype_uses_runtime_data_contract():
    data_path = APP_ROOT / "prototype" / "data" / "demo_state.json"
    html_path = APP_ROOT / "prototype" / "index.html"
    js_path = APP_ROOT / "prototype" / "app.js"

    assert data_path.exists()

    demo_state = json.loads(data_path.read_text(encoding="utf-8"))
    assert demo_state["campaign"]["title"] == "Senior Backend Engineer"
    assert len(demo_state["candidates"]) >= 3
    assert "agentRunLog" in demo_state

    html = html_path.read_text(encoding="utf-8")
    js = js_path.read_text(encoding="utf-8")

    assert 'id="run-agent-journey"' in html
    assert 'id="candidate-list"' in html
    assert 'id="agent-run-log"' in html
    assert "fetch('./data/demo_state.json')" in js
    assert "runAgentJourney" in js
    assert "renderCandidateList" in js
