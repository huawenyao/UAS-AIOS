"""理解模块 - Understanding Module (L2)

负责意图消歧、上下文理解、知识关联。
实现 L2 理解推理能力。
"""

from __future__ import annotations


class UnderstandingModule:
    """理解模块 - 语义理解与意图消歧。

    功能:
    - 意图消歧：消除歧义，确定真实意图
    - 上下文理解：结合历史上下文理解含义
    - 知识关联：将输入与知识图谱关联
    """

    def process(self, perception_result: dict, context: dict) -> dict:
        """执行理解处理。

        Args:
            perception_result: 感知模块输出
            context: 上下文信息

        Returns:
            理解结果
        """
        entities = perception_result.get("entities", [])
        signals = perception_result.get("signals", [])
        situation = perception_result.get("situation", {})

        # 1. 意图识别与消歧
        intent = self._identify_intent(signals, situation, context)

        # 2. 上下文理解
        contextual_understanding = self._understand_context(
            intent,
            context,
        )

        # 3. 知识关联
        knowledge_links = self._link_knowledge(
            intent,
            entities,
            context,
        )

        # 4. 语义补全
        semantic_completion = self._semantic_completion(
            intent,
            knowledge_links,
        )

        return {
            "status": "understood",
            "level": 2,  # L2 理解推理
            "intent": intent,
            "contextual_understanding": contextual_understanding,
            "knowledge_links": knowledge_links,
            "semantic_completion": semantic_completion,
            "confidence": self._calculate_confidence(intent, knowledge_links),
        }

    def _identify_intent(
        self,
        signals: list[dict],
        situation: dict,
        context: dict,
    ) -> dict:
        """识别并消歧意图。

        基于信号和态势确定用户意图。
        """
        # 意图类型映射
        intent_types = {
            "request": ["查询", "执行", "创建", "更新", "删除"],
            "question": ["了解", "解释", "学习"],
            "sentiment": ["反馈", "评价", "抱怨", "表扬"],
        }

        primary_intent = "unknown"
        intent_details = {}

        # 从信号推断意图
        for signal in signals:
            signal_type = signal.get("type")
            if signal_type in intent_types:
                primary_intent = signal_type
                break

        # 结合态势信息
        if situation.get("urgency") == "high":
            intent_details["priority"] = "high"
            intent_details["requires_immediate_action"] = True
        else:
            intent_details["priority"] = "normal"

        # 从上下文推断意图
        if context.get("previous_intent"):
            intent_details["continuation"] = context["previous_intent"]

        return {
            "type": primary_intent,
            "details": intent_details,
            "raw_signals": signals,
        }

    def _understand_context(
        self,
        intent: dict,
        context: dict,
    ) -> dict:
        """理解上下文。

        结合历史和当前上下文深化理解。
        """
        understanding = {
            "context_window": context.get("window_size", 5),
            "history_relevance": 0.0,
            "context_dependencies": [],
        }

        # 评估历史相关性
        history = context.get("history", [])
        if history:
            # 简单计算：最近3条历史相关性
            relevant_count = min(3, len(history))
            understanding["history_relevance"] = relevant_count / 3.0
            understanding["context_dependencies"] = [
                f"history_{i}" for i in range(relevant_count)
            ]

        return understanding

    def _link_knowledge(
        self,
        intent: dict,
        entities: list[dict],
        context: dict,
    ) -> list[dict]:
        """知识关联。

        将识别的实体和意图与知识图谱关联。
        """
        links = []

        # 关联实体
        for entity in entities:
            links.append({
                "source": "entity",
                "entity": entity.get("value"),
                "type": entity.get("type"),
                "link_type": "direct",
            })

        # 关联意图类型
        intent_type = intent.get("type", "unknown")
        if intent_type != "unknown":
            links.append({
                "source": "intent",
                "intent_type": intent_type,
                "link_type": "intent_pattern",
            })

        # 关联上下文
        if context.get("domain"):
            links.append({
                "source": "context",
                "domain": context["domain"],
                "link_type": "domain",
            })

        return links

    def _semantic_completion(
        self,
        intent: dict,
        knowledge_links: list[dict],
    ) -> dict:
        """语义补全。

        基于知识关联补全语义信息。
        """
        completion = {
            "missing_info": [],
            "inferred": {},
            "ready_for_reasoning": len(knowledge_links) >= 2,
        }

        # 检查是否需要更多信息
        if len(knowledge_links) < 2:
            completion["missing_info"].append("需要更多上下文")

        # 推断缺失信息
        if intent.get("type") == "request" and not intent.get("details", {}).get("target"):
            completion["inferred"]["target"] = "inferred_from_context"

        return completion

    def _calculate_confidence(self, intent: dict, knowledge_links: list[dict]) -> float:
        """计算理解置信度。

        基于意图清晰度和知识关联度计算置信度。
        """
        # 基础置信度
        confidence = 0.5

        # 意图越明确置信度越高
        if intent.get("type") != "unknown":
            confidence += 0.2

        # 知识关联越多置信度越高
        if len(knowledge_links) >= 3:
            confidence += 0.2
        elif len(knowledge_links) >= 1:
            confidence += 0.1

        # 详细信息增加置信度
        if intent.get("details"):
            confidence += 0.1

        return min(confidence, 1.0)