"""
UAS世界模型 - P2: 隐空间规划模块

功能：
- 隐空间表示学习
- 想象力训练
- 潜在空间规划
- 对标Dreamer架构
"""

import json
import uuid
import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


class LatentState:
    """隐状态"""

    def __init__(self, vector: np.ndarray = None, deterministic: np.ndarray = None):
        self.vector = vector or np.zeros(32)
        self.deterministic = deterministic or np.zeros(64)

    def __repr__(self):
        return f"LatentState(shape={self.vector.shape})"


@dataclass
class ImaginedTrajectory:
    """想象的轨迹"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    latent_states: list = field(default_factory=list)
    actions: list = field(default_factory=list)
    rewards: list = field(default_factory=list)
    total_reward: float = 0.0
    value: float = 0.0


class Encoder(ABC):
    """编码器抽象"""

    @abstractmethod
    def encode(self, observation: Any) -> LatentState:
        pass


class Decoder(ABC):
    """解码器抽象"""

    @abstractmethod
    def decode(self, latent: LatentState) -> Any:
        pass


class DynamicsModel(ABC):
    """动态模型抽象"""

    @abstractmethod
    def predict(self, latent: LatentState, action: np.ndarray) -> LatentState:
        pass


class SimpleEncoder(Encoder):
    """简化编码器（实际应使用Transformer）"""

    def __init__(
        self, input_dim: int = 512, latent_dim: int = 32, hidden_dim: int = 128
    ):
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim

        # 简化实现：随机投影
        self.projection = np.random.randn(input_dim, hidden_dim)
        self.latent_proj = np.random.randn(hidden_dim, latent_dim)

    def encode(self, observation: Any) -> LatentState:
        # 将观察转换为向量
        if isinstance(observation, str):
            obs_vector = self._text_to_vector(observation)
        elif isinstance(observation, np.ndarray):
            obs_vector = observation
        else:
            obs_vector = np.zeros(self.input_dim)

        # 简单前向
        hidden = np.tanh(obs_vector @ self.projection)
        latent_vector = hidden @ self.latent_proj
        deterministic = hidden

        return LatentState(latent_vector, deterministic)

    def _text_to_vector(self, text: str) -> np.ndarray:
        # 简化实现
        words = text.split()
        vec = np.zeros(self.input_dim)
        for i, word in enumerate(words[: min(len(words), self.input_dim)]):
            vec[i] = hash(word) % 1000 / 1000.0
        return vec


class SimpleDecoder(Decoder):
    """简化解码器"""

    def __init__(self, latent_dim: int = 32, output_dim: int = 512):
        self.latent_dim = latent_dim
        self.output_dim = output_dim
        self.reconstruction_proj = np.random.randn(latent_dim, output_dim)

    def decode(self, latent: LatentState) -> Any:
        reconstruction = latent.vector @ self.reconstruction_proj
        return reconstruction


class SimpleDynamics(DynamicsModel):
    """简化动态模型（实际应使用Transformer RSSM）"""

    def __init__(
        self, latent_dim: int = 32, action_dim: int = 10, hidden_dim: int = 64
    ):
        self.latent_dim = latent_dim
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim

        # 简化实现
        self.W_a = np.random.randn(action_dim, hidden_dim)
        self.W_s = np.random.randn(latent_dim, hidden_dim)
        self.b = np.random.randn(hidden_dim)
        self.W_h = np.random.randn(hidden_dim, latent_dim)

    def predict(self, latent: LatentState, action: np.ndarray) -> LatentState:
        # 简化RNN-style更新
        combined = latent.vector @ self.W_s + action @ self.W_a + self.b
        hidden = np.tanh(combined)
        next_vector = hidden @ self.W_h

        return LatentState(next_vector, hidden)


class RewardPredictor:
    """奖励预测器"""

    def __init__(self, latent_dim: int = 32, action_dim: int = 10):
        self.latent_dim = latent_dim
        self.W = np.random.randn(latent_dim + action_dim, 1)

    def predict(self, latent: LatentState, action: np.ndarray) -> float:
        combined = np.concatenate([latent.vector, action])
        reward = combined @ self.W
        return float(reward)


class Critic:
    """价值网络"""

    def __init__(self, latent_dim: int = 32, gamma: float = 0.99):
        self.latent_dim = latent_dim
        self.gamma = gamma
        self.W = np.random.randn(latent_dim, 1)

    def value(self, latent: LatentState) -> float:
        v = latent.vector @ self.W
        return float(v)

    def lambda_return(
        self, rewards: list[float], last_value: float, lambda_: float = 0.95
    ) -> float:
        """λ-return计算"""
        if not rewards:
            return last_value

        returns = []
        g = 0.0

        for r in reversed(rewards):
            g = r + self.gamma * ((1 - lambda_) * last_value + lambda_ * g)
            returns.insert(0, g)

        return returns[0] if returns else last_value


class Actor:
    """策略网络"""

    def __init__(self, latent_dim: int = 32, action_dim: int = 10):
        self.latent_dim = latent_dim
        self.action_dim = action_dim
        self.W = np.random.randn(latent_dim, action_dim)

    def act(self, latent: LatentState) -> np.ndarray:
        # 简化：确定性策略
        action_probs = latent.vector @ self.W
        action = np.argmax(action_probs)
        action_vec = np.zeros(self.action_dim)
        action_vec[action] = 1.0
        return action_vec


class LatentSpacePlanner:
    """
    隐空间规划器

    对标Dreamer架构：
    1. World Model: Encoder + Dynamics + Decoder + Reward
    2. Actor: 策略网络
    3. Critic: 价值网络
    4. Imagination: 在隐空间进行RL训练
    """

    def __init__(self, config: dict = None):
        self.config = config or {}

        self.latent_dim = self.config.get("latent_dim", 32)
        self.action_dim = self.config.get("action_dim", 10)
        self.imagination_horizon = self.config.get("imagination_horizon", 15)

        # 组件
        self.encoder = SimpleEncoder(latent_dim=self.latent_dim)
        self.decoder = SimpleDecoder(latent_dim=self.latent_dim)
        self.dynamics = SimpleDynamics(
            latent_dim=self.latent_dim, action_dim=self.action_dim
        )
        self.reward_predictor = RewardPredictor(
            latent_dim=self.latent_dim, action_dim=self.action_dim
        )
        self.critic = Critic(latent_dim=self.latent_dim)
        self.actor = Actor(latent_dim=self.latent_dim, action_dim=self.action_dim)

    def encode_observation(self, observation: Any) -> LatentState:
        """编码观察"""
        return self.encoder.encode(observation)

    def imagine(
        self, initial_latent: LatentState, horizon: int = None
    ) -> ImaginedTrajectory:
        """
        想象力：在隐空间模拟轨迹

        对标Dreamer的核心机制：
        - 从真实状态开始
        - 在隐空间 rollout 多个步骤
        - 使用动态模型预测下一状态
        - 累积奖励计算
        """
        horizon = horizon or self.imagination_horizon

        trajectory = ImaginedTrajectory()
        current = initial_latent

        for step in range(horizon):
            # 1. 策略选择动作
            action = self.actor.act(current)

            # 2. 动态模型预测下一状态
            next_latent = self.dynamics.predict(current, action)

            # 3. 奖励预测
            reward = self.reward_predictor.predict(current, action)

            # 4. 记录
            trajectory.latent_states.append(current)
            trajectory.actions.append(action)
            trajectory.rewards.append(reward)
            trajectory.total_reward += reward

            current = next_latent

        # 5. 计算价值
        final_value = self.critic.value(current)
        trajectory.value = self.critic.lambda_return(trajectory.rewards, final_value)

        return trajectory

    def optimize_policy(
        self, initial_latent: LatentState, n_rollouts: int = 10
    ) -> np.ndarray:
        """
        策略优化

        简化实现：
        - 多次想象 rollout
        - 选择平均价值最高的动作
        """
        action_values = {i: 0.0 for i in range(self.action_dim)}

        # 尝试每个动作
        for action_idx in range(self.action_dim):
            action_vec = np.zeros(self.action_dim)
            action_vec[action_idx] = 1.0

            # 模拟
            current = initial_latent
            total_reward = 0.0

            for step in range(self.imagination_horizon):
                reward = self.reward_predictor.predict(current, action_vec)
                total_reward += reward
                current = self.dynamics.predict(current, action_vec)

            action_values[action_idx] = total_reward

        # 选择最佳动作
        best_action = max(action_values.items(), key=lambda x: x[1])
        best_vec = np.zeros(self.action_dim)
        best_vec[best_action[0]] = 1.0

        return best_vec

    def step(self, observation: Any, action_dim: int = None) -> np.ndarray:
        """
        单步执行

        1. 编码观察
        2. 策略优化
        3. 返回动作
        """
        action_dim = action_dim or self.action_dim

        # 编码
        latent = self.encode_observation(observation)

        # 规划
        action = self.optimize_policy(latent)

        return action

    def learn(self, batch: list):
        """
        学习更新（简化版）

        实际Dreamer使用：
        - MSE loss: 重建观察
        - MSE loss: 预测奖励
        - RL loss: 策略梯度
        """
        # TODO: 实现完整的Dreamer训练
        pass

    def to_dict(self) -> dict:
        """导出配置"""
        return {
            "latent_dim": self.latent_dim,
            "action_dim": self.action_dim,
            "imagination_horizon": self.imagination_horizon,
        }


class HybridPlanner:
    """
    混合规划器（结合规划驱动 + 隐空间）

    根据任务选择合适的规划方式：
    - 短程任务: 规划驱动（SimuRA）
    - 长程任务: 隐空间规划（Dreamer）
    """

    def __init__(
        self, planning_engine=None, latent_planner: "LatentSpacePlanner" = None
    ):
        self.planning_engine = planning_engine
        self.latent_planner = latent_planner
        self.task_complexity_threshold = 5

    def plan(self, task: dict, context: dict) -> Any:
        """智能选择规划方式"""
        complexity = self._estimate_complexity(task)

        if complexity < self.task_complexity_threshold:
            # 使用规划驱动
            return self.planning_engine.plan(
                context.get("state"), context.get("goal"), context.get("actions")
            )
        else:
            # 使用隐空间规划
            return self.latent_planner.optimize_policy(context.get("observation"))

    def _estimate_complexity(self, task: dict) -> int:
        """估计任务复杂度"""
        horizon = task.get("horizon", 1)
        actions = len(task.get("available_actions", []))

        return horizon * actions


# 导出
__all__ = [
    "LatentState",
    "ImaginedTrajectory",
    "Encoder",
    "Decoder",
    "DynamicsModel",
    "SimpleEncoder",
    "SimpleDecoder",
    "SimpleDynamics",
    "RewardPredictor",
    "Critic",
    "Actor",
    "LatentSpacePlanner",
    "HybridPlanner",
]
