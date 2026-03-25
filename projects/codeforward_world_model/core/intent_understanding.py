"""
UAS世界模型 - P0: LLM意图理解模块

功能：
- LLM语义理解
- 约束提取
- 目标归一化
- 向量嵌入
"""

import json
import re
import uuid
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, List


class IntentPriority(Enum):
    LOW = 0.3
    MEDIUM = 0.5
    HIGH = 0.7
    CRITICAL = 0.9


@dataclass
class Intent:
    """意图结构"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    raw_input: str = ""
    normalized: str = ""
    constraints: List = field(default_factory=list)
    success_criteria: List = field(default_factory=list)
    goals: List = field(default_factory=list)
    vector: List = field(default_factory=list)
    priority: float = 0.5
    entities: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict = field(default_factory=dict)


@dataclass
class IntentAnalysis:
    """意图分析结果"""

    intent: Intent
    confidence: float
    reasoning: str
    extracted_entities: dict
    extracted_constraints: List
    extracted_goals: List


class LLMInterface(ABC):
    """LLM接口抽象"""

    @abstractmethod
    def chat(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass


class OpenAILLM(LLMInterface):
    """OpenAI LLM实现"""

    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model

    def chat(self, prompt: str, **kwargs) -> str:
        return '{"analysis": "simulated", "confidence": 0.8}'

    def embed(self, text: str) -> List[float]:
        h = hashlib.md5(text.encode()).digest()
        return [b / 255.0 for b in h[:16]]


class IntentUnderstanding:
    """
    意图理解核心引擎

    功能：
    1. 语义理解：使用LLM解析原始输入
    2. 约束提取：从文本中提取must/cannot/without等约束
    3. 目标归一化：标准化意图表达
    4. 向量化：生成意图向量用于匹配
    """

    def __init__(self, llm: LLMInterface = None):
        self.llm = llm or OpenAILLM()
        self.constraint_patterns = [
            r"\b(must|have to|need to|required to)\b",
            r"\b(cannot|must not|should not|without)\b",
            r"\b(only|just|merely)\b",
            r"\b(limit|limited to|max|minimum)\b",
            r"\b(ensure|guarantee|make sure)\b",
        ]
        self.goal_patterns = [
            r"\b(achieve|accomplish|reach|attain)\b",
            r"\b(improve|optimize|enhance|maximize)\b",
            r"\b(reduce|decrease|minimize)\b",
            r"\b(create|build|develop|implement)\b",
            r"\b(solve|resolve|fix|address)\b",
        ]

    def understand(self, raw_input: str, context: dict = None) -> IntentAnalysis:
        """理解输入意图"""
        context = context or {}

        constraints = self._extract_constraints(raw_input)
        goals = self._extract_goals(raw_input)
        entities = self._extract_entities(raw_input)
        llm_analysis = self._llm_analyze(raw_input, context)
        normalized = self._normalize(raw_input, llm_analysis)
        vector = self._vectorize(normalized)

        intent = Intent(
            raw_input=raw_input,
            normalized=normalized,
            constraints=constraints,
            success_criteria=goals,
            goals=goals,
            vector=vector,
            priority=self._calculate_priority(raw_input),
            entities=entities,
            metadata=llm_analysis,
        )

        return IntentAnalysis(
            intent=intent,
            confidence=llm_analysis.get("confidence", 0.8),
            reasoning=llm_analysis.get("reasoning", ""),
            extracted_entities=entities,
            extracted_constraints=constraints,
            extracted_goals=goals,
        )

    def _extract_constraints(self, text: str) -> List[dict]:
        """提取约束"""
        constraints = []
        text_lower = text.lower()

        for pattern in self.constraint_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                constraints.append(
                    {
                        "type": self._classify_constraint(match.group()),
                        "text": match.group(),
                        "position": match.start(),
                    }
                )

        return constraints

    def _extract_goals(self, text: str) -> List[dict]:
        """提取目标"""
        goals = []
        text_lower = text.lower()

        for pattern in self.goal_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                goals.append(
                    {
                        "type": self._classify_goal(match.group()),
                        "text": match.group(),
                        "position": match.start(),
                    }
                )

        return goals

    def _classify_constraint(self, text: str) -> str:
        """分类约束类型"""
        if text in ["must", "have to", "need to", "required to"]:
            return "mandatory"
        elif text in ["cannot", "must not", "should not", "without"]:
            return "prohibition"
        elif text in ["only", "just", "merely"]:
            return "limitation"
        elif text in ["limit", "limited to", "max", "minimum"]:
            return "boundary"
        else:
            return "requirement"

    def _classify_goal(self, text: str) -> str:
        """分类目标类型"""
        if text in ["achieve", "accomplish", "reach", "attain"]:
            return "achievement"
        elif text in ["improve", "optimize", "enhance", "maximize"]:
            return "improvement"
        elif text in ["reduce", "decrease", "minimize"]:
            return "reduction"
        elif text in ["create", "build", "develop", "implement"]:
            return "creation"
        elif text in ["solve", "resolve", "fix", "address"]:
            return "resolution"
        else:
            return "general"

    def _extract_entities(self, text: str) -> dict:
        """提取实体"""
        return {
            "numbers": re.findall(r"\d+(?:\.\d+)?", text),
            "keywords": text.split()[:5],
        }

    def _llm_analyze(self, text: str, context: dict = None) -> dict:
        """LLM深度分析"""
        if self.llm:
            prompt = self._build_analysis_prompt(text, context)
            response = self.llm.chat(prompt)
            try:
                return json.loads(response)
            except:
                return {"confidence": 0.7, "reasoning": "规则基础分析"}

        return {"confidence": 0.7, "reasoning": "规则基础分析"}

    def _build_analysis_prompt(self, text: str, context: dict = None) -> str:
        """构建分析提示"""
        return f"""分析以下用户意图，提取关键信息：

输入: {text}

请JSON格式输出：
{{
    "intent_summary": "一句话总结意图",
    "confidence": 0.0-1.0,
    "reasoning": "分析理由",
    "implicit_requirements": ["隐含需求1", "隐含需求2"]
}}"""

    def _normalize(self, text: str, llm_analysis: dict) -> str:
        """意图归一化"""
        normalized = text.strip().lower()

        replacements = {
            r"\s+": " ",
            r"i want to": "",
            r"i need to": "",
            r"please": "",
            r"could you": "",
        }

        for pattern, replacement in replacements.items():
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

        return normalized.strip()

    def _vectorize(self, text: str) -> List[float]:
        """向量化"""
        return self.llm.embed(text) if self.llm else [0.0] * 16

    def _calculate_priority(self, text: str) -> float:
        """计算优先级"""
        text_lower = text.lower()

        priority_indicators = {
            "critical": 0.9,
            "urgent": 0.8,
            "important": 0.7,
            "asap": 0.8,
            "soon": 0.6,
            "when possible": 0.4,
        }

        for indicator, priority in priority_indicators.items():
            if indicator in text_lower:
                return priority

        return 0.5

    def batch_understand(
        self, inputs: List[str], context: dict = None
    ) -> List[IntentAnalysis]:
        """批量理解"""
        return [self.understand(inp, context) for inp in inputs]


class IntentUnderstandingWithRAG(IntentUnderstanding):
    """带RAG增强的意图理解"""

    def __init__(self, llm: LLMInterface = None, knowledge_base: dict = None):
        super().__init__(llm)
        self.knowledge_base = knowledge_base or {}

    def _retrieve_relevant_knowledge(self, intent: Intent) -> List[dict]:
        """检索相关知识"""
        if not self.knowledge_base:
            return []

        relevant = []
        intent_keywords = set(intent.normalized.split())

        for kb_item in self.knowledge_base.get("items", []):
            kb_keywords = set(kb_item.get("keywords", []))
            overlap = intent_keywords & kb_keywords
            if overlap:
                relevant.append(
                    {
                        "item": kb_item,
                        "relevance": len(overlap) / len(kb_keywords)
                        if kb_keywords
                        else 0,
                    }
                )

        return sorted(relevant, key=lambda x: x["relevance"], reverse=True)[:5]

    def understand(self, raw_input: str, context: dict = None) -> IntentAnalysis:
        """理解意图（带RAG增强）"""
        analysis = super().understand(raw_input, context)

        relevant_knowledge = self._retrieve_relevant_knowledge(analysis.intent)

        if relevant_knowledge:
            analysis.intent.metadata["relevant_knowledge"] = relevant_knowledge
            analysis.intent.metadata["rag_enhanced"] = True

        return analysis


__all__ = [
    "Intent",
    "IntentAnalysis",
    "IntentUnderstanding",
    "IntentUnderstandingWithRAG",
    "LLMInterface",
    "OpenAILLM",
]
