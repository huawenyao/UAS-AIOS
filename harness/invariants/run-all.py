#!/usr/bin/env python3
"""
数字人生态 harness 基线 Invariant 验证。
运行: python harness/invariants/run-all.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = HARNESS_ROOT.parent


class Result:
    def __init__(self, name: str, passed: bool, message: str = "") -> None:
        self.name = name
        self.passed = passed
        self.message = message


def check_harness_structure() -> Result:
    required = [
        HARNESS_ROOT / "state.json",
        HARNESS_ROOT / "entity-map.json",
        HARNESS_ROOT / "knowledge" / "index.yaml",
        HARNESS_ROOT / "requirements" / "REQ-EDH-BASE-001.req.md",
    ]
    missing = [str(p.relative_to(REPO_ROOT)) for p in required if not p.is_file()]
    if missing:
        return Result("harness_structure", False, f"missing: {missing}")
    return Result("harness_structure", True, "ok")


def check_strategic_docs_linked() -> Result:
    state = json.loads((HARNESS_ROOT / "state.json").read_text(encoding="utf-8"))
    docs = state.get("project", {}).get("strategic_docs", [])
    missing = [d for d in docs if not (REPO_ROOT / d).is_file()]
    if missing:
        return Result("strategic_docs_linked", False, f"missing: {missing}")
    return Result("strategic_docs_linked", True, f"{len(docs)} docs")


def check_entity_map_consistency() -> Result:
    emap = json.loads((HARNESS_ROOT / "entity-map.json").read_text(encoding="utf-8"))
    entities = emap.get("entities", {})
    required_keys = [
        "UASKernel",
        "CapabilityService",
        "SelfPawEnterprise",
        "PiPawBusinessAGI",
        "EnterpriseDataPlane",
    ]
    missing = [k for k in required_keys if k not in entities]
    if missing:
        return Result("entity_map_consistency", False, f"missing entities: {missing}")
    deps = emap.get("dependencies", {})
    if "Agent_to_CapabilityService" not in deps:
        return Result("entity_map_consistency", False, "missing Agent_to_CapabilityService rule")
    return Result("entity_map_consistency", True, f"{len(entities)} entities")


def check_knowledge_index() -> Result:
    expected = [
        "product/digital-human-ecosystem-vision.md",
        "technical/edh-platform-baseline.md",
        "technical/capability-service-catalog-baseline.md",
        "domain/glossary.md",
        "constraints/adr-edh-001-dual-track-boundary.md",
        "constraints/adr-edh-002-capability-before-agent.md",
        "technical/capability-service-registry-api.md",
        "technical/enterprise-tenant-org-api.md",
        "technical/enterprise-rbac-abac-spec.md",
        "technical/enterprise-audit-chain-spec.md",
        "technical/system-connector-spec.md",
        "technical/intent-escalation-api.md",
    ]
    missing = [
        rel for rel in expected if not (HARNESS_ROOT / "knowledge" / rel).is_file()
    ]
    if missing:
        return Result("knowledge_index", False, f"missing: {missing}")
    return Result("knowledge_index", True, f"{len(expected)} files")


def check_phase0_requirements_registered() -> Result:
    req_dir = HARNESS_ROOT / "requirements"
    prefixes = ("REQ-EDH-PL-", "REQ-EDH-SP-", "REQ-EDH-PP-", "REQ-EDH-K-")
    files = list(req_dir.glob("REQ-EDH-*.req.md"))
    by_prefix = {p: 0 for p in prefixes}
    for f in files:
        for p in prefixes:
            if f.name.startswith(p):
                by_prefix[p] += 1
    if any(v == 0 for v in by_prefix.values()):
        return Result("phase0_requirements", False, str(by_prefix))
    return Result("phase0_requirements", True, str(by_prefix))


def check_system_connectors() -> Result:
    for path in (
        REPO_ROOT / "configs" / "connectors.json",
        REPO_ROOT / "schemas" / "system_connector.schema.json",
        REPO_ROOT / "asui-cli" / "src" / "asui" / "connectors" / "router.py",
    ):
        if not path.is_file():
            return Result("system_connectors", False, f"missing {path.name}")
    import subprocess

    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_connectors.py"), "validate"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=90,
    )
    if r.returncode != 0:
        return Result("system_connectors", False, (r.stderr or r.stdout).strip()[:500])
    r2 = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_edh_connectors.py", "-q"],
        cwd=str(REPO_ROOT / "asui-cli"),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if r2.returncode != 0:
        return Result("system_connectors", False, (r2.stderr or r2.stdout).strip()[:500])
    return Result("system_connectors", True, "crm+oa mock+pytest")


def check_enterprise_policy() -> Result:
    script = REPO_ROOT / "scripts" / "validate_enterprise_policy.py"
    for path in (
        REPO_ROOT / "schemas" / "enterprise_tenant.schema.json",
        REPO_ROOT / "schemas" / "enterprise_permission.schema.json",
        REPO_ROOT / "configs" / "tenant_catalog.sample.json",
        REPO_ROOT / "configs" / "enterprise_rbac_template.json",
        REPO_ROOT / "schemas" / "audit_record.schema.json",
        REPO_ROOT / "configs" / "audit_policy.sample.json",
    ):
        if not path.is_file():
            return Result("enterprise_policy", False, f"missing {path.name}")
    import subprocess

    r = subprocess.run(
        [sys.executable, str(script), "validate"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    if r.returncode != 0:
        return Result("enterprise_policy", False, (r.stderr or r.stdout).strip()[:500])
    return Result("enterprise_policy", True, "tenant+rbac+isolation")


def check_capability_registry() -> Result:
    registry_path = REPO_ROOT / "configs" / "capability_registry.json"
    schema_path = REPO_ROOT / "schemas" / "capability_service.schema.json"
    if not registry_path.is_file():
        return Result("capability_registry", False, "missing configs/capability_registry.json")
    if not schema_path.is_file():
        return Result("capability_registry", False, "missing schemas/capability_service.schema.json")
    import subprocess

    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_capability_registry.py"), "validate"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    if r.returncode != 0:
        return Result("capability_registry", False, (r.stderr or r.stdout).strip()[:500])
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    n = len(registry.get("services", []))
    min_required = 5
    state = json.loads((HARNESS_ROOT / "state.json").read_text(encoding="utf-8"))
    min_required = state.get("metrics", {}).get("phase_0_exit", {}).get("capability_services_min", 5)
    if n < min_required:
        return Result("capability_registry", False, f"services={n} < {min_required}")
    return Result("capability_registry", True, f"{n} services")


def check_intent_escalation() -> Result:
    for path in (
        REPO_ROOT / "schemas" / "intent_object.schema.json",
        REPO_ROOT / "schemas" / "working_task.schema.json",
        REPO_ROOT / "configs" / "intent_escalation_policy.sample.json",
        REPO_ROOT / "asui-cli" / "src" / "asui" / "intent_hub.py",
    ):
        if not path.is_file():
            return Result("intent_escalation", False, f"missing {path.name}")
    import subprocess

    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_intent_escalation.py"), "validate"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=90,
    )
    if r.returncode != 0:
        return Result("intent_escalation", False, (r.stderr or r.stdout).strip()[:500])
    r2 = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_intent_escalation.py", "-q"],
        cwd=str(REPO_ROOT / "asui-cli"),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if r2.returncode != 0:
        return Result("intent_escalation", False, (r2.stderr or r2.stdout).strip()[:500])
    return Result("intent_escalation", True, "escalate+e2e+pytest")


def check_uas_runtime_list() -> Result:
    script = REPO_ROOT / "scripts" / "run_uas_runtime_service.py"
    if not script.is_file():
        return Result("uas_runtime_list", False, "script missing")
    import subprocess

    r = subprocess.run(
        [sys.executable, str(script), "list"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    if r.returncode != 0:
        return Result("uas_runtime_list", False, (r.stderr or r.stdout)[:500])
    try:
        apps = json.loads(r.stdout)
    except json.JSONDecodeError as e:
        return Result("uas_runtime_list", False, str(e))
    if not apps:
        return Result("uas_runtime_list", False, "no subapps")
    return Result("uas_runtime_list", True, f"{len(apps)} app(s)")


def main() -> int:
    checks = [
        check_harness_structure,
        check_strategic_docs_linked,
        check_entity_map_consistency,
        check_knowledge_index,
        check_phase0_requirements_registered,
        check_capability_registry,
        check_enterprise_policy,
        check_system_connectors,
        check_intent_escalation,
        check_uas_runtime_list,
    ]
    results: list[Result] = []
    for fn in checks:
        try:
            results.append(fn())
        except Exception as e:
            results.append(Result(fn.__name__, False, str(e)))

    print("=== EDH Harness Invariants ===\n")
    failed = 0
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{status}] {r.name}: {r.message}")
        if not r.passed:
            failed += 1
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
