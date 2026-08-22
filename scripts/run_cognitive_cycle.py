#!/usr/bin/env python3
"""仓库根入口：转发到 examples/world-model-studio。"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

TARGET = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "world-model-studio"
    / "scripts"
    / "run_cognitive_cycle.py"
)


if __name__ == "__main__":
    sys.argv[0] = str(TARGET)
    runpy.run_path(str(TARGET), run_name="__main__")
