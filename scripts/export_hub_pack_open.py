#!/usr/bin/env python3
"""把 Hub.pack.open 切片写成 WorkStudio demo 夹具（无 HTTP、无零件 SDK）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "services" / "hub-api"))

from uas_hub.hub import Hub  # noqa: E402

OUT_JSON = REPO / "projects" / "aios-workstudio" / "demo" / "hub-pack-open.fixture.json"
OUT_JS = REPO / "projects" / "aios-workstudio" / "demo" / "hub-pack-open.fixture.js"


def main() -> int:
    fixture = Hub.from_repo(REPO).export_scene_fixture()
    OUT_JSON.write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_JS.write_text("window.HUB_PACK = " + json.dumps(fixture, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(OUT_JSON.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
