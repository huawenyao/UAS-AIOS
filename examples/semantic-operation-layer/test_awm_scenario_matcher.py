from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRIEFS = Path(__file__).resolve().parent / "briefs"


def _load():
    path = ROOT / "scripts" / "awm_scenario_matcher.py"
    spec = importlib.util.spec_from_file_location("awm_scenario_matcher", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_product_definition_doc_exists() -> None:
    doc = (
        ROOT / "docs" / "strategic" / "AWM_PRODUCT_DEFINITION_CUSTOMERS_SCENARIOS_UX.md"
    )
    text = doc.read_text(encoding="utf-8")
    for token in (
        "AWM Lens",
        "AWM Stage",
        "AWM Gate",
        "World-first",
        "Palantir",
        "审批托盘",
    ):
        assert token in text


def test_replenishment_matches_gate() -> None:
    module = _load()
    result = module.match_path(str(BRIEFS / "replenishment_brief.json"))
    assert result["sku"] == "gate"
    assert result["ux_mode"] == "gate"
    assert result["domain_pack"] == "inventory_replenishment"
    assert result["publish_gate"] is True
    assert "SKU" in result["first_objects"]


def test_chat_only_stays_on_lens() -> None:
    module = _load()
    result = module.match_path(str(BRIEFS / "chat_only_brief.json"))
    assert result["sku"] == "lens"
    assert result["ux_mode"] == "lens"
    assert result["publish_gate"] is False
    assert any("对象身份" in reason for reason in result["reasons"])


def test_full_auto_without_compensation_is_stage_not_gate() -> None:
    module = _load()
    result = module.match_path(str(BRIEFS / "full_auto_no_rollback_brief.json"))
    assert result["sku"] == "stage"
    assert result["ux_mode"] == "stage"
    assert any(
        "拒绝 Gate" in reason or "降级" in reason for reason in result["reasons"]
    )
