"""
UAS世界模型 - P1: 规划驱动推理引擎

功能：
- 基于世界模型的模拟推演
- 成本最小化路径选择
- 多步规划与评估
- 对标SimuRA架构
"""

import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


class PlanningState(Enum):
    IDLE = "idle"
    SIMULATING = "simulating"
    EVALUATING = "evaluating"
    SELECTING = "selecting"
    EXECUTING = "executing"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class WorldState:
    """世界状态"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    attributes: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class Action:
    """动作"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    preconditions: list = field(default_factory=list)
    effects: dict = field(default_factory=dict)
    cost: float = 1.0


@dataclass
class Trajectory:
    """轨迹"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    states: list = field(default_factory=list)
    actions: list = field(default_factory=list)
    total_cost: float = 0.0
    score: float = 0.0
    goal_distance: float = float('inf')


@dataclass
class Plan:
    """规划结果"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trajectories: list = field(default_factory=list)
    selected_action: Optional[Action] = None
    reasoning: str = ""
    confidence: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class WorldModelInterface(ABC):
    """世界模型接口"""
    
    @abstractmethod
    def simulate(self, state: WorldState, action: Action) -> WorldState:
        """模拟执行动作后的状态"""
        pass
    
    @abstractmethod
    def predict_reward(self, state: WorldState, goal: WorldState) -> float:
        """预测状态与目标的接近程度"""
        pass
    
    @abstractmethod
    def extract_key_info(self, state: WorldState, goal: WorldState) -> str:
        """提取关键信息（用于自然语言latent space）"""
        pass


class LLMWorldModel(WorldModelInterface):
    """
    基于LLM的世界模型
    
    对标SimuRA：
    - 使用自然语言作为latent space
    - LLM模拟状态转换
    - 成本最小化选择
    """
    
    def __init__(self, llm: Any = None, config: dict = None):
        self.llm = llm
        self.config = config or {}
        self.history: list = []
    
    def simulate(self, state: WorldState, action: Action) -> WorldState:
        """使用LLM模拟状态转换"""
        if self.llm:
            prompt = self._build_simulation_prompt(state, action)
            response = self.llm.chat(prompt)
            return self._parse_simulation_response(response, state)
        
        # 简化fallback
        new_state = WorldState(
            description=f"{state.description} + {action.name}",
            attributes={**state.attributes, **action.effects}
        )
        return new_state
    
    def predict_reward(self, state: WorldState, goal: WorldState) -> float:
        """预测奖励（与目标的距离）"""
        if self.llm:
            prompt = self._build_reward_prompt(state, goal)
            response = self.llm.chat(prompt)
            try:
                return float(json.loads(response).get('distance', 0.5))
            except:
                pass
        
        # 简化fallback：计算属性距离
        distance = 0.0
        for key, goal_value in goal.attributes.items():
            if key in state.attributes:
                state_value = state.attributes[key]
                if isinstance(goal_value, (int, float)) and isinstance(state_value, (int, float)):
                    distance += abs(goal_value - state_value)
        
        return min(1.0, distance / 100.0)
    
    def extract_key_info(self, state: WorldState, goal: WorldState) -> str:
        """提取关键信息为自然语言"""
        return f"当前状态: {state.description}, 目标: {goal.description}"
    
    def _build_simulation_prompt(self, state: WorldState, action: Action) -> str:
        return f"""模拟执行动作后的世界状态：

当前状态: {state.description}
状态属性: {json.dumps(state.attributes)}
执行动作: {action.name}
动作描述: {action.description}

请JSON格式输出下一状态：
{{
    "description": "动作执行后的世界描述",
    "attributes": {{"属性": "值"}}
}}"""
    
    def _build_reward_prompt(self, state: WorldState, goal: WorldState) -> str:
        return f"""评估当前状态与目标的距离：

当前状态: {state.description}
当前属性: {json.dumps(state.attributes)}
目标状态: {goal.description}
目标属性: {json.dumps(goal.attributes)}

请输出0-1之间的距离分数（0表示已达到目标）：
{{
    "distance": 0.0-1.0,
    "reasoning": "分析理由"
}}"""
    
    def _parse_simulation_response(self, response: str, original_state: WorldState) -> WorldState:
        try:
            data = json.loads(response)
            return WorldState(
                description=data.get('description', original_state.description),
                attributes=data.get('attributes', original_state.attributes)
            )
        except:
            return original_state


class PlanningDrivenReasoning:
    """
    规划驱动推理引擎
    
    对标SimuRA架构：
    1. 输入：State + Goal
    2. LLM模拟多步轨迹
    3. 成本评估
    4. 选择最优动作
    """
    
    def __init__(self, world_model: WorldModelInterface = None, config: dict = None):
        self.world_model = world_model or LLMWorldModel()
        self.config = config or {}
        self.max_depth = self.config.get('max_depth', 5)
        self.max_trajectories = self.config.get('max_trajectories', 3)
        self.goal_threshold = self.config.get('goal_threshold', 0.1)
    
    def plan(self, current_state: WorldState, goal_state: WorldState, available_actions: list[Action]) -> Plan:
        """
        规划：找到从当前状态到目标状态的最佳动作序列
        
        Args:
            current_state: 当前世界状态
            goal_state: 目标状态
            available_actions: 可用动作列表
            
        Returns:
            Plan: 规划结果
        """
        # 1. 提取关键信息
        key_info = self.world_model.extract_key_info(current_state, goal_state)
        
        # 2. 生成多条候选轨迹
        trajectories = self._generate_trajectories(
            current_state, goal_state, available_actions
        )
        
        # 3. 评估轨迹
        for trajectory in trajectories:
            self._evaluate_trajectory(trajectory, goal_state)
        
        # 4. 选择最优
        best_trajectory = min(trajectories, key=lambda t: t.goal_distance)
        
        # 5. 选择第一个动作
        selected_action = None
        if best_trajectory.actions:
            selected_action = best_trajectory.actions[0]
        
        return Plan(
            trajectories=trajectories,
            selected_action=selected_action,
            reasoning=f"选择轨迹成本={best_trajectory.total_cost}, 目标距离={best_trajectory.goal_distance}",
            confidence=1.0 - best_trajectory.goal_distance
        )
    
    def _generate_trajectories(self, current_state: WorldState, goal_state: WorldState, 
                               actions: list[Action]) -> list[Trajectory]:
        """生成候选轨迹"""
        trajectories = []
        
        for action in actions[:self.max_trajectories]:
            trajectory = Trajectory()
            trajectory.states.append(current_state)
            
            # 模拟执行动作
            next_state = self.world_model.simulate(current_state, action)
            trajectory.states.append(next_state)
            trajectory.actions.append(action)
            trajectory.total_cost = action.cost
            
            # 检查是否达到目标
            distance = self.world_model.predict_reward(next_state, goal_state)
            trajectory.goal_distance = distance
            
            # 如果接近目标，添加更多模拟步骤
            if distance > self.goal_threshold:
                extended = self._extend_trajectory(
                    next_state, goal_state, trajectory, actions
                )
                trajectories.append(extended)
            else:
                trajectories.append(trajectory)
        
        return trajectories
    
    def _extend_trajectory(self, state: WorldState, goal_state: WorldState,
                          trajectory: Trajectory, actions: list[Action]) -> Trajectory:
        """扩展轨迹（多步模拟）"""
        current = state
        depth = 1
        
        while trajectory.goal_distance > self.goal_threshold and depth < self.max_depth:
            # 选择下一个动作（简单策略：选择cost最低的）
            best_action = min(actions, key=lambda a: a.cost)
            
            next_state = self.world_model.simulate(current, best_action)
            distance = self.world_model.predict_reward(next_state, goal_state)
            
            trajectory.states.append(next_state)
            trajectory.actions.append(best_action)
            trajectory.total_cost += best_action.cost
            trajectory.goal_distance = distance
            
            current = next_state
            depth += 1
        
        return trajectory
    
    def _evaluate_trajectory(self, trajectory: Trajectory, goal_state: WorldState):
        """评估轨迹"""
        if not trajectory.states:
            return
        
        final_state = trajectory.states[-1]
        final_distance = self.world_model.predict_reward(final_state, goal_state)
        
        trajectory.goal_distance = final_distance
        trajectory.score = 1.0 - final_distance
    
    def step(self, current_state: WorldState, goal_state: WorldState, 
             available_actions: list[Action]) -> tuple[Action, Plan]:
        """
        单步规划：返回下一步动作
        
        Returns:
            (selected_action, full_plan)
        """
        plan = self.plan(current_state, goal_state, available_actions)
        return plan.selected_action, plan


class ReactiveReasoning:
    """
    反应式推理（传统CoT方式）
    
    作为对比基线
    """
    
    def __init__(self, llm: Any = None):
        self.llm = llm
    
    def reason(self, state: WorldState, goal: WorldState, actions: list[Action]) -> Action:
        """直接推理选择动作"""
        if self.llm:
            prompt = f"""从以下动作中选择最佳动作：

当前状态: {state.description}
目标: {goal.description}
可用动作: {json.dumps([{'name': a.name, 'description': a.description} for a in actions])}

请直接输出动作名称。"""
            response = self.llm.chat(prompt)
            
            for action in actions:
                if action.name.lower() in response.lower():
                    return action
        
        return actions[0] if actions else None


# 导出
__all__ = [
    'WorldState',
    'Action',
    'Trajectory',
    'Plan',
    'PlanningState',
    'WorldModelInterface',
    'LLMWorldModel',
    'PlanningDrivenReasoning',
    'ReactiveReasoning',
]
