#!/usr/bin/env python3
"""运行时空记忆匣最小可玩闭环：三件种子道具 + 穿梭/改写/抓取/融合。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lifewake.memory_chest import build_seeded_engine  # noqa: E402


def run_demo() -> dict:
    engine = build_seeded_engine()
    hairpin = engine.shuttle("item_moon_hairpin", "relive")
    rain = engine.shuttle("item_rain_scroll", "relive")
    city = engine.shuttle("item_city_compass", "relive")
    rewritten = engine.shuttle(
        "item_moon_hairpin",
        "rewrite",
        mutation="她这次先开口，把发卡放回你掌心，说：今晚我们把这座城走完。",
    )
    captured = engine.capture(
        rewritten["session_id"],
        fragment="掌心还留着发卡的温度，夜色地图在脚边慢慢展开。",
        item_type="story",
        title="发卡落下的下一句",
    )
    fused = engine.fuse(
        "item_moon_hairpin",
        "item_city_compass",
        "林妍走进夜色寻宝图",
    )
    snapshot = engine.snapshot()
    return {
        "ok": True,
        "slogan": snapshot["slogan"],
        "seed_items": ["item_moon_hairpin", "item_rain_scroll", "item_city_compass"],
        "relive": {
            "hairpin": hairpin["scene"]["title"],
            "rain": rain["scene"]["title"],
            "city": city["scene"]["title"],
        },
        "rewrite": {
            "child_item_id": rewritten["item_id"],
            "origin_preserved": rewritten["origin_preserved"],
            "parent_branch_id": rewritten["parent_branch_id"],
        },
        "captured": {
            "item_id": captured["item_id"],
            "title": captured["title"],
            "layer": captured["layer"],
        },
        "fused": {
            "item_id": fused["item_id"],
            "title": fused["title"],
            "is_real_memory": fused["is_real_memory"],
        },
        "invariants": {
            "origin_hairpin_intact": engine.origin_intact("item_moon_hairpin"),
            "origin_rain_intact": engine.origin_intact("item_rain_scroll"),
            "palace_rooms": snapshot["palace"]["room_count"],
            "branch_count": snapshot["graph"]["branch_count"],
            "item_count": len(snapshot["items"]),
        },
        "snapshot": snapshot,
    }


def render_markdown(result: dict) -> str:
    inv = result["invariants"]
    return "\n".join(
        [
            "# LifeWake · 时空记忆匣 Demo",
            "",
            f"> {result['slogan']}",
            "",
            "## 种子道具穿梭",
            f"- 月光发卡 → `{result['relive']['hairpin']}`",
            f"- 雨夜爵士回响卷轴 → `{result['relive']['rain']}`",
            f"- 城市寻宝罗盘 → `{result['relive']['city']}`",
            "",
            "## 改写（COW）",
            f"- 子道具：`{result['rewrite']['child_item_id']}`",
            f"- 原点保留：`{result['rewrite']['origin_preserved']}`",
            f"- 父分支：`{result['rewrite']['parent_branch_id']}`",
            "",
            "## 反向封装",
            f"- `{result['captured']['title']}`（{result['captured']['layer']}）",
            "",
            "## 跨界融合",
            f"- `{result['fused']['title']}` / 真实记忆标记={result['fused']['is_real_memory']}",
            "",
            "## 不变量",
            f"- 发卡原点完整：{inv['origin_hairpin_intact']}",
            f"- 卷轴原点完整：{inv['origin_rain_intact']}",
            f"- 宫殿房间：{inv['palace_rooms']}",
            f"- 时间线分支：{inv['branch_count']}",
            f"- 当前道具：{inv['item_count']}",
            "",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LifeWake 时空记忆匣 Demo")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args(argv)
    result = run_demo()
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, default=str))
    if args.write_report:
        reports = ROOT / "reports"
        reports.mkdir(parents=True, exist_ok=True)
        (reports / "memory_chest_demo.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        (reports / "memory_chest_demo.md").write_text(render_markdown(result), encoding="utf-8")
        db = ROOT / "database" / "runs"
        db.mkdir(parents=True, exist_ok=True)
        (db / "memory_chest_demo.json").write_text(
            json.dumps(
                {"run_id": "memory_chest_demo", "ok": True, "invariants": result["invariants"]},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    return 0 if result["ok"] and result["invariants"]["origin_hairpin_intact"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
