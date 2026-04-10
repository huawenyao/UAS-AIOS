<div align="center">

# UAS-AIOS

**Cognitive Computing Infrastructure — Make Intelligence Reflexive**

[![License: MIT](https://img.shields.io/badge/License-MIT-22d3ee.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

*A knowledge-driven platform for building autonomous AI systems with world models, multi-agent orchestration, and continuous evolution.*

[Architecture](#architecture) · [Quick Start](#quick-start) · [Documentation](#documentation) · [Examples](#examples) · [Contributing](CONTRIBUTING.md)

</div>

---

## What is UAS-AIOS?

UAS-AIOS is a cognitive computing platform that enables organizations to build, deploy, and evolve **world-model-powered AI systems**. Instead of treating AI as a stateless tool, UAS-AIOS provides infrastructure for AI that _understands_ its domain, _plans_ autonomously, and _evolves_ through feedback.

**Core Principles:**
- **Knowledge as Configuration** — Business rules live in config files, not code. Change a config, change the behavior.
- **Build = Run** — No compilation or deployment step. Knowledge updates take effect immediately.
- **Incremental Evolution** — Systems improve continuously through the push → feedback → reflexivity loop.

### Key Components

| Component | Description |
|-----------|-------------|
| **World Model Engine** | Intent understanding, dynamic planning, system modeling, and drift detection |
| **Autonomous Runtime** | Config-driven workflow execution with cognitive state tracking |
| **Agent Orchestration** | Multi-agent coordination, swarm intelligence, and cognitive routing |
| **Evolution Engine** | Automated drift detection, knowledge evolution, and feedback loops |
| **ASUI CLI** | Scaffolding tool to bootstrap new domain projects in seconds |

---

## Architecture

```
UAS-Platform = (I, K, R, A, S, G, E, Π)

I — Intent          Natural-language intent understanding and goal decomposition
K — Knowledge       Hybrid knowledge base (graphs + vectors + rules), ASUI standard
R — Runtime         Autonomous agent runtime with cognitive state management
A — Agent Fabric    Multi-agent orchestration, swarm coordination
S — System Grid     Service integration mesh and data pipelines
G — Governance      Policy enforcement, audit trails, access control
E — Evolution       Drift detection, feedback loops, continuous optimization
Π — Protocol        Standardized interfaces and interoperability contracts
```

**Dual-Track AGI Architecture:**

| Track | Purpose | Implementation |
|-------|---------|----------------|
| **User AGI** | Personal cognitive agent | `selfpaw` — swarm intelligence with five specialized agents |
| **Business AGI** | Organizational intelligence | `Πpaw` — multi-professional agent orchestration |

> See [docs/THEORY_SYSTEM.md](docs/THEORY_SYSTEM.md) for the complete theoretical framework.

---

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### 1. Install the ASUI CLI

```bash
cd asui-cli && pip install -e ".[dev]"
```

### 2. Scaffold a New Project

```bash
# Default UAS sub-app template
asui init my-project -t uas-subapp

# AI recruitment template
asui init recruitment-demo -t recruitment

# Swarm intelligence template
asui init swarm-demo -t selfpaw-swarm
```

### 3. Run the World Model Demo

```bash
python3 uas_world_model/demo.py
```

This demonstrates the cognitive engine's core capabilities: intent understanding, dynamic planning, system modeling, and drift detection.

### 4. Run the UAS Runtime Service

```bash
# List all discovered sub-apps
python3 scripts/run_uas_runtime_service.py list

# Run a sub-app with a business topic
python3 scripts/run_uas_runtime_service.py run \
  --app-id ai-recruitment-os \
  --topic "Evaluate candidates for senior engineer position"
```

### 5. View the Neurospan Website

```bash
cd website && python3 -m http.server 8080
# Open http://localhost:8080
```

---

## Project Structure

```
.
├── asui-cli/                  # ASUI scaffolding CLI tool
│   ├── src/asui/              # CLI source + runtime modules
│   └── tests/                 # Pytest test suite
├── uas_world_model/           # World Model cognitive engine
│   ├── core/                  # Intent, knowledge, planning, evolution modules
│   ├── demo.py                # Interactive demo
│   └── tests/                 # Unit tests
├── scripts/                   # Platform utility scripts
├── projects/                  # Deployed UAS sub-apps
│   └── ai-recruitment-os/     # AI recruitment system (fully operational)
├── examples/                  # Example applications
│   ├── ai-recruitment/        # AI recruitment domain validation
│   ├── selfpaw-cognitive-swarm/   # User AGI swarm intelligence
│   └── triadic-ideal-reality-swarm/ # Ideal-reality analysis
├── docs/                      # Theory, architecture, and strategy docs
├── configs/                   # Business rule configurations
├── whitepaper/                # ASUI architecture whitepaper
├── website/                   # Neurospan static website
└── CLAUDE.md                  # System operations manual (AI-readable)
```

---

## Testing

```bash
# ASUI CLI tests (pytest)
cd asui-cli && python3 -m pytest tests/ -v

# World Model tests (unittest)
python3 -m unittest uas_world_model/tests/test_core.py -v

# Lint
ruff check .
black --check asui-cli/src/ uas_world_model/ scripts/
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Theory System](docs/THEORY_SYSTEM.md) | Complete theoretical framework and methodology |
| [World Model Deep Dive](docs/世界模型/世界模型.md) | World model as "law compiler" — core philosophy |
| [AGI & World Model](docs/AGI_WORLD_MODEL_UAS.md) | Dual-track AGI architecture and evolution roadmap |
| [ASUI Architecture](docs/ASUI_ARCHITECTURE.md) | AI-System-UI Integration paradigm |
| [ASUI Whitepaper](whitepaper/ASUI_WHITEPAPER_CN.md) | Architecture whitepaper |
| [Platform Standard](docs/UAS_PLATFORM_STANDARD.md) | UAS platform technical standard |
| [Cognitive Superintelligence](docs/认知超智能.md) | Representation–Enaction unification theory |
| [Documentation Index](docs/README.md) | Full documentation directory |

---

## Examples

### AI Recruitment System

A fully operational domain application demonstrating the ASUI architecture:

```bash
# Run the recruitment workflow
python3 scripts/run_uas_runtime_service.py run \
  --app-id ai-recruitment-os \
  --topic "Screen candidates for backend engineer role"
```

See [examples/ai-recruitment/README.md](examples/ai-recruitment/README.md) for detailed usage.

### Swarm Intelligence (selfpaw)

Five-agent cognitive swarm for multi-perspective analysis:

See [examples/selfpaw-cognitive-swarm/README.md](examples/selfpaw-cognitive-swarm/README.md).

### Triadic Ideal-Reality Analysis

Macro/meso/micro ideal-reality dialectical synthesis:

See [examples/triadic-ideal-reality-swarm/README.md](examples/triadic-ideal-reality-swarm/README.md).

---

## Roadmap

- [x] ASUI architecture and CLI scaffolding
- [x] World Model cognitive engine (intent, planning, evolution)
- [x] Autonomous agent runtime with cognitive state
- [x] Multi-agent swarm intelligence (selfpaw)
- [x] UAS platform standard and sub-app ecosystem
- [ ] Janus World Model — unified representation + enaction architecture
- [ ] Phase transition engine (crystallization, activation, evaporation, sublimation)
- [ ] Cross-domain law discovery and transfer
- [ ] Real-time perception and continuous learning

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contact

- Email: contact@neurospan.io
- GitHub: [ACA-protocol](https://github.com/ACA-protocol)
