"""Enterprise Sales OS UAS runtime 端到端验收。"""

import json
import subprocess
import sys
from pathlib import Path


def test_enterprise_sales_runtime_run_completed():
    root = Path(__file__).resolve().parents[2]
    payload = json.dumps(
        {
            "governance_controls": ["audit", "approval", "rollback"],
            "evolution_loop": ["intent_activation", "governance_check", "sales_execute"],
            "sales_case_id": "CASE-001",
        },
        ensure_ascii=False,
    )
    result = subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "run_uas_runtime_service.py"),
            "run",
            "--app-id",
            "enterprise-sales-os",
            "--topic",
            "B2B标准线索报价",
            "--evaluate",
            "--payload-json",
            payload,
        ],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    out = json.loads(result.stdout)
    assert out["status"] == "completed"
    assert out["evaluation"]["status"] == "pass"
    assert (root / "projects" / "enterprise-sales-os" / out["audit_log"]).exists()
