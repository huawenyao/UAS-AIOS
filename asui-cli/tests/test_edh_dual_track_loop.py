"""双轨闭环：SelfPaw → Business AGI 工作任务（不经客服数字人）。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.edh_dual_track import run_dual_track_loop  # noqa: E402


def test_dual_track_loop_escalates_without_persona_agent():
    result = run_dual_track_loop(ROOT)
    assert result["status"] == "completed"
    assert result["business_closed_loop"] is True
    assert result["working_task_id"]
    assert result["handoff"]["product_form"] == "world_model_studio"
    assert result["handoff"]["orchestration_identity"] == "pipaw"
    events = [e["event"] for e in result["audit_chain"]]
    assert "intent_escalated" in events
    assert "pipaw_cs_step" not in events
