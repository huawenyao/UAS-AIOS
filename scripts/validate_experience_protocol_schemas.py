#!/usr/bin/env python3
"""Validate reusable UAS experience-protocol schemas and contract examples."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

try:
    from jsonschema import Draft7Validator, FormatChecker
except ImportError:  # The repository baseline intentionally has no third-party runtime dependency.
    Draft7Validator = None
    FormatChecker = None

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "schemas"

CASES = {
    "consent_record.schema.json": {
        "required_key": "subject_id",
        "instance": {
            "consent_id": "consent-example-001",
            "subject_id": "person-a",
            "controller_id": "app-experience",
            "purpose": "create a participant-approved experience",
            "scopes": ["memory.summary", "relationship.context"],
            "status": "granted",
            "recorded_at": "2026-07-22T03:00:00Z",
            "provenance": {"channel": "selfpaw-ui", "actor_id": "person-a"},
        },
    },
    "ritual_envelope.schema.json": {
        "required_key": "steps",
        "instance": {
            "ritual_id": "ritual-example-001",
            "protocol_version": "1.0.0",
            "ritual_type": "reflection.shared",
            "domain_id": "experience.example",
            "purpose": "close a shared reflection",
            "participant_ids": ["person-a", "person-b"],
            "consent_refs": ["consent-example-001", "consent-example-002"],
            "steps": [
                {"step_id": "prepare-1", "kind": "prepare", "sequence": 1},
                {
                    "step_id": "reflect-1",
                    "kind": "reflect",
                    "sequence": 2,
                    "requires_acknowledgement": True,
                },
            ],
            "status": "ready",
            "created_at": "2026-07-22T03:00:00Z",
            "extensions": {"example.presentation": {"mode": "audio"}},
        },
    },
    "emotion_impact.schema.json": {
        "required_key": "dimensions",
        "instance": {
            "impact_id": "impact-example-001",
            "target_ref": "ritual-example-001",
            "subject_ids": ["person-a"],
            "method": "self_report",
            "dimensions": {
                "meaning": {"score": 0.8, "confidence": 0.9},
                "connection": {"score": 0.6},
            },
            "overall_score": 0.7,
            "outcome": "positive",
            "measured_at": "2026-07-22T03:10:00Z",
        },
    },
    "bond_cocreation.schema.json": {
        "required_key": "reciprocity",
        "instance": {
            "cocreation_id": "cocreation-example-001",
            "bond_ref": "relationship-a-b",
            "participant_ids": ["person-a", "person-b"],
            "shared_intent": "create a mutually approved keepsake",
            "consent_refs": ["consent-example-001", "consent-example-002"],
            "contributions": [
                {
                    "contribution_id": "contribution-a",
                    "participant_id": "person-a",
                    "kind": "creative_direction",
                },
                {
                    "contribution_id": "contribution-b",
                    "participant_id": "person-b",
                    "kind": "feedback",
                },
            ],
            "reciprocity": {
                "status": "balanced",
                "evaluated_at": "2026-07-22T03:05:00Z",
            },
            "ownership": "shared",
            "status": "active",
            "created_at": "2026-07-22T03:00:00Z",
        },
    },
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema_structure(schema: dict) -> list[str]:
    """Check Draft-07 metadata and locally resolvable constructs with stdlib only."""
    errors: list[str] = []
    if schema.get("$schema") != "http://json-schema.org/draft-07/schema#":
        errors.append("$schema must select JSON Schema Draft-07")
    if schema.get("type") != "object":
        errors.append("root type must be object")
    if not schema.get("$id", "").startswith("https://asui.dev/schemas/"):
        errors.append("$id must use the repository schema namespace")

    definitions = schema.get("definitions", {})

    def walk(node: object, location: str) -> None:
        if isinstance(node, dict):
            required = node.get("required", [])
            properties = node.get("properties", {})
            if required and not isinstance(required, list):
                errors.append(f"{location}.required must be an array")
            if "properties" in node and isinstance(required, list) and isinstance(properties, dict):
                unknown = sorted(set(required) - set(properties))
                if unknown:
                    errors.append(f"{location}.required references unknown properties: {unknown}")
            if "pattern" in node:
                try:
                    re.compile(node["pattern"])
                except (re.error, TypeError) as exc:
                    errors.append(f"{location}.pattern is invalid: {exc}")
            ref = node.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/definitions/"):
                name = ref.removeprefix("#/definitions/")
                if name not in definitions:
                    errors.append(f"{location} has unresolved $ref {ref}")
            for key, value in node.items():
                walk(value, f"{location}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{location}[{index}]")

    walk(schema, "$")
    return errors


def main() -> int:
    failures: list[str] = []
    full_validation = Draft7Validator is not None
    for filename, case in CASES.items():
        schema = load_json(SCHEMA_DIR / filename)
        failures.extend(f"{filename}: {error}" for error in validate_schema_structure(schema))
        invalid = copy.deepcopy(case["instance"])
        invalid.pop(case["required_key"])
        if case["required_key"] not in schema.get("required", []):
            failures.append(f"{filename}: {case['required_key']} is not required by the contract")

        if full_validation:
            try:
                Draft7Validator.check_schema(schema)
            except Exception as exc:  # jsonschema exposes several schema error subclasses
                failures.append(f"{filename}: invalid schema: {exc}")
                continue
            validator = Draft7Validator(schema, format_checker=FormatChecker())
            valid_errors = list(validator.iter_errors(case["instance"]))
            if valid_errors:
                failures.append(f"{filename}: valid fixture rejected: {valid_errors[0].message}")
            if not list(validator.iter_errors(invalid)):
                failures.append(f"{filename}: missing {case['required_key']} was accepted")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    mode = "jsonschema Draft-07 + stdlib" if full_validation else "stdlib structural"
    print(f"OK: {len(CASES)} experience protocol schemas valid ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
