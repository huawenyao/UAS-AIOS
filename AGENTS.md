# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

ACA-protocol / UAS-AIOS is a knowledge-driven architecture framework (ASUI = AI-System-UI Integration). The installable CLI component is `asui-cli` (Python 3.8+). There are no Docker images or bundled databases; optional pieces include example scripts, a small UAS runtime helper, and a static site under `website/`.

### Key components

| Component | Location | How to run |
|-----------|----------|------------|
| `asui-cli` | `asui-cli/` | `asui init <project-name> [-t template]` |
| Example scripts | `examples/ai-recruitment/scripts/generate_report.py`；客服模板：`asui init demo -t customer-service` 后运行 `scripts/create_ticket.py` | Pipe JSON via stdin: `echo '{"key":"val"}' \| python3 <script>` |
| SelfPaw (User AGI) | **`../aipos/copaw-src`**（本机 `C:\Users\ranwu\XiaomiCloud\aipos\copaw-src`）| 个人认知 OS 主实现；UAS-AIOS 仅企业桥接，见 `docs/SELFPaw_REFERENCE_IMPLEMENTATION.md` |
| UAS Runtime Service (CLI) | `scripts/run_uas_runtime_service.py` | `python3 scripts/run_uas_runtime_service.py list` |
| Static website | `website/` | `cd website && python3 -m http.server 8080` |

### Dev tools

- **Lint**: `ruff check asui-cli/src/ examples/` (passes clean)
- **Format**: `black --check asui-cli/src/ examples/` (existing code may have minor formatting diffs)
- **Test**: `cd asui-cli && python3 -m pytest tests/ -v`

### Caveats

- `pip install -e "./asui-cli[dev]"` installs the `asui` CLI to `~/.local/bin/`. Ensure `$HOME/.local/bin` is on `PATH` (e.g. in `~/.bashrc` on Linux/macOS).
- The `README.md` at the repo root may still contain unresolved merge conflict markers between `cursor/asui-fa59` and `main`; treat as a known documentation issue.
- Example scripts write outputs under `database/` and `reports/` relative to their project root; run from that directory. There is no `examples/customer-service/` — use `asui init` with `-t customer-service` instead.
