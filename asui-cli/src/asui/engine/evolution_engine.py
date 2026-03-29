"""演化引擎。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


class EvolutionEngine:
    """执行评估脚本并提取进化结果。"""

    def evaluate(self, app_root: Path, payload: dict) -> dict:
        candidates = [
            "scripts/evaluate_evolution.py",
            "scripts/evaluate_iteration.py",
        ]
        env = os.environ.copy()
        env.setdefault("PYTHONIOENCODING", "utf-8")
        # evaluate_evolution.py 已支持四维打分（业务/产品/技术/运行效果），驱动自主进化
        for candidate in candidates:
            script_path = app_root / candidate
            if script_path.exists():
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
                return json.loads(result.stdout)
        return {"status": "pass", "suggestions": ["未定义评估脚本，默认通过"]}
