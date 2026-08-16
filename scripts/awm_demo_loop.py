#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AWM 产品 Demo 闭环：Match → Lens → Plan → Stage → Gate → Observe。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "examples" / "semantic-operation-layer" / "replenishment_sio.json"
BRIEF = (
    ROOT
    / "examples"
    / "semantic-operation-layer"
    / "briefs"
    / "replenishment_brief.json"
)
LOOP_JSON = ROOT / "examples" / "semantic-operation-layer" / "demo" / "loop.json"
DEMO_JS = ROOT / "website" / "awm-demo" / "demo-data.js"


def _load(name: str, path: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_closed_loop() -> Dict[str, Any]:
    matcher = _load(
        "awm_scenario_matcher", ROOT / "scripts" / "awm_scenario_matcher.py"
    )
    sol = _load(
        "semantic_operation_layer", ROOT / "scripts" / "semantic_operation_layer.py"
    )
    match = matcher.match_path(str(BRIEF))
    layer = sol.SemanticOperationLayer.from_path(str(SPEC))
    runtime = sol.run_replenishment_demo(str(SPEC))
    type_error = None
    try:
        layer.compile(
            [
                {
                    "id": "step-x",
                    "action": "erp.drop_table",
                    "input": {"sku_id": "sku:A"},
                }
            ]
        )
    except sol.SemanticOperationError as exc:
        type_error = str(exc)

    facts = layer.spec["situation"]["facts"]
    projected = runtime["simulate"]["projected_facts"]
    beats = [
        {
            "id": "match",
            "title": "90 秒匹配",
            "sku": match["sku"],
            "ux_mode": match["ux_mode"],
            "highlight": "先匹配世界结构，不先打开聊天",
            "reasons": match["reasons"],
            "domain_pack": match["domain_pack"],
        },
        {
            "id": "lens",
            "title": "看见世界",
            "highlight": "对象必具名：sku:A / wh:W1，缺口在情境条上",
            "situation": layer.spec["situation"]["id"],
            "subjects": layer.spec["situation"]["subjects"],
            "objects": layer.spec["situation"]["objects"],
            "facts": facts,
            "gaps": ["ERP.on_hand=40 与 Excel.on_hand=52 未对齐"],
        },
        {
            "id": "intent",
            "title": "意图作曲",
            "highlight": "约束是芯片，改芯片即重编译，不是再聊一轮",
            "intent": layer.spec["intent"],
        },
        {
            "id": "plan",
            "title": "封闭计划",
            "highlight": "动作是卡片；未注册动作返回类型错误",
            "operations": runtime["plan"]["sio"]["operations"],
            "policy": runtime["plan"]["policy"],
            "type_error": type_error,
        },
        {
            "id": "stage",
            "title": "先演后做",
            "highlight": "Now ≠ Maybe：仿真不写事实",
            "now": {
                "on_hand": facts["on_hand"],
                "inbound": facts["inbound"],
                "stockout_risk": facts["stockout_risk"],
            },
            "maybe": {
                "expected_on_hand": projected["expected_on_hand"],
                "stockout_risk": projected["projected_stockout_risk"],
            },
            "writes_facts": runtime["simulate"]["writes_facts"],
            "meets_intent": runtime["simulate"]["meets_intent"],
        },
        {
            "id": "gate",
            "title": "门控写回",
            "highlight": "审批是托盘：无批准则 blocked",
            "blocked": runtime["blocked_without_approval"],
            "committed": {
                "status": runtime["committed_with_approval"]["status"],
                "purchase_order": runtime["committed_with_approval"]["facts"].get(
                    "purchase_order"
                ),
            },
        },
        {
            "id": "observe",
            "title": "世界回看",
            "highlight": "预测与观测叠合，闭环进入下一螺旋",
            "observe": runtime["observe"],
            "dikw": runtime["explain"]["dikw"],
            "explain": {
                "situation": runtime["explain"]["situation"],
                "intent": runtime["explain"]["intent"],
                "operations": runtime["explain"]["operations"],
            },
        },
    ]
    return {
        "product": "AWM",
        "tagline": "人与 Agent 共用的可操作世界",
        "loop": [
            "match",
            "lens",
            "intent",
            "plan",
            "stage",
            "gate",
            "observe",
        ],
        "match": match,
        "beats": beats,
        "audit": runtime["audit"],
    }


def write_artifacts(payload: Dict[str, Any]) -> None:
    LOOP_JSON.parent.mkdir(parents=True, exist_ok=True)
    DEMO_JS.parent.mkdir(parents=True, exist_ok=True)
    LOOP_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    DEMO_JS.write_text(
        "window.AWM_DEMO = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    data = build_closed_loop()
    write_artifacts(data)
    print(
        json.dumps(
            {"beats": data["loop"], "sku": data["match"]["sku"]}, ensure_ascii=False
        )
    )
