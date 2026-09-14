"""时空记忆匣：三位一体闭环与治理红线。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lifewake import capabilities  # noqa: E402
from lifewake.memory_chest import (  # noqa: E402
    ChestError,
    MemoryChestEngine,
    build_seeded_engine,
)


SEED_IDS = ("item_moon_hairpin", "item_rain_scroll", "item_city_compass")


@pytest.fixture
def engine() -> MemoryChestEngine:
    capabilities.reset_chest_engine()
    return build_seeded_engine()


class TestSeedLoop:
    def test_three_origin_items_and_palace_wings(self, engine: MemoryChestEngine):
        snap = engine.snapshot()
        ids = {item["item_id"] for item in snap["items"]}
        assert set(SEED_IDS) <= ids
        wings = snap["palace"]["wings"]
        assert "现实记忆层" in wings
        assert "幻想故事层" in wings
        grown = [
            room
            for rooms in wings.values()
            for room in rooms
            if room.get("grown_from_item") == "item_moon_hairpin"
        ]
        assert grown, "high-weight 信物必须增量长出专属锚点"

    def test_relive_does_not_fork_origin(self, engine: MemoryChestEngine):
        before = engine.graph.branches["br_linyan_origin"].readonly
        session = engine.shuttle("item_moon_hairpin", "relive")
        assert session["readonly"] is True
        assert session["mode"] == "relive"
        assert engine.origin_intact("item_moon_hairpin")
        assert engine.graph.branches["br_linyan_origin"].readonly is before
        assert session["scene"]["alive_characters"]

    def test_rewrite_uses_copy_on_write(self, engine: MemoryChestEngine):
        origin_inscription = engine.items["item_moon_hairpin"].inscription
        session = engine.shuttle(
            "item_moon_hairpin",
            "rewrite",
            mutation="她这次先开口，把发卡放回你掌心。",
        )
        assert session["origin_preserved"] is True
        assert session["item_id"] != "item_moon_hairpin"
        child = engine.items[session["item_id"]]
        assert child.is_real_memory is False
        assert child.layer == "fantasy"
        assert engine.items["item_moon_hairpin"].inscription == origin_inscription
        assert engine.origin_intact("item_moon_hairpin")
        parent = engine.graph.branches[session["parent_branch_id"]]
        assert parent.readonly and parent.is_real_memory

    def test_capture_from_scene_creates_fantasy_item(self, engine: MemoryChestEngine):
        session = engine.shuttle("item_rain_scroll", "relive")
        captured = engine.capture(
            session["session_id"],
            fragment="雨停之后，爵士主题还停在杯沿。",
            item_type="emotion",
            title="雨停后的余韵",
        )
        assert captured["is_real_memory"] is False
        assert captured["layer"] == "fantasy"
        assert captured["item_type"] == "emotion"

    def test_fuse_real_memories_downgrades_to_fantasy(self, engine: MemoryChestEngine):
        fused = engine.fuse(
            "item_moon_hairpin",
            "item_city_compass",
            "古风人物走进夜色寻宝图",
        )
        assert fused["is_real_memory"] is False
        assert fused["layer"] == "fantasy"
        assert "item_moon_hairpin" in fused["derived_from"]
        assert engine.origin_intact("item_moon_hairpin")


class TestGovernance:
    def test_missing_rewrite_scope_blocked(self):
        engine = MemoryChestEngine(
            person_id="person_ada",
            consent={
                "consent_id": "c",
                "person_id": "person_ada",
                "scopes": ["memory.revisit"],
                "purpose": "create_for_user",
                "status": "granted",
                "withdrawable": True,
                "expires_at": "2027-01-01",
            },
        )
        engine.load_seed()
        engine.consent = {
            "consent_id": "c",
            "person_id": "person_ada",
            "scopes": ["memory.revisit"],
            "purpose": "create_for_user",
            "status": "granted",
            "withdrawable": True,
            "expires_at": "2027-01-01",
        }
        with pytest.raises(ChestError) as exc:
            engine.shuttle("item_moon_hairpin", "rewrite", mutation="改写")
        assert exc.value.code == "CONSENT_REQUIRED"

    def test_revoked_consent_blocks_itemize(self, engine: MemoryChestEngine):
        engine.consent = {**engine.consent, "status": "revoked"}
        with pytest.raises(ChestError) as exc:
            engine.itemize(
                source_text="一段不该再被处理的记忆",
                item_type="story",
                title="撤回后",
                is_real_memory=True,
            )
        assert exc.value.code == "CONSENT_REVOKED"

    def test_real_item_cannot_sit_on_fantasy_layer(self):
        from lifewake.memory_chest import ChestItem

        with pytest.raises(ChestError) as layer_exc:
            ChestItem(
                item_id="bad",
                item_type="story",
                title="bad",
                vessel="剧情卷轴",
                inscription="x",
                is_real_memory=True,
                layer="fantasy",
                source_timeline_id="t",
                parallel_branch_id="b",
                entity_graph_ref="n",
                person_id="p",
            )
        assert layer_exc.value.code == "LAYER_ISOLATION"

    def test_sealed_item_cannot_fuse(self, engine: MemoryChestEngine):
        engine.seal("item_rain_scroll")
        with pytest.raises(ChestError) as exc:
            engine.fuse("item_rain_scroll", "item_city_compass", "不该合成")
        assert exc.value.code == "ITEM_SEALED"


class TestCapabilities:
    def test_weave_shuttle_capture_via_lw(self, engine: MemoryChestEngine):
        capabilities.reset_chest_engine()
        reg = capabilities.build_registry()
        weave = reg.invoke(
            capabilities.CapabilityCall(
                capability="lw.memory.weave",
                trace_id="chest-1",
                inputs={
                    "source_text": "第一次把心跳编进唱片的夜晚",
                    "item_type": "emotion",
                    "title": "心跳唱片残片",
                    "is_real_memory": False,
                },
            )
        )
        assert weave.is_success()
        item_id = weave.result["item_id"]
        shuttle = reg.invoke(
            capabilities.CapabilityCall(
                capability="lw.memory.shuttle",
                trace_id="chest-2",
                inputs={"item_id": item_id, "mode": "relive"},
            )
        )
        assert shuttle.is_success()
        capture = reg.invoke(
            capabilities.CapabilityCall(
                capability="lw.memory.capture",
                trace_id="chest-3",
                inputs={
                    "session_id": shuttle.result["session_id"],
                    "fragment": "唱针落下，心跳变成可携带的宝石。",
                    "item_type": "emotion",
                    "title": "唱针光斑",
                },
            )
        )
        assert capture.is_success()
        palace = reg.invoke(
            capabilities.CapabilityCall(capability="lw.palace.snapshot", trace_id="chest-4")
        )
        assert palace.result["graph"]["branch_count"] >= 1

    def test_end_to_end_demo_payload_serializable(self, engine: MemoryChestEngine):
        relive = engine.shuttle("item_city_compass", "relive")
        rewrite = engine.shuttle(
            "item_city_compass",
            "continue",
            mutation="罗盘指向心跳唱片，巷口出现一张未写完的菜单。",
        )
        captured = engine.capture(
            rewrite["session_id"],
            fragment="菜单上出现月光晚餐的第一道菜。",
            title="未写完的菜单",
        )
        fused = engine.fuse("item_moon_hairpin", "item_rain_scroll", "月光下的爵士窗台")
        payload = {
            "relive": relive,
            "rewrite": rewrite,
            "captured": captured,
            "fused": fused,
            "snapshot": engine.snapshot(),
        }
        dumped = json.dumps(payload, ensure_ascii=False, default=str)
        assert "item_moon_hairpin" in dumped
        assert engine.origin_intact("item_moon_hairpin")
        assert engine.origin_intact("item_rain_scroll")
