# AGENTS.md

## Cursor Cloud specific instructions

### 项目概述

ACA-protocol / ASUI 是一个知识驱动型 AI 系统架构框架，核心产物是 `asui-cli`——一个 Python CLI 脚手架工具。项目无需运行服务（无 Docker、无 Web 服务器、无数据库）。

### 开发命令

- **Lint**: `ruff check .`（从 repo 根目录运行）
- **格式化检查**: `black --check .`（现有代码存在格式差异，这是已知状态）
- **测试**: `pytest`（项目目前无测试用例，pytest 已安装但会返回 "no tests collected"）
- **CLI 帮助**: `asui --help`
- **脚手架功能**: `asui init <project-name> [-t default|customer-service|recruitment] [-f]`

### 注意事项

- `asui` 命令安装在 `~/.local/bin/`，需确保该路径在 `PATH` 中。update script 已通过 `pip install --user` 自动处理。
- 项目零运行时依赖，开发依赖仅 `pytest`、`black`、`ruff`。
- `examples/` 下的脚本（`create_ticket.py`、`generate_report.py`）通过 stdin 接收 JSON 数据，可直接用 `echo '...' | python3 script.py` 测试。
- `README.md` 中存在 git merge conflict markers（`<<<<<<<` / `>>>>>>>`），这是仓库已有状态。
