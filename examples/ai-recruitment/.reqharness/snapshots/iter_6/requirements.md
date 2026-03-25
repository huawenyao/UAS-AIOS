Feature: AI Recruitment World Model Closed Loop

## Goal
Turn this project into a domainized AI recruitment world model and an autonomous automation closed loop that can be reused by agent workflows.

## Required Deliverables
1. Add domain model module `scripts/domain_world_model.py`:
   - Expose `build_domain_world_model() -> dict`
   - Include entities, events, and closed-loop stages for recruitment.
2. Add orchestration module `scripts/recruitment_closed_loop.py`:
   - Expose `run_recruitment_closed_loop(candidates: list[dict]) -> dict`
   - Produce structured outputs for screening/interview/evaluation/notifications.
3. Add domain document `docs/AI招聘世界模型.md`:
   - Must clearly explain world model, entities, events, and closed-loop scenarios.

## Constraints
- NEVER modify `acceptance/`.
- Prefer additive changes under `scripts/` and `docs/`.
- Keep implementation deterministic and testable.

## Success Criteria
- All tests under `acceptance/` pass.
- World model and closed-loop contracts are machine-verifiable.
