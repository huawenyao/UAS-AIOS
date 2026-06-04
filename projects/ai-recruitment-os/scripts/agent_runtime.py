#!/usr/bin/env python3
"""Deterministic AI Recruitment OS agent runtime.

This module implements the productized P0 journey without external services.
It is intentionally rule-based: the production boundary is the `cs.*`
capability contract, not raw model access or direct ATS calls.
"""

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


class CapabilityExecutionError(Exception):
    """Raised when an agent attempts an invalid capability call."""


def load_agent_system(app_root):
    config_path = Path(app_root) / "configs" / "agent_system_design.json"
    return json.loads(config_path.read_text(encoding="utf-8"))


def initial_demo_state():
    return {
        "campaign": {
            "id": "search-platform-sbe",
            "title": "Senior Backend Engineer",
            "team": "Search Platform",
            "business_goal": "Reduce search latency by 40% in 2 quarters",
            "team_context": "Ranking infrastructure team owns high-traffic APIs and incident recovery.",
            "success_horizon": "180 days",
        },
        "candidates": [
            {
                "id": "lin-chen",
                "name": "Lin Chen",
                "headline": "Search infrastructure lead",
                "skills": ["distributed systems", "search ranking", "incident response", "ownership"],
                "evidence": [
                    "Led ranking migration for 1.2B daily queries",
                    "Maintained 99.95% search API SLA",
                    "Owned cross-team rollout with product and infra",
                ],
                "risks": ["Needs people-lead validation"],
                "stage": "review",
            },
            {
                "id": "maya-patel",
                "name": "Maya Patel",
                "headline": "Platform reliability engineer",
                "skills": ["reliability", "incident response", "platform APIs"],
                "evidence": [
                    "Reduced incident recovery time by 35%",
                    "Built service health dashboards for platform APIs",
                ],
                "risks": ["Less search-domain depth"],
                "stage": "review",
            },
            {
                "id": "jonas-weber",
                "name": "Jonas Weber",
                "headline": "Backend architect",
                "skills": ["backend architecture", "distributed systems"],
                "evidence": [
                    "Designed event-driven services for commerce workflows",
                    "Published internal architecture patterns",
                ],
                "risks": ["Recent roles lack delivery evidence", "Ownership signal is thin"],
                "stage": "review",
            },
        ],
        "post_hire_feedback": {
            "candidate_id": "lin-chen",
            "ninety_day_impact": "Improved incident recovery playbook and reduced ranking rollback time.",
            "manager_rating": 4.5,
            "retention_signal": "positive",
        },
        "audit_chain": [],
    }


def _registered_capability(agent_system, capability_id):
    return next(
        (
            capability
            for capability in agent_system["capability_services"]
            if capability["id"] == capability_id
        ),
        None,
    )


def _registered_agent(agent_system, agent_id):
    return next(
        (agent for agent in agent_system["agents"] if agent["id"] == agent_id),
        None,
    )


def _audit(state, agent_id, capability_id, output_key, human_confirmation_required=False):
    state["audit_chain"].append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": agent_id,
            "capability_id": capability_id,
            "output_key": output_key,
            "human_confirmation_required": human_confirmation_required,
        }
    )


def execute_capability(agent_system, state, agent_id, capability_id):
    agent = _registered_agent(agent_system, agent_id)
    capability = _registered_capability(agent_system, capability_id)

    if not agent:
        raise CapabilityExecutionError(f"Agent {agent_id} is not registered")
    if not capability:
        raise CapabilityExecutionError(f"Capability {capability_id} is not registered")
    if capability_id not in agent["capabilities"]:
        raise CapabilityExecutionError(f"Agent {agent_id} cannot call {capability_id}")
    if not capability_id.startswith("cs."):
        raise CapabilityExecutionError(f"Capability {capability_id} violates cs.* boundary")

    handlers = {
        "cs.role.create_success_model": _create_success_model,
        "cs.role.update_success_model": _update_success_model,
        "cs.candidate.parse_profile": _parse_profiles,
        "cs.candidate.build_evidence_card": _build_evidence_cards,
        "cs.candidate.rank_shortlist": _rank_shortlist,
        "cs.candidate.send_stage_update": _send_stage_update,
        "cs.candidate.generate_feedback": _generate_feedback,
        "cs.interview.generate_scorecard": _generate_scorecard,
        "cs.interview.capture_evidence": _capture_interview_evidence,
        "cs.decision.compare_candidates": _compare_candidates,
        "cs.audit.record_decision_basis": _record_decision_basis,
        "cs.audit.run_fairness_review": _run_fairness_review,
        "cs.audit.freeze_high_risk_action": _freeze_high_risk_action,
        "cs.feedback.collect_post_hire_signal": _collect_post_hire_signal,
        "cs.feedback.update_recruitment_world_model": _update_recruitment_world_model,
    }
    handler = handlers.get(capability_id)
    if not handler:
        raise CapabilityExecutionError(f"Capability {capability_id} has no handler")

    output_key = handler(state)
    _audit(
        state,
        agent_id,
        capability_id,
        output_key,
        human_confirmation_required=capability.get("human_confirmation", False),
    )
    return state[output_key]


def _create_success_model(state):
    campaign = state["campaign"]
    state["role_success_model"] = {
        "title": campaign["title"],
        "team": campaign["team"],
        "business_outcome": campaign["business_goal"],
        "success_horizon": campaign["success_horizon"],
        "must_prove": [
            "Designed and operated high-traffic distributed services",
            "Diagnosed production incidents with clear tradeoffs",
            "Owned cross-team delivery beyond local implementation",
        ],
        "risk_counterexamples": [
            "Only local optimization without production ownership",
            "High confidence without evidence for incident recovery",
        ],
        "interview_evidence": [
            "Architecture case",
            "Failure review",
            "Peer collaboration story",
        ],
    }
    return "role_success_model"


def _update_success_model(state):
    model = state["role_success_model"]
    model["confirmed_by"] = ["recruiter", "hiring_manager"]
    model["status"] = "confirmed"
    return "role_success_model"


def _parse_profiles(state):
    state["parsed_profiles"] = [
        {
            "candidate_id": candidate["id"],
            "name": candidate["name"],
            "normalized_skills": candidate["skills"],
            "source_count": len(candidate["evidence"]),
        }
        for candidate in state["candidates"]
    ]
    return "parsed_profiles"


def _build_evidence_cards(state):
    cards = []
    must_prove = state["role_success_model"]["must_prove"]
    for candidate in state["candidates"]:
        evidence_text = " ".join(candidate["evidence"]).lower()
        skill_text = " ".join(candidate["skills"]).lower()
        score = 55
        if "distributed systems" in skill_text:
            score += 12
        if "search" in skill_text or "ranking" in evidence_text:
            score += 14
        if "incident" in skill_text or "incident" in evidence_text:
            score += 10
        if "ownership" in skill_text or "owned" in evidence_text:
            score += 9
        score -= min(len(candidate["risks"]) * 4, 12)
        cards.append(
            {
                "candidate_id": candidate["id"],
                "name": candidate["name"],
                "headline": candidate["headline"],
                "score": max(0, min(score, 100)),
                "evidence": candidate["evidence"],
                "risks": candidate["risks"],
                "missing_information": [
                    item
                    for item in must_prove
                    if item.lower().split()[0] not in evidence_text
                ][:2],
            }
        )
    state["evidence_cards"] = cards
    return "evidence_cards"


def _rank_shortlist(state):
    ranked = sorted(state["evidence_cards"], key=lambda card: card["score"], reverse=True)
    shortlist = []
    for card in ranked:
        if card["score"] >= 85:
            recommendation = "strong"
        elif card["score"] >= 75:
            recommendation = "review"
        else:
            recommendation = "caution"
        shortlist.append(
            {
                "candidate_id": card["candidate_id"],
                "name": card["name"],
                "recommendation": recommendation,
                "score": card["score"],
                "top_evidence": card["evidence"][0],
                "risk": card["risks"][0] if card["risks"] else "No major risk",
                "human_confirmation_required": True,
            }
        )
    state["shortlist"] = shortlist
    return "shortlist"


def _send_stage_update(state):
    candidate = state["shortlist"][0]
    state["candidate_update"] = {
        "candidate_id": candidate["candidate_id"],
        "stage": "technical_interview",
        "message": "Your technical interview is scheduled. Focus on architecture tradeoffs, incident recovery, and ownership stories.",
    }
    return "candidate_update"


def _generate_feedback(state):
    state["candidate_feedback"] = {
        "candidate_id": state["shortlist"][-1]["candidate_id"],
        "message": "Thank you for the conversation. The current role needs stronger evidence of search-platform delivery, but your backend architecture experience may fit future platform roles.",
        "human_confirmation_required": True,
    }
    return "candidate_feedback"


def _generate_scorecard(state):
    state["scorecard"] = {
        "round": "technical_system_design",
        "dimensions": [
            {"id": "system_design", "weight": 0.35},
            {"id": "incident_recovery", "weight": 0.25},
            {"id": "ownership", "weight": 0.25},
            {"id": "collaboration", "weight": 0.15},
        ],
        "questions": [
            "Describe a high-traffic service decision you owned end to end.",
            "Walk through an incident where your first diagnosis was wrong.",
            "Which alternative architecture did you reject, and why?",
        ],
    }
    return "scorecard"


def _capture_interview_evidence(state):
    top = state["shortlist"][0]
    state["interview"] = {
        "candidate_id": top["candidate_id"],
        "evidence_captured": 7,
        "evidence_required": 7,
        "notes": [
            "Explained ranking migration tradeoffs clearly",
            "Connected rollback strategy to monitoring and product impact",
            "Needs one leadership calibration question",
        ],
        "score_suggestion": 91,
    }
    return "interview"


def _compare_candidates(state):
    state["decision"] = {
        "recommendation": "advance_to_final",
        "candidate_id": state["shortlist"][0]["candidate_id"],
        "reason": "Strongest evidence for search ranking, incident recovery, and ownership.",
        "unresolved_risk": "People-lead validation",
        "human_confirmation_required": True,
    }
    return "decision"


def _record_decision_basis(state):
    state["decision_basis"] = {
        "candidate_id": state["decision"]["candidate_id"],
        "evidence_links": [
            state["shortlist"][0]["top_evidence"],
            state["interview"]["notes"][0],
        ],
        "reviewer": "hiring_manager",
        "status": "ready_for_confirmation",
    }
    return "decision_basis"


def _run_fairness_review(state):
    caution_count = sum(1 for item in state["shortlist"] if item["recommendation"] == "caution")
    risk = "medium" if caution_count > 1 else "low"
    state["fairness_review"] = {
        "risk": risk,
        "flags": [] if risk == "low" else ["Review caution candidates for missing-evidence bias"],
        "required_human_action": risk != "low",
    }
    return "fairness_review"


def _freeze_high_risk_action(state):
    state["risk_freeze"] = {
        "frozen": state.get("fairness_review", {}).get("required_human_action", False),
        "reason": "Fairness review requires human action" if state.get("fairness_review", {}).get("required_human_action", False) else "No freeze required",
    }
    return "risk_freeze"


def _collect_post_hire_signal(state):
    state["post_hire_signal"] = deepcopy(state["post_hire_feedback"])
    return "post_hire_signal"


def _update_recruitment_world_model(state):
    signal = state["post_hire_signal"]
    state["evolution_report"] = {
        "model_update_proposal": [
            "Increase reliability evidence weight by 8%",
            "Add incident rollback drill to technical interview",
        ],
        "basis": signal["ninety_day_impact"],
        "requires_approval": True,
    }
    return "evolution_report"


def run_demo_journey(app_root):
    agent_system = load_agent_system(app_root)
    state = initial_demo_state()

    sequence = [
        ("mission_guard", "cs.role.create_success_model"),
        ("mission_guard", "cs.role.update_success_model"),
        ("talent_evidence_agent", "cs.candidate.parse_profile"),
        ("talent_evidence_agent", "cs.candidate.build_evidence_card"),
        ("shortlist_agent", "cs.candidate.rank_shortlist"),
        ("interview_copilot_agent", "cs.interview.generate_scorecard"),
        ("interview_copilot_agent", "cs.interview.capture_evidence"),
        ("calibration_agent", "cs.decision.compare_candidates"),
        ("calibration_agent", "cs.audit.record_decision_basis"),
        ("candidate_experience_agent", "cs.candidate.send_stage_update"),
        ("candidate_experience_agent", "cs.candidate.generate_feedback"),
        ("fairness_compliance_agent", "cs.audit.run_fairness_review"),
        ("fairness_compliance_agent", "cs.audit.freeze_high_risk_action"),
        ("learning_loop_agent", "cs.feedback.collect_post_hire_signal"),
        ("learning_loop_agent", "cs.feedback.update_recruitment_world_model"),
    ]
    for agent_id, capability_id in sequence:
        execute_capability(agent_system, state, agent_id, capability_id)

    state["status"] = "completed"
    state["agentRunLog"] = [
        {
            "agent": item["agent_id"],
            "capability": item["capability_id"],
            "confirmation": item["human_confirmation_required"],
        }
        for item in state["audit_chain"]
    ]
    return state


def write_demo_outputs(app_root):
    app_root = Path(app_root)
    result = run_demo_journey(app_root)
    data_dir = app_root / "prototype" / "data"
    reports_dir = app_root / "reports"
    data_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    (data_dir / "demo_state.json").write_text(
        json.dumps(_prototype_state(result), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (reports_dir / "agent_runtime_demo.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return result


def _prototype_state(result):
    return {
        "campaign": result["campaign"],
        "roleSuccessModel": result["role_success_model"],
        "candidates": result["shortlist"],
        "interview": result["interview"],
        "scorecard": result["scorecard"],
        "decision": result["decision"],
        "candidateUpdate": result["candidate_update"],
        "fairnessReview": result["fairness_review"],
        "evolutionReport": result["evolution_report"],
        "agentRunLog": result["agentRunLog"],
        "metrics": {
            "qualifiedShortlist": f"{sum(1 for item in result['shortlist'] if item['recommendation'] != 'caution')} / {len(result['candidates'])}",
            "evidenceCoverage": "100%",
            "hmSatisfaction": "92%",
            "biasRisk": result["fairness_review"]["risk"].title(),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run AI Recruitment OS agent demo journey")
    parser.add_argument("--app-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--write-demo", action="store_true")
    args = parser.parse_args()

    if args.write_demo:
        result = write_demo_outputs(args.app_root)
    else:
        result = run_demo_journey(Path(args.app_root))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
