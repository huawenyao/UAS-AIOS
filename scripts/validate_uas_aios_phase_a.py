#!/usr/bin/env python3
"""阶段 A 契约：schema + Hub 门禁/签发。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HUB = REPO / "services" / "hub-api"


def main() -> int:
    sys.path.insert(0, str(HUB))
    suite = unittest.defaultTestLoader.discover(str(HUB / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
