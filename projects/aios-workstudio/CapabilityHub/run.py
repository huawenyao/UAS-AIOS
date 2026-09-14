#!/usr/bin/env python3
"""启动 WorkStudio Capability Hub：同一进程、只暴露 /hub/v1，内核复用 uas_hub。"""

from __future__ import annotations

import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent
REPO = PKG.parents[2]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(REPO / "services" / "hub-api"))

import uvicorn  # noqa: E402


def main() -> None:
    uvicorn.run("capability_hub.http_app:app", host="127.0.0.1", port=18088, reload=False)


if __name__ == "__main__":
    main()
