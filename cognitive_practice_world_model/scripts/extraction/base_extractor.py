"""
世界模型五维度数据提取器基类
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import json


@dataclass
class ExtractedRelation:
    """提取的关系"""
    from_entity: str
    to_entity: str
    relation_type: str
    confidence: float
    evidence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedEntity:
    """提取的实体"""
    id: str
    name: str
    entity_type: str
    embedding: Optional[List[float]] = None
    properties: Dict[str, Any] = field(default_factory=dict)


class BaseExtractor(ABC):
    """提取器基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get("name", self.__class__.__name__)

    @abstractmethod
    def extract(self, model_output: Any) -> Dict[str, Any]:
        """从模型输出中提取数据"""
        pass

    def validate(self, data: Dict[str, Any]) -> bool:
        """验证提取结果"""
        return "entities" in data and "relations" in data

    def to_json(self, data: Dict[str, Any]) -> str:
        """序列化为JSON"""
        return json.dumps(data, indent=2, ensure_ascii=False)


class SpatialExtractor(BaseExtractor):
    """空间关系提取器"""

    def extract(self, model_output: Any) -> Dict[str, Any]:
        """
        形式化: Adjacent(e₁, e₂, t)
        提取位置、距离、拓扑关系
        """
        entities = []
        relations = []

        # 从隐藏状态提取位置编码
        hidden_states = model_output.get("hidden_states", [])
        for i, hs in enumerate(hidden_states):
            entities.append(ExtractedEntity(
                id=f"spatial_e{i}",
                name=f"state_{i}",
                entity_type="spatial_state",
                embedding=hs.tolist() if hasattr(hs, 'tolist') else hs
            ))

        # 从注意力头提取拓扑结构
        attention = model_output.get("attention", None)
        if attention is not None:
            for i in range(len(attention)):
                for j in range(len(attention[i])):
                    if attention[i][j] > self.config.get("threshold", 0.1):
                        relations.append(ExtractedRelation(
                            from_entity=f"spatial_e{i}",
                            to_entity=f"spatial_e{j}",
                            relation_type="adjacent",
                            confidence=float(attention[i][j])
                        ))

        return {
            "dimension": "spatial",
            "entities": [e.__dict__ for e in entities],
            "relations": [r.__dict__ for r in relations],
            "topology": self._analyze_topology(relations),
            "timestamp": datetime.now().isoformat()
        }

    def _analyze_topology(self, relations: List[ExtractedRelation]) -> str:
        """分析拓扑类型"""
        if not relations:
            return "empty"
        # 简化判断：度数分布决定拓扑类型
        degrees = {}
        for r in relations:
            degrees[r.from_entity] = degrees.get(r.from_entity, 0) + 1
            degrees[r.to_entity] = degrees.get(r.to_entity, 0) + 1

        avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
        if avg_degree > 3:
            return "clustered"
        elif avg_degree > 1:
            return "distributed"
        return "hierarchical"


class TemporalExtractor(BaseExtractor):
    """时间关系提取器"""

    def extract(self, model_output: Any) -> Dict[str, Any]:
        """
        形式化: Cause(evt₁, evt₂)
        提取先后、因果、同时性关系
        """
        events = []
        causal_links = []

        # 从序列中提取事件
        sequence = model_output.get("sequence", [])
        for i, token in enumerate(sequence):
            events.append({
                "id": f"evt{i}",
                "timestamp": i,
                "content": token,
                "state": model_output.get("states", [{}])[i] if i < len(model_output.get("states", [])) else {}
            })

        # 从注意力模式推断因果关系
        attention = model_output.get("attention_patterns", None)
        if attention is not None:
            for i in range(len(attention)):
                for j in range(len(attention[i])):
                    if attention[i][j] > self.config.get("confidence_threshold", 0.7):
                        causal_links.append({
                            "cause": f"evt{i}",
                            "effect": f"evt{j}",
                            "confidence": float(attention[i][j]),
                            "type": "temporal_precedence" if i < j else "simultaneous"
                        })

        return {
            "dimension": "temporal",
            "events": events,
            "causal_links": causal_links,
            "timeline": [e["id"] for e in events],
            "timestamp": datetime.now().isoformat()
        }


class SemanticExtractor(BaseExtractor):
    """语义关系提取器"""

    def extract(self, model_output: Any) -> Dict[str, Any]:
        """
        形式化: IsPartOf(e₁, e₂)
        提取上下位、整体部分关系
        """
        concepts = []
        relations = []

        # 从嵌入中提取概念
        embeddings = model_output.get("embeddings", [])
        for i, emb in enumerate(embeddings):
            concepts.append({
                "id": f"c{i}",
                "name": model_output.get("labels", ["concept"])[i] if i < len(model_output.get("labels", [])) else f"concept_{i}",
                "embedding": emb.tolist() if hasattr(emb, 'tolist') else emb,
                "type": "concept"
            })

        # K近邻聚类
        k = self.config.get("k_neighbors", 10)
        if len(embeddings) > 1:
            for i in range(len(embeddings)):
                # 计算与其他概念的相似度
                similarities = []
                for j in range(len(embeddings)):
                    if i != j:
                        sim = self._cosine_similarity(embeddings[i], embeddings[j])
                        similarities.append((j, sim))

                # 取top-k
                similarities.sort(key=lambda x: x[1], reverse=True)
                for j, sim in similarities[:k]:
                    relations.append({
                        "child": f"c{i}",
                        "parent": f"c{j}",
                        "type": "similar_to",
                        "similarity": sim
                    })

        return {
            "dimension": "semantic",
            "concepts": concepts,
            "relations": relations,
            "hierarchy_depth": self._estimate_depth(relations),
            "timestamp": datetime.now().isoformat()
        }

    def _cosine_similarity(self, a, b) -> float:
        """计算余弦相似度"""
        import numpy as np
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _estimate_depth(self, relations: List[Dict]) -> int:
        """估计层次深度"""
        # 简化实现
        return min(5, max(1, len(relations) // 10 + 1))


class CausalExtractor(BaseExtractor):
    """因果关系提取器"""

    def extract(self, model_output: Any) -> Dict[str, Any]:
        """
        形式化: Affect(e₁, e₂, evt)
        提取作用、反作用因果关系
        """
        mechanisms = []
        interventions = []

        # 干预实验
        n_samples = self.config.get("n_samples", 100)
        hidden_states = model_output.get("hidden_states", [])

        for i in range(min(n_samples, len(hidden_states) - 1)):
            # 简化的因果推断
            intervention_effect = model_output.get("intervention_effects", [[]])[i]
            if intervention_effect:
                mechanisms.append({
                    "source": f"e{i}",
                    "target": f"e{i+1}",
                    "mechanism": "activation",
                    "strength": float(sum(intervention_effect) / len(intervention_effect)) if intervention_effect else 0.0
                })

        # 反事实推理
        counterfactuals = model_output.get("counterfactuals", [])
        for cf in counterfactuals:
            interventions.append({
                "do": cf.get("action", "unknown"),
                "effect": cf.get("outcome", "unknown"),
                "probability": cf.get("probability", 0.5)
            })

        return {
            "dimension": "causal",
            "mechanisms": mechanisms,
            "interventions": interventions,
            "confidence": sum(m["strength"] for m in mechanisms) / len(mechanisms) if mechanisms else 0.0,
            "timestamp": datetime.now().isoformat()
        }


class SocialExtractor(BaseExtractor):
    """社会关系提取器"""

    def extract(self, model_output: Any) -> Dict[str, Any]:
        """
        形式化: Role(e₁, role, e₂)
        提取角色、权力、义务关系
        """
        agents = []
        relations = []

        # 角色提取
        embeddings = model_output.get("embeddings", [])
        role_types = self.config.get("role_types", ["provider", "consumer", "mediator", "authority"])

        for i, emb in enumerate(embeddings):
            # 简化：根据嵌入向量聚类确定角色
            role = role_types[i % len(role_types)]
            agents.append({
                "id": f"a{i}",
                "role": role,
                "capabilities": [],
                "needs": []
            })

        # 义务挖掘
        dialogue_contexts = model_output.get("dialogue_contexts", [])
        for ctx in dialogue_contexts:
            # 简化：模式匹配
            content = ctx.get("content", "")
            if "should" in content or "must" in content or "need" in content:
                relations.append({
                    "from": ctx.get("speaker", "unknown"),
                    "to": ctx.get("listener", "unknown"),
                    "type": "obligation",
                    "content": content
                })

        return {
            "dimension": "social",
            "agents": agents,
            "relations": relations,
            "timestamp": datetime.now().isoformat()
        }


# 提取器工厂
class ExtractorFactory:
    """提取器工厂"""

    EXTRACTORS = {
        "spatial": SpatialExtractor,
        "temporal": TemporalExtractor,
        "semantic": SemanticExtractor,
        "causal": CausalExtractor,
        "social": SocialExtractor
    }

    @classmethod
    def create(cls, dimension: str, config: Dict[str, Any]) -> BaseExtractor:
        """创建提取器"""
        extractor_class = cls.EXTRACTORS.get(dimension)
        if not extractor_class:
            raise ValueError(f"Unknown dimension: {dimension}")
        return extractor_class(config)

    @classmethod
    def create_all(cls, configs: Dict[str, Any]) -> Dict[str, BaseExtractor]:
        """创建所有维度提取器"""
        return {
            dim: cls.create(dim, cfg)
            for dim, cfg in configs.items()
            if dim in cls.EXTRACTORS
        }