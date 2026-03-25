# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

UAS-AIOS is a knowledge-driven AI systems platform (Python 3.8+). It has no Docker, no databases, no long-running HTTP services. Everything is CLI-invoked or library-imported.

### Key Components

| Component | Location | Run Command |
|-----------|----------|-------------|
| `asui-cli` | `asui-cli/` | `asui init <project> -t <template>` |
| `uas_world_model` | `uas_world_model/` | `python3 uas_world_model/demo.py` |
| UAS Runtime Service | `scripts/run_uas_runtime_service.py` | `python3 scripts/run_uas_runtime_service.py list` |
| Static Website | `website/` | `cd website && python3 -m http.server 8080` |

### Testing

- **asui-cli tests** (pytest): `cd asui-cli && python3 -m pytest tests/ -v` — 10 tests, all pass.
- **uas_world_model tests** (unittest): `python3 -m unittest uas_world_model/tests/test_core.py -v` — 9/14 pass; 5 pre-existing failures (latent_planning numpy ambiguity, knowledge_evolution API mismatch, intent constraint/priority edge cases).

### Lint

- `ruff check .` — runs from workspace root; pre-existing warnings (unused imports, E402).
- `black --check asui-cli/src/ uas_world_model/ scripts/` — pre-existing formatting differences in ~29 files.

### Gotchas

- `asui` CLI is installed to `~/.local/bin/`. Ensure `PATH` includes `$HOME/.local/bin`.
- `README.md` at workspace root contains unresolved git merge conflict markers between `cursor/asui-fa59` and `main`.
- The `uas_world_model` tests that fail are pre-existing bugs in `latent_planning.py` (numpy truth-value ambiguity) and `knowledge_evolution.py` (unexpected `changes_validated` kwarg). Do not treat these as regressions.
