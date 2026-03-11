"""selfpaw 原生认知蜂群模板。"""

SELFPAW_SWARM_TEMPLATE = {
    "CLAUDE.md": """# selfpaw 原生认知智能体蜂群

## 系统概述

本项目采用 selfpaw 原生蜂群范式：不优化单点认知，而是用五个立场独立、彼此对冲的认知智能体完成“否定之否定”的辩证升维。

## 核心命令

- `/dialectic [议题]` - 发起一次完整的蜂群辩证决策
- `/challenge [议题ID]` - 对既有结论追加第二次否定
- `/retrospective [议题ID]` - 基于实际结果做蜂群复盘

## 运作机制

1. **第一次否定**：五个智能体独立拆解问题，拒绝在个人原始判断内修补
2. **第二次否定**：认知对手盘交叉质询、暴露冲突与盲区
3. **辩证融合**：中立观察者统筹共识、冲突与修订，输出《全维度辩证决策方案》

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/workflow_config.json` | selfpaw 蜂群工作流定义 |
| `configs/swarm_agents.json` | 五大智能体角色、立场、对手盘与交付物 |
| `.claude/skills/swarm_protocol.md` | 否定之否定的执行规则 |
| `.claude/skills/decision_output_contract.md` | 最终决策方案输出契约 |

## 执行准则

- 立场隔离：每个智能体只为自己的维度负责，不预设统一答案
- 升维锁定：最终以蜂群融合结论为准，人类仅做执行统筹
- 持续迭代：每次执行后必须复盘，更新盲区与博弈策略
- 分布式运行：任何单一智能体都不能垄断最终结论
""",
    ".claude/skills/swarm_protocol.md": """# 蜂群辩证协议

## 第一阶段：第一次否定

五个智能体必须独立输出，不允许提前协商：

1. 用户视角智能体 → 《用户真实需求报告》
2. 关卡障碍智能体 → 《关卡与风险清单》
3. 核心决策智能体 → 《初始决策方案》
4. 买单价值智能体 → 《价值与成本评估》
5. 博弈观察智能体 → 《外部博弈格局》

## 第二阶段：第二次否定

认知对手盘执行公开质询：

- 用户视角智能体优先质疑“忽视真实体验”的方案
- 关卡障碍智能体优先质疑“不可执行”的乐观判断
- 核心决策智能体优先质疑“偏离目标”的冗余分析
- 买单价值智能体优先质疑“超出支付阈值”的高成本方案
- 博弈观察智能体只记录，不站队，不直接拍板

## 第三阶段：辩证融合

必须形成以下产物：

1. 统一议题定义
2. 共识清单
3. 核心冲突清单
4. 修订后的执行路径
5. 风险预案
6. 用户适配方案
7. 成本把控细则
8. 博弈应对策略

## 禁忌

- 不允许跳过对手盘质询直接综合
- 不允许以个人偏好推翻蜂群共识
- 不允许让观察智能体提前偏向某一立场
""",
    ".claude/skills/decision_output_contract.md": """# 《全维度辩证决策方案》输出契约

最终输出必须包含以下字段：

- `topic`: 当前决策议题
- `final_decision`: 最终结论
- `execution_path`: 分阶段执行路径
- `risk_preplan`: 主要风险与预案
- `user_adaptation`: 用户适配与体验策略
- `cost_controls`: 成本、价值与买单阈值控制项
- `game_response`: 对外部博弈与变量变化的应对策略
- `consensus`: 蜂群共识
- `open_conflicts`: 尚待观察的冲突点
- `retrospective_triggers`: 触发复盘的信号
""",
    ".claude/agents/README.md": "# 认知智能体定义\n\n智能体元数据统一维护在 `configs/swarm_agents.json`，由工作流按 `agent_id` 引用。\n",
    ".claude/commands/README.md": "# 交互命令\n\n- `/dialectic [议题]`：触发三阶段蜂群辩证\n- `/challenge [议题ID]`：复跑第二次否定\n- `/retrospective [议题ID]`：基于结果复盘并更新蜂群知识\n",
    "configs/swarm_agents.json": """{
  "$schema": "https://asui.dev/schemas/workflow_config.schema.json",
  "version": "v1.0",
  "swarm_name": "selfpaw_native_cognitive_swarm",
  "methodology": "negation-of-negation",
  "governance": {
    "human_role": "execution_orchestrator_only",
    "allow_personal_override": false,
    "observer_must_remain_neutral": true
  },
  "agents": [
    {
      "id": "user_view",
      "name": "用户视角智能体",
      "dimension": "user",
      "stance": "终端用户/需求方",
      "mission": "还原显性需求、隐性痛点、情绪偏好与拒绝理由",
      "deliverable": "用户真实需求报告",
      "challenge_targets": ["decision_core", "payer_value"]
    },
    {
      "id": "obstacle_gate",
      "name": "关卡障碍智能体",
      "dimension": "gate",
      "stance": "极致理性的风险把控者",
      "mission": "拆解关卡、约束、失败场景与资源短板",
      "deliverable": "关卡与风险清单",
      "challenge_targets": ["decision_core", "observer_referee"]
    },
    {
      "id": "decision_core",
      "name": "核心决策智能体",
      "dimension": "decision",
      "stance": "目标达成与执行效率优先",
      "mission": "制定初始执行路径并锚定核心目标",
      "deliverable": "初始决策方案",
      "challenge_targets": ["user_view", "obstacle_gate"]
    },
    {
      "id": "payer_value",
      "name": "买单价值智能体",
      "dimension": "payer",
      "stance": "投入产出与支付意愿守门人",
      "mission": "评估价值兑现、成本边界与买单阈值",
      "deliverable": "价值与成本评估",
      "challenge_targets": ["decision_core", "user_view"]
    },
    {
      "id": "observer_referee",
      "name": "博弈观察智能体",
      "dimension": "observer",
      "stance": "中立第三方观察者",
      "mission": "记录外部变量、多方博弈、共识与冲突，不直接站队",
      "deliverable": "外部博弈格局",
      "challenge_targets": ["user_view", "obstacle_gate", "decision_core", "payer_value"]
    }
  ],
  "pairings": [
    {
      "source": "user_view",
      "target": "decision_core",
      "challenge": "方案是否忽视用户真实体验与采用门槛"
    },
    {
      "source": "obstacle_gate",
      "target": "decision_core",
      "challenge": "方案是否掩盖执行障碍与失败风险"
    },
    {
      "source": "payer_value",
      "target": "decision_core",
      "challenge": "方案是否超出价值兑现周期与成本阈值"
    },
    {
      "source": "observer_referee",
      "target": "all",
      "challenge": "各方是否忽略外部博弈变量与动态变化"
    }
  ]
}
""",
    "configs/workflow_config.json": """{
  "$schema": "https://asui.dev/schemas/workflow_config.schema.json",
  "version": "v1.0",
  "name": "selfpaw 原生认知蜂群工作流",
  "description": "基于否定之否定的三阶段蜂群决策工作流",
  "swarm": {
    "mode": "dialectical-swarm",
    "methodology": "negation-of-negation",
    "decision_policy": "observer_synthesized_consensus",
    "agents": [
      {
        "id": "user_view",
        "name": "用户视角智能体",
        "dimension": "user",
        "stance": "终端用户/需求方"
      },
      {
        "id": "obstacle_gate",
        "name": "关卡障碍智能体",
        "dimension": "gate",
        "stance": "风险把控者"
      },
      {
        "id": "decision_core",
        "name": "核心决策智能体",
        "dimension": "decision",
        "stance": "目标执行者"
      },
      {
        "id": "payer_value",
        "name": "买单价值智能体",
        "dimension": "payer",
        "stance": "价值与成本守门人"
      },
      {
        "id": "observer_referee",
        "name": "博弈观察智能体",
        "dimension": "observer",
        "stance": "中立观察者"
      }
    ],
    "phases": [
      {
        "id": "first_negation",
        "name": "第一次否定",
        "goal": "打破个人单一视角，形成五份独立报告"
      },
      {
        "id": "second_negation",
        "name": "第二次否定",
        "goal": "通过对手盘交叉质询暴露盲区与冲突"
      },
      {
        "id": "synthesis",
        "name": "辩证融合",
        "goal": "汇总共识、冲突与修订，输出最终决策方案"
      }
    ]
  },
  "global_config": {
    "required_sections": [
      "topic",
      "final_decision",
      "execution_path",
      "risk_preplan",
      "user_adaptation",
      "cost_controls",
      "game_response",
      "consensus",
      "open_conflicts",
      "retrospective_triggers"
    ]
  },
  "steps": [
    {
      "id": "intake",
      "name": "议题归一化",
      "type": "llm",
      "description": "明确目标、边界、时间窗与决策成功标准",
      "prompt_template": "请把以下议题归一化为结构化输入，包含目标、约束、时间窗、资源边界、成功标准。\\n\\n{{topic}}",
      "swarm_mode": "topic_normalization"
    },
    {
      "id": "first_negation",
      "name": "第一次否定",
      "type": "parallel",
      "dependencies": ["intake"],
      "description": "五个智能体并行独立输出，不提前妥协",
      "parallel_steps": [
        "user_report",
        "obstacle_report",
        "decision_report",
        "payer_report",
        "observer_report"
      ]
    },
    {
      "id": "user_report",
      "name": "用户真实需求报告",
      "type": "llm",
      "agent_id": "user_view",
      "agent_role": "终端用户/需求方",
      "deliverable": "用户真实需求报告",
      "dependencies": ["intake"],
      "prompt_template": "站在终端用户立场，输出显性需求、隐性痛点、采用障碍、情绪偏好、拒绝理由。\\n\\n输入：{{intake}}"
    },
    {
      "id": "obstacle_report",
      "name": "关卡与风险清单",
      "type": "llm",
      "agent_id": "obstacle_gate",
      "agent_role": "风险把控者",
      "deliverable": "关卡与风险清单",
      "dependencies": ["intake"],
      "prompt_template": "以极致保守视角拆解执行关卡、约束条件、失败场景、资源短板。\\n\\n输入：{{intake}}"
    },
    {
      "id": "decision_report",
      "name": "初始决策方案",
      "type": "llm",
      "agent_id": "decision_core",
      "agent_role": "目标执行者",
      "deliverable": "初始决策方案",
      "dependencies": ["intake"],
      "prompt_template": "以目标达成与效率优先视角输出初始决策路径、里程碑与资源配置。\\n\\n输入：{{intake}}"
    },
    {
      "id": "payer_report",
      "name": "价值与成本评估",
      "type": "llm",
      "agent_id": "payer_value",
      "agent_role": "价值与成本守门人",
      "deliverable": "价值与成本评估",
      "dependencies": ["intake"],
      "prompt_template": "测算投入产出、回报周期、支付意愿阈值与亏损风险。\\n\\n输入：{{intake}}"
    },
    {
      "id": "observer_report",
      "name": "外部博弈格局",
      "type": "llm",
      "agent_id": "observer_referee",
      "agent_role": "中立观察者",
      "deliverable": "外部博弈格局",
      "dependencies": ["intake"],
      "prompt_template": "站在第三方视角，分析多方利益关系、外部变量、对手动作与动态趋势。\\n\\n输入：{{intake}}"
    },
    {
      "id": "second_negation",
      "name": "第二次否定",
      "type": "llm",
      "dependencies": [
        "user_report",
        "obstacle_report",
        "decision_report",
        "payer_report",
        "observer_report"
      ],
      "description": "认知对手盘交叉质询，提炼共识、冲突与修订点",
      "swarm_mode": "cross_examination",
      "prompt_template": "请组织五个智能体完成公开质询。输出：共识、核心冲突、被证伪假设、修订建议、必须继续观察的变量。\\n\\n用户报告：{{user_report}}\\n\\n关卡报告：{{obstacle_report}}\\n\\n决策报告：{{decision_report}}\\n\\n买单报告：{{payer_report}}\\n\\n观察报告：{{observer_report}}"
    },
    {
      "id": "synthesis",
      "name": "辩证融合",
      "type": "llm",
      "dependencies": ["second_negation"],
      "description": "输出经过辩证检验的最终决策方案",
      "prompt_template": "基于第二次否定后的共识、冲突与修订点，输出《全维度辩证决策方案》。必须覆盖执行路径、风险预案、用户适配、成本把控、博弈应对、复盘触发条件。\\n\\n{{second_negation}}",
      "output_schema": {
        "type": "object",
        "properties": {
          "topic": { "type": "string" },
          "final_decision": { "type": "string" },
          "execution_path": {
            "type": "array",
            "items": { "type": "string" }
          },
          "risk_preplan": {
            "type": "array",
            "items": { "type": "string" }
          },
          "user_adaptation": {
            "type": "array",
            "items": { "type": "string" }
          },
          "cost_controls": {
            "type": "array",
            "items": { "type": "string" }
          },
          "game_response": {
            "type": "array",
            "items": { "type": "string" }
          },
          "consensus": {
            "type": "array",
            "items": { "type": "string" }
          },
          "open_conflicts": {
            "type": "array",
            "items": { "type": "string" }
          },
          "retrospective_triggers": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": [
          "topic",
          "final_decision",
          "execution_path",
          "risk_preplan",
          "user_adaptation",
          "cost_controls",
          "game_response",
          "consensus",
          "open_conflicts",
          "retrospective_triggers"
        ]
      }
    },
    {
      "id": "render_report",
      "name": "写入决策报告",
      "type": "script",
      "dependencies": ["synthesis"],
      "description": "将蜂群输出落盘为 JSON 与 Markdown 报告",
      "script": "scripts/render_decision.py"
    }
  ]
}
""",
    "scripts/README.md": "# 执行脚本\n\n- `render_decision.py`：将蜂群决策输出写入 `database/decisions/` 与 `reports/`\n",
    "scripts/render_decision.py": """#!/usr/bin/env python3
\"\"\"渲染 selfpaw 蜂群决策结果。\"\"\"

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r\"[^a-zA-Z0-9]+\", \"-\", value.strip().lower()).strip(\"-\")
    return normalized or \"decision\"


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def section(title: str, items) -> str:
    values = ensure_list(items)
    if not values:
        return f\"## {title}\\n- 暂无\\n\"
    bullet_lines = \"\\n\".join(f\"- {item}\" for item in values)
    return f\"## {title}\\n{bullet_lines}\\n\"


def main() -> int:
    payload = json.load(sys.stdin)
    topic = str(payload.get(\"topic\", \"decision\"))
    synthesis = payload.get(\"synthesis\", payload)
    debate = payload.get(\"second_negation\", {})

    slug = slugify(topic)
    report_dir = Path(\"reports\")
    decision_dir = Path(\"database\") / \"decisions\"
    report_dir.mkdir(parents=True, exist_ok=True)
    decision_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f\"{slug}.md\"
    decision_path = decision_dir / f\"{slug}.json\"

    markdown = [
        f\"# 全维度辩证决策方案：{topic}\",
        \"\",
        f\"**最终结论**：{synthesis.get('final_decision', '待补充')}\",
        \"\",
        section(\"蜂群共识\", synthesis.get(\"consensus\") or debate.get(\"consensus\")),
        section(\"核心冲突\", synthesis.get(\"open_conflicts\") or debate.get(\"conflicts\")),
        section(\"执行路径\", synthesis.get(\"execution_path\")),
        section(\"风险预案\", synthesis.get(\"risk_preplan\")),
        section(\"用户适配\", synthesis.get(\"user_adaptation\")),
        section(\"成本把控\", synthesis.get(\"cost_controls\")),
        section(\"博弈应对\", synthesis.get(\"game_response\")),
        section(\"复盘触发器\", synthesis.get(\"retrospective_triggers\")),
    ]

    report_path.write_text(\"\\n\".join(markdown), encoding=\"utf-8\")

    stored_payload = {
        \"topic\": topic,
        \"second_negation\": debate,
        \"synthesis\": synthesis,
    }
    decision_path.write_text(
        json.dumps(stored_payload, ensure_ascii=False, indent=2),
        encoding=\"utf-8\",
    )

    print(
        json.dumps(
            {
                \"status\": \"written\",
                \"report_path\": str(report_path),
                \"decision_path\": str(decision_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
""",
    "database/README.md": "# 数据持久化\n\n蜂群的结构化决策结果会写入 `database/decisions/`。\n",
    "reports/README.md": "# 报告目录\n\nMarkdown 版《全维度辩证决策方案》会输出到这里。\n",
}
