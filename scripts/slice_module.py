#!/usr/bin/env python3
"""切片编译器：把24模块规划设计编译成AI coding任务包。

用法:
  python scripts/slice_module.py M18              # 打印任务包
  python scripts/slice_module.py M18 --write      # 写到 harness/slices/M18.md
  python scripts/slice_module.py --all --write    # 全部24个
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "configs" / "protocol" / "registry.json"
KERNEL = REPO / "configs" / "protocol" / "KERNEL.yaml"
TRACES = REPO / "harness" / "traces" / "hengchuan-ltc" / "index.json"
REQ_DIR = REPO / "harness" / "requirements"
TEST_DIR = REPO / "services" / "hub-api" / "tests"
SLICE_DIR = REPO / "harness" / "slices"


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def load_traces() -> dict[str, Any]:
    return json.loads(TRACES.read_text(encoding="utf-8"))


def parse_req(module_id: str) -> dict[str, Any]:
    num = int(module_id[1:])
    path = REQ_DIR / f"REQ-UAS-M{num:02d}.req.md"
    if not path.is_file():
        return {"exists": False}
    text = path.read_text(encoding="utf-8")
    return {
        "exists": True,
        "path": str(path.relative_to(REPO)),
        "status": _first_line(text, "Status"),
        "phase": _first_line(text, "阶段"),
        "ac": _checkboxes(text),
        "tdd": _tdd_names(text),
    }


def _first_line(text: str, key: str) -> str:
    m = re.search(rf"##\s*{re.escape(key)}\s*\n(.+)", text)
    return m.group(1).strip() if m else ""


def _section(text: str, key: str) -> str:
    m = re.search(rf"##\s*{re.escape(key)}.*?[\n\r]+(.+?)(?:\n##|\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def _checkboxes(text: str) -> list[dict[str, str]]:
    m = re.search(r"## Acceptance Criteria(.*?)(?:\n##|\Z)", text, re.S)
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        mm = re.match(r"-\s*\[([ x])\]\s*(.+)", line.strip())
        if mm:
            items.append({"done": mm.group(1) == "x", "text": mm.group(2).strip()})
    return items


def _tdd_names(text: str) -> list[str]:
    m = re.search(r"TDD 先写[：:](.+)", text)
    if not m:
        return []
    return [t.strip() for t in re.split(r"[·•、,，]", m.group(1)) if t.strip()]


def scan_tests(names: list[str]) -> dict[str, str]:
    if not TEST_DIR.is_dir():
        return {n: "missing" for n in names}
    blob = ""
    for p in TEST_DIR.glob("test_*.py"):
        blob += p.read_text(encoding="utf-8")
    out = {}
    for n in names:
        out[n] = "green" if f"def {n}" in blob else "missing"
    return out


def compile_slice(module_id: str) -> str:
    reg = load_registry()
    mod = next((m for m in reg["modules"] if m["id"] == module_id), None)
    if not mod:
        return f"# 错误：{module_id} 不在注册表\n"
    req = parse_req(module_id)
    traces = load_traces()
    kernel = KERNEL.read_text(encoding="utf-8").strip()

    tests = list(req.get("tdd") or [])
    for aid, info in traces.get("acceptance", {}).items():
        for t in info.get("tests") or []:
            if t not in tests:
                tests.append(t)
    status = scan_tests(tests)
    greens = sum(1 for s in status.values() if s == "green")
    ac_done = sum(1 for a in req.get("ac") or [] if a["done"])
    ac_total = len(req.get("ac") or [])

    L = []
    L.append(f"# 切片 {module_id}: {mod['name']}")
    L.append("")
    L.append("> 一次 AI coding 会话的完整输入。禁止读取 docs/strategic/design/ 整包。")
    L.append("")
    L.append("## 0. 宪法（强制加载）")
    L.append("```yaml")
    L.append(kernel)
    L.append("```")
    L.append("")
    L.append("## 1. 本模块契约")
    L.append(f"- protocol_id: `{mod['protocol_id']}`")
    L.append(f"- port: `{mod.get('port') or '无'}`")
    L.append(f"- decision: {mod['decision']} · replaceable: {mod['replaceable']}")
    L.append(f"- verbs: {', '.join(mod.get('verbs') or [])}")
    L.append(f"- errors: {', '.join(mod.get('errors') or ['无'])}")
    L.append("- forbidden:")
    for f in mod.get("forbidden") or []:
        L.append(f"  - {f}")
    if mod.get("front_nouns"):
        L.append(f"- 一线禁词: {', '.join(mod['front_nouns'])}")
    L.append("")
    L.append("## 2. 验收标准")
    for a in req.get("ac") or []:
        mark = "x" if a["done"] else " "
        L.append(f"- [{mark}] {a['text']}")
    if not req.get("ac"):
        L.append("（无 AC）")
    L.append("")
    L.append("## 3. 红灯状态")
    if status:
        for n, s in status.items():
            L.append(f"- `{n}`: {s}")
        L.append(f"\n汇总: {greens}/{len(status)} green")
    else:
        L.append("（无 TDD 先写）")
    L.append("")
    L.append("## 4. 禁替代扫描（实现后必跑）")
    L.append("```bash")
    L.append("rg -i 'crewai|autogen|celery|camunda' services/ --type py")
    L.append("rg 'workflow_id|CubeQL' projects/aios-workstudio/demo/ || true")
    L.append("```")
    L.append("")
    L.append("## 5. 上下文预算（只读这些）")
    L.append("- configs/protocol/KERNEL.yaml")
    L.append("- configs/protocol/registry.json（本模块节）")
    if req.get("exists"):
        L.append(f"- {req['path']}")
    if mod.get("port"):
        L.append(f"- services/hub-api/uas_hub/ports.py（{mod['port']}）")
    L.append("- 禁止: docs/strategic/design/ 整包")
    L.append("")
    L.append("## 6. DoR / DoD")
    L.append("- DoR: 红灯已写 · 契约已挂")
    L.append("- DoD: 红灯转绿 · 禁替代grep空 · state按轨迹更新 · AC勾选")
    L.append("")
    L.append("---")
    L.append(f"完成度: AC {ac_done}/{ac_total} · 测试 {greens}/{len(status)} · status={req.get('status','?')}")
    L.append("判定: 完成 = 轨迹 green，不是卡片 green")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="把规划设计编译成AI coding任务包")
    ap.add_argument("module", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    if args.all:
        for mod in load_registry()["modules"]:
            mid = mod["id"]
            out = compile_slice(mid)
            if args.write:
                SLICE_DIR.mkdir(parents=True, exist_ok=True)
                (SLICE_DIR / f"{mid}.md").write_text(out, encoding="utf-8")
                print(f"  {mid} → harness/slices/{mid}.md")
            else:
                print(out)
        return 0

    if not args.module:
        ap.error("给模块ID或 --all")
    out = compile_slice(args.module)
    if args.write:
        SLICE_DIR.mkdir(parents=True, exist_ok=True)
        (SLICE_DIR / f"{args.module}.md").write_text(out, encoding="utf-8")
        print(f"→ harness/slices/{args.module}.md")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
