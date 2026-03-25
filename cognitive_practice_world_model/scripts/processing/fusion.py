"""
世界模型综合数据融合模块
将五维度数据融合为 ComprehensiveWorldModelIR
"""
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime
import json


@dataclass
class SpatialData:
    """空间维度数据"""
    entities: List[Dict] = field(default_factory=list)
    relations: List[Dict] = field(default_factory=list)
    topology: str = "unknown"


@dataclass
class TemporalData:
    """时间维度数据"""
    events: List[Dict] = field(default_factory=list)
    causal_links: List[Dict] = field(default_factory=list)
    timeline: List[str] = field(default_factory=list)


@dataclass
class SemanticData:
    """语义维度数据"""
    concepts: List[Dict] = field(default_factory=list)
    relations: List[Dict] = field(default_factory=list)
    hierarchy_depth: int = 0


@dataclass
class CausalData:
    """因果维度数据"""
    mechanisms: List[Dict] = field(default_factory=list)
    interventions: List[Dict] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class SocialData:
    """社会维度数据"""
    agents: List[Dict] = field(default_factory=list)
    relations: List[Dict] = field(default_factory=list)


@dataclass
class ComprehensiveWorldModelIR:
    """
    综合世界模型中间表示
    整合五维度数据，形成统一的可解释输出
    """
    schema_version: str = "1.0.0"
    model_id: str = ""
    extraction_timestamp: str = ""

    # 五维度数据
    spatial: Optional[SpatialData] = None
    temporal: Optional[TemporalData] = None
    semantic: Optional[SemanticData] = None
    causal: Optional[CausalData] = None
    social: Optional[SocialData] = None

    # 综合指标
    coherence_score: float = 0.0
    completeness_score: float = 0.0
    confidence: float = 0.0

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.extraction_timestamp:
            self.extraction_timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "schema_version": self.schema_version,
            "model_id": self.model_id,
            "extraction_timestamp": self.extraction_timestamp,
            "completeness_score": self.completeness_score,
            "coherence_score": self.coherence_score,
            "confidence": self.confidence,
            "metadata": self.metadata
        }

        # 添加五维度数据
        if self.spatial:
            result["spatial"] = asdict(self.spatial)
        if self.temporal:
            result["temporal"] = asdict(self.temporal)
        if self.semantic:
            result["semantic"] = asdict(self.semantic)
        if self.causal:
            result["causal"] = asdict(self.causal)
        if self.social:
            result["social"] = asdict(self.social)

        return result

    def to_json(self) -> str:
        """序列化为JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComprehensiveWorldModelIR":
        """从字典创建"""
        # 提取维度数据
        spatial = SpatialData(**data.get("spatial", {})) if "spatial" in data else None
        temporal = TemporalData(**data.get("temporal", {})) if "temporal" in data else None
        semantic = SemanticData(**data.get("semantic", {})) if "semantic" in data else None
        causal = CausalData(**data.get("causal", {})) if "causal" in data else None
        social = SocialData(**data.get("social", {})) if "social" in data else None

        return cls(
            schema_version=data.get("schema_version", "1.0.0"),
            model_id=data.get("model_id", ""),
            extraction_timestamp=data.get("extraction_timestamp", ""),
            spatial=spatial,
            temporal=temporal,
            semantic=semantic,
            causal=causal,
            social=social,
            coherence_score=data.get("coherence_score", 0.0),
            completeness_score=data.get("completeness_score", 0.0),
            confidence=data.get("confidence", 0.0),
            metadata=data.get("metadata", {})
        )


class WorldModelFusion:
    """世界模型融合器"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def fuse(
        self,
        spatial_data: Dict[str, Any],
        temporal_data: Dict[str, Any],
        semantic_data: Dict[str, Any],
        causal_data: Dict[str, Any],
        social_data: Dict[str, Any]
    ) -> ComprehensiveWorldModelIR:
        """
        融合五维度数据
        """
        # 创建各维度数据对象
        spatial = SpatialData(
            entities=spatial_data.get("entities", []),
            relations=spatial_data.get("relations", []),
            topology=spatial_data.get("topology", "unknown")
        )

        temporal = TemporalData(
            events=temporal_data.get("events", []),
            causal_links=temporal_data.get("causal_links", []),
            timeline=temporal_data.get("timeline", [])
        )

        semantic = SemanticData(
            concepts=semantic_data.get("concepts", []),
            relations=semantic_data.get("relations", []),
            hierarchy_depth=semantic_data.get("hierarchy_depth", 0)
        )

        causal = CausalData(
            mechanisms=causal_data.get("mechanisms", []),
            interventions=causal_data.get("interventions", []),
            confidence=causal_data.get("confidence", 0.0)
        )

        social = SocialData(
            agents=social_data.get("agents", []),
            relations=social_data.get("relations", [])
        )

        # 创建综合IR
        ir = ComprehensiveWorldModelIR(
            spatial=spatial,
            temporal=temporal,
            semantic=semantic,
            causal=causal,
            social=social
        )

        # 计算综合指标
        ir.completeness_score = self._calc_completeness(ir)
        ir.coherence_score = self._calc_coherence(ir)
        ir.confidence = self._calc_confidence(ir)

        return ir

    def _calc_completeness(self, ir: ComprehensiveWorldModelIR) -> float:
        """计算完整度"""
        score = 0.0
        total = 5

        if ir.spatial and (ir.spatial.entities or ir.spatial.relations):
            score += 1
        if ir.temporal and (ir.temporal.events or ir.temporal.causal_links):
            score += 1
        if ir.semantic and (ir.semantic.concepts or ir.semantic.relations):
            score += 1
        if ir.causal and (ir.causal.mechanisms or ir.causal.interventions):
            score += 1
        if ir.social and (ir.social.agents or ir.social.relations):
            score += 1

        return score / total

    def _calc_coherence(self, ir: ComprehensiveWorldModelIR) -> float:
        """计算一致性"""
        # 简化的 coherence 计算
        # 实际应检查跨维度关系一致性
        scores = []

        # 检查实体一致性（同一实体在不同维度出现）
        entity_sets = []
        if ir.spatial:
            entity_sets.append(set(e["id"] for e in ir.spatial.entities))
        if ir.temporal:
            entity_sets.append(set(e["id"] for e in ir.temporal.events))
        if ir.semantic:
            entity_sets.append(set(c["id"] for c in ir.semantic.concepts))
        if ir.causal:
            entity_sets.append(set(m["source"] for m in ir.causal.mechanisms))
        if ir.social:
            entity_sets.append(set(a["id"] for a in ir.social.agents))

        if len(entity_sets) > 1:
            # 计算Jaccard相似度的平均值
            import numpy as np
            similarities = []
            for i in range(len(entity_sets)):
                for j in range(i + 1, len(entity_sets)):
                    intersection = len(entity_sets[i] & entity_sets[j])
                    union = len(entity_sets[i] | entity_sets[j])
                    if union > 0:
                        similarities.append(intersection / union)

            if similarities:
                scores.append(np.mean(similarities))

        # 返回一致性分数，默认为0.5
        return sum(scores) / len(scores) if scores else 0.5

    def _calc_confidence(self, ir: ComprehensiveWorldModelIR) -> float:
        """计算置信度"""
        scores = []

        # 基于数据量
        total_entities = 0
        if ir.spatial:
            total_entities += len(ir.spatial.entities) + len(ir.spatial.relations)
        if ir.temporal:
            total_entities += len(ir.temporal.events) + len(ir.temporal.causal_links)
        if ir.semantic:
            total_entities += len(ir.semantic.concepts) + len(ir.semantic.relations)
        if ir.causal:
            total_entities += len(ir.causal.mechanisms) + len(ir.causal.interventions)
        if ir.social:
            total_entities += len(ir.social.agents) + len(ir.social.relations)

        if total_entities > 0:
            scores.append(min(1.0, total_entities / 100))

        # 基于因果置信度
        if ir.causal and ir.causal.confidence > 0:
            scores.append(ir.causal.confidence)

        return sum(scores) / len(scores) if scores else 0.0


# 产品化视图生成
class ProductViewGenerator:
    """产品视图生成器"""

    @staticmethod
    def to_ontology_graph(ir: ComprehensiveWorldModelIR) -> Dict[str, Any]:
        """转换为本体图谱视图"""
        nodes = []
        edges = []

        # 从语义维度提取概念作为节点
        if ir.semantic:
            for concept in ir.semantic.concepts:
                nodes.append({
                    "id": concept["id"],
                    "label": concept.get("name", concept["id"]),
                    "type": "concept"
                })

            for relation in ir.semantic.relations:
                edges.append({
                    "from": relation.get("child"),
                    "to": relation.get("parent"),
                    "type": relation.get("type", "is_a")
                })

        return {
            "type": "ontology_graph",
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "depth": ir.semantic.hierarchy_depth if ir.semantic else 0
            }
        }

    @staticmethod
    def to_event_chain(ir: ComprehensiveWorldModelIR) -> Dict[str, Any]:
        """转换为事件链视图"""
        events = []

        if ir.temporal:
            for event in ir.temporal.events:
                events.append({
                    "id": event["id"],
                    "timestamp": event.get("timestamp", 0),
                    "content": event.get("content", "")
                })

        causal_links = []
        if ir.temporal:
            for link in ir.temporal.causal_links:
                causal_links.append({
                    "from": link.get("cause"),
                    "to": link.get("effect"),
                    "confidence": link.get("confidence", 0)
                })

        return {
            "type": "event_chain",
            "events": events,
            "causal_links": causal_links,
            "timeline": ir.temporal.timeline if ir.temporal else []
        }

    @staticmethod
    def to_knowledge_graph(ir: ComprehensiveWorldModelIR) -> Dict[str, Any]:
        """转换为知识图谱视图"""
        nodes = []
        edges = []

        # 综合所有维度的实体作为节点
        if ir.spatial:
            for entity in ir.spatial.entities:
                nodes.append({
                    "id": entity["id"],
                    "label": entity.get("name", entity["id"]),
                    "type": "spatial"
                })

        if ir.semantic:
            for concept in ir.semantic.concepts:
                nodes.append({
                    "id": concept["id"],
                    "label": concept.get("name", concept["id"]),
                    "type": "concept"
                })

        if ir.social:
            for agent in ir.social.agents:
                nodes.append({
                    "id": agent["id"],
                    "label": agent.get("role", agent["id"]),
                    "type": "agent"
                })

        # 综合所有关系作为边
        if ir.spatial:
            for rel in ir.spatial.relations:
                edges.append({
                    "from": rel["from_entity"],
                    "to": rel["to_entity"],
                    "type": "spatial_adjacent",
                    "weight": rel.get("confidence", 0)
                })

        if ir.semantic:
            for rel in ir.semantic.relations:
                edges.append({
                    "from": rel.get("child"),
                    "to": rel.get("parent"),
                    "type": rel.get("type", "semantic"),
                    "weight": rel.get("similarity", 0)
                })

        if ir.social:
            for rel in ir.social.relations:
                edges.append({
                    "from": rel.get("from"),
                    "to": rel.get("to"),
                    "type": rel.get("type", "social"),
                    "content": rel.get("content", "")
                })

        return {
            "type": "knowledge_graph",
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "node_count": len(nodes),
                "edge_count": len(edges)
            }
        }

    @staticmethod
    def to_causal_graph(ir: ComprehensiveWorldModelIR) -> Dict[str, Any]:
        """转换为因果图谱视图"""
        nodes = []
        edges = []

        # 从因果维度提取
        if ir.causal:
            # 机制节点
            for mechanism in ir.causal.mechanisms:
                nodes.append({
                    "id": mechanism.get("source"),
                    "type": "cause"
                })
                nodes.append({
                    "id": mechanism.get("target"),
                    "type": "effect"
                })

                edges.append({
                    "from": mechanism.get("source"),
                    "to": mechanism.get("target"),
                    "mechanism": mechanism.get("mechanism"),
                    "strength": mechanism.get("strength", 0)
                })

        return {
            "type": "causal_graph",
            "nodes": nodes,
            "edges": edges,
            "confidence": ir.causal.confidence if ir.causal else 0
        }


# 便捷函数
def create_comprehensive_model(
    model_id: str,
    spatial: Dict,
    temporal: Dict,
    semantic: Dict,
    causal: Dict,
    social: Dict
) -> ComprehensiveWorldModelIR:
    """创建综合世界模型IR的便捷函数"""
    fusion = WorldModelFusion()
    return fusion.fuse(spatial, temporal, semantic, causal, social)