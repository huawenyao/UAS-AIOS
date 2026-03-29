"""脚本工具网关。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


class ToolGateway:
    """统一执行 sub uas app 内的脚本。"""

    def execute_script(self, app_root: Path, script_relative_path: str, payload: dict) -> dict:
        script_path = app_root / script_relative_path
        env = os.environ.copy()
        env.setdefault("PYTHONIOENCODING", "utf-8")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            capture_output=True,
            cwd=app_root,
            check=True,
        )
        stdout = result.stdout.strip()
        try:
            return json.loads(stdout) if stdout else {}
        except json.JSONDecodeError:
            return {"stdout": stdout}
