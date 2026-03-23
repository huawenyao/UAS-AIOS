from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_world_model_doc_exists() -> None:
    doc = ROOT / "docs" / "AI招聘世界模型.md"
    assert doc.exists(), "missing docs/AI招聘世界模型.md"
    text = doc.read_text(encoding="utf-8")
    assert "## 世界模型" in text
    assert "## 实体模型" in text
    assert "## 事件模型" in text
    assert "## 招聘场景闭环" in text


def test_domain_world_model_contract() -> None:
    module = _load_module(ROOT / "scripts" / "domain_world_model.py", "domain_world_model")
    model = module.build_domain_world_model()
    assert isinstance(model, dict)
    assert model.get("domain") == "ai_recruitment"
    entities = set(model.get("entities", []))
    events = set(model.get("events", []))
    stages = model.get("closed_loop_stages", [])
    for required in ("Job", "Candidate", "Task", "Event", "Notification", "Evaluation"):
        assert required in entities
    for required_event in ("screening_completed", "ai_interview_completed"):
        assert required_event in events
    assert stages == ["sense", "model", "decide", "act", "verify", "learn"]


def test_closed_loop_orchestrator_contract() -> None:
    module = _load_module(
        ROOT / "scripts" / "recruitment_closed_loop.py",
        "recruitment_closed_loop",
    )
    result = module.run_recruitment_closed_loop(
        [
            {"candidate_id": "c1", "total_score": 9.1},
            {"candidate_id": "c2", "total_score": 6.2},
        ]
    )
    assert isinstance(result, dict)
    assert "screening" in result
    assert "interview" in result
    assert "evaluation" in result
    assert "notifications" in result
    assert "events" in result
    assert "screening_completed" in result["events"]
    assert "ai_interview_completed" in result["events"]
