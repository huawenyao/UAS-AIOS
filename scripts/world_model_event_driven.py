#!/usr/bin/env python3
"""
UAS 世界模型认知主体 - 事件驱动与反馈回路

实现：
1. 事件驱动的状态机
2. 实时反馈回路
3. 意图守恒校验
4. 自主演化
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional
from dataclasses import dataclass, field


class CognitiveState(Enum):
    DORMANT = "dormant"
    PERCEIVING = "perceiving"
    UNDERSTANDING = "understanding"
    MAPPING = "mapping"
    REDUCING = "reducing"
    REASONING = "reasoning"
    VALIDATING = "validating"
    ACTING = "acting"
    MONITORING = "monitoring"
    REFLECTING = "reflecting"
    EVOLVING = "evolving"
    COMPLETE = "complete"
    ERROR = "error"
    BLOCKED = "blocked"


class EventType(Enum):
    """认知事件类型"""
    INTENT_RECEIVED = "intent_received"
    PERCEPTION_COMPLETE = "perception_complete"
    UNDERSTANDING_COMPLETE = "understanding_complete"
    MAPPING_COMPLETE = "mapping_complete"
    REDUCTION_COMPLETE = "reduction_complete"
    REASONING_COMPLETE = "reasoning_complete"
    VALIDATION_PASSED = "validation_passed"
    VALIDATION_FAILED = "validation_failed"
    ACTION_COMPLETE = "action_complete"
    FEEDBACK_RECEIVED = "feedback_received"
    DRIFT_DETECTED = "drift_detected"
    DRIFT_CONFIRMED = "drift_confirmed"
    EVOLUTION_COMPLETE = "evolution_complete"
    ERROR_OCCURRED = "error_occurred"


@dataclass
class Intent:
    """意图"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    raw_input: str = ""
    normalized: str = ""
    constraints: list = field(default_factory=list)
    success_criteria: list = field(default_factory=list)
    vector: list = field(default_factory=list)
    priority: float = 0.5
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class CognitiveEvent:
    """认知事件"""
    type: EventType
    source_state: CognitiveState
    target_state: CognitiveState
    payload: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class FeedbackChannel:
    """反馈通道"""
    name: str
    source: str
    delay_tolerance_ms: int = 1000
    callback: Callable = None


@dataclass
class IntentGuard:
    """意图守恒校验器"""
    enabled: bool = True
    threshold: float = 0.8
    checks: list = field(default_factory=lambda: [
        {'name': 'semantic_alignment', 'weight': 0.4},
        {'name': 'constraint_satisfaction', 'weight': 0.3},
        {'name': 'law_consistency', 'weight': 0.3}
    ])


class EventDrivenCognitiveAgent:
    """
    事件驱动的认知主体
    
    核心机制：
    1. 事件发射 → 状态转移
    2. 实时反馈监听
    3. 意图守恒闭环
    4. 漂移检测与演化
    """
    
    def __init__(self, config: dict = None):
        self.id = str(uuid.uuid4())
        self.state = CognitiveState.DORMANT
        self.config = config or {}
        
        self.intent: Optional[Intent] = None
        self.activated_laws = []
        self.reduced_representation = {}
        self.strategy = []
        self.events = []
        
        self.laws = {}
        self.mappers = {}
        
        self.intent_guard = IntentGuard(
            enabled=self.config.get('intent_guard', {}).get('enabled', True),
            threshold=self.config.get('intent_guard', {}).get('threshold', 0.8)
        )
        
        self.feedback_channels = []
        self.evolution_enabled = self.config.get('evolution', {}).get('enabled', True)
        
        self._load_knowledge()
        self._init_feedback_channels()
    
    def _load_knowledge(self):
        """加载知识"""
        if 'laws' in self.config:
            for category in self.config['laws'].get('categories', []):
                for law in category.get('laws', []):
                    self.laws[law['id']] = law
        
        if 'mappers' in self.config:
            for mapper in self.config['mappers'].get('mappers', []):
                self.mappers[mapper['id']] = mapper
    
    def _init_feedback_channels(self):
        """初始化反馈通道"""
        default_channels = [
            FeedbackChannel(name='execution', source='runtime', delay_tolerance_ms=5000),
            FeedbackChannel(name='user', source='human', delay_tolerance_ms=30000),
            FeedbackChannel(name='system', source='monitoring', delay_tolerance_ms=1000)
        ]
        self.feedback_channels = default_channels
    
    # ==================== 事件驱动核心 ====================
    
    def emit(self, event_type: EventType, target_state: CognitiveState, payload: dict = None):
        """发射事件并转移状态"""
        event = CognitiveEvent(
            type=event_type,
            source_state=self.state,
            target_state=target_state,
            payload=payload or {}
        )
        
        self.events.append({
            'type': event_type.value,
            'from': self.state.value,
            'to': target_state.value,
            'timestamp': event.timestamp,
            'payload': event.payload
        })
        
        self.state = target_state
        return event
    
    # ==================== 输入接口 ====================
    
    def receive_intent(self, raw_input: str, **kwargs) -> str:
        """接收意图"""
        self.intent = Intent(
            raw_input=raw_input,
            normalized=raw_input.strip().lower(),
            priority=kwargs.get('priority', 0.5)
        )
        self.intent.constraints = self._extract_constraints(raw_input)
        
        self.emit(EventType.INTENT_RECEIVED, CognitiveState.PERCEIVING)
        return self.intent.id
    
    def receive_feedback(self, feedback: dict, channel: str = 'execution'):
        """接收反馈"""
        self.emit(EventType.FEEDBACK_RECEIVED, CognitiveState.MONITORING, {'feedback': feedback, 'channel': channel})
        
        if self._detect_drift(feedback):
            self.emit(EventType.DRIFT_DETECTED, CognitiveState.REFLECTING, {'feedback': feedback})
    
    # ==================== 状态处理 ====================
    
    def step(self) -> dict:
        """单步执行"""
        handlers = {
            CognitiveState.PERCEIVING: self._on_perceiving,
            CognitiveState.UNDERSTANDING: self._on_understanding,
            CognitiveState.MAPPING: self._on_mapping,
            CognitiveState.REDUCING: self._on_reducing,
            CognitiveState.REASONING: self._on_reasoning,
            CognitiveState.VALIDATING: self._on_validating,
            CognitiveState.ACTING: self._on_acting,
            CognitiveState.MONITORING: self._on_monitoring,
            CognitiveState.REFLECTING: self._on_reflecting,
            CognitiveState.EVOLVING: self._on_evolving,
        }
        
        handler = handlers.get(self.state)
        return handler() if handler else {'state': self.state.value, 'waiting': True}
    
    def run_until_complete(self) -> dict:
        """运行至完成"""
        while self.state not in [CognitiveState.COMPLETE, CognitiveState.ERROR, CognitiveState.BLOCKED]:
            result = self.step()
        
        return self.get_result()
    
    # ==================== 状态处理器 ====================
    
    def _on_perceiving(self) -> dict:
        self.emit(EventType.PERCEPTION_COMPLETE, CognitiveState.UNDERSTANDING)
        return {'state': self.state.value}
    
    def _on_understanding(self) -> dict:
        self.intent.vector = self._encode(self.intent.normalized)
        self.emit(EventType.UNDERSTANDING_COMPLETE, CognitiveState.MAPPING)
        return {'state': self.state.value}
    
    def _on_mapping(self) -> dict:
        self.activated_laws = self._activate_laws()
        self.emit(EventType.MAPPING_COMPLETE, CognitiveState.REDUCING)
        return {'state': self.state.value, 'laws_activated': len(self.activated_laws)}
    
    def _on_reducing(self) -> dict:
        self.reduced_representation = self._reduce()
        self.emit(EventType.REDUCTION_COMPLETE, CognitiveState.REASONING)
        return {'state': self.state.value}
    
    def _on_reasoning(self) -> dict:
        self.strategy = self._reason()
        self.emit(EventType.REASONING_COMPLETE, CognitiveState.VALIDATING)
        return {'state': self.state.value, 'strategy': self.strategy}
    
    def _on_validating(self) -> dict:
        validation = self._validate_alignment()
        
        if validation['passed']:
            self.emit(EventType.VALIDATION_PASSED, CognitiveState.ACTING)
        else:
            if self.evolution_enabled:
                self.emit(EventType.VALIDATION_FAILED, CognitiveState.EVOLVING)
            else:
                self.emit(EventType.VALIDATION_FAILED, CognitiveState.BLOCKED)
        
        return {'state': self.state.value, 'validation': validation}
    
    def _on_acting(self) -> dict:
        self.emit(EventType.ACTION_COMPLETE, CognitiveState.MONITORING)
        return {'state': self.state.value, 'strategy': self.strategy}
    
    def _on_monitoring(self) -> dict:
        if self.events[-1].payload.get('feedback'):
            return {'state': self.state.value, 'waiting': True}
        
        self.emit(EventType.ACTION_COMPLETE, CognitiveState.COMPLETE)
        return {'state': self.state.value}
    
    def _on_reflecting(self) -> dict:
        drift_analysis = self._analyze_drift()
        
        if drift_analysis['correctable'] and self.evolution_enabled:
            self.emit(EventType.DRIFT_CONFIRMED, CognitiveState.EVOLVING)
        else:
            self.emit(EventType.DRIFT_DETECTED, CognitiveState.BLOCKED)
        
        return {'state': self.state.value, 'drift_analysis': drift_analysis}
    
    def _on_evolving(self) -> dict:
        adaptation = self._evolve()
        self.emit(EventType.EVOLUTION_COMPLETE, CognitiveState.VALIDATING)
        return {'state': self.state.value, 'adaptation': adaptation}
    
    # ==================== 核心算法 ====================
    
    def _extract_constraints(self, text: str) -> list:
        return [w for w in ['must', 'cannot', 'without', 'only'] if w in text.lower()]
    
    def _encode(self, text: str) -> list:
        return [hash(w) % 100 / 100.0 for w in text.split()[:10]]
    
    def _activate_laws(self) -> list:
        activated = []
        for law_id, law in self.laws.items():
            if law.get('applicability', {}).get('contexts'):
                if any(ctx in self.intent.normalized for ctx in law['applicability']['contexts']):
                    activated.append(law)
            else:
                activated.append(law)
        return activated[:5]
    
    def _reduce(self) -> dict:
        return {
            'intent_vector': self.intent.vector,
            'laws': [l['id'] for l in self.activated_laws],
            'invariants': sum([l.get('invariants', []) for l in self.activated_laws], []),
            'abstraction': 0.7
        }
    
    def _reason(self) -> list:
        return [{'action': f"apply_{law['name']}", 'confidence': law.get('confidence', 0.8)} 
                for law in self.activated_laws] or [{'action': 'default', 'confidence': 0.5}]
    
    def _validate_alignment(self) -> dict:
        checks = {}
        
        semantic_score = min(1.0, len(self.strategy) / 2.0)
        checks['semantic_alignment'] = {'score': semantic_score, 'weight': 0.4}
        
        constraint_score = 1.0 if self.intent.constraints else 0.8
        checks['constraint_satisfaction'] = {'score': constraint_score, 'weight': 0.3}
        
        law_score = sum(l.get('confidence', 0.5) for l in self.activated_laws) / max(1, len(self.activated_laws))
        checks['law_consistency'] = {'score': law_score, 'weight': 0.3}
        
        overall = sum(c['score'] * c['weight'] for c in checks.values())
        
        return {
            'passed': overall >= self.intent_guard.threshold,
            'overall_score': overall,
            'checks': checks
        }
    
    def _detect_drift(self, feedback: dict) -> bool:
        return feedback.get('expected') != feedback.get('actual')
    
    def _analyze_drift(self) -> dict:
        return {'correctable': True, 'root_cause': '权重偏移', 'suggestion': '调整置信度'}
    
    def _evolve(self) -> dict:
        return {'type': 'confidence_adjustment', 'changes': []}
    
    # ==================== 状态查询 ====================
    
    def get_result(self) -> dict:
        return {
            'agent_id': self.id,
            'state': self.state.value,
            'intent_id': self.intent.id if self.intent else None,
            'strategy': self.strategy,
            'events': len(self.events)
        }
    
    @property
    def is_complete(self) -> bool:
        return self.state in [CognitiveState.COMPLETE, CognitiveState.ERROR, CognitiveState.BLOCKED]


# ==================== 使用示例 ====================

if __name__ == '__main__':
    agent = EventDrivenCognitiveAgent()
    
    agent.receive_intent("优化系统性能，确保响应时间<100ms")
    
    result = agent.run_until_complete()
    print(json.dumps(result, indent=2, ensure_ascii=False))
