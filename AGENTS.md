# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

ACA-protocol is a knowledge-driven architecture framework (ASUI = AI-System-UI Integration). The only installable component is `asui-cli`, a Python CLI scaffolding tool located at `asui-cli/`. There are no web servers, databases, Docker services, or external dependencies.

### Services

| Component | Description | How to run |
|-----------|-------------|------------|
| `asui-cli` | Python CLI scaffolding tool | `asui init <project-name> [-t template]` |
| Example scripts | `examples/customer-service/scripts/create_ticket.py`, `examples/ai-recruitment/scripts/generate_report.py` | Pipe JSON via stdin: `echo '{"key":"val"}' \| python3 <script>` |

### Dev tools

- **Lint**: `ruff check asui-cli/src/ examples/` (passes clean)
- **Format**: `black --check asui-cli/src/ examples/` (existing code has minor formatting diffs; this is the repo's current state)
- **Test**: `cd asui-cli && pytest` (no test files exist yet; framework is set up)

### Caveats

- `pip install -e "./asui-cli[dev]"` installs to `~/.local/bin/`. Ensure `$HOME/.local/bin` is on `PATH` (already configured in this VM's `~/.bashrc`).
- The `README.md` at root has a git merge conflict between branches `cursor/asui-fa59` and `main`. This is a pre-existing issue.
- Example scripts (`create_ticket.py`, `generate_report.py`) write output files to `database/` and `reports/` subdirectories relative to their example project. Run them from their respective example directories.
