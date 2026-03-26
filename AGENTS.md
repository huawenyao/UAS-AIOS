# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

ACA-protocol / UAS-AIOS is a knowledge-driven architecture framework (ASUI = AI-System-UI Integration). The installable CLI component is `asui-cli` (Python 3.8+). There are no Docker images or bundled databases; optional pieces include example scripts, a small UAS runtime helper, and a static site under `website/`.

### Key components

| Component | Location | How to run |
|-----------|----------|------------|
| `asui-cli` | `asui-cli/` | `asui init <project-name> [-t template]` |
| Example scripts | `examples/customer-service/scripts/create_ticket.py`, `examples/ai-recruitment/scripts/generate_report.py` | Pipe JSON via stdin: `echo '{"key":"val"}' \| python3 <script>` |
| UAS Runtime Service (CLI) | `scripts/run_uas_runtime_service.py` | `python3 scripts/run_uas_runtime_service.py list` |
| Static website | `website/` | `cd website && python3 -m http.server 8080` |

### Dev tools

- **Lint**: `ruff check asui-cli/src/ examples/` (passes clean)
- **Format**: `black --check asui-cli/src/ examples/` (existing code may have minor formatting diffs)
- **Test**: `cd asui-cli && python3 -m pytest tests/ -v`

### Caveats

- `pip install -e "./asui-cli[dev]"` installs the `asui` CLI to `~/.local/bin/`. Ensure `$HOME/.local/bin` is on `PATH` (e.g. in `~/.bashrc` on Linux/macOS).
- The `README.md` at the repo root may still contain unresolved merge conflict markers between `cursor/asui-fa59` and `main`; treat as a known documentation issue.
- Example scripts (`create_ticket.py`, `generate_report.py`) write outputs under `database/` and `reports/` relative to their example project; run them from the corresponding example directory.
