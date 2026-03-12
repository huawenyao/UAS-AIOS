import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from asui.init import run_init


def test_triadic_swarm_template_creates_native_assets(tmp_path):
    target = tmp_path / "triadic-swarm"

    assert run_init(target, template="triadic-ideal-reality-swarm")

    expected_files = [
        "CLAUDE.md",
        "configs/workflow_config.json",
        "configs/swarm_agents.json",
        ".claude/skills/triadic_protocol.md",
        ".claude/skills/emergence_output_contract.md",
        "scripts/render_emergence_report.py",
        "reports/README.md",
    ]
    for relative_path in expected_files:
        assert (target / relative_path).exists(), relative_path

    workflow = json.loads((target / "configs" / "workflow_config.json").read_text(encoding="utf-8"))
    assert workflow["swarm"]["methodology"] == "macro-meso-micro-ideal-reality"
    assert workflow["steps"][-1]["script"] == "scripts/render_emergence_report.py"
    assert any(step["id"] == "scene_instantiation" for step in workflow["steps"])
    assert any(step["id"] == "cross_validation" for step in workflow["steps"])

    agents = json.loads((target / "configs" / "swarm_agents.json").read_text(encoding="utf-8"))
    assert len(agents["agents"]) == 9
    assert agents["governance"]["require_scene_activation"] is True
    assert agents["governance"]["require_cross_validation"] is True


def test_triadic_swarm_render_script_writes_report_and_decision(tmp_path):
    target = tmp_path / "triadic-swarm"
    assert run_init(target, template="triadic-ideal-reality-swarm")

    payload = {
        "topic": "industry-solution-and-work-style-emergence",
        "cross_validation": {
            "tensions": ["宏观目的要求协同，但中观流程仍然是烟囱式分工"],
            "validation_matrix": ["宏观生态目标必须能映射到中观流程接口与微观动作"],
        },
        "emergence_synthesis": {
            "purpose_anchor": ["把基础目的激活为真实场景中的协同造化"],
            "macro_ecology": ["行业生态由客户、伙伴、平台、监管与人才共同构成"],
            "meso_value_loops": ["围绕方案设计、交付、反馈形成闭环工作回路"],
            "micro_object_matrix": ["以具体的人为核心，连接角色、工具、对象、信号与动作"],
            "instantiated_entity_map": ["将角色映射到岗位、工具、审批节点与数据接口"],
            "ideal_reality_tensions": ["理念中的协同与现实中的割裂需要用场景机制桥接"],
            "validation_matrix": ["验证宏观目标、中观闭环、微观动作是否一致"],
            "product_definition": ["这是一个把基础目的转译为现实协同工作面的编排系统"],
            "experience_blueprint": ["用户先定义场景，再查看实体映射、验证矩阵和进化建议"],
            "technical_choices": ["采用 UAS 分层编排、工作流配置和结构化知识沉淀"],
            "activation_plan": ["先定义场景，再绑定目的，再重排流程与角色"],
            "emergence_solution": ["建立目的激活编排台与三维协同工作面"],
            "operating_mode": ["宏观定方向，中观定闭环，微观定动作与感知"],
            "key_entities": ["人", "组织单元", "工作对象", "信号", "规则"],
            "evaluation_metrics": ["闭环完成率", "角色协同响应时间", "目的偏移率"],
            "iteration_loop": ["验证失败时回到实例化与中观闭环层重构"],
            "retrospective_triggers": ["角色割裂重复出现", "场景目标连续两周无法达成"],
        },
    }

    result = subprocess.run(
        [sys.executable, str(target / "scripts" / "render_emergence_report.py")],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        cwd=target,
        check=True,
    )

    output = json.loads(result.stdout)
    report_path = target / output["report_path"]
    decision_path = target / output["decision_path"]

    assert report_path.exists()
    assert decision_path.exists()
    assert "三维理念现实涌现方案" in report_path.read_text(encoding="utf-8")
    assert "交叉验证矩阵" in report_path.read_text(encoding="utf-8")

    stored = json.loads(decision_path.read_text(encoding="utf-8"))
    assert stored["topic"] == payload["topic"]
    assert stored["emergence_synthesis"]["activation_plan"] == payload["emergence_synthesis"]["activation_plan"]
    assert stored["emergence_synthesis"]["technical_choices"] == payload["emergence_synthesis"]["technical_choices"]
