"""脚本工具网关。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


class ToolGateway:
    """统一执行 sub uas app 内的脚本。"""

    def execute_script(self, app_root: Path, script_relative_path: str, payload: dict) -> dict:
        script_path = app_root / script_relative_path
        result = subprocess.run(
            [sys.executable, str(script_path)],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            capture_output=True,
            cwd=app_root,
            check=True,
        )
        stdout = result.stdout.strip()
        try:
            return json.loads(stdout) if stdout else {}
        except json.JSONDecodeError:
            return {"stdout": stdout}
