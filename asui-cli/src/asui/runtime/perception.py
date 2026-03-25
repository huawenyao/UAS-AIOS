"""感知模块 - Perception Module (L1)

负责多模态感知、时空建模、态势感知。
实现 L1 感知推理能力。
"""

from __future__ import annotations

from typing import Any


class PerceptionModule:
    """感知模块 - 从输入中提取信息。

    功能:
    - 多模态感知：文本、图像、语音等输入处理
    - 时空建模：时间、空间上下文提取
    - 态势感知：环境状态、关键实体识别
    """

    def process(self, input_data: dict) -> dict:
        """执行感知处理。

        Args:
            input_data: 输入数据字典

        Returns:
            感知结果
        """
        content = input_data.get("content", "")
        raw_input = input_data.get("raw_input", content)
        modality = input_data.get("modality", "text")

        # 1. 多模态感知处理
        entities = self._extract_entities(raw_input, modality)
        temporal_info = self._extract_temporal_info(raw_input)
        spatial_info = self._extract_spatial_info(raw_input)

        # 2. 态势感知
        situation = self._analyze_situation(
            entities,
            temporal_info,
            spatial_info,
        )

        # 3. 关键信号提取
        signals = self._extract_signals(raw_input, modality)

        return {
            "status": "perceived",
            "level": 1,  # L1 感知推理
            "entities": entities,
            "temporal": temporal_info,
            "spatial": spatial_info,
            "situation": situation,
            "signals": signals,
            "summary": f"感知到 {len(entities)} 个实体，{len(signals)} 个信号",
        }

    def _extract_entities(self, raw_input: str, modality: str) -> list[dict]:
        """提取实体。

        从输入中提取关键实体（人名、机构、概念等）。
        """
        entities = []

        # 基于关键词的简单实体提取
        # 实际实现中可接入 NER 模型
        keywords = ["用户", "客户", "系统", "Agent", "数据", "任务", "问题"]

        for keyword in keywords:
            if keyword in raw_input:
                entities.append({
                    "type": "keyword",
                    "value": keyword,
                    "source": "text",
                })

        return entities

    def _extract_temporal_info(self, raw_input: str) -> dict:
        """提取时间信息。"""
        temporal = {
            "has_time_reference": False,
            "urgency": "normal",  # low, normal, high, critical
        }

        # 检测紧急程度
        urgent_keywords = ["紧急", "立即", "马上", "urgent", "asap"]
        normal_keywords = ["尽快", "尽快", "soon"]
        low_keywords = ["不急", "以后", "later", "sometime"]

        for keyword in urgent_keywords:
            if keyword in raw_input:
                temporal["urgency"] = "high"
                temporal["has_time_reference"] = True
                break

        if temporal["urgency"] == "normal":
            for keyword in normal_keywords:
                if keyword in raw_input:
                    temporal["has_time_reference"] = True
                    break

        if temporal["urgency"] == "normal":
            for keyword in low_keywords:
                if keyword in raw_input:
                    temporal["urgency"] = "low"
                    temporal["has_time_reference"] = True
                    break

        return temporal

    def _extract_spatial_info(self, raw_input: str) -> dict:
        """提取空间/上下文信息。"""
        return {
            "has_location": False,
            "context_scope": "global",  # local, global
        }

    def _analyze_situation(
        self,
        entities: list[dict],
        temporal: dict,
        spatial: dict,
    ) -> dict:
        """分析态势。

        综合实体、时间、空间信息判断当前态势。
        """
        # 计算态势复杂度
        complexity = "simple"
        if len(entities) >= 5:
            complexity = "moderate"
        if len(entities) >= 10:
            complexity = "complex"

        return {
            "complexity": complexity,
            "entity_count": len(entities),
            "urgency": temporal.get("urgency", "normal"),
            "context_scope": spatial.get("context_scope", "global"),
        }

    def _extract_signals(self, raw_input: str, modality: str) -> list[dict]:
        """提取关键信号。

        识别输入中的关键信号（请求、问题、情感等）。
        """
        signals = []

        # 请求信号
        request_keywords = ["需要", "请", "帮", "要", "want", "need", "please"]
        for keyword in request_keywords:
            if keyword in raw_input.lower():
                signals.append({"type": "request", "value": keyword})
                break

        # 问题信号
        question_markers = ["？", "?", "怎么", "如何", "why", "how", "what"]
        for marker in question_markers:
            if marker in raw_input:
                signals.append({"type": "question", "value": marker})
                break

        # 情感信号
        positive_markers = ["好", "棒", "优秀", "great", "good", "excellent"]
        negative_markers = ["差", "糟", "问题", "bad", "issue", "problem"]

        for marker in positive_markers:
            if marker in raw_input:
                signals.append({"type": "sentiment", "value": "positive", "marker": marker})
                break
        if not any(s.get("type") == "sentiment" for s in signals):
            for marker in negative_markers:
                if marker in raw_input:
                    signals.append({"type": "sentiment", "value": "negative", "marker": marker})
                    break

        return signals