from __future__ import annotations

import importlib.util
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = Path(__file__).resolve().parent / "replenishment_sio.json"


def _load_layer_module():
    path = ROOT / "scripts" / "semantic_operation_layer.py"
    spec = importlib.util.spec_from_file_location("semantic_operation_layer", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_report_exists_and_uses_sio_mmos_dikw() -> None:
    doc = (
        ROOT
        / "docs"
        / "strategic"
        / "SIO_MMOS_DIKW_Agent_World_Model_And_Semantic_Operation_Layer.md"
    )
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    for token in ("SIO-MMOS", "DIKW", "语义操作层", "DreamerV3", "Palantir", "MCP"):
        assert token in text


def test_replenishment_closed_loop_requires_approval() -> None:
    module = _load_layer_module()
    result = module.run_replenishment_demo(str(EXAMPLE))
    assert result["domain"] == "inventory_replenishment"
    assert result["plan"]["validation"]["ok"] is True
    assert result["simulate"]["writes_facts"] is False
    assert result["simulate"]["meets_intent"] is True
    assert result["blocked_without_approval"]["status"] == "blocked"
    assert result["committed_with_approval"]["status"] == "committed"
    assert result["observe"]["mode"] == "observe"
    assert result["observe"]["meets_intent"] is True
    dikw = result["explain"]["dikw"]
    assert dikw["data"] == 1.0
    assert dikw["information"] == 1.0
    assert dikw["knowledge"] == 1.0
    assert dikw["publishable"] is True
    assert any(item["op"] == "compile" for item in result["audit"])


def test_unregistered_action_is_rejected() -> None:
    module = _load_layer_module()
    layer = module.SemanticOperationLayer.from_path(str(EXAMPLE))
    with pytest.raises(module.SemanticOperationError, match="unregistered action"):
        layer.compile(
            [
                {
                    "id": "step-x",
                    "action": "erp.drop_table",
                    "input": {"sku_id": "sku:A"},
                }
            ]
        )


def test_budget_precondition_blocks_overbuy() -> None:
    module = _load_layer_module()
    layer = module.SemanticOperationLayer.from_path(str(EXAMPLE))
    with pytest.raises(module.SemanticOperationError, match="exceeds budget"):
        layer.compile(
            [
                {
                    "id": "step-1",
                    "action": "replenishment.create_purchase_order",
                    "input": {
                        "sku_id": "sku:A",
                        "warehouse_id": "wh:W1",
                        "supplier_id": "sup:S1",
                        "quantity": 999999,
                    },
                }
            ]
        )


def test_unregistered_object_type_rejected_at_load() -> None:
    module = _load_layer_module()
    layer = module.SemanticOperationLayer.from_path(str(EXAMPLE))
    broken = deepcopy(layer.spec)
    broken["situation"]["objects"].append({"id": "ghost:1", "type": "NotAClass"})
    with pytest.raises(module.SemanticOperationError, match="unregistered type"):
        module.SemanticOperationLayer(broken)
