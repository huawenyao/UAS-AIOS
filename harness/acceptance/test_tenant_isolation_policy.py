"""
REQ-EDH-PL-001 跨租户访问拒绝用例。
运行: python harness/acceptance/test_tenant_isolation_policy.py
或: python scripts/validate_enterprise_policy.py validate
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_enterprise_policy.py"


def main() -> int:
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "validate"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    print(r.stdout or r.stderr)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
