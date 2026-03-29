"""推理模块 - Reasoning Module (L3-L4)

负责逻辑推理、概率推理、因果推理。
实现 L3 逻辑推理和 L4 因果推理能力。
"""

from __future__ import annotations

from typing import Any


class ReasoningModule:
    """推理模块 - 逻辑与因果推理。

    功能:
    - L3 逻辑推理：基于规则的演绎推理
    - L4 因果推理：理解因果关系和影响链
    - L5 类比推理：跨领域知识迁移（与理解模块协作）

    推理策略:
    - 演绎推理：从一般到特殊
    - 归纳推理：从特殊到一般
    - 溯因推理：从结果到原因
    - 类比推理：从相似案例推断
    """

    # 推理方法映射
    REASONING_STRATEGIES = {
        "deductive": "演绎推理",
        "inductive": "归纳推理",
        "abductive": "溯因推理",
        "analogical": "类比推理",
    }

    def __init__(self) -> None:
        self.reasoning_history: list[dict] = []

    def process(
        self,
        understanding_result: dict,
        level: int = 3,
    ) -> dict:
        """执行推理处理。

        Args:
            understanding_result: 理解模块输出
            level: 推理层级 (3=逻辑推理, 4=因果推理)

        Returns:
            推理结果
        """
        intent = understanding_result.get("intent", {})
        knowledge_links = understanding_result.get("knowledge_links", [])
        contextual = understanding_result.get("contextual_understanding", {})

        reasoning_paths = []

        # L3: 逻辑推理 - 基于规则和知识链
        if level >= 3:
            logical_reasoning = self._logical_reasoning(
                intent,
                knowledge_links,
            )
            reasoning_paths.append(logical_reasoning)

        # L4: 因果推理 - 理解因果关系
        if level >= 4:
            causal_reasoning = self._causal_reasoning(
                intent,
                knowledge_links,
                contextual,
            )
            reasoning_paths.append(causal_reasoning)

        # 综合推理结果
        combined_reasoning = self._combine_reasoning(reasoning_paths)

        # 记录推理历史
        self.reasoning_history.append({
            "intent_type": intent.get("type"),
            "level": level,
            "paths": len(reasoning_paths),
            "confidence": combined_reasoning.get("confidence", 0.0),
        })

        return {
            "status": "reasoned",
            "level": level,
            "reasoning_paths": reasoning_paths,
            "combined": combined_reasoning,
            "confidence": combined_reasoning.get("confidence", 0.0),
            "requires_higher_level": combined_reasoning.get("requires_higher_level", False),
            "reasoning_gap": combined_reasoning.get("reasoning_gap"),
        }

    def _logical_reasoning(
        self,
        intent: dict,
        knowledge_links: list[dict],
    ) -> dict:
        """逻辑推理（L3）。

        基于规则和知识链进行演绎推理。
        """
        # 构建推理链
        reasoning_chain = []

        # 从意图开始
        if intent.get("type") != "unknown":
            reasoning_chain.append({
                "step": 1,
                "type": "premise",
                "content": f"意图类型: {intent['type']}",
            })

        # 遍历知识链接构建推理路径
        for i, link in enumerate(knowledge_links[:3]):  # 最多3步
            reasoning_chain.append({
                "step": i + 2,
                "type": "inference",
                "content": f"基于 {link.get('link_type')}: {link.get('source')}",
            })

        # 得出结论
        conclusion = self._derive_conclusion(intent, knowledge_links)

        return {
            "strategy": "deductive",
            "strategy_name": "演绎推理",
            "chain": reasoning_chain,
            "conclusion": conclusion,
            "confidence": min(0.7 + len(knowledge_links) * 0.1, 0.95),
            "supports_causal": len(knowledge_links) >= 2,
        }

    def _causal_reasoning(
        self,
        intent: dict,
        knowledge_links: list[dict],
        contextual: dict,
    ) -> dict:
        """因果推理（L4）。

        理解因果关系和影响链。
        """
        # 识别原因和结果
        causes = []
        effects = []

        # 从意图推断因果
        intent_type = intent.get("type")
        if intent_type == "request":
            causes.append("用户请求")
            effects.append("执行任务")
        elif intent_type == "question":
            causes.append("用户疑问")
            effects.append("提供答案")
        elif intent_type == "sentiment":
            causes.append("用户情感表达")
            effects.append("情感响应")

        # 从知识链接推断因果
        for link in knowledge_links:
            if link.get("link_type") == "domain":
                causes.append(f"领域: {link.get('domain')}")
                effects.append(f"触发{link.get('domain')}相关知识")

        # 构建因果链
        causal_chain = []
        if causes and effects:
            causal_chain = [
                {"node": c, "type": "cause"}
                for c in causes
            ] + [
                {"node": e, "type": "effect"}
                for e in effects
            ]

        # 分析因果强度
        causal_strength = self._calculate_causal_strength(
            len(causes),
            len(effects),
            contextual,
        )

        return {
            "strategy": "abductive",
            "strategy_name": "溯因推理",
            "causes": causes,
            "effects": effects,
            "causal_chain": causal_chain,
            "causal_strength": causal_strength,
            "confidence": causal_strength * 0.9,
            "requires_higher_level": causal_strength < 0.6,
            "reasoning_gap": "需要更多上下文" if causal_strength < 0.6 else None,
        }

    def _derive_conclusion(
        self,
        intent: dict,
        knowledge_links: list[dict],
    ) -> dict:
        """得出推理结论。"""
        intent_type = intent.get("type", "unknown")

        # 基于意图类型和知识链接生成结论
        if intent_type == "request":
            action = "执行操作"
            if any(l.get("link_type") == "domain" for l in knowledge_links):
                action = f"执行{knowledge_links[0].get('domain')}相关操作"
            return {"action": action, "next_phase": "planning"}

        elif intent_type == "question":
            return {"action": "提供信息", "next_phase": "planning"}

        elif intent_type == "sentiment":
            return {"action": "情感响应", "next_phase": "planning"}

        else:
            return {"action": "需要更多信息", "next_phase": "perception"}

    def _calculate_causal_strength(
        self,
        cause_count: int,
        effect_count: int,
        context: dict,
    ) -> float:
        """计算因果强度。

        基于原因数量、结果数量和上下文计算因果推断的可信度。
        """
        # 基础强度
        base = 0.3

        # 原因数量贡献
        cause_contribution = min(cause_count * 0.15, 0.3)

        # 结果数量贡献
        effect_contribution = min(effect_count * 0.15, 0.3)

        # 上下文贡献
        context_contribution = 0.1 if context.get("history_relevance", 0) > 0.5 else 0.0

        strength = base + cause_contribution + effect_contribution + context_contribution
        return min(strength, 0.95)

    def _combine_reasoning(self, reasoning_paths: list[dict]) -> dict:
        """综合多条推理路径的结果。"""
        if not reasoning_paths:
            return {
                "conclusion": {"action": "无法推理"},
                "confidence": 0.0,
                "requires_higher_level": True,
                "reasoning_gap": "缺乏推理输入",
            }

        # 合并置信度
        confidences = [p.get("confidence", 0.0) for p in reasoning_paths]
        combined_confidence = sum(confidences) / len(confidences)

        # 检查是否需要更高层级推理
        requires_higher = any(
            p.get("requires_higher_level", False) for p in reasoning_paths
        )

        # 合并结论
        conclusions = [p.get("conclusion", {}) for p in reasoning_paths]
        primary_conclusion = conclusions[0] if conclusions else {}

        return {
            "conclusion": primary_conclusion,
            "confidence": combined_confidence,
            "requires_higher_level": requires_higher,
            "reasoning_gap": "需要更多上下文进行因果推理" if requires_higher else None,
        }

    def analogical_reasoning(
        self,
        source_domain: dict,
        target_domain: dict,
    ) -> dict:
        """类比推理（L5）。

        跨领域知识迁移。
        """
        # 找出相似点
        similarities = []
        for key in source_domain:
            if key in target_domain:
                if source_domain[key] == target_domain[key]:
                    similarities.append({"property": key, "match": "exact"})
                else:
                    similarities.append({"property": key, "match": "partial"})

        # 推断目标域结论
        inferred = []
        if source_domain.get("conclusion"):
            inferred.append({
                "based_on": "类比",
                "source_conclusion": source_domain.get("conclusion"),
                "transfer": "可能适用于目标域",
            })

        return {
            "strategy": "analogical",
            "strategy_name": "类比推理",
            "similarities": similarities,
            "inferred": inferred,
            "confidence": min(0.5 + len(similarities) * 0.1, 0.8),
        }

    def get_reasoning_history(self) -> list[dict]:
        """获取推理历史。"""
        return self.reasoning_history.copy()