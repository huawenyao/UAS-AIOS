# AGENTS.md (ReqHarness Semantic Map)

## Project Goal
Build an AI recruitment domain world model and an automation closed loop.

## Key Paths
- `configs/`: schemas and event policy
- `scripts/`: executable workflow and runtime logic
- `docs/`: domain knowledge and operation guides
- `acceptance/`: locked evaluator tests for reqharness

## Hard Constraints
- Do not modify `acceptance/`.
- Keep outputs auditable and evidence-oriented.
- Reuse existing entity/event model whenever possible.
