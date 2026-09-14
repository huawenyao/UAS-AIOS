from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(HUB_ROOT))

from uas_hub.policy import PolicyChain  # noqa: E402
from uas_hub.protocol_catalog import REQUIRED_IDS, load_registry, validate_registry  # noqa: E402


class ProtocolRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load_registry(REPO)

    def test_kernel_and_schema_exist(self) -> None:
        self.assertTrue((REPO / "configs" / "protocol" / "KERNEL.yaml").is_file())
        self.assertTrue((REPO / "schemas" / "protocol" / "module_protocol.schema.json").is_file())

    def test_twenty_four_modules(self) -> None:
        ids = [m["id"] for m in self.data["modules"]]
        self.assertEqual(ids, REQUIRED_IDS)

    def test_validate_clean(self) -> None:
        self.assertEqual(validate_registry(self.data), [])

    def test_schema_validates(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = json.loads(
            (REPO / "schemas" / "protocol" / "module_protocol.schema.json").read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator(schema).validate(self.data)

    def test_policy_order_matches_chain(self) -> None:
        self.assertEqual(tuple(self.data["policy_order"]), PolicyChain.ORDER)

    def test_integrated_have_ports(self) -> None:
        for mod in self.data["modules"]:
            if mod["decision"] in {"integrate", "connect"} and mod["id"] not in {"M23"}:
                self.assertTrue(mod.get("port"), mod["id"])
            if mod["decision"] == "integrate":
                self.assertTrue(mod["replaceable"], mod["id"])

    def test_l0_not_replaceable(self) -> None:
        for mid in ("M2", "M3", "M4", "M5", "M6"):
            mod = next(m for m in self.data["modules"] if m["id"] == mid)
            self.assertFalse(mod["replaceable"], mid)
            self.assertEqual(mod["decision"], "own")

    def test_front_forbidden_nouns(self) -> None:
        nouns = set(self.data["front_forbidden_nouns"])
        self.assertIn("workflow_id", nouns)
        self.assertIn("CubeQL", nouns)

    def test_outer_loop_port_exported(self) -> None:
        from uas_hub.ports import OuterLoopPort  # noqa: F401
        from uas_hub.protocol_catalog import REQUIRED_PORTS
        self.assertIn("OuterLoopPort", REQUIRED_PORTS)
