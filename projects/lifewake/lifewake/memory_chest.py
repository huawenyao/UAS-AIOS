"""时空记忆匣 — LifeWake Memory P1 核心引擎。

产品定位：不是第三产品轨，也不是任务驱动开放世界。
它把 Keepsake Vault 空间化为记忆宫殿，把纪念物升级为可溯源道具，
把「记忆时光机」实现为双向穿梭（物品→场景 / 场景→物品）。

机制与表达解耦（MED）：
- 机制固定：物品化、穿梭、抓取、COW 分支、宫殿增量生长、资产治理
- 表达可变：场景文案、铭文、角色状态由图谱填充，模型只做演绎不得改写事实

事实源是叙事图谱，不是 LLM 上下文窗口。
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from .domain import ALLOWED_PURPOSE, DomainError

ItemType = Literal["character", "story", "scene", "emotion"]
PalaceLayer = Literal["real_memory", "fantasy", "history", "future"]
ShuttleMode = Literal["relive", "rewrite", "continue"]
ItemWeight = Literal["low", "medium", "high"]

PREFABS: dict[str, dict[str, Any]] = {
    "character": {
        "vessel": "人物信物",
        "interact": ("wake", "shuttle", "archive"),
    },
    "story": {
        "vessel": "剧情卷轴",
        "interact": ("read", "shuttle", "capture"),
    },
    "scene": {
        "vessel": "场景罗盘",
        "interact": ("enter", "shuttle"),
    },
    "emotion": {
        "vessel": "情绪宝石",
        "interact": ("attune", "shuttle"),
    },
}

REQUIRED_CHEST_SCOPES = {
    "itemize": ("memory.itemize",),
    "relive": ("memory.revisit",),
    "rewrite": ("memory.rewrite",),
    "continue": ("memory.rewrite",),
    "capture": ("memory.itemize",),
    "fuse": ("memory.itemize", "memory.rewrite"),
}

SEED_PATH = Path(__file__).resolve().parents[1] / "configs" / "memory_chest_seed.json"


class ChestError(DomainError):
    """记忆匣不变量违反。"""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _new_id(prefix: str, *parts: str) -> str:
    raw = ":".join(parts)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}_{digest}"


def _require_consent(consent: dict[str, Any], scopes: tuple[str, ...]) -> None:
    if not consent:
        raise ChestError("CONSENT_REQUIRED", "memory chest requires consent")
    if consent.get("purpose") != ALLOWED_PURPOSE:
        raise ChestError("POLICY_DENIED", "purpose must be create_for_user")
    if consent.get("status") != "granted":
        raise ChestError("CONSENT_REVOKED", "consent is not granted")
    if consent.get("withdrawable") is False:
        raise ChestError("POLICY_DENIED", "consent must be withdrawable")
    granted = set(consent.get("scopes") or [])
    missing = [s for s in scopes if s not in granted]
    if missing:
        raise ChestError("CONSENT_REQUIRED", f"missing scopes: {missing}")


@dataclass
class GraphNode:
    node_id: str
    kind: str
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    is_real_memory: bool = False
    readonly: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GraphEdge:
    edge_id: str
    src: str
    dst: str
    rel: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TimelineBranch:
    branch_id: str
    timeline_id: str
    parent_branch_id: str | None
    layer: PalaceLayer
    is_real_memory: bool
    readonly: bool
    label: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class NarrativeGraph:
    """叙事因果图谱：穿梭、人物 Alive、剧情生成的唯一事实源。"""

    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}
        self.edges: dict[str, GraphEdge] = {}
        self.branches: dict[str, TimelineBranch] = {}
        self.membership: dict[str, set[str]] = {}  # branch_id -> node_ids

    def add_node(self, node: GraphNode, branch_id: str) -> None:
        existing = self.nodes.get(node.node_id)
        if existing is None:
            self.nodes[node.node_id] = node
        elif node.is_real_memory or node.readonly:
            # 真实/只读节点优先，避免幻想场景覆写原点人格。
            self.nodes[node.node_id] = GraphNode(
                node_id=existing.node_id,
                kind=existing.kind,
                name=existing.name,
                payload=existing.payload,
                is_real_memory=existing.is_real_memory or node.is_real_memory,
                readonly=existing.readonly or node.readonly,
            )
        self.membership.setdefault(branch_id, set()).add(node.node_id)

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges[edge.edge_id] = edge

    def add_branch(self, branch: TimelineBranch) -> None:
        self.branches[branch.branch_id] = branch
        self.membership.setdefault(branch.branch_id, set())

    def nodes_in(self, branch_id: str) -> list[GraphNode]:
        ids = self.membership.get(branch_id, set())
        return [self.nodes[i] for i in sorted(ids) if i in self.nodes]

    def clone_branch(
        self, source_branch_id: str, new_branch_id: str, *, label: str
    ) -> TimelineBranch:
        source = self.branches.get(source_branch_id)
        if source is None:
            raise ChestError("BRANCH_NOT_FOUND", f"unknown branch {source_branch_id}")
        cloned = TimelineBranch(
            branch_id=new_branch_id,
            timeline_id=source.timeline_id,
            parent_branch_id=source.branch_id,
            layer="fantasy" if source.is_real_memory else source.layer,
            is_real_memory=False,
            readonly=False,
            label=label,
        )
        self.add_branch(cloned)
        for node in self.nodes_in(source_branch_id):
            replica = copy.deepcopy(node)
            replica.readonly = False
            replica.is_real_memory = False
            replica.node_id = f"{node.node_id}@{new_branch_id}"
            replica.payload = {
                **replica.payload,
                "cloned_from": node.node_id,
                "branch_id": new_branch_id,
            }
            self.add_node(replica, new_branch_id)
        for edge in list(self.edges.values()):
            if edge.src in self.membership.get(
                source_branch_id, set()
            ) or edge.dst in self.membership.get(source_branch_id, set()):
                self.add_edge(
                    GraphEdge(
                        edge_id=f"{edge.edge_id}@{new_branch_id}",
                        src=f"{edge.src}@{new_branch_id}"
                        if edge.src in self.membership.get(source_branch_id, set())
                        else edge.src,
                        dst=f"{edge.dst}@{new_branch_id}"
                        if edge.dst in self.membership.get(source_branch_id, set())
                        else edge.dst,
                        rel=edge.rel,
                    )
                )
        return cloned

    def assert_consistent(self, spec: dict[str, Any], branch_id: str) -> None:
        """图谱优先：生成内容不得与只读原点事实冲突。"""
        allowed_names = {n.name for n in self.nodes_in(branch_id)}
        for character in spec.get("characters", []):
            node = self.nodes.get(character) or next(
                (n for n in self.nodes_in(branch_id) if n.payload.get("cloned_from") == character),
                None,
            )
            if node is None and character not in allowed_names:
                raise ChestError(
                    "NARRATIVE_INCONSISTENT",
                    f"character {character} is not in branch {branch_id}",
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges.values()],
            "branches": [b.to_dict() for b in self.branches.values()],
            "membership": {k: sorted(v) for k, v in self.membership.items()},
        }


@dataclass
class ChestItem:
    item_id: str
    item_type: ItemType
    title: str
    vessel: str
    inscription: str
    is_real_memory: bool
    layer: PalaceLayer
    source_timeline_id: str
    parallel_branch_id: str
    entity_graph_ref: str
    person_id: str
    weight: ItemWeight = "medium"
    user_edit_note: str = ""
    sealed: bool = False
    archived: bool = False
    atmosphere: str = ""
    scene: dict[str, Any] = field(default_factory=dict)
    derived_from: tuple[str, ...] = ()
    consent_ref: str = ""

    def __post_init__(self) -> None:
        if self.item_type not in PREFABS:
            raise ChestError("VALIDATION_ERROR", f"unknown item_type {self.item_type}")
        if self.is_real_memory and self.layer != "real_memory":
            raise ChestError(
                "LAYER_ISOLATION",
                "real memory items must live on the real_memory layer",
            )
        if self.layer == "real_memory" and not self.is_real_memory:
            raise ChestError(
                "LAYER_ISOLATION",
                "fantasy/derived items cannot occupy the real_memory layer",
            )

    def provenance(self) -> dict[str, Any]:
        prefab = PREFABS[self.item_type]
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "vessel": self.vessel or prefab["vessel"],
            "source_timeline_id": self.source_timeline_id,
            "parallel_branch_id": self.parallel_branch_id,
            "entity_graph_ref": self.entity_graph_ref,
            "is_real_memory": self.is_real_memory,
            "layer": self.layer,
            "user_edit_note": self.user_edit_note,
            "derived_from": list(self.derived_from),
            "sealed": self.sealed,
            "archived": self.archived,
        }

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["provenance"] = self.provenance()
        data["interact"] = list(PREFABS[self.item_type]["interact"])
        return data


@dataclass
class PalaceRoom:
    room_id: str
    wing: str
    layer: PalaceLayer
    title: str
    item_ids: list[str] = field(default_factory=list)
    grown_from_item: str | None = None
    template: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MemoryPalace:
    """分层记忆宫殿：底层拓扑模板 + 高权重信物增量生长。"""

    def __init__(self, templates: dict[str, Any] | None = None) -> None:
        self.rooms: dict[str, PalaceRoom] = {}
        templates = templates or {}
        for layer, spec in templates.items():
            wing = spec["wing"]
            for title in spec.get("rooms", []):
                room_id = _new_id("room", layer, title)
                self.rooms[room_id] = PalaceRoom(
                    room_id=room_id,
                    wing=wing,
                    layer=layer,  # type: ignore[arg-type]
                    title=title,
                    template=True,
                )

    def assign(self, item: ChestItem) -> PalaceRoom:
        candidates = [r for r in self.rooms.values() if r.layer == item.layer and r.template]
        if not candidates:
            raise ChestError("PALACE_LAYER_MISSING", f"no template for {item.layer}")
        preferred = {
            "character": "人物回廊",
            "story": "人生展厅",
            "scene": "创世工坊" if item.layer == "fantasy" else "时间栈厅",
            "emotion": "情绪井",
        }.get(item.item_type, candidates[0].title)
        room = next((r for r in candidates if r.title == preferred), candidates[0])
        if item.item_id not in room.item_ids:
            room.item_ids.append(item.item_id)
        if item.weight == "high" and item.item_id:
            grown_id = _new_id("room", item.layer, item.item_id)
            if grown_id not in self.rooms:
                self.rooms[grown_id] = PalaceRoom(
                    room_id=grown_id,
                    wing=room.wing,
                    layer=item.layer,
                    title=f"{item.title}专属锚点",
                    item_ids=[item.item_id],
                    grown_from_item=item.item_id,
                    template=False,
                )
            return self.rooms[grown_id]
        return room

    def to_dict(self) -> dict[str, Any]:
        wings: dict[str, list[dict[str, Any]]] = {}
        for room in self.rooms.values():
            wings.setdefault(room.wing, []).append(room.to_dict())
        return {"wings": wings, "room_count": len(self.rooms)}


class MemoryChestEngine:
    """三位一体运行时：宫殿 + 百宝箱 + 穿梭机。"""

    def __init__(self, *, person_id: str, consent: dict[str, Any]) -> None:
        self.person_id = person_id
        self.consent = consent
        self.graph = NarrativeGraph()
        self.palace = MemoryPalace()
        self.items: dict[str, ChestItem] = {}
        self.sessions: dict[str, dict[str, Any]] = {}
        self.audit: list[dict[str, Any]] = []

    def _audit(self, event: str, payload: dict[str, Any]) -> None:
        self.audit.append({"event": event, "payload": payload})

    def load_seed(self, seed: dict[str, Any] | None = None) -> dict[str, Any]:
        seed = seed or json.loads(SEED_PATH.read_text(encoding="utf-8"))
        self.consent = seed.get("consent", self.consent)
        self.person_id = seed.get("person_id", self.person_id)
        self.palace = MemoryPalace(seed.get("palace_templates"))
        for entity in seed.get("entities", []):
            pass  # nodes bound per branch below
        for raw in seed.get("items", []):
            branch = TimelineBranch(
                branch_id=raw["parallel_branch_id"],
                timeline_id=raw["source_timeline_id"],
                parent_branch_id=None,
                layer=raw["layer"],
                is_real_memory=raw["is_real_memory"],
                readonly=bool(raw["is_real_memory"]),
                label=f"origin:{raw['title']}",
            )
            self.graph.add_branch(branch)
            scene = raw.get("scene") or {}
            for entity in seed.get("entities", []):
                if entity["id"] in scene.get("characters", []) or entity["id"] in scene.get(
                    "events", []
                ) or entity["id"] == raw.get("entity_graph_ref"):
                    self.graph.add_node(
                        GraphNode(
                            node_id=entity["id"],
                            kind=entity["kind"],
                            name=entity["name"],
                            payload=entity,
                            is_real_memory=entity.get("is_real_memory", False),
                            readonly=bool(raw["is_real_memory"]),
                        ),
                        branch.branch_id,
                    )
            item = ChestItem(
                item_id=raw["item_id"],
                item_type=raw["item_type"],
                title=raw["title"],
                vessel=raw["vessel"],
                inscription=raw["inscription"],
                is_real_memory=raw["is_real_memory"],
                layer=raw["layer"],
                source_timeline_id=raw["source_timeline_id"],
                parallel_branch_id=raw["parallel_branch_id"],
                entity_graph_ref=raw["entity_graph_ref"],
                person_id=self.person_id,
                weight=raw.get("weight", "medium"),
                user_edit_note=raw.get("user_edit_note", ""),
                atmosphere=raw.get("atmosphere", ""),
                scene=scene,
                consent_ref=self.consent.get("consent_id", ""),
            )
            self.items[item.item_id] = item
            self.palace.assign(item)
        self._audit("chest.seeded", {"item_count": len(self.items)})
        return self.snapshot()

    def itemize(
        self,
        *,
        source_text: str,
        item_type: ItemType,
        title: str,
        is_real_memory: bool,
        scene: dict[str, Any] | None = None,
        entity_name: str = "",
        user_edit_note: str = "",
    ) -> dict[str, Any]:
        _require_consent(self.consent, REQUIRED_CHEST_SCOPES["itemize"])
        if item_type not in PREFABS:
            raise ChestError("VALIDATION_ERROR", f"unknown item_type {item_type}")
        layer: PalaceLayer = "real_memory" if is_real_memory else "fantasy"
        timeline_id = _new_id("tl", title, source_text[:24])
        branch_id = _new_id("br", timeline_id, "origin")
        item_id = _new_id("item", item_type, title, source_text[:32])
        branch = TimelineBranch(
            branch_id=branch_id,
            timeline_id=timeline_id,
            parent_branch_id=None,
            layer=layer,
            is_real_memory=is_real_memory,
            readonly=is_real_memory,
            label=f"origin:{title}",
        )
        self.graph.add_branch(branch)
        node_id = _new_id("node", item_type, title)
        self.graph.add_node(
            GraphNode(
                node_id=node_id,
                kind=item_type,
                name=entity_name or title,
                payload={"source_text": source_text, "title": title},
                is_real_memory=is_real_memory,
                readonly=is_real_memory,
            ),
            branch_id,
        )
        scene_spec = scene or {
            "scene_id": _new_id("scene", title),
            "title": title,
            "setting": "由记忆文本锚定的私有场景",
            "opening": source_text[:180],
            "characters": [node_id],
            "events": [],
            "mood": "待唤醒",
        }
        item = ChestItem(
            item_id=item_id,
            item_type=item_type,
            title=title,
            vessel=str(PREFABS[item_type]["vessel"]),
            inscription=source_text[:48],
            is_real_memory=is_real_memory,
            layer=layer,
            source_timeline_id=timeline_id,
            parallel_branch_id=branch_id,
            entity_graph_ref=node_id,
            person_id=self.person_id,
            weight="medium",
            user_edit_note=user_edit_note,
            scene=scene_spec,
            consent_ref=self.consent.get("consent_id", ""),
        )
        self.items[item.item_id] = item
        room = self.palace.assign(item)
        self._audit(
            "chest.itemized",
            {"item_id": item.item_id, "room_id": room.room_id, "layer": item.layer},
        )
        return item.to_dict()

    def shuttle(self, item_id: str, mode: ShuttleMode, mutation: str = "") -> dict[str, Any]:
        if mode not in REQUIRED_CHEST_SCOPES:
            raise ChestError("VALIDATION_ERROR", f"unknown shuttle mode {mode}")
        item = self.items.get(item_id)
        if item is None:
            raise ChestError("ITEM_NOT_FOUND", item_id)
        if item.archived:
            raise ChestError("ITEM_ARCHIVED", item_id)
        _require_consent(self.consent, REQUIRED_CHEST_SCOPES[mode])
        origin = self.graph.branches[item.parallel_branch_id]
        if mode == "relive":
            spec = self._scene_spec(item, origin.branch_id, mode)
            session_id = _new_id("sess", item_id, mode, spec["scene_id"])
            session = {
                "session_id": session_id,
                "mode": mode,
                "item_id": item_id,
                "branch_id": origin.branch_id,
                "readonly": True,
                "scene": spec,
                "transition": self._transition(item),
            }
            self.sessions[session_id] = session
            self._audit("chest.shuttle.relive", {"item_id": item_id, "session_id": session_id})
            return session

        if origin.readonly and origin.is_real_memory and mode in {"rewrite", "continue"}:
            # COW：原点只读，派生平行幻想分支，绝不覆盖原始记忆。
            new_branch_id = _new_id("br", origin.branch_id, mode, mutation or "fork")
            cloned = self.graph.clone_branch(
                origin.branch_id,
                new_branch_id,
                label=f"{mode}:{item.title}:{mutation[:24]}",
            )
            child_item = ChestItem(
                item_id=_new_id("item", item.item_id, new_branch_id),
                item_type=item.item_type,
                title=f"{item.title} · 平行分支",
                vessel=item.vessel,
                inscription=mutation or f"{mode} 后的新时空线",
                is_real_memory=False,
                layer="fantasy",
                source_timeline_id=origin.timeline_id,
                parallel_branch_id=cloned.branch_id,
                entity_graph_ref=item.entity_graph_ref,
                person_id=self.person_id,
                weight=item.weight,
                user_edit_note="由原始记忆派生，不是原始存档。",
                atmosphere=item.atmosphere,
                scene={
                    **item.scene,
                    "opening": mutation or item.scene.get("opening", ""),
                    "branch_note": "平行宇宙，原点完整保留",
                },
                derived_from=(item.item_id,),
                consent_ref=self.consent.get("consent_id", ""),
            )
            self.items[child_item.item_id] = child_item
            self.palace.assign(child_item)
            spec = self._scene_spec(child_item, cloned.branch_id, mode)
            session_id = _new_id("sess", child_item.item_id, mode)
            session = {
                "session_id": session_id,
                "mode": mode,
                "item_id": child_item.item_id,
                "origin_item_id": item.item_id,
                "branch_id": cloned.branch_id,
                "parent_branch_id": origin.branch_id,
                "readonly": False,
                "origin_preserved": True,
                "scene": spec,
                "transition": self._transition(child_item),
            }
            self.sessions[session_id] = session
            self._audit(
                "chest.shuttle.fork",
                {
                    "origin_item_id": item.item_id,
                    "child_item_id": child_item.item_id,
                    "parent_branch_id": origin.branch_id,
                    "branch_id": cloned.branch_id,
                },
            )
            return session

        spec = self._scene_spec(item, origin.branch_id, mode)
        if mutation:
            spec = {**spec, "opening": mutation}
        session_id = _new_id("sess", item_id, mode, mutation[:12])
        session = {
            "session_id": session_id,
            "mode": mode,
            "item_id": item_id,
            "branch_id": origin.branch_id,
            "readonly": origin.readonly,
            "scene": spec,
            "transition": self._transition(item),
        }
        self.sessions[session_id] = session
        self._audit("chest.shuttle", {"item_id": item_id, "mode": mode})
        return session

    def capture(
        self,
        session_id: str,
        *,
        fragment: str,
        item_type: ItemType = "story",
        title: str = "",
    ) -> dict[str, Any]:
        _require_consent(self.consent, REQUIRED_CHEST_SCOPES["capture"])
        session = self.sessions.get(session_id)
        if session is None:
            raise ChestError("SESSION_NOT_FOUND", session_id)
        parent = self.items[session["item_id"]]
        captured_title = title or f"{parent.title} · 新片段"
        return self.itemize(
            source_text=fragment,
            item_type=item_type,
            title=captured_title,
            is_real_memory=False,
            scene={
                **session["scene"],
                "opening": fragment,
                "captured_from_session": session_id,
            },
            user_edit_note=f"从穿梭会话 {session_id} 抓取，默认进入幻想层。",
        )

    def fuse(self, item_a_id: str, item_b_id: str, title: str) -> dict[str, Any]:
        _require_consent(self.consent, REQUIRED_CHEST_SCOPES["fuse"])
        a = self.items.get(item_a_id)
        b = self.items.get(item_b_id)
        if a is None or b is None:
            raise ChestError("ITEM_NOT_FOUND", f"{item_a_id}/{item_b_id}")
        if a.sealed or b.sealed:
            raise ChestError("ITEM_SEALED", "sealed items cannot be fused")
        if a.archived or b.archived:
            raise ChestError("ITEM_ARCHIVED", "archived items cannot be fused")
        # 真实记忆融合产物必须降为幻想层，禁止冒充原始记忆。
        source_text = f"{a.inscription} × {b.inscription}"
        fused = self.itemize(
            source_text=source_text,
            item_type="scene",
            title=title,
            is_real_memory=False,
            scene={
                "scene_id": _new_id("scene", a.item_id, b.item_id),
                "title": title,
                "setting": f"{a.scene.get('setting', a.title)} 与 {b.scene.get('setting', b.title)} 交叠",
                "style": "跨界合成",
                "mood": "陌生而可逆",
                "opening": f"{a.title} 走进了 {b.title} 的时空。这是创作，不是原始记忆。",
                "characters": list(
                    dict.fromkeys(
                        list(a.scene.get("characters") or [])
                        + list(b.scene.get("characters") or [])
                    )
                ),
                "events": [],
            },
            user_edit_note="跨界合成。若任一来源为真实记忆，产物标注为幻想派生。",
        )
        fused_item = self.items[fused["item_id"]]
        fused_item.derived_from = (a.item_id, b.item_id)
        self._audit(
            "chest.fused",
            {"item_id": fused_item.item_id, "parents": [a.item_id, b.item_id]},
        )
        return fused_item.to_dict()

    def archive(self, item_id: str) -> dict[str, Any]:
        item = self.items.get(item_id)
        if item is None:
            raise ChestError("ITEM_NOT_FOUND", item_id)
        item.archived = True
        self._audit("chest.archived", {"item_id": item_id})
        return item.to_dict()

    def seal(self, item_id: str) -> dict[str, Any]:
        item = self.items.get(item_id)
        if item is None:
            raise ChestError("ITEM_NOT_FOUND", item_id)
        item.sealed = True
        self._audit("chest.sealed", {"item_id": item_id})
        return item.to_dict()

    def origin_intact(self, item_id: str) -> bool:
        item = self.items[item_id]
        branch = self.graph.branches[item.parallel_branch_id]
        return branch.readonly is True and branch.is_real_memory is True

    def _scene_spec(self, item: ChestItem, branch_id: str, mode: ShuttleMode) -> dict[str, Any]:
        nodes = [n.to_dict() for n in self.graph.nodes_in(branch_id)]
        spec = {
            **item.scene,
            "item_id": item.item_id,
            "mode": mode,
            "layer": item.layer,
            "is_real_memory": item.is_real_memory,
            "ground_truth_nodes": nodes,
            "alive_characters": [
                n.to_dict()
                for n in self.graph.nodes_in(branch_id)
                if n.kind == "person"
            ],
        }
        self.graph.assert_consistent(spec, branch_id)
        return spec

    def _transition(self, item: ChestItem) -> dict[str, Any]:
        return {
            "sequence": ["道具激活", "空间扭曲", "记忆碎片闪回", "场景落地"],
            "lens": "私有仪式而非过场黑屏",
            "audio": item.atmosphere or "soft_memory_chime",
            "particle": item.item_type,
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "person_id": self.person_id,
            "slogan": "以记忆筑宫殿，以万物为宝箱，以道具穿时空，人人皆为自己故事的造物主。",
            "views": ["palace", "chest", "shuttle"],
            "items": [i.to_dict() for i in self.items.values() if not i.archived],
            "archived_count": sum(1 for i in self.items.values() if i.archived),
            "palace": self.palace.to_dict(),
            "graph": {
                "branch_count": len(self.graph.branches),
                "node_count": len(self.graph.nodes),
                "readonly_origins": [
                    b.branch_id
                    for b in self.graph.branches.values()
                    if b.readonly and b.is_real_memory
                ],
            },
            "sessions": list(self.sessions.values()),
            "audit": list(self.audit),
        }


def build_seeded_engine() -> MemoryChestEngine:
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    engine = MemoryChestEngine(person_id=seed["person_id"], consent=seed["consent"])
    engine.load_seed(seed)
    return engine
