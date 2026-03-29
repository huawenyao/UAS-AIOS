"""UAS 平台形式化契约（Π）：八元组与 platform_manifest 约定。"""

from __future__ import annotations

import json
from typing import Any

FORMAL_DEFINITION: tuple[str, ...] = ("I", "K", "R", "A", "S", "G", "E", "Π")

LAYER_LABELS: dict[str, str] = {
    "I": "Intent Layer",
    "K": "Knowledge Substrate",
    "R": "Autonomous Agent Runtime",
    "A": "Agent Fabric",
    "S": "System Mesh",
    "G": "Governance Plane",
    "E": "Evolution Loop",
    "Π": "Protocol Stack",
}


def default_platform_manifest_dict() -> dict[str, Any]:
    """与 UAS subapp 默认 ``platform_manifest.json`` 语义一致的结构化表示。"""
    return {
        "$schema": "https://asui.dev/schemas/uas_platform_manifest.schema.json",
        "version": "v1.0",
        "platform": {
            "name": "UAS-Platform",
            "formal_definition": list(FORMAL_DEFINITION),
            "enterprise_agi_definition": (
                "目标驱动 + 知识驱动 + Agent协作 + 系统执行 + 审计治理 + 演化闭环 的平台化统一"
            ),
            "technical_base": "ASUI",
            "runtime": "autonomous_agent",
        },
        "layers": dict(LAYER_LABELS),
        "defaults": {
            "subapp_root": "projects",
            "require_governance": True,
            "require_evolution": True,
            "require_audit": True,
        },
    }


def format_platform_manifest_json() -> str:
    """生成默认 ``platform_manifest.json`` 文本（UTF-8、缩进与换行稳定）。"""
    body = json.dumps(default_platform_manifest_dict(), ensure_ascii=False, indent=2)
    return body + "\n"
