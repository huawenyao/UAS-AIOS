#!/usr/bin/env python3
"""
SelfPaw 蜂群认知智能体 - 工作流启动脚本

用法：
  echo '{"decision_topic": "是否接受某offer", "context": "..."}' | python swarm_run.py

或由 AI 通过 /swarmDecision 命令调用，AI 将根据 configs/swarm_workflow_config.json
执行三阶段工作流，并调用本脚本传递上下文。

本脚本输出工作流执行所需的上下文结构，供 AI 编排器使用。
"""
import json
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
CONFIG_PATH = WORKSPACE / "configs" / "swarm_workflow_config.json"


def get_workflow_context(decision_topic: str, context: str = "") -> dict:
    """生成蜂群工作流执行上下文"""
    return {
        "workflow": "swarm_workflow_config",
        "version": "v1.0",
        "decision_topic": decision_topic,
        "context": context,
        "stage1_vars": ["decision_topic", "context"],
        "stage2_vars": ["stage1_outputs", "stage2_output"],
        "stage3_vars": ["stage1_outputs", "stage2_output"],
        "methodology_ref": ".claude/skills/swarm_methodology.md",
        "opponent_matrix_ref": ".claude/skills/agent_opponent_matrix.md",
    }


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {"decision_topic": "未提供议题", "context": ""}

    topic = payload.get("decision_topic", "未提供议题")
    context = payload.get("context", "")

    ctx = get_workflow_context(topic, context)
    ctx["workflow_config_path"] = str(CONFIG_PATH)

    print(json.dumps(ctx, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
