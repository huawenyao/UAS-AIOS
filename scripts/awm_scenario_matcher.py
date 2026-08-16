#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AWM 场景匹配器：用 SIO-MMOS/DIKW 结构信号推荐 SKU 与 UX 模式。"""

from __future__ import annotations

import json
from typing import Any, Dict, List

DOMAIN_PACKS = {
    "replenishment": "inventory_replenishment",
    "inventory": "inventory_replenishment",
    "sales": "enterprise_sales_os",
    "quote": "enterprise_sales_os",
    "cs": "customer_service",
    "ticket": "customer_service",
    "recruitment": "ai_recruitment",
    "hiring": "ai_recruitment",
    "personal": "selfpaw_personal_world",
    "selfpaw": "selfpaw_personal_world",
}

SKU_RANK = {"none": 0, "lens": 1, "stage": 2, "gate": 3}


class ScenarioMatchError(ValueError):
    """Brief 不足以做匹配。"""


def _pack_for(domain_hint: str) -> str:
    hint = (domain_hint or "").lower()
    for key, pack in DOMAIN_PACKS.items():
        if key in hint:
            return pack
    return "generic_ops"


def match_brief(brief: Dict[str, Any]) -> Dict[str, Any]:
    for key in (
        "id",
        "domain_hint",
        "subjects",
        "named_objects",
        "hard_constraints",
        "executable_actions",
    ):
        if key not in brief:
            raise ScenarioMatchError("brief missing {}".format(key))

    subjects = list(brief.get("subjects") or [])
    objects = list(brief.get("named_objects") or [])
    identified = [item for item in objects if item.get("has_system_id")]
    constraints = list(brief.get("hard_constraints") or [])
    actions = list(brief.get("executable_actions") or [])
    writeback = list(brief.get("writeback_systems") or [])
    feedback_hours = brief.get("feedback_hours")
    data_sources = int(brief.get("data_sources") or 0)
    asked = brief.get("asked_autonomy") or "suggest"
    customer_type = brief.get("customer_type") or "enterprise_ops"
    has_approver = bool(brief.get("has_approver"))
    has_compensation = bool(brief.get("has_compensation"))
    irreversible = bool(brief.get("irreversible_actions"))

    s_score = 0.0
    if len(subjects) >= 2:
        s_score += 0.4
    if len(subjects) >= 3:
        s_score += 0.2
    if identified:
        s_score += 0.4 * min(1.0, len(identified) / 3.0)
    s_score = min(1.0, s_score)

    i_score = 0.0
    if constraints:
        i_score += 0.6
    if brief.get("success_metric"):
        i_score += 0.4
    i_score = min(1.0, i_score)

    o_score = 0.0
    if actions:
        o_score += 0.5
    if writeback:
        o_score += 0.3
    if feedback_hours is not None and feedback_hours <= 72:
        o_score += 0.2
    o_score = min(1.0, o_score)

    dikw = {
        "data": min(1.0, data_sources / 2.0) if data_sources else 0.0,
        "information": 1.0 if identified else 0.0,
        "knowledge": 1.0 if constraints and actions else 0.0,
        "wisdom": 1.0 if has_approver or not writeback else 0.0,
    }

    reasons: List[str] = []
    sku = "none"
    ux_mode = "lens"
    out_of_scope: List[str] = [
        "全自主替代部门",
        "未登记动作直连生产",
        "把预测当事实写入",
    ]

    if s_score < 0.4 or not identified:
        sku = "lens"
        ux_mode = "lens"
        reasons.append("对象身份不足：先做 Lens，把带 ID 的客体对齐")
    elif i_score < 0.6 or not constraints:
        sku = "lens"
        ux_mode = "lens"
        reasons.append("意图不可计算：补硬约束与成功度量后再上 Stage")
    else:
        sku = "stage"
        ux_mode = "stage"
        reasons.append("情境与意图可计算：进入 Stage，用推演证明价值")
        if writeback and actions and dikw["data"] >= 0.5:
            if asked == "full" and (irreversible and not has_compensation):
                reasons.append("客户要全自主但不可逆动作无补偿：拒绝 Gate，停留 Stage")
                out_of_scope.append("无补偿的不可逆自动执行")
            elif (
                has_approver
                and (has_compensation or not irreversible)
                and feedback_hours is not None
                and feedback_hours <= 72
            ):
                sku = "gate"
                ux_mode = "gate"
                reasons.append("具备审批、反馈与补偿/可逆性：可签 Gate")
            elif writeback:
                reasons.append("有写回但审批或反馈不完整：Stage 为主，Gate 不进合同")

    if customer_type == "individual":
        ux_mode = "selfpaw"
        if sku == "gate" and asked == "full":
            sku = "stage"
            reasons.append("个人侧默认草稿/日历门控，不开放静默外发")
        out_of_scope.append("静默群发与跨人代理无确认")

    if asked == "full" and sku != "gate":
        reasons.append("所求自治高于世界成熟度：合同写明降级 SKU")

    first_objects = [item["name"] for item in objects[:8]]
    first_actions = actions[:10]
    overall = round((s_score + i_score + o_score + sum(dikw.values()) / 4.0) / 4.0, 3)

    return {
        "brief_id": brief["id"],
        "match_score": overall,
        "sio": {
            "situation": round(s_score, 3),
            "intent": round(i_score, 3),
            "operation": round(o_score, 3),
        },
        "dikw": {key: round(value, 3) for key, value in dikw.items()},
        "sku": sku,
        "ux_mode": ux_mode,
        "domain_pack": _pack_for(brief.get("domain_hint", "")),
        "first_objects": first_objects,
        "first_actions": first_actions,
        "reasons": reasons,
        "out_of_scope": out_of_scope,
        "publish_gate": sku == "gate",
        "sku_rank": SKU_RANK[sku],
    }


def match_path(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return match_brief(json.load(handle))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Match an AWM customer brief to SKU and UX mode"
    )
    parser.add_argument("--brief", required=True)
    args = parser.parse_args()
    print(json.dumps(match_path(args.brief), ensure_ascii=False, indent=2))
