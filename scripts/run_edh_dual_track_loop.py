#!/usr/bin/env python3
"""运行 SelfPaw → ΠPaw → cs.* 双轨业务闭环原型。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.edh_dual_track import run_dual_track_cs_loop  # noqa: E402


def main() -> int:
    result = run_dual_track_cs_loop(ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
