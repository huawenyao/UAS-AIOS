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
| **Enterprise Agent Ecosystem** | `enterprise/` | `python3 enterprise/examples/b2b_lead_to_payment/scripts/b2b_pipeline.py` |

### Enterprise Agent Ecosystem (L1-L3)

The `enterprise/` directory contains the full UAS-AIOS enterprise-grade Agent ecosystem:

| Layer | Component | Location |
|-------|-----------|----------|
| cs.* Semantic Services | Capability gateway + adapters | `enterprise/platform/capability_services/` |
| Data Plane | Tenant mgmt + event stream + audit chain | `enterprise/platform/data_plane/` |
| Governance | Permission engine + compliance + SLA | `enterprise/platform/governance/` |
| L1 SelfPaw | Personal digital twin (6 capabilities) | `enterprise/agents/l1_selfpaw/` |
| L2 ΠPaw | Functional digital humans (HR/Finance/Compliance) | `enterprise/agents/l2_pipaw/` |
| L3 ΠPaw | Business digital humans (Sales/CS/Bidding) | `enterprise/agents/l3_pipaw/` |
| Domain Packages | Industry-specific Ontology + rules | `enterprise/domain_packages/` |
| Workflow Templates | Parameterized process templates | `enterprise/workflow_templates/` |
| B2B Example | End-to-end lead → payment demo | `enterprise/examples/b2b_lead_to_payment/` |

**CLI Template**: `asui init <name> -t enterprise` scaffolds a full enterprise deployment.

### Dev tools

- **Lint**: `ruff check asui-cli/src/ examples/` (passes clean)
- **Format**: `black --check asui-cli/src/ examples/` (existing code may have minor formatting diffs)
- **Test**: `cd asui-cli && python3 -m pytest tests/ -v`

### Caveats

- `pip install -e "./asui-cli[dev]"` installs the `asui` CLI to `~/.local/bin/`. Ensure `$HOME/.local/bin` is on `PATH` (e.g. in `~/.bashrc` on Linux/macOS).
- The `README.md` at the repo root may still contain unresolved merge conflict markers between `cursor/asui-fa59` and `main`; treat as a known documentation issue.
- Example scripts (`create_ticket.py`, `generate_report.py`) write outputs under `database/` and `reports/` relative to their example project; run them from the corresponding example directory.
