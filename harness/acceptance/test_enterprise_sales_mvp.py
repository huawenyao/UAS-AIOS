"""Enterprise Sales OS MVP CASE-001～008 验收。"""

import subprocess
import sys
from pathlib import Path


def test_sales_mvp_all_cases_pass():
    root = Path(__file__).resolve().parents[2]
    script = root / "projects" / "enterprise-sales-os" / "scripts" / "evaluate_sales_mvp.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
