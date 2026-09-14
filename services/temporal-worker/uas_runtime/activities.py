"""Temporal Activity：只回调 Hub，禁止直连 SoR / 在此跑模型。"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

HUB_ROOT = Path(__file__).resolve().parents[2] / "hub-api"
if str(HUB_ROOT) not in sys.path:
    sys.path.insert(0, str(HUB_ROOT))

from uas_hub.cycle import invoke_and_finish  # noqa: E402


def activity_runtime_cycle(hub: Any, run: dict[str, Any]) -> dict[str, Any]:
    return invoke_and_finish(hub, run)
