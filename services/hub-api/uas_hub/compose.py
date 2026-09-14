"""组合根：按协议注册表把夹具 Port 接到 Hub。真零件替换只改 adapters。"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uas_hub.hub import Hub

REPO = Path(__file__).resolve().parents[3]

_ADAPTERS = (
    ("kg", "uas_hub.adapters.kg", "FixtureKg", ()),
    ("memory", "uas_hub.adapters.memory", "FixtureMemory", ()),
    ("inner_loop", "uas_hub.adapters.inner_loop", "FixtureInnerLoop", ()),
    ("broker", "uas_hub.adapters.broker", "FixtureBroker", ()),
    ("skill", "uas_hub.adapters.skill", "FixtureSkill", ()),
    ("law", "uas_hub.adapters.law", "FixtureLaw", ()),
    ("evolution", "uas_hub.adapters.evolution", "FixtureEvolution", ()),
    ("artifact", "uas_hub.adapters.artifact", "FixtureArtifact", ()),
    ("connector", "uas_hub.adapters.connector", "FixtureConnector", ()),
    ("iam", "uas_hub.adapters.iam", "FixtureIam", ()),
    ("review", "uas_hub.adapters.review", "FixtureReview", ()),
)


def attach_fixtures(hub: "Hub") -> "Hub":
    try:
        cube_mod = importlib.import_module("uas_hub.adapters.cube")
        hub.cube = cube_mod.FixtureCube(osi_dir=REPO / "configs" / "metrics" / "osi")
    except Exception:
        pass
    for attr, module_name, cls_name, args in _ADAPTERS:
        try:
            mod = importlib.import_module(module_name)
            setattr(hub, attr, getattr(mod, cls_name)(*args))
        except Exception:
            continue
    try:
        mcp_mod = importlib.import_module("uas_hub.adapters.mcp")
        hub.mcp = mcp_mod.FixtureMcp(hub)
    except Exception:
        pass
    return hub


def try_attach_fixtures(hub: "Hub") -> "Hub":
    return attach_fixtures(hub)
