#!/usr/bin/env python3
"""启动 Hub HTTP：同一进程、只暴露 /hub/v1。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "services" / "hub-api"
CONSOLE = ROOT / "projects" / "aios-workstudio" / "CapabilityHub"
sys.path.insert(0, str(CONSOLE))
sys.path.insert(0, str(HUB))

import uvicorn  # noqa: E402


def main() -> None:
    uvicorn.run("capability_hub.http_app:app", host="127.0.0.1", port=18088, reload=False)


if __name__ == "__main__":
    main()
