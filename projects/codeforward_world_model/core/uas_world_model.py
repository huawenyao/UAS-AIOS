"""
UAS World Model - 重新设计

定位：UAS 元Agent 的认知引擎组件
- 不独立运行
- 提供目标理解、动态规划、系统建模能力
- 被 UAS Intent/Planning/AgentFabric 调用
"""

import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


class WMCapability(Enum):
    """World Model 能力枚举"""

    INTENT_UNDERSTANDING = "intent_understanding"
    GOAL_DECOMPOSITION = "goal_decomposition"
    DYNAMIC_PLANNING = "dynamic_planning"
    SYSTEM_MODELING = "system_modeling"
    CONTEXT_REASONING = "context_reasoning"
    DRIFT_DETECTION = "drift_detection"


@dataclass
class WMInput:
    """World Model 输入"""

    capability: WMCapability
    raw_input: str = ""
    context: dict = field(default_factory=dict)
    constraints: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class WMOutput:
    """World Model 输出"""

    capability: WMCapability
    success: bool
    data: dict = field(default_factory=dict)
    reasoning: str = ""
    confidence: float = 0.0
    metadata: dict = field(default_factory=dict)


class WorldModelInterface(ABC):
    """
    World Model 抽象接口

    被 UAS 元Agent 调用，提供认知能力
    """

    @abstractmethod
    def invoke(self, input: WMInput) -> WMOutput:
        """
        统一调用入口

        根据 capability 分发到具体能力
        """
        pass

    @abstractmethod
    def understand_intent(self, raw_input: str, context: dict = None) -> WMOutput:
        """目标理解能力"""
        pass

    @abstractmethod
    def decompose_goal(self, goal: str, context: dict = None) -> WMOutput:
        """目标分解能力"""
        pass

    @abstractmethod
    def plan(
        self, goal: str, context: dict, available_actions: list = None
    ) -> WMOutput:
        """动态规划能力"""
        pass

    @abstractmethod
    def model_system(self, system_description: str, context: dict = None) -> WMOutput:
        """系统建模能力"""
        pass

    @abstractmethod
    def detect_drift(
        self, expected: Any, actual: Any, context: dict = None
    ) -> WMOutput:
        """漂移检测能力"""
        pass


class UASWorldModel(WorldModelInterface):
    """
    UAS World Model 实现

    作为 UAS 元Agent 的认知引擎组件
    """

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.capabilities = {}

        # 加载子能力模块
        self._init_capabilities()

    def _init_capabilities(self):
        """初始化能力组件"""
        # 延迟导入，避免循环依赖
        try:
            from intent_understanding import IntentUnderstanding
            from knowledge_base import HybridKnowledgeBase
            from planning_engine import PlanningDrivenReasoning
            from knowledge_evolution import KnowledgeGraphEvolver
        except ImportError:
            from .intent_understanding import IntentUnderstanding
            from .knowledge_base import HybridKnowledgeBase
            from .planning_engine import PlanningDrivenReasoning
            from .knowledge_evolution import KnowledgeGraphEvolver

        self.capabilities = {
            WMCapability.INTENT_UNDERSTANDING: IntentUnderstanding(),
            WMCapability.GOAL_DECOMPOSITION: GoalDecomposer(),
            WMCapability.DYNAMIC_PLANNING: PlanningEngineWrapper(),
            WMCapability.SYSTEM_MODELING: SystemModeler(),
            WMCapability.CONTEXT_REASONING: HybridKnowledgeBase(),
            WMCapability.DRIFT_DETECTION: KnowledgeGraphEvolver(),
        }

    def invoke(self, input: WMInput) -> WMOutput:
        """统一调用入口"""
        capability_map = {
            WMCapability.INTENT_UNDERSTANDING: self.understand_intent,
            WMCapability.GOAL_DECOMPOSITION: self.decompose_goal,
            WMCapability.DYNAMIC_PLANNING: self.plan,
            WMCapability.SYSTEM_MODELING: self.model_system,
            WMCapability.DRIFT_DETECTION: self.detect_drift,
        }

        handler = capability_map.get(input.capability)
        if handler:
            return handler(input.raw_input, input.context)

        return WMOutput(
            capability=input.capability,
            success=False,
            reasoning=f"Unknown capability: {input.capability}",
        )

    def understand_intent(self, raw_input: str, context: dict = None) -> WMOutput:
        """目标理解"""
        handler = self.capabilities.get(WMCapability.INTENT_UNDERSTANDING)

        try:
            analysis = handler.understand(raw_input, context)

            return WMOutput(
                capability=WMCapability.INTENT_UNDERSTANDING,
                success=True,
                data={
                    "intent_id": analysis.intent.id,
                    "normalized": analysis.intent.normalized,
                    "constraints": analysis.intent.constraints,
                    "goals": analysis.intent.goals,
                    "entities": analysis.intent.entities,
                    "vector": analysis.intent.vector,
                },
                reasoning=analysis.reasoning,
                confidence=analysis.confidence,
            )
        except Exception as e:
            return WMOutput(
                capability=WMCapability.INTENT_UNDERSTANDING,
                success=False,
                reasoning=str(e),
            )

    def decompose_goal(self, goal: str, context: dict = None) -> WMOutput:
        """目标分解"""
        handler = self.capabilities.get(WMCapability.GOAL_DECOMPOSITION)

        try:
            result = handler.decompose(goal, context or {})

            return WMOutput(
                capability=WMCapability.GOAL_DECOMPOSITION,
                success=True,
                data=result,
                reasoning="Goal decomposed into sub-goals",
            )
        except Exception as e:
            return WMOutput(
                capability=WMCapability.GOAL_DECOMPOSITION,
                success=False,
                reasoning=str(e),
            )

    def plan(
        self, goal: str, context: dict, available_actions: list = None
    ) -> WMOutput:
        """动态规划"""
        handler = self.capabilities.get(WMCapability.DYNAMIC_PLANNING)

        try:
            from .planning_engine import WorldState, Action

            current_state = WorldState(
                description=context.get("current_state", ""),
                attributes=context.get("state_attributes", {}),
            )

            goal_state = WorldState(
                description=goal, attributes=context.get("goal_attributes", {})
            )

            actions = []
            if available_actions:
                for a in available_actions:
                    actions.append(
                        Action(
                            name=a.get("name", ""),
                            description=a.get("description", ""),
                            cost=a.get("cost", 1.0),
                        )
                    )

            plan = handler.plan(current_state, goal_state, actions)

            return WMOutput(
                capability=WMCapability.DYNAMIC_PLANNING,
                success=True,
                data={
                    "selected_action": plan.selected_action.name
                    if plan.selected_action
                    else None,
                    "trajectories": len(plan.trajectories),
                    "reasoning": plan.reasoning,
                    "confidence": plan.confidence,
                },
                reasoning=plan.reasoning,
                confidence=plan.confidence,
            )
        except Exception as e:
            return WMOutput(
                capability=WMCapability.DYNAMIC_PLANNING,
                success=False,
                reasoning=str(e),
            )

    def model_system(self, system_description: str, context: dict = None) -> WMOutput:
        """系统建模"""
        handler = self.capabilities.get(WMCapability.SYSTEM_MODELING)

        try:
            model = handler.model(system_description, context or {})

            return WMOutput(
                capability=WMCapability.SYSTEM_MODELING,
                success=True,
                data=model,
                reasoning="System model generated",
            )
        except Exception as e:
            return WMOutput(
                capability=WMCapability.SYSTEM_MODELING, success=False, reasoning=str(e)
            )

    def detect_drift(
        self, expected: Any, actual: Any, context: dict = None
    ) -> WMOutput:
        """漂移检测"""
        handler = self.capabilities.get(WMCapability.DRIFT_DETECTION)

        try:
            event = handler.evolve(
                {
                    "expected": expected,
                    "actual": actual,
                    "related_entities": context.get("entities", []) if context else [],
                }
            )

            return WMOutput(
                capability=WMCapability.DRIFT_DETECTION,
                success=True,
                data={
                    "drift_detected": event.type != "no_drift",
                    "changes": event.changes,
                    "description": event.description,
                },
                reasoning=event.description,
            )
        except Exception as e:
            return WMOutput(
                capability=WMCapability.DRIFT_DETECTION, success=False, reasoning=str(e)
            )


# ==================== 子能力组件 ====================


class GoalDecomposer:
    """目标分解器"""

    def decompose(self, goal: str, context: dict) -> dict:
        """分解目标为子目标"""
        # 简化实现
        sub_goals = []

        # 基于关键词分解
        if "and" in goal.lower():
            parts = goal.lower().split("and")
            sub_goals = [{"goal": p.strip(), "type": "conjunctive"} for p in parts]
        elif "or" in goal.lower():
            parts = goal.lower().split("or")
            sub_goals = [{"goal": p.strip(), "type": "disjunctive"} for p in parts]
        else:
            sub_goals = [{"goal": goal, "type": "atomic"}]

        # 估计依赖关系
        dependencies = []
        for i, sg in enumerate(sub_goals):
            if i > 0:
                dependencies.append({"from": i - 1, "to": i, "type": "sequential"})

        return {
            "main_goal": goal,
            "sub_goals": sub_goals,
            "dependencies": dependencies,
            "estimated_steps": len(sub_goals),
        }


class PlanningEngineWrapper:
    """规划引擎包装器"""

    def __init__(self):
        try:
            from planning_engine import PlanningDrivenReasoning, LLMWorldModel
        except ImportError:
            from .planning_engine import PlanningDrivenReasoning, LLMWorldModel

        self.engine = PlanningDrivenReasoning(LLMWorldModel())

    def plan(self, current_state, goal_state, actions):
        return self.engine.plan(current_state, goal_state, actions)


class SystemModeler:
    """系统建模器"""

    def model(self, system_description: str, context: dict) -> dict:
        """生成系统模型"""
        # 提取系统组件
        components = []
        relations = []

        # 简单解析
        lines = system_description.split("\n")
        for line in lines:
            if ":" in line:
                parts = line.split(":")
                components.append(
                    {
                        "name": parts[0].strip(),
                        "type": "component",
                        "description": parts[1].strip() if len(parts) > 1 else "",
                    }
                )

        return {
            "system_description": system_description,
            "components": components,
            "relations": relations,
            "state_space": len(components),
            "model_type": "component_based",
        }


# ==================== UAS 调用接口 ====================


class UASWorldModelService:
    """
    UAS World Model 服务封装

    供 UAS 元Agent 统一调用
    """

    def __init__(self, config: dict = None):
        self.wm = UASWorldModel(config)

    def process_intent(self, raw_intent: str, context: dict = None) -> dict:
        """处理意图（UAS Intent Activation 调用）"""
        output = self.wm.understand_intent(raw_intent, context)
        return output.__dict__

    def create_plan(self, goal: str, context: dict, actions: list = None) -> dict:
        """创建规划（UAS Planning 调用）"""
        output = self.wm.plan(goal, context, actions)
        return output.__dict__

    def model_system(self, description: str, context: dict = None) -> dict:
        """系统建模（UAS AgentFabric 调用）"""
        output = self.wm.model_system(description, context)
        return output.__dict__

    def check_drift(self, expected: Any, actual: Any, context: dict = None) -> dict:
        """漂移检测（UAS Evolution 调用）"""
        output = self.wm.detect_drift(expected, actual, context)
        return output.__dict__


# 导出
__all__ = [
    "WMCapability",
    "WMInput",
    "WMOutput",
    "WorldModelInterface",
    "UASWorldModel",
    "UASWorldModelService",
]
