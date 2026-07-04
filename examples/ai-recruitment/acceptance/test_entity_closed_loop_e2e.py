from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_entity_closed_loop_runner_passes(tmp_path):
    work = tmp_path / "ai-recruitment-run"
    shutil.copytree(ROOT / "configs", work / "configs")
    shutil.copytree(ROOT / "scripts", work / "scripts")
    (work / "database").mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["AI_RECRUITMENT_ROOT"] = str(work)
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        [sys.executable, str(work / "scripts" / "run_entity_closed_loop.py")],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["passed"] is True
    assert payload["counts"]["events"] >= 1
    assert (work / "database" / "evaluations.json").exists()
