"""
UAS世界模型 - P0: 混合知识表示模块

功能：
- 知识图谱表示
- 向量嵌入表示
- 符号规则表示
- 混合检索与推理
"""

import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class KnowledgeType(Enum):
    KNOWLEDGE_GRAPH = "knowledge_graph"
    VECTOR = "vector"
    RULE = "rule"
    HYBRID = "hybrid"


@dataclass
class Entity:
    """知识图谱实体"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: str = ""
    properties: dict = field(default_factory=dict)
    embeddings: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class Relation:
    """知识图谱关系"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = ""
    target_id: str = ""
    type: str = ""
    properties: dict = field(default_factory=dict)


@dataclass
class Rule:
    """符号规则"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    condition: str = ""
    action: str = ""
    priority: int = 0
    enabled: bool = True
    metadata: dict = field(default_factory=dict)


@dataclass
class KnowledgeItem:
    """混合知识项"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    knowledge_type: KnowledgeType = KnowledgeType.HYBRID
    
    entity: Optional[Entity] = None
    relation: Optional[Relation] = None
    rule: Optional[Rule] = None
    
    vector_embedding: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class KnowledgeGraph:
    """
    知识图谱组件
    
    功能：
    - 实体管理
    - 关系管理
    - 图查询
    - 路径推理
    """
    
    def __init__(self):
        self.entities: dict[str, Entity] = {}
        self.relations: dict[str, Relation] = {}
        self.entity_index: dict[str, list[str]] = {}  # type -> entity_ids
    
    def add_entity(self, entity: Entity) -> str:
        """添加实体"""
        self.entities[entity.id] = entity
        
        # 索引
        if entity.type not in self.entity_index:
            self.entity_index[entity.type] = []
        self.entity_index[entity.type].append(entity.id)
        
        return entity.id
    
    def add_relation(self, relation: Relation) -> str:
        """添加关系"""
        self.relations[relation.id] = relation
        return relation.id
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """获取实体"""
        return self.entities.get(entity_id)
    
    def get_entities_by_type(self, entity_type: str) -> list[Entity]:
        """按类型获取实体"""
        entity_ids = self.entity_index.get(entity_type, [])
        return [self.entities[eid] for eid in entity_ids]
    
    def query(self, start_entity_id: str, relation_type: str = None, depth: int = 1) -> list[dict]:
        """图查询"""
        results = []
        visited = set()
        
        def dfs(current_id: str, current_depth: int):
            if current_depth > depth or current_id in visited:
                return
            
            visited.add(current_id)
            entity = self.entities.get(current_id)
            if not entity:
                return
            
            # 查找出边
            for rel in self.relations.values():
                if rel.source_id == current_id:
                    if relation_type is None or rel.type == relation_type:
                        target = self.entities.get(rel.target_id)
                        if target:
                            results.append({
                                'source': entity,
                                'relation': rel,
                                'target': target,
                                'depth': current_depth
                            })
                            dfs(rel.target_id, current_depth + 1)
        
        dfs(start_entity_id, 1)
        return results
    
    def find_path(self, start_id: str, end_id: str, max_depth: int = 3) -> list[list[str]]:
        """路径查找"""
        paths = []
        
        def dfs(current: str, path: list[str], visited: set):
            if len(path) > max_depth:
                return
            if current == end_id:
                paths.append(path.copy())
                return
            
            for rel in self.relations.values():
                if rel.source_id == current and rel.target_id not in visited:
                    visited.add(rel.target_id)
                    path.append(rel.target_id)
                    dfs(rel.target_id, path, visited)
                    path.pop()
                    visited.remove(rel.target_id)
        
        dfs(start_id, [start_id], {start_id})
        return paths
    
    def to_dict(self) -> dict:
        """导出为字典"""
        return {
            'entities': [e.__dict__ for e in self.entities.values()],
            'relations': [r.__dict__ for r in self.relations.values()]
        }


class VectorStore:
    """
    向量存储组件
    
    功能：
    - 向量索引
    - 相似度检索
    - 混合搜索
    """
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.items: dict[str, KnowledgeItem] = {}
        self.vectors: dict[str, list[float]] = {}
    
    def add(self, item: KnowledgeItem) -> str:
        """添加知识项"""
        self.items[item.id] = item
        if item.vector_embedding:
            self.vectors[item.id] = item.vector_embedding
        return item.id
    
    def search(self, query_vector: list[float], top_k: int = 5) -> list[tuple[KnowledgeItem, float]]:
        """向量检索"""
        if not query_vector or not self.vectors:
            return []
        
        # 简化的余弦相似度
        results = []
        for item_id, vec in self.vectors.items():
            similarity = self._cosine_similarity(query_vector, vec)
            results.append((self.items[item_id], similarity))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """余弦相似度"""
        if len(a) != len(b):
            return 0.0
        
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)
    
    def hybrid_search(self, query_vector: list[float], query_text: str, top_k: int = 5) -> list[tuple[KnowledgeItem, float]]:
        """混合搜索（向量 + 关键词）"""
        # 向量搜索
        vector_results = self.search(query_vector, top_k * 2)
        
        # 关键词搜索
        keyword_results = []
        query_words = set(query_text.lower().split())
        for item in self.items.values():
            item_words = set(item.content.lower().split())
            overlap = query_words & item_words
            if overlap:
                keyword_results.append((item, len(overlap) / len(query_words)))
        
        # 合并排序
        combined = {}
        for item, score in vector_results:
            combined[item.id] = combined.get(item.id, 0) + score * 0.7
        
        for item, score in keyword_results:
            combined[item.id] = combined.get(item.id, 0) + score * 0.3
        
        sorted_results = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return [(self.items[item_id], score) for item_id, score in sorted_results[:top_k]]


class RuleEngine:
    """
    符号规则引擎
    
    功能：
    - 规则存储
    - 条件匹配
    - 规则执行
    """
    
    def __init__(self):
        self.rules: dict[str, Rule] = {}
        self.rule_index: dict[str, list[str]] = {}  # trigger -> rule_ids
    
    def add_rule(self, rule: Rule) -> str:
        """添加规则"""
        self.rules[rule.id] = rule
        return rule.id
    
    def evaluate(self, context: dict) -> list[tuple[Rule, Any]]:
        """评估规则"""
        matched = []
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            # 简单条件评估
            if self._match_condition(rule.condition, context):
                action_result = self._execute_action(rule.action, context)
                matched.append((rule, action_result))
        
        # 按优先级排序
        matched.sort(key=lambda x: x[0].priority, reverse=True)
        return matched
    
    def _match_condition(self, condition: str, context: dict) -> bool:
        """条件匹配"""
        try:
            # 简单的表达式评估
            # 实际实现应该使用安全的表达式解析器
            for key, value in context.items():
                condition = condition.replace(f'{{{key}}}', f'"{value}"')
            return eval(condition)
        except:
            return False
    
    def _execute_action(self, action: str, context: dict) -> Any:
        """执行动作"""
        # 简化实现
        return {"executed": True, "action": action, "context": context}


class HybridKnowledgeBase:
    """
    混合知识基座
    
    整合：
    - 知识图谱（推理）
    - 向量存储（检索）
    - 规则引擎（执行）
    """
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.kg = KnowledgeGraph()
        self.vector_store = VectorStore()
        self.rule_engine = RuleEngine()
        self.kg_config = self.config.get('knowledge_graph', {})
        self.vector_config = self.config.get('vector_store', {})
        self.rule_config = self.config.get('rule_engine', {})
    
    def add_knowledge(self, item: KnowledgeItem) -> str:
        """添加知识"""
        if item.entity:
            self.kg.add_entity(item.entity)
        
        if item.relation:
            self.kg.add_relation(item.relation)
        
        if item.rule:
            self.rule_engine.add_rule(item.rule)
        
        if item.vector_embedding or item.content:
            self.vector_store.add(item)
        
        return item.id
    
    def retrieve(self, query: str, query_vector: list[float] = None, top_k: int = 5) -> dict:
        """混合检索"""
        results = {
            'vector': [],
            'graph': [],
            'rules': [],
            'hybrid': []
        }
        
        # 向量检索
        if query_vector:
            vector_results = self.vector_store.search(query_vector, top_k)
            results['vector'] = [
                {'item': item, 'score': score} 
                for item, score in vector_results
            ]
        
        # 关键词检索
        if query:
            # 简单实现：遍历实体名称匹配
            for entity in self.kg.entities.values():
                if query.lower() in entity.name.lower():
                    results['graph'].append({'entity': entity, 'score': 1.0})
        
        # 规则检索
        context = {'query': query, 'input': query_vector}
        rule_results = self.rule_engine.evaluate(context)
        results['rules'] = [{'rule': rule, 'result': result} for rule, result in rule_results]
        
        # 混合结果
        all_items = []
        for r in results['vector']:
            all_items.append((r['item'], r['score'] * 0.5))
        for r in results['graph']:
            all_items.append((r['entity'], r['score'] * 0.3))
        
        all_items.sort(key=lambda x: x[1], reverse=True)
        results['hybrid'] = [{'item': item, 'score': score} for item, score in all_items[:top_k]]
        
        return results
    
    def query_graph(self, entity_id: str, relation_type: str = None, depth: int = 1) -> list[dict]:
        """图查询"""
        return self.kg.query(entity_id, relation_type, depth)
    
    def apply_rules(self, context: dict) -> list[dict]:
        """应用规则"""
        return self.rule_engine.evaluate(context)
    
    def to_dict(self) -> dict:
        """导出"""
        return {
            'knowledge_graph': self.kg.to_dict(),
            'vector_store_count': len(self.vector_store.items),
            'rules_count': len(self.rule_engine.rules)
        }


# 导出
__all__ = [
    'Entity',
    'Relation',
    'Rule',
    'KnowledgeItem',
    'KnowledgeType',
    'KnowledgeGraph',
    'VectorStore',
    'RuleEngine',
    'HybridKnowledgeBase',
]
