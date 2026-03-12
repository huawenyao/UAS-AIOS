"""三维理念现实涌现智能体群模板。"""

TRIADIC_IDEAL_REALITY_SWARM_TEMPLATE = {
    "CLAUDE.md": """# 三维理念现实涌现智能体群

## 系统概述

本项目采用“三维 × 理念现实”涌现范式：围绕宏观、中观、微观三个维度，分别建立理念智能体与现实智能体，并以“目的激活”为锚点，将基础目的转译为具体场景中的真实造化路径。

## 核心命令

- `/emerge [议题]` - 发起一次完整的三维理念现实涌现分析
- `/activate [议题ID]` - 重做目的激活与场景转译
- `/reshape [议题ID]` - 基于现实反馈重构三维方案

## 运作机制

1. **目的激活**：先提炼基础目的，再绑定到真实场景
2. **三维拆解**：宏观、中观、微观分别展开理念与现实的独立分析
3. **理念现实对冲**：每个维度都要完成理念与现实的互相校正
4. **涌现综合**：把目的、维度、实体、机制、工作方式综合成《三维理念现实涌现方案》

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/workflow_config.json` | 三维理念现实蜂群工作流定义 |
| `configs/swarm_agents.json` | 七大智能体角色、维度、对手盘与交付物 |
| `.claude/skills/triadic_protocol.md` | 三维理念现实执行协议 |
| `.claude/skills/emergence_output_contract.md` | 最终涌现方案输出契约 |

## 执行准则

- 目的先行：任何分析都必须先对齐基础目的，不允许只讨论现象
- 三维并行：宏观、中观、微观必须分开建模，不能互相替代
- 理念现实对照：每个维度都要同时看到应然与实然
- 场景激活：一切基础理念都必须转译为具体场景下的动作、实体和工作方式
""",
    ".claude/skills/triadic_protocol.md": """# 三维理念现实涌现协议

## 目的激活阶段

在进入三维拆解前，必须先输出《目的激活报告》：

1. 场景议题是什么
2. 基础目的是什么
3. 该目的在当前场景下的激活条件是什么
4. 哪些变量会导致“目的漂移”

## 第一阶段：三维拆解

六个智能体必须独立输出，不允许提前妥协：

1. 宏观理念智能体 → 《宏观理念报告》
2. 宏观现实智能体 → 《宏观现实报告》
3. 中观理念智能体 → 《中观理念报告》
4. 中观现实智能体 → 《中观现实报告》
5. 微观理念智能体 → 《微观理念报告》
6. 微观现实智能体 → 《微观现实报告》

## 第二阶段：理念现实对冲

必须完成三组质询：

- 宏观理念 vs 宏观现实：校正生态机制与整体约束
- 中观理念 vs 中观现实：校正价值回路与场景闭环
- 微观理念 vs 微观现实：校正具体人、物、信号、动作与工作方式

目的激活智能体必须全程监督，检查是否偏离基础目的。

## 第三阶段：涌现综合

必须形成以下产物：

1. 基础目的与场景激活方式
2. 宏观生态机制图
3. 中观价值回路与闭环流程
4. 微观实体矩阵与工作方式
5. 理念现实张力清单
6. 真实场景下的解决方案
7. 运行机制与评估指标
8. 复盘触发器

## 禁忌

- 不允许只谈宏观理念，不落到中观闭环与微观实体
- 不允许只看现实阻力，不回到基础目的
- 不允许把“人”简化成抽象角色而忽略其具体感知与动作
""",
    ".claude/skills/emergence_output_contract.md": """# 《三维理念现实涌现方案》输出契约

最终输出必须包含以下字段：

- `topic`: 当前议题
- `purpose_anchor`: 基础目的与场景激活锚点
- `macro_ecology`: 宏观生态要素、机制与整体关系
- `meso_value_loops`: 中观价值回路、闭环流程与关键场景
- `micro_object_matrix`: 微观实体、角色、物理对象与理念对象的融合矩阵
- `ideal_reality_tensions`: 各维度的理念现实张力
- `activation_plan`: 从基础目的到场景造化的激活路径
- `emergence_solution`: 最终解决方案与真实工作方式
- `operating_mode`: 运行机制、协作方式与治理规则
- `key_entities`: 必须被智能化建模的核心实体
- `scene_metrics`: 评估该方案是否成立的场景指标
- `retrospective_triggers`: 触发复盘与重构的信号
""",
    ".claude/agents/README.md": "# 三维智能体定义\n\n智能体元数据统一维护在 `configs/swarm_agents.json`，由工作流按 `agent_id` 引用。\n",
    ".claude/commands/README.md": "# 交互命令\n\n- `/emerge [议题]`：触发三维理念现实涌现分析\n- `/activate [议题ID]`：重做目的激活\n- `/reshape [议题ID]`：基于现实反馈重构方案\n",
    "configs/swarm_agents.json": """{
  "$schema": "https://asui.dev/schemas/workflow_config.schema.json",
  "version": "v1.0",
  "swarm_name": "triadic_ideal_reality_emergence_swarm",
  "methodology": "macro-meso-micro-ideal-reality",
  "governance": {
    "human_role": "purpose_orchestrator_only",
    "allow_purpose_drift": false,
    "require_scene_activation": true
  },
  "agents": [
    {
      "id": "purpose_anchor",
      "name": "目的激活智能体",
      "dimension": "purpose",
      "stance": "基础目的与场景激活监督者",
      "mission": "提炼基础目的，识别场景激活条件，防止理念漂移",
      "deliverable": "目的激活报告",
      "challenge_targets": ["macro_ideal", "macro_reality", "meso_ideal", "meso_reality", "micro_ideal", "micro_reality"]
    },
    {
      "id": "macro_ideal",
      "name": "宏观理念智能体",
      "dimension": "macro",
      "stance": "整体生态的应然机制设计者",
      "mission": "提炼生态整体要素、机制、秩序与演化方向",
      "deliverable": "宏观理念报告",
      "challenge_targets": ["macro_reality", "meso_ideal"]
    },
    {
      "id": "macro_reality",
      "name": "宏观现实智能体",
      "dimension": "macro",
      "stance": "生态整体的实然约束观察者",
      "mission": "识别生态中的真实参与者、资源、约束与外部变量",
      "deliverable": "宏观现实报告",
      "challenge_targets": ["macro_ideal", "meso_reality"]
    },
    {
      "id": "meso_ideal",
      "name": "中观理念智能体",
      "dimension": "meso",
      "stance": "价值回路与场景闭环设计者",
      "mission": "设计价值回路、解决方案闭环与理想工作方式",
      "deliverable": "中观理念报告",
      "challenge_targets": ["meso_reality", "micro_ideal"]
    },
    {
      "id": "meso_reality",
      "name": "中观现实智能体",
      "dimension": "meso",
      "stance": "场景流程与组织接口校验者",
      "mission": "还原真实流程、组织分工、工具数据与瓶颈",
      "deliverable": "中观现实报告",
      "challenge_targets": ["meso_ideal", "micro_reality"]
    },
    {
      "id": "micro_ideal",
      "name": "微观理念智能体",
      "dimension": "micro",
      "stance": "具体人-物-理念融合体的应然建模者",
      "mission": "刻画人、物、角色、理念对象在理想状态下的关系与工作方式",
      "deliverable": "微观理念报告",
      "challenge_targets": ["micro_reality", "meso_ideal"]
    },
    {
      "id": "micro_reality",
      "name": "微观现实智能体",
      "dimension": "micro",
      "stance": "具体人-物-信号-动作的实然观察者",
      "mission": "识别可感知的物理对象、行为、信号、限制与现实动作链",
      "deliverable": "微观现实报告",
      "challenge_targets": ["micro_ideal", "meso_reality"]
    }
  ],
  "pairings": [
    {
      "source": "macro_ideal",
      "target": "macro_reality",
      "challenge": "整体生态的应然机制是否脱离真实资源、规则和外部变量"
    },
    {
      "source": "meso_ideal",
      "target": "meso_reality",
      "challenge": "价值回路与场景闭环是否脱离真实组织流程与工作接口"
    },
    {
      "source": "micro_ideal",
      "target": "micro_reality",
      "challenge": "人的理念角色与现实动作链是否真正统一"
    },
    {
      "source": "purpose_anchor",
      "target": "all",
      "challenge": "各维度是否仍然服务于基础目的并完成场景激活"
    }
  ]
}
""",
    "configs/workflow_config.json": """{
  "$schema": "https://asui.dev/schemas/workflow_config.schema.json",
  "version": "v1.0",
  "name": "三维理念现实涌现蜂群工作流",
  "description": "基于宏观/中观/微观与理念/现实对冲的三阶段涌现工作流",
  "swarm": {
    "mode": "triadic-ideal-reality-swarm",
    "methodology": "macro-meso-micro-ideal-reality",
    "decision_policy": "purpose_activated_emergence",
    "agents": [
      { "id": "purpose_anchor", "name": "目的激活智能体", "dimension": "purpose", "stance": "目的监督者" },
      { "id": "macro_ideal", "name": "宏观理念智能体", "dimension": "macro", "stance": "生态应然设计者" },
      { "id": "macro_reality", "name": "宏观现实智能体", "dimension": "macro", "stance": "生态实然观察者" },
      { "id": "meso_ideal", "name": "中观理念智能体", "dimension": "meso", "stance": "价值回路设计者" },
      { "id": "meso_reality", "name": "中观现实智能体", "dimension": "meso", "stance": "流程现实校验者" },
      { "id": "micro_ideal", "name": "微观理念智能体", "dimension": "micro", "stance": "人-物-理念应然建模者" },
      { "id": "micro_reality", "name": "微观现实智能体", "dimension": "micro", "stance": "人-物-信号实然观察者" }
    ],
    "phases": [
      {
        "id": "purpose_activation",
        "name": "目的激活",
        "goal": "把基础目的绑定到具体场景与边界"
      },
      {
        "id": "triadic_scan",
        "name": "三维拆解",
        "goal": "三维理念现实独立输出，不提前混合"
      },
      {
        "id": "emergence",
        "name": "涌现综合",
        "goal": "把目的、维度、实体、流程与工作方式综合成真实方案"
      }
    ]
  },
  "global_config": {
    "required_sections": [
      "topic",
      "purpose_anchor",
      "macro_ecology",
      "meso_value_loops",
      "micro_object_matrix",
      "ideal_reality_tensions",
      "activation_plan",
      "emergence_solution",
      "operating_mode",
      "key_entities",
      "scene_metrics",
      "retrospective_triggers"
    ]
  },
  "steps": [
    {
      "id": "intake",
      "name": "议题归一化",
      "type": "llm",
      "description": "明确议题、场景、边界、目标对象与成功标准",
      "prompt_template": "请把以下议题归一化为结构化输入，至少包含场景、目标对象、约束、当前现实、预期涌现结果。\\n\\n{{topic}}",
      "swarm_mode": "topic_normalization"
    },
    {
      "id": "purpose_activation",
      "name": "目的激活",
      "type": "llm",
      "dependencies": ["intake"],
      "agent_id": "purpose_anchor",
      "agent_role": "基础目的与场景激活监督者",
      "deliverable": "目的激活报告",
      "prompt_template": "基于议题输入，提炼基础目的、场景激活条件、目的漂移风险与必须守住的底线。\\n\\n输入：{{intake}}"
    },
    {
      "id": "triadic_scan",
      "name": "三维拆解",
      "type": "parallel",
      "dependencies": ["purpose_activation"],
      "description": "六个维度智能体并行独立输出",
      "parallel_steps": [
        "macro_ideal_report",
        "macro_reality_report",
        "meso_ideal_report",
        "meso_reality_report",
        "micro_ideal_report",
        "micro_reality_report"
      ]
    },
    {
      "id": "macro_ideal_report",
      "name": "宏观理念报告",
      "type": "llm",
      "agent_id": "macro_ideal",
      "agent_role": "生态应然设计者",
      "deliverable": "宏观理念报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在宏观理念层，提炼整体生态的目的结构、关键要素、作用机制、秩序原则与演化方向。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "macro_reality_report",
      "name": "宏观现实报告",
      "type": "llm",
      "agent_id": "macro_reality",
      "agent_role": "生态实然观察者",
      "deliverable": "宏观现实报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在宏观现实层，识别真实生态中的参与者、资源、规则、外部变量、结构性约束与现实演化趋势。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "meso_ideal_report",
      "name": "中观理念报告",
      "type": "llm",
      "agent_id": "meso_ideal",
      "agent_role": "价值回路设计者",
      "deliverable": "中观理念报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在中观理念层，设计价值回路、场景闭环流程、理想解决方案与应有工作方式。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "meso_reality_report",
      "name": "中观现实报告",
      "type": "llm",
      "agent_id": "meso_reality",
      "agent_role": "流程现实校验者",
      "deliverable": "中观现实报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在中观现实层，还原真实流程、组织接口、工具链、数据流、瓶颈与断点。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "micro_ideal_report",
      "name": "微观理念报告",
      "type": "llm",
      "agent_id": "micro_ideal",
      "agent_role": "人-物-理念应然建模者",
      "deliverable": "微观理念报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在微观理念层，刻画人、物、角色、理念对象的融合体，定义其应有状态、感知、动作与工作方式。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "micro_reality_report",
      "name": "微观现实报告",
      "type": "llm",
      "agent_id": "micro_reality",
      "agent_role": "人-物-信号实然观察者",
      "deliverable": "微观现实报告",
      "dependencies": ["purpose_activation"],
      "prompt_template": "站在微观现实层，识别具体的人、物理对象、信号、动作链、限制条件与真实交互。\\n\\n目的激活：{{purpose_activation}}"
    },
    {
      "id": "ideal_reality_debate",
      "name": "理念现实对冲",
      "type": "llm",
      "dependencies": [
        "macro_ideal_report",
        "macro_reality_report",
        "meso_ideal_report",
        "meso_reality_report",
        "micro_ideal_report",
        "micro_reality_report"
      ],
      "description": "三维内部及跨维度完成理念现实对冲",
      "swarm_mode": "cross_examination",
      "prompt_template": "请组织三组理念现实对冲，并补充跨维度张力：\\n1. 宏观理念 vs 宏观现实\\n2. 中观理念 vs 中观现实\\n3. 微观理念 vs 微观现实\\n4. 目的激活是否被偏离\\n\\n宏观理念：{{macro_ideal_report}}\\n\\n宏观现实：{{macro_reality_report}}\\n\\n中观理念：{{meso_ideal_report}}\\n\\n中观现实：{{meso_reality_report}}\\n\\n微观理念：{{micro_ideal_report}}\\n\\n微观现实：{{micro_reality_report}}"
    },
    {
      "id": "emergence_synthesis",
      "name": "涌现综合",
      "type": "llm",
      "dependencies": ["ideal_reality_debate", "purpose_activation"],
      "description": "输出《三维理念现实涌现方案》",
      "prompt_template": "基于目的激活报告与理念现实对冲结果，输出《三维理念现实涌现方案》。必须覆盖宏观生态、中观价值回路、微观实体矩阵、张力清单、场景激活路径、真实工作方式与评估指标。\\n\\n目的激活：{{purpose_activation}}\\n\\n对冲结果：{{ideal_reality_debate}}",
      "output_schema": {
        "type": "object",
        "properties": {
          "topic": { "type": "string" },
          "purpose_anchor": { "type": "array", "items": { "type": "string" } },
          "macro_ecology": { "type": "array", "items": { "type": "string" } },
          "meso_value_loops": { "type": "array", "items": { "type": "string" } },
          "micro_object_matrix": { "type": "array", "items": { "type": "string" } },
          "ideal_reality_tensions": { "type": "array", "items": { "type": "string" } },
          "activation_plan": { "type": "array", "items": { "type": "string" } },
          "emergence_solution": { "type": "array", "items": { "type": "string" } },
          "operating_mode": { "type": "array", "items": { "type": "string" } },
          "key_entities": { "type": "array", "items": { "type": "string" } },
          "scene_metrics": { "type": "array", "items": { "type": "string" } },
          "retrospective_triggers": { "type": "array", "items": { "type": "string" } }
        },
        "required": [
          "topic",
          "purpose_anchor",
          "macro_ecology",
          "meso_value_loops",
          "micro_object_matrix",
          "ideal_reality_tensions",
          "activation_plan",
          "emergence_solution",
          "operating_mode",
          "key_entities",
          "scene_metrics",
          "retrospective_triggers"
        ]
      }
    },
    {
      "id": "render_report",
      "name": "写入涌现报告",
      "type": "script",
      "dependencies": ["emergence_synthesis"],
      "description": "将涌现输出落盘为 JSON 与 Markdown 报告",
      "script": "scripts/render_emergence_report.py"
    }
  ]
}
""",
    "scripts/README.md": "# 执行脚本\n\n- `render_emergence_report.py`：将三维理念现实涌现输出写入 `database/emergence/` 与 `reports/`\n",
    "scripts/render_emergence_report.py": """#!/usr/bin/env python3
\"\"\"渲染三维理念现实涌现结果。\"\"\"

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "emergence"


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def section(title: str, items) -> str:
    values = ensure_list(items)
    if not values:
        return f"## {title}\\n- 暂无\\n"
    bullet_lines = "\\n".join(f"- {item}" for item in values)
    return f"## {title}\\n{bullet_lines}\\n"


def main() -> int:
    payload = json.load(sys.stdin)
    topic = str(payload.get("topic", "emergence"))
    synthesis = payload.get("emergence_synthesis", payload)
    debate = payload.get("ideal_reality_debate", {})

    slug = slugify(topic)
    report_dir = Path("reports")
    decision_dir = Path("database") / "emergence"
    report_dir.mkdir(parents=True, exist_ok=True)
    decision_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{slug}.md"
    decision_path = decision_dir / f"{slug}.json"

    markdown = [
        f"# 三维理念现实涌现方案：{topic}",
        "",
        section("基础目的与激活锚点", synthesis.get("purpose_anchor")),
        section("宏观生态机制", synthesis.get("macro_ecology")),
        section("中观价值回路", synthesis.get("meso_value_loops")),
        section("微观实体矩阵", synthesis.get("micro_object_matrix")),
        section("理念现实张力", synthesis.get("ideal_reality_tensions") or debate.get("tensions")),
        section("场景激活路径", synthesis.get("activation_plan")),
        section("涌现解决方案", synthesis.get("emergence_solution")),
        section("运行机制", synthesis.get("operating_mode")),
        section("关键实体", synthesis.get("key_entities")),
        section("场景指标", synthesis.get("scene_metrics")),
        section("复盘触发器", synthesis.get("retrospective_triggers")),
    ]

    report_path.write_text("\\n".join(markdown), encoding="utf-8")

    stored_payload = {
        "topic": topic,
        "ideal_reality_debate": debate,
        "emergence_synthesis": synthesis,
    }
    decision_path.write_text(
        json.dumps(stored_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "written",
                "report_path": str(report_path),
                "decision_path": str(decision_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    "database/README.md": "# 数据持久化\n\n三维理念现实涌现结果会写入 `database/emergence/`。\n",
    "reports/README.md": "# 报告目录\n\nMarkdown 版《三维理念现实涌现方案》会输出到这里。\n",
}
