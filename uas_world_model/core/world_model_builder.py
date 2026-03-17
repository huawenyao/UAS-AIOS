"""
UAS世界模型 - P1: LLM世界模型程序化构建

功能：
- 将世界模型编译为Python代码
- 程序化知识表示
- 知识迁移与复用
- 对标WorldCoder架构
"""

import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


class ProgramState(Enum):
    DRAFT = "draft"
    SYNTHESIZING = "synthesizing"
    TESTING = "testing"
    VALID = "valid"
    INVALID = "invalid"


@dataclass
class WorldModelProgram:
    """世界模型程序"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    
    # 转换函数: T(s'|s, a)
    transition_code: str = ""
    
    # 奖励函数: R(s, a)
    reward_code: str = ""
    
    state: ProgramState = ProgramState.DRAFT
    
    confidence: float = 0.0
    test_results: list = field(default_factory=list)
    
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class Experience:
    """经验数据"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state: dict = field(default_factory=dict)
    action: dict = field(default_factory=dict)
    next_state: dict = field(default_factory=dict)
    reward: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class SynthesisResult:
    """程序合成结果"""
    program: WorldModelProgram
    success: bool
    error: str = ""
    iterations: int = 0


class LLMInterface(ABC):
    """LLM接口抽象"""
    
    @abstractmethod
    def chat(self, prompt: str, **kwargs) -> str:
        pass


class WorldModelBuilder:
    """
    LLM世界模型构建器
    
    对标WorldCoder架构：
    1. 接收经验数据
    2. LLM生成候选程序
    3. 测试与调试
    4. 输出转换函数T(s'|s,a)
    """
    
    def __init__(self, llm: LLMInterface = None, config: dict = None):
        self.llm = llm
        self.config = config or {}
        self.programs: dict[str, WorldModelProgram] = {}
        self.experiences: list[Experience] = []
        
        self.max_iterations = self.config.get('max_iterations', 5)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.8)
    
    def add_experience(self, experience: Experience):
        """添加经验数据"""
        self.experiences.append(experience)
    
    def add_experiences(self, experiences: list[Experience]):
        """批量添加经验"""
        self.experiences.extend(experiences)
    
    def build(self, name: str, description: str = "") -> SynthesisResult:
        """
        构建世界模型程序
        
        Args:
            name: 程序名称
            description: 描述
            
        Returns:
            SynthesisResult: 合成结果
        """
        if not self.experiences:
            return SynthesisResult(
                program=WorldModelProgram(name=name, description=description),
                success=False,
                error="No experiences provided"
            )
        
        program = WorldModelProgram(
            name=name,
            description=description,
            state=ProgramState.SYNTHESIZING
        )
        
        # 迭代合成
        for iteration in range(self.max_iterations):
            # 1. 生成候选程序
            code = self._synthesize_program(program)
            
            if code:
                program.transition_code = code.get('transition', '')
                program.reward_code = code.get('reward', '')
            
            # 2. 测试程序
            test_results = self._test_program(program)
            program.test_results = test_results
            
            # 3. 评估结果
            if test_results['passed']:
                program.state = ProgramState.VALID
                program.confidence = test_results['accuracy']
                self.programs[program.id] = program
                return SynthesisResult(
                    program=program,
                    success=True,
                    iterations=iteration + 1
                )
            
            # 4. 调试（如果失败）
            if iteration < self.max_iterations - 1:
                error_msg = test_results.get('error', 'Unknown error')
                program = self._debug_program(program, error_msg)
        
        program.state = ProgramState.INVALID
        return SynthesisResult(
            program=program,
            success=False,
            error="Max iterations reached",
            iterations=self.max_iterations
        )
    
    def _synthesize_program(self, program: WorldModelProgram) -> dict:
        """使用LLM合成程序"""
        if not self.llm:
            return self._generate_fallback_program(program)
        
        # 准备经验数据样本
        sample_size = min(10, len(self.experiences))
        samples = self.experiences[:sample_size]
        
        prompt = self._build_synthesis_prompt(program, samples)
        response = self.llm.chat(prompt)
        
        try:
            return json.loads(response)
        except:
            return self._generate_fallback_program(program)
    
    def _build_synthesis_prompt(self, program: WorldModelProgram, samples: list[Experience]) -> str:
        """构建合成提示"""
        samples_json = json.dumps([
            {
                'state': s.state,
                'action': s.action,
                'next_state': s.next_state,
                'reward': s.reward
            }
            for s in samples
        ], indent=2)
        
        return f"""作为世界模型工程师，请根据以下经验数据生成Python代码形式的转换函数和奖励函数：

任务描述: {program.description}

经验数据样本:
{samples_json}

请JSON格式输出：
{{
    "transition": "def transition(state, action):\\n    # 实现状态转换逻辑\\n    return next_state",
    "reward": "def reward(state, action):\\n    # 实现奖励计算\\n    return reward_value",
    "explanation": "代码解释"
}}

要求：
1. transition函数接受state和action字典，返回next_state字典
2. reward函数接受state和action，返回浮点数奖励值
3. 代码应该能解释观察到的状态转换模式
4. 使用简洁的Python实现"""
    
    def _generate_fallback_program(self, program: WorldModelProgram) -> dict:
        """生成fallback程序（基于统计）"""
        # 简单实现：复制最后一次观察的转换
        if not self.experiences:
            return {"transition": "", "reward": ""}
        
        last = self.experiences[-1]
        
        transition_code = f"""
def transition(state, action):
    # Fallback: 基于统计的简单转换
    return {json.dumps(last.next_state)}

def get_invariants():
    # 从经验中提取的不变量
    return ["状态转换遵循特定规律"]
"""
        
        reward_code = f"""
def reward(state, action):
    # Fallback: 基于奖励的简单计算
    return {last.reward}
"""
        
        return {
            "transition": transition_code,
            "reward": reward_code
        }
    
    def _test_program(self, program: WorldModelProgram) -> dict:
        """测试程序"""
        if not program.transition_code:
            return {"passed": False, "error": "No transition code", "accuracy": 0.0}
        
        try:
            # 编译代码
            namespace = {}
            exec(program.transition_code, namespace)
            transition_fn = namespace.get('transition')
            
            if program.reward_code:
                exec(program.reward_code, namespace)
                reward_fn = namespace.get('reward')
            else:
                reward_fn = None
            
            if not transition_fn:
                return {"passed": False, "error": "No transition function", "accuracy": 0.0}
            
            # 测试每个经验
            correct = 0
            total = len(self.experiences)
            
            for exp in self.experiences:
                # 预测下一状态
                predicted_next = transition_fn(exp.state, exp.action)
                
                # 检查是否匹配
                if self._states_match(predicted_next, exp.next_state):
                    correct += 1
            
            accuracy = correct / total if total > 0 else 0.0
            
            return {
                "passed": accuracy >= self.confidence_threshold,
                "accuracy": accuracy,
                "correct": correct,
                "total": total
            }
            
        except Exception as e:
            return {"passed": False, "error": str(e), "accuracy": 0.0}
    
    def _states_match(self, predicted: dict, actual: dict) -> bool:
        """检查状态是否匹配"""
        if not predicted or not actual:
            return False
        
        # 简单实现：检查关键属性
        for key in actual:
            if key in predicted:
                if predicted[key] != actual[key]:
                    return False
        
        return True
    
    def _debug_program(self, program: WorldModelProgram, error: str) -> WorldModelProgram:
        """调试程序"""
        if not self.llm:
            return program
        
        prompt = f"""调试以下世界模型程序：

错误信息: {error}
当前代码:
{program.transition_code}

请修复代码中的错误，保持相同的函数签名：
def transition(state, action):
    # 修复后的实现
"""
        
        response = self.llm.chat(prompt)
        
        try:
            data = json.loads(response)
            if 'transition' in data:
                program.transition_code = data['transition']
        except:
            pass
        
        program.updated_at = datetime.utcnow().isoformat()
        return program
    
    def use_program(self, program: WorldModelProgram) -> Callable:
        """将程序编译为可执行函数"""
        if program.state != ProgramState.VALID:
            raise ValueError("Program is not valid")
        
        namespace = {}
        exec(program.transition_code, namespace)
        
        return namespace.get('transition')


class SymbolicWorldModel:
    """
    符号化世界模型（编译后的可执行形式）
    """
    
    def __init__(self, program: WorldModelProgram):
        self.program = program
        self.transition_fn = None
        self.reward_fn = None
        self._compile()
    
    def _compile(self):
        """编译程序"""
        if self.program.transition_code:
            namespace = {}
            exec(self.program.transition_code, namespace)
            self.transition_fn = namespace.get('transition')
        
        if self.program.reward_code:
            namespace = {}
            exec(self.program.reward_code, namespace)
            self.reward_fn = namespace.get('reward')
    
    def predict(self, state: dict, action: dict) -> dict:
        """预测下一状态"""
        if self.transition_fn:
            return self.transition_fn(state, action)
        return state
    
    def evaluate(self, state: dict, action: dict) -> float:
        """评估奖励"""
        if self.reward_fn:
            return self.reward_fn(state, action)
        return 0.0
    
    def clone(self) -> 'SymbolicWorldModel':
        """克隆"""
        return SymbolicWorldModel(self.program)
    
    def to_code(self) -> str:
        """导出为代码"""
        return f"""# World Model: {self.program.name}
# Description: {self.program.description}
# Confidence: {self.program.confidence}

{self.program.transition_code}

{self.program.reward_code}
"""


class WorldModelLibrary:
    """
    世界模型库（程序化管理与复用）
    """
    
    def __init__(self):
        self.programs: dict[str, WorldModelProgram] = {}
        self.builder = WorldModelBuilder()
    
    def add(self, program: WorldModelProgram):
        """添加程序"""
        self.programs[program.id] = program
    
    def get(self, program_id: str) -> Optional[WorldModelProgram]:
        """获取程序"""
        return self.programs.get(program_id)
    
    def find_relevant(self, context: dict) -> list[WorldModelProgram]:
        """查找相关程序"""
        relevant = []
        
        for program in self.programs.values():
            if program.state != ProgramState.VALID:
                continue
            
            # 简单匹配：检查元数据
            score = 0
            for key, value in context.items():
                if program.metadata.get(key) == value:
                    score += 1
            
            if score > 0:
                relevant.append(program)
        
        return sorted(relevant, key=lambda p: p.confidence, reverse=True)
    
    def compile(self, program_id: str) -> SymbolicWorldModel:
        """编译为可执行模型"""
        program = self.get(program_id)
        if not program:
            raise ValueError(f"Program {program_id} not found")
        
        return SymbolicWorldModel(program)


# 导出
__all__ = [
    'WorldModelProgram',
    'Experience',
    'SynthesisResult',
    'ProgramState',
    'WorldModelBuilder',
    'SymbolicWorldModel',
    'WorldModelLibrary',
]
