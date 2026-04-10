# Contributing to UAS-AIOS

Thank you for your interest in contributing to UAS-AIOS! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ACA-protocol/UAS-AIOS.git
cd UAS-AIOS

# Install the ASUI CLI with dev dependencies
cd asui-cli && pip install -e ".[dev]"
```

### Running Tests

```bash
# ASUI CLI tests
cd asui-cli && python3 -m pytest tests/ -v

# World Model tests
python3 -m unittest uas_world_model/tests/test_core.py -v
```

### Lint & Format

```bash
ruff check .
black --check asui-cli/src/ uas_world_model/ scripts/
```

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/ACA-protocol/UAS-AIOS/issues) to avoid duplicates
2. Use the **Bug Report** issue template
3. Include: Python version, OS, steps to reproduce, expected vs actual behavior

### Suggesting Features

1. Open an issue using the **Feature Request** template
2. Describe the use case and expected behavior
3. Reference relevant sections of the [theory system](docs/THEORY_SYSTEM.md) if applicable

### Submitting Code

1. Fork the repository
2. Create a feature branch from `main`: `git checkout -b feature/your-feature`
3. Make your changes with clear commit messages
4. Add tests for new functionality
5. Run the test suite and linter
6. Submit a Pull Request

### Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Include tests for new code
- Update documentation if behavior changes
- Follow existing code style (PEP 8 for Python)
- Reference related issues in the PR description

## Project Structure

| Directory | Description | Key Files |
|-----------|-------------|-----------|
| `asui-cli/` | CLI scaffolding tool | `src/asui/main.py`, `src/asui/runtime/` |
| `uas_world_model/` | Cognitive engine library | `core/*.py`, `demo.py` |
| `scripts/` | Platform utility scripts | `run_uas_runtime_service.py` |
| `projects/` | Deployed sub-apps | `ai-recruitment-os/` |
| `examples/` | Example applications | `ai-recruitment/`, `selfpaw-cognitive-swarm/` |
| `docs/` | Documentation | `THEORY_SYSTEM.md`, `ASUI_ARCHITECTURE.md` |
| `configs/` | Business rule configs | `*.json` |

## Code Style

- **Python**: Follow PEP 8. Use `black` for formatting, `ruff` for linting.
- **Documentation**: Use Markdown. Keep language clear and concise.
- **Commit messages**: Use imperative mood ("Add feature" not "Added feature").

## Communication

- **Issues**: For bug reports, feature requests, and discussions
- **Pull Requests**: For code contributions
- **Email**: contact@neurospan.io

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
