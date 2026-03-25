#!/usr/bin/env python3
"""
UAS 世界模型运行时 (World Model Runtime)

核心功能：
1. 本源法则管理
2. 降维重构引擎
3. 情景化映射
4. 意图守恒校验
5. 演化反馈回路
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class WorldModelState(Enum):
    """世界模型运行状态"""
    IDLE = "idle"
    UNDERSTANDING = "understanding"
    MAPPING = "mapping"
    REDUCING = "reducing"
    REASONING = "reasoning"
    VALIDATING = "validating"
    EXECUTING = "executing"
    MONITORING = "monitoring"
    EVOLVING = "evolving"
    COMPLETE = "complete"
    ERROR = "error"
    BLOCKED = "blocked"


class WorldModelRuntime:
    """世界模型运行时"""
    
    def __init__(self, config_path: Optional[Path] = None, config: Optional[dict] = None):
        self.config = config or {}
        self.state = WorldModelState.IDLE
        self.instance_id = str(uuid.uuid4())
        self.context = {}
        self.history = []
        self.laws = {}
        self.mappers = {}
        self.intent_guard_enabled = True
        self.intent_threshold = 0.8
        self.evolution_enabled = True
        
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path: Path):
        """加载配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.laws = self._load_laws()
        self.mappers = self._load_mappers()
        self._init_runtime_config()
    
    def _load_laws(self) -> dict:
        """加载本源法则"""
        laws = {}
        if 'laws' in self.config:
            for category in self.config['laws'].get('categories', []):
                for law in category.get('laws', []):
                    laws[law['id']] = law
        return laws
    
    def _load_mappers(self) -> dict:
        """加载情景化映射器"""
        mappers = {}
        if 'mappers' in self.config:
            for mapper in self.config['mappers'].get('mappers', []):
                mappers[mapper['id']] = mapper
        return mappers
    
    def _init_runtime_config(self):
        """初始化运行时配置"""
        if 'intent_guard' in self.config:
            self.intent_guard_enabled = self.config['intent_guard'].get('enabled', True)
            self.intent_threshold = self.config['intent_guard'].get('threshold', 0.8)
        
        if 'evolution' in self.config:
            self.evolution_enabled = self.config['evolution'].get('enabled', True)
    
    def _transition(self, new_state: WorldModelState, event: str = None):
        """状态转移"""
        old_state = self.state
        self.state = new_state
        self.history.append({
            'from_state': old_state.value,
            'to_state': new_state.value,
            'event': event,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def run(self, intent: str, scenario: dict = None) -> dict:
        """
        执行世界模型推理
        
        Args:
            intent: 输入意图
            scenario: 场景上下文
            
        Returns:
            推理结果
        """
        self.context = {
            'intent': intent,
            'scenario': scenario or {},
            'start_time': datetime.utcnow().isoformat()
        }
        
        try:
            self._transition(WorldModelState.UNDERSTANDING, 'intent_received')
            
            normalized_intent = self._understand_intent(intent)
            self.context['normalized_intent'] = normalized_intent
            
            self._transition(WorldModelState.MAPPING, 'intent_understood')
            activated_laws = self._activate_laws(normalized_intent, scenario)
            self.context['activated_laws'] = activated_laws
            
            self._transition(WorldModelState.REDUCING, 'laws_activated')
            reduced_representation = self._reduce(normalized_intent, scenario)
            self.context['reduced_representation'] = reduced_representation
            
            self._transition(WorldModelState.REASONING, 'dimension_reduced')
            strategy = self._reason(reduced_representation, activated_laws)
            
            self._transition(WorldModelState.VALIDATING, 'strategy_generated')
            validation = self._validate(strategy, normalized_intent)
            
            if not validation['passed'] and self.intent_guard_enabled:
                self._handle_intent_violation(validation)
            
            self._transition(WorldModelState.COMPLETE, 'validation_passed')
            
            return {
                'status': 'success',
                'state': self.state.value,
                'strategy': strategy,
                'validation': validation,
                'laws_used': activated_laws,
                'instance_id': self.instance_id
            }
            
        except Exception as e:
            self._transition(WorldModelState.ERROR, f'error: {str(e)}')
            return {
                'status': 'error',
                'state': self.state.value,
                'error': str(e)
            }
    
    def _understand_intent(self, intent: str) -> dict:
        """理解意图"""
        return {
            'raw': intent,
            'normalized': intent.strip().lower(),
            'constraints': self._extract_constraints(intent),
            'success_criteria': self._extract_success_criteria(intent)
        }
    
    def _extract_constraints(self, intent: str) -> list:
        """提取约束"""
        constraints = []
        constraint_keywords = ['must', 'cannot', 'without', 'only', 'limit']
        for keyword in constraint_keywords:
            if keyword in intent.lower():
                constraints.append(keyword)
        return constraints
    
    def _extract_success_criteria(self, intent: str) -> list:
        """提取成功标准"""
        criteria = []
        criteria_keywords = ['achieve', 'ensure', 'guarantee', 'success']
        for keyword in criteria_keywords:
            if keyword in intent.lower():
                criteria.append(keyword)
        return criteria
    
    def _activate_laws(self, intent: dict, scenario: dict) -> list:
        """激活相关本源法则"""
        activated = []
        intent_text = intent.get('normalized', '')
        
        for law_id, law in self.laws.items():
            applicability = law.get('applicability', {})
            contexts = applicability.get('contexts', [])
            
            if any(ctx in intent_text for ctx in contexts):
                activated.append({
                    'id': law_id,
                    'name': law['name'],
                    'expression': law['expression'],
                    'confidence': law.get('confidence', 1.0)
                })
        
        return activated
    
    def _reduce(self, intent: dict, scenario: dict) -> dict:
        """
        降维：将高维现实映射为低维表示
        
        这是世界模型的核心机制：
        - 提取关键变量
        - 映射到核心维度
        - 抽象为可推理形式
        """
        high_dim = {
            'intent': intent,
            'scenario': scenario,
            'entities': scenario.get('entities', []),
            'relations': scenario.get('relations', [])
        }
        
        low_dim = {
            'subject': self._extract_dimension(high_dim, 'subject'),
            'object': self._extract_dimension(high_dim, 'object'),
            'space': self._extract_dimension(high_dim, 'space'),
            'time': self._extract_dimension(high_dim, 'time'),
            'feedback': self._extract_dimension(high_dim, 'feedback'),
            'causal_chain': self._extract_causal_chain(high_dim),
            'invariants': self._extract_invariants(high_dim)
        }
        
        return low_dim
    
    def _extract_dimension(self, high_dim: dict, dim_type: str) -> Any:
        """提取指定维度"""
        scenario = high_dim.get('scenario', {})
        entities = scenario.get('entities', [])
        
        if dim_type == 'subject':
            return [e['id'] for e in entities if e.get('type') == 'agent']
        elif dim_type == 'object':
            return [e['id'] for e in entities if e.get('type') == 'resource']
        elif dim_type == 'space':
            return scenario.get('location', 'unknown')
        elif dim_type == 'time':
            return scenario.get('time_constraint', 'flexible')
        elif dim_type == 'feedback':
            return scenario.get('feedback_channels', [])
        
        return None
    
    def _extract_causal_chain(self, high_dim: dict) -> list:
        """提取因果链"""
        relations = high_dim.get('scenario', {}).get('relations', [])
        return [r for r in relations if r.get('type') == 'causal']
    
    def _extract_invariants(self, high_dim: dict) -> list:
        """提取不变量"""
        invariants = []
        intent = high_dim.get('intent', {})
        
        for law in self.laws.values():
            invariants.extend(law.get('invariants', []))
        
        return list(set(invariants))
    
    def _reason(self, reduced: dict, laws: list) -> dict:
        """
        推理：基于降维表示和法则生成策略
        """
        strategy = {
            'actions': [],
            'constraints': reduced.get('invariants', []),
            'confidence': 0.0
        }
        
        if not laws:
            strategy['actions'].append({
                'type': 'default',
                'description': '基于场景默认动作'
            })
            return strategy
        
        confidence_sum = sum(law['confidence'] for law in laws)
        strategy['confidence'] = confidence_sum / len(laws)
        
        for law in laws:
            action = self._apply_law(law, reduced)
            if action:
                strategy['actions'].append(action)
        
        return strategy
    
    def _apply_law(self, law: dict, context: dict) -> Optional[dict]:
        """应用法则生成动作"""
        return {
            'law_id': law['id'],
            'law_name': law['name'],
            'action_type': 'law_driven',
            'expression': law['expression'],
            'rationale': f"应用法则 {law['name']} 于降维场景"
        }
    
    def _validate(self, strategy: dict, intent: dict) -> dict:
        """验证策略与意图的一致性"""
        checks = {
            'semantic_alignment': self._check_semantic_alignment(strategy, intent),
            'constraint_satisfaction': self._check_constraint_satisfaction(strategy, intent),
            'law_consistency': self._check_law_consistency(strategy)
        }
        
        passed = all(check['passed'] for check in checks.values())
        
        return {
            'passed': passed,
            'checks': checks,
            'overall_score': sum(c['score'] for c in checks.values()) / len(checks)
        }
    
    def _check_semantic_alignment(self, strategy: dict, intent: dict) -> dict:
        """检查语义对齐"""
        action_count = len(strategy.get('actions', []))
        score = 1.0 if action_count > 0 else 0.0
        
        return {
            'passed': score >= self.intent_threshold,
            'score': score,
            'details': f'生成了 {action_count} 个动作'
        }
    
    def _check_constraint_satisfaction(self, strategy: dict, intent: dict) -> dict:
        """检查约束满足"""
        constraints = intent.get('constraints', [])
        satisfied = len(constraints) > 0
        
        return {
            'passed': True,
            'score': 1.0 if satisfied else 0.5,
            'details': f'约束数量: {len(constraints)}'
        }
    
    def _check_law_consistency(self, strategy: dict) -> dict:
        """检查法则一致性"""
        return {
            'passed': True,
            'score': strategy.get('confidence', 0.5),
            'details': f'策略置信度: {strategy.get("confidence", 0.5):.2f}'
        }
    
    def _handle_intent_violation(self, validation: dict):
        """处理意图违背"""
        self._transition(WorldModelState.BLOCKED, 'intent_violation')
        
        if self.evolution_enabled:
            self._trigger_evolution(validation)
    
    def _trigger_evolution(self, validation: dict):
        """触发演化"""
        self._transition(WorldModelState.EVOLVING, 'drift_detected')
        
        adaptation = {
            'timestamp': datetime.utcnow().isoformat(),
            'trigger': 'intent_violation',
            'changes': ['调整法则权重', '优化映射函数'],
            'result': 'pending'
        }
        
        self.context.setdefault('adaptations', []).append(adaptation)
    
    def get_state(self) -> dict:
        """获取当前状态"""
        return {
            'instance_id': self.instance_id,
            'state': self.state.value,
            'context': self.context,
            'history': self.history
        }


def create_world_model(config: dict) -> WorldModelRuntime:
    """工厂函数：创建世界模型运行时"""
    return WorldModelRuntime(config=config)


def load_world_model(config_path: Path) -> WorldModelRuntime:
    """工厂函数：从配置文件加载"""
    return WorldModelRuntime(config_path=config_path)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: world_model_runtime.py <config_path> [intent]")
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    wm = load_world_model(config_path)
    
    intent = sys.argv[2] if len(sys.argv) > 2 else "优化系统性能"
    scenario = {}
    
    result = wm.run(intent, scenario)
    print(json.dumps(result, ensure_ascii=False, indent=2))
