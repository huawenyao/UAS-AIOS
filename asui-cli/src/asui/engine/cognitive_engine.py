"""认知引擎核心 - Cognitive Agent V3.0

整合感知、理解、推理、规划、执行、反思六大模块，
实现多层次推理能力（L1-L6）和自主学习机制。
"""

from __future__ import annotations

from typing import Any

from .perception import PerceptionModule
from .understanding import UnderstandingModule
from .reasoning import ReasoningModule
from .planning import PlanningModule
from .execution import ExecutionModule
from .reflection import ReflectionModule


class CognitiveEngine:
    """认知引擎主控制器 - 整合六大模块实现完整认知闭环。

    认知流程:
    感知(P) → 理解(U) → 推理(R) → 规划(P) → 执行(E) → 反思(F)
                        ↑                                    │
                        └─────────── 反馈循环 ──────────────┘
    """

    def __init__(
        self,
        app_root: Any,
        configs: dict | None = None,
    ) -> None:
        """初始化认知引擎。

        Args:
            app_root: 应用根目录路径
            configs: 可选的配置字典
        """
        self.app_root = app_root
        self.configs = configs or {}

        # 初始化六大模块
        self.perception = PerceptionModule()
        self.understanding = UnderstandingModule()
        self.reasoning = ReasoningModule()
        self.planning = PlanningModule()
        self.execution = ExecutionModule()
        self.reflection = ReflectionModule(app_root)

        # 认知状态追踪
        self._cognitive_state: dict = {
            "level": 1,  # 当前推理层级 L1-L6
            "history": [],  # 认知历史
            "metacognitive_notes": [],  # 元认知笔记
        }

    def process(self, input_data: dict) -> dict:
        """执行完整认知流程。

        Args:
            input_data: 输入数据，包含:
                - content: 输入内容
                - context: 上下文信息
                - intent: 意图（如有）

        Returns:
            认知处理结果
        """
        # L1: 感知 - 多模态感知与信息提取
        perception_result = self.perception.process(input_data)

        # L2: 理解 - 语义理解与意图消歧
        understanding_result = self.understanding.process(
            perception_result,
            input_data.get("context", {}),
        )

        # L3-L4: 推理 - 逻辑与因果推理
        reasoning_result = self.reasoning.process(
            understanding_result,
            level=self._cognitive_state["level"],
        )

        # L5: 规划 - 目标拆解与路径规划
        planning_result = self.planning.process(
            reasoning_result,
            context=input_data.get("context", {}),
        )

        # 执行 - 任务调度与工具编排
        execution_result = self.execution.process(
            planning_result,
            context=input_data.get("context", {}),
        )

        # L6: 反思 - 结果评估与策略优化
        reflection_result = self.reflection.process(
            execution_result,
            self._cognitive_state,
        )

        # 更新认知状态
        self._update_cognitive_state(
            perception=perception_result,
            understanding=understanding_result,
            reasoning=reasoning_result,
            planning=planning_result,
            execution=execution_result,
            reflection=reflection_result,
        )

        return {
            "status": "completed",
            "perception": perception_result,
            "understanding": understanding_result,
            "reasoning": reasoning_result,
            "planning": planning_result,
            "execution": execution_result,
            "reflection": reflection_result,
            "cognitive_state": self._cognitive_state,
        }

    def _update_cognitive_state(
        self,
        perception: dict,
        understanding: dict,
        reasoning: dict,
        planning: dict,
        execution: dict,
        reflection: dict,
    ) -> None:
        """更新认知状态。

        根据反思结果调整推理层级(L1-L6)，实现元认知能力。
        """
        # 记录到历史
        self._cognitive_state["history"].append({
            "perception": perception.get("summary"),
            "understanding": understanding.get("intent"),
            "reasoning_level": reasoning.get("level"),
            "plan_size": len(planning.get("steps", [])),
            "execution_status": execution.get("status"),
            "reflection_quality": reflection.get("quality", "unknown"),
        })

        # 元认知：根据反思结果调整推理层级
        if reflection.get("requires_higher_level_reasoning"):
            self._cognitive_state["level"] = min(
                self._cognitive_state["level"] + 1,
                6  # 最高到 L6 元认知
            )
            self._cognitive_state["metacognitive_notes"].append(
                f"升级推理层级到 L{self._cognitive_state['level']}：{reflection.get('reasoning_gap')}"
            )
        elif reflection.get("needs_retry"):
            self._cognitive_state["metacognitive_notes"].append(
                f"需要重试：{reflection.get('retry_reason')}"
            )

    def get_cognitive_state(self) -> dict:
        """获取当前认知状态。"""
        return self._cognitive_state.copy()

    def reset(self) -> None:
        """重置认知状态。"""
        self._cognitive_state = {
            "level": 1,
            "history": [],
            "metacognitive_notes": [],
        }