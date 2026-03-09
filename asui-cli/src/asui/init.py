"""ASUI 项目初始化逻辑"""

from pathlib import Path

from .templates import get_template


def run_init(project_path: Path, template: str = "default", force: bool = False) -> bool:
    """初始化 ASUI 项目"""
    project_path = project_path.resolve()

    if not project_path.exists() and project_path != Path.cwd():
        project_path.mkdir(parents=True, exist_ok=True)

    template_content = get_template(template)

    for file_path, content in template_content.items():
        target = project_path / file_path
        if target.exists() and not force:
            print(f"  跳过（已存在）: {file_path}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"  创建: {file_path}")

    print(f"\n✅ ASUI 项目已初始化: {project_path}")
    print("  下一步: 在 Cursor/Claude Code 中打开项目，编辑 CLAUDE.md 和 configs/workflow_config.json")
    return True
