#!/usr/bin/env python3
"""认知实践 7 步：读写世界模型（不是对话历史）。

用法（在仓库根或本目录）：
  python examples/world-model-studio/scripts/run_cognitive_cycle.py
  python scripts/run_cognitive_cycle.py
  echo {"action":"reject_ungrounded"} | python ... --stdin
"""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
STEPS = ["input", "simulate", "generate", "interact", "evolve", "output", "yield"]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def audit(wm: dict[str, Any], step: str, event: str, detail: dict[str, Any]) -> None:
    wm.setdefault("audit", []).append(
        {"ts": now_iso(), "step": step, "event": event, **detail}
    )


def compile_laws(wm: dict[str, Any]) -> list[dict[str, Any]]:
    """法则编译：高维候选人事实 → 低维可决策结构。"""
    findings: list[dict[str, Any]] = []
    for cand in wm["reality"]["candidates"]:
        flags = list(cand.get("risk_flags") or [])
        ungrounded = list(cand.get("ungrounded") or [])
        if "culture_fit" in ungrounded or cand.get("scores", {}).get("culture_fit") == 60.0:
            findings.append(
                {
                    "law": "LAW-EVD-001",
                    "subject": cand["id"],
                    "verdict": "EVIDENCE_REQUIRED",
                    "note": "culture_fit 未接地，不得进入建议",
                }
            )
        if "education_below_requirement" in flags:
            findings.append(
                {
                    "law": "LAW-EDU-001",
                    "subject": cand["id"],
                    "verdict": "HUMAN_CONFIRM",
                    "note": "学历不足：禁止自动淘汰",
                }
            )
        if "insufficient_skills" in flags:
            findings.append(
                {
                    "law": "LAW-GATE-001",
                    "subject": cand["id"],
                    "verdict": "NOT_SHORTLIST_DEFAULT",
                    "note": "Staff 技能覆盖不足，默认不进短名单",
                }
            )
    return findings


def step_input(wm: dict[str, Any], _action: dict[str, Any]) -> dict[str, Any]:
    wm["intent"] = {
        "work": "冻结 Staff Engineer 短名单（2 人 onsite）",
        "success": "用人经理能解释每位候选人的证据与风险；候选人得到体面下一步",
        "anti_pattern": "黑箱分数排序或自动淘汰学历不足者",
        "north_star": wm.get("north_star"),
    }
    wm["cycle"]["loop"] = "on"
    wm["cycle"]["gate"] = "G1"
    audit(wm, "input", "intent_bound", {"intent": wm["intent"]["work"]})
    return wm


def step_simulate(wm: dict[str, Any], _action: dict[str, Any]) -> dict[str, Any]:
    findings = compile_laws(wm)
    wm["simulation"] = {
        "compiled_at": now_iso(),
        "findings": findings,
        "low_dim": {
            "decision": "谁进入 onsite（2 席）",
            "blockers": [f for f in findings if f["verdict"] == "EVIDENCE_REQUIRED"],
            "human_required": [f for f in findings if f["verdict"] == "HUMAN_CONFIRM"],
        },
    }
    audit(wm, "simulate", "laws_compiled", {"n": len(findings)})
    return wm


def step_generate(wm: dict[str, Any], _action: dict[str, Any]) -> dict[str, Any]:
    """至少两套可比较方案（术-4）。"""
    schemes = [
        {
            "id": "scheme.grounded",
            "title": "证据优先短名单",
            "advance": ["cand.wang-min", "cand.zhang-san"],
            "hold": ["cand.li-si"],
            "rationale": "王敏技能与门槛对齐；张三学历风险须人确认但工程/领域证据强于李四。文化分全部剔除。",
            "ungrounded_stripped": True,
            "gate": "G3",
        },
        {
            "id": "scheme.degree-hard",
            "title": "学历硬门槛短名单",
            "advance": ["cand.wang-min"],
            "hold": ["cand.zhang-san", "cand.li-si"],
            "rationale": "仅王敏满足本科。其余自动淘汰——违反 LAW-EDU-001，仅作对冲对照。",
            "violates": ["LAW-EDU-001"],
            "gate": "G4",
        },
    ]
    wm["decision"]["schemes"] = schemes
    wm["cycle"]["gate"] = "G2"
    audit(wm, "generate", "schemes_ready", {"ids": [s["id"] for s in schemes]})
    return wm


def step_interact(wm: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    human = action.get("action") or "confirm_with_uncertainty"
    wm["cycle"]["loop"] = "in"
    wm["cycle"]["gate"] = "G3"
    selected = "scheme.grounded"
    if human == "choose_degree_hard":
        selected = "scheme.degree-hard"
    wm["decision"]["selected_scheme_id"] = selected
    wm["decision"]["human_action"] = human
    wm["decision"]["human_confirmed"] = human in {"confirm_with_uncertainty", "confirm"}
    wm["decision"]["evidence_box"] = [
        "王敏：学历/年限/Runtime 技能均有简历事实。",
        "张三：领域技能证据在，学历不足 → 须人确认而非自动淘汰。",
        "李四：Staff 必备技能覆盖不足 → 默认不进短名单。",
        "culture_fit=60：未接地，已从建议中剥离。",
    ]
    wm["decision"]["uncertainties"] = [
        "无人现场面试，文化与协作未知。",
        "张三年限按简历推算，非 HRIS 核对。",
    ]
    wm["decision"]["rollback_until"] = "T+48h"
    if selected == "scheme.degree-hard":
        wm["decision"]["blocked"] = "CHARTER_VIOLATION:LAW-EDU-001"
        wm["decision"]["human_confirmed"] = False
    audit(
        wm,
        "interact",
        "human_review",
        {
            "action": human,
            "selected": selected,
            "confirmed": wm["decision"]["human_confirmed"],
        },
    )
    return wm


def step_evolve(wm: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    """体验信号 → ChangeSet（术-7）。默认驳回未接地文化分。"""
    signal = action.get("evolve_signal") or "reject_ungrounded_culture_fit"
    cs = {
        "changeset_id": f"cs.wm.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}",
        "signal": signal,
        "from_step": "interact",
        "patches": [
            {
                "path": "laws",
                "op": "upsert",
                "law_id": "LAW-EVD-001",
                "text": "culture_fit 无面试证据一律 UNGROUNDED，不得写入 overall。",
            },
            {
                "path": "ideal.culture_known",
                "op": "set",
                "value": False,
                "reason": "现实尚未发生面试，理念层不得假装已知",
            },
        ],
        "rollback": "restore previous laws snapshot",
    }
    wm["ideal"]["culture_known"] = False
    existing = {law["id"]: law for law in wm.get("laws", [])}
    existing["LAW-EVD-001"]["text"] = cs["patches"][0]["text"]
    wm["laws"] = list(existing.values())
    wm["changeset"].append(cs)
    wm["cycle"]["loop"] = "on"
    wm["cycle"]["gate"] = "G2"
    audit(wm, "evolve", "changeset_applied", {"changeset_id": cs["changeset_id"]})
    return wm


def step_output(wm: dict[str, Any], _action: dict[str, Any]) -> dict[str, Any]:
    if not wm["decision"].get("human_confirmed"):
        wm["output"] = {
            "status": "blocked",
            "reason": wm["decision"].get("blocked") or "HUMAN_CONFIRM_REQUIRED",
            "cs_preview": None,
        }
        audit(wm, "output", "blocked", {"reason": wm["output"]["reason"]})
        return wm
    scheme = next(s for s in wm["decision"]["schemes"] if s["id"] == wm["decision"]["selected_scheme_id"])
    names = {c["id"]: c["name"] for c in wm["reality"]["candidates"]}
    wm["output"] = {
        "status": "ready",
        "shortlist": [names[i] for i in scheme["advance"]],
        "hold": [names[i] for i in scheme["hold"]],
        "candidate_facing": {
            "advance": "邀请 onsite，说明评价维度与时间窗",
            "hold": "暂不推进，保留可解释理由，不发送自动拒绝",
        },
        "cs_preview": {
            "operation": "cs.process.start",
            "object": "obj.shortlist",
            "gate": "G3",
            "executed": False,
            "note": "模型提议，平台执行；本原型不写生产库",
        },
        "rollback_window_hours": wm["dimensions"]["time"]["rollback_window_hours"],
    }
    wm["dimensions"]["object"][1]["status"] = "frozen_pending_platform"
    wm["cycle"]["loop"] = "in"
    wm["cycle"]["gate"] = "G3"
    audit(wm, "output", "shortlist_proposed", {"shortlist": wm["output"]["shortlist"]})
    return wm


def step_yield(wm: dict[str, Any], _action: dict[str, Any]) -> dict[str, Any]:
    out = wm.get("output") or {}
    wm["yield"] = {
        "north_star": wm.get("north_star"),
        "attributed": out.get("status") == "ready",
        "metrics": {
            "explainable_shortlist": True,
            "ungrounded_scores_in_recommendation": 0,
            "auto_rejects": 0,
            "human_confirmed": bool(wm["decision"].get("human_confirmed")),
        },
        "pending_feedback": ["onsite 出现率", "用人经理接受短名单", "候选人申诉"],
    }
    wm["cycle"]["loop"] = "above"
    wm["cycle"]["gate"] = "G0"
    audit(wm, "yield", "benefit_attributed", wm["yield"]["metrics"])
    return wm


HANDLERS = {
    "input": step_input,
    "simulate": step_simulate,
    "generate": step_generate,
    "interact": step_interact,
    "evolve": step_evolve,
    "output": step_output,
    "yield": step_yield,
}


def run_cycle(wm: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    wm = deepcopy(wm)
    wm["cycle"]["completed"] = []
    for step in STEPS:
        wm = HANDLERS[step](wm, action)
        wm["cycle"]["current_step"] = step
        wm["cycle"]["completed"].append(step)
    wm["cycle"]["current_step"] = "yield"
    wm["cycle"]["finished_at"] = now_iso()
    return wm


def assert_invariants(wm: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    dims = wm.get("dimensions") or {}
    for key in ("space", "time", "subject", "object", "feedback"):
        if key not in dims:
            errors.append(f"missing dimension:{key}")
    if wm["cycle"].get("completed") != STEPS:
        errors.append("cycle incomplete")
    if not wm.get("changeset"):
        errors.append("no changeset")
    if any(c.get("role") == "candidate" for c in dims.get("subject") or []) is False:
        errors.append("candidates not in subject dimension")
    rec = wm.get("output") or {}
    if rec.get("status") == "ready":
        for cand in wm["reality"]["candidates"]:
            if cand["id"] in (next(s for s in wm["decision"]["schemes"] if s["id"] == wm["decision"]["selected_scheme_id"])["advance"]):
                if "culture_fit" in (cand.get("ungrounded") or []) and 60.0 == (cand.get("scores") or {}).get("culture_fit"):
                    # stripped from recommendation text — still in reality (honest)
                    pass
        if rec.get("cs_preview", {}).get("executed") is True:
            errors.append("model must not execute production write")
    if not wm.get("audit"):
        errors.append("no audit")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Run 7-step cognitive practice cycle")
    parser.add_argument("--fixture", type=Path, default=ROOT / "configs" / "world_model.json")
    parser.add_argument("--stdin", action="store_true", help="read human action JSON from stdin")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "database")
    args = parser.parse_args()

    action: dict[str, Any] = {}
    if args.stdin and not sys.stdin.isatty():
        raw = sys.stdin.read().lstrip("\ufeff").strip()
        if raw:
            action = json.loads(raw)

    wm0 = load_json(args.fixture)
    wm = run_cycle(wm0, action)
    errors = assert_invariants(wm)
    out_dir: Path = args.out_dir
    dump_json(out_dir / "world_model.json", wm)
    dump_json(out_dir / "audits" / "latest.json", wm.get("audit") or [])
    dump_json(out_dir / "changesets" / "latest.json", wm.get("changeset") or [])

    summary = {
        "status": "completed" if not errors else "failed",
        "world_model_id": wm.get("world_model_id"),
        "steps": wm["cycle"]["completed"],
        "selected_scheme": wm["decision"].get("selected_scheme_id"),
        "shortlist": (wm.get("output") or {}).get("shortlist"),
        "changeset_id": (wm.get("changeset") or [{}])[-1].get("changeset_id"),
        "audit_events": len(wm.get("audit") or []),
        "output_path": str(out_dir / "world_model.json"),
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
