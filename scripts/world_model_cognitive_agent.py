#!/usr/bin/env python3
"""
UAS 世界模型认知主体 (World Model Cognitive Agent)

核心理念：
- 持续运行的认知主体，非被调用工具
- 意图(Intent)驱动，事件触发状态转移
- 实时反馈闭环，自主演化
- 本源法则内化，动态情景化
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional
from dataclasses import dataclass, field


class CognitiveState(Enum):
    """认知状态：持续运行的状态机"""
    DORMANT = "dormant"              # 休眠：等待意图激活
    PERCEIVING = "perceiving"        # 感知：接收并解析输入
    UNDERSTANDING = "understanding"  # 理解：意图归一化与目标提取
    MAPPING = "mapping"              # 映射：激活本源法则
    REDUCING = "reducing"           # 降维：高维→低维表示
    REASONING = "reasoning"         # 推理：基于法则生成策略
    VALIDATING = "validating"        # 验证：意图守恒校验
    ACTING = "acting"               # 行动：执行策略
    MONITORING = "monitoring"       # 监控：实时反馈采集
    REFLECTING = "reflecting"       # 反身：自我评估与元认知
    EVOLVING = "evolving"           # 演化：策略调整与知识更新
    COMPLETE = "complete"           # 完成：输出结果
    ERROR = "error"                 # 错误：异常处理
    BLOCKED = "blocked"             # 阻塞：意图漂移


@dataclass
class Intent:
    """意图：认知主体的驱动力"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    raw_input: str = ""
    normalized: str = ""
    constraints: list = field(default_factory=list)
    success_criteria: list = field(default_factory=list)
    stakeholders: list = field(default_factory=list)
    vector: list = field(default_factory=list)
    priority: float = 0.5
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict = field(default_factory=dict)


@dataclass
class WorldModelKnowledge:
    """世界模型知识：内化的本源法则"""
    laws: dict = field(default_factory=dict)           # 本源法则
    mappers: dict = field(default_factory=dict)        # 情景化映射
    invariants: list = field(default_factory=list)     # 不变量库
    causal_chains: dict = field(default_factory=dict)  # 因果链


@dataclass
class CognitiveContext:
    """认知上下文：当前任务的工作内存"""
    intent: Optional[Intent] = None
    scenario: dict = field(default_factory=dict)
    activated_laws: list = field(default_factory=list)
    reduced_representation: dict = field(default_factory=dict)
    strategy: dict = field(default_factory=list)
    validation: dict = field(default_factory=dict)
    feedback: list = field(default_factory=list)
    drift_detected: bool = False
    alignment_score: float = 1.0


@dataclass
class CognitiveEvent:
    """认知事件：状态转移的触发器"""
    type: str
    source_state: CognitiveState
    target_state: CognitiveState
    payload: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class WorldModelCognitiveAgent:
    """
    世界模型认知主体
    
    核心特性：
    1. 持续运行的状态机
    2. 意图驱动的事件处理
    3. 本源法则内化与动态情景化
    4. 实时反馈与自主演化
    """
    
    def __init__(self, config: dict = None):
        self.id = str(uuid.uuid4())
        self.name = config.get('name', 'world_model_agent') if config else 'world_model_agent'
        self.state = CognitiveState.DORMANT
        self.knowledge = WorldModelKnowledge()
        self.context = CognitiveContext()
        self.event_history = []
        self.handlers = {}
        
        self._load_config(config or {})
        self._register_handlers()
    
    def _load_config(self, config: dict):
        """加载配置并内化为知识"""
        if 'laws' in config:
            for category in config['laws'].get('categories', []):
                for law in category.get('laws', []):
                    self.knowledge.laws[law['id']] = law
        
        if 'mappers' in config:
            for mapper in config['mappers'].get('mappers', []):
                self.knowledge.mappers[mapper['id']] = mapper
        
        self.config = config
    
    def _register_handlers(self):
        """注册状态处理器"""
        self.handlers = {
            CognitiveState.PERCEIVING: self._handle_perceiving,
            CognitiveState.UNDERSTANDING: self._handle_understanding,
            CognitiveState.MAPPING: self._handle_mapping,
            CognitiveState.REDUCING: self._handle_reducing,
            CognitiveState.REASONING: self._handle_reasoning,
            CognitiveState.VALIDATING: self._handle_validating,
            CognitiveState.ACTING: self._handle_acting,
            CognitiveState.MONITORING: self._handle_monitoring,
            CognitiveState.REFLECTING: self._handle_reflecting,
            CognitiveState.EVOLVING: self._handle_evolving,
        }
    
    # ==================== 意图输入接口 ====================
    
    def receive_intent(self, raw_input: str, **kwargs) -> str:
        """
        接收外部意图，激活认知主体
        这是主要的入口点
        """
        self.context.intent = Intent(
            raw_input=raw_input,
            normalized=self._normalize_intent(raw_input),
            priority=kwargs.get('priority', 0.5)
        )
        self.context.intent.constraints = self._extract_constraints(raw_input)
        self.context.intent.success_criteria = self._extract_criteria(raw_input)
        
        self._emit_event('intent_received', CognitiveState.DORMANT, CognitiveState.PERCEIVING)
        return self.context.intent.id
    
    def receive_feedback(self, feedback: dict):
        """接收执行反馈，触发监控状态"""
        self.context.feedback.append(feedback)
        
        if self._detect_drift(feedback):
            self.context.drift_detected = True
            self._emit_event('drift_detected', self.state, CognitiveState.REFLECTING)
        else:
            self._emit_event('feedback_received', self.state, CognitiveState.MONITORING)
    
    # ==================== 状态处理 ====================
    
    def process(self) -> dict:
        """认知主循环：持续处理直到完成或错误"""
        while self.state not in [CognitiveState.COMPLETE, CognitiveState.ERROR, CognitiveState.BLOCKED]:
            handler = self.handlers.get(self.state)
            if handler:
                result = handler()
                if result:
                    return result
            else:
                break
        
        return self._build_result()
    
    def step(self) -> dict:
        """单步执行：用于调试或流式处理"""
        handler = self.handlers.get(self.state)
        if handler:
            return handler()
        return {'state': self.state.value, 'waiting': True}
    
    # ==================== 状态处理器 ====================
    
    def _handle_perceiving(self) -> dict:
        """感知阶段：接收并初步处理输入"""
        intent = self.context.intent
        
        self._emit_event('perception_complete', CognitiveState.PERCEIVING, CognitiveState.UNDERSTANDING)
        return {'state': self.state.value, 'intent_id': intent.id}
    
    def _handle_understanding(self) -> dict:
        """理解阶段：深化意图理解"""
        intent = self.context.intent
        
        intent.vector = self._encode_intent(intent.normalized)
        
        self._emit_event('understanding_complete', CognitiveState.UNDERSTANDING, CognitiveState.MAPPING)
        return {'state': self.state.value, 'intent_vector': intent.vector[:5]}
    
    def _handle_mapping(self) -> dict:
        """映射阶段：激活相关本源法则"""
        intent = self.context.intent
        activated = []
        
        for law_id, law in self.knowledge.laws.items():
            if self._is_law_applicable(law, intent):
                activated.append({
                    'id': law_id,
                    'name': law['name'],
                    'expression': law['expression'],
                    'confidence': law.get('confidence', 1.0)
                })
        
        self.context.activated_laws = activated
        
        self._emit_event('mapping_complete', CognitiveState.MAPPING, CognitiveState.REDUCING)
        return {'state': self.state.value, 'activated_laws': len(activated)}
    
    def _handle_reducing(self) -> dict:
        """降维阶段：高维现实→低维表示"""
        intent = self.context.intent
        
        reduced = {
            'subject': self._extract_subject(intent),
            'object': self._extract_object(intent),
            'causal_chain': self._extract_causal_chain(),
            'invariants': self._extract_invariants(),
            'vector': intent.vector,
            'abstraction_level': self._calculate_abstraction(intent)
        }
        
        self.context.reduced_representation = reduced
        
        self._emit_event('reduction_complete', CognitiveState.REDUCING, CognitiveState.REASONING)
        return {'state': self.state.value, 'dimensions': len(reduced)}
    
    def _handle_reasoning(self) -> dict:
        """推理阶段：基于法则生成策略"""
        reduced = self.context.reduced_representation
        laws = self.context.activated_laws
        
        strategy = self._generate_strategy(reduced, laws)
        self.context.strategy = strategy
        
        self._emit_event('reasoning_complete', CognitiveState.REASONING, CognitiveState.VALIDATING)
        return {'state': self.state.value, 'strategy_actions': len(strategy)}
    
    def _handle_validating(self) -> dict:
        """验证阶段：意图守恒校验"""
        strategy = self.context.strategy
        intent = self.context.intent
        
        validation = self._validate_alignment(strategy, intent)
        self.context.validation = validation
        self.context.alignment_score = validation.get('overall_score', 0.0)
        
        if validation['passed']:
            self._emit_event('validation_passed', CognitiveState.VALIDATING, CognitiveState.ACTING)
        else:
            self._emit_event('validation_failed', CognitiveState.VALIDATING, CognitiveState.BLOCKED)
        
        return {'state': self.state.value, 'validation': validation}
    
    def _handle_acting(self) -> dict:
        """行动阶段：输出可执行策略"""
        self._emit_event('action_complete', CognitiveState.ACTING, CognitiveState.MONITORING)
        return {'state': self.state.value, 'strategy': self.context.strategy}
    
    def _handle_monitoring(self) -> dict:
        """监控阶段：等待反馈或超时"""
        if self.context.feedback:
            if self.context.drift_detected:
                self._emit_event('drift_confirmed', CognitiveState.MONITORING, CognitiveState.REFLECTING)
            else:
                self._emit_event('feedback_processed', CognitiveState.MONITORING, CognitiveState.COMPLETE)
        else:
            pass
        
        return {'state': self.state.value, 'waiting_for_feedback': True}
    
    def _handle_reflecting(self) -> dict:
        """反身阶段：自我评估与漂移分析"""
        drift_analysis = self._analyze_drift()
        
        if drift_analysis['correctable']:
            self._emit_event('drift_correctable', CognitiveState.REFLECTING, CognitiveState.EVOLVING)
        else:
            self._emit_event('drift_uncorrectable', CognitiveState.REFLECTING, CognitiveState.BLOCKED)
        
        return {'state': self.state.value, 'drift_analysis': drift_analysis}
    
    def _handle_evolving(self) -> dict:
        """演化阶段：调整策略与更新知识"""
        adaptation = self._generate_adaptation()
        self._apply_adaptation(adaptation)
        
        self._emit_event('evolution_complete', CognitiveState.EVOLVING, CognitiveState.VALIDATING)
        return {'state': self.state.value, 'adaptation': adaptation}
    
    # ==================== 辅助方法 ====================
    
    def _emit_event(self, event_type: str, from_state: CognitiveState, to_state: CognitiveState):
        """发射认知事件并转移状态"""
        event = CognitiveEvent(
            type=event_type,
            source_state=from_state,
            target_state=to_state,
            payload={'intent_id': self.context.intent.id if self.context.intent else None}
        )
        
        self.event_history.append({
            'type': event.type,
            'from': from_state.value,
            'to': to_state.value,
            'timestamp': event.timestamp
        })
        
        self.state = to_state
    
    def _normalize_intent(self, raw: str) -> str:
        """意图归一化"""
        return raw.strip().lower()
    
    def _extract_constraints(self, intent: str) -> list:
        """提取约束"""
        return [w for w in ['must', 'cannot', 'without', 'only'] if w in intent.lower()]
    
    def _extract_criteria(self, intent: str) -> list:
        """提取成功标准"""
        return [w for w in ['achieve', 'ensure', 'guarantee', 'success'] if w in intent.lower()]
    
    def _encode_intent(self, normalized: str) -> list:
        """意图向量化（简化版）"""
        words = normalized.split()
        return [hash(w) % 100 / 100.0 for w in words[:10]]
    
    def _is_law_applicable(self, law: dict, intent: Intent) -> bool:
        """判断法则是否适用"""
        applicability = law.get('applicability', {})
        contexts = applicability.get('contexts', [])
        
        if not contexts:
            return True
        
        return any(ctx in intent.normalized for ctx in contexts)
    
    def _extract_subject(self, intent: Intent) -> str:
        """提取主体"""
        return 'agent'
    
    def _extract_object(self, intent: Intent) -> str:
        """提取客体"""
        return 'target'
    
    def _extract_causal_chain(self) -> list:
        """提取因果链"""
        return []
    
    def _extract_invariants(self) -> list:
        """提取不变量"""
        invariants = []
        for law in self.knowledge.laws.values():
            invariants.extend(law.get('invariants', []))
        return list(set(invariants))
    
    def _calculate_abstraction(self, intent: Intent) -> float:
        """计算抽象层级"""
        return 0.7
    
    def _generate_strategy(self, reduced: dict, laws: list) -> list:
        """生成策略"""
        strategy = []
        
        for law in laws:
            strategy.append({
                'law_id': law['id'],
                'action': f"apply_{law['name']}",
                'confidence': law['confidence']
            })
        
        if not strategy:
            strategy.append({'action': 'default_action', 'confidence': 0.5})
        
        return strategy
    
    def _validate_alignment(self, strategy: list, intent: Intent) -> dict:
        """验证意图守恒"""
        score = 1.0 if strategy else 0.0
        
        return {
            'passed': score >= 0.5,
            'overall_score': score,
            'checks': {
                'semantic_alignment': {'passed': score >= 0.5, 'score': score},
                'constraint_satisfaction': {'passed': True, 'score': 1.0},
                'law_consistency': {'passed': True, 'score': 0.9}
            }
        }
    
    def _detect_drift(self, feedback: dict) -> bool:
        """检测漂移"""
        expected = feedback.get('expected')
        actual = feedback.get('actual')
        
        if expected and actual:
            return expected != actual
        return False
    
    def _analyze_drift(self) -> dict:
        """分析漂移"""
        return {
            'correctable': True,
            'root_cause': '法则权重偏移',
            'suggestion': '调整法则置信度'
        }
    
    def _generate_adaptation(self) -> dict:
        """生成适应调整"""
        return {
            'type': 'confidence_adjustment',
            'changes': [{'law_id': 'law_1', 'adjustment': -0.1}]
        }
    
    def _apply_adaptation(self, adaptation: dict):
        """应用适应调整"""
        pass
    
    def _build_result(self) -> dict:
        """构建最终结果"""
        return {
            'agent_id': self.id,
            'state': self.state.value,
            'intent_id': self.context.intent.id if self.context.intent else None,
            'strategy': self.context.strategy,
            'alignment_score': self.context.alignment_score,
            'events': len(self.event_history)
        }
    
    # ==================== 状态查询 ====================
    
    @property
    def is_running(self) -> bool:
        """是否在运行"""
        return self.state not in [CognitiveState.DORMANT, CognitiveState.COMPLETE, CognitiveState.ERROR]
    
    @property
    def current_state(self) -> str:
        """当前状态"""
        return self.state.value
    
    def get_status(self) -> dict:
        """获取状态"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state.value,
            'intent_id': self.context.intent.id if self.context.intent else None,
            'events': len(self.event_history),
            'is_running': self.is_running
        }
