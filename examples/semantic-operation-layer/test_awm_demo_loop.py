from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO_HTML = ROOT / "website" / "awm-demo" / "index.html"


def _load_loop():
    path = ROOT / "scripts" / "awm_demo_loop.py"
    spec = importlib.util.spec_from_file_location("awm_demo_loop", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_closed_loop_has_seven_beats_and_type_error() -> None:
    module = _load_loop()
    payload = module.build_closed_loop()
    assert payload["loop"] == [
        "match",
        "lens",
        "intent",
        "plan",
        "stage",
        "gate",
        "observe",
    ]
    assert payload["match"]["sku"] == "gate"
    beats = {item["id"]: item for item in payload["beats"]}
    assert beats["stage"]["writes_facts"] is False
    assert beats["gate"]["blocked"]["status"] == "blocked"
    assert beats["gate"]["committed"]["status"] == "committed"
    assert "unregistered action" in beats["plan"]["type_error"]
    assert beats["observe"]["observe"]["calibrated"] is True
    assert beats["observe"]["dikw"]["publishable"] is True


def test_demo_shell_has_world_first_landmarks() -> None:
    html = DEMO_HTML.read_text(encoding="utf-8")
    for token in (
        "situation-strip",
        "world-canvas",
        "intent-chips",
        "gate-tray",
        "问这个世界",
        "sku:A",
        "尝试未注册动作",
    ):
        assert token in html
    assert "textarea" not in html.lower()
    js = (ROOT / "website" / "awm-demo" / "demo.js").read_text(encoding="utf-8")
    assert "Now" in js and "Maybe" in js
    css = (ROOT / "website" / "awm-demo" / "demo.css").read_text(encoding="utf-8")
    assert ".card.maybe" in css
