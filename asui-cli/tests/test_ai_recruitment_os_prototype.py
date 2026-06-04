"""Artifact checks for the AI Recruitment OS prototype and agent system."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = ROOT / "projects" / "ai-recruitment-os"


def test_recruitment_prototype_exposes_core_user_journeys():
    prototype = APP_ROOT / "prototype" / "index.html"

    assert prototype.exists()

    html = prototype.read_text(encoding="utf-8")
    required_sections = [
        "Hiring Mission",
        "Role Success Model",
        "Evidence Shortlist",
        "Interview Workspace",
        "Calibration Room",
        "Candidate Portal",
        "Learning Loop",
    ]

    for section in required_sections:
        assert section in html


def test_recruitment_agent_system_has_governed_capability_contracts():
    agent_system_path = APP_ROOT / "configs" / "agent_system_design.json"

    assert agent_system_path.exists()

    agent_system = json.loads(agent_system_path.read_text(encoding="utf-8"))
    assert agent_system["platform_model"] == "UAS-Platform"
    assert agent_system["decision_policy"] == "human_confirmed_high_impact_decisions"
    assert len(agent_system["agents"]) >= 8

    capability_ids = {
        capability["id"]
        for capability in agent_system["capability_services"]
    }
    assert {
        "cs.role.create_success_model",
        "cs.candidate.build_evidence_card",
        "cs.interview.capture_evidence",
        "cs.audit.run_fairness_review",
        "cs.feedback.update_recruitment_world_model",
    }.issubset(capability_ids)

    for agent in agent_system["agents"]:
        assert agent["calls_capabilities_only"] is True
        assert agent["audit_required"] is True


def test_recruitment_experience_design_documents_user_value_metrics():
    design_doc = APP_ROOT / "docs" / "PRODUCT_EXPERIENCE_DESIGN.md"

    assert design_doc.exists()

    content = design_doc.read_text(encoding="utf-8")
    for phrase in [
        "更快找到对的人",
        "更少招错人",
        "用证据招对人",
        "Candidate NPS",
        "Evidence coverage rate",
    ]:
        assert phrase in content
