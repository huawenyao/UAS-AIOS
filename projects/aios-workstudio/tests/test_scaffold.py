from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "modules" / "catalog.json").read_text(encoding="utf-8"))
CLUSTER_IDS = {
    "nb", "m1", "m5", "sse", "m6", "hubc", "pack", "gov", "m7", "m13", "m8",
    "m11", "m12", "m10", "m9", "m20", "m21", "m2", "m3", "m4", "m14", "m23",
    "m18", "m19", "m24", "m15", "m16", "m17", "m22", "idp",
}
FORBIDDEN = ("cubejs", "graphiti", "neo4j", "langgraph", "temporal", "lethe", "workflow_id", "CubeQL")


class ScaffoldTests(unittest.TestCase):
    def test_catalog_covers_cluster_modules(self) -> None:
        ids = {m["id"] for m in CATALOG["modules"]}
        self.assertEqual(ids, CLUSTER_IDS)

    def test_each_module_has_spec(self) -> None:
        for mod in CATALOG["modules"]:
            spec = ROOT / "modules" / mod["dir"] / "SPEC.md"
            self.assertTrue(spec.is_file(), spec)
            text = spec.read_text(encoding="utf-8")
            self.assertIn(mod["t"], text)
            self.assertIn("## 定位", text)
            self.assertIn("## 非职责", text)
            self.assertIn("## 接口", text)
            self.assertIn("## 否决", text)
            self.assertIn("## 验收", text)

    def test_workstudio_client_has_no_part_sdk(self) -> None:
        client = (ROOT / "packages" / "hub-client" / "src" / "scene.ts").read_text(encoding="utf-8")
        for noun in FORBIDDEN:
            self.assertNotIn(noun, client, noun)
        self.assertIn("/hub/v1/scene/", client)
        self.assertIn("/hub/v1/exec/", client)
        self.assertNotIn("/v1/load", client)

    def test_workstudio_demo_calls_scene_pack_open(self) -> None:
        demo = ROOT / "demo"
        blob = (demo / "hub-scene.js").read_text(encoding="utf-8")
        html = (demo / "index.html").read_text(encoding="utf-8")
        self.assertIn("/hub/v1/scene/pack/open", blob)
        self.assertIn("/hub/v1/scene/insight/drill", blob)
        self.assertIn("/hub/v1/scene/task/issue", blob)
        self.assertIn("/hub/v1/policy/explain", blob)
        self.assertIn("hub-scene.js", html)
        self.assertNotIn("/hub/v1/ops/", blob)
        for noun in FORBIDDEN:
            self.assertNotIn(noun, blob, noun)

    def test_workstudio_hub_scene_has_exec(self) -> None:
        blob = (ROOT / "demo" / "hub-scene.js").read_text(encoding="utf-8")
        self.assertIn("/hub/v1/exec/open", blob)
        self.assertIn("/hub/v1/instance/cycle_step", blob)
        self.assertIn("/hub/v1/exec/", blob)

    def test_workstudio_exec_ui_copy(self) -> None:
        js = (ROOT / "demo" / "workstudio.js").read_text(encoding="utf-8")
        self.assertIn("execOpen", js)
        self.assertIn("待你确认", js)
        self.assertNotIn("workflow_id", js)

    def test_console_client_only_ops(self) -> None:
        ops = (ROOT / "packages" / "hub-client" / "src" / "ops.ts").read_text(encoding="utf-8")
        self.assertIn("/hub/v1/ops/", ops)
        self.assertIn("/hub/v1/ops/policy/explain", ops)
        self.assertIn("/hub/v1/ops/changeset/submit", ops)
        self.assertNotIn("/hub/v1/instance/invoke_cs", ops)
        self.assertNotIn("/hub/v1/kg/ingest", ops)
        for noun in ("CollectionBlockModel", "plugin-ai", "mcp-server"):
            self.assertNotIn(noun, ops)

    def test_console_demo_is_ops_shell(self) -> None:
        demo = ROOT / "Console" / "demo"
        for name in ("index.html", "console.css", "data.js", "app.js"):
            self.assertTrue((demo / name).is_file(), name)
        html = (demo / "index.html").read_text(encoding="utf-8")
        js = (demo / "app.js").read_text(encoding="utf-8") + (demo / "data.js").read_text(encoding="utf-8")
        self.assertIn("Platform Console", html)
        self.assertIn("看不到 /console", js)
        self.assertIn("I-05", js)
        self.assertIn("auto_apply", js)
        self.assertIn("岗位绑定", js)
        self.assertIn("自动化作业", js)
        self.assertIn("hub.ops.iam.bindings", js)
        self.assertNotIn("invoke_cs", js)
        self.assertNotIn("/hub/v1/kg/ingest", js)
        self.assertNotIn("CollectionBlockModel", js)
        for noun in FORBIDDEN:
            self.assertNotIn(noun, js, noun)

    def test_console_hub_ops_client(self) -> None:
        demo = ROOT / "Console" / "demo"
        blob = (demo / "hub-ops.js").read_text(encoding="utf-8")
        html = (demo / "index.html").read_text(encoding="utf-8")
        self.assertIn("/hub/v1/ops/changeset/submit", blob)
        self.assertIn("/hub/v1/ops/schema/drift", blob)
        self.assertIn("/hub/v1/ops/audit/search", blob)
        self.assertIn("/hub/v1/ops/memory/receipt", blob)
        self.assertIn("/hub/v1/ops/automation/jobs", blob)
        self.assertIn("/hub/v1/ops/wm/list", blob)
        self.assertIn("hub-ops.js", html)
        self.assertNotIn("/hub/v1/scene/", blob)
        self.assertNotIn("invoke_cs", blob)
        self.assertIn("/hub/v1/ops/connector/rotate", blob)
        for noun in FORBIDDEN:
            self.assertNotIn(noun, blob, noun)

    def test_console_demo_degrades_without_hub(self) -> None:
        js = (ROOT / "Console" / "demo" / "app.js").read_text(encoding="utf-8")
        self.assertIn("HubOps", js)
        self.assertIn("只读降级", js)
        self.assertIn("本战役离线", js)
        self.assertIn("caliberStatus", js)
        self.assertIn("memoryReceipt", js)
        self.assertIn("automationJobs", js)
        self.assertIn("wmList", js)
        self.assertIn("connectorRotate", js)
        self.assertNotIn('"run", "caliber", "workflows", "automation"', js)
        self.assertNotIn('"automation", "memory", "wm"', js)

    def test_workstudio_demo_has_no_talent_pack(self) -> None:
        html = (ROOT / "demo" / "index.html").read_text(encoding="utf-8")
        js = (ROOT / "demo" / "workstudio.js").read_text(encoding="utf-8")
        self.assertNotIn("经营 / 人才流", html)
        self.assertNotIn('value="ops"', html)
        self.assertNotIn("HIR-042", js)
        self.assertNotIn("wi-rao", js)
        self.assertNotIn("人才流", js)
        self.assertIn('value="cm"', html)
        self.assertIn('pack: "cm"', js)
        self.assertIn("销售运营", html)
        self.assertIn("企业经营分析", html)
        self.assertIn("投资研究", html)
        self.assertIn("数据", js)
        self.assertIn("洞察", js)
        self.assertIn("策略行动", js)
        self.assertIn("学习沉淀", js)

    def test_workstudio_demo_degrades_without_hub(self) -> None:
        js = (ROOT / "demo" / "workstudio.js").read_text(encoding="utf-8")
        self.assertIn("HubScene", js)
        self.assertIn("packOpen", js)
        self.assertIn("只读降级", js)
        self.assertIn("an-stage-visit", js)

    def test_no_parallel_kernel_packages(self) -> None:
        banned = list((ROOT / "packages").glob("cube*")) + list((ROOT / "packages").glob("graphiti*"))
        self.assertEqual(banned, [])


if __name__ == "__main__":
    unittest.main()
