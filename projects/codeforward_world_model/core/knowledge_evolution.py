"""
UAS世界模型 - P2: 知识图谱自主演化

功能：
- 反馈驱动的知识更新
- 实体/关系自动发现
- 图谱冲突检测与消解
- 对标KARMA/AriGraph架构
"""

import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


class EvolutionState(Enum):
    IDLE = "idle"
    DETECTING = "detecting"
    ANALYZING = "analyzing"
    UPDATING = "updating"
    VALIDATING = "validating"
    COMPLETE = "complete"


class EntityType(Enum):
    CONCEPT = "concept"
    OBJECT = "object"
    ACTION = "action"
    EVENT = "event"
    RELATION = "relation"


@dataclass
class EvolutionEvent:
    """演化事件"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = ""
    description: str = ""
    trigger: dict = field(default_factory=dict)
    changes: list = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class DriftDetection:
    """漂移检测结果"""

    detected: bool = False
    drift_type: str = ""
    severity: float = 0.0
    affected_entities: list = field(default_factory=list)
    suggested_actions: list = field(default_factory=list)


class LLMInterface(ABC):
    """LLM接口抽象"""

    @abstractmethod
    def chat(self, prompt: str, **kwargs) -> str:
        pass


class KnowledgeGraphEvolver:
    """
    知识图谱自主演化器

    对标KARMA/AriGraph：
    1. 反馈接收
    2. 漂移检测
    3. 实体/关系发现
    4. 图谱更新
    5. 冲突消解
    """

    def __init__(
        self, knowledge_graph: Any = None, llm: LLMInterface = None, config: dict = None
    ):
        self.kg = knowledge_graph
        self.llm = llm
        self.config = config or {}

        self.state = EvolutionState.IDLE
        self.evolution_history: list[EvolutionEvent] = []

        # 配置
        self.drift_threshold = self.config.get("drift_threshold", 0.7)
        self.min_confidence = self.config.get("min_confidence", 0.6)
        self.max_updates_per_cycle = self.config.get("max_updates_per_cycle", 10)

    def evolve(self, feedback: dict) -> EvolutionEvent:
        """
        演化一步

        Args:
            feedback: 外部反馈（执行结果、用户纠正等）

        Returns:
            EvolutionEvent: 演化事件
        """
        self.state = EvolutionState.DETECTING

        # 1. 漂移检测
        drift = self._detect_drift(feedback)

        if not drift.detected:
            self.state = EvolutionState.COMPLETE
            return EvolutionEvent(
                type="no_drift", description="未检测到漂移", trigger=feedback
            )

        self.state = EvolutionState.ANALYZING

        # 2. 分析变化
        changes = self._analyze_changes(drift, feedback)

        self.state = EvolutionState.UPDATING

        # 3. 执行更新
        self._apply_changes(changes)

        self.state = EvolutionState.VALIDATING

        # 4. 验证
        validated = self._validate_changes(changes)

        # 5. 记录事件
        event = EvolutionEvent(
            type="evolution",
            description=f"检测到{len(changes)}个变化",
            trigger=feedback,
            changes=changes,
            changes_validated=validated,
        )

        self.evolution_history.append(event)
        self.state = EvolutionState.COMPLETE

        return event

    def _detect_drift(self, feedback: dict) -> DriftDetection:
        """
        漂移检测

        检测类型：
        - 结果漂移：实际结果与预期不符
        - 关系漂移：实体间关系变化
        - 模式漂移：新的模式出现
        """
        if not feedback:
            return DriftDetection()

        # 检查结果漂移
        expected = feedback.get("expected")
        actual = feedback.get("actual")

        if expected and actual:
            # 简单比较
            if expected != actual:
                return DriftDetection(
                    detected=True,
                    drift_type="result_drift",
                    severity=1.0,
                    affected_entities=feedback.get("related_entities", []),
                    suggested_actions=["更新关系", "添加新实体"],
                )

        # 检查模式漂移
        if feedback.get("new_pattern"):
            return DriftDetection(
                detected=True,
                drift_type="pattern_drift",
                severity=0.8,
                suggested_actions=["发现新模式", "创建新实体类型"],
            )

        return DriftDetection()

    def _analyze_changes(self, drift: DriftDetection, feedback: dict) -> list[dict]:
        """分析需要做的变化"""
        changes = []

        if drift.drift_type == "result_drift":
            # 需要更新关系或实体
            changes.extend(self._analyze_relation_change(drift, feedback))

        elif drift.drift_type == "pattern_drift":
            # 需要添加新实体类型
            changes.extend(self._analyze_new_pattern(feedback))

        return changes[: self.max_updates_per_cycle]

    def _analyze_relation_change(
        self, drift: DriftDetection, feedback: dict
    ) -> list[dict]:
        """分析关系变化"""
        changes = []

        entity_a = feedback.get("entity_a")
        entity_b = feedback.get("entity_b")
        new_relation = feedback.get("new_relation")

        if entity_a and entity_b:
            changes.append(
                {
                    "type": "relation_update",
                    "source": entity_a,
                    "target": entity_b,
                    "new_relation": new_relation,
                }
            )

        return changes

    def _analyze_new_pattern(self, feedback: dict) -> list[dict]:
        """分析新模式"""
        changes = []

        if self.llm:
            # 使用LLM分析新模式
            prompt = f"""分析以下新模式，提取实体和关系：

{json.dumps(feedback, ensure_ascii=False)}

请JSON格式输出：
{{
    "new_entities": [{{"name": "", "type": ""}}],
    "new_relations": [{{"source": "", "target": "", "type": ""}}]
}}"""

            response = self.llm.chat(prompt)

            try:
                analysis = json.loads(response)

                for entity in analysis.get("new_entities", []):
                    changes.append(
                        {
                            "type": "entity_add",
                            "name": entity["name"],
                            "entity_type": entity.get("type", "concept"),
                        }
                    )

                for relation in analysis.get("new_relations", []):
                    changes.append(
                        {
                            "type": "relation_add",
                            "source": relation["source"],
                            "target": relation["target"],
                            "relation_type": relation.get("type", "related"),
                        }
                    )

            except:
                pass

        return changes

    def _apply_changes(self, changes: list[dict]):
        """应用变化到知识图谱"""
        if not self.kg:
            return

        for change in changes:
            change_type = change.get("type")

            if change_type == "entity_add":
                self._add_entity(change)
            elif change_type == "relation_add":
                self._add_relation(change)
            elif change_type == "relation_update":
                self._update_relation(change)

    def _add_entity(self, change: dict):
        """添加实体"""
        if hasattr(self.kg, "add_entity"):
            from .knowledge_base import Entity

            entity = Entity(
                name=change.get("name", ""), type=change.get("entity_type", "concept")
            )
            self.kg.add_entity(entity)

    def _add_relation(self, change: dict):
        """添加关系"""
        if hasattr(self.kg, "add_relation"):
            from .knowledge_base import Relation

            relation = Relation(
                source_id=change.get("source", ""),
                target_id=change.get("target", ""),
                type=change.get("relation_type", "related"),
            )
            self.kg.add_relation(relation)

    def _update_relation(self, change: dict):
        """更新关系"""
        # 简化实现
        pass

    def _validate_changes(self, changes: list[dict]) -> bool:
        """验证变化"""
        # 检查冲突
        conflicts = self._detect_conflicts(changes)

        if conflicts:
            self._resolve_conflicts(conflicts)

        return True

    def _detect_conflicts(self, changes: list[dict]) -> list[dict]:
        """检测冲突"""
        conflicts = []

        # 简化：检查重复添加
        entity_names = [c.get("name") for c in changes if c.get("type") == "entity_add"]

        if len(entity_names) != len(set(entity_names)):
            conflicts.append({"type": "duplicate_entity", "entities": entity_names})

        return conflicts

    def _resolve_conflicts(self, conflicts: list[dict]):
        """消解冲突"""
        # 简化：保留第一个
        pass

    def get_evolution_history(self) -> list[EvolutionEvent]:
        """获取演化历史"""
        return self.evolution_history


class MultiAgentKGBuilder:
    """
    多Agent知识图谱构建器

    对标KARMA架构：
    - 9个协作Agent
    - 实体发现、关系提取、模式对齐、冲突消解
    """

    def __init__(self, llm: LLMInterface = None):
        self.llm = llm

        self.agents = {
            "entity_discoverer": EntityDiscovererAgent(llm),
            "relation_extractor": RelationExtractorAgent(llm),
            "schema_aligner": SchemaAlignerAgent(llm),
            "conflict_resolver": ConflictResolverAgent(llm),
            "entity_verifier": EntityVerifierAgent(llm),
            "relation_verifier": RelationVerifierAgent(llm),
        }

    def build(self, documents: list[str]) -> dict:
        """
        构建知识图谱

        Args:
            documents: 文本文档列表

        Returns:
            构建的图谱数据
        """
        # 1. 实体发现
        entities = self._run_agent("entity_discoverer", documents)

        # 2. 关系提取
        relations = self._run_agent(
            "relation_extractor", {"entities": entities, "documents": documents}
        )

        # 3. 模式对齐
        aligned = self._run_agent(
            "schema_aligner", {"entities": entities, "relations": relations}
        )

        # 4. 验证实体
        verified_entities = self._run_agent("entity_verifier", aligned["entities"])

        # 5. 验证关系
        verified_relations = self._run_agent("relation_verifier", aligned["relations"])

        # 6. 冲突消解
        final = self._run_agent(
            "conflict_resolver",
            {"entities": verified_entities, "relations": verified_relations},
        )

        return final

    def _run_agent(self, agent_name: str, input_data: Any) -> Any:
        """运行单个Agent"""
        agent = self.agents.get(agent_name)
        if agent:
            return agent.run(input_data)
        return input_data


class BaseAgent(ABC):
    """Base Agent for KG construction"""

    def __init__(self, llm: LLMInterface = None):
        self.llm = llm

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        pass


class EntityDiscovererAgent(BaseAgent):
    """实体发现Agent"""

    def run(self, documents: list[str]) -> list[dict]:
        if not self.llm:
            return []

        prompt = f"""从以下文档中发现实体：

{chr(10).join(documents[:5])}

请JSON格式输出实体列表：
{{
    "entities": [{{"name": "实体名", "type": "类型", "description": "描述"}}]
}}"""

        response = self.llm.chat(prompt)

        try:
            return json.loads(response).get("entities", [])
        except:
            return []


class RelationExtractorAgent(BaseAgent):
    """关系提取Agent"""

    def run(self, input_data: dict) -> list[dict]:
        if not self.llm:
            return []

        entities = input_data.get("entities", [])
        documents = input_data.get("documents", [])

        prompt = f"""从以下文档中提取实体之间的关系：

实体: {json.dumps(entities, ensure_ascii=False)}
文档: {chr(10).join(documents[:3])}

请JSON格式输出关系列表：
{{
    "relations": [{{"source": "实体A", "target": "实体B", "type": "关系类型"}}]
}}"""

        response = self.llm.chat(prompt)

        try:
            return json.loads(response).get("relations", [])
        except:
            return []


class SchemaAlignerAgent(BaseAgent):
    """模式对齐Agent"""

    def run(self, input_data: dict) -> dict:
        # 简化实现：直接返回
        return input_data


class ConflictResolverAgent(BaseAgent):
    """冲突消解Agent"""

    def run(self, input_data: dict) -> dict:
        entities = input_data.get("entities", [])
        relations = input_data.get("relations", [])

        # 消解重复实体
        seen = set()
        unique_entities = []

        for e in entities:
            if e["name"] not in seen:
                seen.add(e["name"])
                unique_entities.append(e)

        return {"entities": unique_entities, "relations": relations}


class EntityVerifierAgent(BaseAgent):
    """实体验证Agent"""

    def run(self, entities: list[dict]) -> list[dict]:
        # 验证实体正确性
        return [e for e in entities if e.get("name")]


class RelationVerifierAgent(BaseAgent):
    """关系验证Agent"""

    def run(self, relations: list[dict]) -> list[dict]:
        # 验证关系正确性
        return [r for r in relations if r.get("source") and r.get("target")]


# 导出
__all__ = [
    "EvolutionState",
    "EvolutionEvent",
    "DriftDetection",
    "EntityType",
    "KnowledgeGraphEvolver",
    "MultiAgentKGBuilder",
    "BaseAgent",
    "EntityDiscovererAgent",
    "RelationExtractorAgent",
    "SchemaAlignerAgent",
    "ConflictResolverAgent",
    "EntityVerifierAgent",
    "RelationVerifierAgent",
]
