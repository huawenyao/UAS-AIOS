from __future__ import annotations


def build_domain_world_model() -> dict:
    """Return structured world model for AI recruitment domain."""
    return {
        "domain": "ai_recruitment",
        "entities": [
            "Job",
            "Candidate",
            "Task",
            "Event",
            "Notification",
            "Evaluation",
        ],
        "events": [
            "screening_completed",
            "candidate_shortlisted",
            "ai_interview_scheduled",
            "ai_interview_completed",
            "human_interview_completed",
            "evaluation_updated",
        ],
        "closed_loop_stages": ["sense", "model", "decide", "act", "verify", "learn"],
        "scenario_goal": "autonomous recruitment from resume screening to evaluation feedback",
    }


__all__ = ["build_domain_world_model"]
