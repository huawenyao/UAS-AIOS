#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIO-MMOS/DIKW 语义操作层参考实现。

LLM 只应替换候选生成；本模块证明类型系统、门控、仿真与审计可在无模型时闭环。
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Dict, Iterable, List, Optional, Tuple

VALID_KINDS = {"query", "simulate", "assert", "act", "notify", "observe"}
RISK_RANK = {"low": 0, "medium": 1, "high": 2}


class SemanticOperationError(ValueError):
    """计划或世界状态违反 SIO/MMOS 契约。"""


def _index_by_id(items: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    indexed = {}
    for item in items:
        item_id = item.get("id")
        if not item_id:
            raise SemanticOperationError("subject/object missing id")
        if item_id in indexed:
            raise SemanticOperationError("duplicate id: {}".format(item_id))
        indexed[item_id] = item
    return indexed


def _require_keys(payload: Dict[str, Any], keys: Iterable[str], where: str) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise SemanticOperationError(
            "{} missing keys: {}".format(where, ", ".join(missing))
        )


class SemanticOperationLayer:
    """把意图编译为封闭动作类型上的 SIO 计划，并做仿真/门控执行。"""

    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self._validate_spec(spec)
        self.action_types = {item["id"]: item for item in spec["action_types"]}
        self.policies = spec.get("policies") or {
            "auto_execute_max_risk": "low",
            "deny_unregistered_actions": True,
            "predict_writes_facts": False,
        }
        self.audit: List[Dict[str, Any]] = []

    @classmethod
    def from_path(cls, path: str) -> "SemanticOperationLayer":
        with open(path, "r", encoding="utf-8") as handle:
            return cls(json.load(handle))

    def _validate_spec(self, spec: Dict[str, Any]) -> None:
        _require_keys(
            spec,
            ["version", "domain", "ontology", "situation", "intent", "action_types"],
            "spec",
        )
        ontology = spec["ontology"]
        _require_keys(ontology, ["classes", "relations"], "ontology")
        situation = spec["situation"]
        _require_keys(situation, ["id", "subjects", "objects", "facts"], "situation")
        _require_keys(
            spec["intent"], ["goal", "constraints", "success_metric"], "intent"
        )
        classes = set(ontology["classes"])
        objects = situation["objects"]
        for obj in objects:
            if obj.get("type") not in classes:
                raise SemanticOperationError(
                    "object {} has unregistered type {}".format(
                        obj.get("id"), obj.get("type")
                    )
                )
        _index_by_id(situation["subjects"])
        _index_by_id(objects)
        seen = set()
        for action in spec["action_types"]:
            _require_keys(action, ["id", "kind", "input_schema", "risk"], "action_type")
            if action["kind"] not in VALID_KINDS:
                raise SemanticOperationError("invalid kind: {}".format(action["kind"]))
            if action["id"] in seen:
                raise SemanticOperationError(
                    "duplicate action type: {}".format(action["id"])
                )
            seen.add(action["id"])

    def situation_ids(self) -> Tuple[set, set]:
        subjects = {item["id"] for item in self.spec["situation"]["subjects"]}
        objects = {item["id"] for item in self.spec["situation"]["objects"]}
        return subjects, objects

    def compile(
        self, requested_ops: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """编译 SIO 计划。默认按领域启发式生成补货计划。"""
        operations = (
            requested_ops if requested_ops is not None else self._default_plan()
        )
        plan = {
            "plan_id": "plan:{}".format(self.spec["situation"]["id"]),
            "domain": self.spec["domain"],
            "sio": {
                "situation": self.spec["situation"]["id"],
                "intent": self.spec["intent"],
                "operations": operations,
            },
            "validation": self.validate(operations),
            "policy": self.gate(operations),
        }
        self._audit("compile", plan["plan_id"], plan["validation"]["ok"])
        if not plan["validation"]["ok"]:
            raise SemanticOperationError(
                "plan invalid: {}".format("; ".join(plan["validation"]["errors"]))
            )
        return plan

    def _default_plan(self) -> List[Dict[str, Any]]:
        facts = self.spec["situation"]["facts"]
        sku_id = facts["sku_id"]
        warehouse_id = facts["warehouse_id"]
        supplier_id = facts["supplier_id"]
        quantity = int(facts.get("reorder_qty", 0))
        return [
            {
                "id": "step-1",
                "action": "query.stockout_risk",
                "input": {"sku_id": sku_id, "warehouse_id": warehouse_id},
            },
            {
                "id": "step-2",
                "action": "replenishment.create_purchase_order",
                "input": {
                    "sku_id": sku_id,
                    "warehouse_id": warehouse_id,
                    "supplier_id": supplier_id,
                    "quantity": quantity,
                },
            },
            {
                "id": "step-3",
                "action": "notify.procurement",
                "input": {"purchase_order_ref": "po:pending"},
            },
        ]

    def validate(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        errors: List[str] = []
        subject_ids, object_ids = self.situation_ids()
        known_ids = subject_ids | object_ids
        facts = self.spec["situation"]["facts"]
        intent = self.spec["intent"]
        deny_unregistered = self.policies.get("deny_unregistered_actions", True)

        for step in operations:
            action_id = step.get("action")
            if action_id not in self.action_types:
                if deny_unregistered:
                    errors.append("unregistered action: {}".format(action_id))
                continue
            action = self.action_types[action_id]
            payload = step.get("input") or {}
            for field in action.get("input_schema", {}):
                if field not in payload:
                    errors.append("{} missing input {}".format(action_id, field))
                    continue
                expected = action["input_schema"][field]
                value = payload[field]
                if (
                    expected == "id"
                    and value not in known_ids
                    and not str(value).startswith("po:")
                ):
                    errors.append("{} dangling ref {}".format(action_id, value))
                if expected == "positive_int":
                    if not isinstance(value, int) or value <= 0:
                        errors.append(
                            "{} quantity must be positive int".format(action_id)
                        )

            for cond in action.get("preconditions") or []:
                if cond == "stockout_risk > threshold":
                    if facts.get("stockout_risk", 0) <= facts.get("risk_threshold", 0):
                        errors.append(
                            "{} precondition failed: risk below threshold".format(
                                action_id
                            )
                        )
                elif cond == "budget_remaining >= estimated_cost":
                    unit_cost = facts.get("unit_cost", 0)
                    qty = payload.get("quantity", 0)
                    estimated = unit_cost * qty
                    budget = min(
                        facts.get("budget_remaining", 0),
                        intent.get("constraints", {}).get("max_budget", estimated),
                    )
                    if estimated > budget:
                        errors.append(
                            "{} exceeds budget ({} > {})".format(
                                action_id, estimated, budget
                            )
                        )

        return {"ok": not errors, "errors": errors}

    def gate(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        max_auto = RISK_RANK[self.policies.get("auto_execute_max_risk", "low")]
        decisions = []
        for step in operations:
            action = self.action_types.get(step.get("action"))
            if not action:
                decisions.append(
                    {
                        "step": step.get("id"),
                        "decision": "deny",
                        "reason": "unregistered",
                    }
                )
                continue
            needs_approval = (
                bool(action.get("approval")) or RISK_RANK[action["risk"]] > max_auto
            )
            if action["kind"] in {"query", "simulate", "observe"}:
                decision = "allow"
            elif needs_approval:
                decision = "escalate"
            else:
                decision = "allow"
            decisions.append(
                {
                    "step": step.get("id"),
                    "action": action["id"],
                    "decision": decision,
                    "risk": action["risk"],
                    "kind": action["kind"],
                }
            )
        return {"steps": decisions}

    def simulate(self, plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        plan = plan or self.compile()
        if self.policies.get("predict_writes_facts"):
            raise SemanticOperationError(
                "policy violation: PREDICT must not write facts"
            )
        world = deepcopy(self.spec["situation"]["facts"])
        projected = []
        for step in plan["sio"]["operations"]:
            action = self.action_types[step["action"]]
            if action["kind"] == "act" and action["id"].endswith(
                "create_purchase_order"
            ):
                qty = step["input"]["quantity"]
                world["expected_on_hand"] = (
                    world.get("on_hand", 0) + world.get("inbound", 0) + qty
                )
                demand = world.get("forecast_demand_14d", 0)
                world["projected_stockout_risk"] = (
                    0.0 if world["expected_on_hand"] >= demand else 0.2
                )
                projected.append(
                    {"step": step["id"], "effect": "expected_on_hand+={}".format(qty)}
                )
            elif action["kind"] == "query":
                projected.append(
                    {
                        "step": step["id"],
                        "effect": "stockout_risk={}".format(world.get("stockout_risk")),
                    }
                )
            else:
                projected.append({"step": step["id"], "effect": "notify"})
        result = {
            "mode": "simulate",
            "writes_facts": False,
            "projected_facts": world,
            "trace": projected,
            "meets_intent": world.get("projected_stockout_risk", 1.0) < 0.05,
        }
        self._audit("simulate", plan["plan_id"], True)
        return result

    def execute(
        self, plan: Optional[Dict[str, Any]] = None, approved: bool = False
    ) -> Dict[str, Any]:
        plan = plan or self.compile()
        blocked = [
            item
            for item in plan["policy"]["steps"]
            if item["decision"] == "escalate" and not approved
        ]
        if blocked:
            result = {
                "mode": "execute",
                "status": "blocked",
                "reason": "approval required",
                "blocked_steps": blocked,
            }
            self._audit("execute", plan["plan_id"], False)
            return result
        simulation = self.simulate(plan)
        committed = deepcopy(self.spec["situation"]["facts"])
        committed["purchase_order"] = {
            "status": "created",
            "quantity": plan["sio"]["operations"][1]["input"]["quantity"],
        }
        committed["expected_on_hand"] = simulation["projected_facts"][
            "expected_on_hand"
        ]
        result = {
            "mode": "execute",
            "status": "committed",
            "facts": committed,
            "simulation": simulation,
        }
        self._audit("execute", plan["plan_id"], True)
        return result

    def explain(self, plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        plan = plan or self.compile()
        sim = self.simulate(plan)
        return {
            "situation": plan["sio"]["situation"],
            "intent": plan["sio"]["intent"]["goal"],
            "operations": [step["action"] for step in plan["sio"]["operations"]],
            "why_legal": plan["validation"],
            "why_gated": plan["policy"],
            "predicted_effect": sim["projected_facts"].get("projected_stockout_risk"),
            "dikw": self.dikw_score(plan, sim),
        }

    def dikw_score(
        self, plan: Dict[str, Any], simulation: Dict[str, Any]
    ) -> Dict[str, Any]:
        facts = self.spec["situation"]["facts"]
        required = [
            "sku_id",
            "on_hand",
            "forecast_demand_14d",
            "stockout_risk",
            "budget_remaining",
        ]
        data_coverage = sum(1 for key in required if key in facts) / float(
            len(required)
        )
        info_ok = plan["validation"]["ok"]
        knowledge_ok = all(
            obj["type"] in self.spec["ontology"]["classes"]
            for obj in self.spec["situation"]["objects"]
        )
        wisdom_ok = simulation.get("meets_intent") and all(
            item["decision"] != "deny" for item in plan["policy"]["steps"]
        )
        return {
            "data": round(data_coverage, 3),
            "information": 1.0 if info_ok else 0.0,
            "knowledge": 1.0 if knowledge_ok else 0.0,
            "wisdom": 1.0 if wisdom_ok else 0.0,
            "publishable": bool(info_ok and knowledge_ok and data_coverage == 1.0),
        }

    def _audit(self, op: str, plan_id: str, ok: bool) -> None:
        self.audit.append({"op": op, "plan_id": plan_id, "ok": ok})


def run_replenishment_demo(spec_path: str) -> Dict[str, Any]:
    layer = SemanticOperationLayer.from_path(spec_path)
    plan = layer.compile()
    simulated = layer.simulate(plan)
    blocked = layer.execute(plan, approved=False)
    committed = layer.execute(plan, approved=True)
    explained = layer.explain(plan)
    return {
        "domain": layer.spec["domain"],
        "plan": plan,
        "simulate": simulated,
        "blocked_without_approval": blocked,
        "committed_with_approval": committed,
        "explain": explained,
        "audit": layer.audit,
    }


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Run SIO semantic operation demo")
    parser.add_argument(
        "--spec",
        default=str(
            Path(__file__).resolve().parents[1]
            / "examples"
            / "semantic-operation-layer"
            / "replenishment_sio.json"
        ),
    )
    args = parser.parse_args()
    print(json.dumps(run_replenishment_demo(args.spec), ensure_ascii=False, indent=2))
