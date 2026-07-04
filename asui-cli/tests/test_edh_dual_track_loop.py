"""双轨闭环：SelfPaw → ΠPaw → cs.*"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.edh_dual_track import run_dual_track_cs_loop  # noqa: E402


def test_dual_track_cs_loop_completes():
    result = run_dual_track_cs_loop(ROOT)
    assert result["status"] == "completed"
    assert result["business_closed_loop"] is True
    assert result["working_task_id"]
