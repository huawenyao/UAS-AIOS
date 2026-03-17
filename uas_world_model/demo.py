#!/usr/bin/env python3
"""
UAS World Model - Demo 示例

展示如何使用 UAS World Model 认知引擎
"""

import json
import sys
from pathlib import Path

# Add core module to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

# Import from core module
from uas_world_model import UASWorldModelService


def print_section(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


def demo_intent_understanding():
    """演示意图理解"""
    print_section("1. 意图理解演示")

    service = UASWorldModelService()

    test_inputs = [
        "优化招聘流程，确保3天内完成初筛",
        "构建自动化客服系统，必须支持多语言",
        "降低运营成本30%以上",
    ]

    for raw_input in test_inputs:
        print(f"\n输入: {raw_input}")
        result = service.process_intent(raw_input, {"domain": "business"})

        if result.get("success"):
            data = result.get("data", {})
            print(f"  归一化: {data.get('normalized', 'N/A')}")
            print(f"  约束: {data.get('constraints', [])}")
            print(f"  目标: {data.get('goals', [])}")
            print(f"  置信度: {result.get('confidence', 0):.2f}")
        else:
            print(f"  失败: {result.get('reasoning', 'Unknown error')}")


def demo_planning():
    """演示规划引擎"""
    print_section("2. 动态规划演示")

    service = UASWorldModelService()

    result = service.create_plan(
        goal="完成系统优化",
        context={
            "current_state": "人工处理",
            "state_attributes": {"效率": 30, "成本": 10000},
            "goal_attributes": {"效率": 90, "成本": 5000},
        },
        actions=[
            {"name": "自动化", "description": "流程自动化", "cost": 1.0},
            {"name": "并行化", "description": "任务并行处理", "cost": 1.5},
            {"name": "优化算法", "description": "算法优化", "cost": 2.0},
        ],
    )

    if result.get("success"):
        data = result.get("data", {})
        print(f"  规划结果:")
        print(f"    选中动作: {data.get('selected_action', 'N/A')}")
        print(f"    候选轨迹: {data.get('trajectories', 0)}")
        print(f"    置信度: {result.get('confidence', 0):.2f}")
        print(f"    推理: {result.get('reasoning', 'N/A')[:100]}...")


def demo_system_modeling():
    """演示系统建模"""
    print_section("3. 系统建模演示")

    service = UASWorldModelService()

    system_desc = """
用户系统: 用户注册 -> 身份验证 -> 权限分配
订单系统: 下单 -> 支付 -> 发货 -> 签收
客服系统: 接入 -> 问题分类 -> 处理 -> 反馈
"""

    result = service.model_system(system_desc, {"scale": "large"})

    if result.get("success"):
        data = result.get("data", {})
        print(f"  系统组件数: {data.get('state_space', 0)}")
        print(f"  模型类型: {data.get('model_type', 'N/A')}")
        components = data.get("components", [])
        print(f"  组件列表: {len(components)} 个")


def demo_drift_detection():
    """演示漂移检测"""
    print_section("4. 漂移检测演示")

    service = UASWorldModelService()

    test_cases = [
        {
            "expected": {"响应时间": 100, "成功率": 0.95},
            "actual": {"响应时间": 150, "成功率": 0.90},
            "context": {"entities": ["响应时间", "成功率"]},
        },
        {
            "expected": "success",
            "actual": "failed",
            "context": {"entities": ["任务执行"]},
        },
    ]

    for i, case in enumerate(test_cases):
        print(f"\n  测试用例 {i + 1}:")
        result = service.check_drift(case["expected"], case["actual"], case["context"])

        if result.get("success"):
            data = result.get("data", {})
            print(f"    漂移检测: {data.get('drift_detected', False)}")
            print(f"    描述: {result.get('reasoning', 'N/A')[:80]}...")


def demo_full_workflow():
    """演示完整工作流"""
    print_section("5. 完整工作流演示")

    service = UASWorldModelService()

    # Step 1: 意图理解
    print("\n  [Step 1] 意图理解")
    intent_result = service.process_intent(
        "构建AI招聘系统，自动筛选简历，3天内完成初筛"
    )
    print(f"    意图ID: {intent_result['data'].get('intent_id', 'N/A')[:8]}...")
    print(f"    归一化: {intent_result['data'].get('normalized', '')}")

    # Step 2: 规划
    print("\n  [Step 2] 动态规划")
    goal_text = intent_result["data"].get("normalized", "构建AI招聘系统")
    plan_result = service.create_plan(
        goal=goal_text,
        context={
            "current_state": "人工招聘",
            "state_attributes": {"自动化程度": 10},
            "goal_attributes": {"自动化程度": 90},
        },
        actions=[
            {"name": "简历解析", "cost": 1.0},
            {"name": "智能匹配", "cost": 1.5},
            {"name": "自动面试", "cost": 2.0},
        ],
    )
    print(f"    选中动作: {plan_result['data'].get('selected_action', 'N/A')}")
    print(f"    置信度: {plan_result.get('confidence', 0):.2f}")

    # Step 3: 漂移检测
    print("\n  [Step 3] 漂移检测")
    drift_result = service.check_drift(
        expected={"完成度": 100},
        actual={"完成度": 70},
        context={"entities": ["招聘流程"]},
    )
    print(f"    检测到漂移: {drift_result['data'].get('drift_detected', False)}")
    print(f"    建议: {drift_result.get('reasoning', 'N/A')[:60]}...")


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║         UAS World Model - 认知引擎演示                     ║
║                                                            ║
║  定位: UAS 元Agent 的认知引擎组件                         ║
║  功能: 目标理解 | 动态规划 | 系统建模 | 漂移检测          ║
╚════════════════════════════════════════════════════════════╝
    """)

    try:
        demo_intent_understanding()
        demo_planning()
        demo_system_modeling()
        demo_drift_detection()
        demo_full_workflow()

        print("\n" + "=" * 60)
        print("  演示完成!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
