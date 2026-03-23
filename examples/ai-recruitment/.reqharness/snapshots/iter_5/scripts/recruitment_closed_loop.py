from __future__ import annotations


def run_recruitment_closed_loop(candidates: list[dict]) -> dict:
    """Run a deterministic recruitment closed-loop orchestration contract."""
    screened = []
    shortlisted = []
    for c in candidates:
        cid = c.get("candidate_id", "unknown")
        score = float(c.get("total_score", 0.0))
        decision = "recommend" if score >= 7.0 else "borderline"
        item = {"candidate_id": cid, "score": score, "decision": decision}
        screened.append(item)
        if score >= 7.0:
            shortlisted.append(item)

    interview = {
        "scheduled": [x["candidate_id"] for x in shortlisted],
        "completed": [x["candidate_id"] for x in shortlisted],
    }
    evaluation = {
        "count": len(shortlisted),
        "status": "generated",
        "summary": "AI interview evaluation records created for shortlisted candidates.",
    }
    notifications = {
        "hr_recruiter": len(shortlisted),
        "hiring_manager": len(shortlisted),
    }
    events = [
        "screening_completed",
        "ai_interview_completed",
    ]
    return {
        "screening": screened,
        "interview": interview,
        "evaluation": evaluation,
        "notifications": notifications,
        "events": events,
    }


__all__ = ["run_recruitment_closed_loop"]
