"""Schema 校验 — 实体 + RitualEnvelope。

规约来源：docs/lifewake/CAPABILITY_CONTRACTS.md、DOMAIN_MODEL.md、schemas/ritual_envelope.schema.json
优先使用 jsonschema（若安装）；否则回退到 domain.py 的 dataclass 不变量校验。
两种路径都强制红线 15（envelope 必须含 timing/impact ref）与红线 16（审计净化）。
"""

from __future__ import annotations

from typing import Any

from . import domain

try:
    import jsonschema  # type: ignore

    _HAVE_JSONSCHEMA = True
except ImportError:
    _HAVE_JSONSCHEMA = False


# === 声明式 JSON Schema（draft 2020-12） ===

ENTITY_SCHEMAS: dict[str, dict[str, Any]] = {
    "ConsentGrant": {
        "type": "object",
        "required": ["consent_id", "person_id", "scopes", "purpose", "expires_at"],
        "properties": {
            "consent_id": {"type": "string"},
            "person_id": {"type": "string"},
            "scopes": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "purpose": {"type": "string", "const": "create_for_user"},
            "status": {"type": "string", "enum": ["granted", "revoked", "expired"]},
            "withdrawable": {"type": "boolean", "const": True},
            "expires_at": {"type": "string", "minLength": 1},
            "beneficiaries": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": True,
    },
    "RitualEnvelope": {
        "type": "object",
        "required": [
            "envelope_id",
            "ritual_id",
            "intent_ref",
            "artifact_ref",
            "timing_decision_ref",
            "emotion_impact_ref",
        ],
        "properties": {
            "envelope_id": {"type": "string"},
            "ritual_id": {"type": "string"},
            "intent_ref": {"type": "string"},
            "artifact_ref": {"type": "string"},
            "timing_decision_ref": {"type": "string", "minLength": 1},
            "emotion_impact_ref": {"type": "string", "minLength": 1},
            "owners": {"type": "array", "items": {"type": "string"}},
            "consent_refs": {"type": "array", "items": {"type": "string"}},
            "state": {
                "type": "string",
                "enum": [
                    "draft",
                    "ready",
                    "revealed",
                    "saved",
                    "dismissed",
                    "deleted",
                    "cancelled_by_revoke",
                ],
            },
        },
        "additionalProperties": True,
    },
    "ChangeSet": {
        "type": "object",
        "required": ["changeset_id", "target_pack", "auto_apply"],
        "properties": {
            "changeset_id": {"type": "string"},
            "target_pack": {
                "type": "string",
                "enum": ["surprise_policy", "pulse_policy", "consent_copy", "agent"],
            },
            "auto_apply": {"type": "boolean", "const": False},
            "status": {
                "type": "string",
                "enum": ["draft", "approved", "applied", "rolled_back", "rejected"],
            },
        },
        "additionalProperties": True,
    },
    "AuditEvent": {
        "type": "object",
        "required": ["audit_id", "event", "trace_id"],
        "properties": {
            "audit_id": {"type": "string"},
            "event": {"type": "string"},
            "trace_id": {"type": "string"},
            "payload": {"type": "object"},
        },
        "additionalProperties": True,
    },
}

# 审计净化的禁含字段（红线 16）
AUDIT_FORBIDDEN_KEYS = {
    "raw_pulse_stream",
    "free_text_feedback",
    "partner_rejection_reason",
    "exact_age",
    "diagnostic_inference",
}


class ValidationError(ValueError):
    """schema 校验失败。"""


def _sanitize_audit_payload(payload: dict[str, Any]) -> dict[str, Any]:
    leaked = AUDIT_FORBIDDEN_KEYS & set(payload or {})
    if leaked:
        raise ValidationError(
            f"audit payload contains forbidden keys: {sorted(leaked)}"
        )
    return payload


def validate_entity(name: str, data: dict[str, Any]) -> dict[str, Any]:
    """校验单个实体 dict。返回净化后的 data。

    优先 jsonschema；回退到 domain dataclass 构造（强制 __post_init__ 不变量）。
    """
    if name == "AuditEvent":
        data = {**data, "payload": _sanitize_audit_payload(data.get("payload", {}))}

    if _HAVE_JSONSCHEMA and name in ENTITY_SCHEMAS:
        try:
            jsonschema.validate(data, ENTITY_SCHEMAS[name])
        except jsonschema.ValidationError as exc:  # type: ignore
            raise ValidationError(f"{name}: {exc.message}") from exc

    # 始终再走 dataclass 不变量（覆盖 jsonschema 未表达的领域规则，如 duet owners、surprise uniqueness）
    _enforce_domain_invariants(name, data)
    return data


def _enforce_domain_invariants(name: str, data: dict[str, Any]) -> None:
    """用 domain dataclass 强制领域不变量（即使无 jsonschema 也生效）。"""
    mapping = {
        "ConsentGrant": domain.ConsentGrant,
        "RitualEnvelope": domain.RitualEnvelope,
        "ChangeSet": domain.ChangeSet,
        "AuditEvent": domain.AuditEvent,
        "Surprise": domain.Surprise,
        "Bond": domain.Bond,
    }
    cls = mapping.get(name)
    if cls is None:
        return
    try:
        domain.from_dict(cls, data)
    except domain.DomainError as exc:
        raise ValidationError(str(exc)) from exc
    except TypeError as exc:
        # 缺必填字段等 → 转为 ValidationError
        raise ValidationError(f"{name}: {exc}") from exc


def validate_ritual_envelope(data: dict[str, Any]) -> dict[str, Any]:
    """RitualEnvelope 专用校验入口（红线 15）。"""
    return validate_entity("RitualEnvelope", data)


def validate_audit_event(data: dict[str, Any]) -> dict[str, Any]:
    """AuditEvent 专用校验入口（红线 16 净化）。"""
    return validate_entity("AuditEvent", data)


def have_jsonschema() -> bool:
    return _HAVE_JSONSCHEMA
